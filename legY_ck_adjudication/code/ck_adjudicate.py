#!/usr/bin/env python3
"""Leg Y — CK adjudication of the bridge's own catalog: is leg Q's "8" eight different spacetimes?

    /Users/sumit/Github/conjecture_machine/.venv/bin/python ck_adjudicate.py

Gates Y0/Y1/Y2 (+ the pre-registered wall Y3) frozen in ../PREREGISTRATION.md before this was written.
A falsification-flavoured self-check: leg Q's "legible <=> KY-integrable, 8/8, phi=1.0" assumes its eight
catalog entries are eight GENUINELY DIFFERENT spacetimes -- never tested, because until ansatz shipped
scripts/ck.py (S116-S118) the family had no decision procedure for the costume problem.

No preferred outcome. EQUIVALENT (our count corrects down), INEQUIVALENT (leg Q upgraded to proven) and
UNDECIDED (instrument wall) are reported identically.

Metric constructions are the BRIDGE's own (leg O survey_catalog.py / survey_zv.py forms) so Y0 is a
cross-construction check of ansatz's instrument, not a replay of their battery. ck.py + gr_engine are
imported read-only from ansatz (precedent: leg J poincare, leg X mpmath).
"""
import json
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")   # read-only

import sympy as sp

import ck                                                              # read-only
from gr_engine import Geometry                                         # read-only

OUT = Path(__file__).resolve().parent.parent / "results"
BUDGET = 600            # seconds per CK signature (pre-registered)

t, r, u, ph = sp.symbols("t r u phi", real=True)
x, y = sp.symbols("x y", real=True)
om = 1 - u**2
A = sp.Rational(3, 5)


# ---------------------------------------------------------------- the bridge's own constructions
def delta_metric(a, Dexpr, bump=1):
    """leg O survey_catalog.delta_metric — Kerr-form in rational u=cos(theta) coords."""
    a = sp.Rational(a) if not isinstance(a, sp.Expr) else a
    Sig = r**2 + a**2 * u**2
    g = sp.zeros(4)
    g[0, 0] = -(Dexpr - a**2 * om) / Sig * bump
    g[0, 3] = g[3, 0] = -a * om * (r**2 + a**2 - Dexpr) / Sig
    g[1, 1] = Sig / Dexpr
    g[2, 2] = Sig / om
    g[3, 3] = om * ((r**2 + a**2)**2 - Dexpr * a**2 * om) / Sig
    return Geometry(g, [t, r, u, ph])


def kds_metric(a, L3):
    a = sp.Rational(a); L3 = sp.Rational(L3)
    Sig = r**2 + a**2 * u**2
    Dr = (1 - L3 * r**2) * (r**2 + a**2) - 2 * r
    Du = 1 + L3 * a**2 * u**2
    Xi = 1 + L3 * a**2
    al = [1, 0, 0, -a * om]; be = [a, 0, 0, -(r**2 + a**2)]
    g = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            g[i, j] = -(Dr / (Xi**2 * Sig)) * al[i] * al[j] + (Du * om / (Xi**2 * Sig)) * be[i] * be[j]
    g[1, 1] = Sig / Dr
    g[2, 2] = Sig / (Du * om)
    return Geometry(g, [t, r, u, ph])


def taubnut_metric(m, n):
    m = sp.Rational(m); n = sp.Rational(n)
    f = (r**2 - 2 * m * r - n**2) / (r**2 + n**2)
    g = sp.zeros(4)
    g[0, 0] = -f
    g[0, 3] = g[3, 0] = 2 * f * n * u
    g[1, 1] = 1 / f
    g[2, 2] = (r**2 + n**2) / om
    g[3, 3] = om * (r**2 + n**2) - 4 * f * n**2 * u**2
    return Geometry(g, [t, r, u, ph])


def zv_geometry(delta, sigma=1):
    """leg O survey_zv.zv_geometry — exact ZV gamma-metric in prolate spheroidal (t,x,y,phi)."""
    F = ((x - 1) / (x + 1))**delta
    H = ((x**2 - 1) / (x**2 - y**2))**(delta**2)
    s2 = sp.Integer(sigma)**2
    g = sp.zeros(4)
    g[0, 0] = -F
    g[1, 1] = s2 / F * H * (x**2 - y**2) / (x**2 - 1)
    g[2, 2] = s2 / F * H * (x**2 - y**2) / (1 - y**2)
    g[3, 3] = s2 / F * (x**2 - 1) * (1 - y**2)
    return Geometry(g, [t, x, y, ph])


def schwarzschild_std():
    """Standard Schwarzschild (t,r,theta,phi) with M=1 — a DIFFERENT chart from zv_geometry(1)."""
    th = sp.Symbol("theta", real=True)
    f = 1 - 2 / r
    return Geometry(sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2), [t, r, th, ph])


ENTRIES = {
    "Kerr":            (lambda: delta_metric(A, r**2 - 2 * r + A**2), [r > 3, u > 0, u < 1]),
    "Kerr-Newman":     (lambda: delta_metric(A, r**2 - 2 * r + A**2 + sp.Rational(1, 4)),
                        [r > 3, u > 0, u < 1]),
    "Kerr-de Sitter":  (lambda: kds_metric(A, sp.Rational(1, 100)), [r > 3, u > 0, u < 1]),
    "Taub-NUT":        (lambda: taubnut_metric(1, sp.Rational(1, 2)), [r > 3, u > 0, u < 1]),
    "ZV d=1":          (lambda: zv_geometry(1), [x > 2, y > 0, y < 1]),
    "Schwarzschild(std chart)": (schwarzschild_std, [r > 3]),
    "ZV d=2":          (lambda: zv_geometry(2), [x > 2, y > 0, y < 1]),
    "bumpy eps=0.35":  (lambda: delta_metric(A, r**2 - 2 * r + A**2,
                                             bump=1 + sp.Rational(7, 20) * 6 * u**2 / r),
                        [r > 3, u > 0, u < 1]),
}

Y1_SET = ["Kerr", "Kerr-Newman", "Kerr-de Sitter", "Taub-NUT", "ZV d=1"]
Y2_SET = ["bumpy eps=0.35", "ZV d=2"]          # MN handled separately (see note)


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def signature(name):
    """CK signature with the pre-registered time budget; wall-timeouts recorded distinctly."""
    build, dom = ENTRIES[name]
    t0 = time.time()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(BUDGET)
    try:
        ck.set_domain(*dom)
        sig = ck.ck_signature(build(), label=name)
        signal.alarm(0)
        return sig, time.time() - t0, None
    except Timeout:
        signal.alarm(0)
        return {"error": f"WALL: exceeded {BUDGET}s"}, time.time() - t0, "wall"
    except Exception as e:
        signal.alarm(0)
        return {"error": f"{type(e).__name__}: {str(e)[:160]}"}, time.time() - t0, "procedure"
    finally:
        signal.alarm(0)


def main():
    print("LEG Y — CK adjudication of the bridge's own catalog (gates frozen in PREREGISTRATION.md)")
    print(f"  auditing leg Q's independence assumption; budget {BUDGET}s/signature; no preferred outcome\n")
    sigs, meta = {}, {}
    for name in ENTRIES:
        s, dt, kind = signature(name)
        sigs[name], meta[name] = s, {"seconds": round(dt, 1), "fail": kind}
        status = "ok" if "error" not in s else f"UNDECIDED({kind}) — {s['error'][:60]}"
        petrov = s.get("petrov", "-")
        print(f"  signature {name:28s} {dt:7.1f}s  Petrov {str(petrov):4s}  {status}")

    def verdict(a, b):
        v, why = ck.equivalent(sigs[a], sigs[b])
        return str(v), [str(w) for w in (why or [])]

    report = {"budget_s": BUDGET, "timing": meta, "Y0": {}, "Y1": {}, "Y2": {}}

    # ---- Y0 instrument cross-check
    v, why = verdict("ZV d=1", "Schwarzschild(std chart)")
    y0 = (v == str(ck.EQUIVALENT))
    print(f"\n  Y0 cross-construction check — bridge's ZV δ=1 vs standard-chart Schwarzschild:")
    print(f"     {v}  {why}")
    print(f"     →  {'PASS ✅ — ansatz §116 reproduced through the bridge s own construction' if y0 else 'FAIL ❌ / UNDECIDED — downstream verdicts NOT trustworthy'}")
    report["Y0"] = {"verdict": v, "why": why, "pass": bool(y0)}

    # ---- Y1 integrable entries pairwise
    print(f"\n  Y1 — are leg Q's integrable entries distinct spacetimes?")
    y1_pairs, y1_bad, y1_und = [], [], []
    for i in range(len(Y1_SET)):
        for j in range(i + 1, len(Y1_SET)):
            a, b = Y1_SET[i], Y1_SET[j]
            v, why = verdict(a, b)
            y1_pairs.append({"a": a, "b": b, "verdict": v, "why": why})
            mark = "✅" if v == str(ck.INEQUIVALENT) else ("⚠️ DUPLICATE" if v == str(ck.EQUIVALENT) else "· undecided")
            if v == str(ck.EQUIVALENT):
                y1_bad.append((a, b))
            elif v != str(ck.INEQUIVALENT):
                y1_und.append((a, b))
            print(f"     {a:16s} vs {b:16s} → {v:12s} {mark}")
    report["Y1"] = {"pairs": y1_pairs, "duplicates": y1_bad, "undecided": [list(p) for p in y1_und]}
    print(f"     duplicates found: {len(y1_bad)}   undecided: {len(y1_und)}")

    # ---- Y2 the non-integrable classes (the claim at risk)
    print(f"\n  Y2 — leg Q's 'independent non-integrable classes' (the exposed claim):")
    y2_pairs = []
    for i in range(len(Y2_SET)):
        for j in range(i + 1, len(Y2_SET)):
            a, b = Y2_SET[i], Y2_SET[j]
            v, why = verdict(a, b)
            y2_pairs.append({"a": a, "b": b, "verdict": v, "why": why})
            print(f"     {a:16s} vs {b:16s} → {v:12s}  {why}")
    report["Y2"] = {"pairs": y2_pairs,
                    "MN_note": ("Manko-Novikov q=0.5 not attempted in v1: rotating + genuinely "
                                "two-variable (r AND theta), the regime ansatz records as blowing up the "
                                "algebra engine (killed 7.5h runs). Pre-registered Y3 wall; the "
                                "bumpy-vs-MN pair therefore remains ASSUMED-distinct, stated as such.")}

    OUT.mkdir(exist_ok=True)
    (OUT / "ck_adjudication.json").write_text(json.dumps(report, indent=1, default=str))
    print(f"\n  wrote results/ck_adjudication.json")


if __name__ == "__main__":
    main()
