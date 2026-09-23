"""V7d -- conformal concavity (F = tan(theta/4) a convex in u = tan^2(theta/4)) on exactly known corner functions.
Pass rule (frozen): min second divided difference >= -1e-8 * max|F| ; each perturbed control must fail it.
Holographic function: the bridge's own derivation of the Hirata-Takayanagi RT surface (z = rho h(phi)),
normalised L^2/(2G) = 1 so C_T = 3L^2/(pi^3 G) = 6/pi^3; self-checked against sigma = pi^2 C_T/24.
"""
import numpy as np, mpmath as mp, json
mp.mp.dps = 30
def sdd(u, F):
    u = np.asarray(u, float); F = np.asarray(F, float); o = np.argsort(u); u, F = u[o], F[o]
    s = np.diff(F)/np.diff(u); return np.min(np.diff(s)/((u[2:] - u[:-2])/2)), np.max(np.abs(F))
def verdict(u, F):
    m, M = sdd(u, F); return dict(min_sdd=float(m), maxF=float(M), passes=bool(m >= -1e-8*M))
out = {}
# --- EMI: a = 1 + (pi - theta) cot theta  (kappa = pi, sigma = 1/3) ---
th = np.linspace(1e-3, np.pi - 1e-3, 4001)
aE = 1 + (np.pi - th)/np.tan(th); u = np.tan(th/4)**2; F = np.tan(th/4)*aE
out['EMI'] = verdict(np.r_[0, u, 1], np.r_[np.pi/4, F, 0])
bump = aE + 0.05*np.exp(-((th - 1.0)/0.08)**2)
out['EMI_bump_control'] = verdict(np.r_[0, u, 1], np.r_[np.pi/4, np.tan(th/4)*bump, 0])
amin = np.log(1/np.sin(th/2))                              # BWK's minimal function: kappa = 0, F(0) = 0
out['amin_control'] = verdict(np.r_[0, u, 1], np.r_[0, np.tan(th/4)*amin, 0])
# --- holographic (Einstein) ---
def holo(h0):
    h0 = mp.mpf(h0); s = mp.sqrt(1 + h0**2)
    def hh(t): return h0*mp.sin(t)
    Om = 2*mp.quad(lambda t: hh(t)**2*s/(mp.sqrt(1 + hh(t)**2)*mp.sqrt(h0**2 + (1 + h0**2)*hh(t)**2)), [0, mp.pi/2])
    def integrand(t):   # (f - 1/h^2) dh, h = h0 sin t, in a cancellation-free form:
        # (1+h^2)^2 h0^4 - P = (1+h^2)(1+h0^2) h^4  =>  f - 1/h^2 = (1+h^2)(1+h0^2) h^2 / (sqrtP ((1+h^2) h0^2 + sqrtP))
        h = hh(t); c = mp.cos(t); r = mp.sqrt((1 + h**2)*(h0**2 + (1 + h0**2)*h**2)); sqrtP = r*h0*c
        return (1 + h**2)*(1 + h0**2)*h**2/(r*((1 + h**2)*h0**2 + sqrtP))
    # (Drafts 1-2 subtracted 1/h^2 numerically; the 1/t^2 cancellation lost digits near t = 0, the sigma and
    #  monotonicity self-checks FAILED, so those runs' concavity verdicts are void. Instrument fixed, not the tolerance.)
    Q = 1/h0 - mp.quad(integrand, [0, mp.pi/2])
    return float(Om), float(Q)                    # a = (L^2/2G) Q = Q
h0s = np.logspace(-2.5, 2.5, 300)
pts = [holo(h) for h in h0s]
Om = np.array([p[0] for p in pts]); aH = np.array([p[1] for p in pts])
CT = 6/np.pi**3
# self-checks: sigma and kappa
eps = np.pi - Om[-5:]; sig = aH[-5:]/eps**2
kap = Om[:5]*aH[:5]
out['holo_selfcheck'] = dict(sigma_over_CT_numeric=[float(x) for x in sig/CT], sigma_over_CT_expected=float(np.pi**2/24),
                             kappa_over_CT_small_angle=[float(x) for x in kap/CT], monotone_decreasing=bool(np.all(np.diff(aH) < 0)))
uH = np.tan(Om/4)**2; FH = np.tan(Om/4)*aH
kappaH = float(kap[0])     # smallest-angle estimate of kappa
out['holographic'] = verdict(np.r_[uH], np.r_[FH])        # interior points only (endpoint kappa estimated)
out['holographic_with_F0'] = verdict(np.r_[0, uH], np.r_[kappaH/4, FH])
out['holographic_bump_control'] = verdict(uH, np.tan(Om/4)*(aH + 0.02*aH.max()*np.exp(-((Om - 1.2)/0.1)**2)))
# --- CHL09 free-field points (real scalar = complex-scalar entries halved) ---
def four(k, a90, a135):
    return verdict([0, np.tan(np.pi/8)**2, np.tan(3*np.pi/16)**2, 1], [k/4, np.tan(np.pi/8)*a90, np.tan(3*np.pi/16)*a135, 0])
out['CHL09_real_scalar'] = four(0.0397, 0.01183, 0.002520)
out['CHL09_dirac'] = four(0.0722, 0.02329, 0.005022)
out['CHL09_scalar_wrong_complex_a90_control'] = four(0.0397, 0.02366, 0.002520)   # the trap: complex value at 90 deg
for k, v in out.items(): print(k, v)
json.dump(out, open('../results/v7d_known.json', 'w'), indent=1)
