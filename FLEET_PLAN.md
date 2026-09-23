# Fleet plan — how the work fits together

*Draft for discussion with the user, 2026-09-23. Not yet sent to any session as a plan. Built from the six
sessions' lists and `high_rank_killing`'s synthesis. The full merged item list is in
[`fleet/REGISTER.md`](fleet/REGISTER.md) (IDs such as K5 or Q8 refer to it). This page is about how the
tasks connect, not how they score.*

---

## 1. The picture in one paragraph

The six lists describe **five chains of work**. Most tasks are links in a chain: they need something from an
earlier task, or they feed a later one, often in another session. A few tasks are **hubs** that several
chains run through, and **three of those hubs are currently stuck**: a missing proof tool, a pending
decision, and a single overloaded supplier. So the order of work matters more than any single task's appeal.
Unblock the hubs first, and most of the chains start moving on their own.

---

## 2. The five chains

### Chain 1 — The rank-3 vacuum result → something the outside world can check *(ansatz · tabula · bridge · you)*

    EXP-002 (done, high_rank_killing)
      → ansatz verifies it independently and brings it into its repo      [asked; in progress]
      → tabula screens it blind, by a numerical method (K3)               [needs ansatz to supply it, sealed]
      → one outside specialist reads it (F3)                              [only you can do this]
    in parallel:
      which potentials qualify (K2) → the functionally independent version (K1, the moonshot)

**How the pieces work together.** Three different methods — the author's exact construction, the bridge's
independent re-derivation (V5, done), and tabula's numerical screen — look at one object. That is what
makes it presentable. tabula's screen has a known blind spot: it can't see functional dependence. That's
fine, as long as it's stated.

### Chain 2 — Are deformed black holes integrable? *(ansatz · the proof-tool owner · tabula · quantum · bridge)*

This is the fleet's core question, and it runs through **one missing tool**.

    BUILD THE PROOF TOOL (K4) — tested first: ZV δ=2 must come out non-integrable, Kerr integrable
      → Manko–Novikov (K5) ─→ locate its chaotic sea numerically (K20) ─→ PROVE the chaos (K19)
      → Tomimatsu–Sato (K6)       ansatz already has the exact low-rank side
      → scalar-Gauss–Bonnet (K7)  the hardest target, last
      → dCS — is it integrable? (K8)  the published papers contradict each other

    Each target is attacked on three rungs at once, by different sessions:
      exact, rank by rank (ansatz)  ·  numerical screen (tabula, or quantum on a DIFFERENT target)  ·  proof (tool owner)
    ansatz's exact side feeds the dCS question: second-order Carter (K12), pole-order bound (K10), rational engine (K11)

**How the pieces work together.** Every target gets every rung, with a different session on each rung. So
when the rungs agree, it counts as evidence. **Without the proof tool, the chain stops at "none found up to
rank N"**, which is where it has sat for weeks.

**The link to real data.** deepstrain's measurement of how badly the sGB spin series truncates (Round 61)
marks where ansatz's truncated-sGB statements stop describing the real black hole. That's data scoping
theory, and it should be cited that way. The orbital side of this chain (EMRIs, LISA) has **no data path**
in the fleet. Its results are theory and must not be advertised as LIGO-testable.

### Chain 3 — Testing beyond-GR ideas on real LIGO data *(deepstrain · ansatz · bridge)*

    Theory in, data out:
      ansatz supplies the axial–polar splitting (from METRICS) → deepstrain tests isospectrality (Q5)
      sGB spin-series structure (Q16): deepstrain's series + ansatz's symbolic check

    The GW250114 cluster — FOUR analyses of the only informative event:
      direct-wave test (Q8) · quadratic mode (Q10) · isospectrality (Q5) · orthonormal-mode positioning (Q17)
      → these should be run as ONE programme, not four

    Independent-audit pairs:
      deepstrain's injections → an independent statistics audit → "is the GWTC-4 GR tension a bias?" (Q12)
      deepstrain adjudicates the 5.4σ claim (Q3) → an independent audit before anything is called decisive

    Its own next step: the adequate bank from Round 62 → re-score LVK's subsolar triggers (Q6)

**How the pieces work together.** The GW250114 cluster is the one real coordination risk in this chain.
Four analyses of one event share its data preparation. They should share its priors — deepstrain's own L3
finding is that the prior is what moves the answer. And they compound a look-elsewhere effect if each one is
reported alone. One plan for the event, with the four questions pre-registered together, avoids all three
problems.

### Chain 4 — Why the corner band is narrow *(cuspis · quantum · bridge)*

    Two routes to the mechanism, split on purpose:
      cuspis: tripartite information (C2a)       quantum: bound + remainder (C2b)
      → each pre-registers a prediction the other can't see → the bridge compares

    quantum's precision chain:
      continuum a(2π/3), a(π/3) (C20, next) → κ to 30 digits (C16) → closed-form guess by PSLQ (C15)
                                                  ↕
                                   which Painlevé system is behind the equations (C14, the moonshot)

    cuspis's bounds chain:
      test the new cusp inequalities (C17, next) → cuboid under dressing → an UPPER bound on κ (C1, the moonshot)
      every candidate constraint is tested against the "Casimir dressing" trick first

    Settling the free scalar's a₀: analytic route (C13) + larger-mass numerics (C22)

    STUCK: the independent sub-45° check (C12) — waits on your amendment decision, or on a new instrument

**How the pieces work together.** cuspis supplies the settled facts, quantum supplies the precision, and
the bridge compares the two mechanism routes. The two sessions stay on different methods, and quantum never
uses anything built from cuspis's code.

### Chain 5 — Representation learning *(tabula, mostly on its own)*

tabula's own programme (Walrus and the legibility law, embodied agents, learned time-dependent geometry,
field laws, grid cells) is self-contained, and that's healthy. It touches the other chains in three places:
- **The public discoverability benchmark (L12)** takes every session's certified nulls and positives as test
  cases. The rank-3 object is a deliberately subtle positive for it.
- **3+1 Kaluza–Klein (L9)** uses quantum's KK result as a *blind* target.
- **tabula's numerical screens** are the N rung in Chain 2.

---

## 3. The hubs — where chains meet

| Hub | Chains it serves | State | What it needs |
|---|---|---|---|
| **The proof tool** (differential Galois / Kovacic) | 2 (five targets); related tooling to Chain 4's Painlevé work (C14) | **no owner** | your decision |
| **ansatz as supplier** | 1 (absorb, supply the object sealed), 2 (metrics to three sessions), 3 (theory inputs to deepstrain) | **overloaded**: it's on the path of about seven items, plus its own rank-8 run | its supplier duties put ahead of its own new items |
| **Interval-arithmetic tooling** (Arb / CAPD) | 2 (proving chaos, K19); 4 (a certified corner number, C18); certificates for everyone | nobody has it yet | one investment, used three ways |
| **GW250114** | 3 (four analyses) | four separate plans | one programme for the event |
| **Your amendment decision** | 4 (sub-45° check; possibly κ to 30 digits) | pending since this morning | a yes or no |
| **Settled-results index + one certificate format** (bridge, F2 · ansatz, K17) | every chain | not built | prevents another in-fleet miss like B-1 |

**The observation that matters most.** The proof tool and the Painlevé work (C14) are the **same family of
mathematics** — singularity analysis of differential equations. If one session owns both, the fleet gets one
toolkit serving two chains. That's the main reason I'd give the proof tool to **quantum**: its corner work is
paused on your decision anyway, so it has capacity. ansatz would supply the metrics, sealed.

---

## 4. The order that unblocks the most

**Step 1 — decisions (only you):** who owns the proof tool · the amendment · the outside specialist for EXP-002.

**Step 2 — cheap work that feeds other work:**
- ansatz verifies and absorbs EXP-002 → unblocks tabula's blind screen (Chain 1)
- quantum's continuum angles (C20) → feeds its precision chain (Chain 4)
- cuspis's cusp-inequality test (C17) → first step of its bounds chain (Chain 4)
- deepstrain re-scores the subsolar triggers (Q6) — self-contained, and already its declared next
- the bridge builds the settled-results index (F2) — every later list gets checked against it

**Step 3 — build the hubs:** the proof tool, with its controls · one GW250114 programme · the interval-arithmetic
tooling.

**Step 4 — aim the hubs:** Manko–Novikov → chaos proof · dCS on all rungs · the two corner-mechanism routes ·
the GW250114 analyses.

**Kept alive throughout** — one moonshot per session, each inside its own lane: ansatz K1 · tabula K14 or its
Walrus item · deepstrain the direct-wave test · quantum the Painlevé identification · cuspis the upper bound on κ.

---

## 5. One lane per session

| Session | Lane (its instrument) | In the chains above |
|---|---|---|
| **ansatz** | exact symbolic | leads Chain 1's verification; exact rung of Chain 2; theory supplier to Chain 3 |
| **tabula** | numerical screens + representation learning | blind screen in Chain 1; numerical rung of Chain 2; all of Chain 5 |
| **deepstrain** | real data | leads Chain 3 |
| **quantum** | validated numerics + analytic structure | precision and Painlevé in Chain 4; **the proof tool in Chain 2, if you assign it** |
| **cuspis** | corner theory | bounds and mechanism in Chain 4 |
| **bridge** | coordination, independence, statistics audit | compares the method splits; audits Chain 3's claims; settled-results index; error case study |

Lanes are defined by **kind of instrument**, not topic. Several lanes meet on one object on purpose, because
that's what makes agreement count as evidence. What lanes prevent is one instrument used twice on the same
question.

---

## 6. Decisions for you

1. The proof tool's owner — **my recommendation: quantum**, for the toolkit overlap with its Painlevé work.
2. The sub-45° amendment.
3. One outside specialist for EXP-002.
4. Approve the lanes, or move things between them.
5. Whether GW250114's four analyses become one programme under deepstrain.
6. Who owns the statistics-audit pair in Chain 3: the bridge (my proposal) or tabula.
