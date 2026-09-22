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

STATED BLIND SPOTS. A census claiming completeness it does not have is worse than
one that bounds itself (tabula, who stated theirs first and prompted this block).

  1. MATCHES ABSOLUTE PATHS ONLY. A relative "../conjecture_machine/..." or a
     post-chdir relative read would be invisible.
     CHECKED 2026-09-22: this repo has NO chdir anywhere and NO relative sibling
     references, so neither pattern is live here. Re-check if either appears.
  2. BARE SIBLING IMPORTS ARE UNDER-COUNTED. 20 lines of the form
     `from _kt_double import ...` carry no path of their own; they work only
     because a sys.path.insert ran earlier in the SAME file. The file is therefore
     never missed -- the insert is always caught -- but the KIND and COUNT within
     an already-flagged file are under-reported. Structurally identical to
     tabula's chdir case, by a different mechanism.
  3. A file using a sibling with neither an absolute path nor an in-file insert
     would be missed entirely. No such file exists here today; nothing guarantees
     that tomorrow, which is what clause 1 of the gate is for.
"""
import re, sys, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIBS = ["conjecture_machine", "SpaceTime", "BlackHole", "quantum", "corner_function"]
# Anchor on the absolute repo root a real cross-repo reference always carries.
# (tabula's false positive was a slash inside English prose: "ansatz/TheBridge's rule".)
PATH_RE = re.compile(r"/Users/sumit/Github/(" + "|".join(SIBS) + r")(/[\w./\-]*)?")

ALLOWLIST = pathlib.Path(__file__).parent / "cross_repo_allowlist.json"

# PATH-INDEPENDENT SIGNAL (tabula's fix, adopted 2026-09-22).
# The case BOTH path-censuses miss entirely: a file importing a sibling module with
# NEITHER an absolute path NOR an in-file sys.path.insert -- reached via PYTHONPATH,
# a .pth, or an installed package. Paths cannot see it; the NAMESPACE can.
# List built empirically: every module imported by a path-flagged bridge file that
# resolves to a sibling repo and NOT to a file in this one.
SIBLING_MODULES = {
    "conjecture_machine": ["_mn_invariant", "_plateau_v3_section", "_zv_invariant", "ck",
                           "emri", "geodesic_chaos", "gr_engine", "manko_novikov",
                           "poincare", "qnm_precise"],
    "BlackHole": ["echolib", "rdlib"],
}
SIBLING_PREFIXES = {"conjecture_machine": ["_kt_"]}
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([\w.]+)")

def classify(line):
    if ".venv/bin/python" in line:
        return "VENV"
    if "sys.path.insert" in line or re.search(r"^\s*(from|import)\s", line):
        return "IMPORT"
    if re.search(r"\.(json|npz|txt|csv|h5)\b", line):
        return "DATA"
    return "REF"

def scan_namespace():
    """Files importing a sibling MODULE. Split by whether a path also appears:
    with a path -> already covered; WITHOUT -> the case paths cannot see."""
    hits = {}
    for p in sorted(ROOT.rglob("*.py")):
        if ".git" in p.parts or p.name == "cross_repo_census.py":
            continue
        txt = p.read_text(errors="replace")
        has_path = bool(PATH_RE.search(txt))
        for ln in txt.splitlines():
            m = IMPORT_RE.match(ln)
            if not m:
                continue
            mod = m.group(1).split(".")[0]
            for sib, mods in SIBLING_MODULES.items():
                pre = SIBLING_PREFIXES.get(sib, [])
                if mod in mods or any(mod.startswith(x) for x in pre):
                    key = f"NAMESPACE:{sib}" + ("" if has_path else ":NO-PATH")
                    hits.setdefault(key, []).append(f"{p.relative_to(ROOT)}")
    return hits

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

def _run():
    edges = scan()
    edges.update(scan_namespace())
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

def main():
    return _run()

def selftest():
    """Three known-fail arms. A gate only ever seen to pass has not been tested,
    and a control that cannot be re-run becomes decoration (quantum's, 2026-09-22)."""
    import json, tempfile, os
    orig = ALLOWLIST.read_text()
    ctl = ROOT / "ops" / "_selftest_nopath_TMP.py"
    arms, ok = [], True
    try:
        # arm 1: undeclared edge must fail
        d = json.loads(orig); d.pop("IMPORT:conjecture_machine", None)
        ALLOWLIST.write_text(json.dumps(d))
        arms.append(("undeclared edge", _quiet() == 1))
        # arm 2: stale declaration must fail
        d = json.loads(orig); d["DATA:no_such_repo"] = "stale"
        ALLOWLIST.write_text(json.dumps(d))
        arms.append(("stale declaration", _quiet() == 1))
        # arm 3: the invisible file -- sibling import, no path anywhere
        ALLOWLIST.write_text(orig)
        ctl.write_text("from poincare import build_hamilton  # control\n")
        arms.append(("no-path sibling import", _quiet() == 1))
    finally:
        ALLOWLIST.write_text(orig)
        if ctl.exists():
            ctl.unlink()
    for name, passed in arms:
        print(f"  {'PASS' if passed else 'FAIL'}  arm fires on: {name}")
        ok &= passed
    print(f"  {'PASS' if _quiet() == 0 else 'FAIL'}  clean state returns 0")
    return 0 if ok and _quiet() == 0 else 1

def _quiet():
    import io, contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            return _run()
    except SystemExit as e:
        return e.code

if "--selftest" in sys.argv:
    sys.exit(selftest())
sys.exit(main())
