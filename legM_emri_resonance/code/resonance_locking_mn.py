#!/usr/bin/env python3
"""Leg M step 5 — resonance LOCKING in Manko–Novikov under the SELF-CONSISTENT flux direction (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python resonance_locking_mn.py --scan   # part A
    /Users/sumit/Github/conjecture_machine/.venv/bin/python resonance_locking_mn.py --drift  # part B

ansatz §107/§108 exhibited the devil's staircase + the dynamic plateau on ZV δ=2 — the time-domain LISA
signature (a trapped orbit's rotation number stays LOCKED at the rational while the orbit drifts). Two
things they left open that the bridge owns: (i) the metric of record for B1 is **Manko–Novikov** (rotating,
our validated flux lives there); (ii) §108's drift was a *prescribed* dLz/dτ only, "at the flux scale" —
not the actual radiation-reaction direction. This step:

  A (--scan)   MN's own staircase: ν(x0) at fixed (E=0.95, Lz=3.0), a=0.9, q=0.6, across the 2/3 resonance
               (x0∈[7.55,7.87]) — the finite-width LOCKED plateau non-integrability predicts — vs the Kerr
               (q=0, same a, same E,L; bound region starts x0≈8.05) control, which must ride smoothly
               through 2/3 with no plateau (resonant tori are measure-zero when integrable).
  B (--drift)  the SELF-CONSISTENT co-drift: compute (dE/dτ, dLz/dτ) from ansatz's validated
               `quadrupole_flux` AT the island orbit — the true radiation-reaction direction in the (E,Lz)
               plane — and integrate the trapped orbit with E(τ), L(τ) both drifting along it (magnitude
               scaled by a DISCLOSED factor to make the sweep feasible, run at two speeds for
               rate-robustness). Locked windowed-ν while (E,Lz) sweep = sustained resonance under the
               physical drift direction; a riser-control orbit must transit without capture.

Reuses ansatz read-only: build_hamilton_numeric (§99/§102-fixed), poincare._rk4/section, §107's
section_freq estimator, §100/§101 quadrupole_flux. Reboot-resilient: per-orbit checkpoint.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric
from poincare import _rk4, section
from _plateau_v3_section import section_freq                 # §107's validated estimator, read-only

OUT = Path(__file__).resolve().parent.parent / "results"
CKPT = OUT / "locking_scan_ckpt.json"
A, Q, E0, L0 = 0.9, 0.6, 0.95, 3.0
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))
# CONVENTION (measured in the first scan pass): §107's section_freq returns the section winding ν, the
# COMPLEMENT of the epicyclic ratio — the 2/3 epicyclic resonance appears at ν = 1 − 2/3 = 1/3. The MN
# riser descends toward 1/3 from above (0.349→0.338 over x0 7.55→7.87); Kerr's riser crossed ν=1/4
# smoothly (0.25003 at a single point) — the integrable measure-zero control, already in hand.
TARGET = 1.0 / 3.0


def py_onshell(f, x0, E, L):
    val = (-1 - f["W"](x0, 0.0, E, L)) / f["g22"](x0, 0.0, E, L)
    return math.sqrt(val) if val > 0 else None


def nu_of(f, x0, E, L, n=160):
    py = py_onshell(f, x0, E, L)
    if py is None or py < 0.02:
        return None, 0
    pts, dr, _ = section(f, [x0, 0.0, 0.0, py], E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                         n=n, h=0.02, maxst=6_000_000, bounds=BOUNDS)
    if len(pts) < 100:
        return None, len(pts)
    return section_freq([p[0] for p in pts]), len(pts)


def scan():
    OUT.mkdir(exist_ok=True)
    done = json.loads(CKPT.read_text()) if CKPT.exists() else {}
    print(f"PART A — MN staircase at the 2/3 resonance (a={A}, q={Q}, E={E0}, Lz={L0}) vs Kerr control\n")
    jobs = [("mn", Q, round(7.55 + 0.02 * k, 3)) for k in range(17)] + \
           [("kerr", 0.0, round(8.06 + 0.06 * k, 3)) for k in range(16)] + \
           [("mn", Q, round(7.89 + 0.02 * k, 3)) for k in range(15)] + \
           [("mn_fine", Q, round(8.05 + 0.005 * k, 3)) for k in range(13)]  # refine the flattest zone, n=240
    for fam, q, x0 in jobs:
        key = f"{fam}:{x0}"
        if key in done:
            continue
        f = build_hamilton_numeric(1.0, A, q)
        nu, npts = nu_of(f, x0, E0, L0, n=240 if fam == "mn_fine" else 160)
        done[key] = {"family": fam, "x0": x0, "nu": nu, "n": npts}
        CKPT.write_text(json.dumps(done))
        print(f"  {fam:>4} x0={x0:.3f}: nu = {nu if nu is None else round(nu, 5)}  ({npts} crossings)", flush=True)

    mn = sorted((v for v in done.values() if v["family"] == "mn" and v["nu"]), key=lambda r: r["x0"])
    kerr = sorted((v for v in done.values() if v["family"] == "kerr" and v["nu"]), key=lambda r: r["x0"])
    LOCK_TOL = 5e-4
    plat = [r for r in mn if abs(r["nu"] - TARGET) < LOCK_TOL]
    print(f"\n  MN: {len(plat)} of {len(mn)} scan points locked at 2/3 ± {LOCK_TOL} "
          f"({'plateau width Δx0 ≈ %.3f' % (plat[-1]['x0'] - plat[0]['x0']) if len(plat) > 1 else 'no multi-point plateau'})")
    kerr_lock = [r for r in kerr if abs(r["nu"] - 0.25) < LOCK_TOL]      # Kerr's rational in range is 1/4
    mono = all(kerr[i + 1]["nu"] < kerr[i]["nu"] for i in range(len(kerr) - 1)) if len(kerr) > 2 else None
    print(f"  Kerr control (its in-range rational is 1/4): {len(kerr_lock)} point(s) within ±{LOCK_TOL} of 1/4 "
          f"(expect ≤1 — measure-zero smooth crossing); monotone descending riser = {mono}")
    (OUT / "locking_scan.json").write_text(json.dumps(
        {"a": A, "q": Q, "E": E0, "L": L0, "mn": mn, "kerr": kerr,
         "mn_plateau_points": len(plat), "kerr_locked_points": len(kerr_lock)}, indent=1))
    print(f"  wrote results/locking_scan.json")


def drift(q, x0, dE, dL, speed, n_cross=420, W=60, stride=10, h=0.02, maxst=14_000_000):
    """Windowed ν(τ) under the self-consistent co-drift E(τ)=E0+s·Ė·τ, L(τ)=L0+s·L̇·τ."""
    f = build_hamilton_numeric(1.0, A, q)
    py = py_onshell(f, x0, E0, L0)
    s = [x0, 0.0, 0.0, py]
    xs, nus, taus = [], [], []
    prev, st, tau = s[1], 0, 0.0
    while len(xs) < n_cross and st < maxst:
        if not (BOUNDS[0][0] <= s[0] <= BOUNDS[0][1] and BOUNDS[1][0] <= s[1] <= BOUNDS[1][1]):
            break
        Et, Lt = E0 + speed * dE * tau, L0 + speed * dL * tau
        try:
            sn = _rk4(f, s, h, Et, Lt)
        except (OverflowError, ZeroDivisionError, ValueError):
            break
        st += 1
        tau += h
        if prev < 0 <= sn[1]:
            xs.append(sn[0])
            if len(xs) >= W and len(xs) % stride == 0:
                nus.append(section_freq(xs[-W:]))
                taus.append(tau)
        prev = sn[1]
        s = sn
    return nus, taus, tau


def dwell_stats(nus, r, band=8e-4):
    """Observed windows within ±band of the rational r, vs the no-anomaly expectation
    (uniform sweep: expected fraction = 2·band / total ν swept). Ratio > 1 ⇒ anomalous dwell."""
    if len(nus) < 4:
        return None
    inband = sum(1 for n in nus if abs(n - r) < band)
    swept = abs(nus[-1] - nus[0])
    if swept <= 0:
        return None
    expected = len(nus) * min(1.0, 2 * band / swept)
    return {"in_band": inband, "expected_uniform": expected,
            "dwell_ratio": inband / expected if expected > 0 else None,
            "nu_start": nus[0], "nu_end": nus[-1], "swept": swept}


def drift_mode():
    """PART B (transit-dwell version). The refine showed NO resolvable 2/3 island at this slice (any island
    is narrower than Δx0=0.005; ν never pins at 1/3 exactly) — so a §108-style trapped-orbit demo is not
    available here, honestly. The measurable time-domain question instead: driving the orbit THROUGH the
    resonance along the self-consistent flux direction, does the crossing dwell anomalously near ν=1/3 (the
    time-domain counterpart of the ~10× slope collapse)? Kerr driven through ITS rational (1/4) at its own
    flux is the no-structure control."""
    OUT.mkdir(exist_ok=True)
    from emri import quadrupole_flux                          # ansatz §100/§101, read-only
    print(f"PART B — resonance-crossing TRANSIT under the self-consistent flux direction (a={A})\n")
    out = {"a": A, "E0": E0, "L0": L0, "design": "transit dwell (no resolvable island at this slice)",
           "runs": {}}
    plans = [("mn", Q, 8.15, TARGET, "MN q=0.6 through nu=1/3"),
             ("kerr", 0.0, 8.78, 0.25, "Kerr q=0 through nu=1/4 (control)")]
    for tag, q, x_start, rat, desc in plans:
        fl = quadrupole_flux(1.0, A, q, E0, L0, x_start, n_orb=6)
        dE, dL = fl
        # physical flux is per (mu/M)²; scale so the sweep crosses the rational within the run — disclosed.
        speed = 2.5e-3 / (abs(dL) * 2.0e4)
        nus, taus, tauend = drift(q, x_start, dE, dL, speed)
        ds = dwell_stats(nus, rat)
        out["runs"][tag] = {"desc": desc, "x_start": x_start, "rational": rat,
                            "flux": {"dEdt": dE, "dLdt": dL}, "speed": speed,
                            "n_windows": len(nus), "nus": nus, "taus": taus, "dwell": ds}
        print(f"  {tag}: flux (dE,dL)=({dE:.2e},{dL:.2e}), speed={speed:.2e}, {len(nus)} windows, "
              f"ν {nus[0]:.5f} → {nus[-1]:.5f}" if nus else f"  {tag}: no windows (orbit lost)", flush=True)
        if ds:
            print(f"        dwell near {rat:.4f}: {ds['in_band']} windows vs {ds['expected_uniform']:.1f} "
                  f"expected-uniform → ratio {ds['dwell_ratio']:.2f}", flush=True)
    mn_d = out["runs"].get("mn", {}).get("dwell") or {}
    k_d = out["runs"].get("kerr", {}).get("dwell") or {}
    if mn_d.get("dwell_ratio") and k_d.get("dwell_ratio"):
        rel = mn_d["dwell_ratio"] / k_d["dwell_ratio"]
        out["mn_over_kerr_dwell"] = rel
        print(f"\n  VERDICT: MN dwell ratio {mn_d['dwell_ratio']:.2f} vs Kerr control {k_d['dwell_ratio']:.2f} "
              f"→ relative {rel:.2f}× {'(anomalous resonant dwell)' if rel > 2 else '(smooth transit both — no capture at this q, matching the no-island refine)'}")
    (OUT / "locking_drift.json").write_text(json.dumps(out, indent=1))
    print(f"  wrote results/locking_drift.json")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--scan"
    (scan if mode == "--scan" else drift_mode)()
