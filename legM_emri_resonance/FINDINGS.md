# Leg M — Findings: the observational handle on leg J — frequency map, not chaos (B1 + A3)

*Run 2026-06-24 (backlog B1 "make leg J observational / EMRI" + A3 "targeted resonance hunt"). leg J proved
the bump kills the exact Carter constant but the motion is KAM-regular. B1's premise was that broken
integrability would show as resonance-crossing *glitches* (chaotic kicks) in an EMRI waveform. This tests
that — and the answer corrects the premise. Reuses legA/legJ machinery read-only.*

## Result in one line

The bump's broken integrability is **observable in the orbital frequency map** — it shifts ω_r/ω_θ
substantially (Kerr orbits sit near the **1:2** resonance, bump orbits near **1:3**, because the θ-potential
bump raises ω_θ) — **but NOT as chaos**: a targeted hunt at the bump's 1:3 resonance (the single likeliest
place for chaos) finds the Lyapunov exponent at the Kerr floor and no enhanced Carter drift. So the EMRI
signature of *this* deformation is the smooth frequency-map shift, not resonance-crossing glitches.
**B1-full (step 3, 2026-06-26):** a self-consistent quasi-circular inspiral — radiation reaction (ansatz's
Peters-validated flux) draining (E,L) — now **traverses** that resonance sequence, and the MN quadrupole
bump lowers the orbital frequency at each ω_r:ω_θ crossing by a deviation that grows inward (**−4.8% at 3:4
→ −12.6% at 1:3**). The deviation-from-Kerr is driven by radiation reaction, not just mapped.

## Step 1 — the frequency map (the observable)

| metric | ω_r/ω_θ across r_a = 7 → 15 | nearest low-order resonance |
|---|---|---|
| **Kerr** | 0.514 → 0.622 | near **1:2** at small r_a |
| **bump (ε=0.35)** | 0.310 → 0.372 | near **1:3** (0.340 at r_a≈9) |

The orbital frequencies ω_r (radial) and ω_θ (latitudinal) are what an EMRI waveform is built from. The
bump raises ω_θ markedly (the θ-potential modulation), so the *whole frequency map and resonance structure
shift*. That is a frequency-domain, LISA-relevant signature of the deviation-from-Kerr — independent of any
chaos.

## Step 2 — A3: the targeted resonance hunt (is there chaos AT the resonance?)

| metric | orbit | ω_r/ω_θ | Carter drift | Lyapunov λ |
|---|---|---|---|---|
| Kerr | r_a 7–13 | 0.51–0.61 | ~2e-9 (conserved) | 0.016 (floor) |
| bump | r_a=7 (off) | 0.310 | 0.126 | 0.0154 |
| **bump** | **r_a=9 (on 1:3)** | **0.340** | **0.141** | **0.0177** |
| bump | r_a=13 (off) | 0.372 | 0.169 | 0.0156 |

**No enhancement at the resonance.** On-resonance Carter drift (0.141) sits *between* the off-resonance
values (0.126, 0.169) — it tracks eccentricity, not the resonance — and the Lyapunov exponent is at the
Kerr floor (0.018 vs 0.016) everywhere. So the bump's 1:3 is a **regular resonance** (KAM tori survive,
frequencies merely lock), not a chaotic one. This is the sharpest test of leg J's "no chaos" — at the most
likely place — and the null holds.

## Step 3 — B1-full: the self-consistent inspiral that TRAVERSES the resonances (2026-06-26)

leg M step 1 mapped the resonances *statically*; B1's remaining step was to let radiation reaction **drive**
an inspiral *through* them. ansatz built `emri.py` (Peters-validated `quadrupole_flux`) for exactly this.
`code/inspiral_mn.py` does it on Manko–Novikov as a **quasi-circular equatorial** inspiral — the honest way
around the missing 3rd flux: circular equatorial orbits have **Carter Q=0**, so the inspiral is fully
self-consistent in (E,L) alone, *no dQ/dτ kludge*. The orbit loses (E,L) to GW emission and spirals inward;
the radial:vertical epicyclic ratio ω_r:ω_θ sweeps through the low-order resonances.

**Gated first.** The circular-orbit (E,L) solver (the effective potential W is *quadratic* in (E,L), so
W=−1 ∧ ∂ₓW=0 solve algebraically) reproduces the **Kerr a=0.5 prograde ISCO at r≈4.2M** (xc≈3.75), with
ω_r→0 there and ω_r/ω_θ→1 at large radius (Keplerian) — the epicyclic frequencies are correct before any
inspiral is trusted.

**The inspiral sweep (the deviation-from-Kerr signature, now traversed by a real flux):**

| ω_r:ω_θ resonance | Kerr r/M | bump r/M | **Δω_φ/ω_φ (bump−Kerr)** |
|---|---|---|---|
| 3:4 | 10.33 | 10.65 | **−4.8%** |
| 2:3 |  7.92 |  8.26 | **−6.6%** |
| 3:5 |  6.78 |  7.12 | **−8.0%** |
| 1:2 |  5.71 |  6.06 | **−10.0%** |
| 2:5 |  5.06 |  5.43 | **−11.7%** |
| 1:3 |  4.77 |  5.14 | **−12.6%** |

The MN quadrupole (q=0.2) shifts **every** resonance outward and **lowers the orbital frequency** at each
crossing, by a deviation that **grows inward** (−4.8% → −12.6%) as the quadrupole's strong-field influence
rises — and the inspiral rate `dxc/dτ` (read off the flux) accelerates from −0.01 to −0.12 toward the ISCO,
so the orbit genuinely *passes through* the whole sequence. This is leg M's frequency-map deviation, now
**driven by radiation reaction**, not just plotted — closing B1.

## Step 4 — B1-eccentric: the Carter flux dQ/dτ, and an inclined inspiral that de-inclines (2026-06-26)

B1-full was *quasi-circular* (Carter Q=0) only because the flux returned dE/dτ, dL/dτ. We relayed the gap;
ansatz (§101) delivered the third flux — `quadrupole_flux(…, carter=True) → (dEdt, dLdt, dQdt)`, the
leading (Newtonian) Carter flux. `code/inspiral_inclined.py` validates it on genuinely inclined orbits:

- **Clean on Kerr (Ask A validated).** Across a range of launch inclinations (p_y = 1.33 → 2.33 at x0=8),
  `dQ/dτ` is **negative and grows monotonically more negative** (−1.1e-3 → −3.5e-3): radiation reaction
  drives the inclined orbit toward the equatorial plane — the orbit **de-inclines**, exactly as a
  GW-emitting inspiral must. So the bridge inspiral is no longer restricted to Q=0; with the third flux it
  evolves (E, L, Q) self-consistently.
- **Clean on the bump too — after TWO upstream fixes.** Our first run found the flux *degrading* on MN q=0.2
  (|dE/dτ| inflated, `dQ/dτ` sign-flipping). Relaying the exact failing case triggered two ansatz fixes:
  (i) `f4cc1b1` — a convergence-plateau cutoff for `dE` (a near-resonant orbit's harmonic sum wasn't
  converging) and the **Burke–Thorne RR force** for `dQ`; and (ii) `3e08fef` — the **asymptotic-flatness
  metric fix** (see below). Re-running on the corrected metric, MN q=0.2 is now **clean and physical**:
  `dE/dτ ≈ −6.4e-5` (matching Kerr's −6.3e-5) and `dQ/dτ` negative + monotone (−1.1e-3 → −2.7e-3) — and the
  orbits sit **right next to Kerr's** (launch p_y 1.35 → 2.08 vs Kerr 1.33 → 2.07), exactly as a *mild* q=0.2
  bump should. So B1's generic (eccentric-inclined) case is self-consistent **on both Kerr and the deformed
  metric**: the inclined orbit loses (E, L, Q) and de-inclines in both.

**The asymptotic-flatness metric fix (`3e08fef`) — a correctness win the bridge surfaced.** Pushing Ask 2 to
χ=0.9, q=0.95 forced ansatz to make the shared `manko_novikov` computable at high q — which exposed that it
was **never asymptotically flat for any q≠0**: `g_xx → 0.085×` the Minkowski value at infinity (a stray
constant in the γ potential). It hid because the vacuum check is insensitive to a constant in γ (Ricci=0
survives γ→γ+c) and the q=0≡Kerr anchor has that constant =0. The fix normalizes e^{2γ}→1 at infinity; q=0
stays byte-identical to Kerr, vacuum preserved, `g_xx(q=0.2)/g_xx(q=0) → 1.0004`. **Impact, handled:** the
fix is a constant rescaling of g_xx, g_yy, so it **preserves orbit paths exactly** — box-dimensions, Poincaré
sections, and all leg-J integrability/positive-control results are *invariant* (re-verified: B1-full's
circular-orbit resonance table and Δω_φ shifts are unchanged to 8 sig figs, since equatorial orbits have no
radial/polar motion for g_xx/g_yy to touch). Only *proper-time* quantities move for q≠0 — the eccentric-
inclined flux/frequencies — which is why this section's numbers were re-run on the corrected metric.

(The resonant *kick* — a jump in Q as ω_r:ω_θ crosses a low-order rational — is non-adiabatic, beyond any
orbit-averaged flux, and this leg already found the bump's resonances regular; so the smooth de-inclination
is the full adiabatic story.) `results/inspiral_inclined.json`.

## What it means (honest correction of B1's premise)

We expected broken integrability → chaotic resonance-crossing *glitches*. The reality is subtler and matches
leg J: **the bump is non-integrable but regular**, so there are **no chaotic glitches** — the orbits stay on
tori even at the resonance. The deformation's observational handle is therefore the **frequency-map shift**
(a smooth, deterministic change in ω_r, ω_θ and where the low-order resonances fall), which an EMRI
frequency-evolution measurement would see. "No Carter constant" does *not* imply "chaotic waveform" here; it
implies "shifted frequency structure."

## Honest limits
- The bump is strong (ε=0.35) and ad-hoc; a realistic near-Kerr EMRI deviation is far smaller and the
  ω-shift would scale down — the *mechanism* (frequency-map shift, regular resonances) is the transferable
  point, not the numbers.
- Frequencies from libration-period detection on a finite integration; ratios good to ~±0.01.
- **B1-full scope (step 3).** The inspiral is **quasi-circular** (e=0) — chosen so Carter Q=0 and the
  evolution is self-consistent without the (still-missing) dQ/dτ flux. It therefore maps where the ω_r:ω_θ
  resonances *fall* (via the circular epicyclic ratio) and how the bump shifts them; the actual resonant
  *kick* needs finite eccentricity+inclination (and dQ/dτ) — but leg M step 2 already showed those resonances
  are **regular** (no chaotic kick), so the signature is precisely the smooth frequency-shift this quantifies.
  The flux is ansatz's Peters-validated quadrupole *kludge* (not Teukolsky), adiabatic; the MN quadrupole
  q=0.2 is moderate and the shift scales with q. A fully eccentric-inclined inspiral is the next ask
  (sister-request: dQ/dτ from ansatz).

## Artifacts
- `code/compute_freqs.py` — ω_r, ω_θ from radial/latitudinal libration periods; the resonance scan.
- `code/resonance_study.py` — Carter drift + Lyapunov on vs off the bump's 1:3 resonance (A3). `results/resonance_study.json`.
- `code/inspiral_mn.py` — **B1-full**: circular-orbit (E,L) solver (algebraic, Kerr-ISCO-gated) + epicyclic
  frequencies + the Peters-flux-driven quasi-circular inspiral sweeping ω_r:ω_θ resonances; Kerr vs MN bump.
  `--validate` gates on the Kerr ISCO; `--run` writes `results/inspiral_mn.json`.
- `code/inspiral_inclined.py` — **B1-eccentric**: validates ansatz's Carter flux dQ/dτ (`carter=True`) on
  inclined orbits — clean de-inclining on Kerr; documents the leading-order kludge's degradation on the
  strong bump. `results/inspiral_inclined.json`.
