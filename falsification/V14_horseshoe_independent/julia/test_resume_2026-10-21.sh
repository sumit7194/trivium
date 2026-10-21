#!/bin/bash
# Test of the Q2-U checkpoint/resume (before launch): an uninterrupted reference run of one covering vs a run that is
# kill -9'd after its first checkpoint and relaunched. The decisions, leaves, depths and level results must be identical.
set -u
cd /Users/sumit/Github/TheBridge/falsification/V14_horseshoe_independent
JULIA=/Users/sumit/.julia/juliaup/julia-1.13.2+0.aarch64.apple.darwin14/Julia-1.13.app/Contents/Resources/julia/bin/julia
COVER="${1:-AZ: M0 => M0}"
run () { Q2_MAXDEPTH=10 Q2_LEAFPOW=20 Q2U_ONLY="$COVER" Q2U_OUTNAME="$1" Q2U_CKPT_SECONDS=60 nice -n 5 "$JULIA" -t 6 --heap-size-hint=8G --project=julia julia/q2u_main.jl U >> "$2" 2>&1; }
rm -f results/test_resume_ref.json results/test_resume_kill.json results/test_resume_*.log
echo "$(date '+%T') reference run" ; run test_resume_ref.json results/test_resume_ref.log
echo "$(date '+%T') interrupted run"
Q2_MAXDEPTH=10 Q2_LEAFPOW=20 Q2U_ONLY="$COVER" Q2U_OUTNAME=test_resume_kill.json Q2U_CKPT_SECONDS=60 nice -n 5 "$JULIA" -t 6 --heap-size-hint=8G --project=julia julia/q2u_main.jl U >> results/test_resume_kill.log 2>&1 &
pid=$!
until grep -q "CHECKPOINT" results/test_resume_kill.log 2>/dev/null; do sleep 5; kill -0 $pid 2>/dev/null || break; done
sleep 20; kill -9 $pid 2>/dev/null; echo "$(date '+%T') killed $pid (-9) after a checkpoint"; sleep 2
echo "$(date '+%T') relaunch"; run test_resume_kill.json results/test_resume_kill.log
grep -h "RESUME\|CHECKPOINT\|DONE" results/test_resume_kill.log
/usr/bin/python3 - <<'PY'
import json
a=json.load(open('results/test_resume_ref.json'))['covers']; b=json.load(open('results/test_resume_kill.json'))['covers']
def strip(o):
    if isinstance(o,dict): return {k:strip(v) for k,v in o.items() if k not in ('seconds','fallback_images_used')}
    if isinstance(o,list): return [strip(v) for v in o]
    return o
same = strip(a)==strip(b)
for k in a: print(k, 'ref:', a[k]['decision'], a[k].get('leaves'), a[k].get('max_depth'), '| resumed:', b[k]['decision'], b[k].get('leaves'), b[k].get('max_depth'))
print('IDENTICAL (all fields except timings):', same)
PY
ls results/ckpt_q2u 2>/dev/null | wc -l | xargs echo "leftover checkpoints:"
