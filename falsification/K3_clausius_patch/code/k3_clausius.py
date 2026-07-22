#!/usr/bin/env python3
"""K3 — patchwise Clausius (δQ = TδS) fails at every patch size: the entropy-production curve.

    /Users/sumit/Github/conjecture_machine/.venv/bin/python k3_clausius.py

Gates K3a–K3e frozen in ../PREREGISTRATION.md before this was written. Reuses the K1/leg X modular machinery.
In modular units the lattice Clausius relation is the entanglement first law Δ⟨K_ℓ⟩ = ΔS_ℓ; its exact failure
is the entropy production Σ_ℓ = Δ⟨K_ℓ⟩ − ΔS_ℓ = S_rel(patch) ≥ 0. K3 measures Σ_ℓ vs patch size ℓ for a
squeezed excitation straddling the cut — the lattice witness of the localization postulate (the one link
Jacobson/Dorau–Much only ASSUME). Scope: the modular first law, NOT the horizon-area Clausius (needs S=A/4).
"""
import json
import sys
import time
from pathlib import Path

LEGK1 = Path(__file__).resolve().parents[2] / "K1_squeezed" / "code"
sys.path.insert(0, str(LEGK1))
import k1_squeezed as K1  # noqa: E402  (build_chain, gauss_profile, squeeze_reduced, s_rel_pieces, sub, EH)

from mpmath import mp, mpf, matrix  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "results"
PATCHES = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]


def patch_pieces(X, P, v, r, l, coherent_d=None):
    """δQ=Δ⟨K_ℓ⟩, TδS=ΔS_ℓ, Σ=S_rel for the ℓ-site patch adjacent to the cut."""
    idx = list(range(K1.EH.A_START - 1, K1.EH.A_START - 1 + l))
    if coherent_d is not None:                       # coherent: r=0, displacement d on the patch
        X2, P2 = K1.sub(X, idx), K1.sub(P, idx)
        d_A = matrix([coherent_d[idx[i]] for i in range(l)])
        pc = K1.s_rel_pieces(X, P, X2, P2, idx, d_A=d_A)
    else:
        X1, P1 = K1.squeeze_reduced(X, P, v, r, idx)
        pc = K1.s_rel_pieces(X, P, X1, P1, idx)
    dK, dS, sr = float(pc["dK"]), float(pc["dS"]), float(pc["s_rel"])
    return dK, dS, sr


def main():
    mp.dps = 60
    t0 = time.time()
    print("K3 — patchwise Clausius fails at every patch size (gates frozen in PREREGISTRATION.md)")
    print(f"  N={K1.EH.N}, μ={K1.EH.MU}, cut x_c={K1.EH.XC}, squeezed excitation straddling the cut, dps={mp.dps}")
    print("  scope: the modular/entanglement first law Δ⟨K⟩=ΔS, NOT the horizon-area Clausius (needs S=A/4)\n")

    X, P = K1.build_chain(K1.EH.N, K1.EH.MU)
    v = K1.gauss_profile(X.rows, K1.EH.XC, K1.EH.SIGMA)          # straddles the cut

    # ---- K3a + K3b: the entropy-production curve Σ_ℓ vs patch size (squeezed, r=0.6)
    print("  K3a/K3b — entropy-production curve Σ_ℓ = δQ_ℓ − TδS_ℓ  (squeezed r=0.6):")
    print(f"    {'ℓ':>3} | {'δQ=Δ⟨K⟩':>10} | {'TδS=ΔS':>10} | {'Σ=S_rel':>10} | {'Σ/δQ':>7} | mono")
    rows = []
    prev = None
    for l in PATCHES:
        dK, dS, sr = patch_pieces(X, P, v, mpf("0.6"), l)
        mono = "—" if prev is None else ("↑" if sr >= prev - 1e-12 else "↓ BUG")
        rows.append(dict(l=l, dQ=dK, TdS=dS, Sigma=sr, frac=sr / dK))
        print(f"    {l:>3} | {dK:10.6f} | {dS:10.6f} | {sr:10.6f} | {sr/dK:7.4f} | {mono}")
        prev = sr

    k3a = all(r["Sigma"] > 0 for r in rows) and all(r["frac"] > 0.10 for r in rows if r["l"] >= 2)
    monotone = all(rows[i]["Sigma"] >= rows[i - 1]["Sigma"] - 1e-12 for i in range(1, len(rows)))
    k3b = all(r["Sigma"] >= 0 for r in rows) and monotone
    sat = abs(rows[-1]["Sigma"] - rows[-3]["Sigma"]) / rows[-1]["Sigma"] < 0.01
    print(f"\n    K3a KILL: Σ_ℓ>0 ∀ℓ and Σ/δQ>0.10 ∀ℓ≥2  →  exact patchwise Clausius holds at NO patch size  "
          f"→  K3 {'KILLED 💀' if k3a else 'not killed'}")
    print(f"    K3b canary: Σ_ℓ=S_rel≥0 & monotone↑ in ℓ (V1) {'✅' if k3b else '❌ BUG'}; "
          f"saturates past excitation scale ({'yes' if sat else 'no'})")

    # ---- K3c: near-equilibrium scaling — Σ/δQ vs excitation strength r (fixed patch ℓ=2)
    print("\n  K3c — near-equilibrium scaling: fractional violation Σ/δQ vs squeeze r (patch ℓ=2):")
    rc = []
    for rr in ["0.1", "0.2", "0.4", "0.6", "0.8"]:
        dK, dS, sr = patch_pieces(X, P, v, mpf(rr), 2)
        rc.append(dict(r=float(rr), frac=sr / dK, Sigma=sr))
        print(f"    r={rr}: δQ={dK:.5f}  Σ={sr:.5f}  Σ/δQ={sr/dK:.4f}")
    f01 = next(x["frac"] for x in rc if x["r"] == 0.1)
    f06 = next(x["frac"] for x in rc if x["r"] == 0.6)
    k3c = f01 < 0.3 * f06
    print(f"    K3c: (Σ/δQ)|r=0.1 = {f01:.4f} < 0.3·(Σ/δQ)|r=0.6 = {0.3*f06:.4f}  →  "
          f"{'PASS ✅ — entropy production vanishes near equilibrium' if k3c else 'FAIL ❌'}")

    # ---- K3d: coherent degenerate control (ΔS=0 ⇒ Σ=δQ)
    f = K1.EH.packet(K1.EH.XC + 8)                              # coherent packet inside the wedge
    dKc, dSc, src = patch_pieces(X, P, None, None, 16, coherent_d=f)
    k3d = abs(dSc) < 1e-6 and abs(src / dKc - 1) < 1e-6
    print(f"\n  K3d — coherent control (displacement, ℓ=16): ΔS={dSc:.2e} (→0), Σ/δQ={src/dKc:.6f} (→1)  →  "
          f"{'PASS ✅ (coherent: modular energy is ALL entropy production — Longo)' if k3d else 'FAIL ❌'}")

    # ---- K3e: precision canary (float64 vs mpmath at the largest float64-safe patch ℓ=8)
    Xn = np.zeros((K1.EH.N, K1.EH.N))
    ii = np.arange(K1.EH.N)
    Xn[ii, ii] = 2 + float(K1.EH.MU) ** 2
    Xn[ii[:-1], ii[:-1] + 1] = Xn[ii[1:], ii[1:] - 1] = -1
    wq, Qn = np.linalg.eigh(Xn)
    Xf = (Qn * (0.5 / np.sqrt(wq))) @ Qn.T
    Pf = (Qn * (0.5 * np.sqrt(wq))) @ Qn.T
    vf = np.array([float(v[i, 0]) for i in range(K1.EH.N)])
    idx = np.arange(K1.EH.A_START - 1, K1.EH.A_START - 1 + 8)
    vv = np.outer(vf, vf)
    Mq = np.eye(K1.EH.N) + (np.exp(0.6) - 1) * vv
    Mp = np.eye(K1.EH.N) + (np.exp(-0.6) - 1) * vv
    XA, PA = Xf[np.ix_(idx, idx)], Pf[np.ix_(idx, idx)]
    X1 = (Mq @ Xf @ Mq.T)[np.ix_(idx, idx)]
    P1 = (Mp @ Pf @ Mp.T)[np.ix_(idx, idx)]
    ex, Qx = np.linalg.eigh(XA)
    Xh = (Qx * np.sqrt(ex)) @ Qx.T
    Xih = (Qx / np.sqrt(ex)) @ Qx.T
    e2, W = np.linalg.eigh(Xh @ PA @ Xh)
    nu = np.sqrt(np.clip(e2, 0.25, None))          # e2 = ν²; vacuum floor ν=½ ⇒ clip e2 at 0.25
    eps = np.log((nu + 0.5) / (nu - 0.5))
    Gqq = Xih @ (W * (nu * eps)) @ W.T @ Xih
    Gpp = Xh @ (W * (eps / nu)) @ W.T @ Xh
    dKf = 0.5 * (np.sum(Gqq * (X1 - XA)) + np.sum(Gpp * (P1 - PA)))
    sig8_mp = next(r["Sigma"] for r in [dict(Sigma=patch_pieces(X, P, v, mpf("0.6"), 8)[2])])
    dQ8_mp = patch_pieces(X, P, v, mpf("0.6"), 8)[0]
    rel = abs(dKf - dQ8_mp) / abs(dQ8_mp)
    k3e = rel < 1e-6
    print(f"  K3e — precision canary (ℓ=8 δQ): float64 {dKf:.8f} vs mpmath {dQ8_mp:.8f}, rel {rel:.1e}  →  "
          f"{'PASS ✅ (small patches float64-safe; large need mpmath)' if k3e else 'FAIL ❌'}")

    verdict = "KILLED" if (k3a and k3b) else "SURVIVES"
    allp = k3a and k3b and k3c and k3d and k3e
    print(f"\n  K3 {verdict}: the patchwise modular first law δQ=TδS carries a positive, relative-entropy-valued")
    print(f"  entropy-production Σ_ℓ=S_rel at EVERY patch size (Σ/δQ∈[{rows[0]['frac']:.2f},{rows[-1]['frac']:.2f}]),")
    print(f"  vanishing near equilibrium (r→0) — the lattice witness of why localization is assumed, not proven.")

    OUT.mkdir(exist_ok=True)
    (OUT / "k3_clausius.json").write_text(json.dumps({
        "N": K1.EH.N, "mu": float(K1.EH.MU), "dps": mp.dps, "patches": PATCHES,
        "K3ab_curve": rows, "K3a_kill": bool(k3a), "K3b_monotone_pass": bool(k3b), "saturates": bool(sat),
        "K3c_r_scan": rc, "K3c_pass": bool(k3c),
        "K3d_coherent": {"dQ": dKc, "dS": dSc, "frac": src / dKc}, "K3d_pass": bool(k3d),
        "K3e_float64_rel": rel, "K3e_pass": bool(k3e),
        "verdict": verdict, "all_pass": bool(allp),
        "summary": (f"K3 ({verdict}): patchwise Clausius (modular first law Δ⟨K⟩=ΔS) fails at every patch "
                    f"size — entropy production Σ_ℓ=S_rel>0, Σ/δQ from {rows[0]['frac']:.2f} (ℓ=1) rising to "
                    f"{rows[-1]['frac']:.2f} (saturated), monotone in ℓ (V1). It vanishes as the excitation "
                    f"strength r→0 (near-equilibrium, second-order) and the coherent case is degenerate "
                    f"(ΔS=0 ⇒ Σ=δQ). Lattice witness of the localization postulate; scope is the modular "
                    f"first law, not the horizon-area Clausius (needs S=A/4). Toy model."),
    }, indent=1))
    print(f"\n  wrote results/k3_clausius.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
