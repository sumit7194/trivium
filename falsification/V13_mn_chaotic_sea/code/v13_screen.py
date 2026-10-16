"""V13 screen driver (prereg §4, A1–A6). One level = one (point, E, ell, domain) with 60 orbits on the section.
Per orbit: outcome, returns, max |H + 1/2| up to the reading (the last return), and the two arms
(A1 = log10 |dnu| frequency-map diffusion, A2 = 0-1 test K), read only if the orbit completes N returns inside the
domain with drift <= 1e-9; otherwise ABSTAIN (reported by fate).
Usage: python v13_screen.py kerr_null <chi_key>  |  python v13_screen.py pilot_selftest <chi_key>"""
import sys, os, json, math, time, subprocess
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v13_geometry import Point
from v13_orbit import make
from v13_indicators import fma_diffusion, zero_one_K
R = sp.Rational
RES = os.path.join(HERE, '../results')
N_RET, N_ORB, ACC = 2000, 60, 1e-9
POINTS = {'C0': (1, R(9, 10), R(19, 20)/(R(19, 100))**R(3, 2)), 'F5R': (89, 80, R(13394411, 1186380)),
          'p1': (5, 3, R(1, 5)), 'p2': (13, 5, R(-1, 3))}
SHARED = {'C0': (R(19, 20), R(3)), 'F5R': (R(19, 20), R(3)), 'p1': (R(37, 40), R(29, 10)), 'p2': (R(37, 40), R(3))}   # A8

def E_b(P, ell, lo=0.85, hi=0.9999):
    def state(E):
        cs = [c for c in P.components(E, ell) if not c['nan_edge'] and c['hi'] - c['lo'] > 1e-3]
        if any(not c['touches_inner'] and not c['touches_outer'] for c in cs): return 'bound'
        inner = [c for c in cs if c['touches_inner']]
        return 'merged' if inner and max(c['hi'] for c in inner) > 1.2 else 'none'
    Es = [lo + (hi - lo)*i/60 for i in range(61)]; st = [state(E) for E in Es]
    for i in range(60):
        if st[i] == 'bound' and st[i + 1] == 'merged':
            a, b = Es[i], Es[i + 1]
            while b - a > 1e-12:
                m = 0.5*(a + b)
                if state(m) == 'bound': a = m
                else: b = m
            return 0.5*(a + b)
    return None

def kerr_levels(key):
    M, a_, _ = POINTS[key]; K = Point('kerr_' + key, (M, a_, 0)); Es, ls = SHARED[key]
    grid = [round(2.0 + 0.1*j, 1) for j in range(26)]
    grid.sort(key=lambda l: (abs(l - float(ls)), l))
    lw = Eb = None
    for l in grid:
        e = E_b(K, l)
        if e is not None and e < 0.999: lw, Eb = l, e; break
    levels = [dict(kind='whirl', E=Eb - d, ell=lw, dE=d) for d in (1e-4, 1e-3, 1e-2)]
    levels.append(dict(kind='generic', E=Eb - 0.03, ell=lw))
    if K.bounded(float(Es), float(ls)): levels.append(dict(kind='generic_shared', E=float(Es), ell=float(ls)))
    return K, lw, Eb, levels

def sample(P, E, ell, x_min=1.05):
    comps = [c for c in P.bounded(E, ell, x_min) if not c['nan_edge'] and c['hi'] - c['lo'] > 0.05]
    xs = []
    for c in comps:
        lo, hi = c['lo'], c['hi']; m = 0.15*(hi - lo)
        xs += list(np.linspace(lo + m, hi - m, N_ORB))
    xs = xs[:: max(1, len(xs)//N_ORB)][:N_ORB]
    ss = [0.0, 0.3, -0.3, 0.6, -0.6]
    return [(float(x), ss[i % 5]) for i, x in enumerate(xs)], comps

def run_orbits(M, a_, beta, E, ell, orbits, rtol, domain, acc=ACC):
    integ, start, ham, inD, pieces = make(M, a_, beta, R(E).limit_denominator(10**12) if not isinstance(E, sp.Basic) else E,
                                          sp.nsimplify(ell)*sp.nsimplify(M), domain=domain)
    out = []
    for i, (x0, s) in enumerate(orbits):
        q = pieces(x0, 0.0); rest = -1.0 - q[6]
        pmax = math.sqrt(rest/q[0]) if rest > 0 and q[0] > 0 else 0.0
        px0 = 0.98*s*pmax
        oc, nc, tau, drift, steps, sec = integ(x0, px0, N_RET, rtol, rtol*1e-3, 1e9*float(M), 400_000_000)   # tau cap scales with M (bug fix)
        rec = dict(i=i, x0=x0, px0=px0, outcome=int(oc), returns=int(nc), drift=float(drift), tau=float(tau),
                   sec=[[float(v) for v in row[:3]] for row in sec[:nc]])   # (x, p_x, tau) per crossing, for §7 Jaccard
        if nc >= N_RET and drift <= acc:
            d, n1, n2 = fma_diffusion(sec[:, 0], sec[:, 1]); rec.update(A1=d, A2=zero_one_K(sec[:, 0]), status='READ')
            rec['ret_time_median'] = float(np.median(np.diff(sec[:, 2])))
        else:
            rec['status'] = 'ABSTAIN'
        out.append(rec)
    return out

def pilot(M, a_, beta, E, ell, orbits, domain, acc=ACC):
    pick = orbits[:: max(1, len(orbits)//12)][:12]
    if not pick: raise SystemExit('PILOT REFUSES: empty')
    for rtol in (1e-11, 1e-12, 1e-13):
        r = run_orbits(M, a_, beta, E, ell, pick, rtol, domain, acc)
        ok = [x for x in r if x['returns'] >= N_RET]
        if ok and all(x['drift'] <= acc for x in ok): return rtol, r
    return 1e-13, r   # floor; per-orbit acceptance decides

if __name__ == '__main__':
    mode, key = sys.argv[1], sys.argv[2]
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=HERE).stdout.strip()
    if mode == 'kerr_null':
        M, a_, _ = POINTS[key]; K, lw, Eb, levels = kerr_levels(key)
        res = dict(key=key, chi=str(sp.nsimplify(a_)/M), ell_w=lw, E_b=Eb, commit=commit, levels=[])
        for L in levels:
            orbits, comps = sample(K, L['E'], L['ell'])
            if not orbits: res['levels'].append(dict(**L, note='no bound region inside D')); continue
            t0 = time.time(); rtol, pil = pilot(M, a_, 0, L['E'], L['ell'], orbits, 'B9')
            recs = run_orbits(M, a_, 0, L['E'], L['ell'], orbits, rtol, 'B9')
            res['levels'].append(dict(**L, comps=[(c['lo'], c['hi']) for c in comps], rtol=rtol, orbits=recs,
                                      seconds=round(time.time() - t0, 1)))
            print(key, L['kind'], round(L['E'], 6), L['ell'], 'rtol', rtol, 'read',
                  sum(r['status'] == 'READ' for r in recs), '/', len(recs), round(time.time() - t0, 1), 's', flush=True)
        json.dump(res, open(os.path.join(RES, f'v13_kerr_null_{key}.json'), 'w'), indent=1)

    if mode == 'c0_gate':
        # A3: graded on the base domain at the published accuracy (1e-8); the B9 reading is a FINDING, not a gate.
        thr = json.load(open(os.path.join(RES, 'v13_kerr_null_C0_analysis.json')))['thresholds']
        M, a_, beta = POINTS['C0']; P = Point('C0'); E, ell = 0.95, 3.0
        comps = [c for c in P.bounded(E, ell, 1.0 + 1e-9) if not c['nan_edge'] and c['hi'] - c['lo'] > 0.05]
        res = dict(commit=commit, thresholds=thr, regions=[])
        for c in comps:
            lo, hi = c['lo'], c['hi']; m = 0.15*(hi - lo); ss = [0.0, 0.3, -0.3, 0.6, -0.6]
            orbits = [(float(x), ss[i % 5]) for i, x in enumerate(np.linspace(lo + m, hi - m, N_ORB))]
            rtol, _ = pilot(M, a_, beta, E, ell, orbits, 'base', 1e-8)
            base = run_orbits(M, a_, beta, E, ell, orbits, rtol, 'base', 1e-8)
            b9 = run_orbits(M, a_, beta, E, ell, orbits, max(rtol, 1e-13), 'B9', 1e-9)
            for r in base + b9:
                if r['status'] == 'READ': r['verdict'] = 'CHAOTIC' if (r['A1'] > thr['A1'] and r['A2'] > thr['A2']) else 'NOT_CHAOTIC'
            rd = [r for r in base if r['status'] == 'READ']
            k = P.k; reg = dict(x=(lo, hi), rho=(k*math.sqrt(lo**2 - 1), k*math.sqrt(hi**2 - 1)), rtol=rtol, base=base, b9=b9,
                                n_read=len(rd), n_chaotic=sum(r['verdict'] == 'CHAOTIC' for r in rd),
                                b9_left_D=sum(r['outcome'] == 1 for r in b9),
                                b9_read=sum(r['status'] == 'READ' for r in b9),
                                b9_chaotic=sum(r.get('verdict') == 'CHAOTIC' for r in b9))
            res['regions'].append(reg)
            print('region', [round(v, 3) for v in reg['rho']], 'read', reg['n_read'], 'chaotic', reg['n_chaotic'],
                  '| B9: leftD', reg['b9_left_D'], 'read', reg['b9_read'], 'chaotic', reg['b9_chaotic'], flush=True)
        json.dump(res, open(os.path.join(RES, 'v13_c0_gate.json'), 'w'), indent=1)

    if mode == 'counted':
        # Counted screen at a point's shared level (prereg §3-4, A1-A8): B9 domain, 1e-9 acceptance,
        # thresholds from the same chi's Kerr null; section points stored for the §7 Jaccard comparison.
        thr = json.load(open(os.path.join(RES, f'v13_kerr_null_{key}_analysis.json')))['thresholds']
        M, a_, beta = POINTS[key]; Es, ls = SHARED[key]; P = Point(key)
        # A8: sample ONLY the equatorial components whose 2-D allowed component is bound inside D (bug fix: the first
        # p1 run also sampled a second, ring-adjacent component [1.076, 2.767] that is not inside D).
        from v13_geom2d import bound2d
        allc = [c for c in P.bounded(float(Es), float(ls), 1.05) if not c['nan_edge'] and c['hi'] - c['lo'] > 0.05]
        keep = [c for c in allc if bound2d(M, a_, beta, Es, ls, 0.5*(c['lo'] + c['hi']))['ok']]
        orbits, comps = [], keep
        for c in keep:
            lo, hi = c['lo'], c['hi']; m = 0.15*(hi - lo); ss = [0.0, 0.3, -0.3, 0.6, -0.6]
            orbits += [(float(x), ss[i % 5]) for i, x in enumerate(np.linspace(lo + m, hi - m, N_ORB//len(keep)))]
        rtol, _ = pilot(M, a_, beta, Es, ls, orbits, 'B9')
        recs = run_orbits(M, a_, beta, Es, ls, orbits, rtol, 'B9')
        for r in recs:
            if r['status'] == 'READ': r['verdict'] = 'CHAOTIC' if (r['A1'] > thr['A1'] and r['A2'] > thr['A2']) else 'NOT_CHAOTIC'
        rd = [r for r in recs if r['status'] == 'READ']
        res = dict(key=key, E=str(Es), ell=str(ls), commit=commit, thresholds=thr, rtol=rtol,
                   comps=[(c['lo'], c['hi']) for c in comps], n=len(recs), n_read=len(rd),
                   n_chaotic=sum(r['verdict'] == 'CHAOTIC' for r in rd), orbits=recs)
        json.dump(res, open(os.path.join(RES, f'v13_counted_{key}.json'), 'w'))
        print(key, 'shared', Es, ls, 'rtol', rtol, 'READ', len(rd), '/', len(recs), 'CHAOTIC', res['n_chaotic'], flush=True)
