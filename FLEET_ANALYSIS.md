# Fleet analysis — the six plan files, read by the bridge

*Draft for discussion with the user, 2026-09-23. **Not yet shared with any sister session.** Written after
taking over the synthesis from `high_rank_killing` (its `Plans/FLEET_PLAN.md`, uncommitted there).*

**Disclosure.** I read `high_rank_killing`'s synthesis before reading the six plans myself, so this
analysis is **not independent of it**. I aimed at what it missed or got wrong, and at verifying at source
what it graded "relayed".

**Read in full:** bridge `MOONSHOTS.md` · ansatz `docs/SHARED_MOONSHOT_PLAN.md` · deepstrain
`MOONSHOT_BRIEF_DeepStrain.md` · cuspis `SHARED_BACKLOG.md` · quantum `COORDINATION_corner_research_menu.md` ·
tabula `writeups/tabula_next_directions.md`. All six copies in `high_rank_killing/Plans/` match their
originals byte-for-byte (md5), so the synthesis was run on current versions.

---

## 1. The synthesis holds up. Here is what I verified and what it missed

**Verified at the source, upgrading its "relayed" grade:**

| Item | Status now |
|---|---|
| **R-1** B-1 already done | **Verified, and independently re-derived.** `high_rank_killing` EXP-002 (`9384d7f`, 2026-09-05) is a 4D Lorentzian vacuum pp-wave with a rank-3 Killing tensor that is irreducible in the polynomial sense. Bridge check V5 re-derives it with code importing nothing from ansatz (`falsification/V5_rank3_vacuum_independent`). |
| **R-3** B-13 infeasible | **Verified in substance.** quantum's clean lattice angles are 60°/90°/120°; its README marks others as needing a staircase. |
| **R-4** B-7 already done | **Verified.** tabula lists "geometry from entanglement (32/41/42/125)" as done. |
| **R-5** G-6 "probably closed" | **Corrected.** The bridge's claim was *true when made*: cuspis added 2307.05164 at 22:36, two minutes after the bridge doc (22:34). It is now in cuspis's references and backlog, and **still not in `RESULT.md`**, where the positioning belongs. |

**Its best structural insight, which I'd keep as the spine:** the fleet has three instrument kinds
(exact, numerical, real data) and **no fourth, proof (M)**. Four separate items across three lists
(bridge B-9, ansatz #3/#9, quantum V1) are really one missing instrument. Build it once, with ZV δ=2 (must
fail) and Kerr (must pass) as controls, and aim it at several targets (**X-1**).

**What it missed:**

1. **Two lists contradicted an in-fleet result, not just one.** ansatz #1 says a Lorentzian vacuum
   rank ≥ 3 example is *"none known in any dimension"*, the same claim as bridge B-1. Its R-2 corrects
   ansatz's sentence about harmonic potentials but not this headline. **tabula's list got it right**
   (its #1 cites EXP-002 correctly). *So the one sister that read `high_rank_killing` knew, and the two
   that didn't — including the one whose solver produced the count — did not.* That is A4's one-sided
   channel again, this time in planning.
2. **ansatz #4, "Is the dynamical Chern–Simons black hole integrable?", has no place in the plan.** The
   literature contradicts itself (Cárdenas-Avendaño et al.: probably yes; Owen–Yunes–Witek and Deich et
   al.: probably no), the fleet holds an exact rung-P result on it, and it needs precisely the
   exact + proof + numerical + bridge split the synthesis champions. It is mentioned once, in passing.
3. **The six lists rank with incompatible formulas**, so their rank orders cannot be merged as they are:

   | List | Formula | What it rewards |
   |---|---|---|
   | deepstrain | I × D **÷ P** | blows up as P → 0: a 1% item outranks a 50% item by 50× |
   | cuspis | I × C × **(1 − P)** | bounded; the closest to what you asked for |
   | tabula | I × C × (6 − Chance), **Chance scored 1–5** | "chance" isn't a probability here |
   | bridge | qualitative: I, D desc; odds asc | — |
   | ansatz / quantum | tiers / no composite | — |
   | synthesis | **I × odds** | expected value — **the opposite of your criterion** |

   **"Odds" also means five different things**: the stated success criterion (bridge), a clean result
   (ansatz), *"a detection or a decisive answer"* (deepstrain), a clean reportable answer (cuspis), and a
   1–5 score (tabula). deepstrain's M6 shows why this matters: *"real <1%; clean answer ~70%"* — the same
   item ranks first or near-last depending on which odds you use.
   **Fix:** merge on the raw triples (impact, difficulty, odds) with one odds definition — *the chance
   the item's stated success criterion is met* — and every item states that criterion. Then show two
   views: a **moonshot view** (your question; cuspis's bounded formula) and a **portfolio view** (what to
   actually run; expected value).
4. **Its own proposals would give `high_rank_killing` more work** (X-1 candidate, H-2, H-3, H-4). It
   declared its interest in Thread A; the proposals still point one way. See §3.

---

## 2. Reconciliation ledger — current state

| # | Item | State | Next |
|---|---|---|---|
| R-1 | Bridge B-1 / G-3 contradicted by EXP-002 | **resolved — verified (V5)** | B-1 → H-2 (functionally independent) |
| R-2 | ansatz "no harmonic potential with cubic integral" | **resolved — ansatz corrected #1** (the open version is now a harmonic potential whose higher integral is *not* generated by quadratics) | — |
| R-3 | B-13 lattice route | **resolved — verified** | a sub-45° second instrument has no owner |
| R-4 | B-7 already done | **resolved — verified** | dropped |
| R-5 | G-6 | **resolved — cuspis positioned it in RESULT.md §0 and §8 (`2554c92`, 09-24)** | — |
| R-6 | quantum holds a copy of cuspis's solver | **already recorded** — A4 DAG edge 16 | — |
| R-7 | B-9 / B-11 not in ansatz's list | superseded — the plan is no longer organised by score | — |
| R-8 | B-16 not in deepstrain's list | superseded — the plan is no longer organised by score | — |
| **R-9** *(new)* | ansatz #1 "none known in any dimension" contradicted by EXP-002 | **resolved — ansatz verified independently (RESULTS §147) and corrected #1 and CLAUDE.md §1** | — |
| **R-10** *(new)* | incompatible ranking formulas and odds definitions | open | adopt one odds definition; merge on raw triples |
| **R-11** *(new)* | ansatz #4 (dCS integrability) omitted from the synthesis | open | give it a thread (split: E ansatz · M X-1 · N tabula/quantum · B bridge) |

---

## 3. Should `high_rank_killing` become a seventh repo? — my view

**I agree with you: no.** Reasons:

- **It is a task workspace with one finished result**, like `hidden_symmetry` (closed at outcome E), not a
  sustained programme. `corner_function` was promoted because it had a single long-running problem, its own
  instrument, and a 25-item pipeline. `high_rank_killing` has a result and a synthesis.
- **Its open items are ansatz's question.** H-2 is ansatz #1 with the qualifier "functionally
  independent"; H-3 bounds where to look for it. Same vocabulary, same catalogue.
- **Folding it in loses no independence.** Its rank-3 count already ran on ansatz's `solve_kt_modp`, by its
  own disclosure. What *is* independent — the irreducibility argument — has now been re-derived by the
  bridge (V5) anyway. Our own rule L17 says independence lives in inputs and methods, not in repositories.
- **Its synthesis role has moved to the bridge**, which is where cross-repo reconciliation belongs.

**One thing to preserve, and it's the reason to be careful rather than quick:** EXP-002 is the fleet's
**most concrete candidate for a result that stands up outside the fleet** — it answers a statement in a
published paper (Cariglia–Galajinsky 2015). It needs a clean, citable home for an outside expert to read.
`high_rank_killing` is not one of the six public repos, so today the result isn't public anywhere.

**Proposal:**
1. The result moves into **ansatz's public repo** as a documented result with its provenance kept:
   *"constructed in the `high_rank_killing` workspace, EXP-002–004, commits `9384d7f`/`6a5b66c`/`b2ebbef`;
   independently re-derived by trivium V5."* ansatz should **verify it first** — its own list currently
   says the opposite (R-9), so it has to accept the result, not just host it.
2. The workspace is **archived, not deleted** — its history is the provenance.
3. The M instrument (**X-1**) goes to whichever session you choose. ansatz asked someone else to lead proof
   work, and quantum's Painlevé item (V1) is adjacent expertise. It doesn't need a new repo either way.
4. Housekeeping for you: the six uncommitted plan copies in `high_rank_killing/Plans/`, and the one
   accidentally committed in `b2ebbef` (its session disclosed it).

---

## 4. What I'd propose as the merged plan — for discussion

**Now** (hours to days):
- Close R-2, R-7, R-8, R-9, R-10 with the owners.
- **H-1**: a sealed, metric-only blind screen of the rank-3 object by tabula. It is a *third* method
  (numerical) after the author's (exact) and the bridge's (V5, exact but independent code). *Caveat
  tabula raised itself: its screen measures polynomial span and would emit the object without flagging
  functional dependence.*
- Cheap next-ups each repo named for itself: **CF-22** (one owner), **V-11**, **M-11**.

**Next** (weeks, multi-repo):
- **X-1**, the proof instrument, controls first, then Manko–Novikov / Tomimatsu–Sato.
- **M-7**: is the GWTC-4 GR tension a finite-SNR bias? (deepstrain injections plus an independent audit.)
- **R-11**: dCS integrability, split by method.
- **B-14**: the fleet's error record, now with this planning exercise's in-fleet misses as a data point.

**Moonshots** (keep two or three alive): the corner mechanism, split by method (cuspis tripartite ·
quantum bound + remainder); **H-2**; **B-5**.

**The outside expert:** EXP-002, now independently re-derived, is ready for a specialist to read.
**That's the single highest-value action on the list, and only you can take it.**

---

## 5. A process fix, not just a note

Three of the bridge's twenty items and ansatz's headline were wrong because of **results already inside
the fleet**. Every list was built from TODO files; none queried what was *done*. cuspis (§2 "Settled") and
deepstrain (§2–3) already keep machine-checkable done-ledgers; the others don't.
**Mechanical fix:** every repo keeps a short *settled results* table (statement · status · commit), and the
bridge's census gains a *results index* across the fleet. A planning list is then checked against it before
it ships, the same way the code-edge census checks imports.

---

## 6. Decisions for you

1. **`high_rank_killing`:** fold into ansatz and archive (my recommendation), or something else?
2. **Who owns X-1**, the proof instrument?
3. **Seek one outside expert for EXP-002?**
4. **quantum's amendment** on the sub-45° check (still pending from earlier).
5. **Then:** do I send R-2/R-7/R-8/R-9/R-10/R-11 to the owners, and circulate a merged plan?
