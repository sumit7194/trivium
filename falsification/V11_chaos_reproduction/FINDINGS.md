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
