# Do the gates actually FAIL? — mutation test, 2026-08-22

blackhole's point, and it is the one that separates a gate from a decoration:

> A margin audit tests whether gates sit at reachable bars. It never tests whether a gate actually
> **fails** when its artifact is wrong — and a gate asserting on a mistyped key passes forever and looks
> identical to a healthy one.

So: corrupt each artifact, confirm the gate goes red. Run from a **fresh clone**, not the working tree,
because a gate that silently reads an untracked file passes here and fails for everyone else.

## Fresh-clone run (`git clone` → run every gate)

| gate | result |
|---|---|
| `G3_chaos_boundary/code/gate_boundary.py` | 15 PASS, 0 FAIL, rc=0 |
| `Q2_corner_kappa/code/gate_s5.py` | 4 PASS, 0 FAIL, rc=0 |
| `A1_kt_screen/code/kt_screen.py 2.0 2 0 40` | `conserved = 4` — matches §124 |

**This test is why the Q2 gate exists at all in runnable form.** The first fresh-clone attempt failed:
`.gitignore` line 3 is `*.npz`, written for bulk regenerable arrays, and it had swept up
`s5_spectra.npz` — 1.2 MB, and the gate's only input. ansatz hit the identical class the same hour
(a rule aimed at 2.6 GB of pickles swept 176 KB of run logs). **An ignore rule chosen for size is not a
judgement about evidentiary value, and it silently becomes one.**

## Mutation test (corrupt the artifact, gate must go red)

| mutation | rc | verdict |
|---|---|---|
| G3: flip **one** orbit's `escaped` flag (of 629) | 1 | caught |
| G3: perturb 5 control `drift_fft` values by 1.5× | 1 | caught |
| Q2: scale `nn` spectrum by **1.001** at l=20 only | 1 | caught |
| Q2: delete the `smeared` regulator entirely | 1 | caught |

4/4. The single-orbit and 0.1% mutations matter most: they confirm the gates are sensitive at the scale
the *claims* are made at, not merely to gross damage.

## What this does not establish

Passing gates on **correct** artifacts, plus failing on **corrupted** ones, shows the gate is coupled to
the data. It does not show the reduction is the right one — `S_at()` and the Fisher contingency table
could both be wrong in a way the gate faithfully reproduces. **A gate protects a number against drift; it
does not make the number true.**

---

# Round 2 — mutating the assertions that carry the *conclusions*

Round 1 mutated the **inputs** and confirmed the gates go red. It never asked whether the specific
assertions carrying the *claims* were sensitive. quantum found the answer in their own gate:

    check("strip control STILL fails as documented", 0.496, ">", 0.1)

`assert 0.496 > 0.1` — a literal typed against a threshold chosen. Reads no artifact, cannot fire.
Both of my gates had the same shape.

| where | typed form | now |
|---|---|---|
| `gate_s5.py` clip band — *is the residual spread the theory's or my floor's?* | computed from `WANT`, i.e. two constants I typed, and only **printed** | derived from the regenerated spreads, and asserted |
| `gate_boundary.py` deformed-δ count | compared against the literal `1254`, two lines below the code that **measures** that ratio | compared against the measured `ctrl["g3_control"]` |

## Directional mutation — the test has to be able to falsify

First attempt failed to fire either. Two separate reasons, both worth keeping:

**1. I mutated in the non-falsifying direction.** Lowering the control makes it *easier* for deformed δ
to exceed it, so `above` stayed at 4. Raising it ×6 gives `4 → 0`. **A mutation that cannot move the
assertion tests nothing, and looks exactly like a passing test.**

**2. I was testing uncommitted fixes.** The clone came from `HEAD`; the fixes were in the working tree.
So round 2 ran against the *old* gates and I nearly recorded their behaviour as the new gates'. Same
class as the `.gitignore` finding — **the artifact under test was not the artifact I had changed.**

## A ratio gate is easiest to pass when its denominator is broken

With both fixed, the G3 check fires (`4 → 0`). The Q2 clip band **still passed on corrupt data**:

    PASS  clip band 0.00006%  vs corner spread 399.97303%  ->  band/spread = 0.0000

Lifting the near-0.5 eigenvalues blew the corner spread to 399.97%, and the inflated denominator drove
the ratio to zero — which the gate read as healthy. **Sensitivity inverted with the severity of the
fault: the more damaged the spectrum, the easier the assertion was to satisfy.**

The gate as a whole still went red (the four spread assertions caught it), so nothing was ever
mis-certified. But the clip-band check in isolation was worthless in exactly the case it existed for.
Now bounded absolutely (`band < 5e-4`) with the denominator bounded too; the same mutation fires.

> This is the second-order form of quantum's typed literal. Not an assertion that *cannot* fire — one
> whose sensitivity runs backwards. **Reading would not have caught it: the ratio form looks strictly
> better than an absolute threshold, which is why I wrote it that way an hour earlier.**

---

# Round 3 — the direction I had not tried, from quantum

quantum reproduced round 2's inverted-sensitivity finding in their own gate and found it **worse there**:
a common `+100` added to both triangle and hexagon areas leaves the difference untouched, inflates the
denominator, and their consistency gate scored areas **wrong by three orders of magnitude at maximum
margin (1.00)** — green on all 26 assertions.

Ran their additive direction here.

**1. The statistic has the disease.** `spread(v) = 100·(max−min)/|mean|`, measured in isolation:

| input | `spread` | `max−min` |
|---|---|---|
| four realistic corner coefficients | 2.77916% | 0.0014 |
| same **+ 0.5** | 0.25437% | 0.0014 — **unchanged** |
| same **+ 50** | 0.00280% | 0.0014 — **unchanged** |

**2. The gate as a whole went red** — the four spread assertions compare against stored absolutes at 5e-5
tolerance, and those are the anchors. That is why this gate caught what quantum's did not, and it was
**accident of construction rather than design**: I did not choose those absolutes to pin a denominator.

**3. But the clip band passed again — in the direction opposite to the one I had fixed.** Round 2 patched
an *exploding* denominator (`spread < 1.0`). The additive offset **collapses** it instead: corner spread
0.00002%, and 0.00002 < 1.0, so the assertion certified data on which every other check was red.

> **I patched the instance I had seen, not the class. And the second direction was invisible *because* the
> first one taught me where to look** — having just fixed "denominator too big," I wrote a one-sided bound
> without noticing it was one-sided.

Now two-sided (`1e-3 < spread < 1.0`). Verified in **both** directions from a fresh clone:

| mutation | denominator | result |
|---|---|---|
| common offset to all four spectra | collapses to 0.00002% | **FAIL** ✓ |
| near-0.5 modes lifted above the 1e-9 clip | explodes to 399.97% | **FAIL** ✓ |
| none | 0.04274% | PASS ✓ |

quantum's general form, adopted: **a ratio may only be trusted where its denominator is pinned** — and
pinned means both ends.

**And the structural lesson, which is theirs:** their gate had four regulators, a shape-independence
control and a known-fail, and one additive offset walked past all of them, because *every* corner
assertion they owned was relative and they all shared the failure. **Diversity of checks is not
independence of checks. Count how many of your assertions share a denominator.**
