#!/usr/bin/env python3
"""Leg W v2 — re-audit using ONLY values quoted in the paper's own PDF (primary source).

Paper: Pincak, Pigazzini, Pudlak, Bartos, Gen. Rel. Grav. (2026) 58:29, doi 10.1007/s10714-026-03528-z
Every input below is a verbatim paper value with its page/equation location.
"""
import math

GEV_KG = 1.78266e-27

# --- verbatim from the PDF -------------------------------------------------
TAU0 = 246.0          # abstract; p.10; Eq.(37) text; Conclusions p.26  -- "<tau_0> ~ 246 GeV"
MPL_GEV = 1.22e19     # p.10 VERBATIM: "Inserting the numerical values <tau0> ~ 246GeV, l=1, M_Pl ~ 1.22e19GeV"
PAPER_KG = 9e-41      # abstract: "approximately 9 x 10^-41 kg"; Conclusions: "M_res = <tau0>^2/M_Pl ~ 9e-41 kg"
MPL_KG = 2.176e-8     # p.25 Eq.(59) region VERBATIM: "Planck Mass (M_Pl): Approximately 2.176e-8 kg"
MSUN_KG = 1.989e30    # p.25 VERBATIM: "Solar Mass: Approximately 1.989e30 kg"
PAPER_QUBITS = 1.515e77   # p.25 Eq.(62)

print("LEG W v2 — audit against the PDF (primary source), Eq.(37): M_res = <tau0>^2 / M_Pl\n")

m_gev = TAU0**2 / MPL_GEV
m_kg = m_gev * GEV_KG
print(f"  Paper's own inputs: <tau0> = {TAU0} GeV (abstract/p.10/p.26); M_Pl = {MPL_GEV:.3g} GeV (p.10, verbatim)")
print(f"  Eq.(37) evaluated : {m_gev:.4e} GeV  =  {m_kg:.4e} kg  =  {m_kg/1e-41:.3f} x 10^-41 kg")
print(f"  Paper states      : {PAPER_KG:.0e} kg   (abstract AND Conclusions item 1)")
print(f"  ratio paper/formula = {PAPER_KG/m_kg:.2f}x\n")

# what M_Pl would reproduce the quoted kg value?
need_mpl = TAU0**2 / (PAPER_KG / GEV_KG)
print(f"  To GET 9e-41 kg from Eq.(37) with <tau0>=246 you would need M_Pl = {need_mpl:.3g} GeV")
print(f"  (the paper's own stated M_Pl is {MPL_GEV:.3g} GeV -- a factor {MPL_GEV/need_mpl:.1f} larger)\n")

# --- the qubit chain, following the paper's OWN equations 59-62 ------------
r59 = MSUN_KG / MPL_KG
r60 = r59**2
s61 = 4 * math.pi * r60
q62 = s61 / math.log(2)
print("  Qubit chain, reproducing the paper's Eqs.(59)-(62) with its own constants:")
print(f"    Eq.59  M_sun/M_Pl        = {r59:.4e}   (paper: 9.141e37)")
print(f"    Eq.60  (M_sun/M_Pl)^2    = {r60:.4e}   (paper: 8.356e75)")
print(f"    Eq.61  S = 4pi x that    = {s61:.4e} nats (paper: 1.050e77)")
print(f"    Eq.62  q = S/ln2         = {q62:.4e} qubits (paper: 1.515e77)  -> {abs(q62/PAPER_QUBITS-1):.2%} agreement")
print(f"    NOTE: S = 4pi(M/M_Pl)^2 IS the standard Bekenstein-Hawking entropy. The paper's own")
print(f"    Eq.(46)->(58) derives it as such. Correct arithmetic; no model-specific physics in the number.")
