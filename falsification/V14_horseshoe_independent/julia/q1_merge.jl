# V14 Q1: merge the two worker outputs (base+W1, W2+W3; run as 2 processes under the box's 2-core budget) into
# results/q1_rossler.json, and evaluate the Q1 gate per the pre-registration.
using JSON
const RD = joinpath(@__DIR__, "..", "results")
a = JSON.parsefile(joinpath(RD, "q1_rossler_base_W1.json"))
b = JSON.parsefile(joinpath(RD, "q1_rossler_W2_W3.json"))
for k in ("spec_sha256", "map", "system", "ladder", "integrator", "julia", "packages", "git_commit")
    @assert a[k] == b[k] "worker metadata differs: $k"
end
out = deepcopy(a)
out["configs"] = merge(a["configs"], b["configs"])
out["consistency_checks"] = merge(a["consistency_checks"], b["consistency_checks"])
out["workers"] = [Dict("configs" => collect(keys(w["configs"])), "wall_seconds" => w["wall_seconds"],
                       "images_computed" => w["images_computed"], "finished" => w["finished"]) for w in (a, b)]
delete!(out, "wall_seconds"); delete!(out, "images_computed"); delete!(out, "finished")
dec(cfg, lab) = only(c for c in out["configs"][cfg]["covers"] if endswith(c["cover"], lab))
ex_ok = all(c["decision"] == "CERTIFIED" for c in out["configs"]["base"]["covers"])
w_rej = Dict(k => any(c["decision"] == "REJECTED" for c in out["configs"][k]["covers"]) for k in ("W1", "W2", "W3"))
w2mn = dec("W2", "M => N")["decision"] == "CERTIFIED"
out["gate_Q1"] = Dict("four_example_coverings_certified" => ex_ok, "W_configuration_rejected" => w_rej,
    "W2_Mprime_to_N_certified" => w2mn, "PASS" => ex_ok && all(values(w_rej)) && w2mn,
    "rule" => "W configuration REJECTED = at least one of its coverings fails (certified failure, or UNDECIDED at the top of the ladder)")
open(joinpath(RD, "q1_rossler.json"), "w") do f; JSON.print(f, out, 1); end
println("Q1 PASS = ", out["gate_Q1"]["PASS"], "   ", out["gate_Q1"])
for k in sort(collect(keys(out["configs"]))), c in out["configs"][k]["covers"]
    println(rpad(c["cover"], 14), c["decision"], "  level=", c["decided_at_level"], "  ", c["how"])
end
