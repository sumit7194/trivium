#!/bin/bash
# fleet_watch.sh: an unattended watcher that needs NO Claude session (written 2026-10-23 after the trip's monitoring gap).
# Reads tools/fleet_watch.conf. Each non-comment line is:
#     name | pidfile | restart command (or -) | max restarts | [logfile::pattern to alert on, optional]
# Every INTERVAL seconds, for each entry whose pidfile exists:
#   - if the pid is alive: ok;
#   - if the pid is gone and the pidfile still exists (the job did not remove it on a clean finish):
#       log an alert, send a macOS notification, and, if a restart command is given and the restart budget remains,
#       run it once (the job's own resume logic continues from its checkpoints).
#   - Entries without a pidfile are skipped (not started, or finished cleanly).
#   - Optional 5th field: alert once each time 'pattern' newly appears in 'logfile' (e.g. a launcher's GAVE UP line,
#     which a job may write while removing its own pidfile).
# Alerts go to ALERTS.md in the repo root. Launch:  nohup bash tools/fleet_watch.sh > /dev/null 2>&1 &
# Stop:  kill $(cat tools/.fleet_watch.pid)
set -u
ROOT=/Users/sumit/Github/TheBridge
CONF=${FLEET_WATCH_CONF:-$ROOT/tools/fleet_watch.conf}
ALERTS=${FLEET_WATCH_ALERTS:-$ROOT/ALERTS.md}
STATE=${FLEET_WATCH_STATE:-$ROOT/tools/.fleet_watch.state}
INTERVAL=${FLEET_WATCH_INTERVAL:-300}
echo $$ > ${FLEET_WATCH_PIDFILE:-$ROOT/tools/.fleet_watch.pid}
touch "$STATE"
alert () {
  echo "- $(date '+%F %T')  $1" >> "$ALERTS"
  /usr/bin/osascript -e "display notification \"$1\" with title \"Fleet watch\"" >/dev/null 2>&1 || true
}
[ -f "$ALERTS" ] || echo "# Fleet alerts (written by tools/fleet_watch.sh; newest at the bottom)" > "$ALERTS"
alert "fleet_watch started (pid $$, interval ${INTERVAL}s)"
# baseline: patterns already present at start are not re-alerted
while IFS='|' read -r name pidfile cmd maxr watchspec; do
  name=$(echo "$name" | xargs); watchspec=$(echo "${watchspec:-}" | xargs)
  [ -z "$name" ] && continue; case "$name" in \#*) continue;; esac
  [ -n "$watchspec" ] || continue
  lf=${watchspec%%::*}; pat=${watchspec#*::}
  n=$(grep -c -- "$pat" "$lf" 2>/dev/null || true); echo "SEEN $name ${n:-0}" >> "$STATE"
done < "$CONF"
while true; do
  while IFS='|' read -r name pidfile cmd maxr watchspec; do
    name=$(echo "$name" | xargs); pidfile=$(echo "$pidfile" | xargs); cmd=$(echo "$cmd" | xargs); maxr=$(echo "${maxr:-0}" | xargs)
    [ -z "$name" ] && continue; case "$name" in \#*) continue;; esac
    watchspec=$(echo "${watchspec:-}" | xargs)
    if [ -n "$watchspec" ]; then
      lf=${watchspec%%::*}; pat=${watchspec#*::}
      n=$(grep -c -- "$pat" "$lf" 2>/dev/null || true); n=${n:-0}
      seen=$(grep "^SEEN $name " "$STATE" | tail -1 | awk '{print $3}'); seen=${seen:-0}
      if [ "$n" -gt "$seen" ]; then echo "SEEN $name $n" >> "$STATE"; alert "$name: '$pat' appeared in $(basename "$lf"): $(grep -- "$pat" "$lf" | tail -1 | cut -c1-120)"; fi
    fi
    [ -f "$pidfile" ] || continue
    pid=$(cat "$pidfile" 2>/dev/null)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then continue; fi
    used=$(grep -c "^$name " "$STATE" 2>/dev/null || true); used=${used:-0}
    if [ "$cmd" != "-" ] && [ "$used" -lt "$maxr" ]; then
      echo "$name $(date +%s)" >> "$STATE"
      alert "$name: process $pid gone without a clean finish; restart $((used+1))/$maxr: $cmd"
      (eval "$cmd") >/dev/null 2>&1 &
      sleep 30
    else
      if ! grep -q "^GAVEUP $name" "$STATE"; then
        echo "GAVEUP $name" >> "$STATE"
        alert "$name: process $pid gone; NOT restarted (no command or restart budget used). Needs a human."
      fi
    fi
  done < "$CONF"
  sleep "$INTERVAL"
done
