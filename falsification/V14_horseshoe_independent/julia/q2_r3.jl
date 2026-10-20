# V14 Amendment Q2-R3 (pre-registered in fecf042): validation V1/V2 of the integrator-order fallback, then
# application to the single remaining Q2-R2 leaf L of AZ M1 => M2.
include(joinpath(@__DIR__, "q2_m1m2_diag.jl"))     # q2_hh_cover.jl + p1_float (non-rigorous, for V2 only)
include(joinpath(@__DIR__, "q2_fallback.jl"))

const FB_ORDERS = (14, 18)
rbox(rect) = (hull(ratI(rect[1]), ratI(rect[2])), hull(ratI(rect[3]), ratI(rect[4])))
meets(a, b) = !isempty_interval(intersect_interval(a, b))

function image_r3(rect)            # the Q2-R3 rule: registered image; if not ok, orderT 14 then 18
    im = image(rect)
    im[:ok] && return (im, 16)
    Y, Z = rbox(rect)
    for oT in FB_ORDERS
        r = p1_box_fb(fb_integ(oT), Y, Z)
        r[:ok] && return (r, oT)
    end
    return (im, 0)
end

function main_r3()
    sp = parse_spec(joinpath(SPECDIR, "hh1_M1M2.spec")); M = sp["tsets"]["M1"]; N = sp["tsets"]["M2"]
    out = Dict{String,Any}("amendment" => "Q2-R3", "git_commit" => readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`))
    # ---- validation ----
    charts = level3_boxes(LADDER[end][2])[1:20:end][1:200]
    rects = [piece_rect(M, c...) for c in charts]
    prefetch!(rects)
    v1 = 0; v2 = 0; nchk = 0; bad = Any[]
    lk = ReentrantLock()
    Threads.@threads :dynamic for k in eachindex(rects)
        rect = rects[k]; prim = image(rect)
        prim[:ok] || continue
        Y, Z = rbox(rect)
        encl = Any[(16, prim)]
        for oT in FB_ORDERS
            r = p1_box_fb(fb_integ(oT), Y, Z)
            r[:ok] && push!(encl, (oT, r))
        end
        pts = Tuple{Float64,Float64}[]
        r = Float64.(collect(rect))
        for a in range(r[1], r[2], length = 3), b in range(r[3], r[4], length = 3)
            y1, p1 = p1_float(a, b); isnan(y1) || push!(pts, (y1, p1))
        end
        lock(lk) do
            nchk += 1
            for (oT, e) in encl[2:end]
                if !(meets(e[:y], prim[:y]) && meets(e[:z], prim[:z]))
                    v1 += 1; push!(bad, Dict("chart" => string.(charts[k]), "orderT" => oT, "check" => "V1"))
                end
            end
            for (oT, e) in encl, (y1, p1) in pts
                if !(in_interval(y1, e[:y]) && in_interval(p1, e[:z]))
                    v2 += 1; push!(bad, Dict("chart" => string.(charts[k]), "orderT" => oT, "check" => "V2", "pt" => [y1, p1])); break
                end
            end
        end
    end
    out["validation"] = Dict("n_pieces_checked" => nchk, "V1_failures" => v1, "V2_failures" => v2, "failures" => bad)
    valid = nchk == 200 && v1 == 0 && v2 == 0
    println(now(), "  validation: pieces ", nchk, "  V1 failures ", v1, "  V2 failures ", v2, "  -> ", valid ? "PASS" : "FAIL (Q2-R3 void)")
    flush(stdout)
    # ---- application to L ----
    if valid
        L = (Rat(-631, 1024), Rat(-315, 512), Rat(887, 1024), Rat(111, 128))
        im, oT = image_r3(piece_rect(M, L...))
        rec = Dict{String,Any}("leaf" => string.(L), "orderT_used" => oT, "ok" => im[:ok], "reason" => im[:reason])
        if im[:ok]
            U, S = to_frame(N, im[:y], im[:z])
            rec["U"] = [inf(U), sup(U)]; rec["S"] = [inf(S), sup(S)]
            rec["status"] = miss_F(N, U, S, im[:z]) ? "pass" : (violates_a(N, U, S) ? "violation" : "ambiguous")
        else
            rec["status"] = "fail_image"
        end
        out["leaf_L"] = rec
        dec = rec["status"] == "pass" ? "CERTIFIED" : rec["status"] == "violation" ? "REJECTED" : "NEEDS_SUBTREE"
        out["decision"] = dec
        println(now(), "  leaf L: orderT ", oT, "  status ", rec["status"], "  U ", get(rec, "U", "-"), "  S ", get(rec, "S", "-"), "  -> M1=>M2 ", dec)
    else
        out["decision"] = "Q2-R3 VOID (validation failed)"
    end
    out["updated"] = string(now())
    open(joinpath(OUTDIR, "q2_hh_R3.json"), "w") do f; JSON.print(f, out, 1); end
    println("wrote q2_hh_R3.json")
end

if abspath(PROGRAM_FILE) == @__FILE__
    main_r3()
end
