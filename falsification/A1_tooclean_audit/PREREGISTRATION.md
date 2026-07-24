# A1 — Pre-registration: the too-clean audit (institutionalizing L2)

*Frozen 2026-07-24, before `code/audit.py` is written or run. Falsification v2, Tier A — bred from the K2
corpse. **L2: too-clean is a bug smell.** K2's "exact, resolution-independent isospectrality (~1e-15)" was a
disconnected-grid triviality; the resolution-independence *was* the tell. A1 sweeps the bridge's own results
for every machine-precision / "exact" agreement and forces each to be classified: legitimately
exact-by-construction, or a bug suspect. It is both a one-time audit and a standing regression guard.*

## The postulate under attack

**"Every too-clean agreement in the bridge's published results — machine-precision or claimed-exact, from a
*numerical* method — is either exact-by-construction (exact arithmetic or a proven exact symmetry) or a bug."**
A1 KILLS it by finding a counterexample: a numerical-method machine-precision agreement with **no**
construction reason and **not** already flagged. It SURVIVES if the corpus classifies cleanly (every such
agreement explained). Both outcomes are wins — a kill catches the next K2; a survival certifies the exactness
claims and leaves a re-runnable guard.

## Frozen definitions

- **too-clean numeric:** a JSON leaf or reported value with `0 < |x| < 1e-10` (an intentional integer 0 or a
  discrete count is not flagged), i.e. agreement far tighter than any finite-difference / float / sampled /
  neural method's order predicts.
- **exactness keyword** (prose sweep of FINDINGS/PREREGISTRATION): one of
  {`exact`, `identical`, `byte-identical`, `resolution-independent`, `0.00%`, `1.000000`, `1e-1[0-9]`,
  `machine precision`}.
- **classification tags** (frozen; every candidate must land in exactly one):
  - **EXACT-OK** — produced by exact arithmetic (SymPy rationals / integer / symbolic leftover-zero) **or** a
    provable exact symmetry of the operator. Machine-precision agreement is *expected* and correct.
  - **CONVERGENT-OK** — a numerical value agreeing at the method's expected order and **not** claimed exact
    (e.g. FD O(h²) reported as ~0.3–1%); flagged only if prose over-claims it.
  - **KNOWN-BUG** — already caught and corrected (K2 is the sole entry; its exactness claim was retracted).
  - **SUSPICIOUS** — numerical method, machine-precision/resolution-independent, **no** construction reason,
    **not** already flagged. Any SUSPICIOUS ⇒ A1 KILLS the postulate and the item goes to K2-style audit.

## Frozen gates

- **A1-gate:** run the sweep; classify every candidate. **SURVIVES** iff the SUSPICIOUS set is empty.
  **KILLED** iff ≥1 SUSPICIOUS item (a live bug suspect) is found. The classification and its per-item
  *reason* are recorded in `results/audit.json` as the baseline; a re-run that surfaces a candidate not in
  the baseline is the standing guard firing.
- **Frozen prediction:** **SURVIVES expected** — K2 was the one numerical-exactness bug and it is caught;
  every other machine-precision agreement in the corpus is expected to trace to exact arithmetic (leg Z
  SymPy, S1 integer, leg Y CK symbolic certificate, leg X C1/C2 mpmath algebraic identities) or an exact
  operator symmetry (leg U's within-shell degeneracy from the grid's x↔y symmetry; V3's SL(2,ℤ) control,
  which is isometric by construction). A KILL would be the jackpot (a second K2 caught before a sister has to).

## Scope (frozen)

- **In scope:** the bridge's own `**/results/*.json`, `**/FINDINGS.md`, `**/PREREGISTRATION.md`, and root
  docs. This audits what the bridge is responsible for.
- **Out of scope:** sister-owned exact values we merely *cite* (e.g. tabula's 2.2e-19 emit, quantum's 4e-61) —
  the same discipline applies but is the sisters' job; flagged as cited-not-owned.
- **Not a physics postulate** — a hygiene instrument. Zero novelty; the payout is systematic certification +
  a standing guard, exactly L2 made mechanical.
