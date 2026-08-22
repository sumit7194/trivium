# Do the gates actually FAIL? — mutation test, 2026-08-22

blackhole's point, and it is the one that separates a gate from a decoration:

> A margin audit tests whether gates sit at reachable bars. It never tests whether a gate actually
> **fails** when its artifact is wrong — and a gate asserting on a mistyped key passes forever and looks
> identical to a healthy one.

So: corrupt each artifact, confirm the gate goes red. Run from a **fresh clone**, not the working tree,
because a gate that silently reads an untracked file passes here and fails for everyone else.

## Fresh-clone run (`git clone` → run every gate)

| gate | result |
|---|---|
| `G3_chaos_boundary/code/gate_boundary.py` | 15 PASS, 0 FAIL, rc=0 |
| `Q2_corner_kappa/code/gate_s5.py` | 4 PASS, 0 FAIL, rc=0 |
| `A1_kt_screen/code/kt_screen.py 2.0 2 0 40` | `conserved = 4` — matches §124 |

**This test is why the Q2 gate exists at all in runnable form.** The first fresh-clone attempt failed:
`.gitignore` line 3 is `*.npz`, written for bulk regenerable arrays, and it had swept up
`s5_spectra.npz` — 1.2 MB, and the gate's only input. ansatz hit the identical class the same hour
(a rule aimed at 2.6 GB of pickles swept 176 KB of run logs). **An ignore rule chosen for size is not a
judgement about evidentiary value, and it silently becomes one.**

## Mutation test (corrupt the artifact, gate must go red)

| mutation | rc | verdict |
|---|---|---|
| G3: flip **one** orbit's `escaped` flag (of 629) | 1 | caught |
| G3: perturb 5 control `drift_fft` values by 1.5× | 1 | caught |
| Q2: scale `nn` spectrum by **1.001** at l=20 only | 1 | caught |
| Q2: delete the `smeared` regulator entirely | 1 | caught |

4/4. The single-orbit and 0.1% mutations matter most: they confirm the gates are sensitive at the scale
the *claims* are made at, not merely to gross damage.

## What this does not establish

Passing gates on **correct** artifacts, plus failing on **corrupted** ones, shows the gate is coupled to
the data. It does not show the reduction is the right one — `S_at()` and the Fisher contingency table
could both be wrong in a way the gate faithfully reproduces. **A gate protects a number against drift; it
does not make the number true.**
