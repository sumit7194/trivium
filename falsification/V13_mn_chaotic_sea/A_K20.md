# A-K20 (DRAFT for the user's review, 2026-10-18 night): handoff of the located MN chaotic core to quantum's horseshoe stage

**Status: DRAFT.** Not final until the user has reviewed it. Quantum may write code against it, but no registered
run is launched on it until it is marked FINAL.

## What A-K20 hands over
- Per §7, quantum may build MN h-sets only where both screens agree. Both V13 (bridge) and K20 (tabula) find a
  strongly connected core of in-D hyperbolic UPOs with transversal connections at C0 and at F5-R. Sources:
  - V13 FINDINGS, the "§7 tier-2 edge comparison" and "Refinement" sections (c532d82, 70487d7);
  - tabula A13 (SpaceTime 771a5af).
- **Recommended first target: F5-R.** Its parameters are exact rationals, it has the larger shared core
  (6 UPOs, two same-crossing confirmations), and both F5-R period-1 orbits 2 and 4 have same-crossing self-loops.
  C0 is the alternative.

## Exact setup (shared with quantum's B9/B10 conventions)
- **Metric:** Manko–Novikov in the GLM 2008 form, with the axis-regular γ ("−2 outside the sum"). Transcription:
  V9 v9_nve.mn_functions, independently re-verified (V15 V: vacuum to 1e−87, multipoles exact; the Fang 2007 thesis
  agrees on γ).
- **Points (M, a, β):**
  - F5-R = (89, 80, 13394411/1186380);
  - C0 = (1, 9/10, (19/20)/(19/100)^{3/2}).
- **Level:** (E, L_z) = (19/20, 3M) at both. Note L_z = ℓ·M, so F5-R has L_z = 267.
- **Reduced Hamiltonian:** H = ½[g^xx p_x² + g^yy p_y² + W(x, y)] = −½, with the regularised (A-free) W, g^xx and g^yy
  of V13 code/v13_field.py, using the exact identity (x² − 1)(1 − y²)B² − 4C² = A·Q. Gate A2 is PASSED to ≤ 1e−38.
- **Section:** Σ = {y = 0, p_y > 0}, coordinates (x, p_x); p_y is lifted from H = −½ on the positive branch.
- **Domain D = quantum B9:**
  - g_φφ > 0 on the ±0.025 (x, y) box;
  - x − 1 ≥ 0.05;
  - R = √(x² + y² − 1) ≥ 0.5;
  - finite.
  - The strict whole-box recheck passes for every core orbit and connection. SCC boxes clear the CTC region by
    ≥ 7.2e−4 (F5-R) and > 1e−2 (C0).
- **Caveat:** the core lies in the strong-field zone next to the naked ring singularity (V15). The closest approach is
  ~0.1 from the ring point in (x, y), off the equator. h-set enclosures must keep the B9 box margin under interval
  arithmetic (quantum S9).

## Core UPOs and seeds (V13 indices; trace of DP^period, λ_u from λ + 1/λ = trace)

### C0
- Shared SCC core (V13 indices): [1, 3, 4]. Edges confirmed by BOTH codes: 1→1, 3→3 (self-loops; existence confirmed by both codes, different homoclinic points), 2→4 (SAME heteroclinic orbit in both codes), 3→4, 4→1 (both codes; crossing identity inconclusive at 4e-3).

| UPO | period | section points (x, p_x) | trace | λ_u (per period) | min x−1 | min R |
|---|---|---|---|---|---|---|
| 1 | 3 | (2.6284816922, -0.4973728062); (2.0168410001, 0.2507179623); (2.8423399095, 0.4779652564) | -5.250063 | -5.052127 | 1.0168 | 1.7515 |
| 3 | 3 | (2.8423399095, -0.4779652564); (2.0168410001, -0.2507179623); (2.6284816922, 0.4973728062) | -5.250063 | -5.052127 | 1.0168 | 1.7515 |
| 4 | 1 | (3.6213325174, -0.0000000000) | 7.867130 | 7.737896 | 2.6213 | 3.4805 |

### F5R
- Shared SCC core (V13 indices): [2, 3, 4, 6, 7, 8]. Edges confirmed by BOTH codes: 2→2 and 4→4 (same crossing in both codes, ≤1e-6), 2→4, 3→3, 4→2, 4→8, 6→3, 6→6, 8→2 (both codes).

| UPO | period | section points (x, p_x) | trace | λ_u (per period) | min x−1 | min R |
|---|---|---|---|---|---|---|
| 2 | 1 | (3.6419361737, 6.0360992808) | -18.052762 | -17.997198 | 2.6419 | 3.5020 |
| 3 | 3 | (2.8351345960, 42.7008610620); (2.6086564716, -44.4884516459); (2.0104594390, 23.8102634036) | -6.068369 | -5.898844 | 1.0105 | 1.7441 |
| 4 | 1 | (3.6419361737, -6.0360992808) | -18.052762 | -17.997198 | 2.6419 | 3.5020 |
| 6 | 3 | (2.8351345960, -42.7008610621); (2.0104594390, -23.8102634043); (2.6086564716, 44.4884516462) | -6.068369 | -5.898844 | 1.0105 | 1.7441 |
| 7 | 3 | (3.3482091281, 0.0000000000); (2.8958122167, -62.6170252389); (2.8958122167, 62.6170252388) | 32.584838 | 32.554120 | 1.8958 | 2.7177 |
| 8 | 1 | (3.6027445056, 0.0000000000) | 8.114560 | 7.989394 | 2.6027 | 3.4612 |
- Transversal connections and crossing points: results/v13_a10_{C0,F5R}.json (multiple shooting, 085ac13), with
  the strict-box margins in results/v13_a10_densebox.json. The tabula-confirmed set is in V13 FINDINGS.
- Eigenvectors (unstable and stable directions at each section point) are in results/v13_upo_{C0,F5R}_19o20_3.json.

## Suggested h-set design inputs (quantum decides; nothing here is binding)
- F5-R: a symbolic system on {2, 4} (period-1, |λ| ≈ 18, same-crossing self-loops at both, plus 2↔4) gives the
  smallest covering chain. Add the period-3 UPOs 3 and 6 only if needed.
- Check every candidate h-set against the strict B9 box test along all covering flowpipes.

## Open items before FINAL
- [ ] User review of this draft.
- [ ] Quantum confirms the field-gate match (S5) between its B10 code and v13_field.py.
