#!/usr/bin/env python3
"""A3 — mechanical census of mechanism claims in the family's banked findings (gate A3a).

    python3 mechanism_census.py

Gates frozen in ../PREREGISTRATION.md. ENUMERATES ONLY — assigns no labels. Classification (A3b) is by hand
against the frozen definitions, so the sample cannot be curated toward the auditor's disclosed prior.

A mechanism claim is a causal/explanatory assertion (WHY a thing is so) as opposed to a measurement (THAT it
is so). Two of ours were retracted in one day; A3 asks how many more there are.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # repo root (A2's parents[2] bug: do not repeat it)
OUT = Path(__file__).resolve().parent.parent / "results"

CONNECTIVES = [
    (r"\bbecause\b", "because"),
    (r"\bthe reason\b", "the-reason"),
    (r"\bmechanism\b", "mechanism"),
    (r"\bexplains?\b|\bexplanation\b", "explains"),
    (r"\bdue to\b", "due-to"),
    (r"\bhence\b", "hence"),
    (r"\btherefore\b", "therefore"),
    (r"\bwhy\b", "why"),
    (r"\bsince\b", "since"),
]
# structural position markers -> a hit here is a candidate LOAD-BEARING claim
TITLE = re.compile(r"^#\s|^##\s+Result in one line|^>\s*##", re.I)
VERDICT = re.compile(r"VERDICT|Result in one line|^#\s", re.I)


def main():
    targets = sorted(ROOT.glob("falsification/*/FINDINGS.md"))
    targets += [ROOT / "FALSIFICATION_LEDGER.md", ROOT / "FALSIFICATION_V2.md"]
    targets = [p for p in targets if p.exists() and "A3_mechanism_audit" not in p.parts]

    hits, by_file, by_tag = [], defaultdict(int), defaultdict(int)
    for p in targets:
        rel = p.relative_to(ROOT).as_posix()
        lines = p.read_text(errors="replace").splitlines()
        # a claim is "near a headline" if it sits in the first 25 lines or under a title/verdict marker
        for i, line in enumerate(lines, 1):
            tags = [t for rx, t in CONNECTIVES if re.search(rx, line, re.I)]
            if not tags:
                continue
            near_head = i <= 25 or bool(TITLE.search(line)) or bool(VERDICT.search(line))
            hits.append({"file": rel, "line": i, "tags": tags,
                         "near_headline": near_head, "text": line.strip()[:300]})
            by_file[rel] += 1
            for t in tags:
                by_tag[t] += 1

    print("A3a — mechanical mechanism-claim census (enumeration only; NO classification here)\n")
    print(f"  findings documents swept   : {len(targets)}")
    print(f"  candidate mechanism claims : {len(hits)}")
    print(f"  of which near a headline   : {sum(1 for h in hits if h['near_headline'])}"
          f"   (candidate LOAD-BEARING)")
    print(f"  documents with hits        : {len(by_file)}\n")

    print("  top documents:")
    for f, c in sorted(by_file.items(), key=lambda kv: -kv[1])[:14]:
        print(f"    {c:4d}  {f}")
    print("\n  by connective:")
    for t, c in sorted(by_tag.items(), key=lambda kv: -kv[1]):
        print(f"    {c:4d}  {t}")

    OUT.mkdir(exist_ok=True)
    (OUT / "mechanism_census.json").write_text(json.dumps(
        {"docs_swept": len(targets), "candidates": len(hits),
         "near_headline": sum(1 for h in hits if h["near_headline"]),
         "by_file": dict(by_file), "by_tag": dict(by_tag), "hits": hits}, indent=1))
    print(f"\n  wrote results/mechanism_census.json ({len(hits)} candidates for hand-classification)")
    print(f"  NOTE: candidates are LINES; several lines may express one claim. A3b de-duplicates by hand.")


if __name__ == "__main__":
    main()
