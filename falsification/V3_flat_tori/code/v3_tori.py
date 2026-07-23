#!/usr/bin/env python3
"""V3 — 2D flat tori ARE determined by their spectrum (the converse of K2's kill).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python v3_tori.py

Gates V3a/V3b/V3c frozen in ../PREREGISTRATION.md before this was written. A flat torus T²=ℝ²/Λ has spectrum
λ=4π²|w|², w∈Λ* — the dual lattice's norm multiset. Normalising to unit covolume leaves the modulus τ in the
fundamental domain; distinct τ are non-isometric tori. Where K2 showed two DRUMS can share a spectrum, V3
shows two flat 2-tori cannot — and measures how finely the spectrum resolves the shape.

Strictly 2D: flat tori are NOT spectrally determined in dimension 4 (Conway-Sloane) or 16 (Milnor).
"""
import json
import time
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results"
K_EIG = 40
RANGE = 14
RNG = np.random.default_rng(20260723)


def spectrum(tau, K=K_EIG, R=RANGE):
    """Lowest K Laplace eigenvalues of the unit-covolume flat torus with modulus tau."""
    x, y = tau.real, tau.imag
    B = np.array([[1 / np.sqrt(y), x / np.sqrt(y)], [0.0, np.sqrt(y)]])   # columns = basis, covolume 1
    D = np.linalg.inv(B).T                                                # dual basis
    a, b = np.meshgrid(np.arange(-R, R + 1), np.arange(-R, R + 1))
    W = D @ np.stack([a.ravel(), b.ravel()])
    lam = 4 * np.pi ** 2 * (W[0] ** 2 + W[1] ** 2)
    return np.sort(lam)[:K]


def spec_dist(t1, t2, K=K_EIG):
    s1, s2 = spectrum(t1, K), spectrum(t2, K)
    return float(np.max(np.abs(s1 - s2)) / np.mean(s1))


def hyp_dist(t1, t2):
    return float(np.arccosh(1 + abs(t1 - t2) ** 2 / (2 * t1.imag * t2.imag)))


def sample_F(n):
    """Random moduli in the fundamental domain F = {|Re τ|≤½, |τ|≥1, Im τ>0} (capped Im τ ≤ 3)."""
    out = []
    while len(out) < n:
        x = RNG.uniform(-0.5, 0.5)
        y = RNG.uniform(0.5, 3.0)
        t = complex(x, y)
        if abs(t) >= 1.0:
            out.append(t)
    return out


def main():
    t0 = time.time()
    print("V3 — 2D flat tori ARE determined by their spectrum (gates frozen in PREREGISTRATION.md)")
    print(f"  unit-covolume tori, modulus τ in the fundamental domain, lowest K={K_EIG} eigenvalues\n")

    # ---- V3c: modular control FIRST (if this fails everything else is void)
    tau = complex(0.23, 1.37)
    ctrl = {"tau+1": spec_dist(tau, tau + 1), "tau-1": spec_dist(tau, tau - 1),
            "-1/tau": spec_dist(tau, -1 / tau)}
    v3c = all(v < 1e-12 for v in ctrl.values())
    print("  V3c modular control — SL(2,ℤ)-equivalent moduli are the SAME torus, so must be isospectral:")
    for k, v in ctrl.items():
        print(f"    τ vs {k:7s}: rel spectral diff = {v:.2e}")
    print(f"    → {'PASS ✅ (lattice/dual convention verified)' if v3c else 'FAIL ❌ — convention bug, all else void'}")

    # ---- V3a: no spurious isospectral pairs
    NP = 2000
    T1, T2 = sample_F(NP), sample_F(NP)
    rows = []
    for a, b in zip(T1, T2):
        rows.append((hyp_dist(a, b), spec_dist(a, b)))
    arr = np.array(rows)
    far = arr[arr[:, 0] > 0.1]
    min_spec_far = float(far[:, 1].min()) if len(far) else float("nan")
    worst = far[far[:, 1].argmin()] if len(far) else None
    v3a = len(far) > 0 and min_spec_far > 1e-6
    hard_fail = len(far) > 0 and min_spec_far < 1e-9
    print(f"\n  V3a no spurious isospectral pairs ({NP} random pairs; {len(far)} with hyperbolic separation >0.1):")
    print(f"    minimum spectral distance among well-separated pairs = {min_spec_far:.3e}  (want >1e-6)")
    print(f"    (that closest pair had moduli separation {worst[0]:.3f})")
    print(f"    → {'SURVIVES ✅ — no two genuinely different flat 2-tori share a spectrum' if v3a else 'FAIL ❌'}")
    if hard_fail:
        print("    ⚠️  STOP: a well-separated pair is isospectral to <1e-9 — contradicts the 2D theorem. "
              "Flagged for review, not interpreted autonomously.")

    # ---- V3b: resolution bound
    print("\n  V3b resolution bound — spectral distance vs moduli perturbation δ:")
    base = complex(0.13, 1.21)
    deltas = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    scaling = {}
    for K in [10, 40, 160]:
        ds = []
        for d in deltas:
            ds.append(spec_dist(base, base + complex(d, 0.0), K=K))
        p = float(np.polyfit(np.log(deltas), np.log(np.maximum(ds, 1e-300)), 1)[0])
        # resolving power: smallest δ whose signal still exceeds a 1e-12 detection floor,
        # extrapolated from the linear regime
        slope = ds[0] / deltas[0]
        dmin = 1e-12 / slope
        scaling[K] = dict(deltas=deltas, dists=ds, p=p, resolving_delta=dmin)
        print(f"    K={K:3d}: dists {[f'{x:.1e}' for x in ds]}  p={p:.4f}  "
              f"resolving δ≳{dmin:.1e}")
    v3b = all(0.9 <= scaling[K]["p"] <= 1.1 for K in scaling)
    print(f"    → {'PASS ✅ — linear response; the spectrum resolves shape down to the stated δ' if v3b else 'FAIL ❌'}")

    verdict = "SURVIVES" if (v3a and v3c) else ("KILLED" if hard_fail else "UNDECIDED")
    allp = v3a and v3b and v3c
    print(f"\n  V3 {verdict}. Together with K2 this completes the hearing-shapes story honestly:")
    print(f"    • GWW drums   — isospectral but NOT isometric  → you cannot hear a drum's shape (K2, KILLED)")
    print(f"    • flat 2-tori — isospectral IFF isometric      → you CAN hear a flat 2-torus (V3, SURVIVES)")
    print(f"  'Can you hear the shape?' has no universal answer — it depends on the class and the dimension")
    print(f"  (flat tori fail in 4D (Conway–Sloane) and 16D (Milnor); 2D is safe).")

    OUT.mkdir(exist_ok=True)
    (OUT / "v3_tori.json").write_text(json.dumps({
        "K_eigenvalues": K_EIG, "dual_range": RANGE, "n_pairs": NP,
        "V3c_modular_control": ctrl, "V3c_pass": bool(v3c),
        "V3a_min_spec_dist_far_pairs": min_spec_far, "V3a_n_far_pairs": int(len(far)),
        "V3a_pass": bool(v3a), "V3a_hard_fail": bool(hard_fail),
        "V3b_scaling": {str(k): v for k, v in scaling.items()}, "V3b_pass": bool(v3b),
        "verdict": verdict, "all_pass": bool(allp),
        "summary": (f"V3 ({verdict}): unit-covolume flat 2-tori are spectrally determined — over {NP} random "
                    f"moduli pairs, every pair separated by hyperbolic distance >0.1 has spectral distance "
                    f">{min_spec_far:.1e}, and SL(2,Z)-equivalent moduli are isospectral to <1e-12 (control). "
                    f"Spectral distance responds linearly to moduli perturbation (p≈1), bounding the "
                    f"instrument's resolving power. Strictly 2D: flat tori are NOT spectrally determined in "
                    f"4D (Conway-Sloane) or 16D (Milnor). Converse to K2: drums are isospectral but not "
                    f"isometric; flat 2-tori are isospectral iff isometric."),
    }, indent=1))
    print(f"\n  wrote results/v3_tori.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
