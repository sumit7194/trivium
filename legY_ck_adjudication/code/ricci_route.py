#!/usr/bin/env python3
"""Leg Y — Y1b: the cheap SOUND route (order-0 Ricci/Segre invariants), per the post-hoc AMENDMENT.

    /Users/sumit/Github/conjecture_machine/.venv/bin/python ricci_route.py

Frame-independent order-0 invariants (ansatz S117): no tetrad, no canonicalization, no grad-Weyl -- so they
escape the swell wall that stopped ck_adjudicate.py. Logic, one direction only: DIFFERING invariants are a
rigorous INEQUIVALENT; MATCHING ones are INCONCLUSIVE (never reported as evidence of sameness).
"""
import json
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
import sympy as sp
import ck
from ck_adjudicate import ENTRIES, Y1_SET, Timeout, _alarm

# domains as Q-predicates (the form ck.set_domain expects, per ansatz S117 usage) -- BUGFIX
from ck_adjudicate import r, u, x, y


def qdom(name):
    if name.startswith("ZV"):
        return [sp.Q.positive(x - 2), sp.Q.positive(y), sp.Q.positive(1 - y)]
    return [sp.Q.positive(r - 3), sp.Q.positive(u), sp.Q.positive(1 - u)]

OUT = Path(__file__).resolve().parent.parent / "results"
BUDGET = 240


def order0(name):
    build, dom = ENTRIES[name]
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(BUDGET)
    t0 = time.time()
    try:
        ck.set_domain(*qdom(name))
        geo = build()
        inv, Rm = ck.ricci_invariants(geo)          # BUGFIX: returns (list, Rm), not a flat list
        seg = ck.segre_type(geo, Rm)
        signal.alarm(0)
        return {"invariants": [sp.simplify(i) for i in inv], "segre": str(seg),
                "seconds": round(time.time() - t0, 1)}
    except Timeout:
        signal.alarm(0)
        return {"error": f"WALL {BUDGET}s", "seconds": round(time.time() - t0, 1)}
    except Exception as e:
        signal.alarm(0)
        return {"error": f"{type(e).__name__}: {str(e)[:120]}", "seconds": round(time.time() - t0, 1)}
    finally:
        signal.alarm(0)


def main():
    print("LEG Y — Y1b, the cheap SOUND route (post-hoc amendment; differing => rigorous INEQUIVALENT)\n")
    data = {}
    for n in Y1_SET:
        data[n] = order0(n)
        d = data[n]
        if "error" in d:
            print(f"  {n:18s} {d['seconds']:6.1f}s  {d['error']}")
        else:
            print(f"  {n:18s} {d['seconds']:6.1f}s  Segre {d['segre']:22s} inv {[str(i)[:22] for i in d['invariants']]}")

    print(f"\n  pairwise (sound direction only):")
    pairs, decided = [], 0
    for i in range(len(Y1_SET)):
        for j in range(i + 1, len(Y1_SET)):
            a, b = Y1_SET[i], Y1_SET[j]
            da, db = data[a], data[b]
            if "error" in da or "error" in db:
                v, why = "UNDECIDED(wall)", "signature unavailable"
            else:
                diff_seg = da["segre"] != db["segre"]
                diff_inv = any(sp.simplify(x - y) != 0 for x, y in zip(da["invariants"], db["invariants"]))
                if diff_seg or diff_inv:
                    v, why = "INEQUIVALENT (rigorous)", ("Segre differs" if diff_seg else "Ricci invariants differ")
                    decided += 1
                else:
                    v, why = "INCONCLUSIVE", "order-0 matches (necessary, not sufficient) — NOT evidence of sameness"
            pairs.append({"a": a, "b": b, "verdict": v, "why": why})
            print(f"     {a:16s} vs {b:16s} → {v:24s} {why}")

    print(f"\n  decided rigorously by this route: {decided}/{len(pairs)}  "
          f"(the rest stay open; no matching result is counted as support for distinctness)")
    OUT.mkdir(exist_ok=True)
    (OUT / "ricci_route.json").write_text(json.dumps(
        {"amendment": "post-hoc, after the v1 wall", "budget_s": BUDGET,
         "entries": {k: {kk: (str(vv) if kk == "invariants" else vv) for kk, vv in v.items()}
                     for k, v in data.items()},
         "pairs": pairs, "decided_rigorously": decided, "total_pairs": len(pairs)}, indent=1, default=str))
    print(f"  wrote results/ricci_route.json")


if __name__ == "__main__":
    main()
