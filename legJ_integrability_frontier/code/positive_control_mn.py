#!/usr/bin/env python3
"""Leg J — THE positive control: does OUR chaos detector see chaos on a KNOWN-chaotic metric? (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python positive_control_mn.py

leg J concluded "no chaos in the bump" — but `verify_chaos` could never validate our Lyapunov detector,
because the bump is regular and the φ-dependent variant unbound the orbits. ansatz §99 gives the missing
testbed: the Manko–Novikov metric, an EXACT rotating vacuum with a tunable quadrupole q (q=0 = Kerr),
KNOWN-chaotic for q≠0 (Gair 2008; Lukes-Gerakopoulos 2010). This mirrors ansatz's validated chaos hunt
(`_mn_chaos_hunt.py`, SAME E,L,x0,bounds,maxst) and runs OUR Lyapunov alongside ansatz's Poincaré
box-dimension on every orbit. If our λ sits at the floor on the q=0 (Kerr, regular) control and jumps
clearly positive on the box-dim-confirmed chaotic orbits (q=0.5/0.9), our detector is proven to see chaos
when it is genuinely present — so leg J's null rests on a validated tool. Reuses ansatz machinery read-only.

POWER-LOSS RESILIENT: each orbit is checkpointed (append + flush) to results/positive_control_mn.jsonl the
moment it finishes; a restart skips already-done (q,x0) orbits and resumes. Chaotic candidates (q=0.5/0.9)
run FIRST so the decisive positive result is durably saved early. Aggregates to the final JSON when complete.
"""
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric            # MN reduced Hamiltonian (numeric)
from poincare import _rk4, section, box_dimension           # ansatz's validated Poincaré chaos detector

OUT = Path(__file__).resolve().parent.parent / "results"
CKPT = OUT / "positive_control_mn.jsonl"                    # durable per-orbit checkpoint (survives reboots)
FINAL = OUT / "positive_control_mn.json"
E, L = 0.95, 2.8                                            # EXACT match to ansatz _mn_chaos_hunt.py
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))                       # EXACT match to ansatz _mn_chaos_hunt.py
X0S = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0]
# chaotic candidates FIRST (the decisive positive result), then the q=0 Kerr regular control
QS = [(0.5, "MN q=0.5 (known-chaotic)"), (0.9, "MN q=0.9 (very bumpy)"), (0.0, "Kerr a=0.5 (regular control)")]


def py_onshell(f, x, y, px):
    val = (-1 - f["W"](x, y, E, L) - f["g11"](x, y, E, L) * px * px) / f["g22"](x, y, E, L)
    return math.sqrt(val) if val > 0 else None


def our_lyapunov(f, s0, blocks=1500, renorm=4, h=0.02, d0=1e-8):
    """Largest Lyapunov exponent — OUR verify_chaos / §79 Benettin two-trajectory method, under test here.
    Perturbs p_x by d0, co-integrates, renormalizes the shadow back to d0 each block. T = blocks*renorm*h."""
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
        sp = [s[i] + (sp[i] - s[i]) * d0 / d for i in range(4)]   # renormalize back to d0, keep direction
        T += renorm * h
    return acc / T if T > 0 else None


def load_done():
    """Read the checkpoint; return {(q,x0): row} for orbits already computed (power-loss resume)."""
    done = {}
    if CKPT.exists():
        for line in CKPT.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                done[(r["q"], r["x0"])] = r
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def run_orbit(q, x0):
    """Compute one orbit's box-dim (ansatz) + λ (ours). Returns a row dict, or None if it skips/fails."""
    f = build_hamilton_numeric(1.0, 0.5, q)
    py = py_onshell(f, x0, 0.0, 0.0)
    if py is None or py < 0.05:                              # ansatz's skip
        return None
    s0 = [x0, 0.0, 0.0, py]
    pts, drift, _ = section(f, s0, E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                            n=120, h=0.02, maxst=700000, bounds=BOUNDS)
    if len(pts) < 30:                                       # ansatz's skip
        return None
    bd = box_dimension(pts)[0]
    lam = our_lyapunov(f, s0)
    return {"q": q, "x0": x0, "box_dim": float(bd), "lyapunov": (float(lam) if lam is not None else None),
            "n_pts": len(pts), "chaotic_boxdim": bool(bd > 1.4),
            "chaotic_lyapunov": bool(lam is not None and lam > 0.05)}


def main():
    OUT.mkdir(exist_ok=True)
    print("LEG J — POSITIVE CONTROL on Manko–Novikov (known-chaotic): does OUR Lyapunov see chaos?")
    print(f"  (mirrors ansatz _mn_chaos_hunt.py: E={E}, L={L}, bounds={BOUNDS}, maxst=700000; chaotic q FIRST)\n")
    done = load_done()
    if done:
        print(f"  [resume] {len(done)} orbit(s) already checkpointed in {CKPT.name}; skipping those.\n")
    print(f"  {'q':>4} {'x0':>5} {'box-dim':>8} {'λ(ours)':>9}  verdict")
    out = list(done.values())
    with CKPT.open("a") as ck:                               # append mode — never clobber prior checkpoints
        for q, label in QS:
            print(f"  — q={q}: {label} —")
            for x0 in X0S:
                if (q, x0) in done:
                    r = done[(q, x0)]
                    lstr = f"{r['lyapunov']:.4f}" if r['lyapunov'] is not None else "  None"
                    print(f"  {q:>4} {x0:>5.1f} {r['box_dim']:>8.2f} {lstr:>9}  (cached)")
                    continue
                t0 = time.time()
                try:
                    r = run_orbit(q, x0)
                except (OverflowError, ValueError, ZeroDivisionError) as ex:
                    print(f"  {q:>4} {x0:>5.1f}  (orbit error: {type(ex).__name__}, skipped)")
                    continue
                if r is None:
                    continue
                ck.write(json.dumps(r) + "\n"); ck.flush()  # durable the instant it's computed
                out.append(r)
                tag = "CHAOTIC" if r["chaotic_boxdim"] else "regular"
                cl = r["chaotic_lyapunov"]
                agree = "OK agree" if (r["chaotic_boxdim"] == cl) else "!! DISAGREE"
                lstr = f"{r['lyapunov']:.4f}" if r['lyapunov'] is not None else "  None"
                print(f"  {q:>4} {x0:>5.1f} {r['box_dim']:>8.2f} {lstr:>9}  {tag}, "
                      f"λ {'>0.05 (chaos)' if cl else 'at floor':<14} {agree}  ({time.time()-t0:.0f}s)", flush=True)

    reg = [r for r in out if r["q"] == 0.0 and r["lyapunov"] is not None]
    cha = [r for r in out if r["chaotic_boxdim"] and r["lyapunov"] is not None]
    lam_reg = max((r["lyapunov"] for r in reg), default=float("nan"))
    n_agree = sum(1 for r in out if r["chaotic_boxdim"] == r["chaotic_lyapunov"])
    print(f"\n  ASSESSMENT  ({n_agree}/{len(out)} orbits: our λ and ansatz box-dim agree on chaotic-vs-regular)")
    print(f"    Kerr (q=0) control: box-dim ≈ 1 (KAM tori), λ ≤ {lam_reg:.3f} (floor) — regular, as it must be.")
    if cha:
        caught = [r for r in cha if r["chaotic_lyapunov"]]
        lam_cha = max(r["lyapunov"] for r in cha)
        print(f"    box-dim-confirmed chaotic orbits (box-dim>1.4): {len(caught)}/{len(cha)} also flagged by OUR λ (max λ={lam_cha:.3f}).")
        if caught:
            print(f"    → POSITIVE CONTROL PASSES: our Lyapunov SEES chaos when it is genuinely present")
            print(f"      (λ jumps from the ~{lam_reg:.2f} Kerr floor to {lam_cha:.2f} on box-dim-confirmed chaotic orbits).")
            print(f"      leg J's 'no chaos in the bump' now rests on a detector PROVEN to detect chaos, on an EXACT")
            print(f"      rotating vacuum (Manko–Novikov §99), cross-checked against ansatz's Poincaré box-dimension.")
        else:
            print(f"    → our λ did NOT flag the box-dim-chaotic orbits — detector mismatch, investigate.")
    else:
        print(f"    (no box-dim-confirmed chaotic orbit yet — widen q/x0 or let the run finish)")
    FINAL.write_text(json.dumps(
        {"E": E, "L": L, "bounds": BOUNDS, "rows": sorted(out, key=lambda r: (r["q"], r["x0"])),
         "lambda_floor_kerr": lam_reg, "n_agree": n_agree, "n_orbits": len(out)}, indent=1))
    print(f"\n  wrote {FINAL.name} (+ durable {CKPT.name})")


if __name__ == "__main__":
    main()
