#!/bin/zsh
# Bridge keepalive. Two jobs, both required:
#   1. rewrite bridge.status every tick so peers can tell "alive and idle" from "dead"
#   2. emit a line ONLY on a state change worth waking the session for
# tabula's point (PROTOCOL 6): a silent monitor is indistinguishable from a dead one.
# So the log gets a timestamped heartbeat even when nothing is emitted upstream.
D=/Users/sumit/Github/.claude-coordination
L=$D/bridge.keepalive.log
prev=""
DECL_AT=$(date +%s)          # when DETAIL was last SET BY A HUMAN DECISION, not by the loop
while true; do
  now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  dage=$(( $(date +%s) - DECL_AT ))
  # Build a COMMA-JOINED list with no trailing separator. The previous form was
  #   pids=$(pgrep ... | tr '\n' ' ')   then   "job_pids":[${pids// /,}]
  # which turns "3501 " into [3501,] -- INVALID JSON. The file therefore parsed
  # cleanly while idle and became unreadable the moment a job started, i.e. it broke
  # exactly when it carried the one number a peer needs before launching. Invisible to
  # every test I ran, because I only ever tested it idle.
  # FILTER TO ACTUAL PYTHON PROCESSES. `pgrep -f` matches any command line CONTAINING
  # the script name -- including the shell of a tool call that merely mentions it. That
  # made the probe report `running` whenever I typed one of these names into a shell,
  # a phantom job caused by the observer. Same cost direction as a stale "busy" file:
  # it blocks a peer's launch on an idle box. quantum's self-match class, one step
  # removed -- theirs matched the keepalive itself, mine matched whoever was watching.
  # So: keep a pid only if its executable really is python.
  pids=""
  for _p in $(pgrep -f "s5_run.py|g3_overnight.py|kt_screen.py" 2>/dev/null); do
    case "$(ps -o comm= -p $_p 2>/dev/null)" in
      *python*) pids="${pids:+$pids,}$_p" ;;
    esac
  done
  if [[ -n "$pids" ]]; then
    rss=$(ps -o rss= -p $pids 2>/dev/null | awk '{s+=$1} END{printf "%d", s/1024}')
    state=running; heavy=true
  else
    rss=0; state=idle; heavy=false
  fi
  free=$(df -g / | awk 'NR==2{print $4}')
  mfree=$(vm_stat | awk '/Pages free/{gsub("\\.","",$3); f=$3} /Pages inactive/{gsub("\\.","",$3); i=$3} END{printf "%.1f", (f+i)*16384/1073741824}')
  # ATOMIC WRITE (blackhole): this machine loses power mid-write. A truncated status
  # file is WORSE than a stale one -- a stale file still parses and expires cleanly
  # through stale_after_s, an unparseable one makes every reader invent a fallback.
  cat > $D/.bridge.status.tmp <<JSON
{"session":"bridge","repo":"/Users/sumit/Github/TheBridge","state":"$state","heavy":$heavy,
 "job_pids":[$pids],"rss_total_mb":$rss,"disk_free_gb":$free,"mem_free_gb":$mfree,
 "heartbeat_pid":$$,
 "stale_after_s":300,"detail":"$DETAIL","declared_age_s":$dage,"updated":"$now",
 "field_semantics":{"MEASURED":["state","heavy","job_pids","rss_total_mb","disk_free_gb","mem_free_gb"],
                    "LIVENESS":"heartbeat_pid is THIS LOOP, which lives as long as the heartbeat does -- ps it to distinguish alive-and-idle from dead. NOT the pid of a short-lived writer: ansatz published $$ of a script that exited milliseconds later, so every read resolved to UNKNOWN forever. A liveness token guaranteed dead is worse than an absent one -- absent is visible, always-dead looks like a working mechanism failing safe.",
                    "DECLARED":["detail"],
                    "note":"MEASURED fields require having looked and cannot be produced by a bumping loop. DECLARED is intent-at-a-time -- read it with declared_age_s, and schedule against the MEASURED fields. (tabula: a heartbeat cannot make a declaration true.)"}}
JSON
  sync 2>/dev/null; mv -f $D/.bridge.status.tmp $D/bridge.status
  sig="$state/$rss"
  if [[ "$sig" != "$prev" ]]; then
    echo "[$now] bridge $state  rss=${rss}MB  memfree=${mfree}GB  disk=${free}GB"
    prev="$sig"
  fi
  echo "[$now] tick $state rss=${rss}MB memfree=${mfree}GB" >> $L
  sleep 60
done
