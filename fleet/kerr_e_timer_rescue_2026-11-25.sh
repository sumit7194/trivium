#!/bin/zsh
# Cancel the 48 h timer inside the running kerr_e chunks. The computation is untouched.
# For each PID: check it is the expected chunk, attach, alarm(0), detach, resume, and log.
LOG=/Users/sumit/Github/TheBridge/fleet/kerr_e_timer_rescue_2026-11-25.log
typeset -A CHUNK
CHUNK=(6670 N3N4 6675 N4N5 6677 N5N0 93687 N5N1)
for pid in 6670 6675 6677 93687; do
  want="kerr_e/${CHUNK[$pid]}.spec"
  args=$(ps -o args= -p $pid)
  if [[ "$args" != *hs_cover_b15d* || "$args" != *$want* ]]; then
    echo "$(date '+%F %T') SKIP pid $pid: not $want (args: $args)" | tee -a $LOG; continue
  fi
  out=$(lldb -p $pid --batch -o "expr (unsigned int)alarm(0)" -o detach 2>&1)
  left=$(print -r -- "$out" | grep -o '\$0 = [0-9]*' | grep -o '[0-9]*$')
  kill -CONT $pid
  st=$(ps -o stat= -p $pid)
  echo "$(date '+%F %T') pid $pid ${CHUNK[$pid]}: timer had ${left:-UNKNOWN} s left, alarm(0) called, detached, resumed; state now '$st'; computation untouched" | tee -a $LOG
  [[ -z "$left" ]] && print -r -- "$out" | tail -20
done
echo "done"
