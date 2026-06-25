# Leg K — Pre-registration: the information-theoretic count (THE_BRIDGE §9, backlog A9)

*The §9 open question, verbatim: "Do MDL, moduli dimension, and measured DOF all give the same count for a
black hole? Where do they part, and why?" The count-triangle has three lenses (moduli/proved, neural-knee,
measured-δ). This adds a fourth: the information-theoretic dimension of the observation manifold. Reuses
leg 1's observation data read-only.*

## Method
- **Linear MDL** — Minka's PPCA-MDL/BIC on the standardized observation covariance spectrum (principled,
  not a heuristic threshold).
- **Nonlinear intrinsic dimension** — the Levina–Bickel (2004) MLE on nearest-neighbour distances
  (curvature-aware).

## Frozen predictions
- **G1 (calibration):** Schwarzschild (1 modulus) calibrates each estimator's bias.
- **P1:** the *linear* MDL will OVERCOUNT — the observation manifold is nonlinearly embedded, so a linear
  code needs extra dimensions (the leg-7b curvature inflation, in the extreme).
- **P2 (the decisive test):** the *nonlinear* intrinsic dimension recovers the **observable** count
  (Schwarzschild 1, RN 2, dyonic 2). The sharp sub-test is **dyonic vs RN**: if dyonic's ID ≈ RN's, the
  Q²+P² observable degeneracy (electric≡magnetic, observable < algebraic 3) is confirmed by a 4th lens;
  if dyonic's ID ≈ RN's + 1, it parts (the manifold keeps the 3rd algebraic dimension).
- The MLE is known to be upward-biased, so the verdict reads **steps** (Schwarzschild→RN→dyonic), not
  absolute values.

## What each outcome means
- Nonlinear ID steps 0→+1→+0 (dyonic = RN) ⇒ all four lenses agree on the observable count; any "parting"
  is the linear code (curvature), not the physics — a clean §9 answer.
- dyonic ID step ≈ +1 ⇒ the degeneracy is not visible to the information count; a real physical parting to
  explain.
