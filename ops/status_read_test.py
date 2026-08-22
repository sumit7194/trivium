"""Every UNKNOWN path must fire, and the fresh path must not. Both directions, because
never-fires and always-fires are indistinguishable in source.

Written BEFORE trusting the reader anywhere, since the whole reason it exists is that
I trusted a file I had not exercised in the state that mattered.
"""
import json, os, sys, time, tempfile, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import status_read
from status_read import read_status

TMP = Path(tempfile.mkdtemp()); status_read.D = TMP
NOW = time.time()
def stamp(off=0):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW - off))

def w(name, text):
    (TMP / f"{name}.status").write_text(text)

ok = True
def case(label, name, expect_unknown, want_in_why=""):
    global ok
    s = read_status(name, now=NOW)
    good = (s.unknown == expect_unknown) and (want_in_why.lower() in s.why.lower())
    ok &= good
    print(f"  {'PASS' if good else '*** FAIL ***'}  {label:<44} "
          f"unknown={s.unknown}  {s.why[:52]}")
    return s

good_body = dict(state="idle", job_pids=[], rss_total_mb=0, heavy=False,
                 mem_free_gb=7.0, stale_after_s=300, detail="x")

print("UNKNOWN paths — each must fire")
case("missing file",              "nope",   True, "no status file")
w("empty", "")
case("empty file (interrupted write)", "empty", True, "empty")
w("trunc", '{"state":"idl')
case("truncated JSON", "trunc", True, "malformed")
w("comma", '{"job_pids":[3501,],"updated":"%s"}' % stamp())
case("trailing comma (my real bug)", "comma", True, "malformed")
w("nots", json.dumps(dict(good_body, state="idle")))
case("no 'updated' field", "nots", True, "freshness unknowable")
w("stale", json.dumps(dict(good_body, updated=stamp(2253))))
case("stale by 2253s (my real cut)", "stale", True, "stale")
w("fake", json.dumps(dict(good_body, updated=stamp(5), heartbeat_pid=999999)))
case("fresh clock, DEAD heartbeat", "fake", True, "does not resolve")

print("\nFRESH path — must NOT fire")
w("live", json.dumps(dict(good_body, updated=stamp(5))))
case("fresh, no token", "live", False)

print("\nENFORCEMENT — payload must be unreachable when UNKNOWN")
u = read_status("stale", now=NOW)
try:
    u.rss_mb; print("  *** FAIL ***  served rss_mb from a stale file"); ok = False
except ValueError as e:
    print(f"  PASS  refused to serve payload: {str(e)[:64]}...")
print(f"  {'PASS' if u.busy else '*** FAIL ***'}  UNKNOWN counts as BUSY (fails toward caution, not collision)")
ok &= u.busy

print(f"\n  {'ALL PASS' if ok else '*** FAILURES ***'}")
sys.exit(0 if ok else 1)
