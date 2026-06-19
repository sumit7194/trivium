#!/usr/bin/env python3
"""Move D — ANSATZ SIDE: certify each ε's distilled candidate as a Killing tensor.

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python certify_sweep.py

Reuses Move A's certifier (read-only import): reconstructs K^{μν} from tabula's coefficients
and computes the metric-scale-normalized Killing-tensor residual on the deformed metric."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as ex                       # deformed metric, read-only
import certify_killing as ck                        # Move A certifier helpers, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"
EPS_GRID = [0.00, 0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35]
A, R0S = 0.6, (6, 7, 8, 9, 10)


def main():
    print("MOVE D — certifying candidates as Killing tensors across ε (ansatz side)")
    for eps in EPS_GRID:
        cand = json.loads((RESULTS / f"candidate_eps{eps:.2f}.json").read_text())
        gfun = (lambda e: (lambda x: ex.g_bumpy(x, A, e)))(eps)
        Kup = ck.K_upper_from_candidate(cand)
        Kl = ck.K_lower_fn(Kup, gfun)
        pts = ck.sample_points({"r0s": R0S}, 25)
        rr = [ck.killing_residual(Kl, gfun, p) for p in pts]
        raw = max(r for r, _ in rr)
        ks = sum(k for _, k in rr) / len(rr)
        norm = raw / (ks if ks > 1e-12 else 1.0)
        verdict = "EXISTS" if norm < 1e-3 else "DESTROYED"
        out = {"eps": eps, "norm_resid": norm, "verdict": verdict,
               "tabula_verdict": cand["verdict"], "tabula_varratio": cand["heldout_varratio"]}
        (RESULTS / f"certify_eps{eps:.2f}.json").write_text(json.dumps(out, indent=1))
        agree = "AGREE" if verdict == cand["verdict"] else "*** MISMATCH ***"
        print(f"  eps={eps:.2f}  ansatz norm_resid={norm:.2e} → {verdict:9s}  "
              f"tabula {cand['verdict']:9s} (vr={cand['heldout_varratio']:.1e})  {agree}")


if __name__ == "__main__":
    main()
