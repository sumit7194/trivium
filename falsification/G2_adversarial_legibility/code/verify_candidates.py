#!/usr/bin/env python3
"""G2 — bridge-side INDEPENDENT verification of ansatz's sealed verdicts (round 8, §120/§121).

The bridge never accepts a sister's verdict unchecked (leg Y discipline). This recomputes ansatz's
central claims from the metric-only data, on the bridge's own machinery, before the join with tabula.
Does NOT touch tabula and does NOT depend on ansatz's sealed reasoning — only on the metrics.
"""
import sympy as sp

t, x, y, ph, v = sp.symbols("t x y phi v", real=True)
pt, px, py, pph, pv = sp.symbols("p_t p_x p_y p_phi p_v", real=True)


def poisson(F, H, coords, moms):
    return sum(sp.diff(F, q) * sp.diff(H, p) - sp.diff(F, p) * sp.diff(H, q)
               for q, p in zip(coords, moms))


print("=" * 74)
print("CANDIDATE A — integrable, irreducible Killing tensor, NO Killing-Yano root")
print("=" * 74)
# metric (contravariant diagonal) from G2_candidate_A.json
gtt = (-x**2 - y**2) / (y**2 + 1)
gxx = x**2 + y**2
gyy = x**2 + y**2
gpp = x**2 * (x**2 + y**2) / (x**2 + 1)
ginv = [(-y**2 - 1) / (x**2 + y**2), 1 / (x**2 + y**2), 1 / (x**2 + y**2),
        (x**2 + 1) / (x**2 * (x**2 + y**2))]
H = sp.Rational(1, 2) * (ginv[0]*pt**2 + ginv[1]*px**2 + ginv[2]*py**2 + ginv[3]*pph**2)
# contravariant Killing tensor K (diagonal) from the SEALED file — the object under test
Kuu = [y**2*(x**2 - 1)/(x**2 + y**2), y**2/(x**2 + y**2), -x**2/(x**2 + y**2),
       (-x**4 + y**2)/(x**2*(x**2 + y**2))]
Q = Kuu[0]*pt**2 + Kuu[1]*px**2 + Kuu[2]*py**2 + Kuu[3]*pph**2

# (1) Killing-tensor test: {Q, H} = 0 identically in the momenta
PB = sp.simplify(poisson(Q, H, [t, x, y, ph], [pt, px, py, pph]))
print(f"\n [A1] Killing-tensor check  {{Q, H}} = {PB}   -> {'KILLING TENSOR ✅' if PB == 0 else 'NOT ❌'}")

# (2) mixed eigenvalues K^a_b = K^{aa} g_{aa}; must be four DISTINCT functions (=> no KY root)
gdn = [1/gg for gg in ginv]                                  # g_{aa} = 1/g^{aa} (diagonal)
mixed = [sp.simplify(Kuu[i]*gdn[i]) for i in range(4)]
print(f" [A2] mixed eigenvalues K^a_b = {[str(m) for m in mixed]}")
distinct = all(sp.simplify(mixed[i] - mixed[j]) != 0 for i in range(4) for j in range(i+1, 4))
# numeric confirmation at a sample point
sub = {x: sp.Rational(13, 10), y: sp.Rational(7, 10)}
vals = sorted(float(m.subs(sub)) for m in mixed)
gaps = min(vals[i+1]-vals[i] for i in range(3))
print(f"      distinct as functions? {distinct}; at (x,y)=(1.3,0.7): {[round(vv,4) for vv in vals]}, "
      f"min gap {gaps:.3f}  -> {'4 DISTINCT ✅ (even-multiplicity of any Y.Y is impossible)' if distinct and gaps>1e-6 else 'NOT ❌'}")

# (3) non-vacuum: Ricci at a sample point (fully numeric, independent of ansatz's expression)
def ricci_numeric(gdiag, coords, pt_sub):
    g = sp.diag(*gdiag); gi = g.inv()
    Gam = [[[sum(gi[a, d]*(sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                           - sp.diff(g[b, c], coords[d])) for d in range(4))/2
             for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = sp.zeros(4, 4)
    for b in range(4):
        for c in range(4):
            e = 0
            for a in range(4):
                e += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                for d in range(4):
                    e += Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a]
            Ric[b, c] = e.subs(pt_sub)
    return Ric
Ric = ricci_numeric([1/gg for gg in ginv], [t, x, y, ph], sub)
nz = sum(1 for i in range(4) for j in range(4) if abs(sp.N(Ric[i, j])) > 1e-9)
print(f" [A3] non-vacuum: nonzero R_ab at (1.3,0.7): {nz}/16  -> "
      f"{'NOT VACUUM ✅ (consistent with Collinson-Dietz-Ruediger: type-D vacuum+KT would force KY)' if nz > 0 else 'vacuum ❌'}")

print("\n" + "=" * 74)
print("CANDIDATE B — integrable, TRANSCENDENTAL invariant (Galajinsky 2021)")
print("=" * 74)
# 2D block Hamiltonian from G2_candidate_B.json (the t,v sector decouples: p_t,p_v constant)
H2 = sp.Rational(1, 2)*((2 + (x + y)**2)*px**2 + 2*(1 + y*(x + y))*px*py + (1 + y**2)*py**2)
I = py/px - sp.log(px)                                        # the transcendental invariant
PBb = sp.simplify(poisson(I, H2, [x, y], [px, py]))
print(f"\n [B1] transcendental invariant  {{I, H_2}} = {PBb}   -> "
      f"{'CONSERVED ✅ (I = p_y/p_x - ln p_x is a genuine first integral)' if PBb == 0 else 'NOT ❌'}")
# I is non-analytic in p (branch point at p_x=0), so the grading theorem forbids polynomial reduction
print(f"      I is non-analytic in the momenta (ln p_x branch point) -> not a polynomial invariant")
