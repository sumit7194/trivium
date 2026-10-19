# V14 Q2 diagnosis, step 2 (POST HOC, NON-rigorous): dense float probe of the 40 lowest-margin AZ M1 => M2 level-3
# boxes from q2_m1m2_diag.json -> step 2b: ALL non-pass boxes, 17 x 17 grid per box, RK4 dt = 1e-3 first return; reports the minimum margin
# m = max(1 - |s|, |u| - 1) (outside F iff m > 0) and any grid point with m < 0 (a float point of the image inside F).
include(joinpath(@__DIR__, "q2_m1m2_diag.jl"))

function main_probe()
    sp = parse_spec(joinpath(SPECDIR, "hh1_M1M2.spec")); M = sp["tsets"]["M1"]; N = sp["tsets"]["M2"]
    Ni = Float64.(N.Ainv); Nc = Float64.(N.c)
    d = JSON.parsefile(joinpath(OUTDIR, "q2_m1m2_diag.json"))
    rows = d["non_pass"]   # all non-pass boxes (step 2b: corrected margin)
    res = Vector{Any}(undef, length(rows))
    Threads.@threads :dynamic for i in eachindex(rows)
        c = rows[i]["chart"]
        best = (Inf, NaN, NaN, NaN, NaN); inside = 0
        for uu in range(c[1], c[2], length = 17), ss in range(c[3], c[4], length = 17)
            y0 = Float64(M.c[1]) + Float64(M.A[1, 1]) * uu + Float64(M.A[1, 2]) * ss
            p0 = Float64(M.c[2]) + Float64(M.A[2, 1]) * uu + Float64(M.A[2, 2]) * ss
            y1, p1 = p1_float(y0, p0)
            isnan(y1) && continue
            u = Ni[1, 1] * (y1 - Nc[1]) + Ni[1, 2] * (p1 - Nc[2]); s = Ni[2, 1] * (y1 - Nc[1]) + Ni[2, 2] * (p1 - Nc[2])
            m = max(1 - abs(s), abs(u) - 1)   # outside F iff m > 0
            m < 0 && (inside += 1)
            m < best[1] && (best = (m, uu, ss, u, s))
        end
        res[i] = Dict("chart" => c, "coarse_margin" => rows[i]["float_margin"], "dense_min_margin" => best[1],
                      "at_source_us" => [best[2], best[3]], "image_us" => [best[4], best[5]], "n_points_inside_F" => inside)
    end
    sort!(res, by = r -> r["dense_min_margin"])
    for r in res[1:15]
        println(round(r["dense_min_margin"], sigdigits = 3), "  inside F: ", r["n_points_inside_F"], "  src (u,s) = ",
                round.(r["at_source_us"], digits = 5), "  image (u,s) = ", round.(r["image_us"], digits = 5))
    end
    println("boxes with float points inside F: ", count(r -> r["n_points_inside_F"] > 0, res), " of ", length(res))
    open(joinpath(OUTDIR, "q2_m1m2_probe.json"), "w") do f; JSON.print(f, Dict("note" => "POST HOC non-rigorous dense probe", "boxes" => res), 1); end
    println("wrote q2_m1m2_probe.json")
end

if abspath(PROGRAM_FILE) == @__FILE__
    main_probe()
end
