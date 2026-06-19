# Move H — Findings: the horizon is a learnability edge (prediction holds, recipe refuted)

*Run 2026-06-20. Predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md). An honest split: the
predictive claim is confirmed strongly; the constructive "recipe" is **refuted** and dropped, per the
pre-registered commitment.*

## Result in one line

The abstract edges finding closes to GR concretely — **a learned emulator of a horizon-diverging
quantity fails *at* the real black-hole horizon** (edge error 85–88× the bulk; the flat null shows
none), so the horizon genuinely *is* a learnability edge. But the proposed **bulk/exact hybrid recipe
does NOT work** for this case: the leading-order near-horizon asymptotic never consistently beats the
learned emulator, so the hybrid loses to pure-learned at every matching radius. Prediction supported;
recipe dropped.

## The numbers

Emulating `Q(r) = 1/√(−g_tt)` (Schwarzschild) and `√(g_rr)` (Kerr) — both → ∞ at the horizon — from
noisy position, on ansatz's exact metric:

| metric | learned edge/bulk | max-err learned | max-err asymptotic | max-err hybrid |
|---|---|---|---|---|
| Schwarzschild | **85×** | 0.052 | 0.442 | 0.071 |
| Kerr | **88×** | 0.053 | 0.443 | 0.063 |
| flat null (Q=r) | 0.5× | — | — | — |

## H1 (the prediction) — SUPPORTED strongly

The learned emulator's relative error is **85–88× larger in the near-horizon band than in the bulk**,
while the **flat null** (a non-diverging `Q=r`) shows **no** edge failure (0.5×). So the failure is
caused by the *metric divergence at the horizon*, not by the emulator — the horizon is a learnability
edge, exactly as the cross-domain finding (Moves E/F/G: learned recovery fails where the metric
diverges) predicts, now on the real Schwarzschild and Kerr horizons. This is the clean, positive
result: the abstract principle makes a correct, controlled prediction about GR.

## H3 (the recipe) — REFUTED, and dropped

The hybrid (learned bulk + exact near-horizon asymptotics) beats the *pure-asymptotic* emulator (0.07
vs 0.44) but **loses to the pure-learned emulator** (0.07 vs 0.05). A post-hoc matching-radius sweep
confirms it is not a tuning problem: **no** matching radius makes the hybrid beat pure-learned (best
0.0529 vs 0.0521), and a point-by-point crossover analysis shows the leading-order asymptotic and the
learned emulator trade off right at the horizon — neither consistently wins. So the recipe is
genuinely refuted for this case, not mis-tuned. Per the pre-registration ("recipe dropped if H3
fails"), **the constructive-recipe claim is withdrawn.**

**Why it failed (the honest mechanism).** The divergence here is *mild* (`1/√(r−r_h)`), so the learned
emulator's edge error, while huge *relatively* (85×), is modest *absolutely* (~5%); and a
*leading-order* asymptotic carries its own O(few-%) error except in a vanishing sliver at the horizon.
The two error sources are comparable, so the exact-asymptotic cannot improve on the learned emulator.
The recipe would plausibly help only for a *stronger* divergence (where the learned error is
catastrophic) or with a *higher-order* asymptotic (accurate over a wider band) — neither claimed here;
both are future work.

## H2 (failure tracks the divergence) — weak

The local learned error correlates with the metric factor `Q` but only modestly (Spearman 0.43
Schwarzschild, 0.56 Kerr; the pre-registered ≥0.8 not met). The error is concentrated at the edge but
its fine rank-ordering with `Q` is noisy.

## The honest take

A new direction, run with the same rigour, that **half-worked and half-failed — and we report both**.
The *diagnostic* half is a genuine, controlled confirmation that the bridge's edges finding predicts
GR emulator failure at the horizon. The *constructive* half — the hoped-for "hand the edge to the
exact structure" recipe — **does not deliver** for a mild divergence with a leading-order asymptotic,
and we drop the claim rather than tune it into apparent success. The useful, defensible statement is:
*learned GR emulators degrade sharply (relatively) at metric-divergence edges; whether an exact-edge
hybrid helps depends on the divergence strength and the asymptotic order, and for the mild `1/√` case
it does not.*

## Honest limits
- Toy single-quantity emulation (not a waveform); one matching radius; leading-order asymptotic only.
- Mild `1/√` divergences; stronger divergences (e.g. `1/(r−r_h)`) are untested and might flip H3.
- kNN emulator; an MLP or more data would change absolute numbers, not the qualitative H1/H3 split
  (the edge failure is from observation-noise amplification at the divergence, model-independent).

## Artifacts
- `code/horizon_learnability.py` — the three emulators on Schwarzschild/Kerr (ansatz exact metric) + flat null.
- `code/plot_horizon.py` — the figure.
- `results/horizon_learnability.json`.
