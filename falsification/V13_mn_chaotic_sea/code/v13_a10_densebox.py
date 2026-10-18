"""V13 A10 LABELLED POST-HOC check (prompted by tabula; no registered verdict changes): a STRICT box version of the B9
g_phiphi test along the A10 connecting orbits and the in-D hyperbolic UPOs.
v13_orbit.in_D tests g_phiphi > 0 at 9 samples of the box (x, y) +/- 0.025 (exactly as A1 specifies). Here:
  1. Every CONFIRMED_MS edge (plus, labelled, the A9-confirmed edges) is re-integrated from its stored A10 multiple-
     shooting solution (results/v13_a10_<pt>.json: s, s' and the segment points): each segment start w_{k-1} (u_{k-1})
     over pow returns, base domain (no stopping), with the same DOP853 steps as v13_orbit (the section end point is
     checked bitwise against SectionMap's base map). Every UPO (A9 list, in-D hyperbolic) over one period likewise.
     Samples: every accepted step end, plus dense-output points so consecutive samples are <= 0.005 apart in x and y
     (the max gap is reported). W^s-side samples are mirrored y -> -y (that orbit is the time-reverse of G of it).
  2. STRICT box test at every sample: min g_phiphi over a 21 x 21 grid on [x +/- 0.025] x [y +/- 0.025] (numba),
     non-finite values flagged (=> fail); then scipy L-BFGS-B (bounded to the box) from the worst grid point, for the
     NREF samples of each orbit with the lowest grid minimum (the largest grid-vs-refined improvement is reported).
     The other B9 conditions (x - 1 >= 0.05, R >= 0.5, |y| + 0.025 < 1) are applied exactly at every sample.
  3. Per edge / UPO: strict_in_D, min over the orbit of the box-min g_phiphi, the worst sample (x, y, distance to the
     ring point (x_s, 0)), and the y at which min x occurs.
  4. Summary: survivors; SCCs and self-loops of the confirmed graph under the strict test (edges only, and edges with
     both end UPOs strictly in D).
Controls: (3.6, 0) must pass; (x_s + 0.015, 0) must FAIL. x_s (ring, from the bridge): C0 1.92983, F5-R 1.92192;
g_phiphi along y = 0 near x_s is reported as a sanity check.
Usage: python v13_a10_densebox.py   (one process; writes results/v13_a10_densebox.json)"""
import sys, os, json, math, time
import numpy as np, sympy as sp, numba
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v13_a10_multishoot as M
from v13_field import build, gpp_reg, x as X, y as Y
from v13_a9_confirm import tarjan
import scipy.integrate._ivp.dop853_coefficients as DC

XS = {'C0': 1.92983, 'F5R': 1.92192}
BOX, NG, DS, NREF = 0.025, 21, 0.005, 300
NS = DC.N_STAGES
A_ = np.ascontiguousarray(DC.A[:NS, :NS]); B_ = DC.B.copy(); E3 = DC.E3.copy(); E5 = DC.E5.copy(); D_ = DC.D.copy()
AX = np.ascontiguousarray(DC.A[NS + 1:])

def make_dense(pieces):
    """Copy of the v13_orbit DOP853 integrator (base domain, never stops on D), returning sampled (x, y) along the
    whole orbit up to the n-th section crossing, and the section point."""
    @numba.njit
    def rhs(z, out):
        q = pieces(z[0], z[1]); px, py = z[2], z[3]
        out[0] = q[0]*px; out[1] = q[3]*py
        out[2] = -0.5*(q[1]*px*px + q[4]*py*py + q[7]); out[3] = -0.5*(q[2]*px*px + q[5]*py*py + q[8])

    @numba.njit
    def dense_eval(F, y_old, s, out):
        for k in range(4): out[k] = 0.0
        for i in range(7):
            f = F[6 - i]
            for k in range(4): out[k] += f[k]
            fac = s if i % 2 == 0 else 1.0 - s
            for k in range(4): out[k] *= fac
        for k in range(4): out[k] += y_old[k]

    @numba.njit
    def root(F, y_old, s_lo, s_hi):
        tmp = np.empty(4)
        dense_eval(F, y_old, s_lo, tmp); flo = tmp[1]
        for _ in range(60):
            sm = 0.5*(s_lo + s_hi); dense_eval(F, y_old, sm, tmp); fm = tmp[1]
            if (fm < 0) == (flo < 0): s_lo = sm; flo = fm
            else: s_hi = sm
        return 0.5*(s_lo + s_hi)

    @numba.njit
    def run(x0, px0, N, rtol, atol):
        q = pieces(x0, 0.0); rest = -1.0 - q[6] - q[0]*px0*px0
        smp = np.zeros((1, 2)); sec = np.zeros(2)
        if not (rest > 0.0) or not (q[3] > 0.0): return False, smp, sec
        cap = 65536; smp = np.empty((cap, 2)); ns = 0
        y = np.array([x0, 0.0, px0, math.sqrt(rest/q[3])]); f = np.empty(4); rhs(y, f)
        smp[0, 0] = y[0]; smp[0, 1] = y[1]; ns = 1
        K = np.zeros((16, 4)); ynew = np.empty(4); fnew = np.empty(4); tmp = np.empty(4); F = np.zeros((7, 4))
        sc = atol + np.abs(y)*rtol
        d0 = math.sqrt(np.mean((y/sc)**2)); d1 = math.sqrt(np.mean((f/sc)**2))
        h0 = 1e-6 if (d0 < 1e-5 or d1 < 1e-5) else 0.01*d0/d1
        y1 = y + h0*f; f1 = np.empty(4); rhs(y1, f1)
        d2 = math.sqrt(np.mean(((f1 - f)/sc)**2))/h0
        h1 = max(1e-6, h0*1e-3) if (d1 <= 1e-15 and d2 <= 1e-15) else (0.01/max(d1, d2))**(1.0/8.0)
        h = min(100*h0, h1); t = 0.0; ncross = 0; steps = 0; tau_max = 1e12
        while steps < 50_000_000:
            rejected = False
            while True:
                hh = min(h, tau_max - t)
                K[0] = f
                for s in range(1, NS):
                    for k in range(4):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*A_[s, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(4):
                    acc = 0.0
                    for j in range(NS): acc += K[j, k]*B_[j]
                    ynew[k] = y[k] + hh*acc
                rhs(ynew, fnew); K[NS] = fnew
                e5 = 0.0; e3 = 0.0
                for k in range(4):
                    sck = atol + max(abs(y[k]), abs(ynew[k]))*rtol
                    a5 = 0.0; a3 = 0.0
                    for j in range(NS + 1): a5 += K[j, k]*E5[j]; a3 += K[j, k]*E3[j]
                    e5 += (a5/sck)**2; e3 += (a3/sck)**2
                en = 0.0 if (e5 == 0.0 and e3 == 0.0) else hh*e5/math.sqrt((e5 + 0.01*e3)*4)
                if not math.isfinite(en): en = 1e300
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return False, smp[:ns], sec
            steps += 1
            # dense-output coefficients for this step (extra stages do not change the step sequence)
            for s in range(NS + 1, 16):
                for k in range(4):
                    acc = 0.0
                    for j in range(s): acc += K[j, k]*AX[s - NS - 1, j]
                    tmp[k] = y[k] + acc*hh
                rhs(tmp, K[s])
            for k in range(4):
                dy = ynew[k] - y[k]
                F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                for r in range(4):
                    acc = 0.0
                    for j in range(16): acc += D_[r, j]*K[j, k]
                    F[3 + r, k] = hh*acc
            crossing = (y[1] < 0.0 and ynew[1] >= 0.0)
            s_end = 1.0
            if crossing and ncross + 1 >= N: s_end = root(F, y, 0.0, 1.0)
            span = max(abs(ynew[0] - y[0]), abs(ynew[1] - y[1]))
            nsub = int(math.ceil(4.0*span/DS)) + 1          # generous oversampling of the in-step path
            for i in range(1, nsub + 1):
                if ns + 1 >= smp.shape[0]:
                    s2 = np.empty((2*smp.shape[0], 2)); s2[:ns] = smp[:ns]; smp = s2
                dense_eval(F, y, s_end*i/nsub, tmp); smp[ns, 0] = tmp[0]; smp[ns, 1] = tmp[1]; ns += 1
            if crossing:
                ncross += 1
                if ncross >= N:
                    dense_eval(F, y, s_end, tmp); sec[0] = tmp[0]; sec[1] = tmp[2]
                    return True, smp[:ns], sec
            t += hh
            for k in range(4): y[k] = ynew[k]; f[k] = fnew[k]
        return False, smp[:ns], sec
    return run

def make_box(gpp):
    @numba.njit
    def boxmin(smp):
        """Per sample: grid min of g_phiphi over the 21 x 21 box, its location, a non-finite flag, and the exact
        non-g_phiphi B9 conditions."""
        n = smp.shape[0]; gm = np.empty(n); lx = np.empty(n); ly = np.empty(n); bad = np.zeros(n, np.bool_)
        other = np.ones(n, np.bool_)
        for i in range(n):
            xv, yv = smp[i, 0], smp[i, 1]
            if not (xv - 1.0 >= 0.05) or xv*xv + yv*yv - 1.0 < 0.25 or abs(yv) + BOX >= 1.0: other[i] = False
            best = 1e300; bx = xv; by = yv
            for a in range(NG):
                for b in range(NG):
                    xx = xv - BOX + 2*BOX*a/(NG - 1); yy = yv - BOX + 2*BOX*b/(NG - 1)
                    if yy >= 1.0 or yy <= -1.0: bad[i] = True; continue
                    g = gpp(xx, yy)
                    if not math.isfinite(g): bad[i] = True; continue
                    if g < best: best = g; bx = xx; by = yy
            gm[i] = best; lx[i] = bx; ly[i] = by
        return gm, lx, ly, bad, other
    return boxmin

def make_cloud(gpp):
    @numba.njit
    def cloud(x0, x1, y0, y1, h):
        """BOUNDARY points of the CTC set on the grid (CTC cells with a non-CTC 4-neighbour, or on the grid edge):
        for a point outside the set, the distance to the set equals the distance to its boundary."""
        nx = int((x1 - x0)/h) + 1; ny = int((y1 - y0)/h) + 1
        m = np.zeros((nx, ny), np.bool_)
        for i in range(nx):
            for j in range(ny):
                g = gpp(x0 + i*h, y0 + j*h); m[i, j] = (not (g > 0.0)) or (not math.isfinite(g))
        out = np.empty((65536, 2)); n = 0; tot = 0
        for i in range(nx):
            for j in range(ny):
                if not m[i, j]: continue
                tot += 1
                edge = (i == 0 or j == 0 or i == nx - 1 or j == ny - 1)
                if edge or not (m[i - 1, j] and m[i + 1, j] and m[i, j - 1] and m[i, j + 1]):
                    if n >= out.shape[0]:
                        o2 = np.empty((2*out.shape[0], 2)); o2[:n] = out[:n]; out = o2
                    out[n, 0] = x0 + i*h; out[n, 1] = y0 + j*h; n += 1
        return out[:n], tot
    return cloud

HC = 5e-4
def ctc_setup(log):
    """Supplementary margin: the CTC set {g_phiphi <= 0 or non-finite} sampled on a 5e-4 grid over x in (1, 3],
    |y| < 0.9995; the strict box test passes iff the L-infinity distance from a sample to this set exceeds 0.025
    (grid accuracy ~ 2.5e-4)."""
    from scipy.spatial import cKDTree
    pts, tot = make_cloud(W['gpp'])(1.0 + 1e-6, 3.0, -0.9995, 0.9995, HC)
    W['tree'] = cKDTree(pts) if len(pts) else None
    info = dict(n_ctc_cells=int(tot), n_boundary_points=int(len(pts)), grid=HC, x_range=[float(pts[:, 0].min()), float(pts[:, 0].max())] if len(pts) else None,
                y_range=[float(pts[:, 1].min()), float(pts[:, 1].max())] if len(pts) else None)
    log(W['pt'], 'CTC cloud', info); return info

def ctc_dist(smp):
    if W.get('tree') is None: return None
    d, i = W['tree'].query(smp, k=1, p=np.inf); k = int(np.argmin(d)); q = W['tree'].data[i[k]]
    return dict(min_Linf_dist_to_CTC=float(d[k]), at_sample=dict(x=float(smp[k, 0]), y=float(smp[k, 1])),
                nearest_CTC_point=dict(x=float(q[0]), y=float(q[1])), margin_vs_box=float(d[k] - BOX))

W = {}
def setup(pt, sc):
    A9 = json.load(open(os.path.join(M.RES, M.A9F[pt])))
    M.init_worker(pt, *M.level(A9), sc)
    Mm, a_, beta = M.POINTS[pt]; S = build(Mm, a_, beta)
    W['gpp'] = numba.njit(sp.lambdify([X, Y], gpp_reg(S), 'math', cse=True))
    W['run'] = make_dense(M.W['S'].base[4]); W['box'] = make_box(W['gpp']); W['pt'] = pt

def strict_samples(smp, xs, gap=None):
    gm, lx, ly, bad, other = W['box'](smp)
    order = np.argsort(gm)[:NREF]; ref = gm.copy(); impr = 0.0; nref = 0
    g = W['gpp']
    for i in order:
        if bad[i] or not math.isfinite(gm[i]): continue
        xv, yv = smp[i]
        bnds = [(xv - BOX, xv + BOX), (max(yv - BOX, -1 + 1e-15), min(yv + BOX, 1 - 1e-15))]
        r = minimize(lambda p: g(p[0], p[1]), np.array([lx[i], ly[i]]), method='L-BFGS-B', bounds=bnds)
        nref += 1
        if math.isfinite(r.fun) and r.fun < ref[i]: impr = max(impr, gm[i] - r.fun); ref[i] = r.fun
        elif not math.isfinite(r.fun): bad[i] = True
    ok = (~bad) & other & (ref > 0)
    iw = int(np.argmin(np.where(bad, -np.inf, ref)))
    ix = int(np.argmin(smp[:, 0]))
    cd = ctc_dist(smp) if 'tree' in W else None
    if gap is None:
        gap = float(np.max(np.abs(np.diff(smp, axis=0)))) if len(smp) > 1 else 0.0
    return dict(strict_in_D=bool(ok.all()), n_samples=int(len(smp)), max_sample_gap=float(gap),
                n_fail_samples=int((~ok).sum()), n_nonfinite=int(bad.sum()), n_other_B9_fail=int((~other).sum()),
                min_boxmin_gpp=float(ref[iw]), min_boxmin_gpp_grid_only=float(gm.min()),
                worst=dict(x=float(smp[iw, 0]), y=float(smp[iw, 1]), dist_to_ring=float(math.hypot(smp[iw, 0] - xs, smp[iw, 1]))),
                min_x=dict(x=float(smp[ix, 0]), y=float(smp[ix, 1]), dist_to_ring=float(math.hypot(smp[ix, 0] - xs, smp[ix, 1]))),
                min_R=float(np.sqrt(np.maximum(smp[:, 0]**2 + smp[:, 1]**2 - 1, 0)).min()),
                n_refined=nref, max_refine_improvement=float(impr), ctc_distance=cd,
                lowest_unrefined_grid_min=float(np.sort(gm)[NREF]) if len(gm) > NREF else None)

def orbit_samples(starts, n, mirror_flags):
    parts, secok, gap = [], True, 0.0
    for w, mir in zip(starts, mirror_flags):
        ok, smp, sec = W['run'](float(w[0]), float(w[1]), n, M.RT, M.RT*1e-3)
        Pb = M.W['sy'].P(w, n, M.RT)
        secok = secok and ok and Pb is not None and bool(np.array_equal(sec, Pb))
        smp = smp.copy()
        if mir: smp[:, 1] *= -1
        if len(smp) > 1: gap = max(gap, float(np.max(np.abs(np.diff(smp, axis=0)))))
        parts.append(smp)
    return np.concatenate(parts), secok, gap

def controls(pt, xs):
    g = W['gpp']; out = {}
    for nm, p in (('inside_3.6_0', (3.6, 0.0)), ('ring_plus_0.015', (xs + 0.015, 0.0))):
        r = strict_samples(np.array([p]), xs); out[nm] = dict(point=p, strict_in_D=r['strict_in_D'], boxmin=r['min_boxmin_gpp'],
                                                              nonfinite=r['n_nonfinite'], worst=r['worst'],
                                                              b9_9sample_in_D=bool(M.W['S'].b9[3](p[0], p[1])))
    xx = np.linspace(xs - 0.02, xs + 0.02, 9)
    out['gpp_on_axis_near_ring'] = [(float(v), float(g(v, 0.0))) for v in xx]
    out['expected'] = 'inside passes, ring+0.015 fails'
    out['pass'] = bool(out['inside_3.6_0']['strict_in_D'] and not out['ring_plus_0.015']['strict_in_D'])
    return out

def run_point(pt, log):
    R = json.load(open(os.path.join(M.RES, f'v13_a10_{pt}.json'))); sc = [R['scaling']['xscale'], R['scaling']['pscale']]
    setup(pt, sc); xs = XS[pt]; out = dict(x_s=xs); out['ctc_cloud'] = ctc_setup(log)
    out['controls'] = controls(pt, xs); log(pt, 'controls', out['controls']['pass'], {k: (v['strict_in_D'], v['boxmin']) for k, v in out['controls'].items() if isinstance(v, dict)})
    A9 = json.load(open(os.path.join(M.RES, M.A9F[pt])))
    out['upos'] = []
    for u in A9['upos']:
        pw = u['period']
        smp, secok, gap = orbit_samples([np.array(u['z'])], pw, [False])
        r = strict_samples(smp, xs, gap); r.update(idx=u['idx'], period=pw, section_end_matches_base=secok)
        out['upos'].append(r); log(pt, 'UPO', u['idx'], 'strict', r['strict_in_D'], 'boxmin %.4g' % r['min_boxmin_gpp'], 'worst', r['worst'], 'gap %.4f' % r['max_sample_gap'], 'Linf-to-CTC %.4f' % r['ctc_distance']['min_Linf_dist_to_CTC'])
    out['edges'] = []
    for e in R['edges']:
        if not (e['CONFIRMED_MS'] or e['A9_CONFIRMED']): continue
        j = next(j for j in M.edge_jobs(pt, {(e['src'], e['dst'])})[3])
        Ed = M.Edge(j['zi'], j['vi'], j['pi'], j['a'], j['zg'], j['vg'], j['pg'], j['b'])
        s, w, sp_, u = Ed.unpack(np.array(e['ms_13']['X']))
        # a = 0 (b = 0): that side is the single section point w_0 (u_0), sampled at (x, y = 0)
        su, oku, gu = orbit_samples(w[:Ed.a], Ed.pi, [False]*Ed.a) if Ed.a else (np.array([[w[0][0], 0.0]]), True, 0.0)
        ss, oks, gs = orbit_samples(u[:Ed.b], Ed.pg, [True]*Ed.b) if Ed.b else (np.array([[u[0][0], 0.0]]), True, 0.0)
        r = strict_samples(np.concatenate([su, ss]), xs, max(gu, gs))
        r.update(src=e['src'], dst=e['dst'], a=Ed.a, b=Ed.b, CONFIRMED_MS=e['CONFIRMED_MS'], A9_CONFIRMED=e['A9_CONFIRMED'],
                 section_ends_match_base=bool(oku and oks), registered_9sample_min_gpp_box=e['margins']['min_gpp_box'])
        out['edges'].append(r)
        log(pt, 'edge', e['src'], '->', e['dst'], 'strict', r['strict_in_D'], 'boxmin %.4g' % r['min_boxmin_gpp'], '(9-sample %.4g)' % e['margins']['min_gpp_box'],
            'worst', r['worst'], 'min_x', r['min_x'], 'gap %.4f' % r['max_sample_gap'], 'impr %.1e' % r['max_refine_improvement'], 'Linf-to-CTC %.4f' % r['ctc_distance']['min_Linf_dist_to_CTC'])
    nodes = sorted(u['idx'] for u in A9['upos']); ustrict = {u['idx']: u['strict_in_D'] for u in out['upos']}
    conf = [r for r in out['edges'] if r['CONFIRMED_MS']]
    def graph(E):
        adj = {}
        for r in E: adj.setdefault(r['src'], []).append(r['dst'])
        sccs = [c for c in tarjan(nodes, adj) if len(c) > 1 or any(r['src'] == r['dst'] == c[0] for r in E)]
        return dict(edges=[f"{r['src']}->{r['dst']}" for r in E], self_loops=sorted(r['src'] for r in E if r['src'] == r['dst']), sccs=sccs)
    se = [r for r in conf if r['strict_in_D']]; sn = [r for r in se if ustrict[r['src']] and ustrict[r['dst']]]
    out['summary'] = dict(n_confirmed=len(conf), n_strict_survivors=len(se), failing_edges=[f"{r['src']}->{r['dst']}" for r in conf if not r['strict_in_D']],
                          upos_strict={str(k): v for k, v in ustrict.items()}, registered_graph=graph(conf), strict_edges_only=graph(se),
                          strict_edges_and_nodes=graph(sn),
                          min_boxmin_over_confirmed=min((r['min_boxmin_gpp'] for r in conf), default=None),
                          min_boxmin_over_strict_survivors=min((r['min_boxmin_gpp'] for r in se), default=None),
                          min_ctc_Linf_dist_confirmed=min((r['ctc_distance']['min_Linf_dist_to_CTC'] for r in conf), default=None),
                          min_ctc_Linf_dist_upos=min(r['ctc_distance']['min_Linf_dist_to_CTC'] for r in out['upos']),
                          ctc_dist_agrees_with_box_test=all((r['ctc_distance']['min_Linf_dist_to_CTC'] > BOX) == r['strict_in_D'] for r in out['edges'] + out['upos']),
                          max_sample_gap=max(r['max_sample_gap'] for r in out['edges'] + out['upos']),
                          max_refine_improvement=max(r['max_refine_improvement'] for r in out['edges'] + out['upos']),
                          all_section_ends_match_base=all(r.get('section_ends_match_base', r.get('section_end_matches_base')) for r in out['edges'] + out['upos']))
    return out

if __name__ == '__main__':
    T0 = time.time(); env, commit = M.env_commit()
    log = lambda *a: print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)
    res = dict(label='LABELLED POST-HOC check (tabula prompt); no registered verdict changes', commit=commit, env=env,
               params=dict(box=BOX, grid=NG, max_sample_spacing=DS, n_refined_per_orbit=NREF, refine='scipy L-BFGS-B, bounded to the box'))
    for pt in ('C0', 'F5R'):
        res[pt] = run_point(pt, log); M.rss_guard(log)
    res['runtime_s'] = time.time() - T0; res['peak_rss_mb'] = M.rss_mb()
    json.dump(res, open(os.path.join(M.RES, 'v13_a10_densebox.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    log('wrote results/v13_a10_densebox.json; peak RSS %.0f MB' % res['peak_rss_mb'])
