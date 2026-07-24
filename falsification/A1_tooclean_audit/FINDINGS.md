# A1 — Findings: the too-clean audit (SURVIVES — corpus certified, guard installed)

*Run 2026-07-24; gate frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier A — L2 ("too-clean is a bug smell") made mechanical. A sweep flags every machine-precision agreement in
the bridge's corpus; each is then adjudicated to an explicit construction reason or escalated as a bug
suspect. Result: **SURVIVES** — every too-clean agreement is exact-by-construction or the already-caught K2
bug; zero new suspects.*

## Result in one line

The sweep flagged **93 too-clean values (|x| < 1e-10 or exactness prose) across 17 files**; on adjudication
**all 93 classify as legitimate** — 72+ exact-by-construction, the rest known-bug references — leaving
**0 SUSPICIOUS**. No second K2. The corpus's exactness claims are certified, and a complete-baseline,
re-runnable guard is installed.

## Method (the honest two-pass structure)

1. **Mechanical sweep (automatable):** walk all `**/results/*.json` for numeric leaves with `0 < |x| < 1e-10`;
   grep all FINDINGS/PREREGISTRATION/root-docs for exactness keywords (`exact`, `byte-identical`,
   `resolution-independent`, `1.000000`, `1e-1[0-9]`, …). This part has no judgment — it flags everything.
2. **Adjudication (judgment, recorded):** each flagged source is tagged with a **construction reason**.
   The gate is SUSPICIOUS-count = 0 **only because each of the 93 carries a checkable reason** — this is not
   a rubber stamp; a flag with no real reason stays suspicious and escalates. The first run left 14
   unclassified (my initial baseline was incomplete); reading each source resolved all 14 (below), and the
   reasons are now encoded so the baseline is complete.

## What every too-clean value traces to

| class | count-ish | examples & reason |
|---|---|---|
| **EXACT-OK — exact arithmetic** | leg Z, S1, leg Y, K4 | SymPy/integer/symbolic leftover-zero: machine-precision agreement is *expected* (det≡−2; integer theta; CK polynomial certificate; Ricci leftover-zero to all orders in ε) |
| **EXACT-OK — exact symmetry / operator identity** | leg U, V3, **M4** | leg U's 0.00% within-shell degeneracy = the grid's x↔y symmetry (Φ₁=Φ₂); V3's SL(2,ℤ) control = isometric lattices; **M4's ~1e-13 uniform-coupling split = the identity H=−∇²+cI, which shifts all eigenvalues by c and preserves differences on *any* grid** |
| **EXACT-OK — a theorem forcing exact zero** | K1, **K3d** | Longo: a displacement (coherent) excitation factorizes across the cut ⇒ ΔS=0 exactly ⇒ K3d's Σ/δQ = 1.000000 and K1's inside-wedge invariance |
| **EXACT-OK — correct control physics** | **V2** | gapped chain ⟹ central charge 0 ⇒ gapped_pseudo_c ≈ 6e-11 (a control that *should* be ~0) |
| **CONVERGENT-OK (exact underlying form)** | **V2 R²** | R²=1.000000 = fit of the theoretically-exact CFT form S=(c/3)ln(chord)+const; over-precise print of 0.9999996 |
| **KNOWN-BUG (reference)** | K2, **K5** | the disconnected-grid triviality (exactness **retracted**, caught by tabula); K5's prose *quotes* it, not a new value |

## The one that mattered — M4, cleared

M4 was the genuine concern, because its old isospectral floor **rode on the K2 disconnected-grid bug**. A1
forced the check: M4's *current* uniform-coupling numbers (~1e-13) are **not** a K2 residual. They come from
an exact operator identity — adding a constant `cI` shifts every eigenvalue by `c`, preserving all
differences regardless of what `−∇²` is or whether the grid is connected. M4's *substance* (spatially-varying
couplings split the degeneracy, p≈1.0) was already rebuilt on the fixed connected grid. So the uniform floor
is legitimately exact-by-construction, and it never depended on the phantom. **This is A1 doing precisely
what it exists to do:** catching a value that *could* have been a residual bug and confirming, by reading the
mechanism, that it is not.

## Verdict and honest limits

- **SURVIVES:** every machine-precision agreement in the bridge's corpus has a recorded construction reason;
  no unexplained numerical-method exactness remains. The frozen prediction (SURVIVES; K2 was the one) held.
- **What "survives" does and does not mean:** it means *this instrument, at this threshold (1e-10) and this
  keyword set, found no unexplained too-clean value.* It does **not** prove the corpus is bug-free — a bug
  that produces a *plausible-looking, non-exact* wrong number is invisible to A1 (A1 only smells
  *suspiciously clean* ones, which is the specific K2 signature). And the gate is only as sound as the
  adjudication: a wrong construction reason would false-clear. Each reason here is a checkable claim, stated
  so it can be challenged.
- **Standing guard:** `results/audit.json` records the complete baseline. Re-running after any new leg
  surfaces any too-clean value not covered — the next K2 shows up as UNCLASSIFIED before a sister has to
  catch it. That re-runnability is the real deliverable; the clean bill of health is the by-product.
- **Scope:** bridge-owned results only; sister-cited exact values (tabula 2.2e-19, quantum 4e-61) are their
  audit to run. Zero novelty — a hygiene instrument, L2 made mechanical.

## Inputs & artifacts

`code/audit.py` (sweep + frozen classification baseline) · `results/audit.json` (the baseline + verdict).
Sources adjudicated: the corpus's own FINDINGS/results across 17 files.
