#!/usr/bin/env python3
"""Executable form of the leg design requirement. Prose was not enough.

WHY A GATE AND NOT A PARAGRAPH -- tabula, 2026-09-05:

    "Visibility is a weaker referee than executability, and I would rather be corrected
     by my own suite than by my own prose."

Every rule bought today was filed as prose. Prose is a POTENTIAL referee: it works if
someone reads it. This file exists because writing it is what surfaced the round's worst
error (see JOURNAL: "eleven weeks, no legs" was an inference, never measured, and 33
legs contradicted it).

WHAT IT CHECKS. A leg declares its expected verdict class in LEG.toml, and per tabula's
asymmetry the known-fail companion is MANDATORY for a certify and advisory for an emit:

    "A null is what an instrument says when it has stopped looking; a positive is not.
     Two dead instruments agreeing on a null is the EXPECTED joint failure, because null
     is the default output of both. A broken instrument does not emit a specific closed
     form with matching coefficients."

WHAT THIS GATE DOES NOT CHECK -- tabula, on the day it shipped, and it is the sharpest
thing said about it:

    "leg_gate.py encodes a distinction -- certify-vs-emit -- that we settled by ARGUMENT
     this afternoon and have never tested against a case designed to break it. It is a
     gate whose own criterion is an inference, and its known-fail control tests that the
     gate FIRES, not that the criterion is RIGHT."

The four-state control below proves the implementation moves. It says nothing about
whether "companion mandatory for certify, advisory for emit" is the correct rule. That
rule rests on one argument -- a stalled instrument's default output is a null, not a
specific closed form with matching coefficients -- and on one supporting case (tabula's
K0 rediscovering Carter at cosine 0.975, held-out 3.1e-26, which no stalled engine could
have produced). ONE ARGUMENT AND ONE CASE.

    So when a leg surprises you, revisit the CRITERION first, not the implementation.
    The implementation has a control. The criterion has only an afternoon's agreement
    between two parties who wanted it to be true.

AND THE STRONGER FORM, which tabula proved on themselves ninety minutes after warning me
-- they built the same kind of gate, gave it a known-fail control that passed 5/5, and
then it failed the real repository. It flagged a missing artifact whose citation existed
only to record that the file had been RENAMED. The citation was correct and the absence
was the entire point of it. The control passed while the rule was wrong.

    A KNOWN-FAIL CONTROL TESTS THE MECHANISM. ONLY CONTACT WITH REAL DATA TESTS THE RULE.

    The control is built from the same understanding as the thing it checks, so it is
    structurally blind to whatever that understanding omits. It can prove an instrument
    responds. It cannot prove the instrument is asking the right question.

THE STANDING WARNING FOR THIS FILE SPECIFICALLY. leg_gate.py has had NO such contact. Its
only subject is leg3_cross_instrument, which is retired -- so the retired branch returns
early and the certify/emit rule has never actually been applied to a live leg. The 4-state
control below is the whole of its evidence, and by the paragraph above that is evidence
about the mechanism only.

    The first time this gate disagrees with a real leg, the disagreement is evidence
    about the gate, not about the leg. Do not "fix" the leg to satisfy it.

WHY THIS ONE MAY BLOCK WHERE THE AUDIT SWEEP MAY NOT: it has no triage cost. A leg either
declares a companion or it does not -- no judgement call, so no hit rate to erode. Scoped
to legs/ only; the 41 pre-existing top-level leg dirs predate the rule and are not
retro-judged by it.
"""
import sys, pathlib, re

LEGS = pathlib.Path(__file__).resolve().parent.parent / "legs"

def check(leg):
    out, cfg = [], leg / "LEG.toml"
    if not cfg.exists():
        return [f"{leg.name}: no LEG.toml -- expected verdict class undeclared"]
    txt = cfg.read_text()
    m = re.search(r'^\s*expected\s*=\s*"(certify|emit)"', txt, re.M)
    if not m:
        return [f'{leg.name}: LEG.toml declares no expected = "certify"|"emit"']
    if re.search(r'^\s*retired\s*=\s*true', txt, re.M):
        return []
    comp = re.search(r'^\s*companion\s*=\s*"([^"]+)"', txt, re.M)
    if m.group(1) == "certify":
        if not comp or not comp.group(1).strip():
            out.append(f"{leg.name}: expected=certify with NO known-fail companion. A null "
                       f"is the default output of a stalled instrument, so a concurrence "
                       f"would be unfalsifiable.")
        elif not (leg / comp.group(1)).exists():
            out.append(f"{leg.name}: companion {comp.group(1)!r} does not exist")
    return out

def main():
    if not LEGS.is_dir():
        print("  leg gate: no legs/ directory"); return 0
    legs = sorted(p for p in LEGS.iterdir() if p.is_dir())
    fails = [f for leg in legs for f in check(leg)]
    if fails:
        print(f"  leg gate: {len(fails)} FAILING across {len(legs)} leg(s)")
        for f in fails: print(f"    ! {f}")
        return 1
    print(f"  leg gate: {len(legs)} leg(s) OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
