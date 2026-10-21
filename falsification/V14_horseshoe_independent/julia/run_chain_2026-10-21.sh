#!/bin/bash
# V14 unattended chain (PREREGISTRATION.md: Q2-U then Q3-S). Plain processes only; no agents needed.
# Launch (from V14_horseshoe_independent):  nohup bash julia/run_chain_2026-10-21.sh > results/chain.log 2>&1 &
# Stop cleanly:  kill $(cat results/chain.pid)    (the trap also stops the running Julia job)
set -u
cd /Users/sumit/Github/TheBridge/falsification/V14_horseshoe_independent
JULIA=/Users/sumit/.julia/juliaup/julia-1.13.2+0.aarch64.apple.darwin14/Julia-1.13.app/Contents/Resources/julia/bin/julia
STATUS=results/CHAIN_STATUS.md
HEART=results/CHAIN_HEARTBEAT.txt
LIMIT_KB=11534336      # 11 GB: the watchdog kills only this chain's own Julia PID above it
PIDFILE=results/chain.pid
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "REFUSED: chain $(cat "$PIDFILE") already running" >&2; exit 1
fi
echo $$ > "$PIDFILE"
CHILD=""
trap 'echo "- $(date "+%F %T") STOPPED by signal" >> "$STATUS"; [ -n "$CHILD" ] && kill "$CHILD" 2>/dev/null; rm -f "$PIDFILE"; exit 143' TERM INT
[ -f "$STATUS" ] || echo "# V14 chain status (Q2-U, then Q3-S)" > "$STATUS"
echo "- $(date '+%F %T') chain (re)started, pid $$, git $(git -C /Users/sumit/Github/TheBridge rev-parse --short HEAD)" >> "$STATUS"

run_job () {
  local job=$1 log=$2
  echo "- $(date '+%F %T') START $job -> $log" >> "$STATUS"
  Q2_MAXDEPTH=10 Q2_LEAFPOW=20 nice -n 5 "$JULIA" -t 6 --heap-size-hint=8G --project=julia julia/q2u_main.jl "$job" >> "$log" 2>&1 &
  local pid=$!; CHILD=$pid
  echo "  julia pid $pid" >> "$STATUS"
  while kill -0 "$pid" 2>/dev/null; do
    local rss; rss=$(ps -o rss= -p "$pid" 2>/dev/null | tr -d ' ')
    if [ -n "$rss" ] && [ "$rss" -gt "$LIMIT_KB" ]; then
      echo "- $(date '+%F %T') WATCHDOG: killing $pid (rss ${rss} KB > ${LIMIT_KB})" >> "$STATUS"; kill "$pid"
    fi
    { echo "$(date '+%F %T')  job $job  pid $pid  rss_KB ${rss:-?}"; grep -h "DONE\|refinement:\|level 3:" "$log" 2>/dev/null | tail -3; } > "$HEART"
    sleep 60
  done
  wait "$pid"; local rc=$?; CHILD=""
  echo "- $(date '+%F %T') END $job rc=$rc" >> "$STATUS"
  grep -h "DONE" "$log" | sed 's/^/    /' >> "$STATUS"
}

run_job U results/q2u.log
run_job S results/q3s.log
echo "- $(date '+%F %T') chain finished" >> "$STATUS"
rm -f "$PIDFILE"
