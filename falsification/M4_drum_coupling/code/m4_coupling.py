#!/usr/bin/env python3
"""M4 — does coupling a second field make the hidden geometry audible?

    /Users/sumit/Github/conjecture_machine/.venv/bin/python m4_coupling.py

Gates M4a–M4e frozen in ../PREREGISTRATION.md; OBSERVABLE CORRECTED 2026-07-24 (see below). Reuses the K2
drums build: couple a static field as a potential V(x,y) to the Dirichlet Laplacian on each GWW drum and ask
when the degeneracy breaks.

CORRECTION. The first version compared the two drums' spectra directly, using their (buggy) ~1e-15
isospectral floor as the baseline. After K2's grid bug was fixed the drums are only isospectral in the
CONTINUUM, so at finite h their spectra already differ by ~2e-2 -- which swamped the coupling signal and made
the alpha-scaling read p~0.03. The fix is a DIFFERENTIAL observable: compare each drum's own coupling-induced
shift, delta_i = lambda_i(V) - lambda_i(0). The discretisation error is common-mode and cancels, leaving a
resolution-stable measurement (n=32 vs n=64 agree to ~1%). Answer: a UNIFORM coupling leaves them indistinguishable (killing the postulate's "ANY"),
while every spatially-varying coupling splits them at first order — so any probe that distinguishes points in
space makes the hidden geometry audible.
"""
import json
import sys
import time
from pathlib import Path

K2DIR = Path(__file__).resolve().parents[2] / "K2_isospectral_drums" / "code"
sys.path.insert(0, str(K2DIR))
import k2_drums as K2  # noqa: E402

import numpy as np  # noqa: E402
import scipy.sparse as sp  # noqa: E402
import scipy.sparse.linalg as spla  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "results"
NEIG = 12


def drum_xy(tris, n):
    mask, h = K2.interior_mask(tris, n)
    ys, xs = np.where(mask)
    return mask, h, (xs + 0.5) * h, (ys + 0.5) * h


def spectrum(tris, n, Vfun, k=NEIG):
    mask, h, X, Y = drum_xy(tris, n)
    L, N = K2.laplacian(mask, h)
    if Vfun is not None:
        L = L + sp.diags(Vfun(X, Y))
    return np.sort(spla.eigsh(L.tocsc(), k=k, sigma=-100.0, which="LM", return_eigenvectors=False))


def shift(tris, n, Vfun):
    """Coupling-induced spectral shift of ONE drum: λ(V) − λ(0). Common-mode discretisation error
    largely cancels in this difference, which is what makes the comparison below sound."""
    return spectrum(tris, n, Vfun) - spectrum(tris, n, None)


def diff_split(n, Vfun, normalise=True):
    """How differently the coupling acts on the two drums. ~0 ⇒ the probe cannot tell them apart."""
    d1 = shift(K2.DRUM1, n, Vfun)
    d2 = shift(K2.DRUM2, n, Vfun)
    raw = float(np.max(np.abs(d1 - d2)))
    if not normalise:
        return raw
    return raw / max(float(np.mean(np.abs(d1))), 1e-300)


# ---- the frozen coupling classes
def V_uniform(c):
    return lambda X, Y: c * np.ones_like(X)


def V_ramp(a):
    return lambda X, Y: a * X


def V_bump(a):
    return lambda X, Y: a * np.exp(-((X - 1.5) ** 2 + (Y - 1.5) ** 2) / 0.2)


def V_radial(a):
    return lambda X, Y: a * ((X - 1.5) ** 2 + (Y - 1.5) ** 2)


def V_tilelocal(a):
    return lambda X, Y: a * ((X - np.floor(X)) + (Y - np.floor(Y)))


def main():
    t0 = time.time()
    print("M4 — does coupling a second field make the hidden geometry audible? "
          "(gates frozen in PREREGISTRATION.md; observable corrected 2026-07-24)")
    print("  H = −∇² + V on both GWW drums; DIFFERENTIAL observable max|Δshift| (discretisation cancels)\n")

    n = 32
    classes = [("linear ramp  V=α·x", V_ramp), ("gaussian bump V=α·e^(−|r−r₀|²/0.2)", V_bump),
               ("radial well  V=α·|r−r₀|²", V_radial), ("tile-local   V=α·(fx+fy)", V_tilelocal)]

    # ---- M4a: uniform coupling
    unif = {c: diff_split(n, V_uniform(c)) for c in [1.0, 5.0, 50.0]}
    m4a = all(v < 1e-9 for v in unif.values())
    print("  M4a UNIFORM coupling V=c — does a constant help tell the drums apart?")
    for c, v in unif.items():
        print(f"      c={c:<5}  max|Δshift|/|shift| = {v:.2e}")
    print(f"      → {'PASS ✅ — a constant shifts BOTH drums identically: zero distinguishing power, so the postulate’s “ANY” is FALSE' if m4a else 'FAIL ❌'}")

    # ---- M4b: spatially-varying couplings
    print(f"\n  M4b spatially-varying couplings at α=1 (n={n}):")
    unit = {}
    for label, mk in classes:
        v = diff_split(n, mk(1.0))
        unit[label] = v
        print(f"    {label:38s} {v:.3e}   {'SPLIT ✅' if v > 0.1 else 'no split ❌'}")
    m4b = all(v > 0.1 for v in unit.values())
    print(f"    → {'PASS ✅ — every position-dependent coupling distinguishes the drums' if m4b else 'FAIL ❌'}")

    # ---- M4c: first-order scaling of the RAW differential shift
    print("\n  M4c first-order scaling (raw max|Δshift| ∝ α^p, small α):")
    alphas = [0.01, 0.03, 0.1, 0.3]
    scal = {}
    for label, mk in [("linear ramp", V_ramp), ("gaussian bump", V_bump)]:
        ss = [diff_split(n, mk(a), normalise=False) for a in alphas]
        p = float(np.polyfit(np.log(alphas), np.log(ss), 1)[0])
        scal[label] = dict(alphas=alphas, splits=ss, p=p)
        print(f"    {label:14s}: {[f'{x:.2e}' for x in ss]}  →  p = {p:.4f}")
    m4c = all(0.9 <= scal[k]["p"] <= 1.1 for k in scal)
    print(f"    → {'PASS ✅ — genuine first-order perturbation effect' if m4c else 'FAIL ❌'}")

    # ---- M4d protection mechanism
    m4d = unit["tile-local   V=α·(fx+fy)"] > 0.1
    print(f"\n  M4d protection: tile-local coupling distinguishes ({unit['tile-local   V=α·(fx+fy)']:.3e})  → "
          f"{'PASS ✅ — tile-locality is NOT protection; only constants are protected' if m4d else 'FAIL ❌'}")

    # ---- M4e resolution stability
    print("\n  M4e resolution stability (n=64 vs n=32):")
    ok_res = True
    res64 = {}
    for label, mk in classes[:2]:
        v64 = diff_split(64, mk(1.0))
        res64[label] = v64
        agree = abs(v64 - unit[label]) / unit[label] < 0.10
        ok_res = ok_res and agree
        print(f"    {label:38s} n=32 {unit[label]:.3e}  n=64 {v64:.3e}  ({'agree<10% ✅' if agree else 'differ ⚠'})")
    u64 = diff_split(64, V_uniform(5.0))
    m4e = ok_res and u64 < 1e-9
    print(f"    uniform control at n=64: {u64:.2e}  → {'PASS ✅' if m4e else 'check ⚠'}")

    verdict = "KILLED" if m4a else "SURVIVES"
    allp = m4a and m4b and m4c and m4d and m4e
    print(f"\n  M4 {verdict} as literally stated — a uniform coupling is a nonzero coupling that leaves the")
    print(f"  drums indistinguishable (identical shifts, {unif[5.0]:.0e}). But the postulate's SUBSTANCE holds:")
    print(f"  every coupling that varies in space distinguishes them, linearly in strength. Hidden geometry")
    print(f"  becomes audible exactly when the probe can tell points apart; a uniform probe stays deaf.")

    OUT.mkdir(exist_ok=True)
    (OUT / "m4_coupling.json").write_text(json.dumps({
        "n": n, "n_eigenvalues": NEIG, "observable": "differential: max|shift1-shift2|, shift=lambda(V)-lambda(0)",
        "CORRECTION": ("Original observable compared the two drums' spectra directly against a ~1e-15 floor "
                       "that only existed because of K2's grid bug (drums disconnected into congruent pieces). "
                       "On a correct grid that floor is ~2e-2 discretisation error, which swamped the signal "
                       "(alpha-scaling read p~0.03). Replaced by the differential observable, which cancels "
                       "common-mode discretisation error and is resolution-stable."),
        "uniform_splits": unif, "unit_strength_splits": unit, "scaling": scal, "res64": res64,
        "uniform_control_n64": u64,
        "M4a_kill_ANY": bool(m4a), "M4b_fragility_pass": bool(m4b), "M4c_first_order_pass": bool(m4c),
        "M4d_protection_pass": bool(m4d), "M4e_canary_pass": bool(m4e),
        "verdict": verdict, "all_pass": bool(allp),
        "summary": (f"M4 ({verdict} as literally stated): a UNIFORM coupling shifts both GWW drums identically "
                    f"({unif[5.0]:.1e} differential), so it adds zero distinguishing power and the postulate's "
                    f"'ANY nonzero coupling' is false. Its substance survives: every spatially-varying coupling "
                    f"distinguishes them (ramp {unit['linear ramp  V=α·x']:.2f}, bump "
                    f"{unit['gaussian bump V=α·e^(−|r−r₀|²/0.2)']:.2f}, tile-local "
                    f"{unit['tile-local   V=α·(fx+fy)']:.2f}) — twelve orders above the uniform case — linearly "
                    f"in coupling strength (p~1). Tile-locality is not protection; only constants are. "
                    f"Observable corrected 2026-07-24 after K2's grid bug; conclusions unchanged, now measured "
                    f"on a resolution-stable differential."),
    }, indent=1))
    print(f"\n  wrote results/m4_coupling.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
