# V14 Amendments Q2-U and Q3-S (PREREGISTRATION.md, 2026-10-21): one fixed setting for every covering.
#   - the Q2 pipeline (q2_hh_cover.jl), MAXDEPTH / LEAF_CAP from env (the chain sets 10 / 2^20);
#   - the Q2-R3 rule everywhere: if the registered orderT-16 image of a piece fails, retry orderT 14, then 18;
#   - the image cache is cleared between coverings whose source set differs (memory only; images are unchanged).
# Usage: julia -t 6 --project=julia julia/q2u_main.jl U|S
isdefined(@__MODULE__, :main_q2) || include(joinpath(@__DIR__, "q2_hh_cover.jl"))
include(joinpath(@__DIR__, "q2_fallback.jl"))

const NFALLBACK = Ref(0)
const FALLBACK_LOG = Any[]
# The Q2-R3 rule, applied inside the image computation (this redefinition replaces q2_hh_cover.jl's method).
function image_compute(rect::NTuple{4,Rat})
    Y = hull(ratI(rect[1]), ratI(rect[2])); Z = hull(ratI(rect[3]), ratI(rect[4]))
    r = p1_box(Y, Z)
    r[:orderT_used] = 16
    if !r[:ok]
        for oT in (14, 18)
            r2 = p1_box_fb(fb_integ(oT), Y, Z)
            if r2[:ok]
                r2[:orderT_used] = oT; r2[:primary_reason] = r[:reason]
                lock(CACHE_LOCK) do
                    NFALLBACK[] += 1
                    push!(FALLBACK_LOG, Dict("rect" => string.(rect), "orderT" => oT, "primary_reason" => r[:reason]))
                end
                r = r2; break
            end
        end
    end
    r[:rect] = string.(rect)
    r
end

const QSPEC = "/Users/sumit/Github/quantum/qsim/capd/horseshoe_results"
spec_sha(f) = bytes2hex(sha256(read(joinpath(QSPEC, f * ".spec"))))

function job_items(job)
    if job == "U"
        az = ["hh1_M0M0", "hh1_M0M1", "hh1_M1M2", "hh1_M2M3", "hh1_M3M4", "hh1_M4M0", "hh1_M4M1"]
        specs = Dict(s => parse_spec(joinpath(QSPEC, s * ".spec")) for s in vcat(az, ["hh1_W_AZ1_swap", "hh1_W_AZ2_shrink"]))
        ref = specs[az[1]]["tsets"]
        for g in az, (n, H) in specs[g]["tsets"]
            @assert ref[n].c == H.c && ref[n].A == H.A && ref[n].special == H.special && ref[n].capL == H.capL && ref[n].capR == H.capR
        end
        sets = Dict("AZ" => ref, "W1" => specs["hh1_W_AZ1_swap"]["tsets"], "W2" => specs["hh1_W_AZ2_shrink"]["tsets"])
        items = [("AZ", only(specs[g]["covers"])...) for g in az]
        for k in ("W1", "W2")
            @assert ("M2", "M3") in specs[k == "W1" ? "hh1_W_AZ1_swap" : "hh1_W_AZ2_shrink"]["covers"]
            push!(items, (k, "M2", "M3"))
        end
        return items, sets, Dict(s => spec_sha(s) for s in keys(specs))
    elseif job == "S"
        names = ["hh2_N0N0", "hh2_N0N3", "hh2_N3N4", "hh2_N4N5", "hh2_N5N6", "hh2_N6N0", "hh2_N6N3"]
        specs = Dict(s => parse_spec(joinpath(QSPEC, s * ".spec")) for s in names)
        for s in names
            @assert specs[s]["system"] == ["hh"] && specs[s]["iter"] == ["1"] && specs[s]["params"]["level"] == 1 // 6
        end
        ref = specs[names[1]]["tsets"]
        for g in names, (n, H) in specs[g]["tsets"]
            @assert ref[n].c == H.c && ref[n].A == H.A && !H.special
        end
        sets = Dict("S" => ref)
        items = [("S", only(specs[g]["covers"])...) for g in names]
        @assert [(a, b) for (_, a, b) in items] == [("N0","N0"),("N0","N3"),("N3","N4"),("N4","N5"),("N5","N6"),("N6","N0"),("N6","N3")]
        return items, sets, Dict(s => spec_sha(s) for s in names)
    end
    error("job must be U or S")
end

function main_u(job)
    items, sets, sha = job_items(job)
    deps = Dict(string(v.name) => string(v.version) for (u, v) in Pkg.dependencies() if v.is_direct_dep)
    git = readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`)
    results = Dict{String,Any}(); t0 = time(); lastsrc = nothing
    fn = joinpath(OUTDIR, job == "U" ? "q2u_all.json" : "q3s_all.json")
    for (k, a, b) in items
        src = (k == "W1" || k == "W2") ? (k, a) : ("AZ/S", a)
        if src != lastsrc
            lock(CACHE_LOCK) do; empty!(CACHE); end
            GC.gc(); lastsrc = src
        end
        nfb0 = NFALLBACK[]
        r = run_cover_b2(sets[k][a], sets[k][b], "$k: $a => $b")
        r["fallback_images_used"] = NFALLBACK[] - nfb0
        results["$k: $a => $b"] = r
        out = Dict("amendment" => job == "U" ? "Q2-U" : "Q3-S (not blind)", "covers" => results, "spec_sha256" => sha,
            "tsets" => Dict(kk => Dict(n => hset_json(H) for (n, H) in v) for (kk, v) in sets),
            "map" => "P1 (iter 1), section Θ1 = {x = 0, x' > 0, H = 1/6}, coordinates (y, p_y); px from the energy (positive branch)",
            "ladder" => LADDER, "refinement" => Dict("max_depth_below_level3" => MAXDEPTH, "leaf_cap" => LEAF_CAP),
            "fallback_rule" => "Q2-R3: orderT 16; if the image fails, orderT 14 then 18", "fallback_log" => FALLBACK_LOG,
            "integrator" => Dict("method" => "TaylorModels.ValidatedInteg.validated_integ3", "orderQ" => ORDER_Q,
                "orderT" => ORDER_T, "abstol" => ABSTOL, "maxsteps" => MAXSTEPS, "midrad" => B3_MIDRAD),
            "threads" => Threads.nthreads(), "julia" => string(VERSION), "packages" => deps, "git_commit" => git,
            "images_computed" => NCOMPUTED[], "wall_seconds" => time() - t0, "complete" => length(results) == length(items),
            "updated" => string(now()))
        open(fn * ".tmp", "w") do f; JSON.print(f, out, 1); end
        mv(fn * ".tmp", fn; force = true)
        println(now(), "  DONE ", k, ": ", a, " => ", b, "  ", r["decision"], "  (", r["how"], ")  fallback images ", r["fallback_images_used"]); flush(stdout)
    end
    println("wrote ", fn)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main_u(only(ARGS))
end
