#!/usr/bin/env python3
"""Leg J — find a GENUINELY chaotic Manko–Novikov orbit (box-dim>1.4) to complete the positive control.

    /Users/sumit/Github/conjecture_machine/.venv/bin/python chaos_search_mn.py

The first positive-control pass (positive_control_mn.py) found every orbit at E=0.95, L=2.8 to be REGULAR by
the validated Poincaré box-dimension (it converges ≤1.16 even at 1500 crossings — diagnose_lyapunov_boxdim.py),
while the naive two-trajectory Lyapunov FALSE-flagged them (finite-difference-noise artifact, proven 3 ways).
So we have validated box-dim on REGULAR orbits but never on a CHAOTIC one — the control is only half done.

MN chaos (Gair 2008; Lukes-Gerakopoulos 2010) lives in the strong-field region for LOW-angular-momentum
orbits that can access the inner allowed pocket. This scans toward there (lower L, deeper x0, stronger q),
and for each orbit reports the RELIABLE detector (box-dim, n=300, well-resolved) next to BOTH Lyapunovs:
  • λ_naive  — ansatz default (FD step h=1e-6, d0=1e-8): the construction shown to over-report on bumps.
  • λ_clean  — de-noised (FD step h=1e-4, d0=1e-6): where the artifact vanishes (diagnostic test C/B).
A genuinely chaotic orbit shows box-dim>1.4 AND λ_clean clearly above the ~0.04 regular floor — that is the
true positive control. POWER-LOSS RESILIENT: per-orbit JSONL checkpoint, resume-skips done (q,E,L,x0).
"""
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric
from poincare import _rk4, section, box_dimension

OUT = Path(__file__).resolve().parent.parent / "results"
CKPT = OUT / "chaos_search_mn.jsonl"
FINAL = OUT / "chaos_search_mn.json"
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))

# toward MN's documented chaotic zone: strong bump, lower angular momentum, deeper turning points
GRID = []
for q in (0.95, 0.9, 0.7, 0.5):
    for E in (0.95, 0.93):
        for L in (1.6, 1.9, 2.2, 2.5):
            for x0 in (2.5, 3.0, 3.5, 4.0, 5.0, 6.0):
                GRID.append((q, E, L, x0))


def py_onshell(f, x, y, px, E, L):
    val = (-1 - f["W"](x, y, E, L) - f["g11"](x, y, E, L) * px * px) / f["g22"](x, y, E, L)
    return math.sqrt(val) if val > 0 else None


def lyap(f, s0, E, L, blocks=1200, renorm=4, h=0.02, d0=1e-8):
    s = list(s0); sp = list(s0); sp[2] += d0
    acc, T = 0.0, 0.0
    for _ in range(blocks):
        for _ in range(renorm):
            try:
                s = _rk4(f, s, h, E, L); sp = _rk4(f, sp, h, E, L)
            except (OverflowError, ValueError, ZeroDivisionError):
                return (acc / T if T > 0 else None)
        if not (BOUNDS[0][0] < s[0] < BOUNDS[0][1] and BOUNDS[1][0] < s[1] < BOUNDS[1][1]):
            break
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(s, sp)))
        if d <= 0:
            break
        acc += math.log(d / d0)
        sp = [s[i] + (sp[i] - s[i]) * d0 / d for i in range(4)]
        T += renorm * h
    return acc / T if T > 0 else None


def load_done():
    done = set()
    if CKPT.exists():
        for line in CKPT.read_text().splitlines():
            try:
                r = json.loads(line)
                done.add((r["q"], r["E"], r["L"], r["x0"]))
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def main():
    OUT.mkdir(exist_ok=True)
    done = load_done()
    print("LEG J — hunting a genuinely chaotic MN orbit (box-dim>1.4) for the true positive control")
    print(f"  grid={len(GRID)} orbits; {len(done)} already done; box-dim=reliable, λ_clean=de-noised\n")
    print(f"  {'q':>4} {'E':>5} {'L':>4} {'x0':>4} {'box-dim':>8} {'λ_naive':>8} {'λ_clean':>8}  verdict")
    rows, found = [], []
    with CKPT.open("a") as ck:
        for (q, E, L, x0) in GRID:
            if (q, E, L, x0) in done:
                continue
            fn = build_hamilton_numeric(1.0, 0.5, q)             # naive (default h=1e-6)
            fc = build_hamilton_numeric(1.0, 0.5, q, h=1e-4)     # clean derivative
            py = py_onshell(fn, x0, 0.0, 0.0, E, L)
            if py is None or py < 0.05:
                continue
            s0 = [x0, 0.0, 0.0, py]
            t0 = time.time()
            try:
                pts, drift, _ = section(fn, s0, E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                                        n=300, h=0.02, maxst=1_500_000, bounds=BOUNDS)
            except (OverflowError, ValueError, ZeroDivisionError):
                continue
            if len(pts) < 40:
                continue
            bd = float(box_dimension(pts)[0])
            ln = lyap(fn, s0, E, L, d0=1e-8)                     # naive (FD-noise-prone)
            lc = lyap(fc, s0, E, L, d0=1e-6)                     # de-noised
            chaotic = bd > 1.4
            r = {"q": q, "E": E, "L": L, "x0": x0, "box_dim": bd, "n_pts": len(pts),
                 "lam_naive": (round(ln, 4) if ln is not None else None),
                 "lam_clean": (round(lc, 4) if lc is not None else None), "chaotic_boxdim": chaotic}
            ck.write(json.dumps(r) + "\n"); ck.flush()
            rows.append(r)
            if chaotic:
                found.append(r)
            lns = f"{ln:.3f}" if ln is not None else "None"
            lcs = f"{lc:.3f}" if lc is not None else "None"
            print(f"  {q:>4} {E:>5} {L:>4} {x0:>4} {bd:>8.2f} {lns:>8} {lcs:>8}  "
                  f"{'<<< CHAOTIC' if chaotic else 'regular'}  ({time.time()-t0:.0f}s)", flush=True)

    print(f"\n  === {len(found)} box-dim-confirmed chaotic orbit(s) found (of {len(rows)} new) ===")
    for r in sorted(found, key=lambda r: -r["box_dim"])[:8]:
        print(f"    q={r['q']} E={r['E']} L={r['L']} x0={r['x0']}: box-dim={r['box_dim']:.2f}, "
              f"λ_clean={r['lam_clean']} (vs ~0.04 floor)")
    FINAL.write_text(json.dumps({"grid": len(GRID), "rows": rows, "n_chaotic": len(found)}, indent=1))
    print(f"\n  wrote {FINAL.name} (+ durable {CKPT.name})")


if __name__ == "__main__":
    main()
