"""V23 addendum A: Melnikov function M(psi0) = int {K_r, K_1} dlambda computed directly (bracket form), vs Ups*L'(psi0)."""
import json, os, numpy as np, mpmath as mp
from v23 import Level, pieces, theta_motion, harmonics
HERE = os.path.dirname(os.path.abspath(__file__))

def bracket_M(lev, kind, psi0, Nchi=4096, Tfac=40.0, nlam=40001, hx=1e-6):
    G0, G1 = pieces(float(lev.M), float(lev.a), kind)
    M_, a, E, L, Q, k = (float(v) for v in (lev.M, lev.a, lev.E, lev.L, lev.Q, lev.k))
    chi, zt, psit, dpsi, Ups = theta_motion(lev, Nchi)
    # psi(chi) is monotone over a period; build z(psi) by interpolation on an extended grid
    psi_ext = np.concatenate([psit - 2*np.pi, psit, psit + 2*np.pi]); z_ext = np.concatenate([zt, zt, zt])
    zof = lambda p: np.interp(np.mod(p, 2*np.pi), psi_ext, z_ext)
    T = Tfac/float(lev.kap); lam = np.linspace(-T, T, nlam); dl = lam[1] - lam[0]
    A, B, kap, ru = float(lev.A), float(lev.B), float(lev.kap), float(lev.ru)
    den = (B - A) + (A + B)*np.cosh(kap*lam)
    r = ru + 2*A*B/den; drdl = -2*A*B*(A + B)*kap*np.sinh(kap*lam)/den**2
    D = r*r - 2*M_*r + a*a; pr = drdl/D; px = k*pr
    z = zof(psi0 + Ups*lam)
    Zv = Q - (Q + a*a*(1 - E*E) + L*L)*z*z + a*a*(1 - E*E)*z**4; py2 = np.maximum(Zv, 0)/(1 - z*z)**2
    x = (r - M_)/k
    def K1(xx):
        rr = M_ + k*xx; g1 = G1(xx, z)
        return (rr*rr + a*a*z*z)*0.5*(g1['tt']*E*E - 2*g1['tp']*E*L + g1['pp']*L*L + g1['xx']*px*px + g1['yy']*py2)
    dK1dx = (K1(x + hx) - K1(x - hx))/(2*hx)
    g1 = G1(x, z); dK1dpx = (r*r + a*a*z*z)*g1['xx']*px
    # K_r(x, p_x) = 1/2 [ D p_x^2/k^2 - P^2/D + r^2 ],  P = E(r^2+a^2) - aL
    def Kr(xx):
        rr = M_ + k*xx; DD = rr*rr - 2*M_*rr + a*a; P = E*(rr*rr + a*a) - a*L
        return 0.5*(DD*px*px/(k*k) - P*P/DD + rr*rr)
    dKrdx = (Kr(x + hx) - Kr(x - hx))/(2*hx); dKrdpx = D*px/(k*k)
    integ = dKrdx*dK1dpx - dKrdpx*dK1dx
    return float(dl*(integ[0]/2 + integ[1:-1].sum() + integ[-1]/2)), Ups

if __name__ == '__main__':
    base = Level(5, 3, 16, mp.mpf(1)/2, (mp.mpf('0.94'), mp.mpf('13'), mp.mpf('56')))
    h, meta = harmonics(base, 'beta', [2, 4]); L2, L4 = h[2].real, h[4].real; Ups = meta['Ups']
    out = {}
    for psi0 in (np.pi/4, np.pi/8, 0.0):
        Mb, _ = bracket_M(base, 'beta', psi0)
        Mp = Ups*(-4*L2*np.sin(2*psi0) - 8*L4*np.sin(4*psi0))
        out[f'psi0={psi0:.6f}'] = dict(M_bracket=Mb, M_potential=Mp, rel=(abs(Mb/Mp - 1) if Mp else None))
        print('psi0 %.4f  bracket %.9e  Ups*L\' %.9e' % (psi0, Mb, Mp), flush=True)
    Mk, _ = bracket_M(base, 'M', np.pi/4); out['kerr_dM_pi4'] = Mk; print('Kerr dM control', Mk)
    json.dump(out, open(os.path.join(HERE, '../results/v23_bracket.json'), 'w'), indent=1)
