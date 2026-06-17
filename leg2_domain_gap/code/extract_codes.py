#!/usr/bin/env python3
"""Leg-2 DEEPSTRAIN side — extract the 64-d tone-count Embed code on SIM vs REAL.

Run with the ringdown venv (has torch + sbilib deps, no gwpy needed at import):
    /Users/sumit/Github/BlackHole/ringdown_spectroscopy/.venv/bin/python extract_codes.py

BRIDGE code. Imports deepstrain `sbilib` READ-ONLY and loads its trained checkpoints
read-only; it does not modify the BlackHole repo. The batch-building logic is copied
from `ringdown_spectroscopy/scripts/11_tonecount.py` (make_batch / make_batch_real /
norm_seg / ToneCounter) so we reproduce the model's exact input convention without
importing that script (which pulls gwpy). Provenance noted at each copied block.

Writes, per checkpoint, `results/codes_<ckpt>.npz` containing ONLY:
  code_sim, code_real   (n, 64) Embed codes
  y_sim, y_real         tone label (0=1-tone, 1=2-tone)   -- the INVARIANT
  osnr_sim, osnr_real   overtone matched-filter SNR        -- the INVARIANT (continuous)
  loud_sim, loud_real   pre-norm segment RMS               -- the SHORTCUT (loudness)
The tabula-side probe (probe_ladder.py) reads only these arrays.
"""
import sys
from pathlib import Path

import numpy as np
import torch

RING = "/Users/sumit/Github/BlackHole/ringdown_spectroscopy"
sys.path.insert(0, RING + "/scripts")
import sbilib  # READ-ONLY  (numpy/torch/rdlib only; no gwpy at import)
from sbilib import Embed, N_SAMP, simulate_tonecount

MODELS = Path(RING) / "models"
NOISE_POOL = Path(RING) / "data" / "o4_noise_pool.npz"   # cached REAL O4 whitened noise
OUT = Path(__file__).resolve().parent.parent / "results"
OUT.mkdir(exist_ok=True)

AMP_FRAC = (0.1, 1.5)
N_EVAL = 4000
CHECKPOINTS = ["11_tonecount", "11_tonecount_norm", "11_tonecount_realnoise",
               "11_tonecount_matched"]


class ToneCounter(torch.nn.Module):
    """COPIED from 11_tonecount.py (read-only provenance): Embed CNN -> scalar logit."""

    def __init__(self):
        super().__init__()
        self.embed = Embed(n_out=64)
        self.head = torch.nn.Sequential(torch.nn.ReLU(), torch.nn.Linear(64, 1))

    def forward(self, x):
        return self.head(self.embed(x)).squeeze(-1)


def norm_seg(seg):
    """COPIED from 11_tonecount.py (fix A): per-detector unit-std normalization."""
    s = seg.std(axis=-1, keepdims=True)
    return (seg / np.where(s > 0, s, 1.0)).astype(np.float32)


def make_eval_batch(n, rng, real_noise=None):
    """Balanced 1/2-tone eval set, SNR-matched so loudness does NOT trivially predict the
    label (clean probing). real_noise=None -> SIM (idealized white noise); else inject into
    REAL O4 whitened-noise windows (logic from 11_tonecount.make_batch_real). Returns
    (x_normed (n, 2*N_SAMP), y, osnr, loudness=pre-norm RMS)."""
    x = np.empty((n, 2 * N_SAMP), dtype=np.float32)
    y = np.empty(n, dtype=np.float32)
    osnr = np.empty(n, dtype=np.float32)
    loud = np.empty(n, dtype=np.float32)
    if real_noise is not None:
        H1, L1 = real_noise["H1"], real_noise["L1"]
        Lh, Ll = len(H1), len(L1)
    for k in range(n):
        m, c = rng.uniform(40, 120), rng.uniform(0.05, 0.95)
        two = k % 2 == 1
        frac = rng.uniform(*AMP_FRAC) if two else 0.0
        if real_noise is not None:
            oh = int(rng.integers(0, Lh - N_SAMP)); ol = int(rng.integers(0, Ll - N_SAMP))
            nz = np.stack([H1[oh:oh + N_SAMP], L1[ol:ol + N_SAMP]])
            seg, s = simulate_tonecount(m, c, 2 if two else 1, frac, rng, noise=nz, snr_match=True)
        else:
            seg, s = simulate_tonecount(m, c, 2 if two else 1, frac, rng, snr_match=True)
        loud[k] = float(seg.std())                 # pre-norm loudness (the shortcut)
        x[k] = norm_seg(seg).reshape(-1)
        y[k] = 1.0 if two else 0.0
        osnr[k] = s
    return x, y, osnr, loud


def load_model(ckpt):
    """Instantiate, materialize LazyLinear via a dummy forward, then load state_dict."""
    model = ToneCounter()
    with torch.no_grad():
        model(torch.zeros(1, 2 * N_SAMP))          # materialize LazyLinear shapes
    state = torch.load(MODELS / f"{ckpt}.pt", map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return model


def embed_codes(model, x):
    with torch.no_grad():
        return model.embed(torch.from_numpy(x)).numpy()


def model_logit(model, x):
    """The model's own P(2-tone) logit -- the transfer-outcome axis (its real-noise AUC)."""
    with torch.no_grad():
        return model(torch.from_numpy(x)).numpy()


def main():
    pool = np.load(NOISE_POOL)
    real_noise = {"H1": pool["H1"], "L1": pool["L1"]}
    print(f"REAL O4 noise pool: H1 {len(real_noise['H1'])}, L1 {len(real_noise['L1'])} samp")
    for ckpt in CHECKPOINTS:
        if not (MODELS / f"{ckpt}.pt").exists():
            print(f"  {ckpt}: MISSING, skip"); continue
        try:
            model = load_model(ckpt)
        except Exception as e:
            print(f"  {ckpt}: load FAILED ({e}); skip"); continue
        rng = np.random.default_rng(20260617)
        xs, ys, os_, ls = make_eval_batch(N_EVAL, rng)                       # SIM
        xr, yr, orr, lr = make_eval_batch(N_EVAL, rng, real_noise=real_noise)  # REAL
        out = OUT / f"codes_{ckpt}.npz"
        np.savez(out,
                 code_sim=embed_codes(model, xs), y_sim=ys, osnr_sim=os_, loud_sim=ls,
                 logit_sim=model_logit(model, xs),
                 code_real=embed_codes(model, xr), y_real=yr, osnr_real=orr, loud_real=lr,
                 logit_real=model_logit(model, xr))
        print(f"  {ckpt}: wrote {out.name}  (sim/real codes {N_EVAL}x64)")
    print("done.")


if __name__ == "__main__":
    main()
