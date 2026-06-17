# Leg 1b — Pre-registration: the Kerr extension of leg 1

*Frozen 2026-06-17, before any Kerr observable is computed. Discipline: THE_BRIDGE.md §2,
§4A. Extends [leg1_moduli_count](../leg1_moduli_count/FINDINGS.md) to the rotating family —
the doc's literal headline "Kerr = 2, Kerr–Newman = 3."*

This is still the **ansatz ↔ tabula** leg: does tabula's neural bottleneck count of the
observable manifold equal ansatz's exact moduli count, now for **rotating** holes?

## 1. Why this needs new bridge code (and how it stays faithful)

ansatz emits exact observables only for the *static* lapse (`45_observables.py`), so leg 1
used the static charged family. For rotation we write **new bridge code** that imports
ansatz's engine **read-only**: `44_discover_rotating.kerr_delta_metric(Δ)` builds the
**exact** Kerr / Kerr–Newman metric in Boyer–Lindquist `(t, r, u=cosθ, φ)`, and we derive
equatorial geodesic observables from its *exact* components. ansatz stays the metric
oracle; the bridge derives observables from that exact metric via standard
stationary-axisymmetric geodesic conditions — no hand-coded textbook (Bardeen) formulas.

- **Kerr:** Δ = r² − 2Mr + a²  → parameters `(M, a)`.
- **Kerr–Newman:** Δ = r² − 2Mr + a² + Q²  → parameters `(M, a, Q)`.

## 2. The observables (equatorial plane u=0, all from the exact metric)

From the exact `g_tt(r), g_tφ(r), g_φφ(r)` and their r-derivatives:
- **horizon** r₊ (largest root of Δ=0);
- **circular-orbit angular velocity** Ω±(r) = (−g_tφ′ ± √(g_tφ′² − g_tt′ g_φφ′)) / g_φφ′;
- **photon orbits** r_ph^{±} (prograde/retrograde): g_tt + 2Ω± g_tφ + Ω±² g_φφ = 0;
- **ISCO** r_isco^{±}: marginal stability, dE±/dr = 0 (E± = specific energy of circular orbit);
- **frame-dragging** ω(r) = −g_tφ/g_φφ at fixed probe radii — the *rotation-specific*
  observable (≡ 0 for a=0);
- **redshift** proxies from g_tt at fixed probe radii.

Sanity gates (instrument validation, not predictions): at a=0, Q=0 the code must return
r_ph = 3M, r_isco = 6M, ω = 0.

## 3. Predicted counts (frozen) — ansatz exact moduli vs tabula neural intrinsic dim

| Family | params | ansatz `N_dim` | ansatz `N_shape` (M scaled out) |
|---|---|---|---|
| **Kerr** | (M, a) | **2** | **1** (a/M) |
| **Kerr–Newman** | (M, a, Q) | **3** | **2** (a/M, Q/M) |

tabula predictions (carried): `d* = N_dim` and `d* = N_shape` respectively, via the same
whitened bottleneck-AE knee rule as leg 1 (count = # widths d≥1 with whitened marginal
R² gain > 2%, ≥3 seeds).

### The headline sub-prediction (the contrast with leg 1)
The exact equatorial metric (from ansatz's `kerr_delta_metric`) has a clean structure:
- `g_tt = −(r²−2Mr+Q²)/r²` — **a-independent** (probes M, Q);
- `g_tφ = −a(2Mr−Q²)/r²` — **frame-dragging ∝ a** (probes a);
- horizons `r± = M ± √(M²−(a²+Q²))` — depend on **a²+Q²** (the degenerate combination).

So `a²` and `Q²` are degenerate *inside Δ / the horizons*, but the full observable set
breaks the degeneracy because `g_tt` sees Q (not a) and frame-dragging / orbit asymmetry
see a. Leg 1's static dyonic `Q²+P²` degeneracy had **no** observable to break it (3→2);
here the third number **is** recoverable. Therefore:

- **P-K (Kerr): tabula = 2** (dimensionful), **1** (shape).
- **P-KN-full (full observable set): tabula = 3** (dimensionful), **2** (shape) — the third
  number recovered, *unlike* static dyonic.
- **P-KN-deg (Δ-symmetric observables only — quantities that depend on charge/spin solely
  through `a²+Q²`: the two horizons `r±`, and `Δ(rᵢ)/rᵢ²` at fixed radii): tabula = 2**
  (dimensionful) — the `a²+Q²` degeneracy is exposed when only symmetric observables are
  shown.

P-KN-full vs P-KN-deg is a controlled, falsifiable test: the degeneracy lives in Δ
(symmetric set → 2) and is lifted by the symmetry-breaking observables (`g_tt` for Q,
frame-dragging for a) in the full set (→ 3) — the rotating analogue of leg 1, with the
opposite outcome (here the 3rd number is observable).

## 4. Agreement criterion & outcomes (frozen)
- **Agree** on a cell iff tabula `d* == N` (integer). Off-by-one = finding.
- All cells agree → tabula recovers the exact rotating moduli count; the doc's literal
  "Kerr=2, KN=3" is confirmed by an independent neural measurement.
- P-KN-deg shows 2 while P-KN-full shows 3 → confirms frame-dragging as the degeneracy-
  lifting observable (the intended controlled result).
- tabula < N on P-KN-full → an unexpected rotating degeneracy; investigate which observable
  pair collapses (measurement-vs-engine check, §7).

## 5. Deliverables
- `code/kerr_observables.py` — imports `kerr_delta_metric` read-only, derives the exact
  equatorial observables, samples Kerr / KN objects, writes obs `.npz` (sanity-gated at a=0).
- Reuse leg 1's `count_bottleneck.py` instrument (whitened bottleneck-AE knee).
- `results/` — the count table (Kerr, KN-full, KN-deg) + curves; `FINDINGS.md`.
