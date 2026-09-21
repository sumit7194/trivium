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

`.githooks/pre-commit` now warns when a **staged** file is checkpoint-shaped **and** was modified in
the last ten minutes. Static caches never trip it; live state always does. *Verified in both
directions: the July files are silent, a freshly written one fires.*

**This file exists because the defect was never that they were tracked — it was that nothing said
what they are.** A reader finding an uncited `*_ckpt.json` in a results directory cannot tell a
cache from a result.
