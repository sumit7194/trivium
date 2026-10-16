"""V13 chaos indicators on section sequences (x_n, p_n), n = 0..N-1 (prereg §4).
A1, frequency-map diffusion (Laskar NAFF): the dominant frequency nu of z_n = (x_n - <x>) + i (p_n - <p>), on the two
    halves [0, N/2) and [N/2, N); the diffusion index is log10 |nu_1 - nu_2| (in cycles per return). It uses a Hann
    window, an FFT peak, then golden-section refinement of |sum w_n z_n e^{-2 pi i nu n}|.
A2, the 0-1 test for chaos (Gottwald & Melbourne 2009, correlation method) on phi_n = x_n:
    K = median over 100 random c in (pi/5, 4pi/5) of corr(n, D_c(n)), n = 1..N/10.
Self-test (an I-07 synthetic-data check, before any MN use): the Chirikov standard map at K = 0.5 (regular orbit on
an invariant curve), against K = 7 (chaotic sea)."""
import math
import numpy as np

def _amp(z, w, nu):
    n = np.arange(len(z)); return abs(np.sum(w*z*np.exp(-2j*math.pi*nu*n)))

def naff_freq(z):
    N = len(z); w = 0.5*(1 - np.cos(2*math.pi*np.arange(N)/N))
    F = np.abs(np.fft.fft(w*z)); k = int(np.argmax(F[1:])) + 1
    lo, hi = (k - 1)/N, (k + 1)/N
    g = (math.sqrt(5) - 1)/2; a, b = lo, hi
    c, d = b - g*(b - a), a + g*(b - a); fc, fd = _amp(z, w, c), _amp(z, w, d)
    for _ in range(80):
        if fc > fd: b, d, fd = d, c, fc; c = b - g*(b - a); fc = _amp(z, w, c)
        else: a, c, fc = c, d, fd; d = a + g*(b - a); fd = _amp(z, w, d)
    nu = 0.5*(a + b)
    return nu if nu <= 0.5 else nu - 1.0

def fma_diffusion(xs, ps, z=None):
    """Default signal: the centred section point (x - <x>) + i (p - <p>), for closed curves around their centroid.
    A caller may pass its own complex signal z (e.g. e^{i x} for rotational curves of the standard-map self-test)."""
    if z is None: z = (xs - xs.mean()) + 1j*(ps - ps.mean())
    N = len(z); h = N//2
    n1, n2 = naff_freq(z[:h]), naff_freq(z[h:2*h])
    return math.log10(max(abs(n1 - n2), 1e-16)), n1, n2

def zero_one_K(phi, nc=100, seed=7):
    phi = np.asarray(phi, float); N = len(phi); ncut = N//10; rng = np.random.default_rng(seed)
    js = np.arange(1, N + 1); Ks = []
    for c in rng.uniform(math.pi/5, 4*math.pi/5, nc):
        p = np.cumsum(phi*np.cos(js*c)); q = np.cumsum(phi*np.sin(js*c))
        ns = np.arange(1, ncut + 1)
        M = np.array([np.mean((p[n:] - p[:-n])**2 + (q[n:] - q[:-n])**2) for n in ns])
        Vosc = (phi.mean())**2*(1 - np.cos(ns*c))/(1 - math.cos(c))
        Dc = M - Vosc
        Ks.append(np.corrcoef(ns, Dc)[0, 1])
    return float(np.median(Ks))

def standard_map(Kp, x0, p0, N):
    xs = np.empty(N); ps = np.empty(N); x, p = x0, p0
    for i in range(N):
        p = (p + Kp*math.sin(x)) % (2*math.pi); x = (x + p) % (2*math.pi); xs[i] = x; ps[i] = p
    return xs, ps

if __name__ == '__main__':
    import json, os
    out = {}
    for name, Kp, x0, p0 in [('regular_K0.5', 0.5, 3.0, 1.0), ('regular_K0.5_b', 0.5, 1.0, 2.5),
                             ('chaotic_K7', 7.0, 3.0, 1.0), ('chaotic_K7_b', 7.0, 0.5, 4.0)]:
        xs, ps = standard_map(Kp, x0, p0, 2000)
        # the standard map's natural angle signal is e^{i x} (x is an angle; the section curves are rotational)
        d, n1, n2 = fma_diffusion(None, None, z=np.exp(1j*xs))
        K = zero_one_K(np.cos(xs))
        out[name] = dict(log10_dnu=d, K01=K); print(name, round(d, 2), round(K, 3))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/v13_indicator_selftest.json'), 'w'), indent=1)
