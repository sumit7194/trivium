#!/usr/bin/env python3
"""Leg L (A6) — extract the no-hair NPE's summary code (deepstrain venv).

    /Users/sumit/Github/BlackHole/ringdown_spectroscopy/.venv/bin/python export_nohair_codes.py

leg 2 found the deepstrain TONE-COUNT model is information-limited (no legibility/scramble signature).
A6 asks the flagged follow-up: does the *richer-information* no-hair δ SBI (the amortized NPE that infers
M, χ, δ from the full ringdown) encode δ legibly, or is δ buried nonlinearly (a scramble signature)? This
extracts the NPE's 56-d Embed summary code on simulated ringdowns with known (M, χ, δ), so stage 2 can run
the legibility probe ladder. Imports deepstrain sbilib + the trained posterior READ-ONLY.
"""
import sys
from pathlib import Path

import numpy as np
import torch

DS = "/Users/sumit/Github/BlackHole/ringdown_spectroscopy"
sys.path.insert(0, f"{DS}/scripts")
import sbilib
from sbilib import Embed, simulate                      # noqa: F401  (Embed load-bearing for unpickle)

OUT = Path(__file__).resolve().parent.parent / "results"
N = 5000


def main():
    post = torch.load(f"{DS}/results/09_posterior_150k.pt", weights_only=False)
    emb = post.posterior_estimator.embedding_net
    emb.eval()

    rng = np.random.default_rng(0)
    sim_rng = np.random.default_rng(1)
    thetas = np.column_stack([rng.uniform(40, 120, N), rng.uniform(0.05, 0.95, N),
                              rng.uniform(-0.5, 0.5, N)]).astype(np.float32)
    xs = np.empty((N, 2 * sbilib.N_SAMP), dtype=np.float32)
    for k, (m, c, d) in enumerate(thetas):
        xs[k] = simulate(float(m), float(c), float(d), sim_rng).reshape(-1)

    codes = []
    with torch.no_grad():
        for i in range(0, N, 500):
            codes.append(emb(torch.tensor(xs[i:i + 500])).cpu().numpy())
    codes = np.concatenate(codes, 0)
    print(f"  extracted {codes.shape[0]} codes, dim {codes.shape[1]} (Embed n_out); θ=(M,χ,δ)")

    OUT.mkdir(exist_ok=True)
    np.savez(OUT / "nohair_codes.npz", codes=codes.astype(np.float32), thetas=thetas,
             param_names=np.array(["M", "chi", "delta"]))
    print(f"  wrote results/nohair_codes.npz")


if __name__ == "__main__":
    main()
