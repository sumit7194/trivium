# Morning summary, 19 Oct 2026 (written overnight by the bridge)

## Overnight runs
- **Bridge:** the blind Hénon–Heiles test of the independent proof checker (V14 Q2): 2 processes × 4 threads, started
  22:12. Result: see below once it lands.
- **Quantum:** the rigorous run of the second Hénon–Heiles stage (constructor B14, registered 0b60857, frozen 1da283c),
  7 coverings on 4 cores, checkpointed.
  - Also done: the field-equation cross-check against the bridge's code PASSED (agreement to 4e−70 at all four test
    points and their Kerr limits), plus the B10 gate and a per-piece time cap.
- **Tabula:** finished. Its targeted check gave no formal verdict (its own validity test failed). Informally, every
  bridge-confirmed crossing reproduces in tabula's code.

## Waiting for you
- Review the Manko–Novikov handoff draft:
  `falsification/V13_mn_chaotic_sea/A_K20_DRAFT.md`. Quantum won't run anything on it until you've reviewed it.

## Bridge blind Hénon–Heiles test (V14 Q2): partial result at 10:30
- **Proven (4 of 7 required):** M0⇒M0, M0⇒M1, M4⇒M0, M4⇒M1.
- **Wrong configurations, both correctly REJECTED:** W-AZ1 and W-AZ2.
- **Not proven within the registered limits:** M3⇒M4. Condition (b) passes; (a) still has an undecided piece at the
  maximum refinement depth 6, near one edge of the target set.
- **Still running:** M1⇒M2 (in refinement since 01:35, single core). M2⇒M3 was relaunched at 10:40 as its own job
  with parallel refinement.
