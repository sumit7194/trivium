-- Vacuity instances from the OnlyKerr faithfulness read (2026-11-23). NOT YET RUN.
-- Run with: import OnlyKerr.Glue; open OnlyKerr Complex. Simp sets may need small adjustments.
example (a y : ℝ) : DD a y ≠ 0 := by
  intro h
  have hr := congrArg Complex.re h
  have hi := congrArg Complex.im h
  rw [DD_eq] at hr hi
  simp [pow_two] at hr hi
  have hy : y = 0 := by linarith
  subst hy; nlinarith [sq_nonneg a]
example : CertCases (1/2) 0 1 := Or.inl (by norm_num)
example : CertCases (1/2) 1 (I / 10) := by
  right; right; constructor
  · norm_num
  · simp; norm_num
example : ¬ (0 < ((I / 10 : ℂ) ^ 2).re) := by simp [pow_two]; norm_num
example : ¬ CertCases (1/2) 1 (2 * I) := by
  simp [CertCases, pow_two]; norm_num
example : (h1 (0:ℚ) 1).trace = -3 := by rw [curzon_tr_h1 _ _ one_ne_zero]; norm_num
example : (3 * ((2:ℤ):ℝ) ^ 2) / (3 * ((2:ℤ):ℝ) ^ 2 - 4) = 3 / 2 := by norm_num
