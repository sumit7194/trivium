# V14 Amendment B1, gate Q0 re-qualification with the fixed pipeline (b1_rigor.jl: validated_integ3, interval
# Picard validation, midrad = false). Rössler (a = 5.7, b = c = 0.2) from Q0's 5 points to T = 5; the final
# enclosure must contain the 50-digit mpmath reference (results/q0_ref.json). Same setup as q0_rossler.jl
# (parameters as constant extra states with boxes enclosing the exact decimals; orderQ 2, orderT 16, abstol 1e-20).
# Also recorded as data (not the gate): the same run with the package default midrad = true.
using JSON, Pkg, Dates
include(joinpath(@__DIR__, "b1_rigor.jl"))
function rossler!(dx, x, p, t)
    dx[1] = -(x[2] + x[3]); dx[2] = x[1] + x[4]*x[2]; dx[3] = x[4] + x[3]*(x[1] - x[5])
    dx[4] = zero(x[4]); dx[5] = zero(x[5]); nothing
end
const PB = parse(Interval{Float64}, "0.2"); const PA = parse(Interval{Float64}, "5.7")
ref = JSON.parsefile(joinpath(@__DIR__, "..", "results", "q0_ref.json"))
T = 5.0
sp = JetSpace(2*B1_ORDER_Q, ["ξ1", "ξ2", "ξ3", "ξ4", "ξ5"])
function run_q0(midrad::Bool)
    out = []
    for r in ref["points"]
        x0 = Float64.(r["x0"]); X0 = vcat([interval(v) for v in x0], [PB, PA])
        secs = @elapsed sol = b1_integ(rossler!, X0, 0.0, T, sp; midrad = midrad)
        xTM = get_xTM(sol); tv = expansion_point(sol); n = lastindex(sol)
        dom = domain(xTM[1, n]); h = sup(dom)
        reached = BigFloat(tv[n]) + BigFloat(h) == BigFloat(T)
        δt = offset_in_step(T, tv[n], n, T, dom)
        encl = [rig_eval3(xTM[i, n], δt) for i in 1:3]
        refv = [parse(BigFloat, s) for s in r["xT"]]
        ok = reached && all(BigFloat(inf(encl[i])) <= refv[i] <= BigFloat(sup(encl[i])) for i in 1:3)
        # position of the reference inside the enclosure: min over components of distance to the nearer end / width
        rel = minimum(Float64(min(refv[i] - BigFloat(inf(encl[i])), BigFloat(sup(encl[i])) - refv[i]) / BigFloat(diam(encl[i]))) for i in 1:3)
        push!(out, Dict("x0" => x0, "encl" => [[inf(e), sup(e)] for e in encl], "widths" => diam.(encl),
                        "contains_ref" => ok, "reached_T_exactly" => reached, "nsteps" => n - 1,
                        "tdrift" => tdrift3(sol), "min_rel_margin_to_end" => rel,
                        "max_step_remainder" => maximum(mag(remainder(xTM[i, k])) for i in 1:5, k in 2:n),
                        "seconds" => secs))
        println("midrad=$midrad ", x0, " -> widths ", diam.(encl), "  contains ref: ", ok, "  steps ", n - 1,
                "  tdrift ", tdrift3(sol), "  rel margin ", rel)
    end
    return out
end
t0 = time()
gate = run_q0(false)
data_default = run_q0(true)
deps = Dict(string(v.name) => string(v.version) for (u, v) in Pkg.dependencies() if v.is_direct_dep)
res = Dict("gate" => "Q0b (B1 re-qualification)", "all_pass" => all(o["contains_ref"] for o in gate),
    "runs" => gate, "data_midrad_true" => Dict("all_contain" => all(o["contains_ref"] for o in data_default), "runs" => data_default),
    "integrator" => Dict("method" => "TaylorModels.ValidatedInteg.validated_integ3", "orderQ" => B1_ORDER_Q,
        "orderT" => B1_ORDER_T, "abstol" => B1_ABSTOL, "maxsteps" => B1_MAXSTEPS, "midrad" => B1_MIDRAD),
    "evaluation" => "rig_eval3: interval range of each TaylorModelN coefficient over [-1,1]^5 (+ its remainder), interval Horner in τ, + TM1 remainder; τ = T - t_n widened by 4 n eps(T) and intersected with [0, h_n] (labels verified exact)",
    "reference" => "results/q0_ref.json (mpmath odefun, 50 digits)",
    "julia" => string(VERSION), "packages" => deps,
    "git_commit" => readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`),
    "wall_seconds" => time() - t0, "finished" => string(now()))
open(joinpath(@__DIR__, "..", "results", "b1_q0.json"), "w") do f; JSON.print(f, res, 1); end
println("B1 Q0 all_pass = ", res["all_pass"])
