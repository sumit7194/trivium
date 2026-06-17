# Leg 3 — Pre-registration: closing the spine — "how many numbers is a black hole?"

*Frozen 2026-06-17, before the measured-DOF computation. Discipline: THE_BRIDGE.md §2,
§3 (the spine), §4C (proof ↔ test), §5 (the count-triangle).*

This leg completes the spine: the **measured** leg (deepstrain's δ) joins the **proved**
leg (ansatz moduli) and the **inferred** leg (tabula's neural count, leg 1). It is the
ansatz ↔ deepstrain pairing (§4C) plus the three-way synthesis (§5).

---

## 1. The one proposition, three epistemologies

> **An isolated, stationary black hole is fixed by a small fixed set of numbers
> (no hair).** For the astrophysical (rotating, vacuum) case that set is **2** — mass
> and spin `(M, χ)`.

Each oracle addresses this *independently*, on the black-hole family it can reach:

| Oracle | Epistemology | What it returns | Family it addresses |
|---|---|---|---|
| **ansatz** | deductive — *proves* | moduli dimension of the metric; no-hair theorem | any (proved structurally) |
| **tabula** | inductive — *infers* | intrinsic dim of the observable manifold (leg 1) | charged-static (RN) |
| **deepstrain** | empirical — *measures* | the no-hair deviation δ on real ringdowns | rotating-vacuum (Kerr) |

**Honest family caveat (registered up front, not hidden — §7 anti-overclaim).** The three
legs do **not** all probe the *same* black hole: tabula's leg-1 count was on the charged
*static* family `(M, Q)`; deepstrain's δ is on the *rotating-vacuum* family `(M, χ)`;
ansatz proves both are 2-parameter. So the concurrence is on the **count (2)**, across
independent methods *and* across two different 2-parameter black-hole families — not on a
single shared object. That is the honest claim; it is still strong.

---

## 2. The three quantifications (predicted values, frozen)

- **ansatz (proved, exact).** No-hair is proved (`32_no_hair.py`, `33_no_hair_ladder.py`:
  a minimally-coupled scalar adds NO hair in any dimension; the metric is forced). Charge
  enters as one number (`34_hair_criterion.py`), with electric≡magnetic (`Q²+P²`). Kerr is
  a 2-parameter family. **Moduli count = 2** (astrophysical), exact. *Prediction: 2.*
- **tabula (inferred, leg 1).** Neural bottleneck intrinsic dimension of the observable
  manifold for RN = **2** (dimensionful), with the proven dyonic degeneracy showing the
  *observable* count can fall below the *algebraic* one. *Prediction (carried from leg 1):
  2.*
- **deepstrain (measured).** The no-hair test constrains a candidate **third number** δ
  (the 221 overtone's fractional slide off the Kerr prediction). δ consistent with 0 ⟺ no
  third number is resolved ⟺ effective DOF = 2. Recalibrated GW250114:
  **δ = −0.16 [−0.46, +0.33]** (median [90% CI]), σ(δ) ≈ 0.36, coverage ≈ 0.91,
  Kerr inside 90%. *Prediction: consistent with 2 (δ compatible with 0).*

---

## 3. The concrete measured-DOF computation (the only new code in this leg)

Turn deepstrain's δ posterior into a **measured count** comparable to a moduli dimension,
via a transparent nested-model comparison (does the data need the 3rd number?):

- Models: **M2** = Kerr, 2 numbers (δ fixed = 0); **M3** = 2 numbers + a free hair δ.
- **Savage–Dickey density ratio** for the nested point δ=0:
  `BF(M2:M3) = posterior(δ=0) / prior(δ=0)`.
- Posterior approximated as Gaussian from the published summary (median −0.16, 90% CI
  → σ ≈ 0.36). **Prior (frozen, stated as illustrative):** δ ~ Uniform[−1, 1]
  (density 0.5); also report Uniform[−0.5, 0.5] as a sensitivity.
- Report: `BF(M2:M3)`, `σ(δ)` (the resolution on a 3rd number), and the 90%-CI inclusion
  of 0.

**Frozen criteria:**
- **C1 — measurement is consistent with DOF = 2:** δ=0 within the 90% CI **and**
  `BF(M2:M3) ≥ 1` (data does not favor a 3rd number). *Predicted: holds.*
- **C2 — the triangle closes:** all three independent counts = 2 (ansatz proved, tabula
  inferred in leg 1, deepstrain measured here via C1), with the family caveat documented.
  *Predicted: holds.*

**What disagreement would mean (decided now, §3 outcome menu):**
- deepstrain favored δ≠0 (`BF < 1`, 0 outside CI) → either a real no-hair deviation or an
  astrophysical complication; the proved + inferred legs would localize which. (Not
  predicted; GW250114 is Kerr-consistent.)
- tabula ≠ 2 → already resolved in leg 1 (it was 2, with the dyonic degeneracy as the one
  principled departure).
- The interesting *theory-below-measured* case (§5) does not arise here (theory = 2,
  measured ≥ 2-consistent).

## 4. Independence / honesty safeguards (§2)
- The three numbers are obtained by three methods that never saw each other's answer:
  ansatz proves from equations; tabula inferred from observations (leg 1, blind); deepstrain
  measured from real strain. No number is tuned to make the triangle close.
- The Savage–Dickey prior is stated as **illustrative**; the BF is reported with its prior
  sensitivity, and the primary empirical statement is the prior-free one (δ=0 within 90% CI,
  σ(δ)≈0.36). The δ posterior is deepstrain's published result, used as-is (read-only).

## 5. Deliverables
- `code/measured_dof.py` — the Savage–Dickey BF + the assembled §5 count-triangle table,
  reading deepstrain's δ posterior summary (read-only) and leg-1's result.
- `results/` — the triangle table + BF, a figure.
- `FINDINGS.md` — the closed spine, with the family caveat and honest limits.
