#!/usr/bin/env python3
"""R7 — is O4 a threshold artifact, or a real obstruction? (adopting the literature's instrument).

    python3 r7_threshold.py

Gates R7a-R7d frozen in ../PREREGISTRATION.md. M6's prior-art sweep ASSERTED (from reading, not running)
that O4 -- a degree-6 polynomial falsely emitting at 2.7e-7 under our hand-set tau_rel=1e-6 -- was "our
threshold being the wrong kind" and that a noise-calibrated cutoff would dissolve it. R7 tests that claim.
If R7b fails, M6 is wrong on that point and gets amended.

Upgrades adopted, all from other people:
  1. noise-calibrated cutoff  sigma_cut = sqrt(N*p) * eps^(2/3)   [Oellerich & Emelianenko, arXiv:2403.04889 Cor 4.2]
  2. spectral-gap library selection  max(sigma_{j-1} - sigma_j)   [same]
  3. held-out / diversity guard                                    [Ray 2026, arXiv:2603.20474]

Reuses R2's own orbit setup verbatim so O4 is REPRODUCED, not re-created. numpy only; bridge-solo.
"""
import json
import sys
from pathlib import Path

import numpy as np

R2DIR = Path(__file__).resolve().parents[2] / "R2_emit_theorem" / "code"
sys.path.insert(0, str(R2DIR))
import emit_reproduce as R2

OUT = Path(__file__).resolve().parent.parent / "results"
rng = np.random.default_rng(20260726)

TAU_OLD = R2.TAU_REL          # 1e-6, the hand-set floor that O4 slipped under
NORB, NTEST = 6, 2            # 6 orbits, 2 held out
DT, NSTEP = 0.01, 2000        # identical to R2


def design(orbits, basis, normalize=True):
    """R2's design matrix, optionally column-normalised (standard SINDy practice; frozen as primary)."""
    M = R2.design_matrix(orbits, basis)
    if normalize:
        nrm = np.linalg.norm(M, axis=0, keepdims=True)
        M = M / np.where(nrm > 0, nrm, 1.0)
    return M


def orbit_pair(system, z0):
    """Sample-matched dt and dt/2 runs — the direct measurement of integrator perturbation."""
    coarse = R2.orbit(system, z0, dt=DT, n=NSTEP)
    fine = R2.orbit(system, z0, dt=DT / 2, n=2 * NSTEP)[::2]     # same times
    return coarse, fine


def epsilon(orbs_c, orbs_f, basis):
    """eps = max |M_fine - M_coarse| entrywise — a measured perturbation, independent of the invariant."""
    Mc, Mf = design(orbs_c, basis), design(orbs_f, basis)
    return float(np.max(np.abs(Mf - Mc)))


def analyse(orbs_c, orbs_f, basis, label):
    M = design(orbs_c, basis)
    s = np.linalg.svd(M, compute_uv=False)
    N, p = M.shape
    eps = epsilon(orbs_c, orbs_f, basis)
    sig_cut = float(np.sqrt(N * p) * eps ** (2.0 / 3.0))          # O&E Cor. 4.2
    sn = s / s[0]
    gaps = sn[:-1] - sn[1:]
    Mu = design(orbs_c, basis, normalize=False)
    su = np.linalg.svd(Mu, compute_uv=False)
    return {"label": label, "N": N, "p": p,
            "sigma_min": float(s[-1]), "sigma_max": float(s[0]),
            "ratio_norm": float(s[-1] / s[0]),
            "ratio_unnorm": float(su[-1] / su[0]),
            "eps": eps, "sigma_cutoff": sig_cut,
            "emit_new": bool(s[-1] <= sig_cut),
            "emit_old": bool(su[-1] / su[0] <= TAU_OLD),
            "max_gap": float(np.max(gaps)) if len(gaps) else 0.0}


def heldout(orbs_tr, orbs_te, basis):
    """Guard: null vector from TRAIN, scored on unseen orbits. Approximation degrades; representation does not."""
    Mtr = design(orbs_tr, basis)
    _, _, Vt = np.linalg.svd(Mtr, full_matrices=False)
    c = Vt[-1]
    Mte = design(orbs_te, basis)
    return float(np.linalg.norm(Mte @ c) / (np.linalg.norm(Mte) + 1e-300))


def main():
    print("R7 — is O4 a threshold artifact or a real obstruction? (gates in PREREGISTRATION.md)")
    print(f"  adopting: O&E noise-calibrated cutoff + spectral-gap selection + held-out guard")
    print(f"  reusing R2's orbits verbatim (pendulum x0 in [1.6,2.8], Yoshida-4, dt={DT}, n={NSTEP})\n")
    rep = {"tau_old": TAU_OLD}

    z_ho = [[rng.uniform(0.5, 2), rng.uniform(-1, 1)] for _ in range(NORB)]
    z_pe = [[rng.uniform(1.6, 2.8), rng.uniform(-0.3, 0.3)] for _ in range(NORB)]
    ho_c, ho_f = zip(*[orbit_pair("harmonic", z) for z in z_ho])
    pe_c, pe_f = zip(*[orbit_pair("pendulum", z) for z in z_pe])
    ho_c, ho_f, pe_c, pe_f = list(ho_c), list(ho_f), list(pe_c), list(pe_f)

    cos_atom = [lambda z: np.cos(z[:, 0])]
    LIBS = {
        "harmonic  poly2": (ho_c, ho_f, R2.poly_basis(2)),
        "pendulum  poly2": (pe_c, pe_f, R2.poly_basis(2)),
        "pendulum  poly4": (pe_c, pe_f, R2.poly_basis(4)),
        "pendulum  poly6": (pe_c, pe_f, R2.poly_basis(6)),
        "pendulum  poly4+cos": (pe_c, pe_f, R2.poly_basis(4) + cos_atom),
    }

    rows = {}
    print(f"  {'library':22s} | {'sigma_min':>10} | {'eps':>9} | {'sigma_cut':>10} | {'OLD emit':>9} | {'NEW emit':>9}")
    for lab, (oc, of, b) in LIBS.items():
        r = analyse(oc, of, b, lab)
        rows[lab] = r
        print(f"  {lab:22s} | {r['sigma_min']:10.3e} | {r['eps']:9.2e} | {r['sigma_cutoff']:10.3e} | "
              f"{str(r['emit_old']):>9} | {str(r['emit_new']):>9}")

    # ---- R7a regression: true positives must survive the upgrade
    t1, t2 = rows["harmonic  poly2"], rows["pendulum  poly4+cos"]
    r7a = t1["emit_new"] and t2["emit_new"]
    print(f"\n  R7a — regression (the upgrade must not break true positives):")
    print(f"     harmonic poly2      : emit_new={t1['emit_new']}  (σ_min {t1['sigma_min']:.2e} vs cut {t1['sigma_cutoff']:.2e})")
    print(f"     pendulum poly4+cos  : emit_new={t2['emit_new']}  (σ_min {t2['sigma_min']:.2e} vs cut {t2['sigma_cutoff']:.2e})")
    print(f"     →  R7a {'PASS ✅' if r7a else 'FAIL ❌ — upgrade REJECTED, later gates void'}")
    rep["R7a"] = {"pass": bool(r7a), "harmonic": t1, "cos": t2}

    # ---- R7b THE decisive gate: does the noise-calibrated cutoff reject O4?
    o4 = rows["pendulum  poly6"]
    r7b = not o4["emit_new"]
    print(f"\n  R7b — the O4 test (decisive):")
    print(f"     pendulum poly6: OLD ratio {o4['ratio_unnorm']:.2e} vs τ={TAU_OLD:.0e} → emit={o4['emit_old']} (the false positive)")
    print(f"     NEW: σ_min {o4['sigma_min']:.3e} vs noise-calibrated cutoff {o4['sigma_cutoff']:.3e} → emit={o4['emit_new']}")
    print(f"     →  R7b {'PASS ✅ — O4 REJECTED; the threshold was the defect' if r7b else 'FAIL ❌ — O4 survives noise calibration; M6 OVERSTATED'}")
    rep["R7b"] = {"pass": bool(r7b), "poly6": o4}

    # ---- R7c spectral-gap library selection
    pend_libs = {k: v for k, v in rows.items() if k.startswith("pendulum")}
    pick = max(pend_libs, key=lambda k: pend_libs[k]["max_gap"])
    r7c = pick == "pendulum  poly4+cos"
    print(f"\n  R7c — spectral-gap library selection (max σ_{{j-1}}−σ_j):")
    for k, v in pend_libs.items():
        print(f"     {k:22s} max gap = {v['max_gap']:.4f}")
    print(f"     picked: {pick}  →  R7c {'PASS ✅ — picks the library containing the true invariant' if r7c else 'FAIL ❌'}")
    rep["R7c"] = {"pass": bool(r7c), "picked": pick,
                  "gaps": {k: v["max_gap"] for k, v in pend_libs.items()}}

    # ---- R7d held-out guard
    tr, te = pe_c[:NORB - NTEST], pe_c[NORB - NTEST:]
    h_cos = heldout(tr, te, R2.poly_basis(4) + cos_atom)
    h_p6 = heldout(tr, te, R2.poly_basis(6))
    in_p6 = rows["pendulum  poly6"]["ratio_norm"]
    degrade = h_p6 / in_p6 if in_p6 > 0 else float("inf")
    r7d = h_cos < 1e-8 and degrade >= 10
    print(f"\n  R7d — held-out guard (null vector from 4 train orbits, scored on 2 unseen):")
    print(f"     poly4+cos : held-out {h_cos:.2e}  (representation — should stay at machine precision)")
    print(f"     poly6     : in-sample {in_p6:.2e} → held-out {h_p6:.2e}  = {degrade:.1f}× degradation")
    print(f"     →  R7d {'PASS ✅ — the guard separates representation from approximation' if r7d else 'FAIL ❌'}")
    rep["R7d"] = {"pass": bool(r7d), "cos_heldout": h_cos, "poly6_insample": in_p6,
                  "poly6_heldout": h_p6, "degradation": degrade}

    if not r7a:
        verdict = "UPGRADE REJECTED — the noise-calibrated cutoff breaks true positives; later gates void"
    elif r7b:
        verdict = ("postulate TRUE — O4 was a THRESHOLD ARTIFACT: a noise-calibrated cutoff rejects the "
                   "degree-6 false positive while still emitting on true invariants. M6's assertion stands.")
    else:
        verdict = ("postulate FALSE — O4 is a REAL OBSTRUCTION: it survives noise calibration too, so the "
                   "hand-set threshold was NOT the defect. M6 OVERSTATED and must be amended; the held-out "
                   "guard, not the cutoff, is the operative defence.")
    print(f"\n  VERDICT: {verdict}")
    print(f"\n  Scope: zero novelty — all three upgrades are other people's. What R7 decides is which of OUR")
    print(f"  two stories about O4 is correct. One system, one false-positive arm; passing does not prove the")
    print(f"  criterion universally safe, only that it handles the case that broke us.")

    OUT.mkdir(exist_ok=True)
    rep["verdict"] = verdict
    rep["libraries"] = rows
    (OUT / "r7_threshold.json").write_text(json.dumps(rep, indent=1))
    print(f"\n  wrote results/r7_threshold.json")


if __name__ == "__main__":
    main()
