#!/bin/zsh
# Stop the bridge pulse loop WITHOUT signalling by name.
# `pkill -f <word>` is a broadcast across a shared box: it killed my loop four times
# and would have taken tabula's and ansatz's with it. Kill by PID, and verify identity
# first -- a recycled PID is as dangerous to signal as it is to trust.
D=/Users/sumit/Github/.claude-coordination
P=$(cat $D/bridge.pulse.pid 2>/dev/null)
[[ -z "$P" ]] && { echo "no pidfile"; exit 0; }
if ps -o command= -p $P 2>/dev/null | grep -q bridge_pulse; then
  # `kill $P && echo ...` was silent on failure -- and a stop script that fails silently
  # leaves the old loop running while the caller proceeds to start a new one. I have used
  # this script a dozen times today before relaunching; one silent failure would have
  # given me two writers, which is the duplicate-heartbeat state that makes people reach
  # for `pkill -f` and started this whole thread. (quantum's rule: MAKE SILENCE
  # IMPOSSIBLE -- every check reports on both branches.)
  if kill $P 2>/dev/null; then
    echo "stopped $P (identity verified)"
  else
    echo "FAILED to signal $P -- it may still be running; DO NOT start another writer"
    exit 1
  fi
else
  echo "pid $P is not the pulse loop (dead, or PID recycled) — NOT signalling"
fi
