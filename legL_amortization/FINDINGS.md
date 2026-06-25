# Leg L — Findings: legibility of the amortized no-hair NPE, and legibility → real precision

*Run 2026-06-24 (backlog A6 + A1; THE_BRIDGE §9 "does amortization predict sim→real transfer?"). Probes the
**richer-information** no-hair δ SBI — the amortized NPE that infers (M, χ, δ) from the full GW250114
ringdown — where leg 2 had only the information-limited tone-count. Imports deepstrain's `sbilib` + trained
posterior read-only; extracts the 56-d Embed summary code on simulated ringdowns with known (M, χ, δ).*

## Result in one line

**(A6)** In the amortized no-hair summary, M and χ are cleanly legible (R² 0.86 / 0.51) but **δ is
information-limited** (linear 0.08, nonlinear 0.09 — *no* legibility gap) — corroborating leg 2's
tone-count result in a *second, richer* deepstrain model and localizing the limit to the no-hair deviation
itself. **(A1)** The per-parameter **sim legibility predicts the real-data posterior precision**: the
ranking M > χ > δ is identical for legibility and for how tightly GW250114 constrains each — concrete
support for §9's amortization→transfer idea.

## A6 — the legibility ladder (linear Ridge vs nonlinear MLP, held-out R²)

| parameter | linear R² | nonlinear R² | gap | reading |
|---|---|---|---|---|
| **M** (mass) | 0.78 | 0.86 | +0.08 | cleanly (linearly) legible |
| **χ** (spin) | 0.53 | 0.51 | −0.02 | cleanly (linearly) legible |
| **δ** (no-hair) | **0.08** | **0.09** | **+0.01** | **information-limited** |

δ — the decisive parameter (the 221-overtone deviation, the hardest signal) — has both probes at the floor
and *no* legibility gap. So δ is **info-limited, not scrambled**: the no-hair signal is genuinely weak, not
nonlinearly buried. This is the *same* verdict leg 2 reached for the tone-count, now reproduced in the
richer NPE — and sharpened: the amortized summary encodes the *easy* parameters (M, χ) well and hits the
information wall precisely on the *hard* one (δ). The no-hair test is **signal-limited, not
encoding-limited** — across two independent deepstrain models. (Reinforces the spine's leg-2/leg-7
"needs more SNR/data" conclusion.)

## A1 — amortization legibility predicts real-data precision

| parameter | sim legibility (R²) | real precision (prior range / 90% CI) on GW250114 |
|---|---|---|
| M | 0.86 | 4.47 |
| χ | 0.51 | 3.52 |
| δ | 0.09 | 1.28 |

The ranking is **identical**: the parameter most legible in the amortized summary (M) is the most tightly
measured on real data; the least legible (δ) is barely constrained. So a **cheap legibility probe on
simulation predicts which parameters the real measurement will pin down** — a concrete instance of §9's
"amortization → transfer."

**Honest mechanism + scope (no overclaim):** both quantities are downstream of the *same* driver — the
data's Fisher information about each parameter — so this is "the amortized summary's legibility tracks the
information content, which sets real precision," a *useful predictive diagnostic*, not a deeper
amortization-gap-causes-overfitting effect. And it is **3 parameters, 1 event** — a clean ranking, not a
large-N correlation. The stronger A1 (does an NPE's amortization *gap* predict transfer *failure* across
*models*) needs several NPEs of varying capacity, which deepstrain would have to train — logged as the
next step.

## Artifacts
- `code/export_nohair_codes.py` — deepstrain side: extracts the no-hair NPE's 56-d Embed summary on 5000
  simulated ringdowns with known (M, χ, δ). `results/nohair_codes.npz`.
- `code/probe_nohair.py` — the legibility ladder + the legibility↔real-precision ranking. `results/probe_nohair.json`.
