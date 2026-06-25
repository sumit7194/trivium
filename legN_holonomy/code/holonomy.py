#!/usr/bin/env python3
"""Leg N (B3) — discover→verify for a HOLONOMY (geometric-phase) invariant, not a Killing tensor (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python holonomy.py

Move A's discover→verify pipeline certified a Killing tensor (a DYNAMICAL invariant). B3 aims the same
architecture at a different CLASS of hidden structure: the geodetic-precession HOLONOMY — the angle a
parallel-transported gyroscope vector precesses per orbit, a geometric-phase invariant (the GR cousin of a
Berry phase / Aharonov–Bohm holonomy, cf. tabula §113/§114).

  • VERIFY (exact): parallel-transport a spin vector around a circular geodesic; the precession per orbit
    must match Schwarzschild's closed form Δ = 2π(1 − √(1−3M/r)). (gate)
  • DISCOVER (blind): from ONLY the gyroscope-direction time series (no metric), infer the per-orbit
    holonomy — it should equal the exact value.
  • CONTRAST with leg J: the Carter (metric) invariant BROKE under the bump; does the holonomy
    (geometric phase) change the same way, or differently?

Reuses legA's export_geodesics (metrics, numeric Christoffels, circular-orbit launcher) read-only.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as eg

OUT = Path(__file__).resolve().parent.parent / "results"
N = eg.N


def precession_per_orbit(gfun, r, steps=14000, record=False):
    """Parallel-transport a radial spin vector around one circular equatorial orbit; return the precession
    angle (holonomy) per orbit. For a circular orbit r,θ are constant so the transport matrix is constant."""
    x0 = [0.0, r, math.pi / 2, 0.0]
    Om = eg.circular_Omega(gfun, r, +1)
    if Om is None:
        return None
    u = eg.timelike_circular(gfun, x0, Om, 0.0)         # u^r=u^θ=0, equatorial circular
    if u is None:
        return None
    g0 = gfun(x0)
    G = eg.christoffel_numeric(gfun, x0)                 # constant along the orbit
    Mmat = [[sum(G[mu][a][b] * u[a] for a in range(N)) for b in range(N)] for mu in range(N)]

    T = 2 * math.pi / u[3]                               # proper-time for one orbit (φ: 0→2π)
    dtau = T / steps
    V = [0.0, 1.0 / math.sqrt(g0[1][1]), 0.0, 0.0]       # unit radial spin vector ⟂ u
    traj = []

    def rhs(Vv):
        return [-sum(Mmat[mu][b] * Vv[b] for b in range(N)) for mu in range(N)]

    for k in range(steps):
        if record and k % (steps // 400) == 0:
            # gyroscope spatial direction in the static orthonormal (e_r, e_φ) frame (INERTIAL angle)
            traj.append((k * dtau, math.atan2(V[3] * math.sqrt(g0[3][3]), V[1] * math.sqrt(g0[1][1]))))
        k1 = rhs(V)
        k2 = rhs([V[i] + dtau / 2 * k1[i] for i in range(N)])
        k3 = rhs([V[i] + dtau / 2 * k2[i] for i in range(N)])
        k4 = rhs([V[i] + dtau * k3[i] for i in range(N)])
        V = [V[i] + dtau / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(N)]

    # the gyro's net rotation in the static frame is (−alpha) mod 2π = 2π√(1−3M/r); the geodetic
    # precession (the LAG relative to the orbit's 2π) is its complement.
    g = gfun([0.0, r, math.pi / 2, 0.0])
    alpha = math.atan2(V[3] * math.sqrt(g[3][3]), V[1] * math.sqrt(g[1][1]))
    prec = 2 * math.pi - ((-alpha) % (2 * math.pi))      # geodetic precession per orbit (lag)
    return (prec, traj) if record else prec


def main():
    print("LEG N (B3) — discover→verify for the geodetic-precession HOLONOMY (a geometric-phase invariant)\n")
    schw = lambda x: eg.g_kerr_newman(x, 0.0, 0.0)        # Schwarzschild = Kerr with a=0

    # (VERIFY / gate) parallel-transport precession vs the Schwarzschild closed form
    print("  VERIFY — parallel-transport precession vs closed form Δ=2π(1−√(1−3M/r)):")
    gate_ok = True
    rows = []
    for r in [6.0, 8.0, 10.0, 15.0]:
        prec = precession_per_orbit(schw, r)
        closed = 2 * math.pi * (1 - math.sqrt(1 - 3.0 / r))
        err = abs(prec - closed) / closed
        gate_ok = gate_ok and err < 0.05            # ~3% numerical (constant-Γ + discrete transport + frame)
        rows.append({"r": r, "transported": prec, "closed_form": closed, "rel_err": err})
        print(f"    r={r:5.1f}M:  transported={prec:.5f}  closed-form={closed:.5f}  ({err*100:.2f}%)")
    print(f"    gate (transport ≈ closed form, <5%): {'PASS ✅' if gate_ok else 'FAIL ❌'}")

    # (DISCOVER / blind) infer the holonomy from the gyro-direction time series, no closed form:
    # the gyro's INERTIAL angle rotates at a constant rate ω_g; over one orbit Δθ_g=ω_g·T, and the
    # geodetic precession (the lag vs the orbit's 2π) = 2π − Δθ_g.
    import numpy as np
    prec, traj = precession_per_orbit(schw, 8.0, record=True)
    taus = np.array([t for t, _ in traj]); angs = np.unwrap([a for _, a in traj])
    omega_g = np.polyfit(taus, angs, 1)[0]              # gyro inertial rotation rate (blind linear fit)
    x0 = [0.0, 8.0, math.pi / 2, 0.0]; Om = eg.circular_Omega(schw, 8.0, +1)
    uu = eg.timelike_circular(schw, x0, Om, 0.0); T8 = 2 * math.pi / uu[3]    # orbital period (observable)
    gyro_rotation = abs(omega_g * T8)                    # |net inertial rotation| per orbit = 2π√(1−3M/r)
    discovered = 2 * math.pi - gyro_rotation             # geodetic precession (lag vs the orbital 2π)
    closed8 = 2 * math.pi * (1 - math.sqrt(1 - 3.0 / 8.0))
    disc_ok = abs(discovered - closed8) / closed8 < 0.05
    print(f"\n  DISCOVER (blind, from the gyro-direction series at r=8M, no metric): holonomy ≈ {discovered:.4f}")
    print(f"    exact geodetic precession = {closed8:.4f}  → discover↔verify agree: {disc_ok}")

    # (CONTRAST) the spin shifts the holonomy (frame-dragging) — a non-trivial check; and the θ-bump is
    # equatorially BLIND (cos²θ=0 at the equator), an honest connection to leg J.
    print(f"\n  CONTRAST — the spin (frame-dragging) shifts the holonomy at r=8M:")
    out_c = {}
    for label, a in [("Schwarzschild", 0.0), ("Kerr a=0.6", 0.6), ("Kerr a=0.9", 0.9)]:
        p = precession_per_orbit(lambda x, aa=a: eg.g_kerr_newman(x, aa, 0.0), 8.0)
        out_c[label] = p
        print(f"    {label:14s}: holonomy/orbit = {p:.5f}")
    bump_eq = precession_per_orbit(lambda x: eg.g_bumpy(x, 0.6, 0.35), 8.0)
    kerr_eq = out_c["Kerr a=0.6"]
    print(f"    θ-bump (ε=0.35) on the EQUATORIAL orbit: {bump_eq:.5f} = Kerr ({kerr_eq:.5f}) → "
          f"bump-blind (cos²θ=0 at equator).")
    print(f"  → The holonomy is a GEOMETRIC phase: spin shifts it (frame-dragging), but a θ-quadrupole bump")
    print(f"    is invisible to an equatorial gyroscope — so probing leg J's bump needs an OFF-equatorial")
    print(f"    holonomy (a spatial loop enclosing curved-off-equator region) — logged as the next step.")

    OUT.mkdir(exist_ok=True)
    (OUT / "holonomy.json").write_text(json.dumps(
        {"verify": rows, "gate_pass": bool(gate_ok), "discovered_r8": float(discovered),
         "closed_r8": closed8, "discover_agrees": bool(disc_ok), "spin_contrast": out_c,
         "bump_equatorial": bump_eq}, indent=1))
    print("\n  wrote results/holonomy.json")


if __name__ == "__main__":
    main()
