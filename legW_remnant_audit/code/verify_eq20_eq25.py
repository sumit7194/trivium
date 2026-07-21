GEV_KG = 1.78266e-27
v, MPL = 246.0, 1.22e19
exact = v**2/MPL

print("=== Eq.(20), p.8 — the paper prints BOTH values on one line ===")
print(f'  paper: "M_res = (246 GeV)^2/(1.22e19 GeV) ~= 5e-15 GeV ~= 9e-41 kg"\n')
print(f"  the division      : {exact:.4e} GeV   -> paper's '5e-15 GeV'   CORRECT")
print(f"  5e-15 GeV in kg   : {5e-15*GEV_KG:.4e} kg  -> rounds to 9e-42 kg")
print(f"  exact in kg       : {exact*GEV_KG:.4e} kg  -> rounds to 9e-42 kg")
print(f"  paper prints      : 9e-41 kg            -> off by {9e-41/(exact*GEV_KG):.2f}x")
print("\n  FORENSICS: the mantissa '9' is EXACTLY right. Only the exponent is wrong:")
print("  -42 was printed as -41. One digit. The GeV value it converts FROM is correct.\n")

print("=== Eq.(25), p.9 vs Eq.(17), p.7 — same quantity, two more units ===")
m17_gev = 1e-15                       # Eq.(17): "m_phys ~= 1 x 10^-15 GeV"
print(f'  Eq.(17) prints: m_phys ~= 1e-15 GeV      = {m17_gev*1e9:.0e} eV')
print(f'  Eq.(25) prints: m_phi ~ v^2/M_Pl ~= 1e-3 eV')
print(f"  but v^2/M_Pl  = {exact:.3e} GeV        = {exact*1e9:.2e} eV")
print(f"\n  Eq.(25) says this is 'the same order of magnitude as Eq.(17)'.")
print(f"    Eq.(17) in eV : {m17_gev*1e9:.0e} eV")
print(f"    v^2/M_Pl in eV: {exact*1e9:.1e} eV   <- SAME ORDER as Eq.(17). The claim is right.")
print(f"    printed value : 1e-3 eV          <- {1e-3/(exact*1e9):.0f}x larger; NOT the same order as Eq.(17)")
print(f"\n  If GeV->eV were done with 1e12 instead of 1e9: {exact*1e12:.1e} eV ~ 1e-3 eV  <- reproduces it")
print("\n  => BOTH slips are UNIT CONVERSIONS of the SAME correct number, 5e-15 GeV.")
