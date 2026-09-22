#!/usr/bin/env python3
"""A4a -- mechanical census of candidate transfer edges. CLASSIFIES NOTHING.

Per the frozen pre-registration: the enumeration must be mechanical, not curated,
so the sample cannot be cherry-picked toward the auditor's prior. This script emits
candidates with file:line + context. Every classification decision is made later,
by hand, against the frozen E1-E4 conditions.
"""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]

# Repo identity: local dir name, public name, and session/persona alias.
REPOS = {
    "ansatz":     [r"ansatz", r"conjecture_machine"],
    "tabula":     [r"tabula", r"SpaceTime"],
    "deepstrain": [r"deepstrain", r"BlackHole"],
    "quantum":    [r"quantum", r"vestigium"],
    "cuspis":     [r"cuspis", r"corner_function"],
    "bridge":     [r"\bbridge\b", r"trivium"],
}
REPO_RE = {k: re.compile("|".join(v), re.I) for k, v in REPOS.items()}

# Transfer language. Deliberately verb-led: a line naming two repos without a
# transfer verb is co-mention, not an edge.
TRANSFER = re.compile(
    r"\b(relay(?:ed|s|ing)?|sent|send(?:s|ing)?|ask(?:ed|s)?|fulfill?(?:ed)?|"
    r"import(?:ed|s|ing)?|adopt(?:ed|s|ing)?|inherit(?:ed|s|ing)?|"
    r"propagat(?:ed|es|ing)|borrow(?:ed|s)?|vendor(?:ed)?|"
    r"contribut(?:ed|es|ion)|credit(?:ed|s)?|told|gave|given|handed|"
    r"received|reported to|passed (?:to|on)|took from|per their|their number|"
    r"refus(?:ed|es|al)|declin(?:ed|es)|withdrew|withdrawn)\b", re.I)

# Explicit independence language -- tracked separately; these are the rows that
# are findings rather than absences.
INDEP = re.compile(r"\bindependen|\becho\b|\bcorrobora|\brepeated\b|ignorant of each other", re.I)

def sweep(path):
    out = []
    try:
        lines = path.read_text(errors="replace").splitlines()
    except Exception:
        return out
    rel = str(path.relative_to(ROOT))
    for i, ln in enumerate(lines, 1):
        if len(ln.strip()) < 15:
            continue
        hits = sorted(k for k, rx in REPO_RE.items() if rx.search(ln))
        non_bridge = [h for h in hits if h != "bridge"]
        # An edge candidate needs >=1 non-bridge repo named AND a transfer verb.
        if not non_bridge or not TRANSFER.search(ln):
            continue
        out.append({
            "file": rel, "line": i,
            "repos": hits,
            "n_nonbridge": len(non_bridge),
            "independence_language": bool(INDEP.search(ln)),
            "text": ln.strip()[:400],
        })
    return out

def main():
    cands = []
    for p in sorted(ROOT.rglob("*.md")):
        if ".git" in p.parts:
            continue
        cands.extend(sweep(p))

    # A candidate naming TWO OR MORE distinct non-bridge repos on one line, or one
    # non-bridge repo plus the bridge, is a directed-transfer candidate.
    edges = [c for c in cands if c["n_nonbridge"] >= 1 and len(c["repos"]) >= 2]

    res = {
        "candidates_total": len(cands),
        "edge_candidates": len(edges),
        "with_independence_language": sum(1 for c in cands if c["independence_language"]),
        "by_file": {},
    }
    for c in cands:
        res["by_file"][c["file"]] = res["by_file"].get(c["file"], 0) + 1

    outdir = ROOT / "falsification/A4_independence_dag/results"
    (outdir / "census_raw.json").write_text(json.dumps(cands, indent=1))
    (outdir / "census_summary.json").write_text(json.dumps(res, indent=1))

    print(f"candidates (>=1 non-bridge repo + transfer verb): {res['candidates_total']}")
    print(f"  of those, multi-repo on one line:              {res['edge_candidates']}")
    print(f"  carrying explicit independence language:       {res['with_independence_language']}")
    print(f"\nGATE A4a: >=30 distinct edges required -> "
          f"{'PASS' if res['candidates_total'] >= 30 else 'FAIL (audit has no power)'}")
    print("\ntop files:")
    for f, n in sorted(res["by_file"].items(), key=lambda kv: -kv[1])[:12]:
        print(f"  {n:5d}  {f}")

main()
