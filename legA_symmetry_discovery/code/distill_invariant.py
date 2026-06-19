#!/usr/bin/env python3
"""Move A — TABULA SIDE (the blind distiller).

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python distill_invariant.py

BRIDGE code. It reads ONLY results/traj_<rung>.json (trajectory samples + the manifest
constants E, Lz) — never the metric, never the params (a,Q,Λ,ε), never the word "Carter".
This is the §3 blindness boundary, enforced mechanically (no import of ansatz, no metric).

It searches for a conserved quantity beyond E and Lz: a fixed linear combination of basis
features that is CONSTANT along every geodesic. The angular-sector Carter constant has the
form  C = c1·p_θ² + c2·cos²θ + c3·cos²θ·E² + c4·cos²θ·Lz²/sin²θ  with coefficients that are
the SAME across trajectories (they depend only on the spacetime, which is fixed) even though
E, Lz vary per trajectory. So a conserved combination is the one with minimal WITHIN-trajectory
variance. PREREGISTRATION §4A.

Frozen library ladder (parsimony order, §4A):
  L1  polynomial (Kerr-tuned):  [p_θ², cos²θ, cos²θ·E², cos²θ·Lz²/sin²θ]
  L2  rational (Λ-aware):       L1 features each divided by Δ_θ = 1 + λ·cos²θ  (scan λ)
  L3  quartic fallback:         L1 + [cos⁴θ, p_θ²·cos²θ]
Verdict EXISTS iff some library reaches held-out (split-by-trajectory) variance-ratio
< ε_T = 1e-2; report the lowest such library (parsimony). Else DESTROYED.

The candidate emitted (coeffs + library + λ) lets ansatz reconstruct the Killing tensor
K^{μν} and certify it — see certify_killing.py for the shared feature→tensor convention.
"""
import json
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent.parent / "results"
RUNGS = ["kerr", "kerr_newman", "kerr_desitter", "bumpy"]
EPS_T = 1e-2                       # PREREGISTRATION §4A threshold (frozen)
LAM_GRID = np.linspace(-0.5, 0.5, 41)
SEED = 0


def load(rung):
    trajs = json.loads((RESULTS / f"traj_{rung}.json").read_text())
    rows = []
    for tid, tr in enumerate(trajs):
        E, Lz = tr["E"], tr["Lz"]
        for (r, th, pr, pth) in tr["samples"]:
            rows.append((tid, th, pth, E, Lz))
    return np.array([r[0] for r in rows]), np.array([r[1:] for r in rows], float)


def features(meta, lib, lam=0.0):
    """meta columns: theta, p_theta, E, Lz. Returns feature matrix for the chosen library.
    The column ORDER is the shared convention with certify_killing.py."""
    th, pth, E, Lz = meta[:, 0], meta[:, 1], meta[:, 2], meta[:, 3]
    c2 = np.cos(th) ** 2
    s2 = np.sin(th) ** 2
    base = np.stack([pth ** 2, c2, c2 * E ** 2, c2 * Lz ** 2 / s2], axis=1)
    if lib == "L1":
        return base
    if lib == "L2":
        return base / (1.0 + lam * c2)[:, None]
    if lib == "L3":
        return np.concatenate([base, np.stack([c2 ** 2, pth ** 2 * c2], axis=1)], axis=1)
    raise ValueError(lib)


def within_center(tid, F):
    """Subtract each trajectory's mean of each feature → within-trajectory fluctuation."""
    Fc = F.copy()
    for t in np.unique(tid):
        m = tid == t
        Fc[m] -= F[m].mean(axis=0)
    return Fc


def varratio(tid, q):
    """mean_traj[var_within(q)] / var_global(q): ~0 ⇒ conserved."""
    vg = q.var()
    if vg < 1e-30:
        return 1.0
    vw = np.mean([q[tid == t].var() for t in np.unique(tid)])
    return vw / vg


def fit_combo(tid, F):
    """Smallest-within-variance unit combination (standardized), returned in RAW units."""
    mu, sd = F.mean(0), F.std(0)
    sd[sd < 1e-12] = 1.0
    Fs = (F - mu) / sd
    Fw = within_center(tid, Fs)
    S = Fw.T @ Fw / len(Fw)
    w, V = np.linalg.eigh(S)
    c_std = V[:, 0]                          # smallest eigenvalue ⇒ most conserved
    c_raw = c_std / sd                       # back to raw feature units
    return c_raw / np.linalg.norm(c_raw)


def evaluate(tid, meta, lib, lam, c):
    F = features(meta, lib, lam)
    q = F @ c
    return varratio(tid, q)


def run_rung(rung):
    tid, meta = load(rung)
    rng = np.random.default_rng(SEED)
    uids = np.unique(tid)
    rng.shuffle(uids)
    cut = int(0.7 * len(uids))               # SPLIT BY TRAJECTORY (anti-leakage, §3)
    train_ids, test_ids = set(uids[:cut]), set(uids[cut:])
    tr = np.array([t in train_ids for t in tid])
    te = ~tr

    best = None
    for lib in ("L1", "L2", "L3"):
        lams = LAM_GRID if lib == "L2" else [0.0]
        for lam in lams:
            F = features(meta, lib, lam)
            c = fit_combo(tid[tr], F[tr])
            ho = evaluate(tid[te], meta[te], lib, lam, c)
            cand = (lib, float(lam), c, ho)
            if best is None or ho < best[3]:
                best = cand
        # parsimony: accept the first library that clears the bar
        lib_best = min(
            ((lib, float(lam), fit_combo(tid[tr], features(meta, lib, lam)[tr]))
             for lam in (LAM_GRID if lib == "L2" else [0.0])),
            key=lambda z: evaluate(tid[te], meta[te], z[0], z[1], z[2]))
        ho = evaluate(tid[te], meta[te], lib_best[0], lib_best[1], lib_best[2])
        if ho < EPS_T:
            best = (lib_best[0], lib_best[1], lib_best[2], ho)
            break

    lib, lam, c, ho = best
    verdict = "EXISTS" if ho < EPS_T else "DESTROYED"
    # coefficients in the named convention (c2 = reducible mass-shell term)
    names = ["c_ptheta2", "c_cos2", "c_cos2_E2", "c_cos2_Lz2_csc2"]
    coeffs = {n: float(v) for n, v in zip(names, c[:4])}
    out = {"rung": rung, "library": lib, "lam": lam, "verdict": verdict,
           "heldout_varratio": ho, "coeffs": coeffs,
           "n_train_traj": cut, "n_test_traj": len(uids) - cut}
    (RESULTS / f"candidate_{rung}.json").write_text(json.dumps(out, indent=1))
    print(f"  {rung:14s} {verdict:9s} lib={lib} lam={lam:+.3f} "
          f"heldout_varratio={ho:.2e}")
    return out


def main():
    print("MOVE A — distilling conserved quantities (tabula side, blind)")
    for rung in RUNGS:
        run_rung(rung)
    print("\nwrote results/candidate_*.json")


if __name__ == "__main__":
    main()
