"""V19 addendum 2: parity follow-up. Same tori (re-tuned identically), N = 64 and 128."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp, v19 as V
mp.mp.dps = 40
OUT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/v19_add2.jsonl'), 'a')
def log(d): print(json.dumps(d), flush=True); OUT.write(json.dumps(d) + '\n'); OUT.flush()
M, a = 5, 3
TORI = {'A_12': (4, '0.5', mp.mpf(1)/2, 10), 'B_12': (mp.mpf('4.5'), '0.3', mp.mpf(1)/2, 7),
        'C_23': (6, '0.3', mp.mpf(2)/3, 10), 'D_23': (5, '0.5', mp.mpf(2)/3, 17)}
T = {n: V.tune(M, a, rp*M, mp.mpf(zm), tg, ra*M) for n, (rp, zm, tg, ra) in TORI.items()}
PLAN = {'mn': {'A_12': [(4, -2), (1, 1), (0, 1), (2, 1)], 'B_12': [(4, -2), (1, 1), (0, 1), (2, 1)],
               'C_23': [(1, 1), (0, 1), (2, 1)], 'D_23': [(1, 1), (0, 1), (2, 1)]},
        'sabotage': {n: [(0, 2), (1, 2)] for n in TORI},
        'dM': {'A_12': [(4, -2)], 'B_12': [(4, -2)]}, 'da': {'A_12': [(4, -2)], 'B_12': [(4, -2)]},
        'null': {'A_12': [(4, -2)], 'B_12': [(4, -2)]}}
for case, per in PLAN.items():
    G0, G1 = V.pieces(M, a, case)
    for name, ks in per.items():
        for N in (64, 128):
            for k in ks:
                e = V.evaluate(T[name], G0, G1, N, k, check_shell=(k == ks[0]))
                log(dict(case=case, torus=name, N=N, k=list(k), Fk=mp.nstr(e['Fk'], 15), rho=mp.nstr(e['rho'], 6), shell=mp.nstr(e['shell'], 4)))
print('DONE', flush=True)
