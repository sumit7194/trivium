#!/usr/bin/env python3
"""Leg W — arithmetic audit of the G₂-remnant paper (Pinčák et al., GRG 58(3) 2026). Stdlib only.

    python3 remnant_audit.py

Gates W1a/W1b/W2 (+ observation O3) frozen in ../PREREGISTRATION.md before this was written. The audit
recomputes the paper's quoted numbers from its OWN formulas and constants: M_res = <tau0>^2 / M_Pl with
<tau0> = 246 GeV, M_Pl = 1.22e19 GeV; S = 4*pi*(M/M_Pl)^2. Verdicts are about internal consistency of the
published numbers, not about the 7D Einstein-Cartan model.
"""
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results"

# frozen constants (PREREGISTRATION.md)
GEV_TO_KG = 1.78266e-27          # 1 GeV/c^2 in kg
M_PL_GEV = 1.22e19               # the paper's own Planck mass
M_PL_KG = 2.17643e-8
M_SUN_KG = 1.98892e30
TAU0_GEV = 246.0

# the paper's quoted values
PAPER_GEV = 4.96e-15             # eq. 47 (abstract-level ~5e-15 GeV)
PAPER_KG = 9e-41                 # abstract + eq. 20 (the press-propagated number)
PAPER_QUBITS = 1.515e77          # solar-mass information claim


def main():
    print("LEG W — arithmetic audit: Pinčák et al., GRG 58(3) 2026 (gates frozen in PREREGISTRATION.md)\n")

    # ---- W1: the remnant mass, from the paper's own formula
    m_gev = TAU0_GEV ** 2 / M_PL_GEV
    m_kg = m_gev * GEV_TO_KG
    r_gev = PAPER_GEV / m_gev
    r_kg = PAPER_KG / m_kg
    w1a = abs(r_gev - 1) < 0.05
    w1b = max(r_kg, 1 / r_kg) < math.sqrt(10)
    print(f"  W1 M_res = <tau0>^2/M_Pl = 246^2 / 1.22e19:")
    print(f"     formula:            {m_gev:.3e} GeV  =  {m_kg:.3e} kg  (= {m_kg/1e-41:.3f} x 10^-41 kg)")
    print(f"     paper eq.47 (GeV):  {PAPER_GEV:.2e} GeV   ratio {r_gev:.3f}   "
          f"W1a {'PASS ✅' if w1a else 'FAIL ❌'}")
    print(f"     paper eq.20 (kg):   {PAPER_KG:.0e} kg      ratio {r_kg:.2f}x   "
          f"W1b {'PASS ✅' if w1b else 'FAIL ❌ — the kg figure is ~10x its own GeV figure'}")
    if not w1b:
        print(f"     → the paper's two quoted masses are mutually inconsistent: 9e-41 kg back-converts to")
        print(f"       {PAPER_KG/GEV_TO_KG:.2e} GeV, 10x eq.47. The formula-true value is 0.884e-41 kg —")
        print(f"       consistent with a dropped leading zero (0.884e-41 ≈ '0.9e-41' → '9e-41').")
        print(f"       The kg number is the one the world press propagated.")

    # ---- W2: the qubit count = standard Bekenstein-Hawking in bits
    s_nats = 4 * math.pi * (M_SUN_KG / M_PL_KG) ** 2
    s_bits = s_nats / math.log(2)
    r_q = PAPER_QUBITS / s_bits
    w2 = abs(r_q - 1) < 0.01
    print(f"\n  W2 solar-mass information claim:")
    print(f"     4π(M_sun/M_Pl)^2 = {s_nats:.4e} nats = {s_bits:.4e} bits")
    print(f"     paper: {PAPER_QUBITS:.3e} qubits   ratio {r_q:.4f}   W2 {'PASS ✅' if w2 else 'FAIL ❌'}")
    print(f"     note (frozen): this is EXACTLY the standard Bekenstein-Hawking entropy of a solar-mass")
    print(f"     hole, nats→bits — the number contains no physics specific to the 7D model.")

    # ---- O3: observation (not a gate) — the remnant's own geometric entropy
    s_rem = 4 * math.pi * (m_kg / M_PL_KG) ** 2
    gap = math.log10(s_bits) - math.log10(s_rem)
    print(f"\n  O3 (observation, not gated): the remnant's own Bekenstein entropy at M_res is")
    print(f"     4π(M_res/M_Pl)^2 = {s_rem:.2e} nats — vs the ~1e77-qubit storage claim: a ~{gap:.0f}-order")
    print(f"     gap. The standard remnant-capacity objection (Chen-Ong-Yeom 2412.00322); the paper's")
    print(f"     trapped-QNM/interior mechanism must carry all of it. Physics commentary, no verdict.")

    OUT.mkdir(exist_ok=True)
    (OUT / "remnant_audit.json").write_text(json.dumps({
        "formula_gev": m_gev, "formula_kg": m_kg,
        "paper_gev": PAPER_GEV, "paper_kg": PAPER_KG, "ratio_gev": r_gev, "ratio_kg": r_kg,
        "W1a_pass": bool(w1a), "W1b_pass": bool(w1b),
        "s_bits_solar": s_bits, "paper_qubits": PAPER_QUBITS, "ratio_qubits": r_q, "W2_pass": bool(w2),
        "remnant_own_entropy_nats": s_rem, "capacity_gap_orders": gap,
        "verdict": ("The paper's GeV remnant mass (4.96e-15) follows from its own formula (W1a PASS); its "
                    "kg value (9e-41, the press-propagated number) is ~%.1fx the formula/its own GeV value "
                    "(W1b FAIL) — consistent with a dropped leading zero of 0.884e-41 kg. The 1.515e77-qubit "
                    "claim is exact standard Bekenstein-Hawking in bits (W2 PASS, no model-specific "
                    "physics). Audit of quoted numbers only; the 7D model itself is out of scope."
                    % max(r_kg, 1 / r_kg)),
    }, indent=1))
    print(f"\n  wrote results/remnant_audit.json")


if __name__ == "__main__":
    main()
