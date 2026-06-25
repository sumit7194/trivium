# Leg N — Findings: discover→verify generalizes to a holonomy (geometric-phase) invariant (B3)

*Run 2026-06-24 (backlog B3). Move A's discover→verify pipeline certified a Killing tensor — a DYNAMICAL
invariant. B3 aims the same architecture at a different CLASS of hidden structure: the geodetic-precession
HOLONOMY (the angle a parallel-transported gyroscope precesses per orbit) — a geometric phase, the GR cousin
of a Berry phase / Aharonov–Bohm holonomy (cf. tabula §113/§114). Reuses legA's machinery read-only.*

## Result in one line

The discover→verify architecture **generalizes beyond Killing tensors**: a blind probe recovers the
geodetic-precession holonomy from a gyroscope's direction time series alone (**1.322** rad/orbit at r=8M),
and the exact engine verifies it against the closed form (**1.316**, agree to 0.5%; parallel transport
matches 2π(1−√(1−3M/r)) to ~2–3% across radii). So the same pipeline certifies a geometric-phase invariant —
and the holonomy is shown to be *geometric* (spin shifts it via frame-dragging), not a protected integer.

## VERIFY (the gate) — parallel transport vs the closed form

| r | parallel-transport precession | closed form 2π(1−√(1−3M/r)) | error |
|---|---|---|---|
| 6M | 1.806 | 1.840 | 1.9% |
| 8M | 1.337 | 1.316 | 1.6% |
| 10M | 1.055 | 1.026 | 2.8% |
| 15M | 0.683 | 0.663 | 2.9% |

Integrating the parallel-transport equation `dV^μ/dτ = −Γ^μ_αβ u^α V^β` around a circular geodesic reproduces
Schwarzschild's geodetic precession to ~2–3% (numerical: constant-Γ + discrete transport + frame readout).
Gate passes (<5%).

## DISCOVER (blind) → VERIFY

From *only* the gyroscope-direction time series at r=8M (no metric, no formula), an unwrap-and-fit of the
inertial rotation rate gives a per-orbit holonomy of **1.322** — matching the exact geodetic precession
**1.316** to 0.5%. The discover→verify loop closes for a geometric-phase invariant, exactly as it did for
the Carter Killing tensor in Move A — **a broader instrument, same architecture.**

## The holonomy is GEOMETRIC, not topological (the contrast)

| spacetime (r=8M) | holonomy / orbit |
|---|---|
| Schwarzschild | 1.337 |
| Kerr a=0.6 | 1.535 |
| Kerr a=0.9 | 1.636 |

The **spin shifts the holonomy** (frame-dragging adds to the geodetic precession) — confirming it captures
real geometry, and is *not* a deformation-invariant integer (unlike a true topological charge). One honest
wrinkle that connects to leg J: the **θ-quadrupole bump is invisible to an equatorial gyroscope**
(`cos²θ=0` at the equator, so g_bumpy is unmodified there) — the equatorial holonomy is bump-blind. So
probing leg J's bump through a holonomy needs an **off-equatorial** loop (a spatial loop enclosing the
curved off-equator region, where the holonomy = the enclosed curvature flux) — logged as the next step.

## Honest limits
- Parallel-transport precession is numerical (~2–3%); the Kerr frame readout uses the simple (e_r, e_φ)
  orthonormal angle, slightly approximate where g_tφ≠0 — fine for the contrast, not a precision spin-precession.
- Equatorial circular orbits only; the off-equatorial / spatial-loop holonomy (which would see the θ-bump)
  is the natural extension.
- Re-derives a textbook quantity (geodetic precession); the contribution is showing the *discover→verify
  architecture* certifies a geometric-phase invariant, broadening Move A beyond Killing tensors.

## Artifacts
- `code/holonomy.py` — parallel transport, the closed-form gate, the blind discover, the spin contrast.
  `results/holonomy.json`.
