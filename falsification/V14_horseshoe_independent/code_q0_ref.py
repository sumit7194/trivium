"""50-digit non-rigorous reference for V14 Q0b: mpmath odefun (Taylor), Rossler to T = 5."""
import json, mpmath as M
M.mp.dps = 50
pts = [[1.0, 0.0, 0.0], [-8.0, 0.0, 0.0], [0.0, -8.4, 0.03], [5.0, 3.0, 0.5], [-3.0, 4.0, 0.1]]
out = []
for p in pts:
    f = M.odefun(lambda t, v: [-(v[1] + v[2]), v[0] + M.mpf('0.2')*v[1], M.mpf('0.2') + v[2]*(v[0] - M.mpf('5.7'))], 0, [M.mpf(c) for c in p])
    xt = f(5)
    out.append(dict(x0=p, xT=[M.nstr(v, 40) for v in xt]))
    print(p, [M.nstr(v, 20) for v in xt])
json.dump(dict(points=out, note='mpmath odefun, dps 50'), open('results/q0_ref.json', 'w'), indent=1)
