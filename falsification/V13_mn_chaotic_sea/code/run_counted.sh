#!/bin/sh
# V13 counted screens in sequence (one core, nice 10). p2's run 1 sampled only its single bound-in-D component, so it
# stands. p1 is rerun after the sampling fix (run 1 kept as INVALID); then F5-R; then the structure stage.
PY=/Users/sumit/Github/conjecture_machine/.venv/bin/python
cd "$(dirname "$0")"
for k in p1 F5R; do nice -n 10 $PY -u -W ignore v13_screen.py counted $k; done
nice -n 10 $PY -u -W ignore v13_upo.py p1 37/40 29/10 3 10 5
nice -n 10 $PY -u -W ignore v13_upo.py p2 37/40 3 3 10 5
nice -n 10 $PY -u -W ignore v13_upo.py F5R 19/20 3 3 10 5
for f in ../results/v13_upo_p1_37o40_29o10.json ../results/v13_upo_p2_37o40_3.json ../results/v13_upo_F5R_19o20_3.json; do
  nice -n 10 $PY -u -W ignore v13_manifolds.py $f 5 1e-7
done
