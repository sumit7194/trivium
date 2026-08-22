"""Measure the ACTUAL peak of one regulator at a given s, instead of projecting it.

WHY. s=6 (L=960) projects to ~7.2 GB by scaling s=5's measured ~5 GB by (L/800)^2. That
is structurally correct about the correlator matrices and SILENT ABOUT WHICH PHASE
DOMINATES -- the same kind of object as ansatz's 4.75 GiB/prime, which was a real
measurement of the rank step while the true peak was the assembly phase, 8x larger. They
found it by being pushed on the number, not by the run failing.

So: run ONE regulator, sample RSS, report the true high-water mark AND the phase it
occurs in. A quarter the cost of a full rung, and it answers whether s=6 fits at all.

CALIBRATE ON s=5 FIRST, where the peak is already known. A probe that cannot reproduce a
known answer cannot be trusted on an unknown one.
"""
import sys, time, threading, resource, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import correlators
from s5_run import entropy_big

CFG = {3: (480, 1/300., list(range(12, 61, 6))),
       4: (640, 0.0025, list(range(16, 81, 8))),
       5: (800, 0.002,  list(range(20, 101, 10))),
       6: (960, 1/600., list(range(24, 121, 12)))}

s   = int(sys.argv[1])
reg = sys.argv[2] if len(sys.argv) > 2 else "nn"
L, m, ls = CFG[s]

peak = {"gb": 0.0, "where": "start"}
stop = threading.Event()

def rss_gb():
    # darwin ru_maxrss is BYTES (linux gives KiB) -- assert the unit rather than assume it
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30

def sampler():
    while not stop.is_set():
        r = rss_gb()
        if r > peak["gb"]:
            peak["gb"], peak["where"] = r, sampler.phase
        time.sleep(0.25)

sampler.phase = "start"
threading.Thread(target=sampler, daemon=True).start()

print(f"s={s} L={L} m*L={m*L:.2f} regulator={reg} l={ls}", flush=True)
print(f"  baseline rss {rss_gb():.3f} GB", flush=True)
t0 = time.time()
sampler.phase = "correlators"
X, P = correlators(L, m, reg)
print(f"  correlators done [{time.time()-t0:.0f}s]  peak so far {peak['gb']:.2f} GB", flush=True)
for l in ls:
    sampler.phase = f"entropy l={l}"
    entropy_big(X, P, l, L)
    print(f"  l={l:<4} peak {peak['gb']:.2f} GB  ({time.time()-t0:.0f}s)", flush=True)
stop.set()
print(f"\n  TRUE PEAK {peak['gb']:.2f} GB, reached during: {peak['where']}", flush=True)
