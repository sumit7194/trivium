# Non-rational axis data ("K5"): closing digest for this branch (2026-11-21)

*Written by the Bridge. The branch is CLOSED for now. This file records what was established, how well it was checked,
and what stays open. Neon = Google Gemini 3 Neon; outputs are UNVERIFIED except where a fleet check is cited. Full
texts are in neon_work/onlykerr/T32–T47_summary.md and _full.md (outside the repo).*

## Why the branch existed
The Only Kerr statement is proved for RATIONAL axis Ernst data. Its "not claimed" list names non-rational axis data
(digest ONLY_KERR.md §2). Shrinking that open class makes the theorem's boundary sharper. That was the reason for
starting.

## Why it is closed now
After the first results, each next class (doubly periodic, singly periodic, square-root, cube-root, general algebraic)
followed naturally from the previous one, but none was asked for by the Only Kerr argument. Several classes are not
asymptotically flat, so they say nothing about physical spacetimes. On 2026-11-21 Sumit questioned whether the
Gemini throughput was work for its own sake. This branch was the clearest case: no why-it-matters note had been written
for its later steps. It is closed with an honest record, and can be reopened if a physical class needs it.

## What was established (axis NVE v'' + (3/16)(P'/P)² v = 0, P = a − f0)
| Class of f0 | Result (generic a unless stated) | Physically AF? | Check status |
|---|---|---|---|
| Elliptic (doubly periodic), T39 | SL2 for every a if some zero/pole has order ≥ 2; otherwise off a discrete set. Elementary proof: on a torus no point at infinity absorbs the positive-exponent budget | No (an elliptic function cannot tend to 1 at real infinity) | Bridge RK4 reproduces the traces; argument read step by step; two cosmetic slips fixed |
| Simply periodic R(e^{λz}), T42 | SL2 except R = a − c·w^m at a single a | No in z, but by Möbius covariance (T43, proved) the class R(e^{λ/(z−c)}) is Curzon-type and AF iff R is analytic at 1 with R(1) = 1 | Bridge RK4 matches Example 2 to 1e-9; the AF framing error was caught by the Bridge and corrected by Neon |
| Square-root and hyperelliptic √R, T43 | A simple √ branch point is always a nontrivial parabolic, so SL2 off listed special a; includes √(1 − 2M/z) | Yes, for suitable R | Bridge hand-check of the log coefficient; RK4 matches the traces |
| Möbius-power c0 + c·M(z)^δ (includes ZV axis data), T44 | Escapes first-order SL2 only for δ ∈ E1 = ±(2k+1)/(k²+k+1) (Borel) or E2 = ±2/(2j+1) (D∞), via Kimura. δ = 1 (Schwarzschild) is in E1; ZV δ = 2 is in E2 | Yes ((z−σ)/(z+σ))^δ is AF) | Bridge sympy: the E1 explicit solution is exact (δ = 3/5 control fails); the E2 sym² solution holds to 1e-38; Obs_3 matches symbol for symbol |
| General algebraic, zero parabolic points, T45/T47 | a → ∞ period-rank and exactness obstructions close some curves (one genus-2 curve rigorously). They FAIL in general (classes F1–F3, explicit examples), though every tested curve is SL2 by direct monodromy | Some are | NOT closed in general. OPEN |

Earlier parts of K5 (T24, T28, T32, T34): annulus winding and order-0 entire theorems, and the balanced class with a
sharp (3 − √5)/2 threshold in 2I. These are in digest ONLY_KERR.md §13 and T28/T37 in neon_work.

## Novelty status of the E1/E2 classification
MPS 2013 (arXiv:1302.4234) has been read in full, independently by the Bridge and by Neon T47. It uses an EQUATORIAL
radial solution with the first-order NVE and Kovacic, proves δ = 2, checks δ = 1/2, and says general δ needs
case-by-case work. It contains no classification over δ and nothing on the axis. Neon also opened Lukes-Gerakopoulos
2012, the LG–MPS Comment 2013, Vollmer 2015/2016 and Dolan 2019, and found no such statement. That is "not found in
these sources", not proof of novelty.

## Physical-meaning check
For the Only Kerr programme the relevant members are the AF ones: Curzon-type R(e^{λ/(z−c)}), √-type and Möbius-power.
E1 members other than δ = 1, if physically AF with sensible multipoles, are invisible to the first-order axis test,
just like ZV δ = 2. That belongs in the "honestly open" list of ONLY_KERR.md.

## Open (parked)
- The general zero-parabolic algebraic class.
- Dense or slowly decaying meromorphic data (beyond T32/T34).
- Any higher-order (VE2/VE3) axis treatment of the E1/E2 members.
