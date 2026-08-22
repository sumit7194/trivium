#!/usr/bin/env python3
"""Run today's checks mechanically, on any repo, by any session.

WHY THIS EXISTS. PROTOCOL.md is over 1000 lines and every entry is a thing someone
learned the expensive way. quantum's observation at the end of the day is the reason
this file exists rather than another entry:

    Every one of today's failures was DEFENDED BY REASONING at the moment it was made.
    Never an absence of thought -- thought terminating on a plausible argument instead
    of a check. Which is why every durable fix has been SYNTACTIC OR MECHANICAL: an
    assert, a control run, a trigger word, a null distribution, a stated correspondence.

Prose in a long file is retrievable only by someone who remembers it applies. A grep is
cued by the text. So: the triggers, runnable.

    python3 audit_sweep.py /path/to/repo

EVERY CHECK HERE PRODUCES FALSE POSITIVES and says so per-hit. That is deliberate --
the "independent" sweep found 1 real hit in ~12, and the buried-caveat sweep found 2 in
6. A check that needs triage is still worth running; a check that CANNOT fire is not.

    *** THOSE TWO RATIOS ARE NOT COMPARABLE AND SHOULD NOT BE READ TOGETHER. ***
    (quantum, sharpening a weaker caveat of mine.) "2 real in 28" and "1 real in 12" are
    measurements of DIFFERENT CHECKS against DIFFERENT CORPORA, each taken on the repo
    that produced the instance the check was derived from -- the most favourable possible
    sample. They are closer to two anecdotes than to two data points, and REPORTING THEM
    IN THE SAME UNITS IS WHAT MAKES THEM LOOK COMPARABLE. Do not average them, do not
    quote either as a property of a check, and be aware that presenting them side by side
    in a fixed-width block -- as this comment does -- is itself the invitation.

    And the checks themselves are single-instance generalisations. The enumeration
    trigger below is the proof: derived from one real error, its first implementation
    returned 171 hits and was useless. It was the sixth check written and the first one
    tested against a second situation. THE OTHER FIVE HAVE NOT BEEN.
"""
import re, subprocess, sys
from pathlib import Path

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout

def rel(p, root): return str(Path(p).relative_to(root))

def check_independent(root, docs):
    """quantum: a gate asserted 'two independent extractions agree' where both ran on
    the same array. bridge: G3 called two Richardson pairs independent; they shared a
    point. TRIAGE: 'code-independent', 'independently confirmed by X' are usually fine;
    what matters is a claim that two things sharing no inputs agree."""
    hits = []
    for f in docs:
        for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            if re.search(r"\bindependen", line, re.I) and not re.search(
                    r"code-independen|method-independen|not independent", line, re.I):
                hits.append((rel(f, root), i, line.strip()[:110]))
    return hits

def check_absorb(root, docs):
    """A fitted parameter admitting in prose that it swallows an unmodelled term. Found
    M2's 'the residual drift is absorbed by the constant c'. quantum's sharpening: the
    word finds the ADMISSION, and THE SENTENCE AFTER IT is where the unexamined defence
    lives -- so this prints the following line too."""
    hits = []
    for f in docs:
        lines = f.read_text(errors="ignore").splitlines()
        for i, line in enumerate(lines):
            if re.search(r"\babsorb|fold(ed|s)? into|lumped|soaked up", line, re.I):
                nxt = lines[i+1].strip()[:90] if i+1 < len(lines) else ""
                hits.append((rel(f, root), i+1, line.strip()[:90], nxt))
    return hits

def check_silent_shell(root):
    """`cmd && echo ok` is silent on failure, and a check that produces no output on
    failure is indistinguishable from one that produces no output on success. This cost
    bridge a phantom announcement: a heredoc never ran, `ls file && echo written`
    printed nothing, and the absence of an error was read as success."""
    out = sh("grep", "-rn", "--include=*.sh", "--include=*.zsh", "&& echo", str(root))
    hits = [l for l in out.splitlines() if "|| echo" not in l]
    # A CHECK THAT GREPS FOR A PATTERN FLAGS THE COMMENT EXPLAINING WHY THAT PATTERN IS
    # BAD. Running this on the coordination directory returned exactly one hit: the
    # comment inside bridge_pulse_stop.sh documenting the silent-failure bug it fixed.
    # Documenting a fix inline creates a permanent false positive in its own checker --
    # so strip comment lines, and accept that this now cannot see a `&& echo` a author
    # has commented out. Stated rather than silently traded away.
    return [l for l in hits if not re.search(r":\s*#", l)]

def check_buried_caveat(root, docs):
    """A RETRACTION below the fold is a hedge: discoverable, honest, invisible to the
    reader it can mislead. TRIAGE: a 'what this does and does not establish' section at
    70% is correct structure. Only a retraction of the headline is a hit."""
    hits = []
    for f in docs:
        lines = f.read_text(errors="ignore").splitlines()
        if not lines: continue
        for i, line in enumerate(lines, 1):
            if re.search(r"withdraw|retract", line, re.I):
                pct = 100 * i // len(lines)
                if pct > 15:
                    hits.append((rel(f, root), i, len(lines), pct, line.strip()[:80]))
                break
    return hits

def check_unstated_enumeration(root, docs):
    """quantum's trigger, derived from bridge's own error. bridge wrote "the only leg of
    31 with neither code nor artifacts" -- a sweep of ONE SUBDIRECTORY reported as a
    repo-wide result. Eight further directories qualified.

        "The only one of 31" is a satisfying sentence and I never asked what the 31 was.

    Not a wrong measurement: a CORRECT measurement over a set whose boundary was never
    checked. And the count is what makes it sound audited -- a bare "the only one" invites
    less scrutiny than a number does, because the number implies someone enumerated.

    TRIAGE: fine if the enumeration is stated nearby. A hit is a superlative or a
    universal whose SET is not defined in the same sentence."""
    # FIRST VERSION WAS TOO BROAD AND IS RECORDED AS A FAILURE OF THIS TRIGGER. It
    # matched "the only|all N|every one of|N of N|the first|the sole" and returned 171
    # hits on one repo -- against quantum's usable threshold, "reading them took under a
    # minute". Most were legitimate ("all 8 symmetries of the square", "the first move"),
    # with their sets defined right there. A trigger derived from ONE instance does not
    # automatically generalise, and a check nobody will read is as inert as one that
    # cannot fire.
    #
    # Narrowed to the shape the original error actually had: a SUPERLATIVE BOUND TO A
    # COUNT -- "the only one of 31", "1 of 31", "none of the 12". The count is what makes
    # it sound audited, and it is the part that was wrong.
    pat = re.compile(r"\b(the only|the sole|none)\b[^.]{0,40}\b(of|in|among)\b\s*"
                     r"(the\s+)?\d+|\b\d+\s+of\s+(the\s+)?\d+\b", re.I)
    hits = []
    for f in docs:
        for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            if pat.search(line):
                hits.append((rel(f, root), i, line.strip()[:110]))
    return hits


def check_unproduced_numbers(root):
    """quantum's 16: for every number in a doc, can committed code produce it? Weak
    proxy -- flags study dirs holding a findings doc but no artifact at all."""
    hits = []
    for d in sorted(p for p in root.rglob("*") if p.is_dir() and ".git" not in p.parts):
        docs = list(d.glob("FINDINGS*.md"))
        if not docs: continue
        arts = [p for p in d.rglob("*") if p.suffix in (".json", ".log", ".npz", ".csv")]
        if not arts:
            hits.append((rel(d, root), len(list(d.rglob("*.py")))))
    return hits

def main(root):
    root = Path(root).resolve()
    docs = [p for p in root.rglob("*.md") if ".git" not in p.parts]
    print(f"audit_sweep on {root}   ({len(docs)} docs)\n")

    h = check_independent(root, docs)
    print(f"[1] 'independent' claims — {len(h)} hits (expect mostly false positives)")
    for f, i, t in h[:10]: print(f"      {f}:{i}  {t}")
    if len(h) > 10: print(f"      ... {len(h)-10} more")

    h = check_absorb(root, docs)
    print(f"\n[2] fitted parameter absorbing an unmodelled term — {len(h)} hits")
    for f, i, t, nxt in h[:6]:
        print(f"      {f}:{i}  {t}")
        if nxt: print(f"          NEXT LINE (where the defence lives): {nxt}")

    h = check_silent_shell(root)
    print(f"\n[3] shell checks silent on failure (`&& echo` with no `|| echo`) — {len(h)} hits")
    for l in h[:6]: print(f"      {l.strip()[:120]}")

    h = check_buried_caveat(root, docs)
    print(f"\n[4] retraction below the fold — {len(h)} hits")
    for f, i, tot, pct, t in h[:8]: print(f"      {f}:{i}/{tot} ({pct}% in)  {t}")

    h = check_unstated_enumeration(root, docs)
    print(f"\n[5] superlative/universal with an unstated set — {len(h)} hits")
    for f, i, t in h[:8]: print(f"      {f}:{i}  {t}")
    if len(h) > 8: print(f"      ... {len(h)-8} more")

    h = check_unproduced_numbers(root)
    print(f"\n[6] findings doc with NO artifact of any kind — {len(h)} hits")
    for d, npy in h: print(f"      {d}   ({npy} .py files)")

    print("\nNo check here can certify anything. Each needs triage, and each is cued by\n"
          "text rather than by recognising the situation — which is the only reason any\n"
          "of them fire on their own author.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
