# Smoke test: validated integration of the harmonic oscillator over one period. The exact time-2pi flow is the
# identity, so the final enclosure must contain the image of the initial box's centre (1, 0).
using TaylorModels, TaylorIntegration, IntervalArithmetic
using TaylorModels.ValidatedInteg
function osc!(dx, x, p, t)
    dx[1] = x[2]; dx[2] = -x[1]; nothing
end
X0 = [1.0, 0.0] .+ 1e-6 .* symmetric_box(2)
orderQ, orderT = 2, 12
sp = JetSpace(2*orderQ, ["ξ1", "ξ2"])
sol = validated_integ(osc!, X0, 0.0, 2pi, orderQ, orderT, 1e-20, sp)
fin = flowpipe(sol)[end]
println("steps=", length(sol), "  final=", fin)
println("encloses (1,0): ", in_interval(1.0, fin[1]) && in_interval(0.0, fin[2]), "   widths: ", diam.(fin))
