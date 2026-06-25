#!/usr/bin/env python3
"""Leg M (B1 + A3) — orbital frequencies & resonances in the bumpy metric (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python compute_freqs.py

leg J proved the bump kills the exact Carter constant but left the motion KAM-regular. The OBSERVATIONAL
payoff (EMRIs / LISA): broken integrability concentrates at orbital RESONANCES (ω_r:ω_θ = low-order
rational), where an inspiral can stick/jump — a waveform signature. Step 1 here: compute ω_r, ω_θ for a
family of bumpy orbits and locate resonances. Calibrate on Kerr (frequencies smooth, well-defined). Reuses
legJ/legA machinery read-only.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legJ_integrability_frontier/code")
sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_eccentric as ex
import export_geodesics as eg

OUT = Path(__file__).resolve().parent.parent / "results"
N = ex.N


def orbit_freqs(gfun, x0, u0, steps=20000, dtau=0.1, r_lo=1.5, r_hi=60.0):
    """Integrate; return (ω_r, ω_θ) from radial-minima and latitudinal-maxima spacings in proper time."""
    def rhs(state):
        x, u = state[:N], state[N:]
        G = eg.christoffel_numeric(gfun, x)
        return list(u) + [-sum(G[i][b][c] * u[b] * u[c] for b in range(N) for c in range(N)) for i in range(N)]

    state = list(x0) + list(u0)
    rs, ths, taus = [], [], []
    for k in range(steps):
        x = state[:N]
        if not (r_lo < x[1] < r_hi):
            return None
        rs.append(x[1]); ths.append(x[2]); taus.append(k * dtau)
        k1 = rhs(state)
        k2 = rhs([state[i] + dtau / 2 * k1[i] for i in range(2 * N)])
        k3 = rhs([state[i] + dtau / 2 * k2[i] for i in range(2 * N)])
        k4 = rhs([state[i] + dtau * k3[i] for i in range(2 * N)])
        state = [state[i] + dtau / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(2 * N)]

    def period(sig, taus, want_min):
        # spacing between successive local extrema (interior), averaged
        ext = []
        for i in range(2, len(sig) - 2):
            if want_min and sig[i] < sig[i-1] and sig[i] < sig[i+1]:
                ext.append(taus[i])
            if not want_min and sig[i] > sig[i-1] and sig[i] > sig[i+1]:
                ext.append(taus[i])
        if len(ext) < 2:
            return None
        gaps = [ext[i+1] - ext[i] for i in range(len(ext) - 1)]
        return sum(gaps) / len(gaps)

    Tr = period(rs, taus, want_min=True)        # radial period (pericenter to pericenter)
    Tth = period(ths, taus, want_min=False)     # latitudinal period (max-latitude to max-latitude)
    if not Tr or not Tth:
        return None
    return 2 * math.pi / Tr, 2 * math.pi / Tth


def main():
    print("LEG M (B1+A3) step 1 — orbital frequencies & resonance scan (Kerr calibration + bump)\n")
    rp, thmin = 4.5, math.radians(70.0)
    print(f"  {'metric':6s} {'r_a':>5} {'ω_r':>8} {'ω_θ':>8} {'ω_r/ω_θ':>9}   near low-order resonance?")
    for label, eps in [("Kerr", 0.0), ("bump", 0.35)]:
        gfun = lambda x, e=eps: eg.g_bumpy(x, ex.A, e)
        for ra in [7.0, 9.0, 11.0, 13.0, 15.0]:
            (E, L, Q), res = ex.solve_ELQ(rp, ra, thmin)
            if res > 1e-7 or Q < 0:
                continue
            x0, u0 = ex.launch(gfun, rp, E, L, Q)
            fr = orbit_freqs(gfun, x0, u0)
            if fr is None:
                print(f"  {label:6s} {ra:5.1f}   (unbound/too few periods)")
                continue
            wr, wth = fr
            ratio = wr / wth
            # nearest low-order rational n/m (m≤4)
            best = min(((abs(ratio - n/m), f"{n}:{m}") for m in range(2, 5) for n in range(1, 2*m)),
                       key=lambda t: t[0])
            near = f"≈ {best[1]} (|Δ|={best[0]:.3f})" if best[0] < 0.04 else ""
            print(f"  {label:6s} {ra:5.1f} {wr:8.4f} {wth:8.4f} {ratio:9.4f}   {near}", flush=True)
    print("\n  (calibration: Kerr frequencies are smooth/finite; resonances are where ω_r/ω_θ → low-order n:m.)")


if __name__ == "__main__":
    main()
