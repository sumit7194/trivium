# G3 — how to (re)start the run yourself

The run checkpoints **after every orbit**, atomically. A power cut costs minutes, not hours.
Re-running the same command always **resumes** — it never restarts from scratch.

## ⚠️ Prefer launching from your own Terminal

The deaths so far have been **mains power loss** (a known issue in Sumit's area), which nothing
software-side can prevent — the per-orbit checkpoint is the defence, and it works: the last cut
cost 0 completed orbits.

Separately, a run launched inside a Claude Code session is a child of that session's shell and
would not survive the session ending. Launching from Terminal.app avoids that second, smaller
risk. Neither changes the recovery procedure below.

## Start / resume

```bash
nohup /Users/sumit/Github/conjecture_machine/.venv/bin/python -u g3_overnight.py >> ../results/overnight.log 2>&1 &
```

Safe to run any number of times. It reloads completed δ values *and* partially-scanned
orbits, prints what it recovered, and continues.

## Check progress

```bash
tail -20 /Users/sumit/Github/TheBridge/falsification/G3_chaos_boundary/results/overnight.log
```

## Is it still running?

```bash
pgrep -fl g3_overnight.py | grep -i python
```

⚠️ **Use exactly this.** The binary is `Python` with a capital P, so `pgrep -f "python -u ..."`
returns nothing even when the run is healthy. I made that mistake, read the false negative as
"it died", and launched a **second** process against the same checkpoint. Always confirm with the
command above before starting another one — and if two ever appear, `kill` the newer PID.

## Stop it

```bash
pkill -f g3_overnight.py
```

Stopping is safe — the checkpoint is current to the last completed orbit.

---

**Notes.** δ values run in the order `[2.0, 1.0, 1.7, …]` deliberately: δ=2.0 is the G3b
regression gate and δ=1.0 the G3a control, and either failing voids everything downstream —
so they resolve first. **If δ=2.0 comes back with `fired = 0`, the run is already answered
(UNDECIDED(search)) and the remaining ~7 hours are not worth spending.**

Checkpoint: `results/g3_overnight.json` (atomic write — a cut mid-write cannot corrupt it).
Log is appended, not overwritten, so the history of attempts is preserved.
