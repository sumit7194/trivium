# The Falsification Ledger — postulates stated to be killed

*Started 2026-07-22. A standing list of precise postulates the family's instruments can attack, with the
explicit goal of **disproving** them. Philosophy: every kill is a theorem (ansatz extracts the obstruction),
every survivor earns only "survived N attacks," and the jackpot odds are stated honestly up front — the
realistic ceiling is a small genuine theorem, a formalized obstruction, or an instrument the field lacks;
NOT a new law of nature. Our machines test mathematical structures and toy worlds, not nature.*

## The eligibility filter (a postulate enters the ledger only if it passes all four)

1. **Precise** — stated so that a specific computation can contradict it.
2. **In reach** — attackable by an existing family instrument (symbolic one-variable GR, lattice
   Gaussian QFT, FD wave/tower sims, CK equivalence, chaos detectors, neural discovery, real-GW stack).
3. **Pays on failure** — a kill must yield an extracted obstruction or a measured boundary, not a bare "no."
4. **Has a verifier** — the outcome is gated (pre-register → attack → three-valued verdict), never vibes.

**Standing discipline:** each attack gets a pre-registration with kill/survive criteria frozen first;
UNDECIDED is a legitimate outcome; any survivor that starts to look interesting goes through a prior-art
sweep (the quantum session's standing job) **before** anyone gets excited. Postulate status vocabulary:
`OPEN` · `KILLED (obstruction: …)` · `SURVIVED-N` · `UNDECIDABLE-BY-US (wall: …)`.

---

## Tier K — postulates we EXPECT to kill (sharpening-shots; each kill is a clean lesson or theorem)

| ID | Postulate (precise) | Attack | What the kill yields |
|----|---|---|---|
| K1 | **"S_rel = 2π×boost-energy holds for EVERY localized excitation of the vacuum"** (not just coherent states). | leg X machinery + a **squeezed** packet (still Gaussian, so exactly computable): S_rel = Δ⟨K⟩ − ΔS, and squeezing makes ΔS ≠ 0. | The measured deviation IS the entanglement-entropy change ΔS — killing K1 *measures* the correction term and shows why coherent states are special in Longo's theorem. **→ KILLED 2026-07-23, see below.** |
| K2 | **"The KK mass tower determines the hidden geometry"** ("you can hear the shape of the hidden drum"). | Compute spectra of the Gordon–Webb–Wolpert **isospectral drums** (two different shapes, provably identical spectra) with our FD Laplacian. Same tower, different geometry ⇒ dead. | A worked demonstration of spectral non-uniqueness on our own instrument — and it sets up G1 (below), which is the genuinely interesting sequel. |
| K3 | **"Clausius δQ = TδS holds exactly at every patch size"** — the **lattice analog of the localization postulate**. | leg X machinery: compare modular-energy flux vs entropy change for wavepackets crossing wedge sub-patches of shrinking size; look for entropy-production corrections. | A measured curve "Clausius violation vs patch size" on a lattice — a home-built, honest *probe of the exact link both emergent-gravity papers assume*. Toy-model only, and labeled so. |
| K4 | **"Every deformation of a vacuum metric that keeps the vacuum character of its invariants is itself vacuum."** | Already effectively dead via §119 (our own bumpy entry!); formalize: sample ad-hoc g_tt-multiplier deformations, compute Ricci exactly. | The obstruction is instructive: ad-hoc metric surgery essentially never preserves Ricci-flatness — a warning theorem for every "bumpy BH" paper that skips the check. |
| K5 | **"A neural net trained on projections can learn ONLY the spectrum"** (i.e. behavioral data carries no more than eigenvalues). | tabula: train on projections from the two GWW drums (same spectrum). If the net distinguishes them, K5 is dead — eigen*functions* leak through projections. | Sharp statement of *what* representation learning actually accesses — the family's legibility program, sharpened by a falsification. |
| K6 | **"Static one-variable ansatz metrics are always Petrov type D or O."** | ansatz: construct in-family counterexample or extract why the ansatz forces D/O (CK Petrov module, cheap). | Either a counterexample metric or a small classification theorem for the ansatz world ansatz actually lives in. |

## Tier G — genuine uncertainty (the real bets; either verdict is a finding worth keeping)

| ID | Postulate (precise) | Attack | Notes on odds |
|----|---|---|---|
| G1 | **"Flux on T² can stabilize ONLY the volume+axion combination detM — never the shape."** (§114 proved this for the configurations tried; postulate it as a *theorem for all* metric-only flux configs on T².) | ansatz: extend the §114 dictionary theorem G² = 2n²/detM to the full config space (both flux legs, both twists, Λ₆); either leftover-zero generality or the counterexample config. | The dictionary theorem's structure suggests TRUE; a kill (shape-stabilizing flux) would be genuinely surprising and worth a prior-art sweep either way. |
| G2 | **"legible ⟺ KY-integrable survives adversarial metric design."** Current record 8/8 — but nobody has *designed* a metric to break it. Candidates: (a) integrable via rank-4-only Killing tensor (no KY origin) — is it legible? (b) a metric with a *transcendental* (non-polynomial) invariant — integrable but possibly illegible. | ansatz constructs the candidates (its rank-4 search machinery inverted: build, don't detect); tabula runs legibility blind; bridge gates. | This is the family's flagship claim under deliberate attack. A kill would *localize* what "legible" really tracks (KY specifically? any invariant? polynomial invariants only?) — arguably more valuable than the survival. |
| G3 | **"Every stationary non-integrable vacuum in our reach has detectable thin-layer resonance chaos."** (MN: yes. ZV δ=2: yes. Two for two.) | Point the frequency-drift detector at each new non-integrable vacuum entering the catalog; postulate dies on the first clean non-integrable metric with NO layer at instrument resolution. | Instrument-relative by construction (stated in the postulate); a kill = "non-integrability without dynamical signature at resolution X," which would be a real curiosity. |
| G4 | **"The MN deep chaotic sea at x<1.5 is real chaos, not integrator artifact."** | Blocked on the symplectic/extended-precision integrator (the standing parked item) — this postulate is the *reason* to finally build it. | Honest status: UNDECIDABLE-BY-US until the instrument exists. Kept on the ledger as the oldest open wall. |
| G5 | **"No rank-6 Killing tensor for MN q=0.5."** (Rank-2 excluded two ways, rank-4 excluded; the residual.) | ansatz's exact-rational nullspace search extended to rank 6 (large but bounded basis). | Expected TRUE (kill unlikely); value is closing leg J's last residual with a certificate either way. |
| G6 | **"CK terminates at order ≤2 for all 4D vacuum type-D pairs in our catalog"** (the practical-termination postulate; theory allows order 7). | Run the (post-simplifier-fix) CK to order 2 on every decidable pair; a pair needing order ≥3 kills it. | Survival gives a useful *practical* bound for the tool's users; a kill documents the first hard pair — valuable either way, cheap. |
| G7 | **"Every wall the family has hit is instrument-relative"** — i.e. for each logged wall there exists an in-principle instrument upgrade that crosses it. (float64→mpmath crossed one; simplifier-fix crossed another; chart-choice a third.) | Maintain adversarially: for each wall in the ledger, either exhibit the crossing upgrade or argue impossibility. First wall *proven* uncrossable kills it. | This is the family's recurring theme promoted to a falsifiable meta-claim. A kill would be philosophically the most interesting thing we could produce. |
| G8 | **"The 221 overtone's information deficit is fundamental at current SNR"** — no analysis pipeline (learned or classical) can beat the info-limit on δ established by legs 2/L. | Standing challenge to deepstrain: any new pipeline that tightens σ(δ) beyond the Fisher floor kills it. | Survival is the expected thermodynamic answer; a kill would mean the NPE stack is leaving information on the table — deepstrain would want to know immediately. |

## Tier M — moonshots (low odds stated up front; bounded cost; obstruction is the realistic payout)

| ID | Postulate (precise) | Attack | Honest odds |
|----|---|---|---|
| M1 | **"No closed-form equal-spin charged rotating black hole exists in plain 5D Einstein–Maxwell"** (the famous gap; CCLP needs the Chern–Simons term). Postulated in the *kill-me* direction: we hunt the solution; failure = extract the obstruction. | ansatz: equal spins collapse it to one variable — inside the walls. Rational-form family hunt; if dry, obstruction extraction: *why* does the CS term make it solvable? (Already Tier-2 on quantum's roadmap; bounded: one battery.) | Solution: very low (experts suspect none). Obstruction theorem: decent — and that's the real prize. |
| M2 | **"The Srednicki area-law coefficient is independent of regulator scheme"** (lattice vs momentum cutoff vs smearing). | leg X machinery in 3D: entanglement entropy of spheres, three regulator schemes, compare coefficients. | Expected KILL (coefficient is famously scheme-dependent) — but a clean three-scheme demonstration, with the area-*scaling* invariant across all three, is the sharpest home-built statement of *exactly where* S = A/4's "1/4" hides. Direct sequel to today's discussion. **→ KILLED 2026-07-23, see below.** |
| M3 | **"Every consistent 6D→4D truncation in the metric-only T² family embeds §111's 5D EMD islands"** (§112 showed it for the diagonal slice; postulate full generality incl. dynamical χ). | ansatz: the flux-atlas machinery pointed at the truncation-classification question. | If TRUE with certificate: a tidy classification theorem for the family's own KK world. If killed: a genuinely new consistent island — prior-art sweep before any claim. |
| M4 | **"The GWW isospectral pair becomes distinguishable at ANY nonzero coupling to a second field"** (spectral degeneracy is measure-zero fragile). | quantum/bridge: couple a probe field, perturbation theory + numerics on both drums; find the splitting or the protection mechanism. | Either way it sharpens K2/K5 into physics: *what does it take* for hidden geometry to become audible? |

## Tier V — validation postulates (expected to SURVIVE; they harden instruments, cheap to run)

| ID | Postulate | Attack | Why bother |
|----|---|---|---|
| V1 | Relative entropy is monotone under region inclusion on our chain (proven in QFT). | leg X machinery, nested wedges. | If this *fails* we have a bug, not a discovery — the ultimate canary test. |
| V2 | The 1+1 massless chain's interval entropy runs as (c/3)ln L with c = 1. | Covariance-matrix entropy vs L. | Calibrates the entropy instrument against an exact CFT result before M2 trusts it in 3D. **→ SURVIVES 2026-07-23: c=0.977, R²=1.000000, gapped control saturates, float64=mpmath to 5e-9. [falsification/V2_cft_calibration](falsification/V2_cft_calibration).** |
| V3 | 2D flat tori ARE determined by their spectrum (a real theorem — the converse of K2's kill). | Verify numerically across random T² moduli: no spurious isospectral pairs at resolution. | Bounds the instrument's resolution and completes the "hearing shapes" story honestly: audible in 2D-flat, inaudible for drums. |

---

## Recommended first volley (ordered by value-per-effort)

1. ~~**K1** (squeezed-state kill — days, all machinery exists, measures Longo's correction term)~~ **✓ DONE 2026-07-23 — KILLED** (obstruction: cross-cut entanglement; see Results log)
2. ~~**M2** (area-law coefficient — the S = A/4 probe, direct sequel to the emergent-gravity thread)~~ **✓ DONE 2026-07-23 — KILLED** (κ ranges 0.30–0.51 across regulators, exponent stays 2; see Results log)
3. **K3** (lattice localization probe — aims at the ASSUMED link itself; the most philosophically loaded)
4. **G2** (adversarial legibility — needs an ansatz ask to construct the attack metrics)
5. **K2 → K5 → M4** (the isospectral-drums arc — one build, three postulates)
6. **G6** (CK practical termination — cheap, immediately useful to the new tool)

## Results log (attacks run)

### K1 — `KILLED (obstruction: cross-cut entanglement, not squeezing per se)` · 2026-07-23

Full write-up: [falsification/K1_squeezed/FINDINGS.md](falsification/K1_squeezed/FINDINGS.md)
(pre-registration + addendum frozen before code; run on the Mac, mpmath dps=60).

- **Verdict: KILLED.** A squeezed packet **straddling the entangling cut** breaks S_rel = 2π×boost-energy by
  the entanglement-entropy change ΔS > 0 — **22–56%** across squeeze r = 0.2–0.8. All gates pass; the
  Gaussian pipeline is certified non-circularly against brute-force **Fock density matrices to 1.3×10⁻⁹**.
- **The kill is more conditional than K1 assumed — and that is the finding.** A squeeze sitting *entirely
  inside the wedge* leaves the identity **exact** (ΔS = 0: it is a local unitary on A, and entropy is
  invariant under local unitaries). The frozen pre-registered attack put the squeeze inside A and so
  correctly **survived** — the survival located the real obstruction. A position scan shows deviation
  climbing 0 → 63% precisely as the squeeze crosses the cut. **It is *cross-cut* squeezing, not squeezing,
  that kills the identity.**
- **Why coherent states are special, sharpened:** displacement operators **factorize** across any cut
  (D(f)=D(f_A)⊗D(f_Ā)) ⇒ ΔS = 0 for *every* coherent state; single-mode squeezes do not factorize across a
  cut they straddle. The obstruction is non-factorization, cleaner than "coherent = unsqueezed."
- **Payout collected:** the deviation *is* the correction term ΔS (measured independently from the symplectic
  spectra), as K1 promised. **Bonus:** leg X's O4 float64 wall reappeared inside the *certification* (the
  brute-force log is float64-limited exactly where leg X's production was; mpmath crosses it) — another
  walls-are-instrument-relative instance (feeds **G7**).
- **Prior-art note:** the sharp statements (Longo's coherent-state entropy theorem; ΔS = 0 ⟺ local-unitary
  orbit; displacement factorization across a factor) are standard modular-theory / Gaussian-QFT facts. No
  novelty claimed — this is a worked, Fock-certified demonstration + a clean localization of the hypothesis
  on the family's own instrument, which is exactly Tier K's stated payout.

### M2 — `KILLED (obstruction: κ is regulator-dependent; the exponent is not)` · 2026-07-23

Full write-up: [falsification/M2_arealaw/FINDINGS.md](falsification/M2_arealaw/FINDINGS.md) (calibrated by V2;
pre-registration frozen before code; Srednicki radial decomposition, float64).

- **Verdict: KILLED.** The 3D free-scalar entanglement area-law coefficient κ (S ≈ κ(R/a)²) takes three
  clearly different values — **0.301 / 0.414 / 0.511 (51% spread)** — under three UV regulators (bare-NN
  lattice / improved Symanzik stencil / higher-derivative smooth), while the **area-law exponent stays ≈ 2.0
  in all three**. R1 reproduces Srednicki's κ ≈ 0.295 (anchor). All five gates pass.
- **The payout — where the "1/4" hides:** the *exponent* (area law S ∝ R²) is regulator-invariant to ~2%
  (real physics); the *coefficient* κ — the number that would have to equal 1/4G for S = A/4 — moves by tens
  of percent with the UV regulator. A cutoff calculation cannot pin it down.
- **Control makes it a measurement, not fitting noise (M2d):** a coordinate-only change (midpoint r_j=j−½,
  *same* regulator) leaves κ fixed to 1.8% (0.296 vs 0.301), while a genuine regulator change moves it 51%.
- **Method lesson banked:** the ℓ-sum converges slowly (tail ~ ℓ^{−2.6}); ℓ_max ≈ n undercounts κ by ~2×.
  Fixed with summation to L₀=500 + analytic power-law tail; κ stable under L₀, n-window, and box-size N (M2e).
- **Honest scope:** a lattice fact (entanglement coefficient is scheme-dependent), **not** a statement about a
  black hole's actual S = A/4. Well-known result (Srednicki; Bombelli et al; Solodukhin); no novelty claimed —
  the value is the calibrated, control-gated, home-built separation of universal-from-scheme.

## What this ledger is not

Not a route to discovering new physics about nature — no instrument here touches an experiment. Not a
claim that any surviving postulate is true. Not exempt from the house rules: read-only sisters,
pre-registration before attack, prior-art before excitement, and the north star unchanged — robustness
and correctness only.
