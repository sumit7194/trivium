#!/usr/bin/env python3
"""R9 — was R6's non-universal log a real result, or a truncated fit?

    python3 r9_ladder.py

Gates frozen in ../PREREGISTRATION.md. R6 measured b = 2.32/3.72/0.52 across three regulators and called it
KILLED. Its MECHANISM was retracted today: R6 was D=4 spacetime (EVEN), where a universal log SHOULD exist.
R6's own pre-registration named the suspect and the write-up talked past it — "further subleading terms that
a 3-parameter fit may fold into b".

S(n) = a n^2 + b log n + c is a TRUNCATION. If the true expansion carries 1/n, 1/n^2 ... a 3-parameter fit
has nowhere to put them but into b, and how much leaks in can depend on the regulator — manufacturing a
spread out of a universal quantity. R9 climbs the model ladder and watches the spread.

Applies L12 (a residual needs BOTH a floor probe and a limit probe) and tabula's conditioning lesson to our
own fit basis, which is badly conditioned by construction. numpy only; bridge-solo.
"""
import json
import sys
from pathlib import Path

import numpy as np

M2DIR = Path(__file__).resolve().parents[2] / "M2_arealaw" / "code"
sys.path.insert(0, str(M2DIR))
import m2_arealaw as M2

OUT = Path(__file__).resolve().parent.parent / "results"
N, L0 = 200, 500
NS = list(range(6, 45, 2))                 # 20 radii — a 5-param fit on R6's 9 was never a fit
NS_R6 = [8, 12, 16, 20, 24, 28, 32, 36, 40]
COND_MAX = 1e10                            # R9c: above this the fit basis is collinear, verdict excluded
REGS = [("R1 bare", M2.K_bare), ("R2 improved", M2.K_impr), ("R3 higher-deriv", M2.K_hd)]
R6_REF = [2.3216, 3.7185, 0.5221]

# the model ladder: each entry builds the design columns for a radius vector
MODELS = {
    "M2  n²+c":                 lambda n: [n ** 2, np.ones_like(n)],
    "M3  +b·log n  (R6's)":     lambda n: [n ** 2, np.log(n), np.ones_like(n)],
    "M4  +d/n":                 lambda n: [n ** 2, np.log(n), np.ones_like(n), 1.0 / n],
    "M5  +e/n²":                lambda n: [n ** 2, np.log(n), np.ones_like(n), 1.0 / n, 1.0 / n ** 2],
}
B_INDEX = {"M2  n²+c": None, "M3  +b·log n  (R6's)": 1, "M4  +d/n": 1, "M5  +e/n²": 1}


def fit(ns, S, model):
    n = np.asarray(ns, float)
    A = np.vstack(MODELS[model](n)).T
    coef, *_ = np.linalg.lstsq(A, S, rcond=None)
    sv = np.linalg.svd(A / np.linalg.norm(A, axis=0, keepdims=True), compute_uv=False)
    return coef, float(sv[0] / sv[-1])


def b_with_jackknife(ns, S, model):
    i = B_INDEX[model]
    if i is None:
        return None, None, None
    coef, cond = fit(ns, S, model)
    bs = []
    for k in range(len(ns)):
        keep = [j for j in range(len(ns)) if j != k]
        c2, _ = fit([ns[j] for j in keep], S[keep], model)
        bs.append(c2[i])
    return float(coef[i]), float(np.std(bs)), cond


def main():
    print("R9 — was R6's non-universal log a real result, or a truncated fit? (gates in PREREGISTRATION.md)")
    print(f"  M2/R6 pipeline verbatim; radii extended to {len(NS)} values (R6 used {len(NS_R6)})\n")
    rep = {"N": N, "L0": L0, "ns": NS, "ns_r6": NS_R6}

    S_full, S_r6 = {}, {}
    for name, Kf in REGS:
        S_full[name] = np.array(M2.extract_kappa(Kf, N, NS, L0)["S_ext"])
        S_r6[name] = np.array(M2.extract_kappa(Kf, N, NS_R6, L0)["S_ext"])

    # ---- R9a regression against R6
    got = [b_with_jackknife(NS_R6, S_r6[n], "M3  +b·log n  (R6's)")[0] for n, _ in REGS]
    dev = max(abs(g - r) / abs(r) for g, r in zip(got, R6_REF))
    r9a = dev < 0.05
    print(f"  R9a — regression (R6's model, R6's radii): b = "
          f"{', '.join(f'{g:.3f}' for g in got)}  vs R6's {R6_REF}")
    print(f"     max deviation {dev*100:.2f}%  →  R9a {'PASS ✅' if r9a else 'FAIL ❌ — later gates VOID'}")
    rep["R9a"] = {"b_now": got, "b_r6": R6_REF, "max_dev": dev, "pass": bool(r9a)}
    if not r9a:
        rep["verdict"] = "VOID — R9a regression failed"
        OUT.mkdir(exist_ok=True); (OUT / "r9_ladder.json").write_text(json.dumps(rep, indent=1))
        print("\n  VERDICT: VOID"); return

    # ---- R9b/c/d the ladder
    print(f"\n  R9b/c/d — the model ladder on {len(NS)} radii (Δ_b = across-regulator spread of b):")
    print(f"     {'model':24s} | {'b bare':>8} {'impr':>8} {'hd':>8} | {'Δ_b':>8} | {'mean jk err':>11} | {'cond':>9} | ok?")
    ladder = {}
    for m in MODELS:
        if B_INDEX[m] is None:
            continue
        bs, errs, conds = [], [], []
        for name, _ in REGS:
            b, e, c = b_with_jackknife(NS, S_full[name], m)
            bs.append(b); errs.append(e); conds.append(c)
        spread = float(max(bs) - min(bs))
        err = float(np.mean(errs)); cond = float(max(conds))
        ok = cond <= COND_MAX
        ladder[m] = {"b": bs, "spread": spread, "jk_err": err, "cond": cond, "reliable": bool(ok)}
        print(f"     {m:24s} | {bs[0]:8.3f} {bs[1]:8.3f} {bs[2]:8.3f} | {spread:8.3f} | {err:11.3f} | "
              f"{cond:9.2e} | {'yes' if ok else 'NO — UNRELIABLE'}")
    rep["ladder"] = ladder

    reliable = {m: v for m, v in ladder.items() if v["reliable"]}
    d3 = ladder["M3  +b·log n  (R6's)"]["spread"]
    print(f"\n     floor probe (L12): is Δ_b above the jackknife noise at each order? "
          f"{ {m: round(v['spread']/v['jk_err'],1) for m,v in reliable.items()} } (×error)")

    if "M5  +e/n²" in reliable:
        top, dtop = "M5  +e/n²", reliable["M5  +e/n²"]
    elif "M4  +d/n" in reliable:
        top, dtop = "M4  +d/n", reliable["M4  +d/n"]
    else:
        top, dtop = None, None

    # ---- L12's LIMIT probe, made operational: does b itself CONVERGE as the model is extended?
    # The condition number (R9c) said "fine" at every order while b swung by tens — the conditioning proxy
    # was the CONVENIENT quantity, not the right one (L8, on our own gate). The right test is whether the
    # ESTIMATE moves by more than its own error between orders.
    orders = [m for m in ["M3  +b·log n  (R6's)", "M4  +d/n", "M5  +e/n²"] if m in ladder]
    drifts = []
    for a, bb in zip(orders, orders[1:]):
        for k in range(3):
            d = abs(ladder[bb]["b"][k] - ladder[a]["b"][k])
            drifts.append(d / max(ladder[bb]["jk_err"], 1e-300))
    max_drift = float(max(drifts)) if drifts else 0.0
    unstable = max_drift > 3.0
    print(f"     limit probe (L12): max |Δb| between consecutive orders = {max_drift:.1f}× its own jackknife "
          f"error  →  {'UNSTABLE — b does not converge' if unstable else 'stable'}")
    rep["stability"] = {"max_drift_in_errors": max_drift, "unstable": bool(unstable)}

    if unstable:
        verdict = (f"UNDECIDED(extraction unstable) — b does not CONVERGE as the model is extended: it moves "
                   f"by up to {max_drift:.0f}× its own jackknife error between consecutive orders (bare "
                   f"{ladder[orders[0]]['b'][0]:.2f}→{ladder[orders[-1]]['b'][0]:.2f}, higher-deriv "
                   f"{ladder[orders[0]]['b'][2]:.2f}→{ladder[orders[-1]]['b'][2]:.2f}). L12: the spread is "
                   f"above the noise FLOOR at every order but has no LIMIT, so neither 'truncation artifact' "
                   f"nor 'robust measurement' is established. R6 stays UNDECIDED — and we now know why: this "
                   f"instrument cannot stably extract b at all.")
    elif top is None:
        verdict = ("UNDECIDED(conditioning) — every extended model is ill-conditioned on this radius range; "
                   "the ladder cannot decide and R6 stays UNDECIDED.")
    elif dtop["spread"] < 0.5 * d3 and dtop["spread"] < dtop["jk_err"]:
        verdict = (f"postulate TRUE — R6's spread was a TRUNCATION ARTIFACT: at {top.strip()} the "
                   f"across-regulator spread falls to {dtop['spread']:.3f}, below the jackknife error "
                   f"{dtop['jk_err']:.3f}. The regulators are consistent; R6's kill does not survive model "
                   f"extension and b is consistent with being universal.")
    elif dtop["spread"] >= 0.5 * d3:
        verdict = (f"postulate FALSE — R6's measurement is ROBUST: the spread survives model extension "
                   f"({d3:.3f} at M3 → {dtop['spread']:.3f} at {top.strip()}). The truncation suspect is "
                   f"cleared and the puzzle deepens — a universal log is expected at D=4 but we do not see one.")
    else:
        verdict = (f"PARTIAL — spread falls to {dtop['spread']:.3f} (from {d3:.3f}) but not below the "
                   f"jackknife error {dtop['jk_err']:.3f}; a weakening, not a resolution. R6 stays UNDECIDED.")

    print(f"\n  VERDICT: {verdict}")
    print(f"\n  Note (L10): no theoretical value of b was asserted or compared against — the gate is the three")
    print(f"  regulators against EACH OTHER, which is what R6's own pre-registration required and its")
    print(f"  FINDINGS then violated. 'Consistent with universal' is the most that can be claimed here.")

    rep["verdict"] = verdict
    OUT.mkdir(exist_ok=True)
    (OUT / "r9_ladder.json").write_text(json.dumps(rep, indent=1))
    print(f"\n  wrote results/r9_ladder.json")


if __name__ == "__main__":
    main()
