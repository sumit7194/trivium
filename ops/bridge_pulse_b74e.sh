#!/bin/zsh
# Bridge keepalive. Two jobs, both required:
#   1. rewrite bridge.status every tick so peers can tell "alive and idle" from "dead"
#   2. emit a line ONLY on a state change worth waking the session for
# tabula's point (PROTOCOL 6): a silent monitor is indistinguishable from a dead one.
# So the log gets a timestamped heartbeat even when nothing is emitted upstream.
D=/Users/sumit/Github/.claude-coordination
L=$D/bridge.pulse.log
PIDFILE=$D/bridge.pulse.pid
# NAME CHOSEN TO COLLIDE WITH NOTHING. This loop was killed four times today by
# `pkill -f keepalive` run in ANOTHER session -- that pattern matches six processes
# across three sessions here. nohup/disown/os.setsid were all irrelevant: none of them
# protect against being signalled by name, and the signal was never coming from my
# process tree. (quantum's diagnosis; the decisive asymmetry was that their loop
# survived only because its name lacks the substring.)
#   A PROCESS-NAME PATTERN IS NOT A PRIVATE NAMESPACE. `pkill -f <word>` IS A BROADCAST.
# Verified before adopting: 'pkill -f coord' would match filecoordinationd, a system
# daemon. Stop this loop with ./bridge_pulse_stop.sh, which kills by PID from PIDFILE
# after verifying identity with ps -- never by name.
echo $$ > $PIDFILE
# EXIT INSTRUMENTATION. This loop has now died three times and I had no idea why,
# because I detached it with stderr to /dev/null -- discarding exactly the evidence
# needed to diagnose it. Log the exit and the signal.
trap 'echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EXIT trap: last rc=$? " >> "$L.exit"; exit' EXIT TERM INT HUP
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
  # SCOPE THE PROBE TO MY OWN REPO. Bare script names are not a private namespace any
  # more than process names are -- this is ansatz's pkill broadcast pointed the other
  # way, at a READ instead of a kill. Today `kt_screen.py` happens to be unique to
  # TheBridge, but that is luck: ansatz works on Killing tensors too, and the day they
  # create a file by that name my probe silently counts THEIR job as mine, inflating my
  # rss and telling peers I am busy. So require both:
  #   (a) the process really is python  -- from `comm`, not from the command string
  #   (b) its cwd is inside my repo     -- from lsof, not inferred from the name
  REPO=/Users/sumit/Github/TheBridge
  pids=""
  # DO NOT ENUMERATE SCRIPT NAMES. That pattern was an ALLOWLIST, and an allowlist of
  # my own scripts silently omits every script I write next. I launched peak_probe.py
  # and my status published `idle, 0 MB` while the job held gigabytes -- after I had told
  # a peer the status would carry it. The guard was watching the wrong SET, which is the
  # same shape as watching the wrong QUANTITY: honest mechanism, void coverage.
  # The criterion that does not need maintaining is the one already used for scoping:
  # a python process whose cwd is inside this repo IS my job, whatever it is called.
  # Enumerate from ps, not from a pgrep pattern. `pgrep -x -f '.*python.*'` matched shells
  # and `pgrep -f python` matched two processes when three were running -- I tested both
  # before trusting either, which is the only reason this line is not a third guess.
  for _p in $(ps -eo pid=,comm= | awk 'tolower($2) ~ /python/ {print $1}'); do
    case "$(ps -o comm= -p $_p 2>/dev/null)" in
      *python*) ;;
      *) continue ;;
    esac
    _cwd=$(lsof -a -p $_p -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
    case "$_cwd" in
      $REPO*) pids="${pids:+$pids,}$_p" ;;
    esac
  done
  if [[ -n "$pids" ]]; then
    rss=$(ps -o rss= -p $pids 2>/dev/null | awk '{s+=$1} END{printf "%d", s/1024}')
    state=running; heavy=true
  else
    rss=0; state=idle; heavy=false
  fi
  free=$(df -g / | awk 'NR==2{print $4}')
  # NAME THE QUANTITY YOU ACTUALLY MEASURED. This field was called `mem_free_gb` and
  # contained free+inactive -- which at the moment I checked was 6.08 GB against 0.06 GB
  # genuinely free, a 94x overstatement of the thing its NAME promises. A peer sizing a
  # job against "free" would have been reading availability.
  # This is ansatz's class: they published 4.75 GiB/prime measured from a real matrix at
  # the RANK step, while the peak was the ASSEMBLY phase at ~38 GB. Both of us published
  # a number with full measurement-authority and no relationship to the thing it names,
  # and NO freshness, liveness or validity check can see it -- the plumbing works
  # perfectly. Publish all three, named for what they are.
  # EVERY LABEL MUST BE FOUND, not merely produce a number. quantum's find, and I had
  # shipped it inside the fix for the PREVIOUS fabrication twenty minutes earlier: awk
  # treats an absent label as 0, so a vm_stat missing `Pages inactive` published
  # mem_available 2.29 instead of 7.98 -- 5.7 GB fabricated away, silently. My validator
  # waved it through because 0.00 IS numeric. A MISSING LINE IS INDISTINGUISHABLE FROM A
  # ZERO COUNT WHEN YOUR FALLBACK IS ZERO.
  # Direction note: every component is additive, so a lost label always UNDERSTATES, and
  # understating reads as caution. That is luck, not design -- and not harmless: an
  # understatement is what nearly cost ansatz a launch window this morning.
  eval $(vm_stat | awk '
    /Pages free/       {gsub("\\.","",$3); f=$3; hf=1}
    /Pages inactive/   {gsub("\\.","",$3); i=$3; hi=1}
    /Pages speculative/{gsub("\\.","",$3); s=$3; hs=1}
    /compressor/       {gsub("\\.","",$5); c=$5; hc=1}
    END{ if (!(hf && hi && hs && hc)) { printf "mfree=MISSING mavail=MISSING mcomp=MISSING"; exit }
         printf "mfree=%.2f mavail=%.2f mcomp=%.2f", f*16384/1073741824,
                (f+i+s)*16384/1073741824, c*16384/1073741824 }')
  # ATOMIC WRITE (blackhole): this machine loses power mid-write. A truncated status
  # file is WORSE than a stale one -- a stale file still parses and expires cleanly
  # through stale_after_s, an unparseable one makes every reader invent a fallback.
  # VALIDATE BEFORE PUBLISHING -- "rewrite from live measurement OR WRITE NOTHING" was
  # a claim in my own docs that I had never tested. Tested it by injecting a failing
  # measurement into each of df / vm_stat / ps, one tick each:
  #   df fails     -> "disk_free_gb":,   INVALID JSON. Same trailing-value class as the
  #                   trailing-comma bug, different cause. A reader gets JSONDecodeError.
  #   vm_stat fails-> mem_free_gb: 0.0   A FABRICATED number presented as measured. It
  #                   happens to fail toward caution (0 GB reads as pressure), which is
  #                   luck, not design -- the same measurement could as easily read high.
  # So: if any measurement did not produce a number, publish NOTHING and let the file go
  # stale. Peers detect staleness; they cannot detect a confident fabrication.
  _bad=""
  for _f in rss free mfree; do
    _v=${(P)_f}
    case "$_v" in
      ''|*[!0-9.]*) _bad="${_bad:+$_bad,}$_f" ;;
    esac
  done
  if [[ -n "$_bad" ]]; then
    echo "[$now] MEASUREMENT FAILED ($_bad) -- refusing to publish; letting the file go stale" >> $L
    sleep 60; continue
  fi
  cat > $D/.bridge.status.tmp <<JSON
{"session":"bridge","repo":"/Users/sumit/Github/TheBridge","state":"$state","heavy":$heavy,
 "job_pids":[$pids],"rss_total_mb":$rss,"disk_free_gb":$free,"mem_free_gb":$mfree,
 "heartbeat_pid":$$,"mem_available_gb":$mavail,"mem_compressor_gb":$mcomp,
 "stale_after_s":300,"detail":"$DETAIL","declared_age_s":$dage,"updated":"$now",
 "field_semantics":{"MEASURED":["state","heavy","job_pids","rss_total_mb","disk_free_gb","mem_free_gb","mem_available_gb","mem_compressor_gb"],
                    "UNITS":"mem_free_gb is GENUINELY UNCLAIMED pages only. mem_available_gb adds inactive+speculative, which are reclaimable but NOT free -- reclaiming them under a fast large allocation is when this box stalls. Size against free for safety, available for optimism, and never confuse the two: this field was named mem_free_gb while containing available, a 94x overstatement. rss_total_mb is RESIDENT, not PEAK -- a job's high-water mark is not visible here.",
                    "LIVENESS":"heartbeat_pid is THIS LOOP, which lives as long as the heartbeat does -- ps it to distinguish alive-and-idle from dead. NOT the pid of a short-lived writer: ansatz published $$ of a script that exited milliseconds later, so every read resolved to UNKNOWN forever. A liveness token guaranteed dead is worse than an absent one -- absent is visible, always-dead looks like a working mechanism failing safe.",
                    "DECLARED":["detail"],
                    "note":"MEASURED fields require having looked and cannot be produced by a bumping loop. DECLARED is intent-at-a-time -- read it with declared_age_s, and schedule against the MEASURED fields. (tabula: a heartbeat cannot make a declaration true.)"}}
JSON
  sync 2>/dev/null; mv -f $D/.bridge.status.tmp $D/bridge.status
  sig="$state/$rss"
  if [[ "$sig" != "$prev" ]]; then
    echo "[$now] bridge $state  rss=${rss}MB  memfree=${mfree}GB  disk=${free}GB"
  fi
  # ALERT LINE, separate from the state-change line above. A monitor that fires on a
  # PEER's legitimate footprint is noise, and noise trains dismissal -- which is exactly
  # how I waved through the delta that had flagged my spanning error. So the alert fires
  # only on conditions that are MINE or genuinely wrong:
  #   - my own job running (state change already covers it)
  #   - free memory low WHILE I HOLD SOMETHING  (my problem)
  #   - disk nearly full                        (everyone's problem)
  # It does NOT fire on low memory while I am idle: that is a neighbour working.
  if [[ "$state" == "running" ]] && (( $(echo "$mfree < 0.3" | bc -l) )); then
    echo "[$now] ALERT mine-running-and-low-memory rss=${rss}MB free=${mfree}GB"
  fi
  if (( free < 5 )); then
    echo "[$now] ALERT disk-low ${free}GB"
  fi
  if false; then
    prev="$sig"
  fi
  echo "[$now] tick $state rss=${rss}MB memfree=${mfree}GB" >> $L
  sleep 60
done
