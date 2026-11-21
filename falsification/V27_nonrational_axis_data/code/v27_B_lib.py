"""V27-B library: monodromy of v'' + (3/16)(P'/P)^2 v = 0 around a circle |z - z0| = R (double precision, DOP853)."""
import numpy as np
from scipy.integrate import solve_ivp

def monodromy(dlogP, R, z0=0.0, rtol=1e-12, atol=1e-14):
    """Return (M, sol0, sol1) for the loop theta in [0, 2pi]; dlogP(z) = P'(z)/P(z)."""
    def rhs(th, Y):
        z = z0 + R*np.exp(1j*th); dz = 1j*R*np.exp(1j*th)
        q = (3/16)*dlogP(z)**2
        v, vz = Y[0] + 1j*Y[1], Y[2] + 1j*Y[3]
        dv, dvz = vz*dz, -q*v*dz
        return [dv.real, dv.imag, dvz.real, dvz.imag]
    sols = []
    for init in ([1, 0, 0, 0], [0, 0, 1, 0]):
        sols.append(solve_ivp(rhs, (0, 2*np.pi), init, method='DOP853', rtol=rtol, atol=atol, dense_output=True))
    M = np.array([[sols[0].y[0, -1] + 1j*sols[0].y[1, -1], sols[1].y[0, -1] + 1j*sols[1].y[1, -1]],
                  [sols[0].y[2, -1] + 1j*sols[0].y[3, -1], sols[1].y[2, -1] + 1j*sols[1].y[3, -1]]])
    return M, sols

def eta_max(dlogP, R, m, z0=0.0, n=2**16):
    th = np.linspace(0, 2*np.pi, n, endpoint=False); z = z0 + R*np.exp(1j*th)
    return np.max(np.abs(dlogP(z)*(z - z0)/m - 1))

def winding(func, R, z0=0.0, n=2**16):
    th = np.linspace(0, 2*np.pi, n + 1); z = z0 + R*np.exp(1j*th)
    ph = np.unwrap(np.angle(func(z, th))); return (ph[-1] - ph[0])/(2*np.pi)

def floquet_product_winding(M, sols, R, z0=0.0, n=2**14):
    """Winding of y = v+ v- (eigen-solutions of M) around the circle; y is single-valued when det M = 1."""
    w, V = np.linalg.eig(M)
    th = np.linspace(0, 2*np.pi, n + 1)
    b0 = sols[0].sol(th); b1 = sols[1].sol(th)
    basis = np.vstack([b0[0] + 1j*b0[1], b1[0] + 1j*b1[1]])   # v-values of the two basis solutions
    vp = V[0, 0]*basis[0] + V[1, 0]*basis[1]; vm = V[0, 1]*basis[0] + V[1, 1]*basis[1]
    ph = np.unwrap(np.angle(vp*vm)); return (ph[-1] - ph[0])/(2*np.pi), w
