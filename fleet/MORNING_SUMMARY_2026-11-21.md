# Morning summary, 2026-11-21 (updated ~05:45)

## Short version
- **Gemini Neon is worth using, with checking.** It solved real fleet gaps overnight. It is excellent on well-posed,
  computation-heavy steps. Its "SURE" labels on general claims failed twice. Every output was checked by the Bridge,
  ansatz or Cuspis before being trusted.
- **Only Kerr moved a lot:**
  - the last lemmas are proved;
  - the single-centre case was re-derived from scratch;
  - the **"invisible family" now has a proof**, for every Kerr spin, with its core checked to about 1e−11 by two
    independent codes.
- **Non-rational data (K5):** real progress. Curzon–Chazy is proved non-integrable by a new route (as far as we can
  tell). The universal case is narrowed to a precise residual class.
- **Cuspis's δκ crux** is narrowed to one well-posed question. Cuspis paused cleanly; a decision is needed.
- **tabula's training tests** found a real flaw (the loss's boundary data) and a real tooling bug (a guard that never
  fired). §206 is running now.

## Results that held up (all independently checked)
| What | Who | Check |
|---|---|---|
| Three remaining Only-Kerr lemmas | Neon T6 | Bridge V25-C exact |
| Single-centre case from scratch (lower-axis trick plus classification) | Neon T3 + T9 | Bridge V26-E; matches our V26 |
| Invisible family: proof of non-integrability | Neon T8 | Bridge V26-F; ansatz 50-digit (V26-H): agreement ~1e−11 at 3 energies; group step basis-free |
| The same for every Kerr spin a | Neon T11 | Bridge V26-G exact; ansatz review (one gap: k = 4, being tested) |
| Allowed k-range (−∞, 30/7) proved for all spins | Neon T14 | Bridge V26-I: representation matches to 1e−15; wall crossing independently confirmed |
| Curzon–Chazy: SL2 at every energy (hypergeometric) | Neon T16 | Bridge V27-A exact |
| Literature map (16 papers) | Neon T18 | all arXiv IDs verified; one new prior-art paper (Kokkinos 2026) |

## Caught errors (all on record)
- **Neon:**
  - two false "SURE" claims (T10 (e), T12 group test), both corrected after counterexamples;
  - a sign typo in a written formula (T8);
  - a factor-2π mismatch, flagged and under check (T15).
- **Bridge:** four registration slips in tonight's checks (labelling, a tolerance, a control, a clause domain). All are
  recorded as FAIL-as-registered with labelled diagnostics; every underlying Neon claim held. A stronger mechanism is
  adopted: pre-run every control, and match every clause to the claim's own domain.
- **tabula:** a memory guard that always reported success, so its "stop if failed" checks never fired. Fixed and
  proven with a deliberate test.

## Decisions for you
1. **Cuspis: Fable or not?** The last δκ question (growth of Σ̃′ along Im α) is compact. Cuspis can resume with Opus
   from its written spec, or you can approve a Fable brief. Neon's lead (T15/T17) is waiting for Cuspis.
2. **Only Kerr outreach.** Remaining before any outside contact:
   - ansatz's k = 4 test (DONE: not an exception at E = 0.8, spin 0.6);
   - a second reader of the T11 loop construction;
   - re-running T14's interval certificate;
   - our own novelty search.
3. **tabula §206** (fixing the loss's boundary data): results due this morning; then decide on the weighting test.

## Still pending
- Quantum's Melnikov stage-2 verdict (~10:00).
- ansatz's k = 4 test: DONE, not an exception (E = 0.8, spin 0.6).
- Neon T17 (C₊ normalisation and multiple-reflection growth, for Cuspis).
- tabula §206.

## Notes
- The Mac stayed within its limits. One guard stop at 05:08 was caused by Chrome (Gemini pages ~6 GB), not by
  tabula's job. Finished Gemini tabs are now closed (conversation URLs are in NEON_EVAL).
- The Bridge's timestamps in tonight's write-ups ran ~1.5–2 h fast; git times are correct.
