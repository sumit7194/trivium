# V14 Q2 diagnosis (labelled POST HOC; no decision is taken from it): why does AZ M1 => M2 condition (a) leave
# 2977 of 4096 level-3 support boxes failing? For every level-3 box (64 x 64, as in the registered ladder):
#   - the rigorous image (same pipeline: p1_box via image_compute) -> ok / reason; if ok, where its (U, S) sits;
#   - a NON-rigorous float probe (RK4 first return on a 5 x 5 grid of points in the box) -> the true margin
#     m = min over points of (|u| - 1 if |u| > 1 else 1 - |s|); m > 0 means the true image misses F there.
# Output: results/q2_m1m2_diag.json and a summary on stdout.
include(joinpath(@__DIR__, "q2_hh_cover.jl"))

function p1_float(y0::Float64, py0::Float64; dt = 1e-3, tcap = 40.0)
    r = 2 * (1 / 6) - py0^2 - y0^2 + 2 * y0^3 / 3
    r <= 0 && return (NaN, NaN)
    f(u) = (u[3], u[4], -u[1] - 2u[1] * u[2], -u[2] - u[1]^2 + u[2]^2)
    u = (0.0, y0, sqrt(r), py0); t = 0.0
    while t < tcap
        k1 = f(u); k2 = f(u .+ (dt / 2) .* k1); k3 = f(u .+ (dt / 2) .* k2); k4 = f(u .+ dt .* k3)
        un = u .+ (dt / 6) .* (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4)
        if t > 0.5 && u[1] < 0 && un[1] >= 0
            θ = -u[1] / (un[1] - u[1])
            return (u[2] + θ * (un[2] - u[2]), u[4] + θ * (un[4] - u[4]))
        end
        u = un; t += dt
    end
    return (NaN, NaN)
end

function main_diag()
    sp = parse_spec(joinpath(SPECDIR, "hh1_M1M2.spec")); M = sp["tsets"]["M1"]; N = sp["tsets"]["M2"]
    @assert !N.special
    n = LADDER[end][2]
    charts = level3_boxes(n)
    rects = [piece_rect(M, c...) for c in charts]
    t = @elapsed prefetch!(rects)
    println(now(), "  rigorous level-3 images: ", length(rects), " in ", round(t, digits = 1), " s")
    Ni = Float64.(N.Ainv); Nc = Float64.(N.c)
    rows = Any[]
    for (c, rect) in zip(charts, rects)
        im = image(rect)
        st = !im[:ok] ? "fail_image" : (begin
            U, S = to_frame(N, im[:y], im[:z])
            miss_F(N, U, S, im[:z]) ? "pass" : (violates_a(N, U, S) ? "violation" : "fail_ambiguous")
        end)
        st == "pass" && continue
        d = Dict{String,Any}("chart" => Float64.(collect(c)), "status" => st, "reason" => im[:reason])
        if im[:ok]
            U, S = to_frame(N, im[:y], im[:z])
            d["U"] = [inf(U), sup(U)]; d["S"] = [inf(S), sup(S)]
            d["U_width"] = diam(U); d["S_width"] = diam(S)
        end
        # float probe on a 5 x 5 grid
        r = Float64.(collect(rect)); m = Inf; nnan = 0
        for a in range(r[1], r[2], length = 5), b in range(r[3], r[4], length = 5)
            y1, p1 = p1_float(a, b)
            isnan(y1) && (nnan += 1; continue)
            uu = Ni[1, 1] * (y1 - Nc[1]) + Ni[1, 2] * (p1 - Nc[2]); ss = Ni[2, 1] * (y1 - Nc[1]) + Ni[2, 2] * (p1 - Nc[2])
            m = min(m, abs(uu) > 1 ? abs(uu) - 1 : 1 - abs(ss))
        end
        d["float_margin"] = m; d["float_nan_points"] = nnan
        push!(rows, d)
    end
    cnt(f) = count(f, rows)
    println("non-pass boxes: ", length(rows), "  (fail_image ", cnt(r -> r["status"] == "fail_image"),
            ", fail_ambiguous ", cnt(r -> r["status"] == "fail_ambiguous"), ", violation ", cnt(r -> r["status"] == "violation"), ")")
    reasons = Dict{String,Int}(); for r in rows; r["status"] == "fail_image" && (reasons[r["reason"]] = get(reasons, r["reason"], 0) + 1); end
    println("image-failure reasons: ", reasons)
    ms = sort([r["float_margin"] for r in rows if isfinite(r["float_margin"])])
    if !isempty(ms)
        q(p) = ms[clamp(round(Int, p * length(ms)), 1, length(ms))]
        println("float margin over non-pass boxes: min ", ms[1], "  q10 ", q(0.1), "  median ", q(0.5), "  max ", ms[end],
                "  (negative = a float point inside F)")
    end
    amb = [r for r in rows if r["status"] == "fail_ambiguous"]
    if !isempty(amb)
        w = sort([r["U_width"] for r in amb]); ws = sort([r["S_width"] for r in amb])
        println("ambiguous boxes: median U width ", w[cld(length(w), 2)], ", median S width ", ws[cld(length(ws), 2)])
    end
    out = Dict("note" => "POST HOC diagnosis of AZ M1=>M2 (a) at level 3; float margins are non-rigorous",
               "n_boxes" => length(rects), "non_pass" => rows, "image_failure_reasons" => reasons, "updated" => string(now()))
    open(joinpath(OUTDIR, "q2_m1m2_diag.json"), "w") do f; JSON.print(f, out, 1); end
    println("wrote q2_m1m2_diag.json")
end

if abspath(PROGRAM_FILE) == @__FILE__
    main_diag()
end
