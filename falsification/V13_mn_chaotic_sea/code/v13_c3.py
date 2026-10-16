"""V13 C3: regular orbits around the bridge-located elliptic fixed points at C0 (0.95, 3) (the published islands:
inner rho ~ 0.89, outer rho ~ 8.35) must be NOT CHAOTIC on both arms. Base domain, acceptance 1e-8 (as the C0 gate),
thresholds from the chi 0.9 Kerr null. 10 orbits per island at x offsets d = +/-{0.002, 0.005, 0.01, 0.02, 0.04}*x_c
from the centre, p_x = 0. PASS iff 0 of the READ orbits is CHAOTIC."""
import sys, os, json, math, subprocess
import numpy as np
from v13_screen import run_orbits, POINTS, RES
thr = json.load(open(os.path.join(RES, 'v13_kerr_null_C0_analysis.json')))['thresholds']
U = json.load(open(os.path.join(RES, 'v13_upo_C0_19o20_3.json')))
isl = [u for u in U['upos'] if u['type'] == 'elliptic' and u['period'] == 1]
M, a_, beta = POINTS['C0']; out = dict(thresholds=thr, islands=[])
for u in isl:
    xc = u['points'][0][0]; k = math.sqrt(0.19)
    offs = [s*f*xc for f in (0.002, 0.005, 0.01, 0.02, 0.04) for s in (1, -1)]
    orbits = [(xc + d, 0.0) for d in offs]
    recs = run_orbits(M, a_, beta, 0.95, 3.0, orbits, 1e-12, 'base', 1e-8)
    for r in recs:
        if r['status'] == 'READ': r['verdict'] = 'CHAOTIC' if (r['A1'] > thr['A1'] and r['A2'] > thr['A2']) else 'NOT_CHAOTIC'
        r.pop('sec', None)
    rd = [r for r in recs if r['status'] == 'READ']
    out['islands'].append(dict(x_c=xc, rho_c=k*math.sqrt(xc*xc - 1), n_read=len(rd), n_chaotic=sum(r['verdict'] == 'CHAOTIC' for r in rd), orbits=recs))
    print('island x', round(xc, 5), 'rho', round(k*math.sqrt(xc*xc - 1), 4), 'read', len(rd), 'chaotic', sum(r['verdict'] == 'CHAOTIC' for r in rd), flush=True)
out['PASS'] = all(i['n_chaotic'] == 0 and i['n_read'] > 0 for i in out['islands'])
out['commit'] = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
json.dump(out, open(os.path.join(RES, 'v13_c3.json'), 'w'), indent=1); print('C3 PASS' if out['PASS'] else 'C3 FAIL')
