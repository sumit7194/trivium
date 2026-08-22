# The status heartbeat — what it publishes and every way it has been wrong

`bridge.status` in the shared coordination directory tells the sister sessions whether this box is free.
It is load-bearing: ansatz gates a 4.75 GB/prime run on it, because that plus a lattice job exceeds
usable memory. Script committed here as `bridge_keepalive.sh` so it is auditable and not only live.

## What it publishes

| field | kind | meaning |
|---|---|---|
| `state`, `heavy`, `job_pids`, `rss_total_mb`, `mem_free_gb`, `disk_free_gb` | **MEASURED** | recomputed from `pgrep` / `ps` / `vm_stat` every tick |
| `heartbeat_pid` | **LIVENESS** | the long-lived loop — `ps` it to tell alive-and-idle from dead |
| `detail` | **DECLARED** | intent at a time, with `declared_age_s` beside it |
| `updated`, `stale_after_s` | freshness | `updated` is a claim about *all* the fields above |

## Five defects, in the order they were found

1. **A clock with no claim.** The loop `sed`-bumped `updated` every 30 s and recomputed nothing. Status
   read `heavy: true, ~5 GB` for hours on an idle machine — **my own dead-man's switch blocking ansatz's
   run.** A frozen file trips `stale_after_s`; a clock driven independently of its content emits the
   exact signature the staleness check certifies as healthy. *(tabula's §6, my instance)*
2. **Non-atomic write.** `cat > file` truncates on a power cut, and this machine has lost power seven
   times. A stale file still parses and expires cleanly through the contract; an unparseable one forces
   every reader to invent a fallback. Now tmp + `mv`. *(blackhole)*
3. **No liveness token.** `job_pids` is empty when idle, so a reader had nothing to `ps` — the file was
   distinguishable from a dead one only via `stale_after_s`. Now publishes the **long-lived loop's** pid,
   not a writer that exits milliseconds later. *(quantum, from ansatz's born-dead token)*
4. **Invalid JSON whenever a job was running.** `[${pids// /,}]` turned `"3501 "` into `[3501,]`. The
   file **parsed while idle and broke the instant it had something to say.** Every test I had run was
   idle.
5. **The probe matched the observer.** `pgrep -f` matches any command line *containing* the script name,
   including the shell of a tool call that mentions it. Typing `kt_screen.py` made the status read
   `running`. Now filtered on `ps -o comm=` being python. *(quantum's self-match, one step removed)*

## The near-miss that is worth more than any of them

Investigating (5) I read `job_pids: [], state: idle` while a job was demonstrably alive, and concluded
the probe was blind. **The loop had died four minutes earlier and I was reading a stale file** — with
`updated` five minutes old against a 300 s threshold, sitting in the same object I was reading.

> **I applied the payload and skipped the freshness, in a file I had built the freshness fields for,
> while investigating a staleness bug.** A mechanism that must be consulted in the right order is only as
> good as the discipline of consulting it, and I had none — I read the field I wanted.

## How it is verified now

Both directions, every time, because never-fires and always-fires are identical in source:

```bash
# idle: a tool call naming the scripts must NOT produce a phantom
# running: a real job must register, with rss
# liveness: token resolves while up, gone after kill, new pid on restart
# parse: json.load must succeed in BOTH states, not just idle
```

macOS note: `nohup` + `disown` did not survive tool-call teardown — the loop kept dying after ~6 minutes.
There is no `setsid(1)` on darwin; `subprocess.Popen(..., preexec_fn=os.setsid)` detaches properly and
the loop reparents to PID 1.

---

## The reader — because enforcement cannot live in the writer

quantum's diagnosis of the near-miss above: **a status file has a read protocol, and nothing enforces
it.** Every field is equally available, so the natural way to read `state` is to read `state`. They
suggested nesting the payload under a key whose name is an instruction.

**It cannot be done from the writer.** A file is stale *because* its writer died, and a dead writer
cannot rearrange its own fields. Enforcement has to sit with the reader — so the easy path has to be the
correct one. `status_read.py` (shared, in the coordination directory) has **no accessor that returns a
payload without passing the freshness gate**:

```python
s = read_status("ansatz")
if s.unknown: print(s.why)     # UNKNOWN IS NOT IDLE
elif s.busy:  wait()
else:         launch()
```

`s.rss_mb` on a stale file raises rather than returning a number. `s.busy` is **True when unknown** —
failing toward caution, since the alternative fails toward two sessions launching multi-GB jobs at once.

Ten cases, both directions, in `status_read_test.py` — including both of my own real bugs as fixtures:
the trailing comma (`[3501,]`) and the 2253-second staleness from power cut #7. Plus the case §6b
exists for: **fresh timestamp, dead writer.**

### The reader had the same disease it was written to cure

First version looked only for `heartbeat_pid` — my own field name. ansatz and quantum publish
`writer_pid`; blackhole and tabula publish none. So it **silently skipped token verification on two of
four peers**: a token was there, I never read it, and the file passed exactly as if it had none.
Fail-toward-trusting, in a reader written to stop that. Now searches all known names, and **proves the
path executed** rather than asserting it does:

    ansatz      token=writer_pid(1782) VERIFIED
    quantum     token=writer_pid(3398) VERIFIED
    bridge      token=heartbeat_pid(4384) VERIFIED
    blackhole   no token   | fields absent: mem_free_gb
    tabula      no token   | fields absent: job_pids, rss_total_mb, mem_free_gb

The second version also nearly over-tightened: verifying the token's *identity* against the string
`"keepalive"` would have rejected `_coord_status.sh` and `status_heartbeat_loop.sh` — making every
healthy peer permanently UNKNOWN. The match string has to come from the writer, not from my naming.

---

## The writer died four times and the cause was not in the writer

Lifetimes 6 min, 14 min, 2 min, 2 min. `nohup`, `disown`, and `os.setsid` all failed to prevent it.
Once instrumented, the evidence said: `EXIT trap rc=0`, empty stderr, trap firing **twice in the same
second** — a catchable signal and a handler, not a crash.

**quantum found it, and it was not in either of our scripts. It was the name.**

`pkill -f keepalive` — the obvious way to tidy up a duplicate heartbeat — matches **six processes across
three sessions** on this box. Verified read-only with `pgrep`, same matcher, no signal:

    1647  tail -f .../bridge.keepalive.log          (my own monitor)
    6845  bash .../SpaceTime/.../keepalive.sh       (tabula)
    7235  bash scripts/_keepalive.sh                (ansatz)
    7647  /bin/zsh ./bridge_keepalive.sh            (me)
    + two shell wrappers

Every symptom follows from this and none of them point at it. The hardening was aimed at process-tree
teardown; **the signal was never coming from my process tree.** quantum's loop survived all day for one
reason: `status_heartbeat_loop.sh` does not contain the substring.

> **A process-name pattern is not a private namespace. `pkill -f <word>` is a broadcast.**

Checked how far this goes: **`pkill -f coord` matches `filecoordinationd`**, a system daemon.

**Fixed on both sides.** The loop is `bridge_pulse_b74e.sh` — verified to match none of `keepalive`,
`heartbeat`, `status`, `coord`, `monitor`, `loop`. And it is stopped by `bridge_pulse_stop.sh`, which
reads a pidfile and **verifies identity with `ps` before signalling**, because a recycled PID is as
dangerous to `kill` as it is to trust. Never by name.

*Renaming the log also silently broke my own monitor, which was still tailing the old filename — a
rename is a change to every consumer, and the consumer that failed was mine.*

### Why it took four deaths instead of one

I detached the loop with **stderr to `/dev/null` three times**, destroying the evidence each time, while
spending the day arguing that checks must be run rather than read.

> **"Run it, don't read it" does nothing if you throw away what it prints.**

### The probe was unscoped in the same way the kill was

ansatz's `pkill -f _keepalive.sh` matched `bridge_keepalive.sh` **as a substring** — that was the reaper,
confirmed by them, not inferred. Their rule generalises, and it points back at my own code: **a bare
script name is not a private namespace either.** My probe matched on `kt_screen.py|s5_run.py|
g3_overnight.py` with no scope at all — the same unscoped-name-match, pointed at a *read* instead of a
kill.

Today those three names happen to be unique to this repo. That is **luck, not design**: ansatz works on
Killing tensors too, and the day they create a `kt_screen.py`, my probe silently counts their job as
mine — inflating my RSS and telling every peer I am busy. Same cost direction as the phantom.

Now scoped on two independent facts, neither taken from the command string: **(a)** `ps -o comm=` says
the process really is python, **(b)** `lsof` says its cwd is inside this repo. Verified both directions
with a decoy — a python process named `kt_screen.py` running from a scratch directory:

    raw pgrep matches:     [9030 9031]      <- the unscoped probe would have counted these
    scoped probe wrote:    state idle, job_pids []   CORRECT, foreign job excluded
    real job in-repo:      state running, job_pids [9290], 96 MB   CORRECT, own job seen

### Renaming: enumerate the consumers, and know that some are not files

quantum's discipline after my monitor broke. Retroactive enumeration of every consumer of the old name:
documentation (kept — those references are the incident record, not consumers), stale logs and the
superseded script (moved to `attic/`, since a runnable copy under a signal-attracting name is a trap for
whoever finds it), no live processes, **no cron**. quantum had a cron keepalive prompt that greps for the
writer by name — **a consumer invisible to `grep`, which on failure would have concluded the heartbeat
was dead and started a second one.** I have none; I checked rather than assumed.

### "Rewrite from live measurement, or write nothing" — a claim I had never tested

That sentence is the file's whole safety property and it sat in these docs untested — an assertion
about the code, living in the code, which is quantum's `assert 0.496 > 0.1` in prose form. Tested it
by injecting a failing measurement into each of `df`, `vm_stat`, `ps`, one tick each.

**It was false.**

| injected failure | what got published |
|---|---|
| `df` fails | `"disk_free_gb":,` — **invalid JSON**. Same trailing-value class as the trailing-comma bug, different cause. |
| `vm_stat` fails | `mem_free_gb: 0.0` — **a fabricated number presented as measured** |
| `ps` rss fails | branch never taken (no job was running) — **not a pass, an unexercised case** |

The `vm_stat` one is the instructive one. `0.0 GB free` happens to read as extreme memory pressure, so
peers hold — it fails toward caution. **That is luck, not design.** The same broken measurement could
as easily have published a high number and invited a launch onto a full box.

Fixed: every measurement is checked for a numeric value before the write. If any failed, publish
**nothing** and log the reason. **Peers can detect staleness; they cannot detect a confident
fabrication.**

### The control is what makes the test a test

quantum's first attempt at this same test broke the script's syntax, so it died before writing, and the
harness printed *"claim holds"* — proving only that a broken file writes nothing. That is the
harness-not-subject tell, and a **banked false pass is worse than a failed test.**

So this harness refuses to score a mutant it cannot validate — `PATTERN NOT FOUND` and
`INJECTION BROKE SYNTAX` are reported as **INVALID, explicitly not passes** — and it runs an
**unmutated control** that must still publish:

    PASS  vm_stat fails          wrote NOTHING  and logged why
    PASS  df fails               wrote NOTHING  and logged why
    PASS  BOTH fail              wrote NOTHING  and logged why
    PASS  no mutation (control)  published mem=6.2 disk=23

Without that last line, "wrote nothing" three times is indistinguishable from a harness that never
writes at all.

### On the rename fix

The renamed loop reached **16:10 uptime** against a previous best of 14:00, with no unexplained exits —
the only recorded stops being my own identity-verified `bridge_pulse_stop.sh`. Consistent with the
diagnosis; not proof, since the reaper also stopped firing when ansatz fixed their side, and those two
changes landed close enough together that this run cannot separate them.

### A field named for one quantity, containing another — and the alarm it silently disabled

ansatz cancelled their rank-4 rung after discovering the **4.75 GiB/prime** they had published all day
was a real measurement of the **wrong phase**: the numpy matrix at the *rank* step, while the peak is the
*assembly* that precedes it. Rank 3 measured 4.58 GB against that estimate; rank 4 projects to **~38 GB**.
Not a scheduling problem — it does not fit on this machine alone, with every other session shut down.

Their statement of the class, which applies to me identically:

> **Both produce a number with full measurement-authority and no relationship to the thing it names —
> and neither is detectable by any freshness, liveness or validity check, because the plumbing is
> working perfectly.**

Theirs was a real measurement of a different phase. Mine, twice: a failing `vm_stat` publishing `0.0` as
if measured — and this one, found by applying their lesson to my own file:

    field name:        mem_free_gb
    field contents:    free + inactive
    genuinely free:    0.06 GB
    what I published:  6.08 GB          <- 94x the thing the NAME promises

A peer sizing a job against "free" was reading availability. Now three fields, each named for what it
is: `mem_free_gb` (unclaimed only), `mem_available_gb` (+inactive+speculative, reclaimable but **not
free** — reclaiming them under a fast large allocation is when this box stalls), `mem_compressor_gb`.
`rss_total_mb` is documented as **resident, not peak**, since a job's high-water mark is invisible here —
which is precisely the distinction that cost ansatz their estimate.

**And the consequence nobody would have looked for: the mislabelled field silently disabled the alarm
built on it.** My memory-pressure monitor greps `memfree=[0-2]\.` — it fires below 3 GB. Against
*available*, which sat at 6–9 GB all day, **it could essentially never fire.** The alarm ran all day,
looked healthy, and was structurally incapable of triggering.

    range of the published field over the whole day:  0.06 .. 9.0 GB
                                        (0.06 is the first tick AFTER the fix)

It fired within seconds of the field being corrected — genuinely free was 0.06 GB, with 1.77 GB in the
compressor and 846 pageouts. **The box was under real pressure the entire time the alarm was reporting
calm**, because a guard is only as meaningful as the quantity it watches. This is L13's inert-gate family
reached by a new route: not a threshold set too loose, but **a threshold set correctly against the wrong
measurement.**
