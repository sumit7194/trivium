# The scope manifest — required beside any object that crosses a repo boundary

**Why this exists.** In one night `../conjecture_machine` shipped five objects, each correct, each
missing a different scope statement: the ε range, the non-uniqueness, relative-vs-absolute drift,
the H convention, and the χ truncation. **Their own diagnosis is the reason this file is a form and
not advice:**

> *"The pattern is not that I get scope wrong; it is that I DO NOT WRITE IT DOWN, and it is invisible
> to me at exactly the moment the object is finished and feels done."*

**A missing scope statement is invisible from both ends.** The sender cannot see it because the
object is complete in their own frame, where every assumption is ambient. The receiver cannot see it
because absence has no signature — *a truncated object and an exact one are the same characters on
the page.* Nothing in either party's review catches it, which is why it is the fifth instance rather
than the first.

**This is a form because prose decayed.** All five omissions happened while both parties had written
rules about stating assumptions. *The writing is not the artefact; the gate is.*

---

## The eight fields. An object ships with all eight or it does not ship.

    OBJECT        what it is, in one line, naming the ACTUAL mathematical object --
                  not the role it plays. "chain 4, a basis vector of the rank-2
                  nullspace" and NOT "the Carter direction".
                  << the error that cost this family a night: a basis vector named
                     after the invariant it was expected to be >>

    EXACT IN      the parameters in which this object is exact, with no truncation.

    TRUNCATED IN  every other parameter, WITH THE ORDER. If an object is exact in eps
                  and stops at chi^2, say so and say chi^2. An object with no
                  truncation line is read as exact in everything, and that reading
                  will be wrong.

    VALID RANGE   the range of each parameter where the truncation is usable, with the
                  size of the first neglected term at the boundary.
                  << chi = 0.6 gives chi^4 = 0.13: a 13% truncation held FIXED while
                     the exact parameter was swept to zero. Nobody asked. >>

    VALID RANGE   ...and it is not only the expansion parameters. A correction can
                  diverge in a COORDINATE, shrinking its radius of validity in space.
                  << K1 has a genuine simple pole at the horizon, r = 2M -- residue
                     64*chi^2*P_t^2*y^2, verified, not cancelled. So first-order theory
                     fails near the horizon and the expansion is uniform only for
                     eps << (r - 2M). This was visible in the object's own denominator
                     from the moment it shipped. Three parties read that denominator
                     for other reasons without asking what a pole at r=2 meant. It was
                     the SIXTH scope statement of the night and the first that nobody
                     knew -- the other five were things the author knew and had not
                     written down. A form catches both kinds; a habit of stating what
                     you know catches only one. >>

    CONVENTIONS   every definition that could differ between repos, spelled out:
                  is H halved? is Q Carter or total angular momentum? what are the
                  coordinates, the signature, the mass normalisation?
                  << L^2 read as Q cost -8*P_phi^2 in a header written to fix an
                     earlier mislabelling >>

    UNIQUE?       is this object unique, or one representative of a family? If a
                  family, say what the freedom is. A receiver testing a specific
                  representative against a general claim will get a real answer to
                  the wrong question.

    DOMAIN        the set on which the claim holds, AND whether that is the set the
                  receiver will measure on. A result can be exactly true globally
                  and operationally empty on the region actually sampled.
                  << "K1 has a pole at r=2M, every function in the basis is analytic
                     there, therefore K1 is not in the span at any degree" -- correct,
                     proved, and irrelevant to a screen fitting on r in [5.1, 9.1],
                     where 1/(r-2) is ANALYTIC and the existing basis reproduces it
                     to 4.2e-05 relative. Adding it made all three objects WORSE,
                     which is the conditioning cost of a redundant column. The
                     algebra was right, the verification was right, the conclusion
                     followed, and the domain it applied to was not the domain
                     anyone was working on. A CORRECT THEOREM ABOUT THE WRONG SET. >>

    NOT CHECKED   what the sender did NOT verify, stated positively. Absence of a
                  claim is not a claim of absence, and the receiver cannot infer this
                  field from any of the others.

---

## The two lines that make it a gate rather than a checklist

**Every automated check reports, per level or per order, whether it was INFORMATIVE or VACUOUS, and
refuses to return PASS unless at least one level was informative.** *Bought at full price: a check
printed `chi^0 residual zero: True / chi^1 residual zero: True` while the deformation was pure χ² and
the correction carried χ² — it compared 0 to 0 and called it success. The crash that exposed it
landed one level early by luck.*

**A receiver that cannot fill in all eight fields from what it was sent does not run the test.** It
asks. *Every one of tonight's five omissions was recoverable in one message and cost hours instead.*

---

## Why this is the one rule worth making mechanical

The night produced three faults that ordinary review cannot see:

    dead guard      a failing mechanism returns what "nothing to report" returns
    failure-as-value a failing FUNCTION returns a value that looks like an answer
    vacuous level   a WORKING mechanism returns a true PASS that certifies nothing

**All three are invisible to a reader and all three are trivial for a form to catch**, because a form
asks a question the author would not have thought to ask. That is the entire argument.
