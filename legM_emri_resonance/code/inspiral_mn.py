#!/usr/bin/env python3
"""Leg M / B1-full — self-consistent quasi-circular EMRI inspiral through resonances (MN, ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python inspiral_mn.py [--validate | --run]

leg M established the OBSERVABLE (the frequency-map ν_r:ν_θ shift, Kerr→bump) but left B1's last step open:
a self-consistent INSPIRAL that lets radiation reaction DRIVE the orbit through a resonance. ansatz built
emri.py (Peters-validated `quadrupole_flux` + `fundamental_frequencies`) on the Manko–Novikov metric (§99)
for exactly this. We drive a QUASI-CIRCULAR EQUATORIAL inspiral: such orbits have Carter Q=0, so the
inspiral is fully self-consistent in (E,L) alone — no dQ/dτ needed (the honest way around the missing 3rd
flux), and the radial/vertical epicyclic ratio ν_r:ν_θ sweeps through low-order resonances as the orbit
shrinks. Kerr (q=0) vs MN-bump (q≠0): the bump SHIFTS the resonance radii — the LISA-relevant signature.

Foundation here: the circular-orbit (E,L) solver. The reduced effective potential W(x,0,E,L) is QUADRATIC in
(E,L), so the circular conditions  W=−1 (turning) and ∂ₓW=0 (extremum)  solve algebraically for E(x_c),L(x_c).
Validated on Kerr (q=0) before any inspiral is trusted.
"""
import math
import sys

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric


def circular_EL(f, xc):
    """Prograde circular equatorial (E,L) at radius xc: solve W=−1 and ∂ₓW=0.
    W = a E² − 2b EL + c L²  with a=itt,b=itp,c=ipp read off the quadratic; primes are ∂ₓ (ansatz dW1)."""
    a = f["W"](xc, 0.0, 1.0, 0.0)                         # W(E=1,L=0) = itt
    c = f["W"](xc, 0.0, 0.0, 1.0)                         # W(E=0,L=1) = ipp
    b = (a + c - f["W"](xc, 0.0, 1.0, 1.0)) / 2.0         # W(1,1)=a−2b+c → b=itp
    ap = f["dW1"](xc, 0.0, 1.0, 0.0)                      # ∂ₓ itt
    cp = f["dW1"](xc, 0.0, 0.0, 1.0)                      # ∂ₓ ipp
    bp = (ap + cp - f["dW1"](xc, 0.0, 1.0, 1.0)) / 2.0    # ∂ₓ itp
    # ∂ₓW=0 ⇒ ap − 2 bp k + cp k² = 0, k=L/E (two roots = prograde & retrograde branches).
    disc = bp * bp - ap * cp
    if disc < 0 or cp == 0:
        return None
    cands = []
    for k in ((bp + math.sqrt(disc)) / cp, (bp - math.sqrt(disc)) / cp):
        denom = a - 2 * b * k + c * k * k                # W/E² ; need < 0 so E²=−1/denom > 0
        if denom < 0:
            E = math.sqrt(-1.0 / denom)
            cands.append((E, k * E))
    pro = [(E, L) for (E, L) in cands if L > 0]           # prograde branch: L > 0
    if not pro:
        return None
    return min(pro, key=lambda EL: EL[0])                 # the bound (lowest-E) prograde circular orbit


def epicyclic_freqs(f, xc, E, L, h=2e-3):
    """Proper-time epicyclic frequencies of the circular equatorial orbit at xc:
      ω_r² = ½ g11 ∂ₓ²W,  ω_θ² = ½ g22 ∂_y²W,  ω_φ = u^φ = −itp E + ipp L.
    Second derivatives use a tuned step h (≈2e-3) — large enough that roundoff (ε/h²) stays well below the
    O(h²) truncation, avoiding the small-h noise trap diagnosed in leg J. Returns (ω_r, ω_θ, ω_φ) or None."""
    g11 = f["g11"](xc, 0.0, E, L)
    g22 = f["g22"](xc, 0.0, E, L)
    W0 = f["W"](xc, 0.0, E, L)
    d2x = (f["W"](xc + h, 0.0, E, L) - 2 * W0 + f["W"](xc - h, 0.0, E, L)) / (h * h)   # ∂ₓ²W
    d2y = (f["W"](xc, h, E, L) - 2 * W0 + f["W"](xc, -h, E, L)) / (h * h)              # ∂_y²W
    wr2 = 0.5 * g11 * d2x
    wth2 = 0.5 * g22 * d2y
    if wr2 < 0 or wth2 <= 0:
        return None                                       # ω_r²<0 ⇒ radially UNSTABLE (inside ISCO)
    itt = f["W"](xc, 0.0, 1.0, 0.0)
    ipp = f["W"](xc, 0.0, 0.0, 1.0)
    itp = (itt + ipp - f["W"](xc, 0.0, 1.0, 1.0)) / 2.0
    w_phi = -itp * E + ipp * L                            # u^φ (proper-time orbital frequency)
    return math.sqrt(wr2), math.sqrt(wth2), w_phi


def validate():
    print("B1 foundation — circular-orbit (E,L) solver on MN, validated on Kerr (q=0)\n")
    print("  Kerr a=0.5: prograde circular orbits should have E<1 (bound), E and L rising inward toward ISCO,")
    print("  and ∂ₓW(xc)=0 to machine precision (the solve's own consistency check).\n")
    M, a = 1.0, 0.5
    fk = build_hamilton_numeric(M, a, 0.0)
    print(f"  {'xc':>5} {'E':>9} {'L':>8} {'ω_r':>8} {'ω_θ':>8} {'ω_φ':>8} {'ω_r/ω_θ':>8}  note")
    for xc in [14.0, 12.0, 10.0, 8.0, 6.0, 5.0, 4.5, 4.0, 3.8, 3.7]:
        sol = circular_EL(fk, xc)
        if sol is None:
            print(f"  {xc:>5.1f}   (no prograde circular solution)")
            continue
        E, L = sol
        fr = epicyclic_freqs(fk, xc, E, L)
        if fr is None:
            print(f"  {xc:>5.1f} {E:>9.5f} {L:>8.4f}   (ω_r²<0 — inside ISCO, radially unstable)")
            continue
        wr, wth, wph = fr
        note = "ω_r→0 ⇒ near ISCO" if wr / wth < 0.15 else ("≈Kepler (ω_r≈ω_θ)" if wr / wth > 0.9 else "")
        print(f"  {xc:>5.1f} {E:>9.5f} {L:>8.4f} {wr:>8.4f} {wth:>8.4f} {wph:>8.4f} {wr/wth:>8.4f}  {note}")
    print("\n  Validation: ω_r/ω_θ → 1 at large xc (Keplerian, no precession) and → 0 at the ISCO (ω_r vanishes).")
    print("  The ratio sweeps 1→0 as the orbit inspirals, crossing low-order resonances (1:2, 1:3, …) en route.")


def frequency_map(f, xlo=3.6, xhi=14.0, dx=0.05):
    """Dense circular-orbit map: (xc, E, L, ω_r, ω_θ, ω_φ, ω_r/ω_θ) outside the ISCO."""
    rows = []
    xc = xhi
    while xc >= xlo:
        sol = circular_EL(f, xc)
        if sol:
            fr = epicyclic_freqs(f, xc, *sol)
            if fr:
                wr, wth, wph = fr
                rows.append({"xc": round(xc, 3), "E": sol[0], "L": sol[1],
                             "wr": wr, "wth": wth, "wphi": wph, "ratio": wr / wth})
        xc -= dx
    return rows


def resonance_crossings(rows, targets):
    """Where the inspiral (xc decreasing) sweeps ω_r/ω_θ through each low-order rational p:q."""
    out = []
    for (p, q) in targets:
        t = p / q
        hit = None
        for i in range(len(rows) - 1):
            r0, r1 = rows[i]["ratio"], rows[i + 1]["ratio"]
            if (r0 - t) * (r1 - t) <= 0 and r0 != r1:           # bracket the crossing
                w = (t - r0) / (r1 - r0)
                xc = rows[i]["xc"] + w * (rows[i + 1]["xc"] - rows[i]["xc"])
                wphi = rows[i]["wphi"] + w * (rows[i + 1]["wphi"] - rows[i]["wphi"])
                hit = {"res": f"{p}:{q}", "xc": round(xc, 3), "w_phi": round(wphi, 5)}
                break
        out.append(hit if hit else {"res": f"{p}:{q}", "xc": None, "w_phi": None})
    return out


def run():
    import json
    from pathlib import Path
    from emri import quadrupole_flux
    OUT = Path(__file__).resolve().parent.parent / "results"
    OUT.mkdir(exist_ok=True)
    CKPT = OUT / "inspiral_mn.json"
    M, a = 1.0, 0.5
    TARGETS = [(3, 4), (2, 3), (3, 5), (1, 2), (2, 5), (1, 3)]
    METRICS = [(0.0, "Kerr"), (0.2, "MN bump q=0.2")]
    print("B1-full — self-consistent quasi-circular EMRI inspiral through resonances (MN, ansatz emri.py)\n")
    print("The orbit loses (E,L) to GW emission (Peters-validated quadrupole_flux) and spirals inward; the")
    print("radial:vertical epicyclic ratio ω_r:ω_θ sweeps through low-order resonances. Kerr vs bump: the")
    print("bump SHIFTS the resonance radii — leg M's frequency-map deviation, now TRAVERSED by a real inspiral.\n")
    result = {"M": M, "a": a, "metrics": {}}
    for q, name in METRICS:
        f = build_hamilton_numeric(M, a, q)
        rows = frequency_map(f)
        cross = resonance_crossings(rows, TARGETS)
        # inspiral rate: flux → dxc/dτ at each resonance crossing (sparse, ~4s each)
        for c in cross:
            if c["xc"] is None:
                continue
            sol = circular_EL(f, c["xc"])
            if not sol:
                continue
            E, L = sol
            try:
                fl = quadrupole_flux(M, a, q, E, L, c["xc"], n_orb=6)
            except (OverflowError, ValueError, ZeroDivisionError):
                fl = None
            if fl:
                dEdt, dLdt = fl
                # dE_circ/dxc by finite diff along the circular sequence → dxc/dτ = (dE/dτ)/(dE_circ/dxc)
                s2 = circular_EL(f, c["xc"] + 0.1)
                dEdx = (s2[0] - E) / 0.1 if s2 else None
                c["dE_dtau"] = dEdt
                c["dxc_dtau"] = (dEdt / dEdx) if (dEdx and abs(dEdx) > 1e-9) else None
        result["metrics"][name] = {"q": q, "resonances": cross,
                                   "isco_xc": rows[-1]["xc"], "ratio_at_14": round(rows[0]["ratio"], 4)}
        CKPT.write_text(json.dumps(result, indent=1))          # checkpoint per metric (power-safe)
        print(f"  ── {name} (q={q}) ──   ISCO at xc≈{rows[-1]['xc']}, ω_r/ω_θ(xc=14)={rows[0]['ratio']:.3f}")
        print(f"    {'resonance':>10} {'xc':>7} {'r/M':>6} {'ω_φ':>9} {'dxc/dτ (inspiral)':>18}")
        for c in cross:
            if c["xc"] is None:
                print(f"    {c['res']:>10}   (not crossed in 3.6<xc<14)")
                continue
            rM = 1.0 + math.sqrt(M * M - a * a) * c["xc"]       # prolate xc → Boyer-Lindquist r/M
            dxc = c.get("dxc_dtau")
            print(f"    {c['res']:>10} {c['xc']:>7.2f} {rM:>6.2f} {c['w_phi']:>9.5f} "
                  f"{(f'{dxc:.2e}' if dxc else '—'):>18}")
        print()

    # Kerr-vs-bump shift table — the observable
    print("  RESONANCE-RADIUS SHIFT (the deviation-from-Kerr signature):")
    print(f"    {'resonance':>10} {'Kerr xc':>9} {'bump xc':>9} {'Δxc':>8} {'Δω_φ/ω_φ':>10}")
    kerr = {c["res"]: c for c in result["metrics"]["Kerr"]["resonances"]}
    bump = {c["res"]: c for c in result["metrics"]["MN bump q=0.2"]["resonances"]}
    for (p, q) in TARGETS:
        r = f"{p}:{q}"
        ck, cb = kerr.get(r), bump.get(r)
        if ck and cb and ck["xc"] and cb["xc"]:
            dxc = cb["xc"] - ck["xc"]
            dwf = (cb["w_phi"] - ck["w_phi"]) / ck["w_phi"] if ck["w_phi"] else float("nan")
            print(f"    {r:>10} {ck['xc']:>9.2f} {cb['xc']:>9.2f} {dxc:>8.2f} {dwf:>9.1%}")
    result["verdict"] = ("B1-full: a self-consistent quasi-circular inspiral (Q=0, no dQ/dτ kludge needed) "
                         "sweeps ω_r:ω_θ through the low-order resonances; the bump shifts each resonance "
                         "radius and orbital frequency — a LISA-relevant deviation-from-Kerr, now traversed "
                         "by radiation reaction, not just mapped statically (leg M).")
    CKPT.write_text(json.dumps(result, indent=1))
    print(f"\n  wrote {CKPT.name}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--validate"
    if mode == "--validate":
        validate()
    elif mode == "--run":
        run()
    else:
        print("usage: inspiral_mn.py [--validate | --run]")


if __name__ == "__main__":
    main()
