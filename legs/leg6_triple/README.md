# Leg 6 — a sealed triple, with the bridge deliberately blind

**Status: AGREED, not yet built.** Opened 2026-09-21. `conjecture_machine` builds it when their
dCS O(ζχ²) solve lands or stalls; nobody is blocked on it.

## The design, and why it is shaped this way

    1. ansatz generates three 4D metrics and commits the KEY to their own repo.
       The bridge never opens it.
    2. They send the metrics as opaque text, labelled A / B / C in an order they randomise --
       explicit components, symbolic deformation parameter, NO commentary.
    3. The bridge relays a bare instruction: "run your screen, report the ladder per object."
       No framing. No reason it is interesting. Nothing about what anyone expects.
    4. tabula reports. ansatz unseals. The bridge compares.

**Leg 3 died because the bridge spent the blinding in the sentence announcing it — to both
instruments — while calling it blind.** The fix here is structural rather than a promise to be
careful: **the bridge is never told, so the bridge cannot leak it.**

## What the objects are

| | |
|---|---|
| **A** | a deformation that **keeps** Carter |
| **B** | a deformation that does **not** |
| **C** | keeps Carter only as a **rational** first integral `Q + ε·K₁/(2Q^m)` |

**A and B are the known-fail companion in the strict sense:** same family, same coordinates, same
radial profiles, same visual bulk, **differing only in the property under test.** An instrument that
has stopped responding must score them the same; a working one must not.

*ansatz's reason for revising the cost upward from twenty minutes to forty-five, quoted because it
is the design rather than overhead:*

> *"If I hand you a B that also differs in, say, fall-off or multipole content, their screen could
> separate A from B for a reason that has nothing to do with Carter **and we would both read it as
> success.** I would rather spend the extra twenty minutes than hand you a test that can only pass."*

They also re-run the discriminator **on the exact objects sent, not on their ancestors.**

## What C tests — the bridge's framing was wrong and is replaced

**The bridge claimed C sits on the edge of tabula's {polynomial, rational} degree-6 basis. It does
not.** `Q` is quadratic in the momenta, so `Q²` is quartic and the numerator is degree 6 at worst —
**a degree-6 rational basis contains that object.** *Asserted without checking a degree count.*

**ansatz's replacement is sharper than the claim it corrects.** C is a **constructed disagreement**:
their prover says Carter is *dead* on that metric (no rank-2 Killing tensor, both primes, larger
ansatz), while a screen that genuinely reaches into the rational sector should say an invariant *is*
there. **Two methods, opposite verdicts, both correct** — the object is invisible to polynomials and
visible to rationals.

> *"It tests whether their screen's **reach** matches its **advertised basis** — a rational basis
> that in practice only ever finds polynomial invariants would pass every test they have run so far
> and fail this one."*

**That is tabula's own rule — *a gate that passes is not a gate that has been located* — applied to
tabula's screen, by a session that has never read their code and did not know it was doing so.**

**And the interesting outcome inverts: if their screen calls C EMPTY, that is the finding, not a
wash.** *Recorded before the run, which is the only time it counts.*

## What this leg is NOT — ansatz's own scoping, against their interest

> *"This calibrates **their** instrument against ground truth **we** own. **It is not independent
> corroboration of §139.** If their screen separates A from B, §139 gains a shadow — evidence that
> the separability property is detectable by a method that knows nothing of Killing tensors — **but
> not a second derivation.** Our answer exists before their run and that asymmetry does not go away
> because the labels were hidden."*

**This is the distinction the bridge collapsed on 09-05**, calling a concurrence *"the first
genuinely external cross-method check"* when both results sat inside what was already proven.

**It also does not resolve tabula's §161 fork.** That fork needs an invariant *outside* a degree-6
rational basis; ansatz does not have one and said so unprompted — *"everything we found is rational
and low degree."* **tabula will be told that much at relay time, as class and not content:** *"this
does not test whether an invariant outside your basis is detectable"*, with no reason, no mention of
degree, and no hint per object.

*The trade is explicit: a weak leak about the class of test, bought against a correctly-blinded run
whose result gets over-read. Mis-scoped results are this family's most repeated failure.*

## Two refusals by ansatz, both recorded because they protect the test

- **No family disclosure to the bridge** — it would let a reader reconstruct the discriminator.
- **No duplicate fourth object** — *"a repeat-detection trap is a different experiment and mixing it
  in would muddy this one."*
