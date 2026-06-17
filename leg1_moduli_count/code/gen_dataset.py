#!/usr/bin/env python3
"""Leg-1 ANSATZ side — generate observation datasets for the static charged family.

Run with the ansatz (conjecture_machine) venv, which has SymPy:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python gen_dataset.py

This script is BRIDGE code (lives in TheBridge). It imports ansatz's EXACT observable
functions READ-ONLY — `photon_sphere_shadow`, `isco` from `45_observables.py` — and
SymPy's `R_SYM` from the ansatz `gr_engine`. It does not modify the ansatz repo.

For each family (Schwarzschild / Reissner-Nordstrom / dyonic-RN) it:
  1. derives the EXACT closed-form observables once (symbolic, via ansatz), then
     lambdifies them to fast numpy callables;
  2. samples objects per the frozen protocol (PREREGISTRATION.md §3.1);
  3. writes ONLY the observation arrays (+ params, for our bookkeeping) to .npz.

The observation set is the closed-form subset of the frozen probe set:
  - strong-field radii:   r_ph, b_c (shadow), r_isco
  - gravitational redshift z(r) = 1/sqrt(f(r)) - 1 at fixed probe radii.
Light-bending (ansatz `49`) is a numeric integral and adds NO new intrinsic
dimension (it is one more function of the same params), so it is omitted from the
counting vector for speed; this is noted in PREREGISTRATION and JOURNAL.

Two conventions per family (PREREGISTRATION §2):
  - DIMENSIONFUL: observables in raw units (carry the mass scale M); redshift probed
    at fixed ABSOLUTE radii.  -> count should equal N_dim.
  - SHAPE:        observables divided by M (dimensionless); redshift probed at fixed
    MULTIPLES of M.                                       -> count should equal N_shape.
"""

import os
import sys
from pathlib import Path

import numpy as np
import sympy as sp

# --- import ansatz EXACT observables, read-only -----------------------------------
ANSATZ_SCRIPTS = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ_SCRIPTS)
from gr_engine import R_SYM  # noqa: E402  (ansatz's radial symbol)
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "obs45", os.path.join(ANSATZ_SCRIPTS, "45_observables.py")
)
obs45 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(obs45)
photon_sphere_shadow = obs45.photon_sphere_shadow  # exact r_ph, b_c
isco = obs45.isco                                   # exact ISCO radii

RESULTS = Path(__file__).resolve().parent.parent / "results"
RESULTS.mkdir(exist_ok=True)

r = R_SYM
M, Q, P = sp.symbols("M Q P", positive=True)

# Probe radii for the redshift observable. ABSOLUTE radii for the dimensionful
# convention; MULTIPLES of M for the shape convention. Chosen outside the horizon
# for the sampled parameter ranges. Frozen here.
# ABSOLUTE radii must sit OUTSIDE the horizon for every sampled M (M up to 3 ->
# Schwarzschild horizon r_h = 2M up to 6), else f<0 and the redshift is NaN.
ABS_RADII = (8.0, 10.0, 14.0, 20.0, 30.0)  # used as r = value      (dimensionful)
MULT_RADII = (3.0, 4.0, 6.0, 10.0, 20.0)   # used as r = value * M  (shape; r_h<=2M)

N_OBJECTS = 6000
N_TEST = 2000


def lapse(family):
    """The static lapse f(r) for each family (the metric stays internal to ansatz;
    we only ever export the OBSERVABLES derived from it)."""
    if family == "schwarzschild":
        return 1 - 2 * M / r
    if family == "rn":
        return 1 - 2 * M / r + Q ** 2 / r ** 2
    if family == "dyonic":
        return 1 - 2 * M / r + (Q ** 2 + P ** 2) / r ** 2
    raise ValueError(family)


S = sp.Symbol("s", nonnegative=True)   # s = Q^2 + P^2 -- charge enters the lapse ONLY here


def lapse_Ms():
    """Charged static lapse rewritten in (M, s): f = 1 - 2M/r + s/r^2. This single
    expression covers all three families (s=0 Schwarzschild; s=Q^2 RN; s=Q^2+P^2
    dyonic). The (Q,P)->s collapse IS the predicted observational degeneracy."""
    return 1 - 2 * M / r + S / r ** 2


def smooth_observables_Ms():
    """EXACT r_ph and b_c in (M, s), taken from ansatz's photon_sphere_shadow on the
    charged lapse (read-only). These are clean (quadratic) closed forms. Returns
    (r_ph_expr, b_c_expr)."""
    f = lapse_Ms()
    ps = photon_sphere_shadow(f)                    # ansatz EXACT: [(r_ph, b_c), ...]
    # outer photon sphere = larger real root; order by numeric probe at M=1, s=0.18
    def probe(e):
        try:
            v = complex(e.subs({M: 1, S: sp.Rational(9, 50)}).evalf())
        except (TypeError, ValueError):
            return -1e9
        return v.real if abs(v.imag) < 1e-9 else -1e9
    rph = max((rp for rp, _ in ps), key=probe)
    bc = [b for rp, b in ps if sp.simplify(rp - rph) == 0][0]
    return sp.simplify(rph), sp.simplify(bc)


def isco_poly_coeffs_Ms():
    """ANSATZ's exact ISCO condition (45_observables.isco): the marginally-stable
    circular orbit solves  3 f f' - 2 r f'^2 + r f f'' = 0. We take its numerator as
    a polynomial in r with coefficients in (M, s) and root it NUMERICALLY per object
    (robust; the symbolic cubic root is the unstable casus-irreducibilis branch).
    Returns list of callables [c_k(M, s)] (highest degree first)."""
    f = lapse_Ms()
    fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
    cond = sp.numer(sp.together(sp.simplify(3 * f * fp - 2 * r * fp ** 2 + r * f * fpp)))
    poly = sp.Poly(sp.expand(cond), r)
    coeffs = poly.all_coeffs()                      # highest degree first
    return [sp.lambdify((M, S), c, modules="numpy") for c in coeffs]


def _isco_numeric(coeff_funcs, Mv, sv, r_ph_v):
    """Largest real positive ISCO root strictly outside the photon sphere, per object."""
    cols = np.stack([np.broadcast_to(fn(Mv, sv), Mv.shape).astype(float)
                     for fn in coeff_funcs], axis=1)   # (n, deg+1)
    out = np.empty(Mv.shape[0])
    for i in range(Mv.shape[0]):
        roots = np.roots(cols[i])
        real = roots[np.abs(roots.imag) < 1e-7].real
        cand = real[real > r_ph_v[i] + 1e-6]
        out[i] = cand.max() if cand.size else np.nan
    return out


def build_compute(convention):
    """Return (compute, names). compute(Mv, sv) -> (n, m) observation matrix for the
    charged family in (M, s). Same instrument for all three families (they differ
    only in how s is sampled). s = Q^2 + P^2."""
    rph_e, bc_e = smooth_observables_Ms()
    f_s = lapse_Ms()
    isco_coeffs = isco_poly_coeffs_Ms()

    names, smooth_exprs = [], []
    if convention == "dimensionful":
        smooth_exprs += [rph_e, bc_e]
        names += ["r_ph", "b_c"]
        names.append("r_isco")                      # filled numerically below
        for rr in ABS_RADII:                        # redshift at fixed ABSOLUTE radii
            smooth_exprs.append(1 / sp.sqrt(f_s.subs(r, rr)) - 1)
            names.append(f"z_abs_{rr}")
        scale = sp.Integer(1)
    elif convention == "shape":
        smooth_exprs += [rph_e / M, bc_e / M]       # ratios: the scale M divides out
        names += ["r_ph/M", "b_c/M"]
        names.append("r_isco/M")
        for c in MULT_RADII:                        # redshift at fixed MULTIPLES of M
            smooth_exprs.append(1 / sp.sqrt(f_s.subs(r, c * M)) - 1)
            names.append(f"z_mult_{c}")
        scale = M
    else:
        raise ValueError(convention)

    smooth_fn = sp.lambdify((M, S), smooth_exprs, modules="numpy")
    rph_fn = sp.lambdify((M, S), rph_e, modules="numpy")
    scale_fn = sp.lambdify((M, S), scale, modules="numpy")

    def compute(Mv, sv):
        n = Mv.shape[0]
        smooth = [np.broadcast_to(np.asarray(c, dtype=float), (n,)).copy()
                  for c in smooth_fn(Mv, sv)]            # list of (n,), constants broadcast
        r_ph_v = np.broadcast_to(np.asarray(rph_fn(Mv, sv), dtype=float), (n,))
        risco = _isco_numeric(isco_coeffs, Mv, sv, r_ph_v)
        sc = np.broadcast_to(np.asarray(scale_fn(Mv, sv), dtype=float), (n,))
        risco_col = risco / sc                           # raw (dimensionful) or /M (shape)
        # column order matches `names`: [r_ph(/M), b_c(/M), r_isco(/M), z...]
        cols = [smooth[0], smooth[1], risco_col] + smooth[2:]
        return np.stack(cols, axis=1)

    return compute, names


def sample_params(family, n, rng):
    """Frozen protocol (PREREGISTRATION §3.1). Returns (theta dict, M_arr, s_arr).
    theta is our bookkeeping only -- it is NEVER written into the observation X fed
    to the net (it goes in a separate array the harness ignores)."""
    Mv = rng.uniform(1.0, 3.0, n)
    if family == "schwarzschild":
        sv = np.zeros(n)
        theta = {"M": Mv}
    elif family == "rn":
        q = rng.uniform(0.0, 0.9, n)                # q = Q/M
        Qv = q * Mv
        sv = Qv ** 2
        theta = {"M": Mv, "Q": Qv}
    elif family == "dyonic":
        # (Q^2+P^2)/M^2 ~ U[0,0.81], angle atan2(P,Q) ~ U[0,2pi]  -> P fully sampled,
        # yet observables depend only on s = Q^2+P^2 (predicted degeneracy).
        smag = rng.uniform(0.0, 0.81, n) * Mv ** 2  # = Q^2 + P^2
        ang = rng.uniform(0.0, 2 * np.pi, n)
        Qv = np.sqrt(smag) * np.cos(ang)
        Pv = np.sqrt(smag) * np.sin(ang)
        sv = Qv ** 2 + Pv ** 2
        theta = {"M": Mv, "Q": Qv, "P": Pv}
    else:
        raise ValueError(family)
    return theta, Mv, sv


def main():
    rng = np.random.default_rng(20260617)
    families = ["schwarzschild", "rn", "dyonic"]
    conventions = ["dimensionful", "shape"]
    for conv in conventions:
        compute, names = build_compute(conv)        # one instrument; families differ only in s
        for family in families:
            theta, Mv, sv = sample_params(family, N_OBJECTS + N_TEST, rng)
            X = compute(Mv, sv)                      # (n, m)
            assert X.shape == (N_OBJECTS + N_TEST, len(names)), X.shape
            assert np.isfinite(X).all(), f"non-finite obs in {family}/{conv}"
            out = RESULTS / f"obs_{family}_{conv}.npz"
            np.savez(
                out,
                X=X.astype(np.float64),
                feature_names=np.array(names),
                # bookkeeping only -- NOT an input to the counting harness:
                theta_M=theta["M"],
                n_train=np.array(N_OBJECTS),
            )
            print(f"{family:13s} {conv:13s} -> X{X.shape}  features={names}")
    print(f"\nwrote datasets to {RESULTS}")


if __name__ == "__main__":
    main()
