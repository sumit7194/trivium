#!/usr/bin/env python3
"""Move G — falsifying Move D's "no chaos": is SALI valid, and does the bump ever reach chaos?

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python falsify_moveD_chaos.py

Move D claims SALI stays regular (no chaos) for the bump up to ε=0.35. Two failure modes:
  (i)  SALI is insensitive — it would say 'regular' even for a chaotic system → 'no chaos' vacuous.
  (ii) we just did not push ε high enough — chaos appears beyond 0.35.
Controls: (A) a POSITIVE control — a φ-dependent (non-axisymmetric) bump removes L_z conservation
and should be CHAOTIC; if SALI does not drop there, SALI is broken. (B) push the real axisymmetric
bump to high ε and aggressive orbits; does SALI ever drop?
"""
import math
import sys
import json
from pathlib import Path

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from numeric_curvature import christoffel_numeric
sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as ex

RESULTS = Path(__file__).resolve().parent.parent / "results"
N = 4
A = 0.6


def g_bump_axi(x, eps):
    """The Move D bump (axisymmetric): g_tt → g_tt·(1+ε cos²θ·6/r)."""
    g = ex.g_kerr_newman(x, A, 0.0)
    g[0][0] *= (1.0 + eps * math.cos(x[2])**2 * (6.0 / x[1]))
    return g


def g_bump_chaotic(x, eps):
    """POSITIVE control: a φ-DEPENDENT bump → breaks axial symmetry (L_z not conserved) → chaotic."""
    g = ex.g_kerr_newman(x, A, 0.0)
    g[0][0] *= (1.0 + eps * math.cos(x[2])**2 * math.cos(2.0 * x[3]) * (6.0 / x[1]))
    return g


def sali(gfun, x0, u0, steps=2000, dtau=0.2, delta=1e-7, r_lo=2.0, r_hi=60.0):
    def rhs(s):
        x, u = s[:N], s[N:]
        G = christoffel_numeric(gfun, x)
        a = [-sum(G[i][b][c]*u[b]*u[c] for b in range(N) for c in range(N)) for i in range(N)]
        return list(u) + a

    def rk4(s):
        k1 = rhs(s); k2 = rhs([s[i]+dtau/2*k1[i] for i in range(2*N)])
        k3 = rhs([s[i]+dtau/2*k2[i] for i in range(2*N)]); k4 = rhs([s[i]+dtau*k3[i] for i in range(2*N)])
        return [s[i]+dtau/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(2*N)]

    ref = list(x0)+list(u0); s1 = list(ref); s1[2] += delta; s2 = list(ref); s2[6] += delta
    out = []
    for k in range(steps):
        if not (r_lo < ref[1] < r_hi):
            break
        ref, s1, s2 = rk4(ref), rk4(s1), rk4(s2)
        if k % 20 == 0 and k > 0:
            v1 = [s1[i]-ref[i] for i in range(2*N)]; v2 = [s2[i]-ref[i] for i in range(2*N)]
            n1 = math.sqrt(sum(v*v for v in v1)); n2 = math.sqrt(sum(v*v for v in v2))
            if n1 < 1e-30 or n2 < 1e-30: break
            v1 = [v/n1 for v in v1]; v2 = [v/n2 for v in v2]
            out.append(min(math.sqrt(sum((v1[i]+v2[i])**2 for i in range(2*N))),
                           math.sqrt(sum((v1[i]-v2[i])**2 for i in range(2*N)))))
            s1 = [ref[i]+delta*v1[i] for i in range(2*N)]; s2 = [ref[i]+delta*v2[i] for i in range(2*N)]
    return min(out) if out else float("nan")


def min_sali_over_orbits(gfun, n_orbits=8):
    vals = []
    for (x0, u0) in ex.gen_launches(gfun, (5, 6, 7, 8))[:n_orbits]:
        v = sali(gfun, x0, u0)
        if v == v:
            vals.append(v)
    return (min(vals) if vals else float("nan")), (sorted(vals)[len(vals)//2] if vals else float("nan"))


def main():
    print("MOVE G — falsifying Move D's 'no chaos': is SALI valid, and does the bump reach chaos?\n")
    res = {}

    # (A) POSITIVE control: φ-dependent (chaotic) bump — SALI MUST drop here or it is broken
    print("  [A] SALI positive control (φ-dependent bump, axial symmetry broken → expect CHAOS):")
    for eps in (0.35, 0.6):
        mn, md = min_sali_over_orbits(lambda x: g_bump_chaotic(x, eps))
        res[f"chaotic_eps{eps}"] = {"min": mn, "median": md}
        print(f"    ε={eps}: min-SALI={mn:.2e}  median={md:.2e}  {'→ CHAOS detected (SALI works ✅)' if mn < 0.1 else '→ still regular?!'}")

    # (B) push the REAL axisymmetric bump to high ε — does it ever go chaotic?
    print("\n  [B] real axisymmetric bump pushed to high ε (does chaos appear beyond 0.35?):")
    for eps in (0.35, 0.6, 1.0, 1.5):
        mn, md = min_sali_over_orbits(lambda x: g_bump_axi(x, eps))
        res[f"axi_eps{eps}"] = {"min": mn, "median": md}
        print(f"    ε={eps}: min-SALI={mn:.2e}  median={md:.2e}  {'→ CHAOS' if mn < 0.1 else '→ regular'}")

    sali_works = any(res[k]["min"] < 0.1 for k in res if k.startswith("chaotic"))
    axi_chaos = any(res[k]["min"] < 0.1 for k in res if k.startswith("axi"))
    print(f"\n  SALI detects chaos on the positive control? {sali_works}")
    print(f"  the real axisymmetric bump reaches chaos by ε=1.5? {axi_chaos}")
    if not sali_works:
        verdict = "INCONCLUSIVE — SALI did not fire even on the chaotic control; the 'no chaos' claim is unsupported."
    elif not axi_chaos:
        verdict = "SURVIVED ✅ — SALI works (fires on the chaotic control) yet the real axisymmetric bump stays regular even to ε=1.5; 'no chaos' is robust (the bump preserves KAM tori far beyond 0.35)."
    else:
        verdict = "REFINED — SALI works; the real bump DOES reach chaos at high ε (locates the chaos boundary above 0.35, as Move D bounded it)."
    print(f"\n  MOVE D 'no chaos' VERDICT: {verdict}")
    res["verdict"] = verdict; res["sali_validated"] = sali_works; res["axi_reaches_chaos"] = axi_chaos
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "falsify_moveD_chaos.json").write_text(json.dumps(res, indent=1, default=float))
    print("  wrote results/falsify_moveD_chaos.json")


if __name__ == "__main__":
    main()
