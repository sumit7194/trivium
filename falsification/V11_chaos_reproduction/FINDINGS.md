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
