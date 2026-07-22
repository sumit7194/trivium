# K1 — Pre-registration: the squeezed-state kill of the entropic hinge

*Frozen 2026-07-23, before `code/k1_squeezed.py` is written or run. First attack on the Falsification
Ledger. Gates fixed here; UNDECIDED is a legitimate outcome; a survivor goes through prior-art before
anyone gets excited.*

## The postulate under attack (Ledger K1)

> **"S_rel = 2π × boost-energy holds for EVERY localized excitation of the vacuum"** — not just coherent
> states.

Leg X ([../../legX_entropic_hinge](../../legX_entropic_hinge)) established the identity for **coherent**
excitations of a free scalar on a Rindler wedge (Longo 2019; Casini–Grillo–Pontello 2019). By
Bisognano–Wichmann the vacuum modular Hamiltonian on the wedge **is** 2π × the boost generator, so
"2π × boost-energy" = Δ⟨K_σ⟩, the change in modular energy. The postulate is therefore the claim

    S_rel(ρ ‖ σ) = Δ⟨K_σ⟩     ⇔     ΔS ≡ S(ρ_A) − S(σ_A) = 0     for ALL localized ρ.

Longo proved this for coherent states only. K1 postulates it universally. **We expect it to die** (Tier K):
the value is a worked counterexample on our own instrument, a *measurement* of the correction term, and a
sharp statement of what singles out coherent states.

## The kill mechanism (exact, Gaussian)

Relative entropy of Gaussian states obeys the exact first-law decomposition

    S_rel(ρ ‖ σ)  =  Δ⟨K_σ⟩  −  ΔS ,
    Δ⟨K_σ⟩ = ½ Tr(G (γ_ρ − γ_σ)) + ½ dᵀ G d ,
    ΔS     = Σ_k [ s(ν^ρ_k) − s(ν^σ_k) ] ,   s(ν) = (ν+½)ln(ν+½) − (ν−½)ln(ν−½) ,

where G is the vacuum modular quadratic form (K_σ = ½ Rᵀ G R + const), γ_· are reduced covariances, d the
displacement, and ν^·_k the symplectic eigenvalues of the reduced states. **Coherent** ⇒ γ_ρ = γ_σ ⇒ the
Tr-term and ΔS both vanish ⇒ S_rel = ½ dᵀ G d = leg X exactly. A **squeezed** excitation changes the
covariance (γ_ρ ≠ γ_σ) ⇒ ΔS ≠ 0 ⇒ the identity fails, and **the failure equals ΔS**.

## Setup (frozen — inherits leg X)

- Chain: N = 96 sites, Dirichlet, K = (2+μ²)I − hopping, **μ = 0.5**; region A = sites 49…96, cut x_c = 48.5.
- Vacuum global covariance γ_vac = diag(X, P), X = ½K^{−1/2}, P = ½K^{1/2} (leg X `build_chain`).
- **Squeezed excitation:** single-mode squeeze along a normalized real-space Gaussian profile v (width
  σ_v = 2.5, centre j₀ = 60.5 i.e. x₀ = 12 — leg X's baseline packet), by the symplectic map
  M = diag(M_q, M_p), M_q = I + (e^{r}−1) v vᵀ, M_p = I + (e^{−r}−1) v vᵀ. This is a proper single-mode
  squeeze: M_q M_pᵀ = I. Squeezed global covariance = M γ_vac Mᵀ = diag(M_q X M_qᵀ, M_p P M_pᵀ), then
  reduce to A. **Squeeze sweep r ∈ {0.2, 0.4, 0.6, 0.8}**, displacement d = 0 for the primary kill.
- Modular data (reuse): G_qq = `entropic_hinge.modular_form` (A_q), G_pp = `certification_tests.bp_form`
  (B_p), G_qp = 0 (vacuum time-reversal symmetric). ν^σ_k from X_A^{1/2} P_A X_A^{1/2}; ν^ρ_k from the
  squeezed reduced blocks.
- Precision: mpmath **dps = 60** (ansatz `.venv`, read-only), matching leg X.

## Frozen gates

- **K1a — the KILL (primary).** For the squeezed packet, the identity fails far outside leg X's lattice
  tolerance: **|S_rel / Δ⟨K_σ⟩ − 1| > 0.10** at r ≥ 0.4, growing monotonically across the sweep.
  → **KILLED** if satisfied. → **SURVIVES** if the ratio stays within leg-X tolerance (~2%) across the whole
  sweep (would be astonishing). → **UNDECIDED** if it lands in the 2–10% grey band (attributable to lattice
  error, not clearly ΔS).

- **K1b — the PAYOUT (measure the correction).** Report Δ⟨K_σ⟩ (from the modular-form contraction) and ΔS
  (from the two symplectic spectra) as the two ingredients, and S_rel = Δ⟨K_σ⟩ − ΔS as the corrected value.
  **Honesty note (frozen):** on the full chain the decomposition S_rel = Δ⟨K_σ⟩ − ΔS is an *exact identity*,
  not an independent check — every Gaussian route to S_rel collapses to the same algebra — so it cannot
  by itself validate anything. Its role here is to *quantify* the correction: ΔS is the entanglement-entropy
  term that the postulate wrongly sets to zero. The **exactness of the decomposition** (that S_rel really is
  the relative entropy and the deviation really is ΔS) is certified non-circularly by **K1d**, not here.

- **K1c — the CONTROL (why coherent is special).** Re-run with r = 0, displacement d ≠ 0 (leg X's coherent
  packet): **ΔS < 1e-40** (machine zero) and **|S_rel/Δ⟨K_σ⟩ − 1| < 2%** (reproduces leg X). Demonstrates
  ΔS = 0 ⇔ γ_ρ = γ_σ ⇔ coherent.

- **K1d — the NON-CIRCULAR certification (the load-bearing check).** On a SMALL toy chain (N = 6, region
  A = 2 sites) compute all three of {S_rel, Δ⟨K_σ⟩, ΔS} by **two fully independent methods**: (i) the Gaussian
  covariance machinery, and (ii) brute-force truncated **Fock density matrices** with S_rel = Tr ρ(ln ρ −
  ln σ), ⟨K_σ⟩ from K_σ = −ln σ_Fock, and entropies from eigenvalues — **no Gaussian formulas anywhere in
  (ii)**. Gate: the two methods agree on every quantity, and the decomposition S_rel = Δ⟨K_σ⟩ − ΔS holds in
  both, all to **< 1e-6**. This is what certifies — non-circularly — that the full-chain deviation reported
  by K1a/K1b IS the true entanglement-entropy correction, not a covariance-formula artifact. Mirrors leg X's
  C3. If K1d fails, K1a/K1b are void regardless of how clean they look.

- **K1e — positivity canary (bug-catcher, not a verdict).** **S_rel ≥ 0** across the whole sweep (Klein's
  inequality). A negative value ⇒ machinery bug, not a discovery.

## Honest limits (fixed in advance)

- Toy model only — harmonic chain, one packet family, one mass; labeled as such, exactly like leg X. Touches
  no experiment and says nothing about nature or continuum QFT.
- Tier-K expected kill: dying is the base case. The payout is the worked counterexample, the measured ΔS,
  and the localization of Longo's coherent-state hypothesis.
- "Boost energy = Δ⟨K_σ⟩" is exact for the vacuum wedge modular Hamiltonian (Bisognano–Wichmann); on the
  lattice it inherits leg X's ~1.5% dispersion offset — which is why K1a's kill line (10%) sits an order of
  magnitude above it.

## Anchors (read-only)

Longo 2019 (entropy of coherent states) · Casini–Grillo–Pontello 2019 · Bisognano–Wichmann 1976 ·
leg X ([../../legX_entropic_hinge](../../legX_entropic_hinge)); reuses `entropic_hinge.py`,
`certification_tests.py`. Interpreter: conjecture_machine `.venv` (mpmath 1.3.0, numpy 2.4.6).

---

## ADDENDUM (frozen 2026-07-23, after the first run, before `k1_squeezed.py`'s amended kill arm is written)

**What the first run found (frozen result, honored):** the pre-registered attack squeezed a packet at
x₀ = 12 — a mode sitting **entirely inside region A**. Result: **ΔS = 0 to machine precision for every r,
so S_rel = Δ⟨K_σ⟩ exactly and K1 SURVIVED this attack.** This is not a null: a single-mode squeeze whose
support lies inside A is a **local unitary on A**, and von Neumann entropy is invariant under local
unitaries ⇒ ΔS = 0 necessarily. The frozen construction was therefore too weak to test K1 — it could not
move the entanglement entropy even in principle. **The SURVIVED verdict stands for the inside-wedge
squeeze**, and it sharpens the picture: it is not "squeezing" that breaks Longo's identity (the ledger's
K1 phrasing), but specifically **squeezing that entangles across the horizon**.

**Why coherent states are special — the sharp statement this exposes:** displacement operators
**factorize** across any cut, D(f) = D(f_A) ⊗ D(f_Ā), so a coherent excitation is *always* a local unitary
on each side ⇒ ΔS = 0 for **every** coherent state, straddling or not (Longo). Single-mode squeezes do
**not** factorize across a cut they straddle ⇒ they change the reduced spectrum ⇒ ΔS ≠ 0. That
non-factorization is the precise obstruction K1 was blind to.

**Amended attack (frozen now, gates below replace K1a for the kill):**

- **K1a′ — the POSITION SCAN (mechanism).** Fix r = 0.6; sweep the squeeze centre x₀ ∈ {12, 8, 4, 2, 0, −2}
  (site coordinate x_c + x₀), width σ_v = 2.5, so the profile moves from deep inside A (x₀=12) to straddling
  the cut (x₀≈0) to mostly outside (x₀=−2). Frozen prediction: ΔS ≈ 0 inside, rising to a clear maximum as
  the profile straddles the cut. This *is* the mechanism made visible — the identity's failure is controlled
  by cross-cut support, nothing else.
- **K1a″ — the KILL (primary, replaces K1a).** At the straddling centre that maximises cross-cut support
  (x₀ = 0, profile centred on the cut), sweep r ∈ {0.2, 0.4, 0.6, 0.8}, d = 0. Gate:
  **|S_rel/Δ⟨K_σ⟩ − 1| > 0.10** at r ≥ 0.4, **monotone** in r. → KILLED / UNDECIDED (2–10%) / SURVIVES (<2%),
  as before. The inside-wedge SURVIVED row (x₀=12) is retained as the built-in control at the other end of
  the same scan.
- **K1d fix (numerical method; gates unchanged):** the first Fock check missed 1e-6 for two compounding
  reasons, both diagnosed and fixed without touching the pass/fail bar. (i) The squeeze operator built by
  `expm` of the truncated generator develops spurious high-occupation eigenvalues that `ln σ` amplifies —
  replaced by the **normal-ordered (disentangled) form** (a†², a² nilpotent ⇒ exact finite series), with a
  **covariance self-check** confirming the built ρ,σ reproduce their target quadratures to 2e-16. (ii) At
  the r=0.6 toy the reduced ν is large enough that `ln σ`'s modular depth exceeds **float64** in the
  brute-force trace (the same wall leg X logged as O4) — so the certification toy uses a **gentle squeeze
  r=0.3** (ΔS≈0.18, still a genuine cross-cut check, ν≈0.52–0.58), where the float64 Fock log is clean; the
  mpmath dps=60 KILL has no such wall and runs r up to 0.8. Result: Fock↔Gaussian agree to ~1e-9.

All other gates (K1b honesty note, K1c control, K1e positivity, honest limits) stand unchanged.
