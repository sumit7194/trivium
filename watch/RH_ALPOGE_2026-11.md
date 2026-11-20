# Watch: the claimed proof of the Riemann Hypothesis (Alpöge with Claude), started 2026-11-21
Sumit asked the Bridge to read the primary source and track the verification. Rule (memory ai-in-physics-watch):
report what is actually checked, and its status, not commentators' opinions.

## Primary source (read in full, 2026-11-21 00:20 IST)
https://alpo.ge/remark.pdf: a 4-page note, "Remark", first person, by Levent Alpöge (Anthropic). Text extracted
locally with pdftotext.

**Claim.** "I believe I have, working with Claude, discovered a proof of the Riemann Hypothesis."
- It extends to GRH. ERH is expected "with more time".
- "Formalized the arguments without assumptions" in Lean, released only as Lean: lean.tar.gz.part01 … part14. The
  note gives no theorem statement, toolchain or axiom list.

**Idea, as described.**
- A descendant of Stepanov's function-field argument.
- The multiplicity is supplied by a CHAIN of theta lifts between definite unitary groups. Each lift adds
  multiplicity, and the chain length is ~√X for a von Mangoldt sum of length X (Claude's suggestion).
- The ingredients listed include:
  - GGP/Bessel periods, Rallis seesaw;
  - a relative trace formula;
  - an Iwasawa tower (choosing it uses Behrend);
  - Chowla–Selberg, Siegel mass, the Bost slope inequality;
  - a "significant weakening of Vandiver".
- A 20-step timeline, 6 Oct to 16 Nov 2026, with GRH on 16 Nov.

**Author's own caveats.**
- The argument is "incredibly long". A full human-readable write-up would be a 250,000+ page document, which he
  calls "slop", so he posts only Lean.
- He has not mastered parts (higher-rank automorphic forms), and parts of the timeline paraphrase an AI summary that
  "might make zero sense".
- He expects big simplifications, and intends to understand it and write it properly.

**Side claims, unexplained.** He says that OpenAI's Ehrhart equality-case work made him "understand Navier–Stokes was
going to fall". Treat this as a remark, not a claim with evidence.

## Verification status (as of 2026-11-21 00:30 IST)
- **Lean compiles:** according to Scientific American (20 Nov), Andrew Sutherland (MIT) says he independently compiled
  it. That is the only outside compile report seen so far. OfficeChai said nobody had checked yet; those two reports
  conflict.
- **Does the final Lean theorem state RH/GRH with correct definitions?** NOT YET checked by any expert we have seen.
  A secondhand report says Elliot Glazer noted on X that the formal statement is GRH; this was not read at source.
- **No sorry / no non-standard axioms:** not yet reported by anyone independent.
- **Human understanding:** none yet, by the author's own account (Tao's "proof indigestion", live).

## What would settle it (in order)
1. An independent build, with `#print axioms` on the final theorem showing only the standard axioms (propext,
   Classical.choice, Quot.sound).
2. Experts confirm that the final statement, and the definitions it rests on (ζ / L-functions, zeros, critical
   line), match RH/GRH. This is the step most likely to hide problems.
3. A human-readable account that number theorists can check.

## Log
- **2026-11-21 00:30:** note read; status recorded above.
