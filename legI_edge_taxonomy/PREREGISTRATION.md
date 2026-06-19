# Move I — Pre-registration: are all the "edges" one mechanism, or several?

*Frozen 2026-06-20. The deepest open question. Move H showed the divergence-recovery edge is
*observational* (noise amplification). This leg asks whether the OTHER edge types reduce to that,
or are genuinely different — using one clean discriminator, outcome-neutral.*

## The discriminator

For any edge, ask: **does it survive perfect observation (zero noise / exact computation)?**
- If reducing observation noise → 0 **removes** the edge → it is **OBSERVATIONAL** (owned by
  observation precision; no oracle "owns" it — learned and exact fail together, Move H).
- If the edge **persists** at perfect observation → it is **PHYSICAL** (the exact structure genuinely
  changes; the exact oracle owns it).

## The two clearest cases (decisive contrast)

- **Divergence-recovery edge (Moves F/H).** Recover the hyperbolic distance from coordinates with
  observation noise σ. *Test:* edge/bulk recovery-error ratio as **σ → 0**.
- **Integrability-loss edge (Move D).** The approximate invariant's held-out conservation (var-ratio)
  vs deformation ε, on **clean** (noise-floor) geodesics. *Test:* the var-ratio at ε>0 in the
  perfect-observation limit (ε=0 is the integration-noise floor; the rise above it is physical or not).

## Predictions (frozen)

- **I1 (F/H is observational).** The edge/bulk ratio → **≤ 1.3** as σ → 0 (the edge needs the noise;
  with perfect observation the divergence is recovered everywhere).
- **I2 (D is physical).** The var-ratio at ε=0 sits at the integration-noise floor (**< 1e-10**), but
  at ε>0 it is **orders of magnitude higher** (e.g. ~1e-2 by ε=0.08) on the SAME clean geodesics —
  so the edge persists at perfect observation (the deformed torus genuinely admits no low-degree
  invariant; nothing to do with observation noise).
- **Conclusion (the taxonomy).** If I1 and I2 both hold, the bridge's "edges" are **NOT one
  mechanism**: there are at least two kinds — *observational* edges (F/H; vanish with perfect
  observation) and *physical* edges (D; persist). If instead F/H persists at σ=0, or D vanishes at the
  noise floor, the taxonomy is wrong and we report that.

## Where the others fall (classified, lighter touch)

- **Algebraically-special edge (Move C):** the Weyl invariant → 0 at the Petrov-special limit; the
  failure was heavy-tailed regression / probe resolution at small signal. Predicted **observational**
  (an exact computation of `tr(Ẽ²)` recovers O/D perfectly even at small values). Noted, not the
  headline test.

## Honest scope
Two clean cases tested decisively; C classified by argument. The result is a **taxonomy of edges**
(observational vs physical), not a single unifying mechanism — and it sharpens what "exact owns the
edge" means: only for *physical* edges.

## Deliverables
- `code/edge_taxonomy.py` — the F/H noise sweep + the D noise-floor analysis (reuses saved Move D data).
- `FINDINGS.md` — I1/I2 outcomes and the observational-vs-physical taxonomy.
