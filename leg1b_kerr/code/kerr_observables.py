#!/usr/bin/env python3
"""Leg-1b ANSATZ side — exact equatorial Kerr / Kerr-Newman observables.

Run with a venv that has sympy + numpy + scipy (curvature venv works):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python kerr_observables.py

BRIDGE code. Imports ansatz's EXACT rotating metric builder READ-ONLY
(`44_discover_rotating.kerr_delta_metric`) and ansatz's radial symbol; derives equatorial
(u=cosθ=0) geodesic observables from the EXACT metric components via standard
stationary-axisymmetric conditions. ansatz stays the metric oracle; no hand-coded Bardeen
formulas, no edits to the ansatz repo.

Observables (all from g_tt(r), g_tφ(r), g_φφ(r) and their r-derivatives):
  horizon r±, circular Ω±(r), photon orbits r_ph^{±}, ISCO r_isco^{±},
  frame-dragging ω(r)=−g_tφ/g_φφ, redshift z(r)=1/√(−g_tt)−1.
Sanity-gated: at a=Q=0 must give r_ph=3M, r_isco=6M, ω=0.

Families written (obs_<family>_<conv>.npz, key X) for the leg-1 counting harness:
  kerr     (M,a)     full obs           -> expect intrinsic dim 2 (dimensionful) / 1 (shape)
  kn_full  (M,a,Q)   full obs           -> expect 3 / 2  (no degeneracy)
  kn_deg   (M,a,Q)   Δ-symmetric obs    -> expect 2 / 1  (sees only a²+Q²)
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from gr_engine import R_SYM  # noqa: E402

_spec = importlib.util.spec_from_file_location("rot", os.path.join(ANSATZ, "44_discover_rotating.py"))
rot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rot)                    # ansatz rotating metric, READ-ONLY

RESULTS = Path(__file__).resolve().parent.parent / "results"
RESULTS.mkdir(exist_ok=True)

r = R_SYM
M = sp.Symbol("M", positive=True)
a = sp.Symbol("a", positive=True)                # SAME symbol kerr_delta_metric creates
Q = sp.Symbol("Q", nonnegative=True)

ABS_RADII = (8.0, 10.0, 14.0, 20.0)              # outside horizon for all sampled objects
MULT_RADII = (3.0, 4.0, 6.0, 10.0)              # multiples of M (r+ ≤ 2M)
N_OBJECTS, N_TEST = 6000, 2000


def equatorial_components():
    """Exact equatorial g_tt, g_tφ, g_φφ as fast callables of (r, M, a, Q), plus their
    r-derivatives. Metric from ansatz's kerr_delta_metric with Kerr-Newman Δ."""
    Delta = r**2 - 2*M*r + a**2 + Q**2
    g, coords, a2 = rot.kerr_delta_metric(Delta)     # exact KN metric (a2 is the same `a`)
    u = coords[2]
    g = g.subs(u, 0)                                  # equatorial plane
    gtt, gtp, gpp = sp.simplify(g[0, 0]), sp.simplify(g[0, 3]), sp.simplify(g[3, 3])
    syms = (r, M, a, Q)
    out = {}
    for name, e in (("tt", gtt), ("tp", gtp), ("pp", gpp)):
        out[name] = sp.lambdify(syms, e, "numpy")
        out[name + "_r"] = sp.lambdify(syms, sp.diff(e, r), "numpy")
    return out


C = equatorial_components()


def _orbit_funcs(Mv, av, Qv):
    """Return python callables gtt,gtp,gpp,Om±,D±,E± of r for one object."""
    gtt = lambda x: C["tt"](x, Mv, av, Qv)
    gtp = lambda x: C["tp"](x, Mv, av, Qv)
    gpp = lambda x: C["pp"](x, Mv, av, Qv)
    gtt_r = lambda x: C["tt_r"](x, Mv, av, Qv)
    gtp_r = lambda x: C["tp_r"](x, Mv, av, Qv)
    gpp_r = lambda x: C["pp_r"](x, Mv, av, Qv)

    def Om(x, sign):
        disc = gtp_r(x)**2 - gtt_r(x) * gpp_r(x)
        if disc < 0:
            return np.nan
        return (-gtp_r(x) + sign * np.sqrt(disc)) / gpp_r(x)

    def D(x, sign):                                    # −(gtt+2Ω gtφ+Ω² gφφ); >0 timelike
        o = Om(x, sign)
        return -(gtt(x) + 2*o*gtp(x) + o**2*gpp(x))

    def E(x, sign):
        d = D(x, sign); o = Om(x, sign)
        if not (d > 0):
            return np.nan
        return -(gtt(x) + o*gtp(x)) / np.sqrt(d)

    return gtt, gtp, gpp, Om, D, E


def _root_scan(fn, lo, hi, n=600):
    """Smallest sign-change root of fn on [lo,hi] via grid scan + brentq."""
    xs = np.linspace(lo, hi, n)
    vals = np.array([fn(x) for x in xs])
    for i in range(n - 1):
        a0, b0 = vals[i], vals[i+1]
        if np.isfinite(a0) and np.isfinite(b0) and a0 * b0 < 0:
            try:
                return brentq(fn, xs[i], xs[i+1], maxiter=200)
            except Exception:
                continue
    return np.nan


def observables(Mv, av, Qv, radii):
    """Full equatorial observable dict for one object, probing g_tt/ω/Δ at the given
    `radii` (absolute for dimensionful; c·M for shape). Index probes 0..len-1 so feature
    names are convention-independent."""
    rh = Mv + np.sqrt(max(Mv**2 - av**2 - Qv**2, 0.0))      # outer horizon
    rin = Mv - np.sqrt(max(Mv**2 - av**2 - Qv**2, 0.0))     # inner horizon
    gtt, gtp, gpp, Om, D, E = _orbit_funcs(Mv, av, Qv)
    out = {"r_horizon": rh, "r_inner": rin}
    for sign, tag in ((+1, "pro"), (-1, "retro")):
        rph = _root_scan(lambda x: D(x, sign), rh + 1e-3, 30.0)
        # ISCO: minimum of E(r) for r>r_ph -> root of dE/dr
        def dE(x):
            h = 1e-4
            ep, em = E(x + h, sign), E(x - h, sign)
            return (ep - em) / (2 * h)
        risco = _root_scan(dE, (rph if np.isfinite(rph) else rh) + 1e-2, 30.0)
        out[f"r_ph_{tag}"] = rph
        out[f"r_isco_{tag}"] = risco
    for k, rr in enumerate(radii):
        out[f"omega_{k}"] = -gtp(rr) / gpp(rr)              # frame-dragging
        out[f"z_{k}"] = 1.0/np.sqrt(max(-gtt(rr), 1e-12)) - 1.0
        out[f"Delta_{k}"] = (rr**2 - 2*Mv*rr + av**2 + Qv**2) / rr**2
    return out


def sanity():
    o = observables(1.0, 0.0, 0.0, ABS_RADII)
    ok = (abs(o["r_ph_pro"] - 3) < 1e-3 and abs(o["r_isco_pro"] - 6) < 1e-3
          and abs(o["omega_0"]) < 1e-9)
    print(f"SANITY a=Q=0: r_ph={o['r_ph_pro']:.4f} (3), r_isco={o['r_isco_pro']:.4f} (6), "
          f"omega={o['omega_0']:.2e}  {'OK' if ok else 'FAIL'}")
    return ok


def sample(family, n, rng):
    Mv = rng.uniform(1.0, 3.0, n)
    if family == "kerr":
        chi = rng.uniform(0.0, 0.9, n); av = chi*Mv; Qv = np.zeros(n)
    else:  # kn_full / kn_deg: sub-extremal chi²+q² < 0.81
        rad = np.sqrt(rng.uniform(0.0, 0.81, n)); ang = rng.uniform(0, np.pi/2, n)
        av = rad*np.cos(ang)*Mv; Qv = rad*np.sin(ang)*Mv
    return Mv, av, Qv


def feature_vector(family, conv, o, Mv, nrad):
    """Assemble the observation vector per family/convention. For shape, radii are divided
    by M and frame-dragging multiplied by M (z, Δ already dimensionless and, in shape, are
    probed at multiples of M so they depend only on χ,q)."""
    if family == "kn_deg":
        base = [o["r_horizon"], o["r_inner"]] + [o[f"Delta_{k}"] for k in range(nrad)]
        names = ["r_horizon", "r_inner"] + [f"Delta_{k}" for k in range(nrad)]
    else:  # kerr, kn_full -> full set
        base = [o["r_horizon"], o["r_ph_pro"], o["r_ph_retro"],
                o["r_isco_pro"], o["r_isco_retro"]]
        names = ["r_horizon", "r_ph_pro", "r_ph_retro", "r_isco_pro", "r_isco_retro"]
        for k in range(nrad):
            base += [o[f"omega_{k}"], o[f"z_{k}"]]
            names += [f"omega_{k}", f"z_{k}"]
    out = []
    for nm, v in zip(names, base):
        if conv == "shape" and nm.startswith("r_"):
            out.append(v / Mv)                       # radii in units of M
        elif conv == "shape" and nm.startswith("omega"):
            out.append(v * Mv)                       # dimensionless frame-drag
        else:
            out.append(v)
    return np.array(out, dtype=float), names


def build(family, conv, rng):
    n = N_OBJECTS + N_TEST
    Mv, av, Qv = sample(family, n, rng)
    rows = []
    for i in range(n):
        radii = ABS_RADII if conv == "dimensionful" else tuple(c * Mv[i] for c in MULT_RADII)
        o = observables(Mv[i], av[i], Qv[i], radii)
        v, names = feature_vector(family, conv, o, Mv[i], len(radii))
        rows.append(v)
    X = np.array(rows)
    ok = np.isfinite(X).all(axis=1)
    return X[ok], names, int(ok.sum())


def main():
    if not sanity():
        raise SystemExit("sanity gate failed")
    rng = np.random.default_rng(20260617)
    for conv in ("dimensionful", "shape"):
        for fam in ("kerr", "kn_full", "kn_deg"):
            X, names, nkept = build(fam, conv, rng)
            np.savez(RESULTS / f"obs_{fam}_{conv}.npz", X=X.astype(np.float64),
                     feature_names=np.array(names), n_train=np.array(min(N_OBJECTS, nkept-500)))
            print(f"{fam:9s} {conv:13s} X{X.shape} kept={nkept}  feats={names}")
    print(f"\nwrote -> {RESULTS}")


if __name__ == "__main__":
    main()
