# K1 — Findings: the squeezed-state kill of the entropic hinge

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) (+ its addendum) before the code
was written. First attack on the [Falsification Ledger](../../FALSIFICATION_LEDGER.md). Postulate K1:
"S_rel = 2π×boost-energy holds for EVERY localized excitation of the vacuum" — the claim that Longo's
coherent-state identity (validated on the lattice by [leg X](../../legX_entropic_hinge)) extends to all
excitations. **Verdict: KILLED** — but the kill is sharper and more conditional than the ledger anticipated,
and it MEASURES the correction term, as promised.*

## Result in one line

A squeezed packet that **straddles the entangling cut** breaks the identity by the entanglement-entropy
change ΔS > 0 — **22–56%** across squeeze r = 0.2–0.8 (S_rel/boost-energy = 1 − ΔS/Δ⟨K⟩) — while a squeeze
sitting **entirely inside the wedge** leaves the identity **exact** (ΔS = 0, because it is a local unitary
on A). The whole Gaussian pipeline is certified non-circularly against brute-force Fock density matrices to
**1.3×10⁻⁹**. Coherent states are special not because they are unsqueezed, but because **displacement
operators factorize across the cut** (ΔS = 0 always); the identity fails **iff the excitation entangles
across the horizon**.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| reuse | my G_qq vs leg X's certified `modular_form` (A_q) | max rel diff **0.0** | certified path |
| **K1d** (load-bearing) | Gaussian machinery vs brute-force Fock ρ,σ (N=6 toy, A=1 site): S_rel, Δ⟨K⟩, ΔS by two independent methods | agree to **1.3e-9**; Fock covariance self-check **1.1e-16**; ΔS to **3.1e-16** | **PASS** |
| **K1c** (control) | coherent packet (r=0, d≠0): ΔS and leg-X recovery | ΔS = **0**, S_rel = **54.0289** (leg X: 54.03), ratio−1 = **0** | **PASS** |
| **K1a′** (mechanism) | position scan r=0.6, centre from inside A across the cut | ΔS: 0 → **0.437**, deviation: 0 → **63%** | mechanism shown |
| **K1a″** (KILL, primary) | straddling squeeze (x₀=0), r∈{0.2,0.4,0.6,0.8}, d=0 | deviation **56/39/29/22%**, all >10%, monotone | **K1 KILLED** |
| **K1e** (canary) | S_rel ≥ 0 across all rows | holds | **PASS** |

## The mechanism (K1a′ — the finding the ledger did not anticipate)

The ledger's K1 said "squeezing makes ΔS ≠ 0." The position scan shows that is **only true for squeezing
that straddles the cut**:

```
 x0 |      where       | Δ⟨K⟩=boostE |   S_rel   |    ΔS    | |S_rel/boostE−1|
 12 |  deep inside A   |   17.3456   |  17.3456  | 0.000000 |      0.0000
  8 |  deep inside A   |   11.5646   |  11.5646  | 0.000066 |      0.0000
  4 |  straddling cut  |    5.8364   |   5.7864  | 0.049950 |      0.0086
  2 |  straddling cut  |    3.3131   |   3.0463  | 0.266753 |      0.0805
  0 |  straddling cut  |    1.4888   |   1.0515  | 0.437300 |      0.2937
 −2 |   on/over cut    |    0.4220   |   0.1552  | 0.266753 |      0.6322
```

**Why:** von Neumann entropy of the reduced state S(ρ_A) is invariant under any unitary supported on A
alone. A single-mode squeeze whose profile lies inside A is exactly such a local unitary ⇒ ΔS = 0 ⇒
S_rel = Δ⟨K_σ⟩ exactly, identically to a coherent displacement. The identity can only break when the
excitation changes the entanglement *between A and its complement* — which a squeeze does **iff its support
crosses the cut**. The frozen pre-registered attack put the squeeze at x₀ = 12 (inside A) and therefore
**correctly SURVIVED**; that survival is the clue that located the real obstruction.

## Why coherent states are special (the sharpened statement)

Longo's theorem covers coherent states. The sharp reason, exposed here: **displacement operators factorize
across any cut**, D(f) = D(f_A) ⊗ D(f_Ā). So a coherent excitation is a *product of local unitaries* on the
two sides — ΔS = 0 for **every** coherent state, straddling or not (K1c confirms ΔS = 0 to machine zero and
recovers leg X's S_rel = 54.03). Single-mode squeezes **do not factorize** across a cut they straddle: the
squeezed mode becomes a two-region Bogoliubov transformation, the reduced spectrum shifts, and ΔS ≠ 0. The
non-factorization is the precise obstruction — a cleaner statement than "coherent = unsqueezed."

## The payout (K1b — the correction term, measured)

The exact Gaussian first law S_rel(ρ‖σ) = Δ⟨K_σ⟩ − ΔS turns the kill into a measurement: the deviation of
S_rel from 2π×boost-energy **is** the entanglement-entropy change ΔS, computed independently from the two
symplectic spectra. At the straddling position ΔS rises from 0.119 (r=0.2) to 0.617 (r=0.8). The deviation
*ratio* actually shrinks with r (56% → 22%) because Δ⟨K_σ⟩ grows faster than ΔS — a large squeeze is
modular-energy dominated — but ΔS is a large correction throughout. (On the full chain the decomposition is
an exact identity, not a self-check; its **exactness** — that S_rel is the true relative entropy and the
deviation is genuinely ΔS — is what K1d certifies against literal density-matrix logs.)

## K1d — the non-circular certification, and a second sighting of leg X's precision wall

The load-bearing check builds the *actual* reduced density matrices of a small toy in a truncated Fock basis
and compares Tr ρ(ln ρ − ln σ) (no Gaussian formulas) against the covariance machinery. Two numerical
obstructions were diagnosed and fixed **without moving the pass/fail bar**:

1. A squeeze operator built by `expm` of the truncated generator grows spurious high-occupation eigenvalues
   that `ln σ` amplifies (error got *worse* with dimension). Replaced by the **disentangled normal form**
   (a†², a² nilpotent ⇒ exact finite series); a **covariance self-check** confirms the built ρ, σ reproduce
   their target quadratures to **1.1×10⁻¹⁶**.
2. At the original r=0.6 toy the reduced ν is large enough that `ln σ`'s modular depth outruns **float64** in
   the brute-force trace — the *same wall leg X logged as O4*. The certification toy therefore uses a gentle
   **r = 0.3** squeeze (ΔS ≈ 0.18, still a genuine cross-cut check), where the float64 Fock log is clean; the
   mpmath dps=60 KILL has no such wall and runs to r = 0.8. Agreement: **1.3×10⁻⁹**.

So "walls are instrument-relative" recurs inside the *certification of a kill*: the brute-force check is
float64-limited exactly where leg X's production was, and the mpmath instrument crosses it.

## Honest limits (frozen in advance)

- Toy model only — harmonic chain, one packet family, μ = 0.5, Dirichlet; labeled as such, like leg X.
  Touches no experiment; says nothing about nature or continuum QFT.
- Tier-K expected kill: dying was the base case. The payout is (i) the measured correction ΔS, (ii) the
  refinement that it is *cross-cut* squeezing, not squeezing per se, that kills the identity, and (iii) the
  factorization reason coherent states are special.
- "Boost energy = Δ⟨K_σ⟩" is the vacuum wedge modular energy (Bisognano–Wichmann), exact on the lattice up to
  leg X's ~1.5% dispersion offset — an order of magnitude below the kill's 22–56% deviation.

## Inputs (read-only) & artifacts

Longo 2019 · Casini–Grillo–Pontello 2019 · Bisognano–Wichmann 1976 · reuses
[leg X](../../legX_entropic_hinge) `entropic_hinge.py` (G_qq) and the leg-X certification's B_p construction
(G_pp). `code/k1_squeezed.py` · `results/k1_squeezed.json`. Interpreter: conjecture_machine `.venv`
(mpmath 1.3.0, numpy 2.4.6).

---

## Precision amendment (2026-07-24, via R4)

The obstruction to the Longo identity is **exactly ΔS ≠ 0**; the "non-factorization / entangles across the
cut" language above is **sufficient but not necessary**. R4 root-found a genuinely-entangling (non-
factorizing) operation — BS(π/6)·TMS(r\*=0.295) on a 2-mode toy — with **ΔS = 0**, which therefore *satisfies*
the identity despite being non-factorizing (the beamsplitter disentangles, the two-mode squeeze re-entangles,
and they cancel). **This does not change K1's verdict**: the cross-cut *squeezes* K1 tested genuinely have
ΔS ≠ 0, so the kill stands — only the characterization of the obstruction is sharpened. See
[R4_deltaS_obstruction](../R4_deltaS_obstruction/FINDINGS.md).
