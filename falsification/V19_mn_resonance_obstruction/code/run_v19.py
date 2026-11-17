"""V19 driver: sign gate, then controls (all tori, N = 64 and 128; STOP on failure), then the target."""
import sys, os, json, time, resource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
import v19 as V
mp.mp.dps = 40
OUT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/v19_runs.jsonl'), 'a')
def log(d): print(json.dumps(d), flush=True); OUT.write(json.dumps(d) + '\n'); OUT.flush()
def guard():
    st = os.statvfs('/System/Volumes/Data')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9 > 2.0 or st.f_bavail*st.f_frsize/1e9 < 5.0: sys.exit('GUARD')
M, a = 5, 3
TORI = {'A_12': (4, '0.5', mp.mpf(1)/2, (2, -1), 10), 'B_12': (mp.mpf('4.5'), '0.3', mp.mpf(1)/2, (2, -1), 7),
        'C_23': (6, '0.3', mp.mpf(2)/3, (3, -2), 10), 'D_23': (5, '0.5', mp.mpf(2)/3, (3, -2), 17)}
G0f, _ = V.pieces(M, a, 'mn')
# sign gate (G1): which BL sign of a matches MN's chart -- exactly one must pass the mass shell
tori = {}
for name, (rpM, zm, tgt, k, raM) in TORI.items():
    ok = {}
    for s in (+1, -1):
        try:
            T = V.tune(M, s*a, rpM*M, mp.mpf(zm), tgt, raM*M)
        except Exception as ex:
            ok[s] = (False, None); log(dict(tag='gate sign', torus=name, asign=s, error=str(ex)[:120])); continue
        Tm = T; res = V.evaluate(Tm, G0f, lambda x, y: dict(tt=0, tp=0, pp=0, xx=0, yy=0), 8, k, check_shell=True)
        ok[s] = (res['shell'] < mp.mpf(10)**(-30), T)
        log(dict(tag='gate sign', torus=name, asign=s, shell=mp.nstr(res['shell'], 5), ra=mp.nstr(T.ra, 25),
                 ratio_err=mp.nstr(abs(T.ratio() - tgt), 5), E=mp.nstr(T.E, 20), L=mp.nstr(T.L, 20), Q=mp.nstr(T.Q, 20)))
    passing = [s for s in ok if ok[s][0]]
    if len(passing) != 1: print('STOP: sign gate', name, passing, flush=True); sys.exit(2)
    T = ok[passing[0]][1]
    if abs(T.ratio() - tgt) > mp.mpf(10)**(-20): print('STOP: resonance not tuned', name, flush=True); sys.exit(2)
    tori[name] = (T, k)
def run(case, Ns=(64, 128)):
    G0, G1 = V.pieces(M, a, case); res = {}
    for name, (T, k) in tori.items():
        r = {}
        for N in Ns:
            guard(); t0 = time.time(); e = V.evaluate(T, G0, G1, N, k); r[N] = e
            log(dict(tag=case, torus=name, N=N, Fk=mp.nstr(e['Fk'], 20), norm=mp.nstr(e['norm'], 12), rho=mp.nstr(e['rho'], 6),
                     shell=mp.nstr(e['shell'], 4), secs=round(time.time() - t0)))
            if e['shell'] > mp.mpf(10)**(-30): print('STOP: mass shell', case, name, flush=True); sys.exit(2)
        a64, a128 = r[64]['Fk'], r[128]['Fk']
        conv = abs(a64 - a128) <= max(mp.mpf(10)**(-12)*abs(a128), mp.mpf(10)**(-25))
        if not conv: print('STOP: N convergence', case, name, flush=True); sys.exit(2)
        res[name] = r[128]['rho']
    return res
for case in ('dM', 'da', 'null'):
    res = run(case)
    if any(v >= mp.mpf(10)**(-15) for v in res.values()): print('STOP: control', case, 'shows an obstruction', flush=True); sys.exit(3)
    log(dict(tag='control PASS', case=case))
res = run('sabotage')
if not any(v > mp.mpf(10)**(-6) for v in res.values()): print('VOID: sabotage shows no obstruction', flush=True); sys.exit(4)
log(dict(tag='control PASS', case='sabotage'))
res = run('mn')
verdict = 'OBSTRUCTED' if all(v > mp.mpf(10)**(-6) for v in res.values()) else ('NOT OBSTRUCTED' if all(v < mp.mpf(10)**(-15) for v in res.values()) else 'MIXED')
log(dict(tag='VERDICT', verdict=verdict, rho={k: mp.nstr(v, 6) for k, v in res.items()}))
print('DONE', flush=True)
