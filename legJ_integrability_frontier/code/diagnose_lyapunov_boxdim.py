#!/usr/bin/env python3
"""Leg J — DIAGNOSTIC: why does our Lyapunov disagree with ansatz's box-dim on MN q=0.5? (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python diagnose_lyapunov_boxdim.py

The positive control (positive_control_mn.py) surfaced a SYSTEMATIC disagreement on Manko–Novikov q=0.5:
ansatz's Poincaré box-dimension says REGULAR (~1.0 at n=120 crossings) while our two-trajectory Benettin
Lyapunov says CHAOTIC (λ≈0.13–0.31). q=0 Kerr agrees (both regular). Two hypotheses, opposite implications:
  H-A  the orbits ARE (weakly) chaotic; box-dim at 120 crossings is under-resolved (box-count saturates at
       ≤120 boxes → biased toward dim 1). Then our λ is the MORE sensitive detector.
  H-B  the orbits are regular; our λ is a FALSE POSITIVE — finite-difference force noise. build_hamilton_numeric
       differentiates the metric by central differences (h=1e-6 → roundoff ~1e-10 rel); with d0=1e-8 that noise
       is a large fraction of the true separation signal, worse on the bumpy (q=0.5) metric than smooth Kerr.

Three decisive tests, no claim assumed:
  (A) GROUND TRUTH — box-dim vs n (120→1500 crossings on the SAME long orbit). Climbs→2 ⇒ chaotic (H-A);
      stays ~1 ⇒ regular (H-B).
  (B) d0-SENSITIVITY of our λ. A TRUE exponent is d0-independent; a noise-driven one GROWS as d0 shrinks.
  (C) h-SENSITIVITY of our λ (ansatz's build_hamilton_numeric takes the finite-difference step h as an arg!).
      Real chaos is independent of how derivatives are computed; a numerical artifact collapses with cleaner
      (larger-h, less-roundoff) derivatives.
Reuses ansatz machinery read-only; varies only the diagnostic knobs (n, d0, h).
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
E, L = 0.95, 2.8
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))


def py_onshell(f, x, y, px):
    val = (-1 - f["W"](x, y, E, L) - f["g11"](x, y, E, L) * px * px) / f["g22"](x, y, E, L)
    return math.sqrt(val) if val > 0 else None


def our_lyapunov(f, s0, blocks=1500, renorm=4, h=0.02, d0=1e-8):
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


def main():
    ORBITS = [(0.5, 4.0), (0.5, 7.0), (0.0, 4.0)]            # two "disagree" q=0.5 + one Kerr control
    report = {"E": E, "L": L, "orbits": []}
    JF = OUT / "diagnose_lyapunov_boxdim.json"
    done = {}
    if JF.exists():                                          # power-loss resume: keep completed orbits
        try:
            for o in json.loads(JF.read_text()).get("orbits", []):
                done[(o["q"], o["x0"])] = o
        except (json.JSONDecodeError, KeyError):
            done = {}
    print("LEG J DIAGNOSTIC — is the MN q=0.5 'chaos' real (H-A) or finite-difference noise (H-B)?\n")
    if done:
        print(f"  [resume] {len(done)} orbit(s) already saved; recomputing only the rest.\n")

    for q, x0 in ORBITS:
        if (q, x0) in done:                                  # already computed (survived a prior run)
            report["orbits"].append(done[(q, x0)])
            print(f"=== q={q}, x0={x0}  (cached) ===\n")
            continue
        f = build_hamilton_numeric(1.0, 0.5, q)             # ansatz default h=1e-6
        py = py_onshell(f, x0, 0.0, 0.0)
        print(f"=== q={q}, x0={x0}  (py={py:.4f}) ===")
        rec = {"q": q, "x0": x0}
        if py is None or py < 0.05:
            print("  (skipped: off-shell / py<0.05)\n"); report["orbits"].append({**rec, "skipped": True}); continue
        s0 = [x0, 0.0, 0.0, py]

        # (A) ground truth: one long section, box-dim on growing prefixes
        t0 = time.time()
        pts, drift, _ = section(f, s0, E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                                n=1500, h=0.02, maxst=4_000_000, bounds=BOUNDS)
        bdims = {}
        for k in (120, 400, 800, 1500):
            if len(pts) >= k:
                bdims[k] = float(box_dimension(pts[:k])[0])
        bdstr = "  ".join(f"n={k}:{v:.2f}" for k, v in bdims.items())
        trend = ("CLIMBS→chaotic" if (max(bdims) in bdims and bdims[max(bdims)] > 1.4)
                 else "flat~1 → regular")
        print(f"  (A) box-dim vs n  [{len(pts)} crossings, {time.time()-t0:.0f}s]:  {bdstr}   ⇒ {trend}")
        rec["box_dim_vs_n"] = bdims

        # (B) d0-sensitivity of our λ (ansatz default h=1e-6)
        lam_d0 = {}
        for d0 in (1e-6, 1e-7, 1e-8, 1e-9, 1e-10):
            v = our_lyapunov(f, s0, d0=d0)
            lam_d0[f"{d0:.0e}"] = (round(v, 4) if v is not None else None)
        print(f"  (B) λ vs d0:  " + "  ".join(f"{k}:{v}" for k, v in lam_d0.items()))
        rec["lambda_vs_d0"] = lam_d0

        # (C) h-sensitivity of our λ (rebuild Hamiltonian with larger finite-difference step → less roundoff)
        lam_h = {}
        for hh in (1e-6, 1e-5, 1e-4, 1e-3):
            fh = build_hamilton_numeric(1.0, 0.5, q, h=hh)
            v = our_lyapunov(fh, s0, d0=1e-8)
            lam_h[f"{hh:.0e}"] = (round(v, 4) if v is not None else None)
        print(f"  (C) λ vs FD-step h (d0=1e-8):  " + "  ".join(f"{k}:{v}" for k, v in lam_h.items()))
        rec["lambda_vs_h"] = lam_h
        print()
        report["orbits"].append(rec)
        OUT.mkdir(exist_ok=True)                            # durable per-orbit (flaky power tonight)
        (OUT / "diagnose_lyapunov_boxdim.json").write_text(json.dumps(report, indent=1))

    # interpretation
    print("INTERPRETATION:")
    print("  • If (A) stays ~1 AND (B) λ grows as d0↓ AND (C) λ collapses as h↑  ⇒  H-B: our λ is FD-noise")
    print("    (the MN q=0.5 orbits are regular; box-dim is right; our two-trajectory λ over-reports on the")
    print("     finite-difference-force Hamiltonian — a detector limitation, not real chaos).")
    print("  • If (A) climbs→2 AND (B)/(C) λ stable  ⇒  H-A: real (weak) chaos, box-dim under-resolved at n=120.")
    OUT.mkdir(exist_ok=True)
    (OUT / "diagnose_lyapunov_boxdim.json").write_text(json.dumps(report, indent=1))
    print(f"\n  wrote results/diagnose_lyapunov_boxdim.json")


if __name__ == "__main__":
    main()
