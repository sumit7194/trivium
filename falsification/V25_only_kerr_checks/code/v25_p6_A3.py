"""V25 amendment A3: ZV delta=2 exact, loop around z = 1, eps in {0.04, 0.02, 0.01, 0.005}."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); __file__ = os.path.join(HERE, 'v25_p6.py')
exec(open(os.path.join(HERE, 'v25_p6.py')).read().split('out = {}')[0])
axz = AxisPoly([1, 2, 1], [1, -2, 1], 0.8); Uz, dUz, _ = prolate_U('zv', sp.Rational(4, 5))
rec = loop_case('ZV exact: loop around z=1 (zero of f0) [A3]', axz, Uz, dUz, 1.0, (0.4, 0.6), 1, eps_list=(0.04, 0.02, 0.01, 0.005), rtol=1e-14)
json.dump(rec, open(os.path.join(HERE, '../results/v25_p6_A3.json'), 'w'), indent=1, default=str)
