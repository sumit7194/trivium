# V8-mono — Pre-registration: the bridge reproduces quantum's TS δ=2 v2 monodromy certificates (rows 0–5)

*2026-10-05 ~03:30 IST. Written and committed BEFORE any bridge integration. Not blind: quantum's targets are known
(from its cross-session message of ~03:20). The bridge reads none of quantum's files. This closes the gap V8 left open:
the TS monodromy has so far been uncorroborated.*

**Equations: the bridge's own.**
- Ansatz's TS2 metric components feed the bridge's V8 provenance code, which was already Ernst- and twist-checked. That
  code gives the non-reduced ξ₁ coefficients p(x) and q(x), rational in x.
- The chart is x = (t + 1/t)/2, with p_t = x′p − x″/x′ and q_t = x′²q.
- P1 = (p, q) = (3/5, 4/5) and P2 = (4/5, 3/5), with rows as in quantum's message.

**Integrator:** the V9-eq′ code path (DOP853 in complex128, 16-gon CCW loops, Y(z₀) = I, with g and h as matrix
products).

**Gates:**
1. Provenance: the back-converted p, q at x = 5/4 must match `results/v8_ts_provenance.json` to better than 1e−12.
2. Abel: det M must equal exp(−∮p_t), to better than 1e−8.
3. Convergence: tolerances 1e−11 and 1e−13 must agree to better than 1e−7.

**Verdict per row:**
- REPRODUCED if the agreement with quantum's midpoints of tr²/det(g), tr²/det(h) and tr[g,h] is better than 1e−7.
- DISAGREES if it is worse than 1e−5 with the gates passing.
- INCONCLUSIVE otherwise.

quantum's v2 radii are ≤ 1e−17, so the CONSISTENT rule from V9-eq isn't needed.

The result is numerical corroboration, not a certificate.
