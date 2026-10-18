# V14 Amendment B3: merge the two B2 worker outputs (groups N and M) into results/b3_q1.json; evaluate the Q1 gate
# (unchanged rule) and check for certified-vs-rejected contradictions with B1 (results/b1_q1.json), which are a FAIL.
using JSON
const RD = joinpath(@__DIR__, "..", "results")
gN = JSON.parsefile(joinpath(RD, "b3_q1_N.json")); gM = JSON.parsefile(joinpath(RD, "b3_q1_M.json"))
for k in ("spec_sha256", "ladder", "refinement", "integrator", "julia", "packages")
    @assert gN[k] == gM[k] "worker metadata differs: $k"
end
@assert gN["complete"] && gM["complete"]
covers = merge(gN["covers"], gM["covers"])
@assert length(covers) == 16
undec(c) = c["decision"] == "UNDECIDED"
certfail(c) = c["decision"] == "REJECTED"                  # B2 records UNDECIDED separately, so REJECTED = certified
dec(lab) = covers[lab]
base = ["base: M => M", "base: M => N", "base: N => M", "base: N => N"]
ex_ok = all(dec(l)["decision"] == "CERTIFIED" for l in base)
w_rej = Dict(k => any(c["decision"] != "CERTIFIED" for (l, c) in covers if startswith(l, k * ":")) for k in ("W1", "W2", "W3"))
w_rej_cert = Dict(k => any(certfail(c) for (l, c) in covers if startswith(l, k * ":")) for k in ("W1", "W2", "W3"))
w2mn = dec("W2: M => N")["decision"] == "CERTIFIED"
# B1 comparison
b1 = JSON.parsefile(joinpath(RD, "b1_q1.json"))
b1d = Dict(c["cover"] => c for k in keys(b1["configs"]) for c in b1["configs"][k]["covers"])
b1status(c) = c["how"] == "UNDECIDED at the top of the ladder (level 3)" ? "UNDECIDED" : c["decision"]
contr = []; table = []
for l in sort(collect(keys(covers)))
    c = covers[l]; o = b1d[l]
    s1 = b1status(o)
    ((c["decision"] == "CERTIFIED" && s1 == "REJECTED") || (c["decision"] == "REJECTED" && s1 == "CERTIFIED")) &&
        push!(contr, Dict("cover" => l, "B3" => c["decision"], "B1" => s1))
    ref = get(c, "refinement", nothing)
    push!(table, Dict("cover" => l, "B3" => c["decision"], "B3_level" => c["decided_at_level"], "B3_how" => c["how"],
                      "leaves" => c["leaves"], "max_depth" => c["max_depth"],
                      "refinement_seconds" => ref === nothing ? 0.0 : ref["seconds"], "B1" => s1, "B1_level" => o["decided_at_level"]))
end
out = Dict("gate" => "Q1 (B2 re-qualification)", "covers" => covers, "decision_table" => table,
    "gate_Q1" => Dict("four_example_coverings_certified" => ex_ok, "W_configuration_rejected" => w_rej,
        "W_configuration_rejected_by_certified_failure" => w_rej_cert, "W2_Mprime_to_N_certified" => w2mn,
        "PASS" => ex_ok && all(values(w_rej)) && w2mn && isempty(contr),
        "rule" => "as registered (q1_merge.jl): W configuration REJECTED = at least one of its coverings fails (certified failure, or UNDECIDED); any certified-vs-rejected contradiction with B1 is a FAIL"),
    "contradictions_with_B1" => contr,
    "workers" => [Dict("group" => g["group"], "images_computed" => g["images_computed"], "wall_seconds" => g["wall_seconds"],
                       "git_commit_at_start" => g["git_commit"], "finished" => g["updated"]) for g in (gN, gM)])
for k in ("spec_sha256", "tsets", "map", "ladder", "refinement", "integrator", "julia", "packages"); out[k] = gN[k]; end
out["git_commit"] = readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`)
open(joinpath(RD, "b3_q1.json"), "w") do f; JSON.print(f, out, 1); end
println("B2 Q1 PASS = ", out["gate_Q1"]["PASS"], "   contradictions with B1: ", length(contr))
for r in table
    println(rpad(r["cover"], 14), rpad(r["B3"], 11), " level=", r["B3_level"], " leaves=", r["leaves"], " maxdepth=", r["max_depth"],
            "   (B1: ", r["B1"], ")   ", r["B3_how"])
end
