"""V17 driver (amendment 2 run plan). Controls first; STOP on any control failure; then the target with escalation."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v17 as V
out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/v17_runs.jsonl'), 'a')
def log(d, tag): d['tag'] = tag; print(json.dumps(d), flush=True); out.write(json.dumps(d) + '\n'); out.flush()
def basic_ok(d):
    return d['gate_E0_basis'] and d['basis_rank'] == d['kerr_count'] and d['nullity_E0'] >= d['kerr_count'] \
        and d['S_A'] == d['S_B'] and d['S_A'] >= d['floor']
for case in ('dM', 'da', 'null', 'sabotage'):
    for pt in ('PA', 'PB'):
        for qi in (0, 1):
            for r in range(1, 7):
                d = V.run(case, 'p1', pt, r, r + 1, qi, +1)
                ok = basic_ok(d)
                if case in ('dM', 'da', 'null'): ok = ok and d['S_A'] == d['kerr_count']
                if case == 'sabotage' and r == 2: ok = ok and d['S_A'] < d['kerr_count']
                log(d, 'control ' + ('PASS' if ok else 'FAIL'))
                if not ok: print('STOP: control failure', flush=True); sys.exit(2)
# amendment 3 gate: series exactness for every case and the target, both points, at N = 7 (largest used first)
for case in ('dM', 'da', 'null', 'sabotage', 'mn'):
    for pn in (('p1',) if case != 'mn' else ('p1', 'p2')):
        for pt in ('PA', 'PB'):
            V.set_prime(V.PRIMES[0]); M, a = V.PARAMS[pn]
            ok = V.exactness_gate(case, M, a, V.POINTS[pt], 7)
            d = dict(case=case, params=pn, point=pt, gate='series exactness N=7 vs truncated N=8', ok=bool(ok)); d['tag'] = 'gate ' + ('PASS' if ok else 'FAIL')
            print(json.dumps(d), flush=True); out.write(json.dumps(d) + '\n'); out.flush()
            if not ok: print('STOP: series exactness gate failed', flush=True); sys.exit(4)
for pn in ('p1', 'p2'):
    for pt in ('PA', 'PB'):
        for qi in (0, 1):
            for r in range(1, 7):
                for N in (r + 1, r + 2, r + 3):
                    d = V.run('mn', pn, pt, r, N, qi, +1)
                    ok = basic_ok(d)
                    log(d, 'target ' + ('ok' if ok else 'INTERNAL-FAIL'))
                    if not ok: print('STOP: internal check failed on target', flush=True); sys.exit(3)
                    if d['S_A'] == d['floor']: break
print('DONE', flush=True)
