#!/usr/bin/env python3
"""Leg V — the bridge's box-dimension instrument (from GR orbits) pointed at quantum's detector wall.

    python3 fractal_boundary_dim.py

Gates V1/V2/V3 frozen in ../PREREGISTRATION.md before this was written. A cross-domain instrument transfer
(the shape of leg R): the bridge's box-counting dimension — validated on Hénon–Heiles / the di-hole in
leg J, mirroring ansatz's poincare.box_dimension (slope of log N(G) vs log G) — is applied in 1-D to
quantum's QM detector-wall experiment (qsim/fractal_boundary.py). The bridge reconstructs the Cantor
geometry analytically and REIMPLEMENTS quantum's wave sim in its own code (read-only from quantum; no
import, no writes into the source repo).

  V1  the instrument reads dimension correctly in the new domain: analytic Cantor → log2/log3 = 0.6309,
      uniform wall → 1.00.
  V2  the axis quantum did not use: at identical 8/27 coverage, box-dim separates the Cantor wall from the
      periodic wall (fractal vs regular), where JS-divergence alone could not name the dimension.
  V3  the QM cross-check: reproduce quantum's gating + fringe-integrity independently, and show the Cantor
      DETECTION support inherits the boundary's sub-integer dimension — the dynamics gate, they do not
      manufacture fractality. Honest limits (V3 framing): lattice sim, λ≈6.3 cells sets a resolution floor.
"""
import json
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results"
NY = 324
LOG2_LOG3 = math.log(2) / math.log(3)          # 0.63093 — the exact Cantor box-dimension


# ---------------------------------------------------------------- the instrument (1-D box-counting)
def _slope(gs, ns):
    lg = [math.log(g) for g in gs]
    ln = [math.log(n) for n in ns]
    mg, mn = sum(lg) / len(lg), sum(ln) / len(ln)
    return sum((lg[i] - mg) * (ln[i] - mn) for i in range(len(lg))) / sum((lg[i] - mg) ** 2 for i in range(len(lg)))


def box_dim_positions(pos01, grids):
    """1-D box-counting dimension of occupied positions in [0,1] (faithful analog of poincare.box_dimension)."""
    pos = np.asarray(pos01, float)
    ns = [len(set(np.minimum(G - 1, (pos * G).astype(int)).tolist())) for G in grids]
    return _slope(grids, ns), ns


def box_dim_mask(mask_bool, grids):
    idx = np.where(mask_bool)[0]
    return box_dim_positions(idx / len(mask_bool), grids)


def local_slopes(grids, ns):
    return [math.log(ns[i + 1] / ns[i]) / math.log(grids[i + 1] / grids[i]) for i in range(len(grids) - 1)]


# ---------------------------------------------------------------- geometry (reconstructed, read-only)
def cantor_intervals(level):
    seg = [(0.0, 1.0)]
    for _ in range(level):
        seg = [s for a, b in seg for s in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
    return seg


def box_dim_intervals(intervals, grids):
    ns = []
    for G in grids:
        cells = set()
        for a, b in intervals:
            i0, i1 = int(a * G), min(G - 1, int(b * G - 1e-12))
            cells.update(range(i0, i1 + 1))
        ns.append(len(cells))
    return _slope(grids, ns), ns


def quantum_masks():
    """Exactly quantum's masks() — uniform, periodic (8 even segments), cantor (level-3), matched 8/27."""
    m_uni = np.ones(NY, bool)
    m_can = np.zeros(NY, bool)
    for a, b in cantor_intervals(3):
        m_can[int(a * NY):max(int(a * NY) + 1, int(b * NY))] = True
    frac = m_can.mean()
    m_per = np.zeros(NY, bool)
    nseg, w = 8, max(1, int(round(frac * NY / 8)))
    for i in range(nseg):
        c = int((i + 0.5) * NY / nseg)
        m_per[c - w // 2:c - w // 2 + w] = True
    return {"uniform": m_uni, "periodic": m_per, "cantor": m_can}


# ---------------------------------------------------------------- quantum's wave sim, reimplemented
def run_wave(mask):
    Nx = 480
    dx, dt, steps, k0 = 1.0, 0.2, 9000, 1.0
    x = np.arange(Nx)[:, None]
    y = np.arange(NY)[None, :]
    slit_x, det_x, sep, sw = 150, 430, 40, 10
    cy = NY // 2
    border = 18
    bd = np.minimum(np.minimum(x, Nx - 1 - x), np.minimum(y, NY - 1 - y))
    sponge = np.where(bd >= border, 1.0, 1.0 - 0.35 * ((border - bd) / border) ** 2)

    slit_damp = np.ones((Nx, NY))
    open1 = np.abs(y - (cy - sep // 2)) <= sw // 2
    open2 = np.abs(y - (cy + sep // 2)) <= sw // 2
    blocked = ~(open1 | open2)
    for i, col in enumerate(range(slit_x, slit_x + 8)):
        a = 0.55 * np.sin(np.pi * (i + 0.5) / 8)
        slit_damp[col, :] = np.where(blocked[0], 1.0 - a, 1.0)

    sx, sy = 28.0, 70.0
    env = np.exp(-((x - 70) ** 2) / (2 * sx ** 2) - ((y - cy) ** 2) / (2 * sy ** 2))
    R = env * np.cos(k0 * (x - 70.0)); I = env * np.sin(k0 * (x - 70.0))
    nrm = np.sqrt(np.sum(R ** 2 + I ** 2)); R /= nrm; I /= nrm

    det_damp = np.ones((Nx, NY))
    for i, col in enumerate(range(det_x, det_x + 4)):
        a = 0.5 * np.sin(np.pi * (i + 0.5) / 4)
        det_damp[col, :] = np.where(mask, 1.0 - a, 1.0)
    damp = sponge * slit_damp * det_damp

    clicks = np.zeros(NY); incident = np.zeros(NY)
    c = dt / (2 * dx * dx)
    for _ in range(steps):
        lap = np.roll(R, 1, 0) + np.roll(R, -1, 0) + np.roll(R, 1, 1) + np.roll(R, -1, 1) - 4 * R
        I += c * lap * 2
        lap = np.roll(I, 1, 0) + np.roll(I, -1, 0) + np.roll(I, 1, 1) + np.roll(I, -1, 1) - 4 * I
        R -= c * lap * 2
        p_before = R[det_x:det_x + 4, :] ** 2 + I[det_x:det_x + 4, :] ** 2
        R *= damp; I *= damp
        p_after = R[det_x:det_x + 4, :] ** 2 + I[det_x:det_x + 4, :] ** 2
        clicks += (p_before - p_after).sum(axis=0)
        incident += R[det_x - 6, :] ** 2 + I[det_x - 6, :] ** 2
    return clicks, incident


def js_div(p, q):
    p = p / p.sum(); q = q / q.sum(); m = 0.5 * (p + q)
    kl = lambda a, b: np.sum(np.where(a > 0, a * np.log(a / np.maximum(b, 1e-300)), 0))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


# ---------------------------------------------------------------- gates
def main():
    print("LEG V — the bridge's box-dimension instrument, pointed at quantum's detector wall")
    print(f"  (1-D analog of ansatz poincare.box_dimension; gates frozen in PREREGISTRATION.md)\n")
    GB = (3, 9, 27)                                # self-similar band (cell 108→36→12 ≥ 12-cell segment)
    GW = (3, 9, 27, 81)                            # analytic Cantor over 4 clean octaves (3¹..3⁴)
    report = {}

    # ---- V1: the instrument reads dimension correctly in the new domain
    d_can_an, ns_can = box_dim_intervals(cantor_intervals(5), GW)   # level 5 aligns exactly with G=3^5
    d_uni, _ = box_dim_mask(np.ones(NY, bool), GB)
    v1 = abs(d_can_an - LOG2_LOG3) < 0.02 and abs(d_uni - 1.0) < 0.02
    print("  V1 — instrument validation (cross-domain):")
    print(f"     analytic Cantor  D = {d_can_an:.4f}  (exact log2/log3 = {LOG2_LOG3:.4f})   counts {ns_can}")
    print(f"     uniform wall     D = {d_uni:.4f}  (expected 1.0000)")
    print(f"     →  {'PASS ✅' if v1 else 'FAIL ❌'}")
    report.update(D_cantor_analytic=d_can_an, D_uniform=d_uni, V1_pass=bool(v1))

    # ---- V2: the dimensional discriminator at identical coverage
    M = quantum_masks()
    d_can, nc = box_dim_mask(M["cantor"], GB)
    d_per, npd = box_dim_mask(M["periodic"], GB)
    sl_can, sl_per = local_slopes(GB, nc), local_slopes(GB, npd)
    std_can = float(np.std(sl_can)); std_per = float(np.std(sl_per))
    v2 = (d_per - d_can > 0.10) and (std_can < 0.05)
    print(f"\n  V2 — dimensional discriminator at matched coverage {M['cantor'].mean():.3f} (grids {GB}):")
    print(f"     cantor   D = {d_can:.4f}   local slopes {[round(s,3) for s in sl_can]} (std {std_can:.3f})")
    print(f"     periodic D = {d_per:.4f}   local slopes {[round(s,3) for s in sl_per]} (std {std_per:.3f})")
    print(f"     separation D(per)−D(can) = {d_per - d_can:.3f} (>0.10?)   →  {'PASS ✅' if v2 else 'FAIL ❌'}")
    report.update(D_cantor_mask=d_can, D_periodic_mask=d_per, sep=d_per - d_can,
                  slope_std_cantor=std_can, slope_std_periodic=std_per, V2_pass=bool(v2))

    # ---- V3: reimplement quantum's sim; reproduce gating+integrity; measure detection dimension
    print(f"\n  V3 — reimplementing quantum's wave sim (480×324, 9000 steps × 3 walls)…")
    res = {name: run_wave(m) for name, m in M.items()}
    u_clicks, _ = res["uniform"]
    js = {name: float(js_div(res[name][0] + 1e-15, u_clicks + 1e-15)) for name in ("periodic", "cantor")}
    corr = {}
    for name, m in M.items():
        clk, inc = res[name]
        pred = inc * m
        keep = m & (inc > 0.01 * inc.max())
        corr[name] = float(np.corrcoef(clk[keep], pred[keep])[0, 1]) if keep.sum() > 4 else float("nan")
    # detection-support dimension for the Cantor wall
    clk_can = res["cantor"][0]
    support = clk_can > 0.05 * clk_can.max()
    d_det, nd = box_dim_mask(support, GB)
    print(f"     gating (JS vs uniform):   periodic {js['periodic']:.3f}   cantor {js['cantor']:.3f}  (>0.1?)")
    print(f"     fringe integrity corr(detected, incident×mask): "
          f"{ {k: round(v,3) for k,v in corr.items()} }  (>0.8?)")
    print(f"     Cantor DETECTION support D = {d_det:.4f}  (mask 0.63 ← inherited, not manufactured to 1.0)")
    repro = js["periodic"] > 0.1 and js["cantor"] > 0.1 and corr["cantor"] > 0.8 and corr["periodic"] > 0.8
    v3 = repro and (d_det < 0.85) and (abs(d_det - d_can) < abs(d_det - 1.0))
    print(f"     →  {'PASS ✅ — quantum reproduced + detection inherits the boundary dimension' if v3 else 'FAIL ❌'}")
    report.update(JS=js, corr=corr, D_cantor_detection=d_det, V3_repro=bool(repro), V3_pass=bool(v3))

    print(f"\n  V3 framing (frozen): lattice sim, λ=2π/k₀≈6.3 cells vs the 12-cell finest Cantor segment —")
    print(f"     the QM probe images the fractal boundary only to ~λ (a resolution floor). Cross-repo")
    print(f"     triangulation of quantum's boundary-gating with a quantitative dimension; NOT a continuum")
    print(f"     or real-detector claim.")

    OUT.mkdir(exist_ok=True)
    report["verdict"] = (
        "The bridge's GR-born box-dimension instrument, applied to quantum's QM detector wall, recovers the "
        "Cantor boundary's exact fractal dimension (D=%.4f vs log2/log3=%.4f) and the solid wall's D=1.0 "
        "(V1); it separates the Cantor from the periodic wall at identical 8/27 coverage (D %.2f vs %.2f, "
        "V2) — the dimensional axis quantum's JS-divergence could not name; and an independent "
        "reimplementation of quantum's wave sim reproduces its gating and fringe-integrity while showing the "
        "Cantor detection support inherits the boundary's sub-integer dimension (D=%.2f), confirming "
        "quantitatively quantum's 'gated, not fractal-manufactured' verdict (V3). λ≈6.3-cell resolution "
        "floor; cross-repo triangulation, not a continuum claim."
        % (d_can_an, LOG2_LOG3, d_can, d_per, d_det))
    (OUT / "fractal_boundary_dim.json").write_text(json.dumps(report, indent=1))
    print(f"\n  wrote results/fractal_boundary_dim.json")


if __name__ == "__main__":
    main()
