# G3 — Pre-registration: where does thin-layer chaos stop being *detectable*?

*Frozen 2026-07-26, before `code/g3_boundary.py` is written or run. Tier G — a **genuine bet**, the oldest
unfired one on the v1 ledger, and the first new Tier-G attack since the falsification campaign opened.*

## The postulate, and why it is more interesting now than when it was written

**G3 (as written):** *"Every stationary non-integrable vacuum in our reach has detectable thin-layer resonance
chaos."* Record: **MN yes, ZV δ=2 yes — two for two.** The ledger's own note calls it *"instrument-relative by
construction; a kill = non-integrability without dynamical signature at resolution X."*

Two things have changed since it was filed:

1. **[A2](../A2_wall_audit/FINDINGS.md) killed G7 and built the wall taxonomy.** A G3 kill now has a *sharp*
   verdict space: is undetectable-but-real chaos a **species-1** wall (our detector's resolution — crossable)
   or something stronger?
2. **[L9](../../FALSIFICATION_V2.md) (quantum):** *scan the physical regime — the interesting answer is
   usually a boundary, not a yes/no.* G3 has only ever been evaluated at isolated points.

And there is a **structural reason to expect the boundary to exist**, which makes the yes/no framing
inadequate: in the Zipoy–Voorhees family **δ = 1 IS Schwarzschild**, which is integrable. ansatz proved
δ ≠ 1 non-integrable algebraically (§97/§98) and exhibited the chaotic layer at δ = 2 (§106). So as **δ → 1⁺
the deformation vanishes continuously and the chaotic layer must shrink to zero width.**

> **Therefore G3 as literally stated is expected FALSE, and trivially so — by continuity, not by physics.**
> The content is not *whether* it fails but **where**, and **how the signal scales on the way down.** The
> deliverable is a curve, not a boolean (**L3**).

## Method

ZV metric from ansatz's `_zv_invariant.metric(delta)` (read-only import; `sigma = 1/delta` fixes M = 1),
integrated with `poincare`'s `_rk4`/`p_on_shell`, exactly the machinery §105/§106 used.

**The regime knob is δ**, scanned **2.0 → 1.02** toward the integrable Schwarzschild point, with **δ = 1.0 as
the integrable control**. At fixed (E, L_z), scan the initial radius `x0` across the plunge-separatrix region
and, for each orbit, record the two signatures §106 used — **both are required**, as there:

- **frequency drift** (the §105 area-blind detector — the dominant frequency *wanders* along the series);
- **finite escape lifetime** (chaotic transport sticks then escapes; KAM tori are eternal).

For each δ report the **maximum drift found** over the scanned window and whether any orbit fires on both
signatures. The regular neighbours at the same δ furnish the per-δ noise floor.

## Frozen gates

- **G3a — the integrable control (must pass first).** At **δ = 1.0 (Schwarzschild)** no orbit may fire.
  A detector that reports chaos on an integrable metric is broken and **every later gate is void.** This is
  the positive-control discipline that caught our leg-J Lyapunov false positive.
- **G3b — regression on the known point.** At **δ = 2.0** the layer must be found, reproducing ansatz §106's
  exhibited result (drift ≫ the regular-neighbour floor, plus a finite lifetime). If §106 does not reproduce,
  the port is wrong and later gates are void.
- **G3c — the boundary (the L9 scan, decisive).** Scan δ downward and locate **δ\***, the smallest δ at which
  the layer is still detectable at our resolution.
  - **G3 KILLED as stated** iff some δ ≠ 1 (proven non-integrable) shows **no detectable chaos** — i.e.
    δ\* > 1. Expected, and expected to be *uninteresting on its own*; the finding is δ\* and the scaling.
  - **G3 SURVIVES** iff the layer fires at **every** δ ≠ 1 tested, down to δ = 1.02.
  - **UNDECIDED(search)** iff the separatrix hunt fails to locate bound orbits at small δ — a search failure,
    not a physics result, and reported as such with the window searched.
- **G3d — species classification (the payout).** If killed, classify the failure by
  [A2's taxonomy](../A2_wall_audit/FINDINGS.md). **Predicted species-1 (precision):** the evidence would be
  max-drift **declining smoothly toward the floor** as δ → 1, rather than vanishing abruptly. A smooth decline
  says "the layer is still there, our detector ran out"; an abrupt one would be a genuine surprise.
- **A1 guard.** Per-δ floors come from the regular neighbours actually integrated, never assumed. Any orbit
  whose Hamiltonian drift is not ≪ its frequency drift is discarded as an integration artifact, not reported
  as chaos (§106's own discipline).

## Honest scope and stated risks

- **Zero novelty in the physics.** ZV non-integrability is ansatz §97/§98; the δ=2 layer is §106 and
  Lukes-Gerakopoulos PRD **86**, 044013 *[reference relayed from ansatz's §106 header —_
  `[asserted, unverified]` on our side per **L10**; our gates compare orbits against each other, never against
  a quoted coordinate]*. What is new here is **the boundary and its scaling on our instrument.**
- **The search is delicate and may fail.** §106 found the δ=2 layer only by stepping `x0` at 0.002 near the
  separatrix; the separatrix *moves with δ*, and at small δ the layer is expected exponentially thin.
  **UNDECIDED(search) is a live, pre-registered outcome** — and would itself be a species-1 statement about
  the hunt, not about the physics.
- **Transient/sticky chaos is step-size sensitive** (§106's own honest note): drift *magnitude* varies with
  the integration step because different `h` realises the layer differently. **Both signatures must persist**
  for a fire to count, and the controls must show neither — that is the discipline that makes the comparison
  meaningful even when magnitudes move.
- Compute is bounded up front: crossings per orbit and grid size are fixed in the script and reported, so a
  null is always accompanied by exactly what was searched.
- Bridge-solo; imports ansatz read-only; no sister dependency.

---

# ADDENDUM — instrument upgrade for the overnight run (frozen 2026-07-26, before the rerun)

*The first attempt returned **UNDECIDED(search)**: the drift measure's floor (2/N = 0.0333 at N=60) sat
**above** the signal being hunted (§106's 0.027). [A2](../A2_wall_audit/FINDINGS.md) classifies that as a
**species-1** wall — prescription: **upgrade the instrument**. **The gates G3a–G3d are UNCHANGED**; only the
instrument is. Recorded before the rerun so the upgrade cannot be tuned to a result.*

## Four changes, each answering a named defect

1. **Continuous drift estimator.** The FFT peak now uses **parabolic sub-bin interpolation** (the same fix
   S2's rest-buzz used), so the resolution is set by the data rather than by the bin grid `2/N`. This kills
   the quantization that made every δ return an identical 6.67e-2.
2. **Hunt the separatrix, not the band interior.** ⚠️ **The first run looked in the wrong place.** §106's
   layer sits at the **plunge separatrix**; we scanned `x₀ ∈ [10,16]`, the *interior* of the long-lived band.
   Tonight's probe locates the plunge↔survive transition at **x₀ ≈ 8–10**. The rerun finds that transition
   **per δ** and steps finely across it.
3. **§106's actual stepping and record length:** `x₀` step **0.002** across the transition, **N = 200**
   crossings (up to 1.2M integration steps per orbit) — versus 9 samples and N=60.
4. **Each conjunct validated independently on the control** — tonight's real lesson. The `drift AND escape`
   criterion passed vacuously twice (first on zero orbits, then on a dead drift conjunct). G3a now
   additionally requires that the drift measure be **non-degenerate** on the control (a real spread, not one
   repeated value) and reports separately whether the escape detector ever fired anywhere in the run. **A
   conjunctive gate certifies nothing unless each conjunct is known to be alive.**

## Unchanged, and stated so

Gates **G3a–G3d**, the fire criterion (`drift ≥ 3× floor` **and** finite escape lifetime), the A1 integration
guard (`dH < 1e-4`), E = 0.95, Lz = 3.0, and the δ list. **UNDECIDED(search) remains a live outcome** — a
better instrument is not a guarantee, and if the layer still does not reproduce that is reported as such.
Results are written **incrementally per δ** so a partial run is still evidence.
