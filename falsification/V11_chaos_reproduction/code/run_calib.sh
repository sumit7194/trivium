#!/bin/zsh
# V11 addendum 2 calibration on controls only (ZV layer x2, ZV torus, flagged Kerr orbit)
PY=/Users/sumit/Github/conjecture_machine/.venv/bin/python
$PY -u v11_chaos.py zv 0.95 2.9 7.56263 > ../results/calib_zv29.log 2>&1 &
$PY -u v11_chaos.py zv 0.95 3.0 7.57274 7.62 > ../results/calib_zv30.log 2>&1 &
$PY -u v11_chaos.py kerr45 0.97 1.25 4.44855 > ../results/calib_kerr.log 2>&1 &
wait
echo CALIB_DONE
