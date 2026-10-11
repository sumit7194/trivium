# V11 — Findings

## Validation gate (ZV δ=2, E = 0.95): PASS

| Orbit | rtol 1e−11 | rtol 1e−13 | Verdict |
|---|---|---|---|
| L = 2.9, x0 = 7.56263 | plunge after 187 crossings; S_ex 73.4; fd 0.017 | 300 crossings, no plunge; S_ex **10.7**; fd 0.0006; H drift 3e−13 | CHAOTIC |
| L = 3.0, x0 = 7.57274 | plunge after 267; S_ex 84.7 | 300 crossings; S_ex **19.1**; H drift 3e−13 | CHAOTIC |
| L = 3.0, x0 = 7.62 | S_ex −4.03; fd 3.6e−6 | S_ex −4.03; fd 3.6e−6 | REGULAR |

**Agreement with ansatz.** Classifications match ansatz on all three orbits. The regular torus's S_ex (−4.03) matches
ansatz's ≈ −4 independently, from an exact Jacobian plus DOP853 against central differences plus DP5(4).

**A detector caveat, found here and sent to ansatz.** At rtol 1e−11 both layer orbits PLUNGE, and the H drift at the
final state is huge (~1e8). The plunge leg itself (near the strong-field core) is integrated badly, and its divergence
of nearby orbits is real but has nothing to do with the layer's chaos. Both inflate S_ex (73, 85). The rtol 1e−13
runs don't plunge within 300 crossings and give S_ex 10.7 and 19.1. Those values are uncontaminated and still
≥ 10, but L = 2.9 is marginal.
- **Recommendation:** compute S_ex only up to the last section crossing BEFORE a plunge, and report the H drift over
  the same window.
- The pre-registered classification rule is unchanged here. Both tolerances say CHAOTIC, so the gate passes as
  registered. The caveat applies to future candidates.

## Calibration (addendum 2), on controls only

| Control | rtol | Outcome | S_trunc | fd | R | Carter max rel. dev | H drift |
|---|---|---|---|---|---|---|---|
| Kerr flagged (kerr45, E 0.97, L 1.25, x0 4.44855) | 1e−11 | 300 crossings, no plunge | −1.5 | 0.0011 | 0.0115 | 1.0e−10 | 5e−11 |
| same | 1e−13 | 300 crossings, no plunge | 4.0 | 0.0001 | 0.0052 | 6.5e−13 | 4e−13 |
| ZV layer, L 2.9, x0 7.56263 | 1e−11 / 1e−13 | plunge at 186 / 300 crossings | 14.6 / 9.6 | 0.017 / 1e−4 | 0.044 / 0.002 | – | – |
| ZV layer, L 3.0, x0 7.57274 | 1e−11 / 1e−13 | 300 / plunge at 296 | 19.8 / 23.1 | 0.0055 / 0.0145 | 0.0015 / 0.58 | – | – |
| ZV torus, x0 7.62 | both | 300 crossings | −4.0 | 0 | 0.0008 | – | – |

**The flagged Kerr orbit is REGULAR in V11 at both tolerances.** Carter is conserved to 1e−10 and 6e−13, the orbit
never plunges, and S_ex stays below 10. That independently confirms ansatz's resolution: its 1e−11 plunge was
integration error. V11's 8th-order DOP853 doesn't produce it.

**Neither geometric diagnostic separates the controls.** Regular Kerr reaches R = 0.0115, which is above the layer's
0.0015–0.002 realisations, and D is broken. So per addendum 2, R is reported only. The primary V11 criterion is the
addendum-4 basin structure.

**The layer realisations are sticky and inconsistent** (see addendum 3). That is why the single-orbit classification
gave INCONCLUSIVE for L 2.9 on this build.

## Ensembles a–g (addenda 3–5), run 2026-10-10/11: ALL INCONCLUSIVE, the instrument failed its design
- **TS sides:**
  - most neighbours ended "capped" (the 3M-evaluation cap), not "plunge";
  - e.g. ensemble d had all 9 capped;
  - the TS boundary search found "capped | survive" edges, not "plunge | survive".
- **Kerr sides:**
  - the scan found NO plunge/survive transition at any matched level;
  - e.g. ensemble a: 138 survive, 45 capped, 1 plunge;
  - so the Kerr ensembles were never built and the verdict rule could not apply.
- **Diagnosis:**
  - Orbits heading into the strong-field core stiffen, and DOP853 at rtol 1e−13 exhausts the evaluation budget before
    they reach the x < 1.5 plunge cut.
  - So "capped" here mostly means "plunging into the core", not "numerical stall near a singularity".
  - Addendum 5's rule (capped is neither S nor P) therefore removed exactly the plunge outcomes the basin score needs.
- **Descriptive only (no verdict):**
  - TS ensemble b shows S/P/capped interleaving (T = 2 over non-capped members);
  - the others show survive vs capped patterns.
- **Status:** V11 provides NO independent confirmation yet. ansatz §150 (α, the matched table) stands on its own
  instrument. Any V11 rerun with a physically defined plunge criterion (inside the barrier radius, moving inward) and a
  stall-based (per-chunk) cap would be POST-DATA and labelled as such.

### Root cause of the a–g failure (diagnosed 2026-10-11): a bug, not physics
The plunge check ran only at chunk ends. Orbits that crossed x = 1.5 mid-chunk fell into the (x, y) → (1, ±1) corner
and crawled until capped. That was misread at first as stiffness, then as inner-region trapping; the direct trace
shows a plain plunge.

Fixed in addendum 6 (terminal plunge and escape events; a per-chunk stall guard). The regular controls are unchanged.
A rerun is scheduled post-failure.

## Rerun of ensembles a–g after addendum 6 (POST-FAILURE), 2026-10-11

| Ens | TS (E, L) | TS T / V (capped) | Kerr T / V | Kerr Carter max | Verdict |
|---|---|---|---|---|---|
| a | ts45 (0.95, -6.25) | 1 / 1 (0) | (0, 0) | 3.1e-13 | **INCONCLUSIVE** |
| b | ts45 (0.97, -6.25) | 2 / 2 (0) | (0, 0) | 2.4e-13 | **CONFIRMED** |
| c | ts45 (0.97, 6.25) | 4 / 2 (0) | (0, 0) | 5.0e-13 | **CONFIRMED** |
| d | ts45 (0.95, -5.125) | 0 / 4 (0) | (1, 0) | 1.3e-12 | **CONFIRMED** |
| e | ts35 (0.97, 5.333) | 1 / 1 (0) | no Kerr transition | — | **INCONCLUSIVE** |
| f | ts35 (0.97, 11.83) | 2 / 3 (0) | no Kerr transition | — | **INCONCLUSIVE** |
| g | ts35 (0.97, 6.333) | 1 / 2 (0) | no Kerr transition | — | **INCONCLUSIVE** |

**Reading:**
- **3 of 7 CONFIRMED (b, c, d).** TS shows interleaved or non-monotone escape structure (T ≥ 2 or V ≥ 2). The matched Kerr
  ensembles are clean (T ≤ 1, V = 0) with Carter conserved to ≤ 1.3e−12.
- **a: INCONCLUSIVE.** TS has T = 1, V = 1, below the bar.
- **e, f, g (the p = 3/5 levels): INCONCLUSIVE.** The Kerr scan found NO survive/plunge transition at the same E and
  L/m, so no Kerr ensemble could be built. The TS sides show T/V = 1/1, 2/3 and 1/2.
- **Design limitation:** addendum 3 matched Kerr by L/m, not by distance to each system's OWN separatrix. ansatz §150
  matches by ε_sep, which is the better matching. Recorded as a lesson, not changed post-data.
- **Net:** V11 independently CONFIRMS the TS-vs-Kerr basin-structure contrast at 3 of 4 p = 4/5 candidates. No candidate
  contradicts it: every Kerr ensemble built is clean, and no TS ensemble reads integrable-clean except a, which is
  borderline. This is a post-failure rerun, labelled as such.

**Environment (back-filled 2026-10-11, per the fleet reproducibility policy):** CPython 3.14.5,
`/Users/sumit/Github/conjecture_machine/.venv`; numpy 2.4.6 (Accelerate), scipy 1.18.0, sympy 1.14.0, mpmath 1.3.0,
numba 0.65.1; macOS 26.5 arm64. Pinned in `ENVIRONMENT/` (bridge_env.json, bridge_requirements.lock). Assumed
unchanged since the run; the venv was not upgraded in between.
