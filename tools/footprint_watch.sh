#!/bin/zsh
# Usage: footprint_watch.sh <pid> <cap_MB> <log>. Sums top-reported MEM (resident+compressed) over <pid> AND all its
# descendants (so wrappers such as `timeout` or `nice` are handled); if the sum exceeds cap, TERMs the whole tree.
# 2026-11-20: previously measured <pid> only, which silently guarded the 1 MB `timeout` wrapper instead of python.
pid=$1; cap=$2; log=$3
tree() { local p=$1; echo $p; for c in $(pgrep -P $p 2>/dev/null); do tree $c; done; }
while kill -0 $pid 2>/dev/null; do
  tot=0; pids=($(tree $pid))
  for p in $pids; do
    m=$(top -l 1 -pid $p -stats mem 2>/dev/null | tail -1 | tr -d ' +-')
    mb=$(python3 -c "s='$m'; u=s[-1:]; v=float(s[:-1] or 0); print(int(v*{'K':1/1024,'M':1,'G':1024}.get(u,1/1048576)))" 2>/dev/null)
    [ -n "$mb" ] && tot=$((tot + mb))
  done
  [ "$tot" -gt "$cap" ] && { echo "$(date +%T) KILL tree of $pid (${pids}) at ${tot} MB > ${cap}" >> $log; kill -TERM ${(Oa)pids}; exit 1; }
  sleep 15
done
