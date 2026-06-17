#!/usr/bin/env python3
"""phase_shift_resolution.py

Generates Locked Kerr ringdown waveforms, applies FFT magnitude and Hilbert envelope transformations,
and sweeps autoencoder bottlenecks to resolve the intrinsic parameter dimension.
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn
from scipy.signal import hilbert

# Insert BlackHole scripts path to import rdlib
sys.path.insert(0, "/Users/sumit/Github/BlackHole/ringdown_spectroscopy/scripts")
import rdlib

FS = 4096.0
SEG = 0.04
N_SAMP = int(SEG * FS)
N_SAMP += N_SAMP % 2  # 164 samples
N_TRAIN = 8000
DIMS = (0, 1, 2, 3, 4, 5)
SEEDS = (0, 1, 2)
STEPS = 4000
BATCH = 512
WHITEN_FLOOR = 1e-6

# Load Kerr mapping
kerr220 = rdlib.KerrMap(2, 2, 0)
kerr221 = rdlib.KerrMap(2, 2, 1)

CHI_GRID = np.linspace(0.01, 0.97, 200)
W220 = np.array([kerr220.f_tau(1.0, c) for c in CHI_GRID])
W221 = np.array([kerr221.f_tau(1.0, c) for c in CHI_GRID])

def get_freq_tau(mass, chi):
    i = np.searchsorted(CHI_GRID, chi)
    i = min(max(i, 0), len(CHI_GRID) - 1)
    f1, tau1 = W220[i][0] / mass, W220[i][1] * mass
    f2, tau2 = W221[i][0] / mass, W221[i][1] * mass
    return f1, tau1, f2, tau2

class AE(nn.Module):
    def __init__(self, m: int, d: int):
        super().__init__()
        self.d = d
        self.enc = nn.Sequential(
            nn.Linear(m, 128), nn.Tanh(), nn.Linear(128, 64), nn.Tanh(),
            nn.Linear(64, max(d, 1)),
        )
        self.dec = nn.Sequential(
            nn.Linear(max(d, 1), 64), nn.Tanh(), nn.Linear(64, 128), nn.Tanh(),
            nn.Linear(128, m),
        )

    def forward(self, x):
        if self.d == 0:
            code = torch.zeros(x.shape[0], 1, device=x.device)
        else:
            code = self.enc(x)
        return self.dec(code)

def r2(model, Xte):
    device = next(model.parameters()).device
    model.eval()
    with torch.no_grad():
        pred = model(torch.from_numpy(Xte).to(device)).cpu().numpy()
    sse = ((pred - Xte) ** 2).sum()
    sst = ((Xte - Xte.mean(0)) ** 2).sum()
    return 1.0 - sse / sst if sst > 0 else 1.0

def train_ae(Xtr, Xte, d, seed):
    torch.manual_seed(1000 + 17 * d + seed)
    device = torch.device("cpu")
    m = Xtr.shape[1]
    model = AE(m, d).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.MSELoss()
    Xt = torch.from_numpy(Xtr).to(device)
    rng = np.random.default_rng(seed)
    for _ in range(STEPS):
        idx = rng.integers(0, Xtr.shape[0], BATCH)
        xb = Xt[idx]
        opt.zero_grad()
        loss = lossf(model(xb), xb)
        loss.backward()
        opt.step()
    return r2(model, Xte)

def prep(X, n_train):
    Xtr_raw, Xte_raw = X[:n_train], X[n_train:]
    mu, sd = Xtr_raw.mean(0), Xtr_raw.std(0)
    keep = sd > 1e-7
    if keep.sum() == 0:
        return None
    
    std = lambda A: ((A[:, keep] - mu[keep]) / sd[keep]).astype(np.float32)
    Xtr_s, Xte_s = std(Xtr_raw), std(Xte_raw)
    
    # PCA Whitening on train standardized
    cov = np.cov(Xtr_s, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    
    kept = eigvals / max(eigvals[0], 1e-9) > WHITEN_FLOOR
    comps = eigvecs[:, kept].T
    scale = np.sqrt(eigvals[kept])
    scale = np.clip(scale, 1e-9, None)
    
    white = lambda A: (((A - Xtr_s.mean(0)) @ comps.T) / scale).astype(np.float32)
    return {
        "std": (Xtr_s, Xte_s),
        "white": (white(Xtr_s), white(Xte_s)),
        "linear_spectrum": (eigvals / eigvals.sum()).round(5).tolist(),
        "n_linear_kept": int(kept.sum()),
        "n_features": int(keep.sum()),
    }

def main():
    t = np.arange(N_SAMP) / FS
    t0 = 0.0
    
    families = ["locked", "free"]
    report = {}
    
    for family in families:
        print(f"\n========================================")
        print(f"Generating and training for family: {family.upper()}")
        print(f"========================================")
        
        # Reset RNG per family to ensure identical parameter distributions (mass, chi)
        rng_param = np.random.default_rng(42)
        masses = rng_param.uniform(40, 120, N_TRAIN)
        chis = rng_param.uniform(0.05, 0.95, N_TRAIN)
        
        # For free family, we use a separate RNG for relative amplitude/phase to keep masses/chis identical
        rng_free = np.random.default_rng(2026)
        
        raw_obs = np.zeros((N_TRAIN, 2 * N_SAMP), dtype=np.float32)
        fft_obs = np.zeros((N_TRAIN, 2 * (N_SAMP // 2 + 1)), dtype=np.float32)
        env_obs = np.zeros((N_TRAIN, 2 * N_SAMP), dtype=np.float32)
        
        for k in range(N_TRAIN):
            f1, tau1, f2, tau2 = get_freq_tau(masses[k], chis[k])
            
            if family == "locked":
                amp1 = 5.0
                amp2 = 4.0
                phi2 = 0.0
            else:
                amp1 = 5.0
                amp2 = amp1 * rng_free.uniform(0.2, 1.5)
                phi2 = rng_free.uniform(-np.pi, np.pi)
                
            params = [
                dict(f=f1, tau=tau1, amp=amp1, phi=0.0),
                dict(f=f2, tau=tau2, amp=amp2, phi=phi2),
            ]
            x1 = rdlib.damped_sinusoids(t, t0, params)
            x2 = rdlib.damped_sinusoids(t, t0, params)
            
            # 1. Baseline: Raw time domain
            raw_obs[k] = np.concatenate([x1, x2])
            
            # 2. FFT Magnitude
            X1 = np.abs(np.fft.rfft(x1))
            X2 = np.abs(np.fft.rfft(x2))
            fft_obs[k] = np.concatenate([X1, X2])
            
            # 3. Hilbert Envelope
            env1 = np.abs(hilbert(x1))
            env2 = np.abs(hilbert(x2))
            env_obs[k] = np.concatenate([env1, env2])
            
        representations = {
            "baseline": raw_obs,
            "fft_magnitude": fft_obs,
            "hilbert_envelope": env_obs
        }
        
        family_report = {}
        n_train = int(N_TRAIN * 0.9)
        
        for key, X in representations.items():
            print(f"\nProcessing representation: {key} (shape={X.shape})")
            p = prep(X.astype(np.float64), n_train)
            if p is None:
                continue
                
            res = {
                "linear_spectrum": p["linear_spectrum"],
                "n_linear_kept": p["n_linear_kept"],
                "n_features": p["n_features"],
                "std_R2": {},
                "white_R2": {}
            }
            
            for space in ("std", "white"):
                Xtr, Xte = p[space]
                res[f"{space}_R2"] = {}
                for d in DIMS:
                    vals = [train_ae(Xtr, Xte, d, s) for s in SEEDS]
                    res[f"{space}_R2"][str(d)] = [float(np.mean(vals)), float(np.std(vals))]
                    
            family_report[key] = res
            row = "  ".join(f"d{d}:{res['white_R2'][str(d)][0]:.4f}" for d in DIMS)
            print(f"  white R²(d): {row}")
            
        report[family] = family_report
        
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "leg7b_phase_shift_results.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"\nSaved Leg 7b results to {out_path}")

if __name__ == "__main__":
    main()
