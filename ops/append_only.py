#!/usr/bin/env python3
"""Find sections that grew repeatedly and never shortened -- nobody re-read while adding.

quantum's detector, and it is a partial answer to a claim I made that the stranger-read
cannot be mechanised. It cannot: this reads nothing and cannot tell a legitimately
accumulating section (a reference list, a changelog) from a buried one.

WHAT IT DOES IS NARROW WHERE TO LOOK, which matters because the alternative is
"re-read everything periodically", and that is a resolution rather than a check.

    A section that grows repeatedly and never once shortens is one nobody re-read
    while adding to it.

On their own repo it flagged two sections. They had already consolidated one. The other
they had never opened -- and it held the constant's stability stated THREE DIFFERENT
WAYS, two of them superseded by a result added at the top the same evening.

    python3 append_only.py <repo> [since]
"""
import re, subprocess, sys
from collections import defaultdict
from pathlib import Path

def sh(*a, cwd=None):
    return subprocess.run(a, capture_output=True, text=True, cwd=cwd).stdout

def sections(text):
    """Map heading -> non-blank line count.

    TWO BLIND SPOTS FOUND BY RUNNING THIS ON A REPO WHOSE AUTHOR APPENDS DIFFERENTLY.
    quantum's failure mode grows an existing section; bridge's ADDS NEW SECTIONS, so a
    purely within-section detector returned ZERO hits on a file that had grown from ~200
    to 366 lines the same day. Not clean -- invisible.

    And bridge's actual defect was in the PREAMBLE before the first heading (23 of the
    first 30 lines were qualification with no statement of the result), which a
    heading-keyed map does not track at all.

    So: the preamble is a pseudo-section, and the caller also watches SECTION COUNT.
    A detector shaped around one author's habit does not see another's.
    """
    out, cur, n = {}, "(preamble, before the first heading)", 0
    for line in text.splitlines():
        if re.match(r"^#{1,3} ", line):
            if cur: out[cur] = n
            cur, n = line.strip(), 0
        elif cur and line.strip():
            n += 1
    if cur: out[cur] = n
    return out

def main(repo, since="8 hours ago"):
    repo = Path(repo).resolve()
    revs = sh("git", "log", "--format=%H", f"--since={since}", cwd=repo).split()[::-1]
    if len(revs) < 2:
        print(f"  fewer than 2 revisions since '{since}' -- nothing to compare"); return
    files = {f for r in revs for f in
             sh("git", "show", "--name-only", "--format=", r, cwd=repo).split()
             if f.endswith(".md")}
    print(f"  {len(revs)} revisions since '{since}', {len(files)} markdown files touched\n")
    flagged = 0
    for f in sorted(files):
        hist = defaultdict(list)
        for r in revs:
            txt = sh("git", "show", f"{r}:{f}", cwd=repo)
            if not txt: continue
            for h, n in sections(txt).items():
                hist[h].append(n)
        for h, seq in hist.items():
            if len(seq) < 3: continue
            grows = sum(1 for i in range(1, len(seq)) if seq[i] > seq[i-1])
            shrinks = sum(1 for i in range(1, len(seq)) if seq[i] < seq[i-1])
            if grows >= 3 and shrinks == 0:
                flagged += 1
                print(f"  APPEND-ONLY  {f}")
                print(f"     {h[:78]}")
                print(f"     {seq[0]} -> {seq[-1]} lines, {grows} growth steps, 0 shrinks\n")
    # SECTION-COUNT GROWTH: the append-new-sections failure mode.
    for f in sorted(files):
        counts = []
        for r in revs:
            txt = sh("git", "show", f"{r}:{f}", cwd=repo)
            if txt: counts.append(len(sections(txt)))
        if len(counts) >= 3:
            grows = sum(1 for i in range(1, len(counts)) if counts[i] > counts[i-1])
            shrinks = sum(1 for i in range(1, len(counts)) if counts[i] < counts[i-1])
            if grows >= 3 and shrinks == 0:
                flagged += 1
                print(f"  SECTIONS-ONLY-ADDED  {f}")
                print(f"     {counts[0]} -> {counts[-1]} sections, {grows} additions, 0 removals")
                print(f"     nothing was ever merged or removed -- the document only accreted\n")
    if not flagged:
        print("  no append-only sections found")
    print("  This cannot tell an accumulating section from a buried one. It tells you\n"
          "  where to spend a re-read, and the judgement is still irreducible.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".",
         sys.argv[2] if len(sys.argv) > 2 else "8 hours ago")
