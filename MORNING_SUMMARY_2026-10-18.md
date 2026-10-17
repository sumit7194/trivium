# Morning summary, 18 Oct 2026 (written overnight by the bridge)

## 1. The chaos screen: chaos inside the safe region now has solid numerical support
- I re-checked the candidate crossings with the corrected method (solving each step separately rather than chaining
  them all at once). It passed both built-in sanity checks: it confirmed all 54 known chaotic loops in Hénon–Heiles,
  and it rejected the deliberately planted fake crossings.
- **Main test point (C0):** 16 of 18 crossings confirmed. Three periodic orbits loop back onto themselves, and four
  orbits are linked in a closed cycle. All the connecting orbits stay inside the safe region, away from the ring
  singularity and the time-loop zone.
- **Second test point (F5-R):** 35 of 42 confirmed. Six orbits loop back onto themselves, and seven are linked in a
  cycle.
- **What it means:** strong numerical evidence that the Manko–Novikov chaos lives in the safe region too, which is
  what the computer-assisted proof needs. It is NOT a proof yet; the proof is quantum's job, plus our independent
  replay.
- **Honest caveats (recorded):**
  - One precision limit sits close to the integrator's own noise for the most stretching orbits. All 9 failures are
    there, and passes near the limit are partly luck.
  - An extra test I hadn't registered beforehand passes all 60 crossings comfortably. That counts only as support.
  - Tabula's independent check is still to come; we compare only after both sides seal.
- Committed: 085ac13.

## 2. (more sections are added below as the overnight jobs finish)
