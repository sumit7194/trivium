# Diagnostic for Q0b misses: is the reference inside (i) the last flowpipe box, (ii) the TM evaluated at T?
using TaylorModels, TaylorIntegration, IntervalArithmetic, JSON
using TaylorModels.ValidatedInteg
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
    tTM = expansion_point(sol); n = lastindex(sol); fp = flowpipe(sol)[n]
    refv = [parse(BigFloat, s) for s in r["xT"]]
    inbox = [isinf(sup(fp[i])) || (BigFloat(inf(fp[i])) <= refv[i] <= BigFloat(sup(fp[i]))) for i in 1:3]
    xTM = get_xTM(sol); δt = interval(5.0) - interval(tTM[n])
    e = [evaluate(evaluate(xTM[i, n], δt), symmetric_box(5)) for i in 1:3]
    ine = [BigFloat(inf(e[i])) <= refv[i] <= BigFloat(sup(e[i])) for i in 1:3]
    dom = domain(sol, n)
    println(x0, "  t_n=", tTM[n], " dom=", dom, " δt=", δt, "\n   in flowpipe box: ", inbox, "  in TM(T): ", ine,
            "  miss/width: ", [ine[i] ? 0.0 : Float64(min(abs(refv[i]-BigFloat(inf(e[i]))), abs(refv[i]-BigFloat(sup(e[i]))))/BigFloat(diam(e[i]))) for i in 1:3])
end
