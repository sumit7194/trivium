GEV_KG = 1.78266e-27
import math
v, MPL = 246.0, 1.22e19
exact = v**2/MPL

print("ALL 33 PAGES READ. Four checkable arithmetic statements.\n")

print("[1] Eq.(20) p.8 + Eq.(47) p.19 -- the remnant mass")
print(f'    Eq.47 prints: "(246)^2/(1.22e19) ~ 4.96e-15 GeV"')
print(f'    computed    : {exact:.4e} GeV                    -> CORRECT')
print(f'    Eq.20 prints: "~ 5e-15 GeV ~ 9e-41 kg"')
print(f'    5e-15 GeV in kg = {5e-15*GEV_KG:.3e} kg -> rounds to 9e-42 kg')
print(f'    paper says 9e-41 kg  -> WRONG by {9e-41/(exact*GEV_KG):.1f}x (mantissa 9 right, exponent -42 -> -41)\n')

print("[2] Eq.(25) p.9 vs Eq.(17) p.7 -- same quantity in eV")
print(f'    Eq.17 prints: m_phys ~ 1e-15 GeV = {1e-15*1e9:.0e} eV')
print(f'    Eq.25 prints: m_phi ~ v^2/M_Pl ~ 1e-3 eV, "same order of magnitude as Eq.(17)"')
print(f'    computed    : v^2/M_Pl = {exact*1e9:.2e} eV  -> same order as Eq.17 CORRECT')
print(f'    paper says 1e-3 eV   -> WRONG by {1e-3/(exact*1e9):.0f}x, and contradicts its own Eq.17\n')

print("[3] Eq.(49) p.19 -- the KK mass")
kk = MPL**2/v
print(f'    Eq.49 prints: "M_KK ~ M_Pl^2/<tau0> = (1.22e19)^2/246 ~ 6.05e15 GeV"')
print(f'    computed    : {kk:.3e} GeV')
print(f'    mantissa 6.05 MATCHES; exponent off by {round(math.log10(kk/6.05e15))} orders')
print(f'    (elsewhere the paper gives M_KK ~ 5e15 GeV: Eq.21 p.8, Eq.29 p.10, Eq.C.8 p.31 -- so the')
print(f'     PHYSICAL value is consistent; it is the printed division in Eq.49 that does not evaluate)\n')

print("[4] Eq.(C.7) p.31 vs Eq.(48) p.19 -- the instanton action")
ratio = MPL/exact
print(f'    Eq.48 prints: (M_Pl/M_res)^2 = (2.46e33)^2 ~ 6.05e66      [computed: {ratio:.3e} -> {ratio**2:.3e}] CORRECT')
print(f'    Eq.C.6      : S_inst = 8pi^2 * M_Pl^2/M_res^2')
print(f'    Eq.C.7 uses : 8pi^2 * 2.5e33 = 2e35     <- 2.5e33 is M_Pl/M_res, NOT its SQUARE')
print(f'    should be   : 8pi^2 * {ratio**2:.3e} = {8*math.pi**2*ratio**2:.2e}')
print(f'    -> Eq.C.7 contradicts Eq.48 in the same paper (and Eq.45 p.18 says exp(-1e69), a 3rd value)')
print(f'    -> physically inconsequential (all are effectively zero) but arithmetically inconsistent')
