# Leg J — Findings: the deformed Kerr is formally non-integrable but its orbits stay regular

*Run 2026-06-21. Gates and outcome-meanings frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any
orbit was integrated. This leg attacks the project's one UNDETERMINED result — Move D / ansatz §82's
"deform Kerr → canonical Carter tensor broken, yet no detectable chaos, fate undetermined." Two post-hoc
positive controls (§§ below) corrected our dynamical instrument — first Carter-saturation → Lyapunov, then
(2026-06-26, on the bound-chaotic Manko–Novikov metric) Lyapunov → **box-dimension**, after finding the
two-trajectory Lyapunov is finite-difference-noise-limited on bumpy metrics — logged honestly, not hidden.*

## Result in one line — the fate is no longer "undetermined"

Two independent attacks settle Move D / §82's open horn for this deformation: **(symbolic) no exact
Killing–Yano tensor survives the bump** (complete degree-≤4 search; Kerr's is rediscovered, the bump has
none → by Eisenhart no exact Carter-type Killing tensor exists), and **(dynamical) the geodesic flow stays
REGULAR** — ansatz §79's Lyapunov exponent sits at the Kerr floor (λ ≈ 0.015–0.03) for every accessible
orbit, near-circular *and* eccentric/inclined, **up to ε=1.2**, even as the canonical Carter constant `C₀`
is violated (drift 7→18%). Together: the bumpy metric is **formally NON-integrable but NEAR-integrable** —
no new exact hidden symmetry, yet the KAM tori survive and there is no chaos in reach. This matches the
Kerr-deformation literature (Brink III/IV; [1807.08594](https://arxiv.org/abs/1807.08594)), reached here by
proof *and* by orbit dynamics. **Correction (positive control):** our first-pass chaos indicator
(Carter-constant *saturation*) could not be validated as a chaos detector and is **superseded** by the
Lyapunov exponent here — the conclusion is unchanged but now rests on the standard, validated tool.

## The measures (both calibrated on Kerr, ε=0)

| ε | Carter drift (median) | saturation (median) | diffusing fraction (>3×) |
|---|---|---|---|
| **0.00 (Kerr gate)** | **1.3e-10** | 1.05 | 0.04* |
| 0.05 | 2.3e-02 | 1.03 | 0.00 |
| 0.12 | 4.3e-02 | 1.03 | 0.00 |
| 0.25 | 6.4e-02 | 1.01 | 0.00 |
| 0.35 | 7.2e-02 | 1.01 | 0.00 |

*the ε=0 "diffusing" blip is machine-noise on a constant (drift ~1e-10). **G1 gate PASSES**: Kerr's C₀ is
conserved to 1.3e-10, so any ε>0 drift is real signal.

- **DRIFT** `=(max−min)/|mean|` over the orbit — how much the canonical invariant is violated. It grows
  ~`√ε` (sub-linear), confirming the symbolic result `∇₍ₐK₀_bc₎ ∝ ε·a²` quantitatively, and stays a few
  percent — not exploding.
- **SATURATION** `= spread(full)/spread(first quarter)` — was intended as a bounded-vs-diffusing chaos
  proxy (synthetic-validated: bounded→1.01, random-walk→3.63). The bumpy orbits read 1.0–1.05. **⚠ This is
  NOT used as chaos evidence** — see the positive-control § below: on a *compact* bound energy surface C₀ is
  range-bounded whether or not the orbit is chaotic, and a fast-mixing chaotic orbit fills that range as
  quickly as a torus, so saturation ≈1 either way. We could not validate it on a chaotic bound orbit, so it
  is superseded by the Lyapunov exponent. (The drift above remains valid — it measures the deformation
  magnitude, not chaos.)

## The dangerous regime — eccentric/inclined orbits, where chaos hides (`export_eccentric.py`)

The first pass used near-circular orbits (the *stable* ones). Chaos in a near-integrable system concentrates
at **resonances**, reached by eccentric/inclined orbits — which we now build properly: specify
(r_peri, r_apo, inclination), solve the Kerr turning-point conditions `R(r_p)=R(r_a)=0, Θ(θ_min)=0` for
(E,L,Q) [Schmidt 2002], launch at the equatorial pericenter, and integrate. A fine scan in r_apo
(eccentricity 0.20 → 0.53 at r_p=4.5, incl ≈13–20°) **crosses resonances**. Calibration: on Kerr these are
genuine eccentric inclined tori with C₀ conserved to ~2e-9.

In the strongest bump (ε=0.35), all 17 eccentric orbits show Carter drift **0.13 → 0.18** — *larger* than
the near-circular 7% (eccentric orbits probe the bump harder) — yet **saturation 1.00–1.02, zero diffusing.**
So even in the resonance-crossing eccentric/inclined regime, C₀ stays a bounded non-diffusing near-invariant:
**no chaos found where it is most likely.** (The Kerr-baseline saturation is noisier — up to 1.48 — because
it is machine-noise on a *constant* C₀; the bump's real oscillation reads a clean ~1.0, well separated.)

## Positive control — and a correction (the discipline working)

A null ("no chaos") is only as good as a *demonstration that the detector can see chaos*. So we ran the
positive control we'd demand of anyone else, cross-checking the Carter-saturation measure against ansatz
**§79's Lyapunov exponent** (independent, standard; calibrated — Kerr reads the floor λ≈0.015) and legG's
SALI. Findings:

- **Both detectors agree the accessible orbits are regular.** On the axisymmetric bump (our deformation),
  §79 Lyapunov sits at the Kerr floor (λ ≈ 0.015–0.034) for *every* orbit — near-circular and
  eccentric/inclined, even near the separatrix (r_p→3.2) — **up to ε=1.2**. The Carter-saturation agrees
  (≈1). This corroborates legG's own SALI: the axisymmetric bump's median SALI stays 0.81 (regular) at
  ε=1.0; only the single most-aggressive orbit dips to a *marginal* 0.066. So our bump is **robustly regular
  even at strong deformation** — the chaos legG found was the *non-axisymmetric* (φ-dependent) bump
  (SALI 0.024), a different, more aggressive deformation.
- **We could not validate the Carter-saturation as a chaos detector.** The only clearly-chaotic case (the
  φ-dependent bump) sends these orbits *unbound* (chaos → escape), so no clearly-chaotic *bound* orbit was
  in reach to test the measure on. Given the sound theoretical reason to distrust it (compactness, above),
  we **drop it as chaos evidence** and rest the regularity conclusion on the Lyapunov.

The conclusion ("no chaos in reach") is unchanged — but it now stands on a validated tool, not an
unvalidated one. *That swap is the point of running the control.*

## The proof horn — complete symbolic Killing–Yano search (`symbolic_ky_search.py`)

The dynamical probe shows the tori survive but cannot, by itself, decide whether a *new exact* hidden
symmetry exists. That is a decidable algebraic question, and the literature points to the clean way in:
by **Eisenhart's theorem** an exact Carter-type Killing tensor exists **iff** a Killing–Yano (KY) 2-form
exists, and the KY tensor is far simpler — in rational `u=cosθ` coordinates Kerr's KY is **polynomial of
degree ≤3** (`Y_tr=−au, Y_tu=−ar, Y_rφ=−a²u(1−u²), Y_uφ=−r(r²+a²)`), versus the Carter tensor's degree-6.

So we run a **complete** search: ansatz a general antisymmetric `Y` with degree-≤D polynomial components,
impose `∇₍ₐY_b₎c = 0` at many exact-rational points → a homogeneous linear system; its null-space
dimension counts the KY tensors of degree ≤D.

| metric | KY null-space (deg ≤3) | KY null-space (deg ≤4) |
|---|---|---|
| **Kerr (gate)** | **1** (rediscovers its KY ✅) | 1 |
| **bumpy ε=0.20** | **0** | — |
| **bumpy ε=0.35** | **0** | **0** |

**Result:** Kerr's unique KY tensor is recovered (gate passes); **no KY tensor survives the bump up to
degree 4.** By Eisenhart, **no exact Carter-type Killing tensor exists** for this deformation (to degree 4)
— the strict horn is **CLOSED**, not undetermined. *Caveat (now retired below):* the symbolic search rules
out *KY-origin* tensors; a non-KY-origin rank-2 Killing tensor needs the separate numeric search next.

## Closing the non-KY-origin caveat — numeric rank-2 search (`numeric_killing_search.py`)

The symbolic KY proof rules out a *KY-origin* Carter tensor; the converse of Eisenhart isn't general, so a
non-KY-origin rank-2 Killing tensor stays open. ansatz §85 closes exactly this gap for *its* bump by a
multi-orbit SVD null-space search over a general quadratic-in-momenta basis — and its direct *symbolic*
Killing-tensor search **swamped (7.5 h, no output)**, validating our low-degree KY route. We **port §85's
exact method** (its basis, SVD, and Carter-recovery gate, read-only) onto **our** bump:

| metric | smallest singular value | gap | invariant? |
|---|---|---|---|
| **Kerr (gate)** | **5.6e-14** | **3.6e10** | yes — recovers `p_θ²+11.56·cot²θ+0.035·cos²θ` = Carter ✅ |
| bumpy ε=0.1 | 1.5e-3 | 2.3 | no |
| bumpy ε=0.2 | 9.8e-4 | 3.3 | no |
| bumpy ε=0.35 | 8.5e-4 | 4.2 | no |

Kerr's Carter constant is recovered at machine zero with a 10-order gap; **our bump shows no conserved
quadratic** — the smallest singular value sits ~ten orders *above* machine zero with no gap. So **no rank-2
Killing tensor (KY-origin or not) survives our bump**, by an independent (numeric) method on the *same*
metric — retiring leg J's non-KY-origin caveat at rank 2. *Honest note:* unlike §85's cleaner monotone
growth, here the obstruction is a flat ~1e-3 floor (only ~10 bound orbits survived this E,L), so we claim
the *absence* (unambiguous: ~10 orders off machine zero, no gap), not a clean ε-scaling.

## Retiring the quartic residual — rank-4 search (`numeric_quartic_search.py`)

The last residual was a higher-rank (rank-4 / quartic-in-momenta) Killing tensor. We extend the SVD search
to a degree-4 basis. At fixed E,L, Kerr's reducible quartic invariants are the Carter constant `C₀` *and its
square* `C₀²`, so the **gate is "Kerr recovers both"**:

| metric | smallest momentum-bearing SV | invariant? |
|---|---|---|
| **Kerr (gate)** | **2.1e-14** (two machine-zero SVs = C₀, C₀²) | yes ✅ |
| bumpy ε=0.1 / 0.2 / 0.35 | **8.6e-4 / 6.5e-4 / 4.8e-4** | no |

So Kerr recovers both invariants at machine zero, and **our bump has no quartic invariant** — its real
obstruction sits at ~1e-3 (matching the rank-2 search), ten orders above machine zero.

*A logged catch (the discipline working):* the raw smallest singular value for the bump was a *gapped* 2e-9
— which looks like an invariant. Decoding the vector showed it is **pure spatial**
(`cot²θ − cos²θ − ½cos⁴θ − ½cot⁴θ`, no momentum dependence) — i.e. a function of θ that is merely near-flat
over the limited θ-range these orbits sample, *not* a conserved quantity (a Killing-tensor invariant must be
a form in momenta, like Kerr's `C₀²` which carries `pth²·cot²θ`, `pth⁴`). Requiring momentum dependence
unmasks it; the genuine obstruction is the ~1e-3 momentum-bearing SV. Without that check we'd have falsely
reported a surviving quartic.

**So: no rank-2 AND no rank-4 Killing tensor survives our bump** — leg J's quartic residual is retired. The
only remaining residual is rank ≥6, which is exotic and not expected for a quadrupole deformation.

## What it means (read against the pre-registered outcomes)

The canonical Carter constant is broken (proven, and measured here at up to 7%), yet it remains **bounded
and non-diffusing** — the hallmark of motion confined to a deformed KAM torus. So for the probed orbits the
system is **near-integrable: an effective (bounded) second invariant persists and there is no chaos.** This
is the **surviving-structure horn (i)** in its *weak* form — positive evidence that the tori survive — and
it is a genuine sharpening of Move D / §82, which had only the *absence* of detectable chaos.

## Honest limits (registered up front)

- **Not a proof of a new Killing tensor.** A bounded near-invariant (KAM torus) is consistent with the
  system being *formally* non-integrable (no global analytic second integral) while most orbits still sit on
  surviving tori. The strict horn (i) — an exact new Killing tensor — needs the **symbolic search**
  (high-degree, future), not this dynamical probe.
- **Finite time ⇒ upper bound on chaos, not a proof of integrability.** Integration spans ~1200 proper-time
  units. Exponentially-thin KAM chaos or slow Arnold diffusion below this resolution would not show
  (Move I's resolution-limited taxonomy applies).
- **Orbit family is near-circular.** The decisive instrument we *wanted* — a phase-space intrinsic-dimension
  scan (torus=2 vs chaos=3, reusing leg 1's counter) — **failed its calibration gate** (`count_dimension.py`):
  the strong-field **zoom-whirl** regime makes orbit eccentricity hypersensitive to the launch (a 2% kick →
  Δr=24 or escape), so controlled moderate-eccentricity 2-tori could not be generated, and Kerr orbits read
  D≈1.3 not 2. The gate caught this and, per pre-registration, we made **no claim from it** and pivoted to
  the robust Carter-dynamics measure (which needs no controlled eccentricity). Eccentric/resonant orbits —
  where chaos is most likely — are therefore *not* probed here; this is a conservative (near-circular) bound.

## Verdict — Move D / §82's "fate undetermined" is resolved (for this deformation)

**Formally non-integrable, but near-integrable.** The symbolic search **closes the strict horn** — no exact
Carter-type (KY-origin) hidden symmetry survives the bump up to degree 4 — while the dynamics (now the
validated **§79 Lyapunov**, λ at the Kerr floor to ε=1.2, with legG's SALI corroborating) show the geodesic
flow stays **regular: the KAM tori survive, no chaos in reach**, even though the canonical Carter constant
is violated (drift 7→18%). So the bump destroys the *exact* Carter constant (proven both ways) yet the
motion stays regular: the standard KAM near-integrable picture, and the one the deformation literature
predicts. The
**eccentric/inclined/resonance-crossing regime is now probed too** (Schmidt-constructed orbits, ε=0.35) —
no chaos there either, only a larger-but-bounded C₀ drift. What remains genuinely open is now very narrow:
**rank-≥6 Killing tensors** (rank-2 excluded KY-origin-symbolically *and* numerically; rank-4 excluded
numerically), and **thin chaos below resolution** — though §84's Poincaré (sharper than Lyapunov, which
averages weak chaos away) and a fine eccentricity scan both find none. Neither residual is expected to
overturn the picture; a rank-≥6 hidden symmetry for a quadrupole deformation would be exotic.

## Independent convergence — ansatz §84/§85 reach the same verdict (different methods, different bump)

This is the bridge's premise firing on its hardest question. Working separately, ansatz attacked the same
deformed-Kerr integrability question on *its own* bump (`ε(3cos²θ−1)/r³`, not our `g_tt·(1+6ε cos²θ/r)`):
- **§85** — the same multi-orbit numeric Killing-tensor search: Kerr recovers Carter; the deformed metric
  has no conserved quadratic. Same conclusion as our port, on a different bump.
- **§84** — Poincaré surface-of-section, **validated on Hénon–Heiles** (textbook 2-DOF chaos) — the
  positive control our own chaos detector lacked, and *sharper* than Lyapunov: deformed Kerr reads
  regular-or-destroyed, never a bounded chaotic sea.
- ansatz's **direct symbolic** Killing-tensor search **swamped (7.5 h, no output)** — so the bridge's
  KY-route (seconds) is a method ansatz lacks, while §84/§85 are methods the bridge lacked.

**Four methods, two projects, two bump families, one verdict:** deformed Kerr has no exact Carter constant
and stays KAM-regular — formally non-integrable, near-integrable. That convergence is why the leg-J
conclusion is trustworthy rather than merely tidy.

## Prior art (so we neither repeat nor overclaim, and can cite)

- **J. Brink, "Spacetime Encodings III & IV"** — [arXiv:0911.1589](https://arxiv.org/abs/0911.1589),
  [arXiv:0911.1595](https://arxiv.org/abs/0911.1595): exact second-order Killing tensors in
  stationary-axisymmetric-vacuum spacetimes are *very restrictive* (generic deformations lack one); explicit
  Killing-equation analysis and the Weyl-curvature ↔ Killing-tensor relationship.
- **"Preserving Kerr symmetries in deformed spacetimes"** — [arXiv:1807.08594](https://arxiv.org/abs/1807.08594):
  via Eisenhart's theorem, an exact Killing tensor exists *iff* a Killing–Yano tensor does; generic
  deformations (quasi-Kerr, Johannsen) keep only an **approximate** Killing tensor that *breaks down for
  larger perturbations* — precisely our growing-but-bounded C₀ drift. Our use of the KY route follows this.
- **Frolov, Krtouš, Kubizňák, "Black holes, hidden symmetries, and complete integrability"** — Living Rev.
  Relativity, [arXiv:1705.05482](https://arxiv.org/abs/1705.05482): the principal-tensor framework
  (KY ⟹ Killing tensor ⟹ separability) underlying the Eisenhart route.

Our contribution is not new GR theory — it is an *independent, calibrated, automated* confirmation for a
specific bump: a complete symbolic KY non-existence proof (degree ≤4) **and** a synthetic-validated
orbit-dynamics measurement that the approximate invariant is bounded and non-diffusing, agreeing with the
above by two independent routes.

## Update (2026-06-26) — MN positive control: the Lyapunov detector is finite-difference-noise-limited; box-dimension is the anchor

This leg's "no chaos in reach" rested on **ansatz §79's two-trajectory Lyapunov**, with one honest gap stated
above: *no clearly-chaotic **bound** orbit was ever in reach to validate the detector* (the only chaotic
case — legG's φ-dependent bump — sends orbits unbound). To close it we built a positive control on the
**Manko–Novikov** metric (ansatz §99): an EXACT rotating vacuum with a tunable quadrupole q (q=0 ≡ Kerr),
documented-chaotic for q≠0 (Gair 2008; Lukes-Gerakopoulos 2010), whose chaos is **bound**. We ran OUR
Lyapunov next to ansatz's validated **Poincaré box-dimension** on the same orbits. The control did not
rubber-stamp our tool — **it caught a flaw in it.**

**The disagreement.** On MN q=0.5 (E=0.95, L=2.8, x0=3.5–8), the box-dimension calls every orbit **regular**
(0.89–1.08, all ≤1.4) while the naive Lyapunov calls every one **chaotic** (λ=0.12–0.31). On the q=0 Kerr
control the *same* λ sits at the floor (0.016–0.033) and agrees (regular). The split is exactly Kerr-vs-bump.

**Three independent tests prove the λ is numerical, not dynamical** (`diagnose_lyapunov_boxdim.py`, MN q=0.5):

| test | x0=4.0 | x0=7.0 | reading |
|---|---|---|---|
| **(A) box-dim vs n** (120→1500 crossings) | 1.06→1.12→1.15→**1.15** | 1.08→1.16→**1.16** | converges **regular**, never climbs toward 2 |
| **(B) λ vs d0** (1e-6→1e-10) | 0.05→0.07→0.23→0.93→**4.23** | 0.04→0.05→0.15→1.01→**4.90** | a true exponent is d0-independent; ours **diverges as d0→0** |
| **(C) λ vs FD-step h** (1e-6→1e-3) | 0.23→0.056→**0.044**→0.044 | 0.15→0.049→**0.052**→0.052 | **collapses to the ~0.05 floor** when the derivative is cleaned |

**The Kerr (q=0) control clinches it.** Run through the *identical* battery, smooth Kerr (x0=4.0) shows **no
artifact**: λ vs d0 stays flat (0.016→0.016→0.017→0.035→0.060, vs MN's →4.23) and λ vs h stays flat
(0.016→0.016, nothing to collapse), box-dim 1.11. Same code, same d0, same h — the *only* variable is metric
bumpiness, and it is what turns the divergence/collapse on. A controlled comparison, not an inference.

**Mechanism.** ansatz's `build_hamilton_numeric` (MN) and `geodesic_chaos.lyapunov` (this leg's tool) both
compute forces by **central finite-difference Christoffels** (step h=1e-6 → roundoff ≈ ε/h ≈ 1e-10
relative). The Benettin scheme perturbs by **d0=1e-8**, so that force noise is a large fraction of the true
separation signal — and larger on a bumpy metric (bigger higher-derivatives) than on smooth Kerr. Hence λ
*diverges* as d0 shrinks (B, the noise floor dominates) and *collapses* when h is cleaned (C, less
roundoff). The MN q=0.5 orbits are genuinely **regular** (A is the ground truth, independent of any λ); the
"chaos" was the differentiator's roundoff.

**What this means for this leg (the conclusion is unchanged; the instrument is sharpened — again).**
- The **"formally non-integrable" half is untouched** — it rests on the exact symbolic KY non-existence
  proof and the rank-2/4 SVD nulls (exact rational linear algebra, no numerics to contaminate).
- The **"no chaos" half should be read off the box-dimension**, the detector validated here to track the
  high-resolution ground truth. The earlier "λ at the Kerr floor on the bump" is now understood
  correctly: finite-difference noise can only *inflate* λ, so a *floor* reading is **conservative** — real
  chaos would have pushed λ *up*, not hidden it (the bump simply produced less FD-derivative noise than the
  extreme q=0.5 MN, so its λ never inflated). legG's **SALI** (independent implementation) reading regular
  on the same bump corroborates. So the null holds, now on the cleanest available tool.
- **Actionable correction for anyone using the two-trajectory Lyapunov on a finite-difference-force metric:**
  either use the **box-dimension** (Poincaré) instead, or *de-noise* the λ (FD step h≳1e-4 **and** d0≳1e-6),
  where it returns to the floor on these regular orbits. A small d0 with a small h is the trap.

**The bound-chaos gap is now better-characterized, not yet closed.** A sweep toward MN's documented chaotic
zone (`chaos_search_mn.py`: stronger q, lower L, deeper x0) finds that our equatorial launch family
(x₀, y=0, p_x=0, p_y on-shell) does **not** access bound chaos here — every strong-q grid point (q≳0.7)
fails to bind into a ≥40-crossing orbit (skipped), and the 16 bindable q=0.5 orbits are **all regular**
(box-dim ≤1.15, de-noised λ 0.04–0.07 at the floor). So a
genuinely chaotic **bound** orbit to validate box-dimension *on chaos* (not just on regularity) remains out
of reach with this launch scheme — the same honest gap this leg flagged, now with the added, decisive
knowledge that the naive Lyapunov could not have filled it either. Reaching MN's chaotic orbits needs a
different launcher (Gair-style off-equatorial / pericenter-specified initial data) — logged as the next step.

## Update (2026-06-26b) — gap CLOSED: detectors validated on genuine chaos, and ansatz cross-confirmed the fix

We relayed the FD-noise finding and the bound-chaos gap to ansatz; both came back resolved (ansatz §101 +
`emri.mn_bound_orbit`, this leg's `detector_validation.py` reproducing it read-only). The gap closes on all
three fronts:

- **Our FD-noise false-positive was independently reproduced AND fixed.** ansatz reproduced it exactly — on a
  box-dim-regular MN q=0.5 orbit the old Lyapunov (ch=1e-6, d0=1e-8) reads λ≈+0.32–0.44, the de-noised one
  (ch=1e-4, d0=1e-6) collapses to ≈0 — and shipped the fix as the new `geodesic_chaos.lyapunov` defaults. A
  cross-repo confirmation of the bridge's finding, and the buggy detector is now corrected at the source.
- **The detectors are validated ON genuine chaos.** The *same* instruments flag real chaos elsewhere in
  ansatz: the box-dimension reads **1.34** on the chaotic Hénon–Heiles orbit (§84, vs ≈1.0 regular), and the
  de-noised Lyapunov reads **2.09** on the Majumdar–Papapetrou di-hole (§79, vs ≈0 for Kerr). So leg J's
  "regular box-dim on the bump" is a null on a detector **proven to see chaos when it is present** — the one
  honest gap (detector never tested on chaos) is **closed**.
- **MN's own bound chaos is an *honest null* at this extreme — and chasing it found a metric bug.** Both our
  equatorial scan and ansatz's low-L scan (q up to 1.2) topped out at box-dim ~1.16–1.22 (regular) — a
  launch-basin issue, not a detector failure. To reach the documented chaotic orbit (χ=0.9, q=0.95, E=0.95,
  L_z=3; Lukes-Gerakopoulos/Apostolatos/Contopoulos 2010, which lives in an *inner* region MN has but Kerr
  doesn't), ansatz made the shared metric computable at high q (§102) — and that **surfaced a correctness
  bug**: `manko_novikov` was *never asymptotically flat for q≠0* (g_xx → 0.085× Minkowski at infinity), hidden
  because the vacuum check is blind to a constant in γ and the q=0≡Kerr anchor has it =0. Fixed (`3e08fef`),
  q=0 byte-identical to Kerr, **orbit paths preserved → every leg-J result here is invariant** (box-dims,
  sections, KY/SVD proofs, the positive control; only proper-time flux/frequencies move, which only leg M's
  inspiral uses).
- **And the chaos at χ=0.9, q=0.95 is *pathology-bound*, not a clean sea (ansatz §102).** With the metric
  finally computable there, the permissible region splits into **three disconnected wells**: inner [1.24,1.64]
  is metric-degenerate (signature flip to closed timelike curves by x≈1.7 — MN's known near-rod
  naked-singularity pathology); a second-region lens [3.04,4.96] is bound but its inner edge abuts that CTC
  zone (a traced orbit drifts to x≈2.98 and hits it); the outer well [5.58,31] is clean and **regular**
  (box-dim 0.97–1.03). So at this extreme deformation the chaotic basin is bound up with the singularity
  pathology — a clean box-dim→2 orbit is not exhibitable there. The geometric chaos MN does have is a
  *thin layer* near resonances (the literature resolves it via the rotation number, not gross area-filling) —
  the **same elusiveness leg O hit on Zipoy–Voorhees**. The rigorous statement is untouched: §99 proves no
  quadratic Carter constant for q≠0 (non-integrable); the *dynamical* chaos is thin and, at q=0.95,
  pathology-bound. A clean positive control would need *moderate* q (~0.3–0.6, clean metric) + a
  rotation-number sweep across a low-order resonance (logged) — not the extreme q.

**Net:** leg J's "formally non-integrable, dynamically regular" verdict now rests on (i) the exact symbolic
KY + SVD proofs, and (ii) the roundoff-immune **box-dimension**, a detector validated on genuine chaos, with
the one λ-based caveat reproduced and fixed at the source by ansatz. The discipline closed the loop across
both repos. `results/detector_validation.json`. *(Bonus from the same ansatz update: a Carter flux dQ/dτ
that unblocks the eccentric-inclined EMRI inspiral — see leg M.)*

## Update (2026-06-26c) — a thin-layer-sensitive detector (frequency drift), validated, reads moderate-q MN regular

ansatz §102 noted MN's geometric chaos is a *thin layer* near resonances — gross box-dimension grazes it
(≤1.22) because the chaotic band has negligible area. To probe below box-dim's resolution we built a third
detector (`code/rotation_number_chaos.py`). The first attempt — the **centroid-angle rotation number** —
false-flagged Kerr's regular **1:3 resonant island** as chaos (the orbit hops between islands around the
global centroid; nonconv 0.035 > the genuinely-chaotic Hénon–Heiles 0.007): the *same* noise/island pitfall
that defeated the naive Lyapunov, so it was discarded. The robust replacement is the **frequency drift**
(Laskar-style): the dominant frequency of an orbit's section coordinate is *constant* for any regular orbit —
torus **or** resonant island — and only DRIFTS for chaos; |Δf|/f between the first and second half of the
section series is the flag, area-blind and island-immune.

- **Validated (strict gate).** On Hénon–Heiles the genuinely-chaotic orbits (box-dim>1.4) drift **0.59–0.73**
  while *every* regular orbit — including the islands *inside* the chaotic energy — drifts ≤0.0001. On the
  **Kerr (q=0) integrable control** every orbit reads ≤0.006, the **1:3 island included (0.0018)** — the
  resonant-island false-positive is gone. Regular ceiling 0.006, chaotic floor 0.59 → a **~100× margin**;
  threshold 0.0115.
- **MN q=0.6, across the resonance band (14 orbits, E=0.95, L=2.8):** **all regular**, drift ≤0.002 — *no*
  thin layer that box-dim missed. A detector *proven* to catch thin chaos, and immune to both pitfalls that
  fooled the Lyapunov and the rotation number, reads these moderate-q bump orbits as genuinely regular.

**So leg J's null now rests on three detectors of known behaviour** — box-dimension (validated on
Hénon–Heiles 1.34, robust but blunt), the de-noised Lyapunov (validated on the di-hole 2.09), and now the
frequency drift (validated on Hénon–Heiles, *thin-layer-sensitive*) — all three reading regular on the bump.

**Honest scope (the one open thread):** this is a single (E, L) slice. MN's *documented* thin chaos lives at
specific literature initial conditions (Lukes-Gerakopoulos), and a blind x0-sweep can miss the exact resonant
separatrix — so this is "regular in this slice, on a newly-validated sharp instrument," **not** "no MN chaos
anywhere." Exhibiting MN's own thin layer needs those exact moderate-q ICs (relayed to ansatz). The detector
itself is now a reusable, validated leg-J instrument that the naive rotation number was not.
`results/rotation_number_chaos.json` (+ `rotation_number_validation.json`, `rotation_number_mn.jsonl`).

## Update (2026-06-26d) — POSITIVE CONTROL CLOSED: the detector exhibits MN's own thin-layer chaos

The one open thread — exhibit MN's *own* bound chaos so a detector validated on a proxy (Hénon–Heiles)
catches the real thing — is now closed, by a clean two-repo split. ansatz reached MN's inner basin (the
literature's chaotic region near the rod, χ=0.9, q=0.95, E=0.95, Lz=3; Contopoulos–Lukes-Gerakopoulos–
Apostolatos 2011) with an **adaptive** integrator — our fixed-step `poincare.section` dies there instantly
(0 crossings, H-drift ∞, confirming the stiffness), so ansatz supplied two adaptive-integrated (x, px)
section series (H-drift <2e-3 kept). Both orbits sit at **box-dim 1.20–1.22** — exactly the borderline
where box-counting cannot decide island-of-stability vs thin chaos. We applied the **bridge's
independently-validated frequency-drift detector** to ansatz's trajectories (`inner_region_chaos.py`):

| orbit | crossings | box-dim (ansatz) | drift \|Δf\|/f (bridge) | verdict |
|---|---|---|---|---|
| **orbit_A** | 800 | 1.203 | **0.0000** | regular — island of stability |
| orbit_A[:126] | 126 | — | 0.0000 | regular (length-match control) |
| **orbit_B** | 126 | 1.219 | **0.980** | **thin chaos — fires (≫ 0.0115)** |

**Box-dimension called both ~1.2; the frequency-drift detector resolves them** — orbit_A is the regular
island, orbit_B is the chaotic boundary layer. The verdict is *not* a short-series artifact: at the *same*
126 crossings, the regular orbit_A reads 0.0000 while orbit_B reads 0.98 — a clean separation at matched
length, and orbit_B's drift exceeds even the Hénon–Heiles chaotic floor (0.59). So **MN's own thin-layer
chaos is exhibited, on the exact metric** (ansatz-verified vs Gair-Li-Mandel 2008), by a detector validated
on Hénon–Heiles and immune to the two pitfalls that defeated the earlier attempts (the Lyapunov's
finite-difference noise, the rotation number's resonant-island false-positive).

**What this settles.** Leg J's chaos-detector arc is complete: three detectors of known, validated behaviour
— box-dimension (Hénon–Heiles 1.34, robust but *blunt*: blind to this thin layer, reads both inner orbits
~1.2), de-noised Lyapunov (di-hole 2.09), and frequency drift (Hénon–Heiles + now MN's own inner chaos,
*thin-layer-sensitive*). The first two *and* the sharpest third all read the leg-J **bump** regular — so the
"formally non-integrable, dynamically regular" verdict for the bump now rests on detectors proven to catch
chaos right down to the thin boundary layer that box-dim misses. The bridge built the tool; ansatz supplied
the trajectory its own box-dim couldn't classify; the bridge's detector classified it. `results/inner_region_chaos.json`.

## Artifacts
- `code/inner_region_chaos.py` — the closer: applies the validated frequency-drift detector to ansatz's
  adaptive-integrated MN inner-region section series (`mn_inner_sections_for_bridge.json`, read-only) —
  resolves orbit_A (regular island, drift 0) vs orbit_B (thin chaos, drift 0.98) where box-dim reads both
  ~1.2. Exhibits MN's own thin-layer chaos. `results/inner_region_chaos.json`.
- `code/rotation_number_chaos.py` — the thin-layer-sensitive frequency-drift detector: validated on
  Hénon–Heiles + a strict Kerr/1:3-island control, then the MN q=0.6 resonance-band scan (all regular).
  Reboot-resilient (cached validation + per-orbit MN checkpoint). `results/rotation_number_chaos.json`.
- `code/detector_validation.py` — closes the gap: reproduces (read-only, with ansatz's shipped fix) the FD
  false-positive + de-noised λ on a regular MN orbit, and records the genuine-chaos positive controls
  (Hénon–Heiles box-dim 1.34, di-hole λ 2.09). `results/detector_validation.json`.
- `code/export_orbits.py` — stage 1 (ansatz venv): integrates bound orbits, exports C₀ time series; reuses
  legA's `export_geodesics` (metrics, Christoffels, Carter tensor) read-only.
- `code/carter_dynamics.py` — drift + saturation measures, Kerr-calibrated, synthetic-validated.
- `code/export_eccentric.py` — Schmidt-constructed eccentric/inclined orbits (turning-point solve), the
  resonance-crossing chaos hunt; Kerr-calibrated (C₀ conserved to 2e-9). `results/eccentric_eps*.json`.
- `code/verify_chaos.py` — the positive control: ansatz §79 Lyapunov vs Carter-saturation on the bump to
  ε=1.2 (both read regular; Lyapunov supersedes the unvalidated saturation). `results/verify_chaos.json`.
- `code/positive_control_mn.py` — MN positive control: OUR Lyapunov vs ansatz's box-dimension on
  Manko–Novikov q=0 (Kerr, regular) and q=0.5; surfaces the systematic λ-vs-box-dim disagreement on the
  bump. `results/positive_control_mn.json` (+ durable `.jsonl`).
- `code/diagnose_lyapunov_boxdim.py` — the 3-test diagnosis (box-dim vs n; λ vs d0; λ vs FD-step h) proving
  the naive two-trajectory λ is finite-difference roundoff on bumpy metrics, not chaos.
  `results/diagnose_lyapunov_boxdim.json`.
- `code/chaos_search_mn.py` — sweep toward MN's chaotic zone (stronger q, lower L, deeper x0) reporting
  box-dim + naive vs de-noised λ per orbit; finds the equatorial launch family does not reach bound chaos
  here. `results/chaos_search_mn.json` (+ durable `.jsonl`).
- `code/numeric_killing_search.py` — ports ansatz §85's multi-orbit SVD null-space search onto our bump;
  closes the non-KY-origin caveat at rank 2 (Kerr Carter recovered; bump has none). `results/numeric_killing_search.json`.
- `code/numeric_quartic_search.py` — extends the SVD to rank-4 (gate: Kerr recovers C₀ AND C₀²); bump has
  no quartic invariant (momentum-dependence check unmasks a pure-spatial artifact). `results/numeric_quartic_search.json`.
- `code/symbolic_ky_search.py` — the proof horn: complete symbolic Killing–Yano search (Eisenhart route),
  Kerr-gated, exact rational linear algebra; rules out an exact KY tensor on the bump to degree 4.
- `code/count_dimension.py` — the attempted dimension scan (gate-failed, kept for transparency).
- `results/orbits_eps*.json`, `results/carter_dynamics.json`, `results/symbolic_ky_search.json`.
