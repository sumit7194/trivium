#!/usr/bin/env python3
"""A2 — mechanical census of every wall logged in the family's own documents (gate A2a).

    python3 wall_census.py

Gates frozen in ../PREREGISTRATION.md. This script ENUMERATES ONLY — it assigns no labels. Classification
(A2b) is done by hand against the frozen definitions and recorded in FINDINGS.md, precisely so that the
sample cannot be curated toward the auditor's stated prior.

Sweeps every *.md in the repo for wall-language, emits one record per hit with file:line + context, and
groups them by the document that logged them.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

# parents[3] = the REPO ROOT. parents[2] is falsification/ — using it silently swept ~1/3 of the corpus
# (missing JOURNAL/CAPSTONE/THE_BRIDGE/BACKLOG/the ledgers/every leg*/ dir) while still passing the ≥10 gate.
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent.parent / "results"

# Wall-language. The family's own term is "wall"; the rest catch walls logged under other words.
PATTERNS = [
    (r"\bwall(s|ed)?\b", "wall"),
    (r"\bundecidable\b", "undecidable"),
    (r"\bunreachable\b", "unreachable"),
    (r"\binfeasible\b", "infeasible"),
    (r"\bout of reach\b|\bbeyond (our|any) reach\b", "out-of-reach"),
    (r"\bPARKED\b|\bparked\b", "parked"),
    (r"\bblocked (on|by)\b", "blocked"),
    (r"\bcannot (be )?(cross|resolve|distinguish|determine|decide)", "cannot"),
    (r"\bnot (spectrally )?determined\b", "not-determined"),
    (r"\bin principle\b", "in-principle"),
]

# Boilerplate to drop: the ledger's own G7 statement recurs in many files and is not itself a wall.
NOISE = re.compile(r"instrument-relative|G7\b", re.I)


def main():
    files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    hits, by_file = [], defaultdict(int)
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        try:
            lines = p.read_text(errors="replace").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            tags = [t for rx, t in PATTERNS if re.search(rx, line)]
            if not tags:
                continue
            ctx = line.strip()
            hits.append({"file": rel, "line": i, "tags": tags,
                         "g7_boilerplate": bool(NOISE.search(ctx)),
                         "context": ctx[:400]})
            by_file[rel] += 1

    substantive = [h for h in hits if not h["g7_boilerplate"]]
    print(f"A2a — mechanical wall census (enumeration only; NO classification here)\n")
    print(f"  markdown files swept          : {len(files)}")
    print(f"  raw wall-language hits        : {len(hits)}")
    print(f"  minus G7-boilerplate lines    : {len(substantive)}")
    print(f"  documents containing hits     : {len(by_file)}\n")

    print(f"  top documents by hit count:")
    for f, c in sorted(by_file.items(), key=lambda kv: -kv[1])[:14]:
        print(f"    {c:4d}  {f}")

    tagcount = defaultdict(int)
    for h in substantive:
        for t in h["tags"]:
            tagcount[t] += 1
    print(f"\n  hits by language tag:")
    for t, c in sorted(tagcount.items(), key=lambda kv: -kv[1]):
        print(f"    {c:4d}  {t}")

    OUT.mkdir(exist_ok=True)
    (OUT / "wall_census.json").write_text(json.dumps(
        {"files_swept": len(files), "raw_hits": len(hits),
         "substantive_hits": len(substantive), "by_file": dict(by_file),
         "by_tag": dict(tagcount), "hits": substantive}, indent=1))
    print(f"\n  wrote results/wall_census.json  ({len(substantive)} records for hand-classification)")
    print(f"  NOTE: raw hits are LINES, not distinct walls — many lines describe the same wall.")
    print(f"  A2b de-duplicates into distinct walls by hand, against the frozen definitions.")


if __name__ == "__main__":
    main()
