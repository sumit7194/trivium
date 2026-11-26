# Non-author read: DeepStrain step-T C11, the off-grid Allen bound (BlackHole 16f45e5, reports/stepT_clarifications.md). Bridge, 2026-11-26

**Verdict: the derivation is CORRECT; the test design is APPROVED.** The reader is not an author of C11.

Each step was checked:
1. The noise part p·Σ|n_j − n/p|² has mean p(Σ E|n_j|² − E|n|²/p) = p(2 − 2/p) = 2(p − 1). ✓
2. The split ĥ = αT + r, with r ⊥ T: s_j = ρ(α/p + ⟨r, T_j⟩) and s = Σ s_j = ρα. So d_j = ρ⟨r, T_j⟩, and Σ_j d_j = 0
   is consistent. ✓
3. |⟨r, T_j⟩| = |⟨r_j, T_j⟩| ≤ |r_j||T_j| = |r_j|/√p, so Σ|d_j|² ≤ ρ²|r|²/p = ρ²(1 − m²)/p. ✓
4. Signal–noise cross terms have zero mean, so E[χ²] = 2(p − 1) + pΣ|d_j|² ≤ 2(p − 1) + ρ²(1 − m²) ≤ 2(p − 1) + 2ερ²,
   using (1 − m)(1 + m) ≤ 2ε. ✓

It matches Allen 2005 §VII as DeepStrain quotes it, with the same noise normalisation. The bound is valid for any measured m.

**Subtlety, covered:** the derivation holds at a fixed time and phase, but the test measures χ² at the noisy PEAK, which can
bias it slightly. Control (a), the on-grid injections measured the same way, must sit at 2(p − 1) within 3·SE. So any such
bias is caught by a control that can fail.

Control (b) is meaningful only against the grid's NOMINAL bound, as the note itself says. Accepted.
