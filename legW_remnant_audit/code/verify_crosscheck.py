import math
GEV_M = 1.9733e-16      # GeV^-1 -> m
v, MPL = 246.0, 1.22e19
mres = v**2/MPL

def line(tag, printed, correct, note=""):
    r = correct/printed if printed else float('nan')
    print(f"  {tag:22s} paper {printed:<12.3g} correct {correct:<12.3g} off {r:>10.3g}x  {note}")

print("INDEPENDENT CHECK of the other session's claims (from my own PDF read)\n")

print("Their NEW items:")
line("Eq.15 p.7", 1.35e-32, (1/3)*(v/MPL)**2, "mantissa 1.35 EXACT")
mkk = 5e15
line("Eq.22 p.8 r4/lPl", 2.4e33, MPL/mkk, "2.4e33 = M_Pl/M_res (Eq.48) -> transplanted")
line("Eq.45 p.18", 1e69, 64*math.pi**3*(MPL/mres)**2, "order-of-mag claim, mild")
mkk29 = 8.6e15
line("Sec2.6 dS", 1e-29, (4*math.pi/3)*v**2/mkk29**2, "")

print("\nEq.49's deeper problem (their r_4 point):")
r4_sec7 = v/MPL**2 * GEV_M
r4_appA = 3.9e-32
print(f"  r4 from 'r4 ~ <tau0>/M_Pl^2' (Sec 7.1.4) = {r4_sec7:.3g} m")
print(f"  r4 from Appendix A Eq.(A.13)            = {r4_appA:.3g} m")
print(f"  ratio = {r4_appA/r4_sec7:.4g}   <- their claimed 1.2e20   CONFIRMED")

print("\nEq.C.7 -- I HAVE the PDF page 31, they could not see it. Verbatim:")
print('  "Gamma ~ exp(-S_inst) ~ exp(-8pi^2 x 2.5 x 10^33) = exp(-2 x 10^35)"   (C.7)')
print(f"  8pi^2 x 2.5e33 = {8*math.pi**2*2.5e33:.3g}  -> their internal arithmetic is self-consistent")
print(f"  BUT M_Pl/M_res       = {MPL/mres:.4g}      <- this is the 2.5e33 they used")
print(f"      (M_Pl/M_res)^2   = {(MPL/mres)**2:.4g}  <- what Eq.C.6 actually calls for (= Eq.48's number)")
print(f"      correct S_inst   = {8*math.pi**2*(MPL/mres)**2:.3g}")
print("  => CONFIRMED: C.7 substitutes the UNSQUARED ratio. Their proxy inference was right.")

print("\nTHE STRUCTURAL ONE -- Appendix B:")
lnO = (math.pi/3)*(v/MPL)**3
print(f"  Eq.B.8  ln(Omega) = (pi/3)<tau0>^3/M_Pl^3 = {lnO:.3g}   (paper prints 8.6e-51)  MATCHES")
s_with_mres = 4*math.pi*(mres/MPL)**2
print(f"  Eq.B.9  claims that equals 4pi M_BH^2/M_Pl^2")
print(f"          with M_BH = M_res: {s_with_mres:.3g}   (paper's own 2.1e-66)  MATCHES")
print(f"          B.8 vs B.9 differ by {lnO/s_with_mres:.3g}x  -> ~15 orders   CONFIRMED")
print("  Symbolically: B.8 ~ <tau0>^3/M_Pl^3 ; 4pi M_BH^2/M_Pl^2 with M_BH=<tau0>^2/M_Pl ~ <tau0>^4/M_Pl^4")
print(f"          different POWERS of <tau0> -- ratio = (1/12)(M_Pl/<tau0>) = {(1/12)*(MPL/v):.3g}")
print("  And B.1-B.8 contain ONLY <tau0> and M_Pl -- both fixed constants. No M_BH anywhere.")
print("  => a fixed number cannot equal a quantity that scales with progenitor mass.  CONFIRMED")

print("\nWhat is CLEAN (their claim, my check):")
MPL_KG, MSUN = 2.176e-8, 1.989e30
q = 4*math.pi*(MSUN/MPL_KG)**2/math.log(2)
print(f"  Eqs.59-62 solar qubit count = {q:.4g} vs paper 1.515e77  -> clean, confirmed")
