#!/bin/zsh
# V11 addendum 3 ensembles for ansatz's orbits a)-g), three lanes in parallel
PY=/Users/sumit/Github/conjecture_machine/.venv/bin/python
lane(){ for spec in "$@"; do $PY -u v11_ensemble.py ${=spec} >> ../results/ens_run.log 2>&1; done }
lane "ts45 0.95 -6.25 5.538637 2.5 kerr45 1.25 a" "ts45 0.95 -5.125 5.935068 2.5 kerr45 1.25 d" "ts35 0.97 6.333333333333333 13.473771 3.3333333333333335 kerr35 1.6666666666666667 g" &
lane "ts45 0.97 -6.25 5.195279 2.5 kerr45 1.25 b" "ts35 0.97 5.333333333333333 12.866727 3.3333333333333335 kerr35 1.6666666666666667 e" &
lane "ts45 0.97 6.25 10.384509 2.5 kerr45 1.25 c" "ts35 0.97 11.833333333333334 16.697461 3.3333333333333335 kerr35 1.6666666666666667 f" &
wait
echo ENS_DONE >> ../results/ens_run.log
