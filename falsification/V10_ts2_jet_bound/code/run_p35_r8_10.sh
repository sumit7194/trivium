#!/bin/zsh
# V10 valence 8-10 targets (addendum 2). Guard: kill if RSS > 10 GB or memory free < 10%.
PY=/Users/sumit/Github/conjecture_machine/.venv/bin/python
for r in 8 9 10; do for P in "3/2 1/3" "7/4 -2/5"; do
  $PY -u v10_jet.py ts35 $r ${=P} $((r+1)),$((r+2)) >> ../results/v10_p35_r8_10.log 2>&1 &
  pid=$!
  while kill -0 $pid 2>/dev/null; do
    rss=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' '); free=$(memory_pressure | tail -1 | grep -o '[0-9]*%' | tr -d '%')
    if [[ -n $rss && $rss -gt 10485760 ]] || [[ -n $free && $free -lt 10 ]]; then kill $pid; echo "GUARD KILL r=$r P=$P rss=$rss free=$free" >> ../results/v10_p35_r8_10.log; fi
    sleep 10
  done
done; done
echo DONE >> ../results/v10_p35_r8_10.log
