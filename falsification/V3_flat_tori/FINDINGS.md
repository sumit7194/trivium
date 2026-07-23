# V3 — Findings: 2D flat tori ARE determined by their spectrum (the converse of K2)

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item V3
(Tier V — validation). **Verdict: SURVIVES.** Together with [K2](../K2_isospectral_drums) this completes the
"can you hear the shape?" story honestly.*

## Result in one line

Unit-covolume flat 2-tori are spectrally determined: across 2000 random moduli pairs, **every** pair
genuinely separated in moduli (hyperbolic distance > 0.1) has spectral distance **≥ 1.5×10⁻²** — no spurious
isospectral pairs — while SL(2,ℤ)-equivalent moduli (the *same* torus) are isospectral to **10⁻¹⁶**. The
spectrum responds **linearly** to shape perturbations (p ≈ 1.00), resolving moduli down to **δ ≈ 7×10⁻¹³**.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **V3c** (canary, run first) | SL(2,ℤ)-equivalent moduli isospectral, rel < 1e-12 | **4.5e-16 / 4.5e-16 / 9.0e-16** (τ+1, τ−1, −1/τ) | **PASS** — convention verified |
| **V3a** (postulate) | no well-separated pair isospectral (> 1e-6) | min over 1886 far pairs = **1.476e-2** | **SURVIVES** |
| **V3b** (resolution) | linear response, p ∈ [0.9,1.1]; report resolving power | p = **1.0004 / 0.9882 / 1.0005** (K=10/40/160) | **PASS** |

## The resolution bound (V3b — the honest deliverable)

| K (eigenvalues used) | exponent p | resolving δ |
|---|---|---|
| 10 | 1.0004 | 8.3×10⁻¹³ |
| 40 | 0.9882 | 8.1×10⁻¹³ |
| 160 | 1.0005 | 6.6×10⁻¹³ |

Two things worth stating plainly:

1. **The response is exactly linear** in the moduli perturbation δ over five decades (10⁻² → 10⁻⁶). The
   spectrum is a first-order-faithful probe of shape — no degeneracy, no flat directions.
2. **More eigenvalues barely help.** Going from 10 to 160 eigenvalues improves the resolving power by only
   ~20%. The limit is the **numerical floor** (float64 round-off in the eigenvalues), not the information
   content of the spectrum — the first ten eigenvalues already pin the shape essentially as well as 160 do.
   That is the honest characterisation of "bounds the instrument's resolution": the spectrum determines the
   torus, but any *measurement* of it determines the torus only to the precision of the eigenvalues you hold.

## The K2 contrast — what the pair of results actually says

| object | isospectral ⇒ isometric? | verdict |
|---|---|---|
| **GWW drums** (K2) | **No** — identical spectra to 10⁻¹⁵, provably non-congruent | K2 **KILLED** |
| **flat 2-tori** (V3) | **Yes** — spectrally determined | V3 **SURVIVES** |

"Can you hear the shape?" has **no universal answer**. It depends on the class of object and on the
dimension. The family's instrument reproduces both halves: it fails to distinguish the drums (because they
genuinely cannot be distinguished) and cleanly distinguishes every pair of flat tori (because they genuinely
can be). A single instrument giving both answers correctly is the real validation here.

## Honest limits (frozen in advance)

- **Strictly 2D — and this matters.** Flat tori are spectrally determined only in low dimension. In **4D**
  there are isospectral non-isometric flat tori (Conway–Sloane), and in **16D** is Milnor's classic
  counterexample. A statement about "flat tori" with no dimension attached is simply false; V3 is stated and
  tested for 2D only, where the theorem holds.
- **Known theorem, zero novelty claimed.** Tier-V payout: instrument hardening plus a measured resolution
  bound, and completing the hearing-shapes story alongside K2.
- Approximations are the finite eigenvalue count (K) and finite dual-lattice enumeration (|a|,|b| ≤ 14); V3b
  measures exactly the resolution these impose rather than hiding them.

## Inputs (read-only) & artifacts

Milnor 1964 (16-D counterexample) · Conway–Sloane (4-D isospectral lattices) · Kac 1966 ·
Gordon–Webb–Wolpert 1992 · [K2](../K2_isospectral_drums). `code/v3_tori.py` · `results/v3_tori.json`.
Interpreter: conjecture_machine `.venv` (numpy 2.4.6).
