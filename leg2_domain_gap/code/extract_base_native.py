#!/usr/bin/env python3
"""Leg 2 (A8) — the base tone-count model in its NATIVE convention (deepstrain venv).

    /Users/sumit/Github/BlackHole/ringdown_spectroscopy/.venv/bin/python extract_base_native.py

leg 2 fed every checkpoint norm_seg (unit-std) input AND snr_match=True — both of which REMOVE the loudness
cue, so the base model's loudness shortcut (P4) was never probed where it lives. The base model was trained
PRE-norm. This extracts its 64-d Embed code on its NATIVE input — un-normalized, NOT SNR-matched — where
2-tone signals are genuinely louder (the 221 adds energy), so loudness is a real cue. Records the tone label
and the pre-norm loudness so stage 2 can ask: does the base model lean on the loudness shortcut natively?
Imports deepstrain sbilib + the base checkpoint read-only.
"""
import sys
from pathlib import Path

import numpy as np
import torch

RING = "/Users/sumit/Github/BlackHole/ringdown_spectroscopy"
sys.path.insert(0, f"{RING}/scripts")
from sbilib import Embed, N_SAMP, simulate_tonecount     # noqa: F401

OUT = Path(__file__).resolve().parent.parent / "results"
AMP_FRAC = (0.1, 0.5)
N = 4000


class ToneCounter(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = Embed(n_out=64)
        self.head = torch.nn.Sequential(torch.nn.ReLU(), torch.nn.Linear(64, 1))

    def forward(self, x):
        return self.head(self.embed(x)).squeeze(-1)


def main():
    model = ToneCounter()
    with torch.no_grad():
        model(torch.zeros(1, 2 * N_SAMP))                  # materialize LazyLinear
    model.load_state_dict(torch.load(f"{RING}/models/11_tonecount.pt", map_location="cpu"))
    model.eval()

    rng = np.random.default_rng(0)
    X = np.empty((N, 2 * N_SAMP), dtype=np.float32)
    y = np.empty(N); loud = np.empty(N)
    for k in range(N):
        m, c = rng.uniform(40, 120), rng.uniform(0.05, 0.95)
        two = k % 2 == 1
        frac = rng.uniform(*AMP_FRAC) if two else 0.0
        seg, _ = simulate_tonecount(m, c, 2 if two else 1, frac, rng, snr_match=False)  # NATIVE: not matched
        X[k] = seg.reshape(-1)                              # NATIVE: un-normalized (no norm_seg)
        y[k] = 1.0 if two else 0.0
        loud[k] = float(seg.std())                          # pre-norm loudness (the shortcut)

    with torch.no_grad():
        codes = []
        for i in range(0, N, 500):
            codes.append(model.embed(torch.tensor(X[i:i + 500])).cpu().numpy())
        codes = np.concatenate(codes, 0)

    # quick shortcut-existence check (no model): does raw loudness predict the tone label?
    two_loud = loud[y == 1].mean(); one_loud = loud[y == 0].mean()
    print(f"  native regime: 2-tone mean loudness {two_loud:.3f} vs 1-tone {one_loud:.3f} "
          f"→ loudness {'IS' if abs(two_loud-one_loud)/one_loud > 0.05 else 'is NOT'} a cue for the tone label")
    print(f"  extracted {codes.shape[0]} base-model codes (dim {codes.shape[1]}), native un-normalized input")

    OUT.mkdir(exist_ok=True)
    np.savez(OUT / "base_native_codes.npz", codes=codes.astype(np.float32), y=y, loud=loud)
    print(f"  wrote results/base_native_codes.npz")


if __name__ == "__main__":
    main()
