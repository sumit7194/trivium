"""V13 A10 supplementary diagnostics (NOT registered checks), run after v13_a10_multishoot.py, for the edges whose W^u
side starts at the strongest UPO (C0 UPO 8, F5-R UPO 9; lambda ~ -180/-200, one P^4 segment stretches by ~4e4):
 (a) one-extra-segment reparametrisation initialised FROM the registered solution (w'_1 = registered w_0 = z + s v,
     w'_{k+1} = registered w_k, s~ = s/Lambda; same on the W^s side). Tests whether the registered crossing is a
     W^u/W^s crossing of the true (curved) local manifold, independent of the initial-guess sensitivity of the
     diagnostic in v13_a10_multishoot.py (which propagates from s/Lambda and can slide along a folded W^u);
 (b) the exact variational Jacobian of the first W^u segment against central differences at h = 1e-7 .. 1e-9 scaled
     (v13_a10_multishoot used 1e-6, which is in the nonlinear range at this stretch).
Writes results/v13_a10_diag.json (small). Usage: python v13_a10_diag.py"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v13_a10_multishoot as M

def run(pt, srcs):
    A9, sc, scope, jobs = M.edge_jobs(pt)
    R = json.load(open(os.path.join(M.RES, f'v13_a10_{pt}.json')))
    reg = {(r['src'], r['dst']): r for r in R['edges']}
    M.init_worker(pt, *M.level(A9), sc); sy = M.W['sy']; out = []
    for j in jobs:
        if j['src'] not in srcs: continue
        r = reg[(j['src'], j['dst'])]; n13 = r['ms_13']
        E = M.Edge(j['zi'], j['vi'], j['pi'], j['a'], j['zg'], j['vg'], j['pg'], j['b']); E.lam_i, E.lam_g = j['lam_i'], j['lam_g']
        s, w, sp_, u = E.unpack(np.array(n13['X']))
        Li = E.lam_i if E.lam_i > 0 else E.lam_i**2; Lg = E.lam_g if E.lam_g > 0 else E.lam_g**2
        E2 = M.Edge(E.zi, E.vi, E.pi, E.a + 1, E.zg, E.vg, E.pg, E.b + 1)
        X = np.zeros(E2.n); X[E2.iS] = s/Li; X[E2.iSp] = sp_/Lg
        for k in range(1, E2.a + 1): X[E2.col_w(k):E2.col_w(k) + 2] = w[k - 1]
        for k in range(1, E2.b + 1): X[E2.col_u(k):E2.col_u(k) + 2] = u[k - 1]
        R0, seg0 = M.ms_residual(sy, E2, X, M.RT)
        sol = M.ms_solve(sy, E2, X, M.RT)
        rec = dict(point=pt, edge=f"{j['src']}->{j['dst']}", a=E.a, b=E.b, s=float(s), CONFIRMED_MS=r['CONFIRMED_MS'],
                   init_max_seg_res=max(seg0), init_first_seg_res=seg0[0],
                   reparam_from_solution=dict(ok=sol['ok'], max_seg_res=sol.get('max_seg_res'), iters=sol.get('iters_accepted'),
                       point_vs_registered_scaled=M.scaled_dist(sy, sol['point'], n13['point']) if sol['ok'] else None,
                       ang_raw=sol.get('ang_raw'), step=sol.get('final_step_scaled_2norm')),
                   reparam_from_propagation_in_main_run=(r.get('diag_reparam') or {}).get('point_vs_primary_scaled'))
        w0 = E.zi + s*E.vi; Jk = sy.J(w0, E.pi, M.RT); fd = {}
        for h in (1e-7, 1e-8, 1e-9):
            errs = []
            for e in np.eye(2):
                d = e*h*sy.sc
                a1, a2 = sy.P(w0 + d, E.pi, M.RT), sy.P(w0 - d, E.pi, M.RT)
                errs.append(float(np.linalg.norm((a1 - a2)/2 - Jk @ d)/np.linalg.norm(Jk @ d)))
            fd[f'h={h:g} scaled'] = max(errs)
        rec['fd_first_Wu_segment_rel'] = fd
        out.append(rec); print(json.dumps(rec), flush=True)
    return out

if __name__ == '__main__':
    T0 = time.time(); env, commit = M.env_commit()
    res = dict(note='supplementary diagnostics, not registered checks', commit=commit, env=env,
               C0=run('C0', {8}), F5R=run('F5R', {9}))
    res['runtime_s'] = time.time() - T0; res['peak_rss_mb'] = M.rss_mb()
    json.dump(res, open(os.path.join(M.RES, 'v13_a10_diag.json'), 'w'), indent=1)
