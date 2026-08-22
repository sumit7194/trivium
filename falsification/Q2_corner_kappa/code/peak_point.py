"""One (s, l) point, in a FRESH process, sampling CURRENT rss -- not ru_maxrss.

quantum found two defects in their equivalent probe that mine shares by construction:

  ru_maxrss NEVER FALLS. My per-l numbers were the running maximum over the whole
  process, so a later l that genuinely needs less than an earlier one reads as equal.
  I argued this was harmless because the true peak rises with l -- an ASSUMPTION I did
  not test, and the thing being estimated from those numbers was the exponent.

  PYTHON DOES NOT RETURN FREED MEMORY PROMPTLY. After a large l the process keeps the
  arena, so subsequent points read the plateau rather than their own demand. That
  produces exactly the signature I reported as a finding: an apparent exponent that
  DECAYS with l (mine ran 4.02 -> 1.16) purely because the readings saturate.

So: one point per process, current RSS from psutil-free /proc-free ps, and the baseline
subtracted. Under 3 samples is INVALID, not a measurement.
"""
import sys, os, time, threading, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

s, l = int(sys.argv[1]), int(sys.argv[2])
reg = sys.argv[3] if len(sys.argv) > 3 else "nn"
CFG = {3:(480,1/300.),4:(640,0.0025),5:(800,0.002),6:(960,1/600.)}
L, m = CFG[s]

def rss_gb():
    out = subprocess.run(["ps","-o","rss=","-p",str(os.getpid())],
                         capture_output=True, text=True).stdout.strip()
    return int(out)/2**20 if out else 0.0

samples = []
stop = threading.Event()
def sampler():
    while not stop.is_set():
        samples.append(rss_gb()); time.sleep(0.02)
threading.Thread(target=sampler, daemon=True).start()

from entropy import correlators
from s5_run import entropy_big
base = rss_gb()
X, P = correlators(L, m, reg)
after_corr = rss_gb()
n0 = len(samples)
t0 = time.time()
entropy_big(X, P, l, L)
stop.set(); time.sleep(0.05)
ent = samples[n0:]
if len(ent) < 3:
    print(f"s={s} l={l}  INVALID: only {len(ent)} samples in the entropy phase "
          f"({time.time()-t0:.2f}s) -- too fast to measure, not 0.0")
else:
    print(f"s={s} l={l}  entropy_peak {max(ent)-base:.3f} GB  "
          f"(base {base:.3f}, after_corr {after_corr-base:.3f}, "
          f"{len(ent)} samples, {time.time()-t0:.1f}s)")
