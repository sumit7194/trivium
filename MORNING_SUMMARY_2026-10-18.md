# Morning summary, 18 Oct 2026 (written overnight by the bridge)

## 1. The chaos screen: chaos inside the safe region now has solid numerical support
- I re-checked the candidate crossings with the corrected method (solving each step separately rather than chaining
  them all at once). It passed both built-in sanity checks: it confirmed all 54 known chaotic loops in Hénon–Heiles,
  and it rejected the deliberately planted fake crossings.
- **Main test point (C0):** 16 of 18 crossings confirmed. Three periodic orbits loop back onto themselves, and four
  orbits are linked in a closed cycle. All the connecting orbits stay inside the safe region and outside the time-loop zone.
  **Correction (later that morning):** "away from the ring singularity" was wrong. These orbits pass within about
  0.02 (in the x coordinate) of the ring, on its non-time-loop side. They are inside the safe region as defined, but
  in the strong-field zone right next to the ring.
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

## 2. Manko email: drafted, nothing sent or published
- **Address:** vsmanko@cinvestav.mx, from his official Cinvestav profile page (dated 2025-02-11). His 2023 arXiv
  papers print no email. Recommend writing to Manko alone.
- **Draft:** `outreach/mn_ring_manko/EMAIL_DRAFT.txt` (~530 words, same style as the 2007 email). It asks:
  (a) is the ring already known, perhaps in the 1992 or 1990 papers we couldn't read;
  (b) is our copy of the metric faithful to his original;
  (c) does he see a flaw.
  - It links the ring to his own 2011 paper on Tomimatsu–Sato δ=2 (arXiv:1110.6564). I checked that this paper
    exists and is his.
  - A one-page summary is at `ONE_PAGER.md` and `.pdf`. Checklist and claim-by-claim sources:
    `README_FOR_USER.md`.
- **Snapshot repo:** built locally only at `~/Github/snapshots/mn-ring-singularity/`. It re-runs and reproduces the
  stored results, and every fingerprint in its MANIFEST checks.
- **Before it goes public, I recommend cleaning three things:**
  1. one `env.json` line names Apple's maths library (Accelerate) as the linear-algebra backend. With the Apple
     report still open, I'd remove that line;
  2. a few logs contain `/Users/sumit/...` paths;
  3. mentions of "Fable" and of our session names.
  None of them is sensitive in itself, but cleaning them costs nothing.
- **Decisions for you:**
  - edit and approve the email;
  - make the snapshot public (after the clean-up);
  - a separate short note to Brink about the two misprints in his 2008 appendix (I'd keep them out of the Manko
    email).
- If the ring-proof derivation (section 3) succeeds, one sentence in the email changes: "one step assumed" becomes
  "derived".

## 3. Quantum: Hénon–Heiles proof calculations
- The restart killed the two unfinished calculations with no results. The other five finished before it and are
  sealed.
- Before rerunning, quantum added the ability to save progress partway and resume, tested it on the Rössler case, and
  registered the change before launching. A future restart can't wipe out hours of work again.
- The two reruns are going now (4 low-priority processes, very little memory).
- Quantum disclosed a slip of its own: it once stopped its own test process by name pattern instead of by ID. Nothing
  else was affected.

## 4. Our independent chaos-proof checker: the Rössler test passed, but it found a weakness in itself
- **The test:** redo quantum's Rössler test cases with completely separate software (Julia), reading only the case
  definitions, not quantum's answers. **It passed every pre-registered requirement:**
  - all 4 genuine coverings confirmed;
  - all deliberately wrong ones rejected;
  - the one "trick" case that should pass, passed.
- **Its own weak point:** the Julia package does some internal arithmetic in ordinary floating point without counting
  the rounding errors. For these results the margins are about 10 billion times larger than that error, so the
  answers are safe. But it means the checker is not yet fully rigorous, which matters for the real Manko–Novikov
  proof.
- **The fix:** registered before any further use (6158857), and running now. Either use interval coefficients
  throughout, or add a proven rounding bound, then redo the Rössler tests with the fixed version.
- **One open question to quantum:** the test files don't say which cross-section they use. We assumed the standard
  one and asked quantum to confirm.

## 5. The ring proof: the missing step is now derived, and Fable isn't needed
- The one step we had only checked numerically (how fast the curvature blows up near the ring) has now been derived
  by hand, by an Opus agent.
- The formula matches the computer values at all four test rings to about 27–35 digits (the requirement was 6), and
  reduces exactly to Kerr's known result.
- **It also explains why** the curvature grows a million-fold per tenfold step and not faster: right at the ring the
  geometry looks like a flat gravitational wave with no curvature invariants at all, and the blow-up comes only from
  the next correction.
- I've updated the matching sentence in the Manko email draft (it said "one step assumed"; now it gives the derived
  formula).
- A side result for later: the same formula suggests the off-equator rings at negative q are singular too. Not
  checked separately.
- Committed: c8467f9.

