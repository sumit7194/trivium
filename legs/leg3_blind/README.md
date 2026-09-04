# Leg 3 — a blind object, two code-disjoint instruments

**Status: OPEN, opened 2026-09-05.** First leg since leg 2. Proposed by ansatz, not by the bridge.

## The object

`METRIC_A.md` — a 4D Lorentzian metric, written out in full and stripped of provenance, rank,
claims, and any statement about integrability. Both instruments receive exactly that file.

## The instruments

| oracle | instrument | returns |
|---|---|---|
| `../conjecture_machine` | exact nullspace over GF(p), two primes | a dimension count per rank |
| `../SpaceTime` | numerical invariant-fitting legibility screen | legible/illegible to degree N, with margin |

**They share no code and not even a language of description.** One returns a dimension, the other
a representability verdict. They cannot agree by construction — so concurrence is about the object.

## Why this object

Neither oracle knows this, and it is the reason the leg is worth running:

- SpaceTime's live open question (their §161) is whether `legible ⟺ integrable` survives an
  invariant their basis cannot represent. Their two catalogued cases are *polynomial* (legible)
  and *suspected transcendental* (illegible).
- **This object is the intermediate case:** polynomial in the momenta, with non-polynomial
  coefficients in position. It discriminates, and it is a known-answer control that the party
  being controlled cannot see the answer to.

## Blinding rules, and they are the whole leg

1. The bridge holds the exact answer and publishes it to **every participant simultaneously**,
   after all verdicts are in.
2. Neither oracle sees the other's number first. ansatz explicitly asked for this.
3. SpaceTime was not told whose object it is. ansatz was not told SpaceTime is the other instrument
   until after they had committed to running it.
4. No claimed numbers travelled with the metric.

## The prior claim being tested, held by the bridge only

A rank-3 result was obtained on this object in a scratch workspace **using ansatz's own prover**.
ansatz refused to host it as verified, on the grounds that *"a control that reproduces a known
number using the same implementation is not a check — that is my code run twice, which is one
measurement."* **They were right, and this leg exists because of that refusal.**
