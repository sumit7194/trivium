"""Actually RUN s=6, instead of declining it from a projection.

The whole day was about numbers with measurement-authority and no referent. Then I
measured s=6's requirement at 13.5 GB, compared it against `available` (~10 GB), and
declined -- WITHOUT EVER TESTING THAT COMPARISON. "Requirement > available therefore
fails" is itself an untested model, and macOS compresses and swaps dynamically:

    RAM 16.0 GB + up to ~22 GB of dynamic swap on free disk = ~38 GB addressable

So 13.5 GB is well inside the ceiling. The real question is whether the working set is
HOT. Dense eigendecomposition on n x n with n = l^2 touches every element repeatedly,
which is the worst case for paging -- but that is a PREDICTION, and predictions are what
this day has been about.

THE DISCRIMINATOR IS WALL-CLOCK, NOT MEMORY. Compute scales as O(n^3) = O(l^6), so from
the measured s=5 timing at l=100 (176.8 s) the in-RAM expectation at l=120 is
176.8 * 1.2^6 = 529 s ~ 9 min. Then:

    finishes near ~9 min      -> it FITS; the projection-based refusal was wrong
    finishes in 30-90 min     -> swap works, it is just slow; a real option for one rung
    no progress + heavy paging-> genuinely out of reach, now MEASURED rather than assumed

GUARD: a watchdog thread kills the run if the machine is thrashing with no progress, so
this cannot take the box down for the other sessions or the user.
"""
import sys, os, time, threading, subprocess, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

L, m, ls = 960, 1/600., list(range(24, 121, 12))
STALL_S = 900          # no new l for 15 min...
FREE_FLOOR = 0.15      # ...while genuinely-free memory is under 150 MB -> abort

def vm():
    o = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    g = lambda k: int([x for x in o.split("\n") if k in x][0].split()[-1].rstrip("."))
    return (g("Pages free")*16384/2**30, g("Pageouts"),
            g("Pages occupied by compressor")*16384/2**30)

def swap_used():
    o = subprocess.run(["sysctl","-n","vm.swapusage"], capture_output=True, text=True).stdout
    for tok in o.split():
        if tok.startswith("used"): pass
    import re
    mm = re.search(r"used\s*=\s*([\d.]+)M", o)
    return float(mm.group(1))/1024 if mm else 0.0

state = {"l": None, "t": time.time(), "abort": False}
def watchdog():
    while not state["abort"]:
        time.sleep(30)
        free, po, comp = vm()
        stalled = time.time() - state["t"]
        if stalled > STALL_S and free < FREE_FLOOR:
            print(f"\n  WATCHDOG ABORT: no progress for {stalled:.0f}s with free={free:.2f} GB "
                  f"-- thrashing, killing rather than taking the box down", flush=True)
            os.kill(os.getpid(), signal.SIGKILL)
threading.Thread(target=watchdog, daemon=True).start()

from entropy import correlators
from s5_run import entropy_big

def rss():
    o = subprocess.run(["ps","-o","rss=","-p",str(os.getpid())],capture_output=True,text=True).stdout.strip()
    return int(o)/2**20 if o else 0.0

print(f"s=6 L={L} m*L={m*L:.2f} l={ls}", flush=True)
print(f"  RAM 16.0 GB, swap dynamic. In-RAM expectation at l=120: ~529 s (l^6 from s=5)", flush=True)
t0 = time.time()
X, P = correlators(L, m, "nn")
print(f"  correlators [{time.time()-t0:.0f}s] rss {rss():.2f} GB", flush=True)
for l in ls:
    state["l"], state["t"] = l, time.time()
    t1 = time.time()
    entropy_big(X, P, l, L)
    free, po, comp = vm()
    print(f"  l={l:<4} {time.time()-t1:7.1f}s  rss {rss():5.2f} GB  free {free:4.2f}  "
          f"swap {swap_used():5.2f} GB  comp {comp:4.2f}  pageouts {po}", flush=True)
state["abort"] = True
print(f"\n  COMPLETED in {time.time()-t0:.0f}s total", flush=True)
