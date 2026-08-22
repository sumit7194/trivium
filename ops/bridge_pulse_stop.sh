#!/bin/zsh
# Stop the bridge pulse loop WITHOUT signalling by name.
# `pkill -f <word>` is a broadcast across a shared box: it killed my loop four times
# and would have taken tabula's and ansatz's with it. Kill by PID, and verify identity
# first -- a recycled PID is as dangerous to signal as it is to trust.
D=/Users/sumit/Github/.claude-coordination
P=$(cat $D/bridge.pulse.pid 2>/dev/null)
[[ -z "$P" ]] && { echo "no pidfile"; exit 0; }
if ps -o command= -p $P 2>/dev/null | grep -q bridge_pulse; then
  kill $P && echo "stopped $P (identity verified)"
else
  echo "pid $P is not the pulse loop (dead, or PID recycled) — NOT signalling"
fi
