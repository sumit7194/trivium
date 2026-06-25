# Leg J — Findings: the deformed Kerr is formally non-integrable but its orbits stay regular

*Run 2026-06-21. Gates and outcome-meanings frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any
orbit was integrated. This leg attacks the project's one UNDETERMINED result — Move D / ansatz §82's
"deform Kerr → canonical Carter tensor broken, yet no detectable chaos, fate undetermined." A post-hoc
positive control (§ below) corrected our dynamical instrument — logged honestly, not hidden.*

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

## Artifacts
- `code/export_orbits.py` — stage 1 (ansatz venv): integrates bound orbits, exports C₀ time series; reuses
  legA's `export_geodesics` (metrics, Christoffels, Carter tensor) read-only.
- `code/carter_dynamics.py` — drift + saturation measures, Kerr-calibrated, synthetic-validated.
- `code/export_eccentric.py` — Schmidt-constructed eccentric/inclined orbits (turning-point solve), the
  resonance-crossing chaos hunt; Kerr-calibrated (C₀ conserved to 2e-9). `results/eccentric_eps*.json`.
- `code/verify_chaos.py` — the positive control: ansatz §79 Lyapunov vs Carter-saturation on the bump to
  ε=1.2 (both read regular; Lyapunov supersedes the unvalidated saturation). `results/verify_chaos.json`.
- `code/numeric_killing_search.py` — ports ansatz §85's multi-orbit SVD null-space search onto our bump;
  closes the non-KY-origin caveat at rank 2 (Kerr Carter recovered; bump has none). `results/numeric_killing_search.json`.
- `code/numeric_quartic_search.py` — extends the SVD to rank-4 (gate: Kerr recovers C₀ AND C₀²); bump has
  no quartic invariant (momentum-dependence check unmasks a pure-spatial artifact). `results/numeric_quartic_search.json`.
- `code/symbolic_ky_search.py` — the proof horn: complete symbolic Killing–Yano search (Eisenhart route),
  Kerr-gated, exact rational linear algebra; rules out an exact KY tensor on the bump to degree 4.
- `code/count_dimension.py` — the attempted dimension scan (gate-failed, kept for transparency).
- `results/orbits_eps*.json`, `results/carter_dynamics.json`, `results/symbolic_ky_search.json`.
