# S3 — Pre-registration: two compactifications with IDENTICAL mass towers but DIFFERENT couplings

*Frozen 2026-07-24, before `code/s3_drum_kk.py` is written or run. Falsification v2, Tier S — the item that
**unifies the drums arc in field-theory language**. K2 (KILLED): the GWW drums are isospectral, so the mass
tower does not determine the hidden geometry. K5 (KILLED): a net separates them anyway, because *a recording
is the spectrum weighted by eigenfunction overlaps*. S3 lifts that from analogy to an actual **KK
compactification** and asks for the field-theory observable that carries the difference.*

## The postulate

**"A KK reduction on a GWW-drum cross-section yields two 4D field theories with identical mass towers but
distinguishable local physics."**

Concretely: take a massless scalar on `ℝ^{1,3} × D` with Dirichlet walls, `D` a GWW drum. Expanding
`Φ(x,y) = Σ_k φ_k(x) ψ_k(y)` with `−Δ_D ψ_k = λ_k ψ_k` gives a 4D tower of scalars with

> **masses `m_k² = λ_k`** — an eigen**value** quantity, *identical* for the two drums (GWW), while
> **cubic couplings `g_{ijk} = ∫_D ψ_i ψ_j ψ_k d²y`** — an eigen**function** quantity, which need not be.

So the claim is sharp and computable: **same spectrum, different vertices.** The particles weigh the same;
the interactions do not.

## The observable (frozen, and chosen to be basis-invariant)

Individual `g_{ijk}` are ill-defined under (i) eigenvector sign flips and (ii) rotations inside degenerate
multiplets. The gate therefore uses the **squared Frobenius norm of the truncated cubic coupling tensor**

> **`G(M) = Σ_{i,j,k ≤ M} g_{ijk}²`**

which is invariant under independent orthogonal transformations on each index — hence under both sign
choice and any within-multiplet basis choice. Physically: the total cubic interaction strength among the
lightest M Kaluza–Klein modes. Eigenfunctions normalized `Σ_grid ψ² h² = 1`.

**Truncation rule (frozen):** `M` = the largest `m ≤ 8` such that `λ_{m+1}/λ_m − 1 > 0.02`, i.e. the
truncation is placed at a genuine spectral **gap** so no near-degenerate multiplet is cut in half. The chosen
M and the gap structure are reported.

## The critical control: physical difference vs discretisation error

A raw "the couplings differ" number proves nothing — FD on a staircase boundary makes *everything* differ a
little. The gate is therefore about **convergence behaviour** across resolutions `n ∈ {16, 32, 48, 64}`
(K2's corrected grid, distinct offsets, connectivity assertion inherited):

- `δ_spec(n)` = max relative difference of the two towers over the M modes — must **shrink** with n (K2's
  established ≈h⁰·⁹⁷ convergence: the drums really are isospectral).
- `δ_coup(n)` = relative difference of `G(M)` between the drums — must **NOT** shrink to zero.

## Frozen gates

- **S3a — identical towers.** `δ_spec(n)` decreases monotonically with n and `δ_spec(64) < 3%`. PASS ⇒ the
  two compactifications have the same 4D particle masses (K2 reproduced inside the KK setting).
- **S3b — different couplings (the postulate).** `δ_coup(64) > 10 × δ_spec(64)` **and** `δ_coup` is not
  converging away (`δ_coup(64) ≥ ½·δ_coup(16)`). PASS ⇒ **postulate TRUE**: identical masses, distinguishable
  vertices — local physics separates what the tower cannot.
- **S3c — the congruence null (what makes S3b mean anything).** Repeat everything for **drum 1 vs its mirror
  image** under `(x,y) → (y,x)` — a *congruent* domain re-gridded from different triangles, so both tower and
  couplings must agree. PASS iff `δ_coup(null) < δ_coup(GWW)/5` **and** decreasing with n. Without this, a
  large `δ_coup` could be pure grid artifact.
- **S3d — A1 too-clean guard.** No quantity may agree to ~1e-15; the drums' *discrete* operators must not be
  one matrix relabelled (K2's retracted bug). K2's connectivity assertion is inherited and must fire never.

## Verdict rule (three-valued)

- **postulate TRUE** — S3a, S3b, S3c all PASS: KK on isospectral drums gives identical towers and
  distinguishable couplings. The drums arc closes in field-theory language.
- **KILLED** — S3b fails: `δ_coup` shrinks with resolution like `δ_spec` does, i.e. the couplings agree too.
  That would say the two compactifications are indistinguishable even locally at cubic order — and would sit
  in real tension with K5, which is exactly the kind of cross-repo disagreement the bridge exists to surface.
- **UNDECIDED(numerics)** — S3c fails: the null's coupling difference is comparable to the GWW pair's, so the
  instrument cannot separate physics from grid artifact at these resolutions. Reported with the numbers.

## Honest scope

- **A toy compactification.** A drum with Dirichlet walls is not a smooth closed internal manifold, and a
  free scalar with a `Φ³` vertex is not a realistic KK theory. The reduction is exact *as stated*; the
  physics claim is confined to that setting and is not a statement about real extra dimensions.
- **Zero novelty.** That isospectral domains have different eigenfunctions is the content of GWW /
  Sunada transplantation; that KK couplings are eigenfunction overlap integrals is textbook dimensional
  reduction. The bridge's contribution is **the join**: K2's kill and K5's kill stated as one falsifiable
  field-theory sentence, *with the convergence control that separates a physical difference from
  discretisation error* — which is the part that is easy to get wrong and easy to overclaim.
- **Inherits K2's corrected build**, including the bug that tabula caught (equal grid offsets disconnected
  each drum into 3 congruent pieces, making the two operators one matrix relabelled). Distinct offsets and
  the connectivity assertion carry over; S3d re-checks it.
- Bridge-solo; imports the bridge's own K2 module; read-only from sisters. numpy/scipy.
