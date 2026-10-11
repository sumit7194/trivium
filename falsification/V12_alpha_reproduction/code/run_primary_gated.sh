#!/bin/zsh
# V12 primary: start only when the 5-min load < 8 and free+inactive >= 3 GB (pre-registered resource rule)
cd "$(dirname "$0")"
while true; do
  l5=$(sysctl -n vm.loadavg | awk '{print $3}')
  pg=$(vm_stat | awk '/Pages free/ {f=$3} /Pages inactive/ {i=$3} END {gsub(/\./,"",f); gsub(/\./,"",i); print (f+i)*16384/1073741824}')
  if (( $(echo "$l5 < 8" | bc -l) )) && (( $(echo "$pg >= 3" | bc -l) )); then break; fi
  echo "$(date +%T) waiting: load5=$l5 freeGB=$pg"; sleep 60
done
echo "$(date +%T) gate open: load5=$l5 freeGB=$pg"
/Users/sumit/Github/conjecture_machine/.venv/bin/python -u v12_run.py primary 6
echo "PRIMARY EXIT $?"
