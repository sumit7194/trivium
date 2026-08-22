"""G3 gate: regenerate every headline number in FINDINGS_BOUNDARY.md from the
banked JSONs, and assert them.

WHY THIS EXISTS: an audit prompted by quantum found that G3's decisive numbers --
Fisher p=1.0000, the 2/312 vs 3/317 counts, and the re-measured control at
1254/1238 that WITHDREW the FINDINGS headline -- existed only in FINDINGS and in
messages. They were computed in `python -c` one-liners whose terminals have
scrolled away. The scans are on disk; the quantities quoted FROM them were not.

That is quantum's heredoc hazard on my own most consequential result: a withdrawal
that nobody, including me, could reproduce from the repo.
"""
import json, sys
import numpy as np
from scipy.stats import fisher_exact, ks_2samp, beta
from pathlib import Path
R = Path(__file__).resolve().parent.parent / "results"
ok = True
def check(label, got, want, tol=None):
    global ok
    good = abs(got-want) <= (tol if tol is not None else 0)
    ok &= good
    print(f"  {'PASS' if good else '*** FAIL ***'}  {label:<46} {got!r}"
          + ("" if good else f"   expected {want!r}"))

d = json.load(open(R/"g3_power.json"))["orbits"]
A, B = d["1.3"], d["1.5"]
nA, eA = len(A), sum(1 for v in A.values() if v["escaped"])
nB, eB = len(B), sum(1 for v in B.values() if v["escaped"])
print("B1 — the decisive test")
check("delta=1.3 orbits", nA, 312); check("delta=1.3 escapes", eA, 2)
check("delta=1.5 orbits", nB, 317); check("delta=1.5 escapes", eB, 3)
p = fisher_exact([[eA,nA-eA],[eB,nB-eB]])[1]
check("Fisher exact p", round(p,4), 1.0)
print(f"    -> BOUNDARY {'NOT SUPPORTED' if p>=0.05 else 'REAL'}  (frozen rule: p>=0.05)")

print("B3 — drift still separates nothing at 3x the sample")
for est, want in (("drift_fft",0.9944), ("drift_naff",0.8840)):
    a = np.log10([v[est] for v in A.values() if v.get(est) and v[est]>0])
    b = np.log10([v[est] for v in B.values() if v.get(est) and v[est]>0])
    check(f"KS p ({est})", round(ks_2samp(a,b).pvalue,4), want, 1e-4)

print("B4 — A1 guard inert")
dh = [v["dH"] for v in list(A.values())+list(B.values())]
check("orbits", len(dh), 629); check("rejections at DH_MAX=1e-4", sum(1 for x in dh if x>=1e-4), 0)

print("CONTROL RE-MEASUREMENT — the numbers that WITHDREW the headline")
for f, want_n, want_r in (("g3_control",320,1254), ("g3_control_spacing",160,1238)):
    o = json.load(open(R/f"{f}.json"))["orbits"]["1.0"]
    dr = [v["drift_fft"] for v in o.values() if v.get("drift_fft") and v["drift_fft"]>0]
    r = max(dr)/np.median(dr)
    check(f"{f}: n", len(o), want_n)
    check(f"{f}: max/median", round(r), want_r, 1)
S = json.load(open(R/"g3_overnight.json"))["scan"]
lad = {k: v["max_drift"]/v["floor"] for k,v in S.items() if k != "1.0"}
above = sum(1 for v in lad.values() if v > 1254)
check("deformed delta ABOVE the re-measured control", above, 4)
check("original control max/median (now known inflated)", round(S["1.0"]["max_drift"]/S["1.0"]["floor"]), 2980, 1)
print(f"\n  {'ALL ASSERTIONS PASS' if ok else '*** SOME ASSERTIONS FAILED ***'}")
sys.exit(0 if ok else 1)
