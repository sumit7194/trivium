#!/bin/zsh
# V12 extensions in sequence (outer secondary, E2, E1); each waits for load5 < 8 and >= 3 GB free+inactive.
cd "$(dirname "$0")"
gate() {
  while true; do
    l5=$(sysctl -n vm.loadavg | awk '{print $3}')
    pg=$(vm_stat | awk '/Pages free/ {f=$3} /Pages inactive/ {i=$3} END {gsub(/\./,"",f); gsub(/\./,"",i); print (f+i)*16384/1073741824}')
    if (( $(echo "$l5 < 8" | bc -l) )) && (( $(echo "$pg >= 3" | bc -l) )); then echo "$(date +%T) gate open ($1): load5=$l5"; return; fi
    sleep 60
  done
}
for m in outer E2 E1; do gate $m; /Users/sumit/Github/conjecture_machine/.venv/bin/python -u v12_run.py $m 6; echo "$m EXIT $?"; done
echo ALL_EXT_DONE
