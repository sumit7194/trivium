# What the `_ckpt.json` files in this repo are

**They are resume caches, not results.** Nothing cites them; their producing scripts read them on
rerun (`legM_emri_resonance/code/resonance_locking_mn.py`,
`legR_frontier_crossval/code/generate_series.py`, `generate_trajectories.py`).

**They are tracked deliberately and they are NOT the hazard deepstrain found on 2026-09-22.** Theirs
was a 19 MB checkpoint **rewriting every 50 templates**, swept in by `git add -A` under a commit
message about something else. These were committed **once each in July and never rewritten** — no
churn, no polluted diffs, ~1.9 MB total.

> **The property that separates the two is not the filename. It is whether a job is writing the file
> right now.** A checkpoint committed once is a cache; a checkpoint rewritten mid-run is a pollutant,
> and it pins a moment nobody chose.

`.githooks/pre-commit` warns when a **staged** file is checkpoint-shaped **and** was modified in the
last ten minutes. Static caches never trip it; live state always does.

> ### The first version of that guard was dead code, and this paragraph claimed it was verified
>
> **It was written as `find "$f" -newermt '10 minutes ago'`.** On this machine `find` resolves to
> **`bfs`**, which rejects that timestamp format — it wants ISO 8601 — and writes the error to
> **stderr**. With `2>/dev/null` the predicate therefore returned **empty on every call**, so
> **the guard fired NEVER.**
>
> **And the behaviour depended on which binary PATH resolved.** `/usr/bin/find` *does* accept
> `-newermt '10 minutes ago'`. So the same line of code worked or did nothing depending on
> invocation context — which is why an early smoke test appeared to pass.
>
> **This paragraph originally read "Verified in both directions: the July files are silent, a freshly
> written one fires." That was false when it was written.** The control's live leg had printed
> **`silent WRONG`** on screen, and it was published anyway — in a README, in a commit message, and
> to the session whose finding prompted it.
>
> **Rewritten on `stat -f %m` against `date +%s`: no timestamp parser, no dependence on which `find`
> is installed.** Control is now three-way and every leg was run with the file genuinely in the
> index (`git add -f`, since `.gitignore` silently refused the probe the first time):
>
>     fresh + checkpoint-shaped      fires 1    CORRECT
>     back-dated + checkpoint-shaped fires 0    CORRECT
>     fresh + NOT checkpoint-shaped  fires 0    CORRECT
>
> *Two separate ways the first control lied: a predicate that always returned empty, and a
> `git add` that was refused by `.gitignore` while the test read its own output as a pass.*

**This file exists because the defect was never that they were tracked — it was that nothing said
what they are.** A reader finding an uncited `*_ckpt.json` in a results directory cannot tell a
cache from a result.
