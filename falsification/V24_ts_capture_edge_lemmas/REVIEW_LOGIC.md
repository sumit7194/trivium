# V24 review: the logic of Fable's capture-edge reduction (REVIEW.md §1–§4; L3_ANALYTIC.md §3–§6). Bridge, Opus 5.5, 2026-11-20

The inequalities were checked separately: R and I1/I2 are exact or interval; I3 is a sample (V24 FINDINGS).
This file covers the arguments only.

## Verdict: SOUND, on the points I checked step by step. One region (the brake-latitude sliver) is unverified.

1. **Theorem 2 (F4).** Agreed, including the fix that "⟺" must read "⟹" (F6).
   - P⁻¹(U) ⊂ U holds, because backward iterates of the arc z*→h stay on that arc.
   - So iterates of D-points land on ∂D only on S, and the E_k are open and disjoint, given L2 and L3.
   - F5 is right: the sentence about mouth endpoints is false but unused.
2. **Lemma L2′ (L2 from I1, I2, F-b′, U1).** Agreed.
   - **Step 2 (returns).** In flat coordinates v̈ = −V_v = 2y sin v ∂V/∂s > 0 for y > 0. That uses I2, which needs
     x ≤ 77.1, and Hill's region gives x ≤ 77.06.
   - A bounded convex v that never crosses the equator would converge with y bounded below, contradicting v̈ ≥ c > 0.
   - **Step 5 (no hole).** P maps ∂H injectively into a segment, so ∂H is homeomorphic to a compact subset of ℝ. Such a
     set has trivial Čech H¹ and, by Alexander duality, does not separate the plane, while the boundary of a bounded
     open set does. Correct.
3. **Lemma G (γ's curve is a global one-way gate).** Agreed as a deduction from I3 on a foliation of Z.
   - At a tangency to a leaf, τ̈ < 0, so τ has only strict maxima.
   - A monotone, bounded τ(t) would have a nonempty ω-limit on one leaf, invariant with τ̇ ≡ 0. That contradicts
     τ̈ < 0 there.
   - The leaf τ = 0 is x = 9.3 < 9.49, which hands over to the funnel (Lemma F, I1).
   - **The foliation must cover all of Z, including the sliver beyond the brake latitude,** where Fable continues the
     leaves as straight lines and reports C ≤ −3.0. V24 did NOT check the sliver (it sampled v ≥ v_b + 1e−3). Open item.
4. **Hole lemma, Proposition E, Lemma L3′.** Agreed in structure.
   - The hole lemma is the L2′ argument applied to any Jordan J outside D with x > x* (> 9.49).
   - L3′ propagates the lobe J₀ = cl(O₁) by the hole lemma for j₀ returns.
   - Each J_i misses D, because its boundary can't cross S except through the W^u arc (excluded by C1) or a
     transversal corner (excluded by T).
   - C2 lands it in cl(Q⁻), where Lemma Q (block plus gate) finishes.
   - Proposition E's path argument is fine: straight-in is open; there's a first non-straight-in point; it must lie on
     W^s or be trapped.
5. **Lemma Q and hypothesis N (hyperbolic block).** Standard: cone conditions at an analytic area-preserving saddle.
   Needs explicit constants (interval Newton plus cones) to be a proof.

## What is now established, and how
- **Exact or interval:** the flat-plane form; I1; I2.
- **Sample, independent:** I3, with margin 0.632.
- **Logic reviewed:** Theorem 2 (as "⟹"), Lemma L2′, Lemma G (modulo the sliver), the hole lemma, Proposition E,
  Lemma L3′, Lemma Q.

## Still open, to make Fable's conditional theorem a full one
1. **I3 as a proof:** a validated γ enclosure plus interval arithmetic over the leaf zone, including the sliver.
2. **Hypothesis N:** an interval-Newton fixed point and cone conditions at z*.
3. **The 1D lobe conditions T, C1, C2** (with F-b′ and U1): follow W^u_out from z* through h and m for ~j₀ + 6 ≈ 8 returns,
   with the W^u–S gap of 2e−6 to 1e−5 resolved. Float64 sample first (independent of Fable's c04/c05/c10), then
   validated.
4. **The transverse crossing at h**, rigorously: the CAPD-type step, quantum's route.

Items 2–4 are exactly what a computer-assisted horseshoe proof for TS needs anyway, so this route and B-5 share their
remaining work.

## Addendum (2026-11-20, afternoon): Lemma G at the brake latitude. A GAP in the straight-line continuation
- **Float geometry (exploratory, scratch scripts; planning only).**
  - Below v_b the Hill region inside γ is a cap less than 1e−3 thick in v, with u ∈ [u₁, ≤ u_b].
  - In the cap: V_u ≥ 0.999, V_v ≈ −163.
  - γ's slope at the brake point: g′(v_b) ≈ −0.0061.
- **The corner sign (by hand).** τ = (u − u₁)/(g(v) − u₁) above v_b, and τ = (u − u₁)/(g(v_b) − u₁) on Fable's
  straight continuation below.
  - So τ_v⁺ = −τg′/(g − u₁) > 0 and τ_v⁻ = 0.
  - For an orbit crossing v = v_b in EITHER direction, τ̇ jumps by (τ_v⁺ − τ_v⁻)|v̇| > 0. That is an upward kink, so a
    local MINIMUM of τ is possible there.
  - Lemma G's argument ("τ has only strict maxima") therefore does not go through as written. Fable's own list had
    flagged "the brake ends and the sliver" for attack.
- **Alternatives fail in the cap.** Any corner with the safe sign needs a continuation slope ≤ g′(v_b). But the
  term g′V_v is then positive, and C in the cap becomes worse.
- **Proposed fix (to register before checking).**
  - Continue the leaves C¹: matching slope, g″ allowed to jump. Then τ is C^{1,1}. At a tangency on v = v_b, both
    one-sided values of C are negative, so the maximum is still strict.
  - Float: max C over the cap ≈ −0.0010, attained at the brake point. There C → 0 by continuity with γ, where C ≡ 0
    on τ = 1.
  - So the proof needs C < 0 on the cap away from the brake point (interval), plus a LOCAL analysis at the brake
    point (Taylor jets: ∂C/∂τ ≈ 3.0 there).
- **Status:** Lemma G is sound except at the brake latitude, where the continuation must be changed and one local
  lemma added. This item is on the Bridge's list.
