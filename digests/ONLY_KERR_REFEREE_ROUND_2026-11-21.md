# Only Kerr: the referee round of 2026-11-21 (digest)

*Written by the Bridge, 2026-11-21 evening. This complements digests/ONLY_KERR.md (sections 12–13). Every claim names
who produced it and who checked it. "Neon" means Google Gemini 3 Neon on Sumit's accounts; its outputs count only
after a fleet check.*

## Why this round mattered
The Only Kerr statement is the fleet's strongest candidate for outside readers. Before any expert sees it, it should
survive a hostile read. A claim that outruns its proof burdens the reader, which is the opposite of our goal of
helping science. So we commissioned an independent referee-style audit (Neon T38). We then treated its findings as
work items, not as verdicts.

## What the referee said, and how each point was graded
The owner (ansatz) graded every point (data/nve/T38_GRADING.md, d153394, plus addenda).

| T38 point | Referee's verdict | Owner's grade | Status now |
|---|---|---|---|
| First-order axis NVE, Kovacic count, both axes, generic energy | VALID | agreed | — |
| 1a: k = 0 is Kerr, so "K* empty" was mis-stated | ERROR | wording slip | fix the text: "every k ≠ 0" |
| 1b: k = 4 branch points collide with poles | GAP | already handled (the merger is at Re z = 0, outside the working half-plane) | closed |
| 1c: k < 0 has real branch points | GAP | VALID, with a consequence the referee missed | k < 0 violates regularity on the lower outer axis, so the physical family is 0 ≤ k ≤ 30/7. The negative-k part of gap B concerns complex metrics, and is labelled so |
| 1d: the k = 30/7 endpoint (a J = 0, AF member) is not covered | ERROR / gap | REAL GAP | **closed by two routes** (below) |
| 1e: only spin 0.6 checked | GAP | caveat already stated | spin runs at 0.3, 0.8, 0.9 in progress |
| 2a: abelian G3⁰ if G1⁰ is trivial | GAP | REAL GAP | **closed by two routes** (below) |
| 2b: confluence limit in Lemma X | GAP | a paragraph, not a hole | write-up |
| 2c: Zipoy–Voorhees δ = 2 exclusion | GAP | handled (digest §12) | text to match |
| 3: MRS punctures; single-valued domain for family (ii) | GAP | write-up | Neon drafting (T49); ansatz will check it against the code's singular sets |
| 4: reference-subtraction ρ⁴ cancellation | UNCLEAR | handled (V25 P1) | write-up |
| 5: complex-meromorphic vs real-analytic integrals | GAP | handled (§6) | promote to the abstract |
| 6: regularity on both outer segments; i⁰ citation | wording | agreed | write-up |

## The two real gaps, and how they closed
**1d, the endpoint k = 30/7.**
- Route 1 (ansatz §161, cb305c2; window §162, 10b77ad):
  - the lower-axis test at spin 0.6, E = 0.8 is OBSTRUCTED;
  - argument-principle counts over 15 functions show no exceptional k in [3.95, 30/7 − 1e−12];
  - the registered run was VOID (control-design errors). The verdict comes from a post-unblinding amendment A1, with
    every control's failure route kept.
- Route 2 (Neon T41, different energy and observable): at E = 1.5 the global VE1/VE3 monodromy commutators are
  5.788 / 164.70 (10+ digits), Kerr gives 0, and k = 1 is nonzero. It also gives an elementary closed form for c0 at
  the endpoint, and a continuity argument.
- Remaining: the open sliver (30/7 − 1e−12, 30/7). Every point sampled there is non-integrable; an interval-certified
  δ0 has been requested (Neon T48).

**2a, G1⁰ = C*.**
- ansatz (49ade38): the exact solutions v± = (ND)^{1/4}e^{±κu}; κω(E) diverges like log E, so it is non-constant.
- Neon T41: the same structure, with κ² = (μ² − E²)β² − μ²c/2. ansatz verified algebraically that the two forms agree
  (both give a²(1 − E²) for Kerr).

## What the round taught us (target choice and process)
- **Two of the referee's three "major" items were real.** Our own earlier reviews had missed both. A hostile
  outside-style read earns its place before outreach.
- **The referee also over-flagged** (1b). Its verdicts were graded, not adopted.
- **One correction came from checking the referee's own background claims.** MPS 2013 settled ZV δ = 2 with the
  FIRST-order NVE along an equatorial radial orbit, not with higher-order equations. The Bridge had briefly said
  otherwise and corrected it. Two independent full-text reads (Bridge, Neon T47) agree.

## Physical-meaning check
- The excluded integrals are those meromorphic near the complexified axis geodesics (including the ring points
  z = ±ia). Real-analytic integrals on the physical exterior are not excluded. This belongs in the abstract.
- Family (ii) is a mathematical family. Its physical members are 0 ≤ k ≤ 30/7, set by regularity on both outer axis
  segments.

## Open items before the talk test (no outreach until these are done)
1. ~~The sliver near 30/7~~ CLOSED (2026-11-21 evening): Neon T48b's interval certificate (Zariski density Z1–Z4 over [30/7 − δ0, 30/7], δ0 = 1.37e-11 at E = 0.8 and 2.04e-10 at E = 1.5). ansatz read the code, reproduced it and cross-checked it with its own 50-digit walker (3c2d29c). Both minor items are fixed in ansatz's patched copy (5f1b291, data/nve/t48b_fixed/; δ0 = 1.37e-11 at E = 0.8 and 1.90e-9 at E = 1.5), which is the copy to cite. **Net at spin 0.6: no exceptional k in (0, 30/7]** (the sliver is interval-certified; the rest is 50-digit floating point).
2. Spin coverage beyond 0.6 (ansatz runs at 0.3, 0.8, 0.9), and the E = 1.5 point for §161.
   - **Spin 0.8 (2026-11-22, 8241c9b):** registered EXCEPTIONAL CANDIDATES because of a classifier design flaw:
     tr(M1Γ) = tr M1 · tr Γ identically (Fricke), so the two "independent" traces were not independent.
   - **Resolved post hoc (labelled):** at the common zero k* = 4.00816, an independent circle pair passes Z1–Z4. So
     there is no exceptional k (floating point).
   - **Sliver certificates (2026-11-22):** interval-certified at spins 0.6, 0.8 and 0.9 (E = 0.8), with spins 0.8 and
     0.9 under a post-failure amendment the Bridge checked as sound. Spin 0.3 FAILS for a real reason: the endpoint
     group is near-degenerate (τ ≈ −4.5e-10), so the sliver there is floating point only, and a registered S4 failed (certified only within 7.4e-15 of the
     endpoint).
   - **Answer for the claim sentence:** the endpoint obstruction weakens fast toward low spin (|tr Y| ∝ a^7–a^8).
     Spins below 0.3 are not tested.
   - **Two implementations (2026-11-22):** Neon T50, blind to ansatz's numbers, reproduces the endpoint table to 15 digits at
     all four spins (ansatz grade AGREE, f118158). Wording: "two independent implementations of the same loop invariants".
     T50 also located the degenerate spin a_c = 0.858446…, where an independent pair is Zariski dense; ansatz will reproduce it.
3. Write-up items: the MRS section (T49 draft, then ansatz's check), points 2b, 4, 5, 6, and the 1a wording.
4. ~~One claim sentence carrying every scope qualifier~~ DONE 2026-11-22. The reference text is
   conjecture_machine/data/nve/CLAIM_FAMILY_II.md (eed501f), with a per-number source table. Any outreach text must
   quote it, not paraphrase it.
5. ~~Citations and the MRS section~~ DONE 2026-11-22: conjecture_machine/data/nve/MRS_SECTION.md.
   - Verified at source: MRS 2007, Beig–Simon 1981 and FHP 1989. Casale 2009 is dropped (it doesn't cover open Γ).
   - The Bridge-requested Lemma C (the covering and the algebraic gauge preserve G⁰) is added, sourced via Audin 2003,
     Combot and Singer.
   - Prop. 2 (single-valued off-axis metric) is labelled citation-pending.
   - **READY FOR THE TALK TEST.**
