#!/usr/bin/env python3
"""Leg 5c — Integrability Fingerprints.

Derives exact 3D massive geodesic equations in Kerr and deformed Kerr spacetimes,
integrates them, computes Carter constant conservation statistics, and runs
the autoencoder bottleneck sweep to count the intrinsic dimensionality (2 vs 3).
"""

import json
import os
import sys
import time
from pathlib import Path
import numpy as np
import sympy as sp
import torch
from torch import nn

# Add conjecture_machine scripts for Geometry
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from gr_engine import Geometry, R_SYM

# Hyperparameters
DLAMBDA = 0.05
STEPS = 6000
N_TRAJECTORIES = 5
AE_STEPS = 4000
BATCH = 512
WHITEN_FLOOR = 1e-7
DIMS = (0, 1, 2, 3, 4)
SEEDS = (0, 1, 2)

RESULTS = Path(__file__).resolve().parent.parent.parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def build_geodesic_integrator(epsilon, a_val=0.5):
    """Symbolically compute Christoffel symbols and return numeric functions for derivatives and Carter constant."""
    t, u, ph = sp.symbols("t u phi", real=True)
    coords = [t, R_SYM, u, ph]
    
    # Boyier-Lindquist style metric
    D = sp.Symbol("Delta")
    a_sym = sp.Symbol("a", positive=True)
    s2 = 1 - u**2
    Sig = R_SYM**2 + a_sym**2 * u**2

    g = sp.zeros(4, 4)
    g[0, 0] = -(D - a_sym**2 * s2) / Sig
    g[0, 3] = g[3, 0] = -a_sym * s2 * (R_SYM**2 + a_sym**2 - D) / Sig
    g[1, 1] = Sig / D
    g[2, 2] = Sig / s2
    g[3, 3] = s2 * ((R_SYM**2 + a_sym**2)**2 - D * a_sym**2 * s2) / Sig

    M_sym = sp.Symbol("M", positive=True)
    # Delta_deformed = r^2 - 2*M*r + a^2 + epsilon * M^2 * u^2
    Delta_def = R_SYM**2 - 2*M_sym*R_SYM + a_sym**2 + epsilon * M_sym**2 * u**2
    g_num = g.subs(D, Delta_def).subs({M_sym: 1.0, a_sym: a_val})

    geo = Geometry(g_num, coords)
    Gamma = geo.christoffel

    # Lambdify Christoffel symbols
    gamma_func = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(b, 4):
                expr = Gamma[a][b][c]
                gamma_func[a][b][c] = sp.lambdify((R_SYM, u), expr, "numpy") if expr != 0 else (lambda r_val, u_val: 0.0)
                gamma_func[a][c][b] = gamma_func[a][b][c]

    # Lambdify metric components
    g_func = {}
    for i in range(4):
        for j in range(4):
            g_func[(i, j)] = sp.lambdify((R_SYM, u), g_num[i, j], "numpy") if g_num[i, j] != 0 else (lambda r_val, u_val: 0.0)

    def derivs(state):
        r_val = state[1]
        u_val = state[2]
        v = state[4:8]
        dxdl = v
        dvdl = np.zeros(4)
        for a in range(4):
            val = 0.0
            for b in range(4):
                for c in range(4):
                    gam = gamma_func[a][b][c](r_val, u_val)
                    val += gam * v[b] * v[c]
            dvdl[a] = -val
        return np.concatenate([dxdl, dvdl])

    def carter(state, mu2=1.0):
        r_val = state[1]
        u_val = state[2]
        v = state[4:8]
        
        gtt_val = g_func[(0, 0)](r_val, u_val)
        gtp_val = g_func[(0, 3)](r_val, u_val)
        gpp_val = g_func[(3, 3)](r_val, u_val)
        guu_val = g_func[(2, 2)](r_val, u_val)
        
        E = -(gtt_val * v[0] + gtp_val * v[3])
        Lz = gtp_val * v[0] + gpp_val * v[3]
        pu = guu_val * v[2]
        
        ptheta2 = (1.0 - u_val**2) * pu**2
        K = ptheta2 + u_val**2 * (a_val**2 * (mu2 - E**2) + Lz**2 / (1.0 - u_val**2 + 1e-9))
        return K

    return derivs, carter, g_func


def generate_trajectories(epsilon, derivs_fn, carter_fn, g_func, r0=12.0, a_val=0.5):
    """Integrate a single long massive geodesic, returning dataset and Carter constant stats."""
    X = []
    K_all = []
    
    r_hor = 1.0 + np.sqrt(1.0 - a_val**2)
    
    # Launch at r0, u0=0, phi0=0
    u0 = 0.0
    phi0 = 0.0
    vr0 = 0.0
    vu0 = 0.05
    vphi0 = 0.04
    
    # Calculate vt0
    gtt = g_func[(0, 0)](r0, u0)
    gtp = g_func[(0, 3)](r0, u0)
    gpp = g_func[(3, 3)](r0, u0)
    grr = g_func[(1, 1)](r0, u0)
    guu = g_func[(2, 2)](r0, u0)

    A = gtt
    B = 2.0 * gtp * vphi0
    C = gpp * vphi0**2 + grr * vr0**2 + guu * vu0**2 + 1.0

    disc = B**2 - 4.0 * A * C
    if disc < 0:
        raise ValueError("Initial velocity is not timelike!")
    vt0 = (-B - np.sqrt(disc)) / (2.0 * A)

    state = np.array([0.0, r0, u0, phi0, vt0, vr0, vu0, vphi0])
    
    # We want 30,000 steps total for the single trajectory
    for _ in range(30000):
        r_val = state[1]
        u_val = state[2]
        
        # Singularities / horizon check
        if r_val < r_hor + 0.1 or abs(u_val) >= 0.99 or not np.isfinite(state).all():
            break
            
        # Momenta computation
        grr_val = g_func[(1, 1)](r_val, u_val)
        guu_val = g_func[(2, 2)](r_val, u_val)
        
        p_r = grr_val * state[5]
        p_u = guu_val * state[6]
        
        X.append([r_val, u_val, p_r, p_u])
        K_all.append(carter_fn(state))
        
        # RK4
        k1 = derivs_fn(state)
        k2 = derivs_fn(state + 0.5 * DLAMBDA * k1)
        k3 = derivs_fn(state + 0.5 * DLAMBDA * k2)
        k4 = derivs_fn(state + DLAMBDA * k3)
        state += (DLAMBDA / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
    X = np.array(X, dtype=np.float32)
    K_double = np.array(K_all, dtype=np.float64)
    K_mean = K_double.mean()
    K_std = K_double.std()
    K_all = K_double.astype(np.float32)
    return X, K_all, K_mean, K_std


# ---- tabula Autoencoder counting machinery ----

class AE(nn.Module):
    def __init__(self, m: int, d: int):
        super().__init__()
        self.d = d
        self.enc = nn.Sequential(
            nn.Linear(m, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, max(d, 1)),
        )
        self.dec = nn.Sequential(
            nn.Linear(max(d, 1), 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, m),
        )

    def forward(self, x):
        if self.d == 0:
            code = torch.zeros(x.shape[0], 1)
        else:
            code = self.enc(x)
        return self.dec(code)


def r2(model, Xte):
    with torch.no_grad():
        pred = model(torch.from_numpy(Xte)).numpy()
    sse = ((pred - Xte) ** 2).sum()
    sst = ((Xte - Xte.mean(0)) ** 2).sum()
    return 1.0 - sse / sst if sst > 0 else 1.0


def train_ae(Xtr, Xte, d, seed):
    torch.manual_seed(1000 + 17 * d + seed)
    m = Xtr.shape[1]
    model = AE(m, d)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.MSELoss()
    Xt = torch.from_numpy(Xtr)
    rng = np.random.default_rng(seed)
    for _ in range(AE_STEPS):
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
    keep = sd > 1e-9
    std = lambda A: ((A[:, keep] - mu[keep]) / sd[keep]).astype(np.float32)
    Xtr_s, Xte_s = std(Xtr_raw), std(Xte_raw)
    U, S, Vt = np.linalg.svd(Xtr_s - Xtr_s.mean(0), full_matrices=False)
    var = S ** 2
    kept = var / var.max() > WHITEN_FLOOR
    comps = Vt[kept]
    scale = S[kept] / np.sqrt(len(Xtr_s))
    white = lambda A: (((A - Xtr_s.mean(0)) @ comps.T) / scale).astype(np.float32)
    return {
        "std": (Xtr_s, Xte_s),
        "white": (white(Xtr_s), white(Xte_s)),
        "n_linear_kept": int(kept.sum()),
        "n_features": int(keep.sum()),
    }


def count_dim(white_R2, dims):
    count = 0
    for d in dims:
        if d == 0:
            continue
        gain = white_R2[d][0] - white_R2[d-1][0]
        if gain > 0.02:
            count += 1
    return count


def main():
    print("RUNNING LEG 5c: INTEGRABILITY FINGERPRINTS STUDY\n")
    
    spacetimes = [
        ("kerr", 0.0),
        ("deformed", 0.1)
    ]
    
    report = {}
    
    for name, eps in spacetimes:
        print(f"\n========================================")
        print(f"SPACETIME: {name.upper()} (epsilon = {eps})")
        print(f"========================================")
        
        t0 = time.time()
        derivs_fn, carter_fn, g_func = build_geodesic_integrator(eps)
        print(f"  derived Christoffel symbols symbolically in {time.time()-t0:.1f}s")
        
        X, K, K_mean, K_std = generate_trajectories(eps, derivs_fn, carter_fn, g_func)
        print(f"  integrated 1 trajectory, collected {len(X)} coordinates")
        print(f"  Carter constant conservation:")
        print(f"    mean value: {K_mean:.6f}")
        print(f"    std dev:    {K_std:.2e}  (ratio std/mean: {K_std/K_mean:.2e})")
        
        # Save observations
        npz_path = RESULTS / f"obs_integrability_{name}.npz"
        n_train = int(len(X) * 0.8)
        
        # Shuffle X randomly to prevent chronological OOD split issues
        rng_shuffle = np.random.default_rng(42)
        shuffled_idx = rng_shuffle.permutation(len(X))
        X_shuffled = X[shuffled_idx]
        
        np.savez(npz_path, X=X_shuffled, n_train=n_train, K_mean=K_mean, K_std=K_std)
        
        p = prep(X_shuffled, n_train)
        res = {"std_R2": {}, "white_R2": {}, "n_features": p["n_features"], "n_linear_kept": p["n_linear_kept"]}
        
        for space in ("std", "white"):
            Xtr, Xte = p[space]
            for d in DIMS:
                vals = [train_ae(Xtr, Xte, d, s) for s in SEEDS]
                res[f"{space}_R2"][d] = [float(np.mean(vals)), float(np.std(vals))]
                
        res["count"] = count_dim(res["white_R2"], DIMS)
        print(f"  tabula dimension count:")
        for space in ("std", "white"):
            row = "  ".join(f"d{d}:{res[f'{space}_R2'][d][0]:.4f}" for d in DIMS)
            print(f"    {space:5s} R²(d):  {row}")
        print(f"    → count = {res['count']}")
        
        report[name] = {
            "epsilon": eps,
            "carter_mean": float(K_mean),
            "carter_std": float(K_std),
            "n_points": len(X),
            "std_R2": res["std_R2"],
            "white_R2": res["white_R2"],
            "count": res["count"]
        }
        
    out_path = RESULTS / "leg5c_integrability_results.json"
    out_path.write_text(json.dumps(report, indent=2))
    print(f"\nWrote results to {out_path}")


if __name__ == "__main__":
    main()
