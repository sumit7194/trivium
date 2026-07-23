# K4 — Findings: ad-hoc metric surgery essentially never preserves vacuum

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item K4
(Tier K — expected kill). **Verdict: KILLED**, with the ledger's stated payout delivered: an **exact
obstruction theorem**, not a pile of examples. Formalises [leg Y](../../legY_ck_adjudication)'s single-metric
check of ansatz §119 into a general statement.*

## Result in one line

For the deformation family bumpy-black-hole constructions actually use — multiply g_tt by (1+εh(r)) and
leave g_rr alone — the metric is Ricci-flat **iff h is constant**, i.e. iff the "deformation" is a pure
rescaling of t. **No nontrivial bumpy profile of this form is ever a vacuum.** And the postulate's own
hypothesis fails: the Ricci **scalar** can vanish identically while the Ricci **tensor** does not.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **K4d** (controls, first) | ε=0 and h=const both give R_ab ≡ 0 | True / True | **PASS** |
| **K4b** (the OBSTRUCTION) | exact identity ⇒ vacuum ⟺ h′=0 | identity confirmed; solving gives **h = C₁** | **PASS** — theorem |
| **K4a** (KILL) | sampled ad-hoc profiles are not Ricci-flat | **4/16** nonzero R_ab for all 5 profiles | **K4 KILLED** |
| **K4c** (invariant trap) | R ≡ 0 compatible with R_ab ≠ 0? | scalar ≡ 0 **True**, tensor **3/16** nonzero | **PASS** |

## K4b — the obstruction (the payout, exact in ε)

Computed from the full metric with no linearisation:

$$\frac{R_{tt}}{A} + \frac{R_{rr}}{B} \;=\; \frac{\epsilon\,(r-2M)\,h'(r)}{r^{2}\,\bigl(1+\epsilon h(r)\bigr)}$$

This vanishes **iff h′(r) = 0**. Solving returns **h(r) = C₁**. So the deformed metric is vacuum exactly when
h is constant — which is nothing but a rescaling of the time coordinate, i.e. **pure gauge**. The theorem
holds to **all orders in ε**, not merely perturbatively.

**Stated for practitioners:** *if you build a "bumpy black hole" by multiplying g_tt by a radial profile and
leaving g_rr untouched, your metric is not a vacuum solution unless your bump is a constant.* Five sampled
profiles (1/r, 1/r², e^(−r), a localized Gaussian bump, and a §119-style 6/r) each give 4 nonvanishing Ricci
components — consistent with leg Y's independent finding for the Kerr-based bumpy entry.

## K4c — the invariant trap (why the postulate is false *as stated*)

The postulate's hypothesis is that the deformation "keeps the vacuum character of its **invariants**". Test
the simplest one, the Ricci scalar. At O(ε) the condition R = 0 is the linear ODE

$$h''\,r(2M-r) + h'\,(M-2r) = 0 \qquad\Longrightarrow\qquad h(r) = C_1 + C_2\sqrt{\tfrac{r}{r-2M}}$$

The C₁ branch is the gauge/vacuum one. On the **C₂ branch** the O(ε) Ricci scalar is identically zero while
the Ricci tensor is not — at (M=1, r=4):

```
R[0,0] = 0        R[1,1] = −0.0441942        R[2,2] = R[3,3] = 0.176777
```

A **traceless but nonvanishing** Ricci tensor: g^{ab}R_{ab} = 0 with R_{ab} ≠ 0. The metric passes the
scalar-invariant test and is still not vacuum — it silently sources traceless matter. **A vanishing scalar
invariant does not certify vacuum**, which is precisely the check ad-hoc constructions skip.

## Method note — a solver result that had to be thrown away

sympy's `dsolve` returns a **bogus** closed form for the R=0 ODE (an *r-dependent exponent*,
`r^{-(M+r)/(r-2M)}`, together with spurious `log(r)` terms). The solution reported above was **hand-derived**
by integrating h′ ∝ r^{−1/2}(r−2M)^{−3/2} and then **verified by substitution** — the production script
performs that substitution check and prints the residual (0). No result here rests on the solver's output.

A second practical note: recomputing Christoffels from scratch with the √ profile makes `simplify` thrash
(the first run had to be killed after 10+ minutes). Substituting h into the already-computed general-h Ricci
is equivalent and reduces the whole run to ~4 s; non-vanishing of components is then established by a
nonzero numeric probe, which is decisive.

## Honest limits (frozen in advance)

- The theorem is proved **for this deformation family** — static, spherically symmetric, g_tt-multiplier with
  g_rr untouched — which is exactly the family ad-hoc "bumpy" constructions use. It is **not** a claim about
  all deformations of all vacuum metrics.
- The complementary case is worth stating and is *not* re-proved here: if you also adjust g_rr so the product
  A·B stays constant, the remaining vacuum equation forces Schwarzschild with a shifted mass (Birkhoff). So
  ad-hoc surgery either **breaks vacuum** or **merely relabels the mass** — never yields a new vacuum.
- **No novelty claimed** — Birkhoff's theorem is textbook. The payout is the *explicit obstruction* (the h′
  identity) and the *explicit counterexample* to "invariants look vacuum ⇒ vacuum", in the form a bumpy-BH
  practitioner would actually need.
- K4b is exact in ε; the O(ε) linearisation is used for **K4c only**.

## Inputs (read-only) & artifacts

Birkhoff's theorem · [leg Y](../../legY_ck_adjudication) `verify_bumpy_vacuum.py` (ansatz §119's bumpy entry,
independently recomputed by the bridge) · leg O/Q's bumpy catalogue entry. `code/k4_bumpy.py` ·
`results/k4_bumpy.json`. Interpreter: conjecture_machine `.venv` (sympy 1.14.0).
