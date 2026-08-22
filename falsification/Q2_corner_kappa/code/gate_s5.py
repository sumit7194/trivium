"""Q2 gate: regenerate the s=5 headline numbers from the banked spectra and ASSERT them.

Q2 came out CLEAN in the repo-wide audit that quantum's check prompted -- every spread
quoted in FINDINGS is in results_s*.log, which are stdout of committed scripts. But
PROTOCOL 16a's tightened rule is not "an artifact exists", it is "the writeup cites an
artifact a stranger can regenerate." A log is a record of a run; it cannot fail. This
asserts, so that the next edit to S_at() or fit() announces itself.

s=3 and s=4 spectra were not banked (checkpointing arrived only after the fifth power
cut), so those two rungs rest on committed-script logs and are reproducible only by
re-running, ~20 min each. Stated rather than papered over.
"""
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from s5_run import S_at, REG
ls = list(range(20, 101, 10))   # declared here, not imported: the gate fixes its own grid
from extract import fit, spread

z = np.load(Path(__file__).resolve().parent.parent/"s5_spectra.npz", allow_pickle=True)
S = {k: list(z[k]) for k in z.files}
print(f"s=5 gate — regulators banked: {sorted(S)}   l = {list(ls)}")
assert sorted(S) == sorted(REG), f"regulator set changed: {sorted(S)} vs {sorted(REG)}"

WANT = {(1e-14,"3p"): (36.2227, 0.04274), (1e-14,"4p"): (36.2242, 0.04398),
        (1e-09,"3p"): (36.2223, 0.04269), (1e-09,"4p"): (36.2237, 0.04430)}
ok = True
GOT = {}
for (floor, model), (wa, wc) in WANT.items():
    A, B = [], []
    for reg in REG:
        a, b = fit(ls, np.array([S_at(ev, floor) for ev in S[reg]]), model)
        A.append(a); B.append(b)
    ga, gc = spread(A), spread(B)
    GOT[(floor, model)] = (ga, gc)
    good = abs(ga-wa) <= 5e-4 and abs(gc-wc) <= 5e-5
    ok &= good
    print(f"  {'PASS' if good else '*** FAIL ***'}  floor={floor:.0e} {model}: "
          f"area {ga:.4f}%  CORNER {gc:.5f}%" + ("" if good else f"   expected {wa}/{wc}"))

# The clip band carries the PHYSICAL conclusion -- is the residual spread the theory's
# or my eigenvalue floor's? -- so it must be derived from the REGENERATED spreads. It
# was originally computed from WANT, i.e. two literals I typed: quantum's third species,
# an arithmetic identity over constants printed as a measurement, reading no artifact and
# unable ever to fire. Now derived from GOT, and ASSERTED rather than narrated.
band  = abs(GOT[(1e-14,"3p")][1] - GOT[(1e-09,"3p")][1])
ratio = band / GOT[(1e-14,"3p")][1]
# A RATIO GATE IS EASIEST TO PASS WHEN ITS DENOMINATOR IS BROKEN. Found by mutation:
# lifting the near-0.5 modes blew the corner spread to 399.97%, which drove band/spread
# to 0.0000 and the ratio test PASSED on thoroughly corrupt data. Fails safe in exactly
# the wrong direction. So bound the band ABSOLUTELY as well, and bound the denominator.
band_ok = ratio < 0.01 and band < 5e-4 and GOT[(1e-14,"3p")][1] < 1.0
ok &= band_ok
print(f"\n  {'PASS' if band_ok else '*** FAIL ***'}  clip band {band:.5f}%  vs corner "
      f"spread {GOT[(1e-14,'3p')][1]:.5f}%  -> band/spread = {ratio:.4f}  (gate: < 0.01)")
print("  band << spread: the s=5 corner spread is NOT set by my eigenvalue floor.")
print(f"\n  {'ALL ASSERTIONS PASS' if ok else '*** SOME ASSERTIONS FAILED ***'}")
sys.exit(0 if ok else 1)
