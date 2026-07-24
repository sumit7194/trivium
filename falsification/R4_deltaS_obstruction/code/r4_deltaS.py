#!/usr/bin/env python3
"""R4 — is "non-factorization" a faithful proxy for the K1 obstruction ΔS≠0? (2-mode Gaussian toy).

    python3 r4_deltaS.py

Gates R4a/R4b frozen in ../PREREGISTRATION.md. The Longo identity S_rel=2π·boostE holds iff ΔS=0. R4a shows
the obstruction is ΔS (a cross-cut displacement straddles the cut but ΔS=0; a cross-cut squeeze has ΔS≠0).
R4b searches genuinely-entangling symplectics for a non-factorizing ΔS=0 excitation — deciding whether
"non-factorization" is sufficient-but-not-necessary (postulate TRUE) or faithful (SURVIVES).
"""
import json
from itertools import product
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results"
I2 = np.eye(2); Z2 = np.diag([1.0, -1.0])
S_VAC = 0.5
NU_VAC = np.cosh(2 * S_VAC)


def h(x):
    return x * np.log(x) if x > 0 else 0.0


def s_ent(nu):
    nu = max(nu, 1.0)
    return h((nu + 1) / 2) - h((nu - 1) / 2)


def vacuum():
    c, s = np.cosh(2 * S_VAC), np.sinh(2 * S_VAC)
    g = np.zeros((4, 4))
    g[:2, :2] = c * I2; g[2:, 2:] = c * I2
    g[:2, 2:] = s * Z2; g[2:, :2] = s * Z2
    return g


def nu_A(g):
    """symplectic eigenvalue of the A-block (mode 1) = sqrt(det) for a 1-mode block."""
    A = g[:2, :2]
    return float(np.sqrt(max(np.linalg.det(A), 0.0)))


def dS(g):
    return s_ent(nu_A(g)) - s_ent(NU_VAC)


# ---- symplectic generators (x1,p1,x2,p2 ordering)
def BS(theta):
    c, s = np.cos(theta), np.sin(theta)
    S = np.zeros((4, 4)); S[:2, :2] = c * I2; S[2:, 2:] = c * I2
    S[:2, 2:] = s * I2; S[2:, :2] = -s * I2
    return S


def TMS(r):
    c, s = np.cosh(r), np.sinh(r)
    S = np.zeros((4, 4)); S[:2, :2] = c * I2; S[2:, 2:] = c * I2
    S[:2, 2:] = s * Z2; S[2:, :2] = s * Z2
    return S


def sq_mode1(xi):
    S = np.eye(4); S[0, 0] = np.exp(xi); S[1, 1] = np.exp(-xi); return S


def rot_mix(alpha):
    """orthogonal mixing of modes 1,2 into c=(1+2)/√2 etc. — used to build a cross-cut single-mode squeeze."""
    return BS(alpha)


def is_factorizing(S, tol=1e-9):
    """S factorizes iff its A↔B off-diagonal 2×2 blocks vanish (local ⊕ local)."""
    return np.allclose(S[:2, 2:], 0, atol=tol) and np.allclose(S[2:, :2], 0, atol=tol)


def main():
    print("R4 — is non-factorization a faithful proxy for the ΔS≠0 obstruction? (gates in PREREGISTRATION.md)")
    print(f"  2-mode toy: vacuum = TMS(s={S_VAC}), ν_vac={NU_VAC:.4f}, S(A)_vac={s_ent(NU_VAC):.4f}\n")
    g0 = vacuum()
    report = {"nu_vac": NU_VAC, "S_vac": s_ent(NU_VAC)}

    # ---- R4a: straddling ≠ entangling
    # cross-cut displacement: covariance unchanged ⇒ ΔS=0 (displacement doesn't touch γ)
    dS_disp = dS(g0)                                   # identity op on covariance = displacement's effect on γ
    # cross-cut single-mode squeeze: squeeze the mode c=(1+2)/√2 → rotate, squeeze mode-1-in-c-frame, rotate back
    R = rot_mix(np.pi / 4)
    Scc = R @ sq_mode1(0.6) @ R.T
    g_cc = Scc @ g0 @ Scc.T
    dS_cc = dS(g_cc)
    r4a = abs(dS_disp) < 1e-12 and abs(dS_cc) > 1e-3
    print("  R4a straddling ≠ entangling:")
    print(f"     cross-cut DISPLACEMENT: ΔS = {dS_disp:.2e}  (straddles the cut, but γ unchanged ⇒ identity holds)")
    print(f"     cross-cut SQUEEZE:      ΔS = {dS_cc:.3f}   (entangles across the cut ⇒ identity fails)")
    print(f"     →  {'PASS ✅ — the obstruction is ΔS, not spatial straddling' if r4a else 'FAIL ❌'}")
    report["R4a"] = {"dS_displacement": dS_disp, "dS_crosscut_squeeze": dS_cc, "pass": bool(r4a)}

    # ---- R4b: ROOT-FIND (not grid) a non-factorizing ΔS=0 op. BS disentangles (ΔS<0, a 50:50 BS purifies
    #      mode A), TMS entangles (ΔS>0); so at fixed θ∈(0,π/2), ΔS(BS(θ)·TMS(r)) crosses 0 at some r*>0.
    def dS_of(th, r):
        S = BS(th) @ TMS(r)
        return dS(S @ g0 @ S.T), S
    th0 = np.pi / 6
    lo, hi = 0.0, 2.0                                  # dS(r=0)=dS_BS(θ0)<0 ; dS(r=2)>0  → bracket
    d_lo, _ = dS_of(th0, lo); d_hi, _ = dS_of(th0, hi)
    bracketed = d_lo < 0 < d_hi
    for _ in range(80):                                # bisection to machine precision
        mid = (lo + hi) / 2
        dm, Smid = dS_of(th0, mid)
        if dm < 0:
            lo = mid
        else:
            hi = mid
    rstar = (lo + hi) / 2
    d_star, S_star = dS_of(th0, rstar)
    g_star = S_star @ g0 @ S_star.T
    nonfact = not is_factorizing(S_star)
    nontrivial = not np.allclose(g_star, g0, atol=1e-6)
    r4b_found = bracketed and abs(d_star) < 1e-9 and nonfact and nontrivial
    print("\n  R4b — root-find a non-factorizing ΔS=0 op (BS disentangles, TMS entangles; bisect r at θ=π/6):")
    print(f"     bracket: ΔS(r=0)={d_lo:.4f} (<0, BS purifies A) → ΔS(r=2)={d_hi:.4f} (>0, TMS entangles)")
    print(f"     root:    r*={rstar:.6f} → ΔS={d_star:.2e}; non-factorizing={nonfact}; γ≠γ_vac={nontrivial}")
    print(f"     the op BS(π/6)·TMS(r*) genuinely entangles A↔B (off-diag blocks ≠ 0) yet leaves ΔS=0")
    print(f"     →  {'postulate TRUE ✅ — non-factorization is SUFFICIENT-BUT-NOT-NECESSARY' if r4b_found else 'not found'}")
    report["R4b"] = {"found": bool(r4b_found), "theta": th0, "r_star": rstar, "dS_at_root": d_star,
                     "nonfactorizing": bool(nonfact), "nontrivial": bool(nontrivial),
                     "bracket": [d_lo, d_hi],
                     "note": "grid-scan (60x60) missed this zero — the ΔS=0 curve exists (BS<0, TMS>0); "
                             "root-finding is the correct instrument, not sampling"}

    # verdict
    verdict = "postulate TRUE — non-factorization sufficient-but-not-necessary; obstruction = ΔS≠0 exactly (K1 wording amended)" if r4b_found else "postulate FALSE — K1 wording SURVIVES (faithful)"
    print(f"\n  VERDICT: {verdict}")
    print(f"  R4c: either way, the Longo-identity obstruction is EXACTLY ΔS≠0 (the entanglement-entropy")
    print(f"  change). R4 settles whether 'non-factorization' faithfully names it. 2-mode toy; K1's chain")
    print(f"  verdict unaffected — this is precision hygiene on the mechanism's wording.")

    OUT.mkdir(exist_ok=True)
    report["verdict"] = verdict
    (OUT / "r4_deltaS.json").write_text(json.dumps(report, indent=1))
    print(f"\n  wrote results/r4_deltaS.json")


if __name__ == "__main__":
    main()
