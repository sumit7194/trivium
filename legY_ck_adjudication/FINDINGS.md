# Leg Y — Findings: auditing our own count. No duplicate found; the instrument reached less far than we did.

*Run 2026-07-21; gates Y0/Y1/Y2/Y3 frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any code, with
**all outcomes pre-declared equally acceptable**. A falsification-flavoured self-check: leg Q's
"legible ⟺ KY-integrable, **8/8**, φ = 1.0" assumed — never tested — that its eight entries are eight
genuinely different spacetimes. ansatz's new Cartan–Karlhede procedure (§116–§118) made the test possible
for the first time.*

## Result in one line

**No duplicate was found — and the count was not proven either.** The bridge's own ZV δ=1 construction is
confirmed byte-identically Schwarzschild (Y0 PASS, a genuine cross-construction check of ansatz's new
instrument); **7 of 10** integrable pairs are now **rigorously proven distinct**; and the rest — including
the one pair that most needed proving (**bumpy vs Manko–Novikov**) — hit the symbolic-algebra wall and
remain **explicitly assumed**. Leg Q's headline stands unchanged; its independence assumption is now
*named* rather than silent.

## The gates

| gate | result |
|---|---|
| **Y0** cross-construction check | **PASS ✅** — bridge's `zv_geometry(1)` (prolate spheroidal) vs standard-chart Schwarzschild → **EQUIVALENT**, certificate `z³ + 27w³z² + 243w⁶z + 729w⁹ + 729w⁸/8` — *byte-identical to ansatz §116's*, reached through a different metric construction |
| **Y1** full CK on the integrable entries | **10/10 UNDECIDED (wall)** — 6 of 8 signatures exceeded the 600 s budget; Kerr–de Sitter failed on a frame-norm sign (UNDECIDED-procedure, distinguished in the JSON) |
| **Y1b** *(post-hoc amendment)* order-0 sound route | **7/10 rigorously INEQUIVALENT** (see below) |
| **Y2** the exposed non-integrable pair | **UNDECIDED (wall)**; MN not attempted — pre-registered Y3 |

## Y1b — what the cheap sound route decided

§117's `tr((R^a_b)^k)` are frame-independent order-0 invariants: no tetrad, no canonicalization, no ∇C, so
they escape the wall. Differing ⇒ **rigorous** INEQUIVALENT; matching ⇒ inconclusive, never evidence of
sameness.

| entry | Segre type | order-0 invariants |
|---|---|---|
| Kerr | vacuum | 0,0,0,0 |
| Kerr–Newman | **non-null electromagnetic** [(11)(1,1)] | 0, ≠0, 0, ≠0 |
| Kerr–de Sitter | **Einstein space** | 3/25, 9/2500, 27/250000, 81/25000000 |
| Taub–NUT | vacuum | 0,0,0,0 |
| ZV δ=1 | vacuum | 0,0,0,0 |

**7 pairs proven distinct** (every pair involving Kerr–Newman or Kerr–de Sitter). **3 remain open** —
Kerr vs Taub–NUT, Kerr vs ZV δ=1, Taub–NUT vs ZV δ=1 — all three *vacuum-vs-vacuum*, exactly as the
amendment predicted: their matter sector is identically zero, so separating them needs the Weyl-side
machinery that walled. These are physically distinct beyond serious doubt (spin, NUT charge), but **that is
argument, not proof**, and this leg only reports what was decided.

## What this does and does not change for leg Q

- **Unchanged:** the 8/8 agreement and φ = 1.0. No duplicate was found; nothing corrects downward.
- **Upgraded:** 7 of the 10 integrable-entry pairs move from *assumed distinct* to **proven distinct**.
- **Newly named (the honest cost):** leg Q's "three independent non-integrable classes" — bumpy, ZV δ=2,
  MN q=0.5 — rests on an assumption this leg could not test. Established *before* running (structural, not
  a result): bumpy is stationary-rotating and ZV δ=2 is static, so those two cannot coincide. **The
  bumpy-vs-MN pair — both rotating quadrupole deformations of Kerr — is untested.** Per the
  pre-registration's outcome 3, leg Q's FINDINGS is amended today to state that assumption explicitly.

## Y3 — the wall, measured

This is the leg's second finding, and the one with teeth. ansatz's CK decides types D and I in *their*
charts; on **our** catalog, in leg O's rational u = cos θ Kerr-form coordinates, the procedure walled at
600 s on Kerr, Kerr–Newman, Taub–NUT, ZV δ=2 and bumpy — while the same procedure finished **ZV δ=1 in
5.9 s and Schwarzschild in 1.6 s**. The reach is not a property of the metric alone but of the
**metric-plus-chart-plus-budget**: the same spacetime is cheap in one chart and unreachable in another.
That is *walls-are-instrument-relative* (legs 2/7/J/R/V, and leg X's float64 edition) in its
symbolic-algebra form — and it says the honest ceiling on auditing our own catalog is set by computer
algebra, not by CK's theory. MN, being rotating *and* genuinely two-variable, is the regime ansatz records
as having killed 7.5-hour runs; not attempting it was the pre-registered call, not a silent omission.

## Correctness ledger (the bridge's own bug, caught)

The first Y1b run returned `AttributeError` on all five entries in 0.1–20 s. **Not a wall — our bug**, and
the short runtimes are what exposed it: `ck.ricci_invariants` returns a *tuple* `(invariants, Rm)` which we
unpacked as a flat list, and `ck.set_domain` expects `sp.Q.positive(...)` predicates, not raw relationals.
Both fixed, rerun clean. Logged because a wall and a calling bug look identical in a results table if you
only read the verdict column.

## Honest limits

- Y1b is a **post-hoc amendment**, written after seeing the wall, and is labelled as such here and in the
  pre-registration. It can only add decided pairs; no matching invariant was counted as support for
  distinctness.
- The 3 open pairs and the whole non-integrable set stay open. This leg **narrows** leg Q's assumption; it
  does not discharge it.
- Scope unchanged: this audits only the *independence of the entries* (the denominator of "8/8"), not the
  KY/legibility verdicts themselves, and not tabula's toy-model fidelity (leg Q's own scope note stands).

## Inputs (read-only) & artifacts

ansatz `scripts/ck.py` §116–§118 (`564769c`→`3ca3f08`) via their venv · bridge's own metric constructions
(leg O `survey_catalog.py`, `survey_zv.py`) · `code/ck_adjudicate.py`, `code/ricci_route.py` ·
`results/ck_adjudication.json`, `results/ricci_route.json`.

---

## Update (2026-07-21) — Y2 RESOLVED by ansatz §119, below our cheapest tier; and a correction to our own catalog

The blocked pair is decided. **bumpy ε=0.35 and Manko–Novikov q=0.5 are different spacetimes** — rigorously,
at order 0, without a canonical frame, a PND quartic, or ∇C. The walling regime was never entered.

**The move we missed.** We assumed both entries were vacuum deformations and wrote off §117's Ricci/Segre
route as inapplicable ("both are vacuum-type deformations" — PREREGISTRATION amendment). That was wrong
about our own metric. Our bumpy entry multiplies Kerr's g_tt by (1 + ε·6u²/r) and leaves the rest of Kerr
alone; an ad-hoc deformation of a vacuum solution is essentially never Ricci-flat, and this one isn't. So
the cheap frame-free sector decided it outright:

| entry | Segre type | verdict |
|---|---|---|
| MN q=0.5 | **vacuum** (R_ab = 0) | |
| bumpy ε=0.35 | **not vacuum** | **rigorous INEQUIVALENT** (Segre differs) |

**Independently verified by the bridge** (`code/verify_bumpy_vacuum.py`, exact, no sampling, our own
`delta_metric`): the ε=0 control is *identically* vacuum — confirming the construction is exactly Kerr and
isolating the deformation as the cause — while ε=0.35 gives a Ricci scalar that is **not identically zero**,
**R(r=4, u=0.3) = −0.0407695** against ansatz's independently-computed −0.0408, with 8/16 nonzero R_ab
components. Two independent computations, same number.

### What this settles, stated at exactly its strength

ansatz asked that their verdict not be rounded up, and it won't be. The three non-integrable classes are
distinct, by two different grades of evidence:

| pair | status |
|---|---|
| bumpy vs MN q=0.5 | **rigorously distinct** — machine certificate (differing Segre type) |
| bumpy vs ZV δ=2 | distinct by **structural argument** (stationary-rotating vs static: hypersurface-orthogonal timelike Killing vector or not) — sound, but *not* machine-certified |
| ZV δ=2 vs MN q=0.5 | same structural argument (static vs rotating) — *not* machine-certified |

So leg Q's "three independent non-integrable classes" **stands, and is no longer a bare assumption** — one
pair carries a proof, two carry a structural argument. That is a real upgrade over this morning's "named
assumption," and it is *not* the same as "all three proven distinct."

### The correction we owe our own catalog

**Our "bumpy ε=0.35" is not a vacuum spacetime.** It is an ad-hoc metric deformation with implicit,
unspecified matter content — perfectly legitimate as a testbed for KY-integrability (a geometric property
of *any* metric, vacuum or not), which is all legs J/M/O/Q ever used it for. But it should be *described*
that way, and until today it wasn't. Legs O and Q are amended accordingly. Read positively: the three
classes are more heterogeneous than we claimed — two exact vacuum solutions (ZV δ=2, MN) plus one
non-vacuum deformation — which if anything strengthens the breadth argument, provided it is stated.

### The wall was largely *their simplifier*, not our chart

ansatz measured it directly on a Kinnersley tetrad on Kerr in our u = cos θ chart — the seven tetrad
normalization dot products: **>8.5 min CPU unfinished** under `zsimp`'s full `sp.simplify` chain vs
**0.3 s** under `cancel(together(expand(·)))`, six of seven exactly right immediately. `zsimp` now
escalates (cheap rational normal form first, expensive chain only on the nonzero path); §116/§117/§118 all
re-verified unchanged. Their honest limit, recorded as they stated it: **this did not reach full Kerr CK** —
a second hot spot remains past the tetrad stage, logged as the instrument's reach rather than claimed as a
fix. Consequence for us, on their explicit advice: **the leg-O catalog is not re-rationalized.** Our
chart isn't the villain, so the Y3 finding is refined — the wall was *implementation*-relative more than
chart-relative, which is a sharper version of the same theme.

Our Kerr–de Sitter `ValueError` is confirmed as a **real edge case, mostly not a bug**: for a rotating
metric ∂_t is timelike outside the ergosurface and spacelike inside, so the frame norm genuinely changes
sign and no single answer is correct. Their refusal now prints the offending expression, seed index,
declared domain and sampled signs, so "straddling an ergosurface" is distinguishable from "the oracle
couldn't prove it."
