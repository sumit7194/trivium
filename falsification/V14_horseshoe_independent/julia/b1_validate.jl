# V14 Amendment B1: validation of the fix against 256-bit BigFloat references (non-gating data; the gates are
# b1_q0.jl and b1_q1_cover.jl). Three parts:
#  (A) Box test with an exact solution, x' = x^2, x0 ∈ [1 - r, 1 + r] (x(t) = x0 / (1 - x0 t)):
#      the pre-B1 integrator (validated_integ) vs the B1 one (validated_integ3). Shows the sigma-truncation gap of
#      validated_integ (degrees > orderQ dropped and not bounded), which is separate from the Float64 rounding gap.
#  (B) Q0's 5 Rössler points, step by step: a 256-bit Taylor reference (own code below, independent of TaylorSeries)
#      at the exact times of every validated step.
#      - B1 (validated_integ3): the reference must lie in every step's enclosure (τ = 0, h/2, h).
#      - pre-B1 (validated_integ): |reference - Float64 polynomial| vs the package's remainder (the registered gap).
#  (C) Q1 spot check: the B1 P^2 enclosures of sampled pieces vs a 256-bit P^2 of the centre and 4 corners.
using JSON, Pkg, Dates, Random
include(joinpath(@__DIR__, "b1_poincare.jl"))
setprecision(BigFloat, 256)
const OUT = Dict{String,Any}()

# ---------------- 256-bit Taylor integrator for Rössler (b = 1/5, a = 57/10 exact to 256 bits) ----------------
const Bb = BigFloat(1) / 5; const Ab = BigFloat(57) / 10
const KREF = 40
function rcoeffs(u::NTuple{3,BigFloat})
    K = KREF
    x = zeros(BigFloat, K + 1); y = zeros(BigFloat, K + 1); z = zeros(BigFloat, K + 1)
    x[1], y[1], z[1] = u
    for k in 0:K-1
        conv = BigFloat(0)
        for j in 0:k; conv += z[j+1] * x[k-j+1]; end
        x[k+2] = -(y[k+1] + z[k+1]) / (k + 1)
        y[k+2] = (x[k+1] + Bb * y[k+1]) / (k + 1)
        z[k+2] = ((k == 0 ? Bb : BigFloat(0)) + conv - Ab * z[k+1]) / (k + 1)
    end
    return x, y, z
end
hornerB(c, s) = (acc = BigFloat(0); for k in length(c):-1:1; acc = acc * s + c[k]; end; acc)
function stepsize(x, y, z)
    m = max(abs(x[end]), abs(y[end]), abs(z[end]), abs(x[end-1]), abs(y[end-1]), abs(z[end-1]))
    return min(BigFloat(1) / 10, (BigFloat(10)^-40 / m)^(BigFloat(1) / KREF) / 2)
end
# State at increasing target times (BigFloat), from u0 at t = 0.
function ref_at(u0::NTuple{3,BigFloat}, targets::Vector{BigFloat})
    u = u0; t = BigFloat(0); out = NTuple{3,BigFloat}[]
    for T in targets
        while t < T
            x, y, z = rcoeffs(u); h = min(stepsize(x, y, z), T - t)
            u = (hornerB(x, h), hornerB(y, h), hornerB(z, h)); t += h
        end
        push!(out, u)
    end
    return out
end
# 256-bit P^2 on {x = 0, x' > 0}: second upcrossing (x from < 0 to >= 0) after t > 0.1, as in q1_spotcheck.jl.
function ref_p2(y0::BigFloat, z0::BigFloat)
    u = (BigFloat(0), y0, z0); t = BigFloat(0); ups = 0
    while t < 40
        x, y, z = rcoeffs(u); h = stepsize(x, y, z)
        un = (hornerB(x, h), hornerB(y, h), hornerB(z, h))
        if t > BigFloat(1) / 10 && u[1] < 0 && un[1] >= 0
            ups += 1
            if ups == 2
                lo = BigFloat(0); hi = h                     # bisection to bracket, then Newton
                for _ in 1:60
                    m = (lo + hi) / 2; hornerB(x, m) < 0 ? (lo = m) : (hi = m)
                end
                dxc = [k * x[k+1] for k in 1:KREF]
                s = (lo + hi) / 2
                for _ in 1:20; s -= hornerB(x, s) / hornerB(dxc, s); end
                return (hornerB(y, s), hornerB(z, s), t + s)
            end
        end
        u = un; t += h
    end
    error("no second return")
end

# ---------------- (A) x' = x^2 box test ----------------
f1!(dx, x, p, t) = (dx[1] = x[1]^2; nothing)
partA = []
for r in (1e-1, 1e-2, 1e-3)
    X = interval(1 - r, 1 + r); sp1 = JetSpace(4, ["ξ1"])
    exact_range(T) = (BigFloat(inf(X)) / (1 - BigFloat(inf(X)) * T), BigFloat(sup(X)) / (1 - BigFloat(sup(X)) * T))
    # pre-B1
    s1 = validated_integ(f1!, [X], 0.0, 0.4, 2, 12, 1e-20, sp1; maxsteps = 2000)
    x1 = get_xTM(s1); n1 = lastindex(s1); h1 = sup(domain(x1[1, n1]))
    T1 = sum(BigFloat(sup(domain(x1[1, k]))) for k in 2:n1)
    devs = Float64[]
    for ξ in (-1.0, -0.5, 0.0, 0.5, 1.0)
        x0 = BigFloat(mid(X)) + BigFloat(radius(X)) * ξ
        pv = sum(BigFloat(c([ξ])) * BigFloat(h1)^(k - 1) for (k, c) in enumerate(polynomial(x1[1, n1]).coeffs))
        push!(devs, Float64(x0 / (1 - x0 * T1) - pv))
    end
    E1 = rig_eval(x1[1, n1], interval(h1), [interval(-1.0, 1.0)])
    lo, hi = exact_range(T1)
    v1_range_ok = BigFloat(inf(E1)) <= lo && hi <= BigFloat(sup(E1))
    # B1
    s3 = b1_integ(f1!, [X], 0.0, 0.4, sp1)
    x3 = get_xTM(s3); n3 = lastindex(s3); h3 = sup(domain(x3[1, n3]))
    T3 = sum(BigFloat(sup(domain(x3[1, k]))) for k in 2:n3)
    E3 = rig_eval3(x3[1, n3], interval(h3))
    lo3, hi3 = exact_range(T3)
    b1_ok = BigFloat(inf(E3)) <= lo3 && hi3 <= BigFloat(sup(E3)) && tdrift3(s3) == 0.0 && T3 == BigFloat(0.4)
    push!(partA, Dict("r" => r, "preB1_remainder_mag" => mag(remainder(x1[1, n1])), "preB1_pointwise_dev_xi_-1_-.5_0_.5_1" => devs,
        "preB1_max_dev_over_remainder" => maximum(abs.(devs)) / mag(remainder(x1[1, n1])),
        "preB1_range_encl" => [inf(E1), sup(E1)], "exact_range" => Float64.([lo, hi]), "preB1_range_contains_exact" => v1_range_ok,
        "B1_range_encl" => [inf(E3), sup(E3)], "B1_contains_exact" => b1_ok, "B1_overestimate" => Float64(BigFloat(diam(E3)) - (hi3 - lo3))))
    println("(A) r=$r  pre-B1 max|dev|/|rem| = ", partA[end]["preB1_max_dev_over_remainder"], "  pre-B1 range contains exact: ", v1_range_ok, "  B1 contains exact: ", b1_ok)
end
OUT["A_xsquared_box"] = partA

# ---------------- (B) Q0 points, every step ----------------
function rossler5!(dx, x, p, t)
    dx[1] = -(x[2] + x[3]); dx[2] = x[1] + x[4]*x[2]; dx[3] = x[4] + x[3]*(x[1] - x[5])
    dx[4] = zero(x[4]); dx[5] = zero(x[5]); nothing
end
const PBq = parse(Interval{Float64}, "0.2"); const PAq = parse(Interval{Float64}, "5.7")
q0ref = JSON.parsefile(joinpath(@__DIR__, "..", "results", "q0_ref.json"))
sp5 = JetSpace(4, ["ξ1", "ξ2", "ξ3", "ξ4", "ξ5"])
partB = []
for r in q0ref["points"]
    x0 = Float64.(r["x0"]); X0 = vcat([interval(v) for v in x0], [PBq, PAq]); u0 = Tuple(BigFloat.(x0))
    # reference integrator check against the 50-digit mpmath value at T = 5
    uT = ref_at(u0, [BigFloat(5)])[1]
    refdiff = maximum(Float64(abs(uT[i] - parse(BigFloat, r["xT"][i]))) for i in 1:3)
    # B1
    s3 = b1_integ(rossler5!, X0, 0.0, 5.0, sp5); x3 = get_xTM(s3); n3 = lastindex(s3)
    starts = BigFloat[0]; for k in 2:n3-1; push!(starts, starts[end] + BigFloat(sup(domain(x3[1, k])))); end
    targets = BigFloat[]; meta = Tuple{Int,Float64}[]
    for k in 2:n3, τ in (0.0, sup(domain(x3[1, k])) / 2, sup(domain(x3[1, k])))
        push!(targets, starts[k-1] + BigFloat(τ)); push!(meta, (k, τ))
    end
    p = sortperm(targets); refs = Vector{NTuple{3,BigFloat}}(undef, length(targets))
    refs[p] = ref_at(u0, targets[p])
    nout = 0; minrel = Inf; maxuse = 0.0
    for (j, (k, τ)) in enumerate(meta), i in 1:3
        E = rig_eval3(x3[i, k], interval(τ)); v = refs[j][i]
        inside = BigFloat(inf(E)) <= v <= BigFloat(sup(E))
        nout += !inside
        minrel = min(minrel, Float64(min(v - BigFloat(inf(E)), BigFloat(sup(E)) - v) / BigFloat(diam(E))))
        maxuse = max(maxuse, Float64(abs(v - (BigFloat(inf(E)) + BigFloat(sup(E))) / 2) / (BigFloat(diam(E)) / 2)))
    end
    # pre-B1: Float64 polynomial at the exact parameters vs the package's remainder, at the end of every step
    s1 = validated_integ(rossler5!, X0, 0.0, 5.0, 2, 16, 1e-20, sp5; maxsteps = 20000); x1 = get_xTM(s1); n1 = lastindex(s1)
    ξ4 = (Bb - BigFloat(mid(PBq))) / BigFloat(radius(PBq)); ξ5 = (Ab - BigFloat(mid(PAq))) / BigFloat(radius(PAq))
    ends = BigFloat[]; acc = BigFloat(0)
    for k in 2:n1; acc += BigFloat(sup(domain(x1[1, k]))); push!(ends, acc); end
    r1 = ref_at(u0, ends)
    ratios = Float64[]; nout1 = 0
    for k in 2:n1, i in 1:3
        tm = x1[i, k]; h = BigFloat(sup(domain(tm)))
        pv = BigFloat(0)
        for c in reverse(polynomial(tm).coeffs)
            cv = evaluate(c * BigFloat(1), BigFloat[0, 0, 0, ξ4, ξ5])
            pv = pv * h + cv
        end
        dev = r1[k-1][i] - pv; R = remainder(tm)
        nout1 += !(BigFloat(inf(R)) <= dev <= BigFloat(sup(R)))
        push!(ratios, Float64(abs(dev)) / mag(R))
    end
    push!(partB, Dict("x0" => x0, "ref_integrator_vs_mpmath_at_T5" => refdiff,
        "B1_steps" => n3 - 1, "B1_samples" => 3 * length(meta), "B1_outside" => nout,
        "B1_min_rel_margin_to_end" => minrel, "B1_max_|ref-mid|/radius" => maxuse,
        "preB1_steps" => n1 - 1, "preB1_samples" => length(ratios), "preB1_ref_outside_poly+rem" => nout1,
        "preB1_max_|ref-poly|/|rem|" => maximum(ratios), "preB1_median_|ref-poly|/|rem|" => sort(ratios)[end ÷ 2]))
    println("(B) ", x0, "  ref vs mpmath ", refdiff, "  B1 outside ", nout, "/", 3 * length(meta), " (min rel margin ", minrel,
            ")  pre-B1 outside ", nout1, "/", length(ratios), " (max |ref-poly|/|rem| ", maximum(ratios), ")")
end
OUT["B_q0_points_every_step"] = partB

# ---------------- (C) Q1 spot check, B1 P^2 vs 256-bit P^2 ----------------
const PB = ratI(1 // 5); const PA = ratI(57 // 10)
srcs = Dict("M" => (-42//5, -38//5, 7//250, 17//500), "N" => (-57//10, -23//5, 7//250, 17//500),
            "W2_Mprime" => (-8003//1000, -7997//1000, -369//1000, 431//1000), "W3_M" => (-20001//2500, -19999//2500, 7//250, 17//500))
rng = MersenneTwister(20261018)
partC = []; nbad = 0; nsamp = 0
for (name, (y1, y2, z1, z2)) in sort(collect(srcs)), (kind, n) in (("support_level2", 16), ("support_level3", 64), ("edge_level3", 128))
    dy = (y2 - y1) / (kind == "edge_level3" ? 1 : n); dz = (z2 - z1) / n
    i = rand(rng, 1:n); j = rand(rng, 1:n)
    r = kind == "edge_level3" ? (rand(rng, Bool) ? (y1, y1, z1 + (j-1)*dz, z1 + j*dz) : (y2, y2, z1 + (j-1)*dz, z1 + j*dz)) :
                                (y1 + (i-1)*dy, y1 + i*dy, z1 + (j-1)*dz, z1 + j*dz)
    im = p2_box(hull(ratI(r[1]), ratI(r[2])), hull(ratI(r[3]), ratI(r[4])), PB, PA)
    if !im[:ok]
        push!(partC, Dict("src" => name, "kind" => kind, "rect" => string.(r), "ok" => false, "reason" => im[:reason])); continue
    end
    pts = [((r[1] + r[2]) / 2, (r[3] + r[4]) / 2)]
    for a in (r[1], r[2]), b in (r[3], r[4]); push!(pts, (a, b)); end
    inside = Bool[]
    for (a, b) in unique(pts)
        yv, zv, tv = ref_p2(BigFloat(a), BigFloat(b))     # BigFloat(::Rational) rounds to 256 bits
        push!(inside, BigFloat(inf(im[:y])) <= yv <= BigFloat(sup(im[:y])) && BigFloat(inf(im[:z])) <= zv <= BigFloat(sup(im[:z])) &&
                      BigFloat(inf(im[:tret])) <= tv <= BigFloat(sup(im[:tret])))
    end
    global nbad += count(!, inside); global nsamp += length(inside)
    push!(partC, Dict("src" => name, "kind" => kind, "rect" => string.(r), "ok" => true, "n_points" => length(inside), "all_inside" => all(inside),
                      "y" => [inf(im[:y]), sup(im[:y])], "z" => [inf(im[:z]), sup(im[:z])], "tret" => [inf(im[:tret]), sup(im[:tret])]))
    println("(C) ", name, " ", kind, " ", r, "  inside: ", inside, "  y width ", diam(im[:y]))
end
OUT["C_q1_spotcheck"] = Dict("samples" => partC, "n_points" => nsamp, "n_outside" => nbad)

deps = Dict(string(v.name) => string(v.version) for (u, v) in Pkg.dependencies() if v.is_direct_dep)
OUT["reference"] = "own 256-bit Taylor integrator (order $KREF, step from the last two coefficients, local error target 1e-40); P^2 crossing by bisection + Newton on the step polynomial"
OUT["julia"] = string(VERSION); OUT["packages"] = deps
OUT["git_commit"] = readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`); OUT["finished"] = string(now())
open(joinpath(@__DIR__, "..", "results", "b1_validation.json"), "w") do f; JSON.print(f, OUT, 1); end
println("wrote results/b1_validation.json")
