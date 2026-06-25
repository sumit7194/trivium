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
- **Not a waveform.** A full EMRI signal needs the GW energy/angular-momentum fluxes (radiation reaction) to
  drive the inspiral through the resonance; that is the next step (B1 remains PARTIAL). What is established
  here is the geodesic frequency map and that the resonances are regular (no chaotic kick to model).
- Frequencies from libration-period detection on a finite integration; ratios good to ~±0.01.

## Artifacts
- `code/compute_freqs.py` — ω_r, ω_θ from radial/latitudinal libration periods; the resonance scan.
- `code/resonance_study.py` — Carter drift + Lyapunov on vs off the bump's 1:3 resonance (A3). `results/resonance_study.json`.
