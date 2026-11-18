"""V21 C3 (PREREGISTRATION.md + amendment 1): static MN (alpha = 0) axis NVE, eq. (4) in sigma = 2 beta/x^3,
monodromy traces around one / two consecutive turning points of the lattice sigma_j = ln(E^2/mu^2) + i pi (2j+1)."""
import sys, os, json, cmath, math
import numpy as np
from scipy.integrate import solve_ivp

def make(beta, E, mu2):
    def xs(s):
        return (2*beta/s)**(1/3) if True else None      # principal complex cube root (numpy/complex power)
    def dlnP(s):
        x = complex(2*beta/s)**(1/3); W = cmath.exp(s); G = (x - 1)/(x + 1); Gx = 2/(x + 1)**2; xsig = -x/(3*s)
        P = E*E - mu2*W*G; dP = -mu2*(W*G + W*Gx*xsig)
        return dP/P, x
    return dlnP

def monodromy(dlnP, c, R, rtol):
    def rhs(t, Y):
        s = c + R*cmath.exp(1j*t); ds = 1j*R*cmath.exp(1j*t); L, _ = dlnP(s)
        v, vs = Y[0], Y[1]
        return [ds*vs, ds*(-(4/(3*s))*vs - (3/16)*L*L*v)]
    M = np.zeros((2, 2), complex)
    for k, Y0 in enumerate(([1+0j, 0j], [0j, 1+0j])):
        sol = solve_ivp(rhs, (0, 2*math.pi), Y0, method='DOP853', rtol=rtol, atol=rtol*1e-6)
        M[:, k] = sol.y[:, -1]
    return M

out = []
for (beta, E, mu2) in [(0.2, 1.0, 4.0), (-1/3, 1.0, 9.0)]:
    dlnP = make(beta, E, mu2); s0 = math.log(E*E/mu2)
    for j in [10, 100, 1000, 10**4, 10**5, 10**6]:
        sj = complex(s0, math.pi*(2*j + 1))
        row = dict(beta=beta, E=E, mu2=mu2, j=j, x_abs=abs(complex(2*beta/sj)**(1/3)))
        for rtol in (1e-12, 1e-13):
            M1 = monodromy(dlnP, sj, math.pi/2, rtol)                       # one turning point
            M2 = monodromy(dlnP, sj + 1j*math.pi, 1.5*math.pi, rtol)        # two: sigma_j and sigma_{j+1}
            row[f'tr1_{rtol}'] = [np.trace(M1).real, np.trace(M1).imag]
            row[f'tr2_{rtol}'] = [np.trace(M2).real, np.trace(M2).imag]
            row[f'det2_{rtol}'] = abs(np.linalg.det(M2))
        out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/c3.json'), 'w'), indent=1)
