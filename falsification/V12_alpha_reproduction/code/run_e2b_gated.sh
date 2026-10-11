#!/bin/zsh
# E2' (addendum 11): starts after the extension queue (outer, E2, E1) has finished, then waits for the load gate.
cd "$(dirname "$0")"
until grep -q ALL_EXT_DONE ../results/v12_ext.log; do sleep 60; done
while true; do
  l5=$(sysctl -n vm.loadavg | awk '{print $3}')
  if (( $(echo "$l5 < 8" | bc -l) )); then echo "$(date +%T) gate open (E2b): load5=$l5"; break; fi; sleep 60
done
/Users/sumit/Github/conjecture_machine/.venv/bin/python -u v12_run.py E2b 6; echo "E2b EXIT $?"
