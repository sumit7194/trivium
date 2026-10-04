"""V8-mono: the bridge's reproduction of quantum's TS delta=2 v2 monodromy (PREREG_TS_V2_MONODROMY.md). Own equations
(V8 provenance builder on ansatz's metric components), t-chart x = (t+1/t)/2, integrator from V9-eq'. Loop specs are
transcribed from quantum's message; no quantum file is read."""
import sys, json, numpy as np, sympy as sp
sys.path.insert(0, '../../V9_mn_obstruction_check/code')
from v9_equatorial_monodromy import monodromy, loop_pts, abel_det, inv, comm
ns = {}; exec(open('v8_nve.py').read().split("def zv():")[0], ns)
x, y, load = ns['x'], ns['y'], ns['load']
t = sp.Symbol('t')
FILES = {'P1': 'ts2_metric_components_t1o2.txt', 'P2': 'ts2_metric_components_t1o3.txt'}

def coeffs(tag, E, L, mu2):
    g = load(FILES[tag])
    gtt, gtp, gpp, gxx_dn, gyy_dn = g['g_TT'], g['g_Tphi'], g['g_phiphi'], g['g_xx'], g['g_yy']
    det = gtt*gpp - gtp**2
    Gtt, Gtp, Gpp, Gxx, Gyy = gpp/det, -gtp/det, gtt/det, 1/gxx_dn, 1/gyy_dn
    d2 = lambda e: sp.diff(e, y, 2).subs(y, 0)
    E, L, mu2 = map(sp.Integer, (E, L, mu2))
    V0 = (Gtt*E**2 - 2*Gtp*E*L + Gpp*L**2).subs(y, 0); V2 = d2(Gtt)*E**2 - 2*d2(Gtp)*E*L + d2(Gpp)*L**2
    Gxx0 = Gxx.subs(y, 0); px2 = (-mu2 - V0)/Gxx0
    A = Gyy.subs(y, 0); X = Gxx0*(-mu2 - V0); B = sp.Rational(1, 2)*(d2(Gxx)*px2 + V2)
    pc = -(sp.diff(A, x)/A - sp.diff(X, x)/(2*X)); qc = A*B/X
    # Compose numerically (no symbolic cancel: it blew up memory on the first attempt, killed at ~8 GB).
    pxf = sp.lambdify(x, pc, 'numpy', cse=True); qxf = sp.lambdify(x, qc, 'numpy', cse=True)
    x1f = lambda z: (1 - 1/z**2)/2; x2f = lambda z: 1/z**3
    pt = lambda z: x1f(z)*pxf((z + 1/z)/2) - x2f(z)/x1f(z)
    qt = lambda z: x1f(z)**2*qxf((z + 1/z)/2)
    return pc, qc, pt, qt

ROWS = {
 0: ('P1', (1, 0, 4), 2.838135716376561 - 2.7537235491540395j,
     dict(a=(0.482412944837899 - 1.7624496982235884j, 0.2706744562203041), b=(1.6774660622300568, 0.20323981866901702), c=(-1j, 0.14812973226326212)),
     ('a', 'b'), ('a', 'c'), (3.4879659893877317 - 77.342864830834457j, -0.95044102933945884 + 1.3762707973151855j, 1.5828596194084399 - 75.617797717067583j)),
 1: ('P1', (1, 0, 9), 2.776723447334296 + 2.8804459721510023j,
     dict(a=(0.39602470481590324 + 1.6044467846319757j, 0.21678845311704484), b=(1.6774660622300568, 0.20323981866901702), c=(1j, 0.13118027406765523)),
     ('a', 'b'), ('a', 'c'), (-8.3162927914153368 + 26.687603197824362j, -0.66989312461885025 - 21.275453190658606j, -2.3362886125588271 + 6.5727523980736595j)),
 2: ('P1', (1, 1, 4), 2.838135716376561 - 2.7537235491540395j,
     dict(a=(0.5660894874145761 - 1.7624145390932489j, 0.2848789064609491), b=(1.6774660622300568, 0.20323981866901702), c=(-1j, 0.15389729145017533)),
     ('a', 'b'), ('a', 'c'), (36.018161855848577 - 51.562102088278822j, -0.63528391097699423 + 0.65697831082101477j, 33.578391634390881 - 50.744938715928927j)),
 3: ('P2', (1, 0, 4), 2.632281148776495 - 2.553991532383206j,
     dict(a=(0.22956326400200533 - 1.462175080013619j, 0.15481427165748143), b=(1.401118545620634, 0.12033556368619022), c=(-1j, 0.10459814314679294)),
     ('a', 'b'), ('a', 'c'), (-50.707942315934390 + 109.09748003097748j, -2.3625160542176303 + 7.4746528008320791j, -49.075933489700412 + 101.82768659276655j)),
 4: ('P2', (1, 0, 9), 2.5753232107995436 + 2.6715225733610675j,
     dict(a=(0.14642914961616427 + 1.0702894436866155j, 0.04636690361399948), b=(1.401118545620634, 0.12033556368619022), c=(0.1254790442704036 + 0.9171595740229119j, 0.045107398566500576)),
     ('a', 'b'), ('b', 'c'), (6.0912024311356193 + 6.9203847477148020j, 6.0912024311356193 - 6.9203847477148020j, -0.98173973435702931 + 0j)),
 5: ('P2', (1, 1, 4), 2.5753232107995436 + 2.6715225733610675j,
     dict(a=(0.3729678737067366 + 1.5188376061265878j, 0.1916944826315153), b=(1.401118545620634, 0.12033556368619022), c=(1j, 0.12256989375629589)),
     ('a', 'b'), ('a', 'c'), (-93.520510069692272 + 21.310319434306618j, -2.2443215278010807 - 2.3184031010151625j, -92.115500570103438 + 20.638261599509653j)),
}

if __name__ == '__main__':
    prov = json.load(open('../results/v8_ts_provenance.json'))
    out = {}
    for i in [int(a) for a in sys.argv[1:]] or range(6):
        tag, (E, L, mu2), base, loops, gw, hw, tg = ROWS[i]
        pc, qc, pt, qt = coeffs(tag, E, L, mu2)
        pv = prov[f'{tag}|E={E},L={L},mu2={mu2}']['5/4']
        e1 = max(abs(sp.N(pc.subs(x, sp.Rational(5, 4)), 40)/sp.Float(pv['p'], 50) - 1),
                 abs(sp.N(qc.subs(x, sp.Rational(5, 4)), 40)/sp.Float(pv['q'], 50) - 1))
        pf, qf = pt, qt
        target = dict(inv_g=tg[0], inv_h=tg[1], comm=tg[2]); res = {}
        for tol in (1e-11, 1e-13):
            Ms = {k: monodromy(pf, qf, loop_pts(base, c, r), tol) for k, (c, r) in loops.items()}
            g, h = Ms[gw[0]] @ Ms[gw[1]], Ms[hw[0]] @ Ms[hw[1]]
            res[tol] = dict(inv_g=inv(g), inv_h=inv(h), comm=comm(g, h),
                            abel=max(abs(np.linalg.det(Ms[k])/abel_det(pf, loop_pts(base, c, r)) - 1) for k, (c, r) in loops.items()))
        lo, hi = res[1e-11], res[1e-13]
        conv = max(abs(hi[k]/lo[k] - 1) for k in target); agree = max(abs(hi[k]/target[k] - 1) for k in target)
        gates = e1 < 1e-12 and max(lo['abel'], hi['abel']) < 1e-8 and conv < 1e-7
        verdict = ('REPRODUCED' if agree < 1e-7 else 'DISAGREES' if agree > 1e-5 else 'INCONCLUSIVE') if gates else 'INCONCLUSIVE'
        print(f'row {i} {tag} {(E, L, mu2)}: prov {float(e1):.1e}  Abel {max(lo["abel"], hi["abel"]):.1e}  conv {conv:.1e}  '
              f'agree {agree:.1e}  tr[g,h]={hi["comm"]:.10g}  -> {verdict}', flush=True)
        out[i] = dict(prov=float(e1), conv=conv, agree=agree, verdict=verdict, values={k: str(v) for k, v in hi.items()})
    json.dump(out, open('../results/v8_ts_monodromy.json', 'w'), indent=1)
