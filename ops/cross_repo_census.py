#!/usr/bin/env python3
"""Mechanical cross-repo edge census for TheBridge.

A4 §8 said the next independence audit must be mechanical, not testimonial, and
tabula's gate then MEASURED why: their own hand answer to this exact question was
incomplete within the hour. A census answers "what is there now"; a prose claim
answers "what was there when I wrote it".

Three edge classes, because they carry different evidential weight:
  IMPORT  sys.path.insert -> we run THEIR code.   Their measurement, not ours.
  DATA    we read THEIR results file.             Their number, not ours.
  VENV    we run under THEIR interpreter.         Environment only -- NOT an edge.

Exit 1 on: an undeclared IMPORT/DATA edge, or a DECLARED edge that has vanished
(a stale allowlist is a scope statement with the identical defect as the sentence
it replaced -- L18).
"""
import re, sys, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIBS = ["conjecture_machine", "SpaceTime", "BlackHole", "quantum", "corner_function"]
# Anchor on the absolute repo root a real cross-repo reference always carries.
# (tabula's false positive was a slash inside English prose: "ansatz/TheBridge's rule".)
PATH_RE = re.compile(r"/Users/sumit/Github/(" + "|".join(SIBS) + r")(/[\w./\-]*)?")

ALLOWLIST = pathlib.Path(__file__).parent / "cross_repo_allowlist.json"

def classify(line):
    if ".venv/bin/python" in line:
        return "VENV"
    if "sys.path.insert" in line or re.search(r"^\s*(from|import)\s", line):
        return "IMPORT"
    if re.search(r"\.(json|npz|txt|csv|h5)\b", line):
        return "DATA"
    return "REF"

def scan():
    edges = {}
    for p in sorted(ROOT.rglob("*.py")):
        if ".git" in p.parts or p.name == "cross_repo_census.py":
            continue
        for i, ln in enumerate(p.read_text(errors="replace").splitlines(), 1):
            m = PATH_RE.search(ln)
            if not m:
                continue
            kind = classify(ln)
            key = f"{kind}:{m.group(1)}"
            edges.setdefault(key, []).append(f"{p.relative_to(ROOT)}:{i}")
    return edges

def main():
    edges = scan()
    declared = json.loads(ALLOWLIST.read_text()) if ALLOWLIST.exists() else {}

    live = {k: v for k, v in edges.items() if not k.startswith("VENV:")}
    undeclared = sorted(set(live) - set(declared))
    stale      = sorted(set(declared) - set(live))

    print(f"{'EDGE':<28} {'N':>4}  STATUS")
    for k in sorted(edges):
        n = len(edges[k])
        if k.startswith("VENV:"):
            status = "environment only (not an edge)"
        elif k in declared:
            status = f"declared -- {declared[k]}"
        else:
            status = "*** UNDECLARED ***"
        print(f"  {k:<26} {n:>4}  {status}")

    fail = False
    if undeclared:
        print(f"\nFAIL: {len(undeclared)} undeclared edge class(es): {undeclared}")
        for k in undeclared:
            print(f"  {k} first seen at {edges[k][0]}")
        fail = True
    if stale:
        print(f"\nFAIL: {len(stale)} DECLARED edge(s) no longer present: {stale}")
        print("  A stale allowlist is a scope statement with the defect it was meant to fix (L18).")
        fail = True
    if not fail:
        print(f"\nPASS: {len(live)} edge class(es), all declared; none stale.")
    return 1 if fail else 0

sys.exit(main())
