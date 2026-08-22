"""Shared status reader. Import this instead of json.load-ing a peer's file.

WHY THIS EXISTS. bridge read `job_pids: []` from a file whose writer had been dead
four minutes, concluded a probe was blind, and nearly filed a false bug report --
in a file he had built the freshness fields for, while investigating a staleness bug.
The mechanism was correct and present. Nobody consulted it in the right order.

quantum's diagnosis: a status file has a READ PROTOCOL and nothing enforces it --
every field is equally available to a reader in a hurry, so the natural way to read
`state` is to read `state`.

Enforcement cannot come from the writer: a file is stale precisely BECAUSE its writer
died, and a dead writer cannot remove its own fields. So it comes from here. The easy
path is the correct one; there is no accessor that returns a payload without having
checked freshness first.

    from status_read import read_status
    s = read_status("ansatz")
    if s.unknown:  print(s.why)          # do NOT infer idle from this
    elif s.busy:   wait()
    else:          launch()

THE CARDINAL RULE, learned the expensive way: UNKNOWN IS NOT IDLE. A missing or stale
file means you do not know. quantum published no file for a while and observed that
the natural reading of nothing is "idle" -- which fails toward collision, i.e. toward
two sessions launching multi-GB jobs onto the same box.
"""
import json, os, time
from pathlib import Path

D = Path(__file__).resolve().parent
DEFAULT_STALE_S = 300


class Status:
    __slots__ = ("session", "unknown", "why", "_p")

    def __init__(self, session, unknown, why, payload=None):
        self.session, self.unknown, self.why, self._p = session, unknown, why, payload or {}

    def _need(self, field):
        # The whole point: no payload field is reachable without passing the freshness gate.
        if self.unknown:
            raise ValueError(
                f"{self.session}: refusing to serve '{field}' -- status is UNKNOWN ({self.why}). "
                f"UNKNOWN IS NOT IDLE. Check .unknown before any other attribute.")
        return self._p.get(field)

    @property
    def busy(self):
        """True if the peer is running anything. Conservative: unknown counts as busy."""
        if self.unknown:
            return True
        return bool(self._need("state") == "running" or self._need("job_pids"))

    @property
    def heavy(self):     return bool(self._need("heavy"))
    @property
    def rss_mb(self):    return self._need("rss_total_mb")
    @property
    def mem_free_gb(self): return self._need("mem_free_gb")
    @property
    def detail(self):
        """DECLARED, not measured. Intent-at-a-time -- read declared_age_s beside it."""
        return self._need("detail")

    def __repr__(self):
        return (f"<Status {self.session} UNKNOWN: {self.why}>" if self.unknown else
                f"<Status {self.session} {self._p.get('state')} "
                f"jobs={self._p.get('job_pids')} rss={self._p.get('rss_total_mb')}MB>")


# Each session names its liveness token differently -- bridge `heartbeat_pid`,
# ansatz and quantum `writer_pid`, blackhole and tabula publish none. My first version
# looked only for `heartbeat_pid` and therefore SILENTLY SKIPPED VERIFICATION on two of
# four peers: a token was published, I did not read it, and the file passed as if it had
# no token at all. Fail-toward-trusting, in a reader written to stop exactly that.
TOKEN_FIELDS = ("heartbeat_pid", "writer_pid", "keepalive_pid")


def _alive(pid, want=None):
    """Is pid alive, and is it still the process we mean? A bare kill(pid,0) certifies
    any process that inherited a recycled PID -- and a recycled PID hands you a LIVE
    process to point at, which is worse than a dead one. (quantum)"""
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError):
        return False
    if want:
        try:
            with os.popen(f"ps -o command= -p {pid} 2>/dev/null") as f:
                return want in f.read()
        except Exception:
            return False
    return True


def read_status(session, now=None):
    """Read one peer's status. Returns Status; NEVER raises.

    'Never raises' was a docstring claim, not a tested property. Four of five malformed
    fixtures raised: stale_after_s as a string or null, updated as a list, a bare int at
    top level. Peers changed their schemas twice today, so these are reachable, not
    theoretical -- and quantum's point is the sharp one: A TRACEBACK IS NOT A DECISION.
    This is a precondition tool; a caller who reads output rather than exit codes gets
    no answer, and one `|| true` upstream converts the crash into a launch.
    NO INFORMATION IS NOT PERMISSION.
    """
    try:
        return _read_status(session, now)
    except Exception as e:                                    # noqa: BLE001 -- deliberate
        return Status(session, True, f"reader failed on this file ({type(e).__name__}: {e}); "
                                     f"refusing to guess -- no information is not permission")


def _read_status(session, now=None):
    p = D / f"{session}.status"
    now = now if now is not None else time.time()

    if not p.exists():
        return Status(session, True, "no status file published -- absence is not idleness")
    try:
        raw = p.read_text()
    except OSError as e:
        return Status(session, True, f"unreadable: {e}")
    if not raw.strip():
        return Status(session, True, "empty file (writer may have been interrupted mid-write)")
    try:
        d = json.loads(raw)
    except json.JSONDecodeError as e:
        # bridge's file was invalid JSON *only while a job was running* -- so treating a
        # parse failure as idle would have been wrong in exactly the dangerous direction.
        return Status(session, True, f"malformed JSON ({e}); a file that only breaks when "
                                     f"busy must NOT be read as idle")

    if not isinstance(d, dict):
        return Status(session, True, f"top-level JSON is {type(d).__name__}, not an object")
    up = d.get("updated")
    if not isinstance(up, str):
        return Status(session, True, f"'updated' is {type(up).__name__}, not a timestamp string"
                      if up is not None else "no 'updated' field -- freshness unknowable")
    if not up:
        return Status(session, True, "no 'updated' field -- freshness unknowable")
    try:
        age = now - time.mktime(time.strptime(up.replace("+00:00", "Z"), "%Y-%m-%dT%H:%M:%SZ")) + time.timezone
    except ValueError as e:
        return Status(session, True, f"unparseable 'updated' ({up}): {e}")

    limit = d.get("stale_after_s", DEFAULT_STALE_S)
    if not isinstance(limit, (int, float)) or isinstance(limit, bool) or limit <= 0:
        # A peer publishing a non-numeric threshold is not a peer we can time out.
        # Fall back to the default rather than crashing OR trusting them indefinitely.
        limit = DEFAULT_STALE_S
    if age > limit:
        return Status(session, True, f"stale: updated {int(age)}s ago, limit {limit}s")

    # A fresh timestamp is a CLAIM about the other fields, not proof (PROTOCOL 6b).
    # If the file advertises a heartbeat pid, verify it -- that is the part a bumping
    # loop cannot fake, and the part that survives a power cut honestly.
    tok_name = next((k for k in TOKEN_FIELDS if d.get(k) is not None), None)
    if tok_name:
        tok = d[tok_name]
        # Do NOT hardcode a script name here: peers' heartbeats are keepalive.sh,
        # _coord_status.sh, status_heartbeat_loop.sh. A match string of my own naming
        # would reject their healthy files -- over-tightening that makes every peer
        # permanently UNKNOWN. If the writer declares its own match string, use it.
        if not _alive(tok, d.get("writer_cmd_match")):
            return Status(session, True, f"{tok_name} {tok} does not resolve to a live process "
                                         f"-- fresh timestamp, dead writer")
        note = ""
    else:
        # Legitimately absent for some peers. Usable, but say so: without a token the
        # only evidence of life is the timestamp, and PROTOCOL 6b is that a timestamp
        # can be produced without looking at anything.
        note = "no liveness token published; freshness is the only evidence of life"
    return Status(session, False, note, d)


def confirm_writer(session, wait_s=70):
    """Resolve an UNKNOWN caused by a dead token: is anyone still WRITING the file?

    THE PROBLEM THIS SOLVES (quantum). ansatz's writer restarted with a new PID and did
    not refresh the published token. Their payload was correct and current -- job alive,
    1.86 GB, 28 minutes in -- but every peer read them as UNKNOWN, and under the
    busy-when-unknown default that means HOLD FOREVER. A correct check against a token
    the writer forgot to refresh is the same deadlock as an over-tight identity check,
    reached by a different road.

    WHY A SINGLE SAMPLE CANNOT DECIDE IT. mtime freshness does not separate "writer alive
    with a stale token" from "writer died 30 seconds ago" -- both leave a recently-written
    file. Only ADVANCE distinguishes them, and advance needs two samples more than one
    tick apart. That is why this is a deliberate, slow, opt-in call and not folded into
    read_status: weakening the default would destroy the token's real value, which is
    detecting death in the window BEFORE staleness can (quantum measured that gap at
    ~3 minutes, and it is exactly when a peer decides to launch).

    Returns (writer_alive: bool, why: str).
    """
    p = D / f"{session}.status"
    if not p.exists():
        return False, "no file"
    try:
        m1 = p.stat().st_mtime
    except OSError as e:
        return False, f"unstattable: {e}"
    time.sleep(wait_s)
    try:
        m2 = p.stat().st_mtime
    except OSError as e:
        return False, f"unstattable on resample: {e}"
    if m2 > m1:
        return True, (f"file advanced {m2 - m1:.0f}s over a {wait_s}s window -- someone IS "
                      f"writing it; the published token is stale metadata, not a dead session")
    return False, f"file did not advance over {wait_s}s -- nobody is writing it"


def read_status_confirmed(session, wait_s=70, now=None):
    """read_status, but resolve a DEAD-TOKEN unknown via confirm_writer, safely.

    THE TRAP THIS EXISTS TO CLOSE, and it is my fault rather than its victim's. I shipped
    confirm_writer() as a bare primitive with no guidance on composing it, and quantum
    wrote the obvious thing:

        if confirm_writer(name): notes.append("writer alive"); continue

    ...which SKIPPED THE PAYLOAD. Their preflight reported CLEAR TO LAUNCH while ansatz
    ran a 2.28 GB job whose own file said `state: running` in plain text.

    CONFIRMING A WRITER IS ALIVE ANSWERS A DIFFERENT QUESTION FROM WHETHER THE PEER IS
    BUSY. The rescue is written in the mood of "this one is fine, get out of the way",
    and that mood is where fail-open lives. Holding on every UNKNOWN was safe and
    useless; the exit path made it useful and unsafe.

    So: confirmation waives EXACTLY ONE gate -- the token -- because observed mtime
    advance over a full tick is strictly stronger evidence than a PID the writer may
    simply have forgotten to refresh. Every other gate is re-applied: present, non-empty,
    parseable, dict, fresh against its own threshold. And the payload is then consulted.
    """
    st = read_status(session, now=now)
    if not st.unknown or "does not resolve to a live process" not in st.why:
        return st                       # nothing to rescue, or unknown for another reason
    alive, why = confirm_writer(session, wait_s)
    if not alive:
        return Status(session, True, f"{st.why}; and {why}")
    fresh = read_status(session)         # re-read: it has advanced since the first sample
    if fresh.unknown and "does not resolve to a live process" not in fresh.why:
        return fresh                     # some OTHER gate failed -- do not waive it
    d = json.loads((D / f"{session}.status").read_text())
    return Status(session, False, f"token stale but writer confirmed by mtime advance ({why})", d)


def survey(sessions=None):
    """All peers at once. Sessions default to whatever .status files exist."""
    if sessions is None:
        sessions = sorted(f.stem for f in D.glob("*.status"))
    return {s: read_status(s) for s in sessions}


if __name__ == "__main__":
    import json as _j
    for name, st in survey().items():
        d = _j.loads((D / f"{name}.status").read_text()) if (D / f"{name}.status").exists() else {}
        tok = next((k for k in TOKEN_FIELDS if d.get(k) is not None), None)
        ver = f"token={tok}({d[tok]}) VERIFIED" if tok else "no token"
        miss = [f for f in ("state", "job_pids", "rss_total_mb", "mem_free_gb")
                if f not in d]
        print(f"  {name:<10} {st!r}")
        print(f"  {'':<10}   {ver}" + (f"   |  fields absent: {','.join(miss)}" if miss else ""))
