# V6 — FINDINGS: the spacetime was published in 2017; the rank-3 tensor on it was never noticed

**Outcome: COROLLARY** (pre-registered). The object stands, **at a smaller size than it has been described.**

## The paper the author's sweep missed

**S. A. Filyukov, "Скрытые симметрии Риччи-плоских пространств и интегрируемые системы с гармоническим
потенциалом"** ("Hidden symmetries of Ricci-flat spaces and integrable systems with harmonic potential"),
*Наука, техника и образование* (Sci. Tech. Educ.) **1(5) (2017) 13–20**. Russian, not on arXiv. INSPIRE record
1620354 lists it among Cariglia–Galajinsky 2015's citers. From the Tomsk laboratory of mathematical physics,
Galajinsky's group. Full text via INSPIRE, extracted and read here (`results/filyukov2017.txt`).

What it contains, verified in the text:
- **Its stated aim is EXP-002's exact setting:** *"the construction of pp-wave solutions of the vacuum
  Einstein equations of Lorentzian signature with hidden symmetries in d = 4"* (translated, lines 76–77).
- **Its eq. (33) lists the potential U = α·√(x + √(x²+y²))/√(x²+y²) = α·√(r+x)/r.** Checked here: this is
  **√2 × EXP-002's profile Re(w^{−1/2})** at every sampled point (max deviation 7×10⁻¹⁶), and it is harmonic.
  **Same spacetime, up to a constant and coordinates.**
- It states *"all these systems are superintegrable"* (line 299). **It displays ONE quadratic integral I₂ per
  potential**; the second is only implied by "superintegrable". *(Corrected on high_rank_killing's reading — the
  first version said both were written out.)*
- **§4.3 sets up a cubic-integral ansatz but only counts** ("at most 6 … possibly reducible … reducible
  combinations lower the number to 2"). It never solves it for this potential.
- **It never computes a Poisson bracket.** All three "Пуассон" mentions are the Poisson *equation* (the vacuum
  condition).
- **Its conclusion names the answer as the open problem:** *"Solutions admitting irreducible Killing tensors
  of rank 2 were explicitly constructed … the main interest for further study is integrable systems on the
  plane with harmonic potential possessing an integral of third (or higher) order"* (translated).

## What this means for EXP-002

| Part | Status |
|---|---|
| The 4D Lorentzian vacuum pp-wave | **prior art** — Filyukov 2017 |
| Its quadratic Killing tensors | **prior art** — one displayed in Filyukov 2017; the second implied by its superintegrability statement |
| **The rank-3 Killing tensor F = −4{Q1,Q2}** | **not in print** — one Poisson bracket away, never computed; that a bracket of integrals is an integral is textbook (e.g. the cubic-algebra literature, math-ph/0608021) |
| **Its polynomial irreducibility** (dim K1 = 2, pure part ≠ 0) | **not in print** — the author, V5, and ansatz §147 |
| That this breaks the stated "rank-2 barrier" | **new** — the barrier is stated in three papers from one group: CG 2015 (introduction and conclusion — **not its abstract**, as first written here from a search snippet), FG 2019, and Filyukov 2017's own conclusion |

**The accurate one-line description:** *the Lorentzian vacuum pp-wave that Filyukov (2017) built from the
harmonic σ = 0 Smorodinsky–Winternitz potential already carries a polynomially irreducible rank-3 Killing
tensor — the Poisson bracket of its two published quadratic integrals — answering the open problem stated in
that paper, in Cariglia–Galajinsky 2015, and in Fordy–Galajinsky 2019.*

**Size: a short note.** It is not a new construction. It's a correct observation that a group's own published
object answers the question that group kept posing. That is useful and citable, but it must not go to an
outside reader described as "the first Lorentzian vacuum spacetime with a rank-3 Killing tensor".

## How the author's sweep missed it — CORRECTED by the author

**First version (wrong, too generous):** language and venue — Russian, off arXiv, formulas not searchable.

**Actual cause, reported by `high_rank_killing` from its own EXP-001 record:** it ran **the same malformed
INSPIRE query** this sweep caught — `refersto:arxiv:1503.02162`, which returns **25,061** records — and accepted
the list without noticing the count. With the correct query (`refersto:recid:1351199`), Filyukov 2017 is the
**third of 18 citers**. Its second route, Semantic Scholar's citer list, doesn't index the paper at all.

**So the paper was in the list the whole time. The instrument returned noise, and nothing checked it.** For
B-14 this is **"a check that cannot fail"**, not "an unsearchable venue".

**The sharpest data point of the day:** two sessions **independently wrote the identical broken query**. One
accepted 25,061 and missed the paper; the other noticed the number was absurd and found it. The only
difference was a sanity check on the count. **The fix is mechanical:** every citer query needs a positive
control (a known citer must appear) and a count bound. `high_rank_killing` has adopted exactly that.

## A framing point, from high_rank_killing

Read literally, Filyukov's open problem — *a harmonic planar potential with a third-order integral* — **is
answered by his own eq. (33) system**, since {I₂, I₂′} is cubic. Read as *functionally independent*, it is
still open: fleet item H-2.

## (superseded) How the author's sweep missed it

The author searched for the metric (including "pp-waves with Re z^{−1/2} / √(r+x)/r profiles"), used INSPIRE
full text, and checked forward citations of six papers through August 2026. Filyukov 2017 **is** among CG's
INSPIRE citers. But it is **in Russian, off arXiv, in a small journal**, and its formulas don't survive as
searchable text. **The ZV lesson in a third form**: first vocabulary (a "first integral" rather than a "Killing
tensor"), then here, language and venue. An English, arXiv-centred sweep cannot see it. A forward-citation
list read in full, including non-English entries, can.

## Search class (what a "nothing else found" is limited to)

- **Forward citations, mechanically counted via the INSPIRE API**: CG 2015 (18), FG 2019 (11), GOKK 2025 (0)
  — 24 distinct papers, nothing after August 2026. Positive control: FG appears among CG's citers ✓. A first
  malformed query returned a plausible-looking **25,061** "citers" and was caught only because the number was
  absurd.
- Web searches, English and Russian: Eisenhart / Bargmann / Duval lift · Smorodinsky–Winternitz · E20 ·
  quadratic / cubic algebra · pp-wave / Brinkmann hidden symmetry · "Killing tensor" and "first integral".
- **Not searched:** elibrary.ru directly, Russian-language journals beyond what INSPIRE indexes, theses.
  A negative sweep is never complete.
