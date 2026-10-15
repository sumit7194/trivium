# Moonshot review, 2026-10-16: the four impact-5 / difficulty-5 items, re-read after three weeks

*Bridge, 2026-10-16. Re-reads `MOONSHOTS.md` (2026-09-23) items B-2, B-3, B-4 and B-5 against (i) what the fleet
has done since, from the repos' own committed docs, and (ii) three fresh literature sweeps (bridge subagents, 2026-10-16;
arXiv API, INSPIRE, Crossref, PDFs; no AI summarisers), with every load-bearing reference re-checked by the bridge on
INSPIRE or the arXiv API. Draft for discussion with the user; nothing here is a work order.*

---

## 0. What changed since the list was written

| 2026-09-23 | 2026-10-16 |
|---|---|
| B-5 sat "after K5": no proof tool existed; the chain stopped at "no Killing tensor up to rank N". | Quantum built the Morales–Ramis / certified-monodromy tool. 24 certificates (14 Tomimatsu–Sato, 10 Manko–Novikov) are v2-certified, v1-replayed, CAPD third-replayed with 0 contradictions, and Lean-checked (52/52). The bridge reproduced them by an independent route (V8, V9). |
| No interval-arithmetic tooling on the box. | CAPD 6.0.0 is built from source on the box (MPFR intervals, arm64 patch, full test suite run; `quantum/qsim/capd/PINS.md`). |
| "Computer-assisted proofs of chaos are mature" was the only literature fact for B-5. | A full sweep (`outreach/paper_ts_mn/LIT_SWEEP_chaos_proof.md`, 2026-10-15): no rigorous chaos proof for TS, MN or ZV; no computer-assisted chaos proof for any GR geodesic flow. |
| Where TS chaos lives was unknown. | Ansatz §150 (FINAL): transient chaos at the inner capture edge, fractal-like basin boundary down to ε≈1e−14, no strict-limit fractal claimed; V11/V12 reproduce; tabula's MEGNO cannot discriminate there. The far-field (Dubeibe 2007's region) is regular. |
| B-11 (blind rediscovery of the Jan 2026 exact rotating hairy hole) was B-2's planned positive control. | That solution is in generalized Proca theory, not scalar–Gauss–Bonnet (see §2). |
| B-3's mechanism was open. | Cuspis proved the known constraints do not localise κ/C_T, reduced the band to "closeness to the EMI shape", and showed every known positivity bound is closed under Casimir dressing (one-sided). Still no mechanism, in the fleet or in print. |

---

## 1. B-5: a computer-assisted proof of chaos in a black-hole spacetime

**Status in the fleet.** Quantum's handoff lists "chaos-proof phase 2 (Hénon–Heiles / Kerr controls, then the proof):
undecided, waits for the user". Phase 1 (toolchain: CAPD built, tested, used for the third replay) is done. K20 (locate
MN's chaotic sea numerically) is still open; the fleet's chaos numerics so far are on TS.

**Literature (verified).** Sweep of 2026-10-15, bridge-verified rows: Moeckel 1992 (CMP 150, 415) and Xue 2020
(arXiv:2012.03047) are the only rigorous horseshoe-type results for GR geodesics, both perturbative; Kluitenberg–Roest–Seri
2023 (arXiv:2211.06880) is non-perturbative but static, non-vacuum, N ≥ 3 centres, and leaves the two-centre
Majumdar–Papapetrou case open as their Conjecture 1. No CAPD/interval proof for any GR geodesic flow. arXiv checked through
2026-10-15 for TS and MN: nothing competing.

**What the fleet's own measurements say about the target.**
- TS δ=2: the chaos is transient, at the plunge/survive edge, thin. Covering relations need h-sets with clear expansion;
  a thin layer means small splitting angles, long excursions, high precision. The sweep's §(d)1 names this the main risk.
- MN: the literature (Lukes-Gerakopoulos et al. 2010, arXiv:1003.3120; Contopoulos et al. 2011, arXiv:1108.5057) reports an
  inner permissible region that is "mainly chaotic" with a large island. A broad sea is far friendlier to h-sets. The
  fleet has NOT yet located or characterised that sea itself (K20).
- Kerr is a clean negative control everywhere the fleet has looked (Carter conserved to ≤1e−12; α≈1; MEGNO 0/360).

**Honest odds.** The list said ~10%. With the tool built, the Morales–Ramis results in hand, no competitor, and MN as the
first target, the bridge would put a first GR horseshoe at ~20–25%, conditional on phase-2 controls passing. The risk is
technical (wrapping effect, near-horizon cost, expression size of the MN vector field), not priority.

**A staged plan, cheapest rung first, each pre-registered:**
1. *Decision + pre-registration* (user; quantum writes it): target MN first, TS second; success criterion = covering
   relations certified for a Poincaré map on h-sets in the physical exterior, giving a semi-conjugacy to a shift
   (positive topological entropy); failure modes named in advance.
2. *Controls* (quantum, days): Rössler a=5.7 (published CAPD proof, < 2 s) for the pipeline; Hénon–Heiles at E=1/6
   (Arioli–Zgliczyński 2001) as the open-system positive control, after obtaining the full texts; Kerr at matched
   (E, L) as the negative control, recording *which* check fails.
3. *K20, locate the MN sea* (bridge, with tabula as an independent numerical screen; days, detached): Poincaré sections
   and escape maps at the two certified MN parameter points, seeded from Contopoulos–Harsoula–Lukes-Gerakopoulos 2012
   (arXiv:1203.1010); measure the homoclinic splitting angle at candidate points (if < 1e−6, plan multiprecision from
   the start). Output: candidate h-sets and return times, with Han 2008's exterior check (h-sets outside the source).
4. *GR warm-up, possibly its own result* (quantum): Majumdar–Papapetrou two-centre planar null geodesics — strong
   hyperbolicity, known symbolic coding (Shipley–Dolan 2016), and explicitly open (Kluitenberg et al. Conjecture 1).
   Tests the GR-specific parts (horizons as sinks, geodesic Hamiltonian) on an easy case.
5. *The MN horseshoe* (quantum, with the bridge replaying by an independent route as for V8/V9).

**Why first.** It is the one impact-5 item whose gate has been removed by the fleet's own work, it is new on the
literature's showing, it turns the TS/MN paper's numerical chaos section into a certificate, and every tool it needs
is already on the box. It also serves C18 (a certified corner number) with the same tooling.

---

## 2. B-2: a closed-form rotating black hole in scalar–Gauss–Bonnet gravity

**Status in the fleet.** Ansatz's own 2026 moonshot list: "most likely there is no closed form … chance ~1–2%".
Ansatz is blocked by P0 (the simplifier wall on rotating metrics); rotating EdGB as a full 2D PDE is parked. The
rotating-EdGB fit (R2, a 4-number compact fit at 0.17%) is a fit, not a solution, and ansatz's own prior-art correction
(2026-06-23) says so.

**Literature (verified).** No closed-form rotating sGB/EsGB/EdGB solution exists as of 2026-10-16. Every rotating
solution is numerical (Kleihaus–Kunz–Radu; Cunha–Herdeiro–Radu; Delgado–Herdeiro–Radu, arXiv:2002.05012;
Fernandes–Mulryne spectral code, arXiv:2212.07293, CQG 40, 165001) or perturbative. The "closed-form analytic" spinning
sGB metrics of Lam–Chung–Yunes (arXiv:2509.07061, PRL 136, 021401; arXiv:2510.05208, PRD 113, 024030) are spectral fits
to leading order in the coupling. Numerical spinning EsGB holes are always Petrov type I (Fernandes–Mulryne §3.4.3), and
slowly rotating sGB is type I with no rank-2 Killing tensor (Owen–Yunes–Witek, arXiv:2103.15891, PRD 103, 124057),
which argues against any Kerr–Schild or type-D closed form, though no theorem forbids one.

**Two corrections to MOONSHOTS.md (recorded there too):**
- The "primary hair (Jan 2026)" exact rotating hairy hole is Fernandes, arXiv:2601.21163: Kerr–Schild in *generalized
  Proca* theory (vector–tensor), no scalar, no Gauss–Bonnet term, non-circular. So B-11 is a positive control for "can
  the engine find an exact rotating hairy hole by a Kerr–Schild route", not for the sGB class. The nearest exact
  *scalar*-tensor rotating hole remains disformal Kerr in DHOST/Horndeski (Anson et al. 2020, arXiv:2006.06461;
  Ben Achour–Cisterna–Roussille, arXiv:2512.19549, JCAP 04 (2026) 041), with no GB coupling.
- arXiv:2412.04135 is Ben Achour's DHOST review (EPJC 85, 424 (2025)), not a spectral sGB QNM paper. The spectral QNM
  papers are 2406.11986 and 2412.09377 (and 2412.17073 for EdGB).

**Honest odds.** 1–2%, as ansatz says. **Recommendation: park.** If anything, run ansatz's cheap GP-plus-exact-verifier
search once, pre-registered as a null ("the rational/Laurent class contains no rotating sGB solution at O(ζ)"), which
is recordable either way. Not before the outreach work.

---

## 3. B-3: the mechanism behind near-universal corner entanglement a(θ)/C_T

**Status in the fleet.** Cuspis has done the analytic part that was open on 09-23: (i) the theorem that the six known
general constraints C1–C6 do not localise κ/C_T; (ii) the band reduced to "computed corner functions sit near the EMI
shape" (EXP-016); (iii) every known positivity bound (rectangle, cuboid, conformal concavity, fusion-EFT, Rindler) is
one-sided and closed under Casimir dressing (EXP-017, EXP-024), so an *upper* bound needs a constraint in which the
Casimir energy enters other than multiplicatively; (iv) conformal concavity at n=1 derived at physics level, giving
κ/C_T ≥ 2.894. C2a′ (Dirac cumulant route) closed: the free-Dirac corner is 89–90% Gaussian; parked. Cuspis's own
ranking: upper bound on κ/C_T first (3%), the band second (5%), Ising κ third (8%).

**Literature (verified).** No paper in 2024–2026 proposes or proves a mechanism for the band. The September 2026 cusp
bootstrap (Lanzetta–Moult–Wang, arXiv:2609.04041 and 2609.04302) gives κ_n ≥ (2π/3)a_n(π/2) and conformal concavity for
n ≥ 2, both one-sided; cuspis already cites and extends them (its [LMW26]). The 2023 PRL conjecture (free scalar
extremal, normalised by F₀) is still unproven in d=3, and its d=5 analogue fails for general regions (Bueno et al.,
arXiv:2604.01436, JHEP 08 (2026) 133). Fuzzy-sphere work has not extracted a corner function (Hu–Zhu–He,
arXiv:2401.17362, keep the cut smooth on purpose). **One new datum:** Ngai, Chau, Rong, Cheng, Liao, Meng,
arXiv:2512.00382 (Rep. Prog. Phys. 89, 068006 (2026)): a precise QMC Rényi-2 corner coefficient for 3d Ising at 90°,
four-corner sum 0.020(1) against 0.025(1) at the Gaussian point. The subagent's conversion (not the paper's) puts Ising's
a₂(π/2)/C_T about 15% below the free scalar; cuspis should redo that conversion in its own conventions.

**Honest odds.** The mechanism stays at ~5%. **Recommendation:** no moonshot work now; relay the Ising datum and the
d=5 paper to cuspis (cheap, today). The instrument-level route (fuzzy-sphere lune) has no owner and no instrument.

---

## 4. B-4: why the physical black hole carries a principal tensor

**Status in the fleet.** Unowned, no instrument, no live session. The hidden_symmetry page (outcome E) stands: the field
equations do not generate the symmetry (Krtouš–Frolov–Kubizňák 2008, arXiv:0804.4705, PRD 78, 064022: a principal tensor
alone gives type D, separability and integrability; Einstein's equations then select Kerr–NUT–(A)dS). Which spacetimes
admit one is open: Frolov–Krtouš–Kubizňák, arXiv:1712.08070 (PRD 97, 104071) drop the spacelike-gradient assumption and
find new Lorentzian off-shell metrics with null eigenvalues. Ansatz's reframing ("deformed Kerr is not Kerr–NUT–(A)dS, so
no principal tensor, so no tower") is in its CLAUDE.md.

**Literature (verified).** None of 1712.08070's nine citers extends the null-eigenvalue branch. Two 2026 preprints
circle the "why": Kim, arXiv:2603.08408 ("local origin of hidden symmetry": within a restrictive stationary-axisymmetric
ansatz plus a local-equilibrium condition, the mixed Einstein equations force a projective alignment whose regular
branch is Carter–Plebański type, hence type D and a principal tensor; the author calls it a "local structural
precursor", not a uniqueness theorem) and Baines, arXiv:2606.14076 (hidden symmetry as an *input*: Killing–Yano plus
separable Teukolsky plus asymptotics forces Kerr and Ricci-flatness, theory-agnostic). On deformations: Ben Achour–
Gourgoulhon–Roussille (arXiv:2506.09882, JCAP 10 (2025) 012) give an off-shell family keeping the full Killing tower;
Kocherlakota–Narayan (arXiv:2507.18706, PRD 112, 124058) find a Killing–Yano tensor only in a degenerate type-D subclass of
the doubly separable spacetimes. In sGB/dCS nothing beyond Owen–Yunes–Witek 2021 (type I; Killing tensor at linear order
in dCS only).

**Honest odds.** 5%, and it is a characterisation question more than a physics one. **Recommendation: park.** The
only fleet-shaped rung is ansatz's K12 (which deformations keep Carter at second order), which the 2025 papers above
partly pre-empt; worth a note to ansatz, no more.

---

## 5. Proposed order

1. **B-5 now**, staged as in §1: decision and pre-registration this week; controls and K20 can run detached while the
   outreach front doors are built; the MN proof after the controls pass. Owner quantum; bridge on K20 and the
   independent replay; tabula as the independent numerical screen of the sea.
2. **B-3: a relay only** (Ngai et al. 2026; Bueno et al. d=5; the cusp-bootstrap pair) to cuspis.
3. **B-2 and B-4: parked**, with the errata and new prior art recorded.

This does not displace the outreach queue in `outreach/audit_2026-10-15/CORRECTED_ROADMAP_2026-10-15.md` (front doors,
landing page, CI, then the emails): B-5's first two rungs are small, and its compute runs detached on the Mac, which is
free on weekdays while the phone finishes DeepStrain's C1–C4 (about 2026-10-23).

---

## 6. Verification record

Bridge-verified on INSPIRE or the arXiv API, 2026-10-16: 0804.4705, 1712.08070, 2103.15891, 2212.07293, 2307.05164,
2401.17362, 2412.04135, 2506.09882, 2507.18706, 2509.07061, 2510.05208, 2512.00382, 2512.19549,
2601.21163, 2603.08408, 2604.01436, 2606.14076, 2608.22523, 2609.04041, 2609.04302, 2004.09472. The theorem *contents*
rest on the subagents' reading (abstract or full text as their reports state); the subagents' full reports are in the
bridge session's scratch directory and were not committed. Not re-verified by the bridge: 2610.16640 (verified 10-15),
the numerical-sGB and QMC-corner rows beyond those listed.
