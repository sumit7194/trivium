# Practice change — DRAFT for Sumit's approval (2026-11-27)

**Why.** We are good at catching errors and bad at asking whether the work is worth doing. Evidence from the record:
the horseshoe plan has 67 revisions since 16 Oct and no proof yet; Kerr control runs were launched before the target
they protect existed, then projected at 3 weeks to 2 months; about 1,350 commits in the last week (586 of them the
Bridge's own log lines); 9 registered clarifications in one evening on one project; memory under-declared 5 times.
Every fix so far went to the incident, not to the cause.

**Root causes.** (1) We gate correctness, never value. (2) No stop rule balances "rigour always / don't park / no
budget limit". (3) Costs are estimated after launch, not measured before. (4) Each sister builds its own launch
tooling, so the same mistakes recur. (5) One log serves both the machine record and the human reader.

## The five changes

1. **Value-and-cost gate.** Any run over ~12 hours or ~1 core-day needs one plain paragraph *before* launch:
   what result it gives and which decision it changes; its cost, **measured by a short pilot**; whether it depends on
   something not yet working; and its stop rule. The Bridge approves on value, not only on correctness.
   **Anything over ~3 days of machine time goes to Sumit.**

2. **Time box per research thread.** Each thread gets a budget in weeks and at most **3 plan revisions** per stage.
   At the limit: write up what is solid, then continue only with a fresh, short plan that Sumit approves — or close it.
   First application: the horseshoe thread's stop-or-go test (the small MN covering pilot).

3. **"Good enough" decided up front.** Each proof states at the start what counts as done (e.g. ansatz: a certified
   lower part of region A is a publishable result). Reaching it means we stop and publish, not chase the rest.

4. **Two-layer reporting.** The full log stays for honesty, but it is not what humans read. Each thread keeps **one
   plain-language page** (what we know, what's running, next decision), updated only when something changes. The
   Bridge logs far less: decisions and outcomes, not every message. Clarifications are batched into one amendment, not
   dribbled out one by one.

5. **One shared launch kit.** One tested set of guards, watchers and true-memory measurement for every sister,
   including a pilot step that measures memory and time before anything is declared. Built once, used everywhere.

**Not changed.** Pre-registration, sealed predictions, non-author reads, honest reporting of misses, pause-only guards.
These work; the change is about *what* we spend them on and *when we stop*.

**If approved:** the Bridge sends this to every sister, adds it to FLEET_PRACTICES, starts the one-page summaries
with the four active threads, and applies the value gate to the next long run.
