# Hypothesis test for the Q0b misses: is the package's step-start time label t_n (Float64) off from the true elapsed
# time by ~1e-15? If so, widening δt by ±ε restores containment, and the misses are time-bookkeeping, not state error.
using TaylorModels, TaylorIntegration, IntervalArithmetic, JSON
using TaylorModels.ValidatedInteg
include(joinpath(@__DIR__, "v14_rigor.jl"))
function rossler!(dx, x, p, t)
    dx[1] = -(x[2] + x[3]); dx[2] = x[1] + x[4]*x[2]; dx[3] = x[4] + x[3]*(x[1] - x[5])
    dx[4] = zero(x[4]); dx[5] = zero(x[5]); nothing
end
const PB = parse(Interval{Float64}, "0.2"); const PA = parse(Interval{Float64}, "5.7")
ref = JSON.parsefile(joinpath(@__DIR__, "..", "results", "q0_ref.json"))
sp = JetSpace(4, ["ξ1", "ξ2", "ξ3", "ξ4", "ξ5"])
for r in ref["points"]
    x0 = Float64.(r["x0"]); X0 = vcat([interval(v) for v in x0], [PB, PA])
    sol = validated_integ(rossler!, X0, 0.0, 5.0, 2, 16, 1e-20, sp; maxsteps=20000)
    tTM = expansion_point(sol); n = lastindex(sol); xTM = get_xTM(sol)
    refv = [parse(BigFloat, s) for s in r["xT"]]
    res = Dict{Float64,Bool}()
    for ε in (0.0, 1e-15, 1e-14, 1e-13)
        δt = interval(5.0) - interval(tTM[n]) + interval(-ε, ε)
        e = [rig_eval(xTM[i, n], δt, collect(symmetric_box(5))) for i in 1:3]
        res[ε] = all(BigFloat(inf(e[i])) <= refv[i] <= BigFloat(sup(e[i])) for i in 1:3)
    end
    println(x0, "  steps=", n, "  contains with δt widened by ε: ", sort(collect(res)))
end
