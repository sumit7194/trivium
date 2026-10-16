# V14 gate Q0b: TaylorModels.jl validated flow of Rossler (a = 5.7, b = c = 0.2) to T = 5 from 5 points.
# The final enclosure must contain a 50-digit mpmath reference (computed separately by q0_ref.py).
using TaylorModels, TaylorIntegration, IntervalArithmetic, JSON
using TaylorModels.ValidatedInteg
include(joinpath(@__DIR__, "v14_rigor.jl"))
# Parameters enter as constant extra states (x[4] = b = 0.2, x[5] = a = 5.7), with initial boxes that enclose the
# exact decimals, so the flow is enclosed for the true parameters, not for their binary floats.
function rossler!(dx, x, p, t)
    dx[1] = -(x[2] + x[3]); dx[2] = x[1] + x[4]*x[2]; dx[3] = x[4] + x[3]*(x[1] - x[5])
    dx[4] = zero(x[4]); dx[5] = zero(x[5]); nothing
end
const PB = parse(Interval{Float64}, "0.2"); const PA = parse(Interval{Float64}, "5.7")
ref = JSON.parsefile(joinpath(@__DIR__, "..", "results", "q0_ref.json"))
orderQ, orderT, T = 2, 16, 5.0
sp = JetSpace(2*orderQ, ["ξ1", "ξ2", "ξ3", "ξ4", "ξ5"])
out = []
for r in ref["points"]
    x0 = Float64.(r["x0"]); X0 = vcat([interval(v) for v in x0], [PB, PA])
    sol = validated_integ(rossler!, X0, 0.0, T, orderQ, orderT, 1e-20, sp; maxsteps=20000)
    # evaluate the last Taylor model at the exact final time
    tTM = expansion_point(sol); xTM = get_xTM(sol); n = lastindex(sol)
    ε = tlabel_widen(n, T); δt = interval(T) - interval(tTM[n]) + interval(-ε, ε)
    encl = [rig_eval(xTM[i, n], δt, collect(symmetric_box(5))) for i in 1:3]
    refv = parse.(Float64, r["xT"])
    ok = all(in_interval(refv[i], encl[i]) for i in 1:3)
    push!(out, Dict("x0" => x0, "encl" => [string(e) for e in encl], "widths" => diam.(encl), "contains_ref" => ok))
    println(x0, " -> ", encl, "  contains ref: ", ok)
end
open(joinpath(@__DIR__, "..", "results", "q0_rossler.json"), "w") do f
    JSON.print(f, Dict("gate" => "Q0b", "all_pass" => all(o["contains_ref"] for o in out), "runs" => out,
                       "julia" => string(VERSION)), 1)
end
