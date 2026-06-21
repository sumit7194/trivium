#!/usr/bin/env python3
"""Leg J stage 2 — intrinsic dimension of each orbit cloud (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python count_dimension.py

Method A: a bound orbit on a torus has intrinsic dimension 2; a chaotic orbit fills a 3-D shell.
PRIMARY estimator = correlation dimension (Grassberger–Procaccia) — invariant under the curved
embedding, so it is not fooled by torus curvature. CROSS-CHECK = leg 1's bottleneck AE counter (the
bridge's own tool), carrying its known +1 curvature-inflation caveat (leg 7b / Move G). Method B
(Carter-constant drift) is read straight from stage 1.

Calibration gate G1: on Kerr (ε=0) the correlation dimension must read ≈2 for the bound orbits, else
the instrument is void. Then report the bumpy distribution. No outcome assumed.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/TheBridge/leg1_moduli_count/code")

RES = Path(__file__).resolve().parent.parent / "results"
RNG = np.random.default_rng(0)


def whiten(cloud):
    X = np.asarray(cloud, float)
    mu, sd = X.mean(0), X.std(0)
    keep = sd > 1e-9
    return ((X[:, keep] - mu[keep]) / sd[keep]) if keep.any() else None


def corr_dim(X, n_sub=500):
    """Grassberger–Procaccia correlation dimension: slope of log C(r) vs log r in the scaling band."""
    n = len(X)
    Y = X[RNG.choice(n, min(n, n_sub), replace=False)]
    d = np.sqrt(((Y[:, None, :] - Y[None, :, :]) ** 2).sum(-1))
    d = d[np.triu_indices(len(Y), 1)]
    d = d[d > 0]
    if len(d) < 50:
        return float("nan")
    rs = np.logspace(np.log10(np.percentile(d, 2)), np.log10(np.percentile(d, 60)), 16)
    C = np.array([(d < r).mean() for r in rs])
    m = (C > 0.01) & (C < 0.6) & (rs > 0)
    if m.sum() < 4:
        return float("nan")
    return float(np.polyfit(np.log(rs[m]), np.log(C[m]), 1)[0])


def ae_knee(X):
    """Leg 1's nonlinear AE knee (bridge tool; may inflate curved manifolds by +1)."""
    try:
        from count_bottleneck import train_ae, prep
    except Exception:
        return None
    Xs = X.astype(np.float32)
    RNG.shuffle(Xs)
    p = prep(Xs, int(0.7 * len(Xs)))
    if p is None:
        return 0
    Xtr, Xte = p["white"]
    r2 = {0: 0.0}
    for d in (1, 2, 3, 4):
        r2[d] = max(train_ae(Xtr, Xte, d, s) for s in (0, 1))
    return sum(1 for d in (1, 2, 3, 4) if r2[d] - r2[d - 1] > 0.02)


def main():
    print("LEG J — intrinsic dimension of bound orbits (torus=2, chaos=3) + Carter drift\n")
    files = sorted(RES.glob("orbits_eps*.json"), key=lambda f: float(f.stem.split("eps")[1]))
    summary, kerr_med = [], None
    for f in files:
        D = json.loads(f.read_text())
        eps = D["eps"]
        cds, drifts, knees = [], [], []
        for o in D["orbits"]:
            X = whiten(o["cloud"])
            if X is None or len(X) < 80:
                continue
            cds.append(corr_dim(X))
            drifts.append(o["C0_drift"])
            if len(knees) < 8:                                  # AE is slow — sample a few
                k = ae_knee(X)
                if k is not None:
                    knees.append(k)
        cds = [c for c in cds if np.isfinite(c)]
        med = float(np.median(cds)) if cds else float("nan")
        frac3 = float(np.mean([c > 2.7 for c in cds])) if cds else float("nan")   # >2.7: clear of curved-torus ~2.3
        dmed = float(np.median(drifts)) if drifts else float("nan")
        kmed = float(np.median(knees)) if knees else float("nan")
        if eps == 0.0:
            kerr_med = med
        summary.append({"eps": eps, "n": len(cds), "Dcorr_median": med, "frac_D>2.7": frac3,
                        "Carter_drift_median": dmed, "AE_knee_median": kmed})
        print(f"  ε={eps:.2f}: n={len(cds):2d}  D_corr median={med:.2f}  frac(D>2.7)={frac3:.2f}  "
              f"Carter drift={dmed:.1e}  AE knee≈{kmed:.1f}")

    gate = kerr_med is not None and 1.6 <= kerr_med <= 2.6      # GP overestimates curved tori (~2.3); clear of 3
    print(f"\n  G1 calibration gate (Kerr ε=0 → D_corr≈2): {'PASS ✅' if gate else 'FAIL ❌'} "
          f"(Kerr median D_corr = {kerr_med:.2f})")
    if gate:
        bumpy = [s for s in summary if s["eps"] > 0]
        worst = max(bumpy, key=lambda s: s["frac_D>2.7"]) if bumpy else None
        print(f"  G2 result: across the bump, Carter drift grows "
              f"{summary[0]['Carter_drift_median']:.1e} → {summary[-1]['Carter_drift_median']:.1e}; "
              f"max chaotic-volume fraction (D>2.7) = {worst['frac_D>2.7']:.2f} at ε={worst['eps']:.2f}.")
        print("  → Interpret per the pre-registration: tori-survive (D≈2, drift bounded) vs "
              "tori-destroyed (D→3). Resolution-limited: a D≈2 null is an upper bound on chaos, not a proof.")
    (RES / "dimension_verdict.json").write_text(json.dumps(
        {"calibration_gate_pass": bool(gate), "kerr_Dcorr_median": kerr_med, "by_eps": summary}, indent=1))
    print("\n  wrote results/dimension_verdict.json")


if __name__ == "__main__":
    main()
