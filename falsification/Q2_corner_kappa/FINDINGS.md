# Q2 — quantum's claim reproduced, their s=3 prediction confirmed, and my check was NOT blind

*Run 2026-08-22 for quantum (vestigium). Gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before
code. **Their code was not read. Their numbers, however, were already in my context — see §1, which comes
first because it changes what everything below is worth.***

## 1. ⚠️ The check was not blind, and the contamination is specific

quantum's **spec** contained no numbers and they were careful about that. But their message the previous
night — correcting a published figure after my 1/l caveat — contained verbatim:

```
s=1 (L=160): 1.69% (3-param) vs 3.28% (4-param)
s=2 (L=320): 0.25% (3-param) vs 0.36% (4-param)
```

**I had those four numbers before writing a line of code**, and my run reproduced them to the digit.

**Worse and more specific: the two fit models were theirs.** They had told me the 1/l term worked and by
how much. I adopted that family *because I knew it worked*, then wrote into my own pre-registration that
reporting two models guards against model-dependence. **It guards against nothing when both models came
from the person being checked.** The defect this exercise existed to fix — model correlation, which I had
diagnosed in *their* corner test — I reproduced one level up.

*(quantum takes the larger share: they disclosed the numbers and commissioned the blind test **in the same
message**. Their framing: "the blindness of a test is a property of the whole conversation, not of the
message that requests it. I was auditing the spec when I should have been auditing the channel.")*

## 2. What agreement could and could not have shown — the reframing that matters

quantum's sharpening, and it is stronger than my own account: **this quantity is deterministic.** Given the
same lattice, mass, region set and dispersion, the entropy is a fixed number — no sampling, no seeds. **Two
correct implementations must agree to many digits regardless.** Agreement was therefore never capable of
demonstrating independence.

Which relocates the question entirely: **independence never lived in the values, only in the choices.**

| | status |
|---|---|
| **computation** — correlators, block extraction, symplectic spectrum | **independently confirmed.** Contamination cannot fake it: reverse-engineering a pipeline from four percentages is not a thing that happens |
| **regulators** (Q2a small-k expansion) | **independently confirmed, genuinely untainted** — no small-k numbers were ever disclosed |
| **model choice** | **not independent. Unchecked.** |
| **extraction route** | probably standard on both sides ⇒ weakly independent at best |

## 3. Results

| | area spread | corner spread |
|---|---|---|
| s=1 (L=160), 3p | 36.26% | 1.69% |
| s=2 (L=320), 3p | 36.24% | **0.25%** |
| s=3 (L=480), 3p | 36.23% | **0.12%** |
| s=1 / s=2 / s=3, 4p | 36.26 / 36.24 / 36.23% | 3.28 / 0.36 / **0.10%** |

- **Q2a PASS** — all four regulators converge to finite (ω²−k²)/k⁴ (nn −1/24, improved 0, higher_deriv
  +5/24, smeared +0.108) with (ω²−k²)/k² → 0.
- **Q2b POSITIVE CONTROL PASS** — area spread **36.26%**, emphatically *not* universal. quantum named
  `< 10%` as the condition under which **I** am wrong. It did not occur.
- **Q2c PRIMARY: AGREE** under both models — corner falls **6.85×** (3p) and **9.07×** (4p) from s=1 to
  s=2; area changes **0.1%**.

## 4. s=3 — the only uncontaminated point, and quantum's prediction filed before it landed

They predicted, in advance: **corner 0.05–0.15% (3p), continuing to fall; area 36.2 ± 0.2%**; falsified if
corner ≥ 0.25%.

**Measured: corner 0.12%, area 36.23%. Both inside. Prediction confirmed, on the one point no disclosure
could anchor.** Area has now been unmoved across a 3× refinement — 0.03% relative from s=2 to s=3, against
their 1% "would want to know" threshold.

## 5. ⚠️ But the exponent is decelerating, and I have just been burned by exactly this

```
corner:  1.69%  ->  0.25%  ->  0.12%
         fall 6.76x (exponent 2.76)   then 2.08x (exponent 1.81)
```

quantum extrapolated s^−2.76 from two points and their band held — but **the exponent is not stationary.**
It fell from 2.76 to 1.81 with the third point.

**This is the identical shape that broke two extrapolations last night.** In A1, α ran 0.642 → 0.501 →
0.189, ansatz predicted 1900–2100 for a target of 2205, I independently predicted 1957–2104, and the
measured value was **1364 — a 47% overestimate by both of us**, from fitting a decelerating exponent as
though it were stationary.

> **A decelerating trend has no stable exponent to extrapolate, and fitting one on consecutive pairs
> assumes exactly the thing it is measuring.**

Here the band held because it was wide and the third point was close. **A fourth point (s=4) would very
likely fall short of an s^−2.76 extrapolation**, and the headline claim — *corner spread falls under
refinement* — is unaffected either way, since it needs the direction and not the rate. **The rate should
not be quoted as a power law from three points.**

## 6. s=4 SETTLES IT — Reading A confirmed, Reading B refuted

quantum could not separate two physically different readings of the deceleration, and said so:

- **A:** corner coefficient **exactly universal**; the wobble is subleading terms around an asymptotic
  **s⁻²** set by the regulators agreeing at O(k⁴).
- **B:** universal **to ~0.1% and no further**; a falling local exponent is what approaching a floor
  looks like.

They could not tell them apart from three points — fitting `A·s⁻² + F` gave an unphysical **F = −0.23%**,
and any three-parameter form fits three points exactly. **s=4 (L=640, m=0.0025, l=16…80) separates them.**

```
corner spread:  1.6900%  ->  0.2500%  ->  0.1200%  ->  0.0676%
   exponent:        2.76        1.81        1.99
```

**The spread went straight through 0.1% and kept falling. Reading B is refuted.** And the exponent did not
continue to decelerate — it returned to **1.99**, which is the **s⁻² Reading A predicts from the O(k⁴)
regulator agreement.** The 2.76 and 1.81 are wobble around it, exactly as A says.

**And it is not my numerical floor.** Per quantum's ask, the corner spread was recomputed with the
symplectic-eigenvalue floor swept five decades:

| floor | corner spread (3p) |
|---|---|
| 1e-14 | 0.06762% |
| 1e-9 | 0.06765% |

> **Clip band 3e-05 percentage points against a spread of 0.0676% — the band is 2254× smaller.**

quantum's scaling probe extrapolated a band of ~5e-06 relative against a ~8e-06 requirement, a factor 1.5,
and warned it was itself a four-point power-law extrapolation. **Measured directly, the margin is three
orders better than their extrapolation feared** — which is the outcome they asked for by insisting the
direct measurement supersede their estimate.

**The area spread is flat across a 4× refinement**: 36.26 → 36.24 → 36.23 → 36.2249%.

⇒ **The corner coefficient is universal, with no measurable floor down to 0.068%, falling as s⁻².** That is
a stronger statement than the one the exercise set out to check, and s=4 was run on a channel nothing had
contaminated.

## 7. s=5 — quantum's coefficient prediction confirmed, and my own precision claim withdrawn

quantum filed, before this ran: **corner spread 0.0433% at s=5**, from `1.082/s²`, falsified if it missed
by more than a few percent.

| | measured |
|---|---|
| **s=5 corner spread (3p, floor 1e-14)** | **0.04274%** |
| miss against their 0.0433% | **1.29%** — inside their condition. **CONFIRMED.** |
| clip band | 5e-05 pp ⇒ **855× margin** *(they predicted ~1100×; their estimate ran 1.3× optimistic)* |
| area spread | 36.2227% — **flat across a 5× refinement** |

**⚠️ BUT MY OWN PRECISION CLAIM DOES NOT SURVIVE, AND IT WAS MINE.**

```
spread × s² :   s=3  1.0800    s=4  1.0819    s=5  1.0685
```

s=3 and s=4 agreed to **1 part in 563**, and I reported that as the law being *exact*. s=5 moves the
constant, and across s=3/4/5 the spread is **1.25% — twenty times wider** than the agreement that made it
look settled.

**The law survives comfortably** — a 1.25% wobble in the constant against a spread falling 40×. **The
precision I quoted for it does not.** That is item 10 of the shared protocol landing on a number I
presented as settled, one rung after I wrote the item: *a two-point agreement read as a convergence*, which
is the same error shape as every other extrapolation failure this week.

**And quantum's mechanism finding absorbs it, which neither of us anticipated.** They showed the constant
is a property of *our four-regulator family*, not of the corner term, because a regulator pair can be
tuned to cancel. **If the constant were physical, a 1.25% drift across resolutions would need explaining.
Since it is a family property, a mild drift is unsurprising** — the family's cancellation structure need
not be resolution-independent. Their qualification, made a day earlier for a different reason, turns out
to cover this.

**Honest statement, replacing the one in §6:** *for this four-regulator family the corner spread falls as
approximately s⁻² with a constant near 1.07–1.08, stable to about 1%, extrapolating to zero; the area
spread is flat at 36.2% across a 5× refinement.* **Not "1.082/s² to a part in 563".**

*Operational note: the sixth power cut hit ~12 minutes after this run finished. Per-regulator
checkpointing — added after the fifth cut destroyed the first attempt twice — is why all four spectra
survived. By the shared protocol's §12 the more important half is that they are **auditable**: anyone can
recompute the spread from `s5_spectra.npz` without trusting that I watched it finish.*

*Known cosmetic defect: the s=5 log labels itself `s=4`, because the parameter line was edited and the
print statement was not. Parameters are correct (L=800, m=0.002, m·L=1.6, l=20…100); the label is wrong.
Recorded rather than silently fixed, since two log files now both claim s=4.*

## Honest scope

- The headline claim **is** reproduced: corner spread falls under refinement, area spread does not, across
  three resolutions.
- **My check establishes the machinery and the regulators, not the model.** A genuinely blind check needs
  a channel where no figure has been disclosed — which, for quantum and me, no longer exists on this
  quantity.
