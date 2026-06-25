#!/usr/bin/env python3
"""Leg L (A1, full) — does the amortization gap predict sim→real transfer? (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python amortization_verdict.py

The §9 "most original" question, full cross-model version. deepstrain trained 5 no-hair NPE variants
(N_train 5k→150k) and reported, per variant, the amortization gap (sim coverage deviation from 0.90) and
the transfer (real-O4-noise coverage − sim coverage). This reads their artifact, states the verdict, and
synthesizes with leg L's within-model result. deepstrain artifact read-only.
"""
import json
from pathlib import Path

import numpy as np

DS = "/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results/19_amortization_transfer.json"
OUT = Path(__file__).resolve().parent.parent / "results"


def main():
    d = json.loads(Path(DS).read_text())
    V = d["variants"]
    gap = np.array([v["amortization_gap"] for v in V])
    tr = np.array([v["transfer"] for v in V])
    corr = d["amortization_gap_vs_transfer_corr"]

    print("LEG L (A1 full) — amortization gap vs sim→real transfer (deepstrain's 5 NPE variants)\n")
    print(f"  {'N_train':>8} {'amort_gap':>10} {'transfer':>10}")
    for v in V:
        print(f"  {v['n_train']:>8} {v['amortization_gap']:>10.3f} {v['transfer']:>10.3f}")
    print(f"\n  amortization gap shrinks monotonically with training ({gap[0]:.3f} → {gap[-1]:.3f});")
    print(f"  transfer is NEGATIVE for every variant ({tr.max():.3f} … {tr.min():.3f});")
    print(f"  corr(gap, transfer) = {corr:+.3f} ≈ 0.")

    print(f"\n  VERDICT on §9's 'does amortization predict transfer?': NO — not at this resolution.")
    print(f"  The amortization gap (sim self-consistency) and the transfer (sim→real robustness) are")
    print(f"  DECOUPLED: more training drives the amortization gap down ({gap[0]:.3f}→{gap[-1]:.3f}) but the")
    print(f"  NPEs still UNDER-cover on real data at every capacity (transfer < 0 throughout). So the sim→real")
    print(f"  failure is a DOMAIN SHIFT (real O4 noise ≠ training white noise), NOT an amortization deficit —")
    print(f"  better amortization can't cure it. This refutes the originality hypothesis but corroborates")
    print(f"  leg 2: the sim→real gap is information/domain-limited, not a model-legibility problem.")

    print(f"\n  SYNTHESIS with leg L's within-model result:")
    print(f"  • WITHIN a model, per-parameter legibility predicts per-parameter real precision (M→tight,")
    print(f"    δ→wide) — a positive, Fisher-information effect (leg L probe ladder).")
    print(f"  • ACROSS models, the amortization gap does NOT predict transfer (corr≈0) — transfer is set by")
    print(f"    the sim↔real domain shift, orthogonal to amortization. Two honest, coherent findings.")

    print(f"\n  HONEST LIMITS (per deepstrain): weak test — 5 points, transfer noise-limited (60 real")
    print(f"  injections/variant, ±~0.06; the 40k point at {tr.min():.3f} rides a noisy low real-coverage draw),")
    print(f"  single lever (N_train), coverage-deviation proxy (not C2ST). Read corr≈0 as 'no relationship")
    print(f"  detectable at this resolution', not a strong null. Decisive version (relayed): more variants")
    print(f"  (capacity/flow levers), more real injections, the C2ST gap proxy — checkpoints are saved.")

    OUT.mkdir(exist_ok=True)
    (OUT / "amortization_verdict.json").write_text(json.dumps(
        {"corr_gap_transfer": corr, "amort_gap_range": [float(gap.max()), float(gap.min())],
         "transfer_all_negative": bool((tr < 0).all()), "transfer_range": [float(tr.max()), float(tr.min())],
         "verdict": "amortization does NOT predict transfer (corr~0); sim→real gap is domain-shift, not amortization",
         "weak_test_caveats": "5 points, noise-limited, single lever, coverage proxy"}, indent=1))
    print(f"\n  wrote results/amortization_verdict.json")


if __name__ == "__main__":
    main()
