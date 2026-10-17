A10 work in progress, saved 2026-10-17 when the user paused the fleet for disk space.
- The A10 agent was stopped by the bridge before it finished.
- hh_run.py (the HH positive control) was killed at ~2.3 GB of memory, because the disk was nearly full.
- The helper scripts here were in the bridge scratchpad and are copied as-is.
- v13_a10_multishoot.py and results/v13_a10_controls.{json,log} are partial.
- NO A10 verdict exists. On resume: cap memory at ~500 MB, run the controls first, then the scoped edges, all per
  PREREGISTRATION A10.
