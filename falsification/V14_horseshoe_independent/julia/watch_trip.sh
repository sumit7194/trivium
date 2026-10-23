#!/bin/bash
# Event-only watcher for the trip runs (no agent work between events). Exits with a one-line reason on the first event.
V=/Users/sumit/Github/TheBridge/falsification/V14_horseshoe_independent/results
T=/Users/sumit/Github/SpaceTime/curvature/results
done0=$(cat $V/q2u.log $V/q3s.log 2>/dev/null | grep -c " DONE ")
while true; do
  sleep 300
  d=$(cat $V/q2u.log $V/q3s.log 2>/dev/null | grep -c " DONE ")
  [ "$d" -gt "$done0" ] && { echo "EVENT V14 covering finished: $(cat $V/q2u.log $V/q3s.log 2>/dev/null | grep ' DONE ' | tail -1 | cut -c1-200)"; exit 0; }
  grep -q "WATCHDOG\|STOPPED\|chain finished" $V/CHAIN_STATUS.md && { echo "EVENT V14 status: $(tail -2 $V/CHAIN_STATUS.md)"; exit 0; }
  kill -0 "$(cat $V/chain.pid 2>/dev/null)" 2>/dev/null || { echo "EVENT V14 chain process gone"; exit 0; }
  /usr/bin/python3 -c "import json,sys;s=json.load(open('$T/198_status.json'));sys.exit(0 if (s.get('errors') or s.get('verdict')) else 1)" 2>/dev/null && { echo "EVENT tabula status: errors/verdict present"; exit 0; }
  kill -0 "$(cat $T/198_launcher.pid 2>/dev/null)" 2>/dev/null || { echo "EVENT tabula launcher gone (finished or died)"; exit 0; }
  kill -0 24176 2>/dev/null || { echo "EVENT quantum B15 (24176) exited"; exit 0; }
done
