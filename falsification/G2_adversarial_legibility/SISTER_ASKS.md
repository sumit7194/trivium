# Round-8 sister asks — the adversarial-legibility round (G2) + K5 + G6

*Compiled 2026-07-23 by the bridge. Two paste-ready blocks: one for **ansatz** (`conjecture_machine`), one for
**tabula** (`SpaceTime`). The joint gate is frozen in [PREREGISTRATION.md](PREREGISTRATION.md) **before** either
sister is asked — deliberately, so no goalpost can move once verdicts arrive.*

**Dependency map**

| ask | to | independent? | bridge wait-point |
|---|---|---|---|
| **A. Build the two adversarial metrics** (G2 candidates A & B) | ansatz | ✅ | bridge seals the symbolic verdict, then joins tabula's blind run |
| **B. Blind legibility on those metrics** (G2) | tabula | ✅ — **must stay blind to ansatz's verdict** | the G2 decision table |
| **C. Blind legibility on the GWW drums** (K5) | tabula | ✅ | K5 verdict (bridge ships the drum data) |
| **D. Extend CK to order 2** (G6) | ansatz | ✅ | G6 becomes testable at all |

**Ordering note:** B depends on A (tabula needs the metrics). C and D are independent and can run immediately.

---

## Block 1 — to **ansatz** (`conjecture_machine`)

> **Round-8 ask from the bridge — adversarial metric design (Falsification Ledger G2) + a CK upgrade (G6).**
>
> Context: leg Q established "a learned geometry is **legible ⟺ the metric is KY-integrable**" — 8/8 metrics,
> Matthews φ = 1.0, across three independent non-integrable deformation classes, cross-validated between your
> symbolic KY survey and tabula's neural probe. But **all 8 were found, not designed.** The bridge's
> Falsification Ledger item G2 attacks that claim deliberately. The joint gate is already frozen on our side
> (`falsification/G2_adversarial_legibility/PREREGISTRATION.md`) — we are not going to move it after seeing
> your answer.
>
> The problem: in every catalog entry so far, **KY-ness, integrability, and polynomial-invariance coincide**,
> so the record cannot distinguish three different things legibility might really be tracking — KY structure
> specifically, integrability in general, or merely the existence of a *polynomial* invariant. Two designed
> metrics separate them.
>
> **A1 — Candidate A: integrable, but with NO Killing–Yano root.**
> Construct a 4D metric admitting an **irreducible Killing tensor (rank 2 or rank 4) that is not the square of
> any Killing–Yano tensor**. This is your §98 quartic-search machinery **inverted — build, don't detect** — with
> §69's KY machinery used to *certify the absence* of a KY root (K_ab ≠ Y_ac Y_b{}^c for any Y). Please ship:
> the metric, the explicit conserved quantity, the Killing-tensor rank, and the KY-absence certificate.
>
> **A2 — Candidate B: integrable, but with a TRANSCENDENTAL invariant.**
> Construct (or identify, with citation, from the integrable-systems literature) a metric — or, if no geometric
> example is in reach, a geodesic-like Hamiltonian we can hand tabula — whose conserved quantity is **not
> polynomial in the momenta**, with polynomial invariants of degree ≤ 4 **excluded** by your §97/§98 searches
> while the transcendental one is exactly conserved.
>
> **Honest scoping, stated up front:** either candidate may simply not exist in the one-variable ansatz world.
> **"Not constructible" is a fully acceptable, pre-registered outcome** — we have logged UNDECIDED-by-construction
> in advance. Please treat this as a bounded ask, not an open-ended search, and tell us the obstruction if you
> hit one (an obstruction is itself a result we will bank).
>
> **Blind protocol — important:** please send the symbolic verdicts (KY yes/no, rank, the invariant) **to the
> bridge only**. tabula must run legibility on these metrics *without* knowing their integrability status. The
> two repos being ignorant of each other is the entire reason an agreement counts as evidence rather than an
> echo; leakage voids the round.
>
> **D — separate, independent ask (Ledger G6): extend `ck.py` to order 2.**
> G6 postulates "CK terminates at order ≤ 2 for all 4D vacuum type-D pairs in our catalog" (theory allows 7).
> We went to test it and found we cannot: `ck.py` computes **orders 0 and 1 only** — it has no order-2 path at
> all, and the tool itself flags the gap (the `cert_failures` branch says *"the order-1 elimination was skipped
> — needs order 2"*). We deliberately did **not** patch your code — sisters are read-only for us. Extending the
> recursion to order 2 would make G6 testable, and would also close the three vacuum-vs-vacuum pairs leg Y left
> open (Kerr vs Taub–NUT, Kerr vs ZV δ=1, Taub–NUT vs ZV δ=1), which walled precisely because their matter
> sector is identically zero and separating them needs the Weyl-side machinery.
>
> Also worth noting for your own ledger: leg Y concluded **"the wall was largely the simplifier, not the
> chart"**, and your §119 `zsimp`-escalation already decided bumpy vs Manko–Novikov at order 0 — so the order-2
> extension may now be much cheaper than it looked in July.

---

## Block 2 — to **tabula** (`SpaceTime` / `curvature`)

> **Round-8 ask from the bridge — blind adversarial legibility (Ledger G2) + the isospectral drums (K5).**
>
> Context: your legibility instrument (§127/§132/§144) and ansatz's symbolic KY survey agree metric-by-metric —
> leg Q's "legible ⟺ KY-integrable", 8/8, φ = 1.0. The bridge's Falsification Ledger now attacks that claim on
> purpose. **All 8 entries were found, not designed**; we have asked ansatz to *design* two metrics specifically
> to break the biconditional.
>
> **B — the G2 blind run.** ansatz is building two adversarial metrics. When they arrive (the bridge will relay
> them), please run your **emit-or-certify** legibility instrument on each, exactly as you did for ZV (§132) and
> Manko–Novikov (§144): build the geodesic Hamiltonian, look for a conserved quantity, and report **legible**
> (you emit a verified invariant, with your held-out variance numbers) or **illegible** (you certify none, with
> the drift/floor ratio).
>
> **Please stay blind.** We will send you the metrics **without** their integrability or Killing–Yano status.
> ansatz's symbolic verdict is sealed on the bridge side until your answer is in. That blindness is exactly what
> made the MN cross-check evidence rather than an echo (you built MN from Gair–Li–Mandel, not from ansatz's
> code) — we would like to preserve it. If you happen to recognise a metric, please say so rather than
> proceeding, and we will handle it.
>
> One thing we genuinely do not know the answer to, stated honestly: one candidate is designed to be integrable
> via a **transcendental** (non-polynomial in momenta) invariant. If your distillation head is polynomial-basis
> by construction, "illegible" is a perfectly good and informative answer — it would tell us legibility tracks
> *polynomial* invariants specifically. We are not fishing for a particular verdict; both directions are
> pre-registered as findings.
>
> **C — separate, independent ask (Ledger K5): can a net hear the shape of a drum?**
> K5 postulates *"a neural net trained on projections can learn ONLY the spectrum"* — i.e. behavioural data
> carries no more than eigenvalues. The bridge has just built the test case (Ledger K2,
> `falsification/K2_isospectral_drums/`): the two **Gordon–Webb–Wolpert** drums, whose Dirichlet spectra we
> verified identical to **~10⁻¹⁵ and, crucially, resolution-independently** — the discrete transplantation is
> combinatorially exact, not an FD approximation — while the domains are provably non-congruent (exhaustive
> dihedral + translation search).
>
> So: **train on projections from the two drums and ask whether your net can distinguish them.** If it can,
> K5 is dead — eigen*functions* leak through projections even when eigen*values* are identical, which would be
> a sharp statement about what representation learning actually accesses. If it cannot, that is equally
> informative. The bridge ships `code/k2_drums.py` (exact vertex data, the interior-mask/Laplacian builder, and
> the verified-identical spectra) so you can generate as much data as you want at any resolution — note our
> grid-alignment guard: use n where the two drums give **equal interior-point counts** (n = 16, 32, 64 are good;
> n = 24 is not).

---

## What the bridge does when answers land

1. Seal ansatz's symbolic verdicts; relay **metrics only** to tabula.
2. On tabula's blind verdicts, unseal and apply the **frozen decision table** in
   [PREREGISTRATION.md](PREREGISTRATION.md) — G2 is KILLED if either candidate breaks the biconditional
   (legible without KY, or KY without legible), and SURVIVES-9/10 only if it holds on both.
3. K5 and G6 are logged as their own ledger entries with their own verdicts.
4. Any survivor that starts to look interesting goes through the standing **prior-art sweep before anyone gets
   excited** — including a check on whether the constructed candidates are already known objects.
