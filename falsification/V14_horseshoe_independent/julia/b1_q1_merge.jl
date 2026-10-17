# V14 Amendment B1: merge the two B1 Q1 worker outputs (base+W1, W2+W3) into results/b1_q1.json, evaluate the Q1 gate
# exactly as q1_merge.jl does, and list every decision change against the pre-B1 Q1 (results/q1_rossler.json).
# An UNDECIDED-at-the-top-of-the-ladder covering is reported as UNDECIDED (run_cover records it as REJECTED with
# how = "UNDECIDED at the top of the ladder"; for a W configuration that counts as rejection by the registered rule,
# for an example covering it is a failure to certify).
using JSON
const RD = joinpath(@__DIR__, "..", "results")
a = JSON.parsefile(joinpath(RD, "b1_q1_base_W1.json"))
b = JSON.parsefile(joinpath(RD, "b1_q1_W2_W3.json"))
for k in ("spec_sha256", "map", "system", "ladder", "integrator", "julia", "packages", "git_commit")
    @assert a[k] == b[k] "worker metadata differs: $k"
end
out = deepcopy(a)
out["configs"] = merge(a["configs"], b["configs"])
out["consistency_checks"] = merge(a["consistency_checks"], b["consistency_checks"])
out["workers"] = [Dict("configs" => collect(keys(w["configs"])), "wall_seconds" => w["wall_seconds"],
                       "images_computed" => w["images_computed"], "finished" => w["finished"]) for w in (a, b)]
delete!(out, "wall_seconds"); delete!(out, "images_computed"); delete!(out, "finished")
status(c) = c["how"] == "UNDECIDED at the top of the ladder (level 3)" ? "UNDECIDED" : c["decision"]
dec(cfg, lab) = only(c for c in out["configs"][cfg]["covers"] if endswith(c["cover"], lab))
ex_ok = all(c["decision"] == "CERTIFIED" for c in out["configs"]["base"]["covers"])
w_rej = Dict(k => any(c["decision"] == "REJECTED" for c in out["configs"][k]["covers"]) for k in ("W1", "W2", "W3"))
w2mn = dec("W2", "M => N")["decision"] == "CERTIFIED"
out["gate_Q1"] = Dict("four_example_coverings_certified" => ex_ok, "W_configuration_rejected" => w_rej,
    "W2_Mprime_to_N_certified" => w2mn, "PASS" => ex_ok && all(values(w_rej)) && w2mn,
    "rule" => "as registered (q1_merge.jl): W configuration REJECTED = at least one of its coverings fails (certified failure, or UNDECIDED at the top of the ladder)")
old = JSON.parsefile(joinpath(RD, "q1_rossler.json"))
changes = []; table = []
for k in sort(collect(keys(out["configs"]))), c in out["configs"][k]["covers"]
    o = only(x for x in old["configs"][k]["covers"] if x["cover"] == c["cover"])
    row = Dict("cover" => c["cover"], "B1" => status(c), "B1_level" => c["decided_at_level"], "B1_how" => c["how"],
               "preB1" => status(o), "preB1_level" => o["decided_at_level"],
               "B1_levels" => [Dict("level" => l["level"], "b" => l["b"]["status"], "a" => l["a"] === nothing ? nothing : l["a"]["status"],
                                    "b_failed_pieces" => l["b"]["n_failed_pieces"],
                                    "a_failed_boxes" => l["a"] === nothing ? nothing : l["a"]["n_failed_boxes"]) for l in c["levels"]])
    push!(table, row)
    (row["B1"] != row["preB1"] || row["B1_level"] != row["preB1_level"]) && push!(changes, row)
end
out["decision_table"] = table
out["changes_vs_preB1_Q1"] = changes
open(joinpath(RD, "b1_q1.json"), "w") do f; JSON.print(f, out, 1); end
println("B1 Q1 PASS = ", out["gate_Q1"]["PASS"], "   ", out["gate_Q1"])
for r in table
    println(rpad(r["cover"], 14), rpad(r["B1"], 11), " level=", r["B1_level"], "   (pre-B1: ", r["preB1"], " level=", r["preB1_level"], ")   ",
            join(["L$(l["level"]): b=$(l["b"]) a=$(l["a"])" for l in r["B1_levels"]], "; "))
end
println("changes vs pre-B1: ", length(changes))
