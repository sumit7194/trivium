"""V13 C2 pilot self-test (A6): the pilot orbits of a level, rerun at rtol 1e-7, must FAIL the 1e-9 drift standard
(at least one orbit over the standard), while the pilot's chosen rtol must PASS. Usage: python v13_pilot_selftest.py <chi_key>"""
import sys, os, json
import sympy as sp
from v13_screen import kerr_levels, sample, run_orbits, POINTS, ACC, N_RET, RES
key = sys.argv[1]; M, a_, _ = POINTS[key]; K, lw, Eb, levels = kerr_levels(key)
L = [l for l in levels if l['kind'] == 'generic'][0]
orbits, _ = sample(K, L['E'], L['ell']); pick = orbits[:: max(1, len(orbits)//12)][:12]
bad = run_orbits(M, a_, 0, L['E'], L['ell'], pick, 1e-7, 'B9'); good = run_orbits(M, a_, 0, L['E'], L['ell'], pick, 1e-11, 'B9')
mb = max(r['drift'] for r in bad); mg = max(r['drift'] for r in good if r['returns'] >= N_RET)
res = dict(key=key, level=L, max_drift_rtol1e7=mb, max_drift_rtol1e11=mg, PASS=bool(mb > ACC and mg <= ACC))
json.dump(res, open(os.path.join(RES, f'v13_pilot_selftest_{key}.json'), 'w'), indent=1); print(res)
