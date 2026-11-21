# V28: sealed Bridge predictions for Cuspis's direct same-tip coefficient (2026-11-21, before Cuspis's result)
Purpose: Cuspis is building a direct 2D computation of the same-tip coefficient C+ at real alpha = 0.3. Three
candidate formulas exist:
- Cuspis's CH05 route;
- Neon T20 with outer vector v0 on both legs;
- Neon T23 with asymmetric legs v_R = e^{-alpha p} e^{-(u/2)cosh p} (left) and v_L = e^{+alpha p} e^{-(u/2)cosh p}
  (right).
The Bridge re-implements the T20 and T23 formulas independently (own code, not Neon's or Cuspis's) and SEALS the
absolute predicted values by commit, before Cuspis's direct result exists. T23 is held from Cuspis.

Formula: C+ = -(lambda/(4pi^2 Gamma(1+alpha)^2)) int dq e^q (e^q/2)^{2alpha} vL'^T (1 - lambda^2 R^T R)^{-1} R^T vR',
with u = e^q, lambda = sin(pi alpha)/pi and
R(p,p') = e^{-(u/2)cosh p} e^{(alpha-1/2)(p-p')}/(2cosh((p-p')/2)) e^{-(u/2)cosh p'}.
Leg placement follows Neon's written formula.

**Checks (these test claims too):**
- **S1:** the m = 0 term with v0 reproduces the Born closed form,
  -(sin(pi a)/(4pi^3))(Gamma(a+1/2)/Gamma(a+1))^2 Gamma(2a+1/2)Gamma(3/2)/Gamma(2a+2), to 1e-6 at a in {0.05, 0.3, 0.45}.
- **S2 (T23's claim b):** the m = 0 term with (v_R, v_L) reproduces T23's closed form, with Gamma(3a+1/2)Gamma(3/2-a)
  in place of Gamma(2a+1/2)Gamma(3/2), to 1e-6 at the same a. (Leg orientation: try both assignments; report which
  reproduces it.)
- **S3:** grid convergence of the resummed values (N_p doubling, p and q range extension) at < 1e-6 relative.
- **SEAL:** the absolute C+resum(0.3) for v0 and for (v_R, v_L); their ratios to their own m = 0 terms; and the same
  at a = 0.2 and 0.4.

The controls S1/S2 test the code paths. They are not pre-run separately, because they ARE the claims being checked
and the seal values are not compared to anything yet.

## Addendum B (12:30, before computing anything against T25): per-slice shape test, T25 BIE vs the two leg candidates
Data: Neon T25's direct BIE Delta C(w, a) (neon_work/dkappa/T25_summary.md; UNVERIFIED; the code was built blind from
Cuspis's spec, with no candidate formulas). In 2D at m = 1, a slice at separation w is the u = w slice of the
k_y-integrated problem. So the Bridge's per-slice bilinear B_X(u) = v_l^T (1 - lambda^2 R^T R)^{-1} R^T v_r
(V28 code) must be proportional to Delta C(w = u, a) with a factor that depends on a only, if candidate X is right.
- **Test:** k_X(w) = Delta C_BIE(w)/B_X(w) for X in {RL (T23), v0 (T20 symmetric)}:
  - at a = 0.3, w in {1, 0.3, 0.1, 0.03, 0.01} (w = 3 is excluded: its BIE relative error is 6%);
  - at a = 0.2 and 0.4, w in {0.3, 0.1, 0.03, 0.01}.
- **PASS for X:** at every twist, the max/min ratio of k_X over w is within 1 + max(3 x the largest BIE relative
  error in that set, 1e-3).
- **Decision:** RL is supported if RL passes AND v0 fails at every twist. v0 is supported if the reverse holds.
  Anything else is inconclusive.
- **Descriptive:** whether k_RL is a simple constant (e.g. related to -lambda/(4pi), giving an absolute
  cross-check).
- **Pre-check:** both B_X are computed by the V28 code paths that already reproduced their closed forms to 1e-14.
  The comparison arithmetic is trivial.
