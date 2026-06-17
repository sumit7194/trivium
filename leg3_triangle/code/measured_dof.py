#!/usr/bin/env python3
"""Leg-3 — close the spine: the §5 count-triangle + a measured-DOF from deepstrain's δ.

Run with any venv that has numpy + matplotlib (curvature venv works):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python measured_dof.py

BRIDGE code. Reads deepstrain's published δ posterior summary READ-ONLY from
`ringdown_spectroscopy/results/10_recalibration.json`. Does not modify any source repo.

Turns the no-hair δ posterior into a "measured count" comparable to a moduli dimension:
a Savage-Dickey density ratio for the nested point δ=0 (Kerr, 2 numbers) vs a free hair δ
(a candidate 3rd number). Then assembles the three independent counts (PREREGISTRATION §2).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DEEPSTRAIN = Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results/10_recalibration.json")
OUT = Path(__file__).resolve().parent.parent / "results"
OUT.mkdir(exist_ok=True)

Z90 = 1.6448536269514722   # standard normal 90% two-sided half-width


def gaussian_density(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


def main():
    rec = json.loads(DEEPSTRAIN.read_text())
    med, lo90, hi90 = rec["gw250114_delta"]            # [median, low90, high90]  (read-only)
    coverage = float(np.mean(rec["coverage_heldout"]))
    kerr_in_90 = rec["kerr_inside_90"]

    # Gaussian approx of the δ posterior from its published 90% interval.
    sigma = (hi90 - lo90) / (2 * Z90)
    delta0_in_90 = lo90 <= 0.0 <= hi90
    post0 = gaussian_density(0.0, med, sigma)          # posterior density at δ=0

    # Savage-Dickey BF(M2:M3) = posterior(δ=0)/prior(δ=0). M2 = Kerr (2 numbers, δ=0);
    # M3 = + free hair δ (a 3rd number). Priors stated as ILLUSTRATIVE (PREREGISTRATION §3).
    priors = {"U[-1,1]": 0.5, "U[-0.5,0.5]": 1.0}
    BF = {name: post0 / dens for name, dens in priors.items()}

    # C1: measurement consistent with DOF=2.
    C1 = bool(delta0_in_90 and all(b >= 1.0 for b in BF.values()))

    # ----- the §5 count-triangle -----
    # tabula's count is the established leg-1 result (RN dimensionful whitened intrinsic
    # dim = 2; dyonic showed observable < algebraic). See leg1_moduli_count/FINDINGS.md.
    triangle = {
        "ansatz (proved moduli dim)":      {"count": 2, "kind": "exact / proved",
                                            "note": "Kerr 2-param; scalar no-hair proved (32/33); charge=1 number, e≡m (34)"},
        "tabula (inferred, leg 1)":        {"count": 2, "kind": "neural intrinsic dim",
                                            "note": "RN observable manifold = 2 (dyonic degeneracy: observable<algebraic)"},
        "deepstrain (measured, this leg)": {"count": 2, "kind": "no-hair δ consistent with 0",
                                            "note": f"GW250114 δ={med:+.3f} [{lo90:+.3f},{hi90:+.3f}] 90%, σ(δ)≈{sigma:.3f}"},
    }
    C2 = all(v["count"] == 2 for v in triangle.values()) and C1

    out = {
        "delta_median": med, "delta_90": [lo90, hi90], "sigma_delta": sigma,
        "coverage_heldout_mean": coverage, "kerr_inside_90": kerr_in_90,
        "delta0_in_90": delta0_in_90, "savage_dickey_BF_M2_over_M3": BF,
        "C1_consistent_with_DOF2": C1, "C2_triangle_closes": C2,
        "triangle": triangle,
    }
    (OUT / "measured_dof.json").write_text(json.dumps(out, indent=1, default=float))

    print("§5 COUNT-TRIANGLE — how many numbers is a black hole?\n")
    for k, v in triangle.items():
        print(f"  {k:34s} count = {v['count']}   [{v['kind']}]")
        print(f"       {v['note']}")
    print(f"\n  deepstrain measured-DOF: δ=0 within 90% CI = {delta0_in_90}; σ(δ)≈{sigma:.3f}")
    print(f"  Savage-Dickey BF(2-number : 3-number): " +
          ", ".join(f"{n} -> {b:.2f}" for n, b in BF.items()))
    print(f"\n  C1 (measurement consistent with DOF=2): {C1}")
    print(f"  C2 (the triangle closes — all three = 2): {C2}")

    # ----- figure: the δ posterior with δ=0 (Kerr / 2-number) marked -----
    fig, ax = plt.subplots(figsize=(8, 4.6))
    xs = np.linspace(med - 4 * sigma, med + 4 * sigma, 400)
    ax.plot(xs, gaussian_density(xs, med, sigma), color="steelblue", lw=2,
            label="GW250114 no-hair posterior p(δ)")
    ax.fill_between(xs, 0, gaussian_density(xs, med, sigma),
                    where=(xs >= lo90) & (xs <= hi90), color="steelblue", alpha=0.2,
                    label="90% credible interval")
    ax.axvline(0.0, color="crimson", lw=2, ls="--",
               label="δ=0  (Kerr / exactly 2 numbers)")
    ax.axvline(med, color="navy", lw=1, ls=":")
    ax.set_xlabel("no-hair deviation δ  (the candidate 3rd number)")
    ax.set_ylabel("posterior density")
    ax.set_title("Leg 3 — the measured leg closes the triangle:\n"
                 "δ=0 (2 numbers) sits well inside the 90% CI — no hair resolved")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "leg3_nohair_delta.png", dpi=140)
    print(f"\nwrote {OUT / 'measured_dof.json'} and leg3_nohair_delta.png")


if __name__ == "__main__":
    main()
