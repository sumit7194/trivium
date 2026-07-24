#!/usr/bin/env python3
"""K2 — the mass tower does NOT determine the hidden geometry (isospectral drums).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python k2_drums.py

Gates K2a/K2b/K2c frozen in ../PREREGISTRATION.md before this was written. The Gordon-Webb-Wolpert pair:
two non-congruent planar domains, each 7 congruent right-isosceles triangles glued differently, with
identical Dirichlet spectra in the CONTINUUM (Gordon-Webb-Wolpert 1992). On a correct FD grid the two
discrete spectra CONVERGE to each other as h->0. Kills "you can hear the shape of the hidden drum."

CORRECTION 2026-07-24 (bug found by tabula, confirmed by the bridge): an earlier version of this script
used the same grid offset in x and y, which dropped every point lying on an internal diagonal and thereby
disconnected each drum into the SAME 3 congruent pieces -- the two operators were one matrix relabelled,
so their "exact, resolution-independent isospectrality" was a triviality, not transplantation. Fixed by
using distinct offsets (no grid point can lie on any edge) plus a connectivity assertion.
"""
import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

OUT = Path(__file__).resolve().parent.parent / "results"

# The GWW pair: 7 unit right-isosceles triangles each (Cleve Moler's vertex form)
DRUM1 = [[(0, 0), (0, 1), (1, 0)], [(0, 1), (1, 1), (1, 0)], [(0, 1), (1, 2), (1, 1)],
         [(1, 1), (1, 2), (2, 1)], [(1, 2), (2, 2), (2, 1)], [(1, 2), (2, 3), (2, 2)],
         [(2, 2), (3, 2), (2, 1)]]
DRUM2 = [[(1, 0), (0, 1), (1, 1)], [(0, 1), (1, 2), (1, 1)], [(0, 1), (0, 2), (1, 2)],
         [(1, 1), (1, 2), (2, 1)], [(1, 2), (2, 2), (2, 1)], [(2, 1), (2, 2), (3, 2)],
         [(2, 2), (2, 3), (3, 2)]]
OUT1 = [(0, 0), (0, 1), (2, 3), (2, 2), (3, 2), (2, 1), (1, 1), (1, 0)]
OUT2 = [(1, 0), (0, 1), (0, 2), (2, 2), (2, 3), (3, 2), (2, 1), (1, 1)]
NEIG = 20
RESOLUTIONS = [16, 32, 64, 96]          # connected grids; convergence is the gate (see bug note)


def in_tri(px, py, tri):
    (ax, ay), (bx, by), (cx, cy) = tri
    d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    a = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / d
    b = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / d
    return (a > 0) & (b > 0) & (1 - a - b > 0)          # strict interior


A_OFF, B_OFF = 0.5, 0.25          # DIFFERENT offsets — see the bug note below


def interior_mask(tris, n):
    """Interior grid points, on a grid offset by (A_OFF, B_OFF)·h in x and y.

    BUG FIX (2026-07-24, found by tabula). The first version used the SAME offset ½ in both
    directions. Then grid points land exactly on the internal diagonals x±y ∈ ℤ, and since
    `in_tri` is a STRICT test such points are interior to no triangle and get dropped. Those
    dropped lines act as walls: each drum was cut into 3 disconnected pieces, and the two drums
    decomposed into the SAME pieces — so the two discrete Laplacians were one matrix relabelled
    and their "exact isospectrality" was a triviality, not transplantation.

    The fix: choose A_OFF ≠ B_OFF with A_OFF, B_OFF, A_OFF±B_OFF all non-integer. Then
    i+A ≠ mn, j+B ≠ mn, (i+j)+(A+B) ≠ cn and (i−j)+(A−B) ≠ cn for all integers — no grid point
    can lie on a horizontal, vertical, or diagonal edge, so the strict test is exact and the
    domain stays connected. `laplacian()` now asserts connectivity to prevent regression.
    """
    h = 1.0 / n
    xs = (np.arange(0, 3 * n) + A_OFF) * h
    ys = (np.arange(0, 3 * n) + B_OFF) * h
    XX, YY = np.meshgrid(xs, ys)
    m = np.zeros(XX.shape, bool)
    for t in tris:
        m |= in_tri(XX.ravel(), YY.ravel(), t).reshape(XX.shape)
    return m, h


def laplacian(mask, h):
    """5-point Dirichlet Laplacian on the interior cells (exterior neighbours contribute 0)."""
    idx = -np.ones(mask.shape, int)
    ids = np.where(mask.ravel())[0]
    idx.ravel()[ids] = np.arange(len(ids))
    N = len(ids)
    rows, cols = [], []
    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        sh = np.roll(np.roll(idx, dy, 0), dx, 1)
        if dy == 1:
            sh[0, :] = -1
        if dy == -1:
            sh[-1, :] = -1
        if dx == 1:
            sh[:, 0] = -1
        if dx == -1:
            sh[:, -1] = -1
        ok = (idx >= 0) & (sh >= 0)
        rows.append(idx[ok])
        cols.append(sh[ok])
    r = np.concatenate(rows)
    c = np.concatenate(cols)
    L = sp.coo_matrix((-np.ones(len(r)), (r, c)), shape=(N, N)).tocsr() + sp.diags(4 * np.ones(N))
    # REGRESSION GUARD: the domain must be a single connected component. The original bug
    # silently disconnected each drum into 3 congruent pieces, making the two operators the
    # same matrix relabelled. Never let that pass unnoticed again.
    import scipy.sparse.csgraph as _csg
    _A = sp.csr_matrix(L, copy=True)
    _A.setdiag(0)
    _A.eliminate_zeros()
    _nc, _ = _csg.connected_components(_A, directed=False)
    if _nc != 1:
        raise AssertionError(f"discretised drum is DISCONNECTED into {_nc} components — the "
                             f"grid is dropping interior points (see interior_mask bug note)")
    return (L / h ** 2).tocsc(), N


def spectrum(tris, n, k=NEIG):
    mask, h = interior_mask(tris, n)
    L, N = laplacian(mask, h)
    ev = spla.eigsh(L, k=k, sigma=0.0, which="LM", return_eigenvectors=False)
    return N, np.sort(ev)


def polygon_area_perimeter(v):
    v = np.array(v, float)
    x, y = v[:, 0], v[:, 1]
    area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    per = float(np.sum(np.hypot(np.diff(np.append(x, x[0])), np.diff(np.append(y, y[0])))))
    return float(area), per


def canonical(vs):
    """Translation-normalised sorted vertex set (exact, integer arithmetic)."""
    a = np.array(vs, int)
    a = a - a.min(axis=0)
    return tuple(sorted(map(tuple, a.tolist())))


def congruent(v1, v2):
    """Exhaustive check over the 8 symmetries of the square + translation. Exact/finite."""
    a = np.array(v2, int)
    for k in range(4):
        r = a.copy()
        for _ in range(k):                                  # rotate 90°: (x,y)->(-y,x)
            r = np.stack([-r[:, 1], r[:, 0]], axis=1)
        for refl in (False, True):
            s = np.stack([-r[:, 0], r[:, 1]], axis=1) if refl else r
            if canonical(s) == canonical(v1):
                return True, (k, refl)
    return False, None


def main():
    t0 = time.time()
    print("K2 — the mass tower does NOT determine the hidden geometry (gates frozen in PREREGISTRATION.md)")
    print("  Gordon-Webb-Wolpert pair: 7 congruent right-isosceles triangles glued two ways\n")

    # ---- K2b: geometry — same area & perimeter (required), but NOT congruent
    a1, p1 = polygon_area_perimeter(OUT1)
    a2, p2 = polygon_area_perimeter(OUT2)
    same_ap = abs(a1 - a2) < 1e-12 and abs(p1 - p2) < 1e-12
    cong, how = congruent(OUT1, OUT2)
    k2b = same_ap and not cong
    print(f"  K2b geometry: area {a1:.4f} vs {a2:.4f}; perimeter {p1:.6f} vs {p2:.6f}  "
          f"→ share heat-trace c₀,c₁ {'✅' if same_ap else '❌'}")
    print(f"       congruent under any of the 8 square symmetries + translation? {cong}  "
          f"→ {'PASS ✅ (genuinely different shapes)' if k2b else 'FAIL ❌'}")

    # ---- K2a/K2c (CORRECTED 2026-07-24): spectra converge with resolution.
    # The original gates demanded EXACT agreement; that was only ever attainable because the
    # buggy grid disconnected both drums into the same three pieces. On a correct (connected)
    # discretisation the drums are isospectral in the CONTINUUM (GWW theorem) and a generic FD
    # grid approaches it — so the honest gate is convergence, not exactness.
    print(f"\n  K2a/K2c — lowest {NEIG} Dirichlet eigenvalues, both drums (connected grids):")
    rows = []
    for n in RESOLUTIONS:
        N1, e1 = spectrum(DRUM1, n)
        N2, e2 = spectrum(DRUM2, n)
        rel = float(np.max(np.abs(e1 - e2)) / np.mean(e1))
        rows.append(dict(n=n, N1=int(N1), N2=int(N2), rel=rel, lam=[float(x) for x in e1[:6]]))
        print(f"    n={n:3d}: N₁={N1:6d} N₂={N2:6d}   max|Δλ|/λ̄ = {rel:.3e}")

    rels = [r["rel"] for r in rows]
    monotone = all(rels[i] < rels[i - 1] for i in range(1, len(rels)))
    shrink = rels[0] / rels[-1]
    k2a = monotone and rels[-1] < 0.05 and shrink > 3
    # observed convergence order from the finest pair
    p_obs = float(np.log(rels[-2] / rels[-1]) / np.log(RESOLUTIONS[-1] / RESOLUTIONS[-2]))
    k2c = monotone

    n_show = rows[-1]["n"]
    _, e1 = spectrum(DRUM1, n_show)
    _, e2 = spectrum(DRUM2, n_show)
    print(f"\n    spectra at n={n_show} (first 6):")
    print(f"      drum 1: {np.round(e1[:6], 4)}")
    print(f"      drum 2: {np.round(e2[:6], 4)}")

    print(f"\n    K2a KILL: spectra CONVERGE — {rels[0]:.2e} → {rels[-1]:.2e} "
          f"(shrink ×{shrink:.1f}, monotone {monotone})  →  K2 {'KILLED 💀' if k2a else 'not killed'}")
    print(f"    K2c convergence order ≈ h^{p_obs:.2f} (staircase-boundary limited) — the two drums'"
          f" spectra approach each other as h→0, consistent with exact continuum isospectrality")
    print(f"    ⚠️  RETRACTED: the earlier claim of resolution-INDEPENDENT exact agreement (~1e-15) was")
    print(f"        an artifact of a disconnection bug (see interior_mask). Exact DISCRETE isospectrality")
    print(f"        would need a transplantation-compatible grid; a generic grid is not one.")

    verdict = "KILLED" if (k2a and k2b) else "SURVIVES"
    allp = k2a and k2b and k2c
    print(f"\n  K2 {verdict}: two provably non-congruent domains whose Dirichlet towers converge to each")
    print(f"  other as the grid refines (order ~h^{p_obs:.2f}), consistent with the exact continuum GWW")
    print(f"  isospectrality. You cannot hear the shape of the drum — the spectrum does NOT fix the geometry.")

    OUT.mkdir(exist_ok=True)
    (OUT / "k2_drums.json").write_text(json.dumps({
        "resolutions": rows, "n_eigenvalues": NEIG, "grid_offsets": [A_OFF, B_OFF],
        "convergence_order_h": p_obs, "rel_shrink_factor": shrink, "monotone_convergence": bool(monotone),
        "geometry": {"area": [a1, a2], "perimeter": [p1, p2], "same_area_perimeter": bool(same_ap),
                     "congruent": bool(cong)},
        "K2a_kill": bool(k2a), "K2b_geometry_pass": bool(k2b), "K2c_convergence_pass": bool(k2c),
        "RETRACTION": "The pre-fix run reported resolution-independent EXACT agreement (~1e-15). That was an artifact of a grid bug that disconnected each drum into the same 3 congruent pieces, making the two operators one matrix relabelled. Found by tabula, confirmed by the bridge. Corrected here: connected grids, convergent (not exact) agreement.",
        "spectrum_drum1": [float(x) for x in e1], "spectrum_drum2": [float(x) for x in e2],
        "verdict": verdict, "all_pass": bool(allp),
        "summary": (f"K2 ({verdict}): the Gordon-Webb-Wolpert drums — two non-congruent domains (proved by "
                    f"exhaustive dihedral+translation search) sharing area 3.5 and perimeter — have Dirichlet "
                    f"spectra that CONVERGE to each other as the grid refines ({rels[0]:.2e} at n={RESOLUTIONS[0]} "
                    f"to {rels[-1]:.2e} at n={RESOLUTIONS[-1]}, order ~h^{p_obs:.2f}), consistent with the exact "
                    f"continuum isospectrality of the GWW theorem. The mass tower does not determine the hidden "
                    f"geometry. CORRECTION: an earlier run claimed resolution-independent EXACT agreement; that "
                    f"was a grid-bug artifact (each drum was disconnected into the same 3 congruent pieces, so "
                    f"the two operators were one matrix relabelled) — found by tabula, confirmed and fixed here, "
                    f"with a connectivity assertion added as a regression guard. Known theorem (Kac 1966 / GWW "
                    f"1992); no novelty claimed."),
        }, indent=1))
    print(f"\n  wrote results/k2_drums.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
