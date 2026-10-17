# V14 gate Q1: Rössler qualification on quantum's exact h-set specs (read as inputs only).
# Checks per the V14 pre-registration (AZ 2001 Def. 2 as used in quantum's T0/B8), map P^2 on {x = 0, x' > 0}:
#   (b) P(M^l) ⊂ N_le = {u_N < -1} and P(M^r) ⊂ N_ri = {u_N > 1}  (orientation +1), or the reverse (orientation -1);
#   (a) P(|M|) misses {|u_N| ≤ 1, |s_N| ≥ 1}; the strong form |s_N| < 1 is recorded as data.
# Ladder: level 1/2/3 = 8/32/128 pieces per edge and 4×4/16×16/64×64 boxes per support. A covering is CERTIFIED at
# the first level where every piece of (a) and (b) certifies at that level; REJECTED (certified failure) as soon as
# a rigorous enclosure refutes (b) in both orientations, or lies inside the forbidden set of (a); otherwise
# UNDECIDED after level 3.
# Usage: julia --project=julia julia/q1_rossler_cover.jl [config ...]   (configs: base W1 W2 W3; default all)
using JSON, SHA, Dates, Pkg
include(joinpath(@__DIR__, "q1_poincare.jl"))

const SPECDIR = "/Users/sumit/Github/quantum/qsim/capd/horseshoe_results"
const SPECS = ["r1_ex_coneM", "r1_ex_coneN", "r1_W1_swap", "r1_W2_rot90", "r1_W3_shrink"]
const LADDER = [(8, 4), (32, 16), (128, 64)]       # (pieces per edge, boxes per support side)
const OUTDIR = joinpath(@__DIR__, "..", "results")

const Rat = Rational{BigInt}
parse_rat(s) = (p = split(s, "/"); length(p) == 1 ? Rat(parse(BigInt, p[1])) : parse(BigInt, p[1]) // parse(BigInt, p[2]))

# h-set: section point (y, z) = c + A (u, s), A = [U S] (columns), Ainv given; |u|, |s| ≤ 1.
struct HSet
    name::String
    c::Vector{Rat}
    A::Matrix{Rat}
    Ainv::Matrix{Rat}
end
# Spec reading (stated in the report): "tset NAME c1 c2 U1 U2 S1 S2 I11 I12 I21 I22": centre (y, z), u-column U,
# s-column S, and the inverse of A = [U S] row-major. Verified exactly below (A * Ainv = I) for every tset.
function parse_spec(path)
    d = Dict{String,Any}("tsets" => Dict{String,HSet}(), "covers" => Tuple{String,String}[], "params" => Dict{String,Rat}())
    for ln in eachline(path)
        w = split(strip(ln)); isempty(w) && continue
        if w[1] == "param"
            d["params"][w[2]] = parse_rat(w[3])
        elseif w[1] == "tset"
            v = parse_rat.(w[3:end]); @assert length(v) == 10
            A = [v[3] v[5]; v[4] v[6]]; Ai = [v[7] v[8]; v[9] v[10]]
            @assert A * Ai == [1 0; 0 1] "inverse check failed in $path"
            d["tsets"][w[2]] = HSet(w[2], v[1:2], A, Ai)
        elseif w[1] == "cover"
            push!(d["covers"], (w[2], w[3]))
        elseif w[1] == "ex_cone"
            # "ex_cone y1 y2 z1 z2 α β": the box [y1, y2] × [z1, z2] with u = y, s = z (α, β: cone-form data, unused)
            v = parse_rat.(w[2:5])
            c = [(v[1] + v[2]) / 2, (v[3] + v[4]) / 2]
            A = [(v[2] - v[1]) / 2 0; 0 (v[4] - v[3]) / 2]
            d["ex_cone_box"] = HSet("box", c, A, inv(A))
            d["ex_cone_form"] = w[6:7]
        else
            d[w[1]] = w[2:end]
        end
    end
    return d
end

is_monomial(A) = (A[1, 2] == 0 && A[2, 1] == 0 && A[1, 1] != 0 && A[2, 2] != 0) ||
                 (A[1, 1] == 0 && A[2, 2] == 0 && A[1, 2] != 0 && A[2, 1] != 0)

# Section rectangle (exact rationals) of the source-frame piece [u1,u2] × [s1,s2]; A is monomial, so the image of a
# frame rectangle is an axis-aligned rectangle.
function piece_rect(M::HSet, u1, u2, s1, s2)
    pts = [M.c + M.A * [u, s] for u in (u1, u2), s in (s1, s2)]
    ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
    return (minimum(ys), maximum(ys), minimum(zs), maximum(zs))
end
edge_pieces(M::HSet, side::Int, K::Int) = [piece_rect(M, Rat(side), Rat(side), Rat(-1) + Rat(2(k - 1), K), Rat(-1) + Rat(2k, K)) for k in 1:K]
support_boxes(M::HSet, n::Int) = [piece_rect(M, Rat(-1) + Rat(2(i - 1), n), Rat(-1) + Rat(2i, n), Rat(-1) + Rat(2(j - 1), n), Rat(-1) + Rat(2j, n)) for i in 1:n for j in 1:n]

# Target frame coordinates of an image enclosure, in interval arithmetic (monomial Ainv: no wrapping).
function to_frame(N::HSet, yI, zI)
    Ai = ratI.(N.Ainv); c = ratI.(N.c)
    dy = yI - c[1]; dz = zI - c[2]
    return (Ai[1, 1] * dy + Ai[1, 2] * dz, Ai[2, 1] * dy + Ai[2, 2] * dz)
end

const PB = ratI(1 // 5); const PA = ratI(57 // 10)
const CACHE = Dict{NTuple{4,Rat},Dict{Symbol,Any}}()
const NCOMPUTED = Ref(0)
function image(rect::NTuple{4,Rat})
    get!(CACHE, rect) do
        NCOMPUTED[] += 1
        Y = hull(ratI(rect[1]), ratI(rect[2])); Z = hull(ratI(rect[3]), ratI(rect[4]))
        r = p2_box(Y, Z, PB, PA)
        r[:rect] = string.(rect)
        r
    end
end

fstr(I) = [inf(I), sup(I)]

# ---- condition (b) at one level ----
function check_b(M::HSet, N::HSet, K::Int)
    imgs = Dict(side => [image(r) for r in edge_pieces(M, side, K)] for side in (-1, 1))
    fr = Dict(side => [im[:ok] ? to_frame(N, im[:y], im[:z]) : nothing for im in imgs[side]] for side in (-1, 1))
    allok = all(im[:ok] for side in (-1, 1) for im in imgs[side])
    L = fr[-1]; R = fr[1]
    okL(f, test) = f !== nothing && test(f[1])
    orient_p = allok && all(okL(f, U -> sup(U) < -1) for f in L) && all(okL(f, U -> inf(U) > 1) for f in R)
    orient_m = allok && all(okL(f, U -> inf(U) > 1) for f in L) && all(okL(f, U -> sup(U) < -1) for f in R)
    some(fs, test) = any(f !== nothing && test(f[1]) for f in fs)
    refute_p = some(L, U -> inf(U) >= -1) || some(R, U -> sup(U) <= 1)
    refute_m = some(L, U -> sup(U) <= 1) || some(R, U -> inf(U) >= -1)
    status = (orient_p || orient_m) ? "PASS" : ((refute_p && refute_m) ? "CERTIFIED_FAILURE" : "UNDECIDED")
    orientation = orient_p ? 1 : (orient_m ? -1 : 0)
    hullU(fs) = (g = [f[1] for f in fs if f !== nothing]; isempty(g) ? nothing : fstr(reduce(hull, g)))
    hullS(fs) = (g = [f[2] for f in fs if f !== nothing]; isempty(g) ? nothing : fstr(reduce(hull, g)))
    d = Dict{String,Any}("pieces_per_edge" => K, "status" => status, "orientation" => orientation,
        "all_pieces_computed" => allok,
        "n_failed_pieces" => count(!im[:ok] for side in (-1, 1) for im in imgs[side]),
        "failure_reasons" => unique([im[:reason] for side in (-1, 1) for im in imgs[side] if !im[:ok]]),
        "left_edge_image_uN_hull" => hullU(L), "right_edge_image_uN_hull" => hullU(R),
        "left_edge_image_sN_hull" => hullS(L), "right_edge_image_sN_hull" => hullS(R),
        "refutes_orientation_+1" => refute_p, "refutes_orientation_-1" => refute_m)
    if orientation != 0
        # margin: how far inside the required side each edge image lies, in N's u-units (positive = inside)
        mL = minimum(orientation == 1 ? (-1 - sup(f[1])) : (inf(f[1]) - 1) for f in L)
        mR = minimum(orientation == 1 ? (inf(f[1]) - 1) : (-1 - sup(f[1])) for f in R)
        uscale = maximum(abs.(N.A[:, 1]))     # |u-column| (monomial: one nonzero entry)
        d["margin_left_uN"] = mL; d["margin_right_uN"] = mR
        d["margin_left_abs"] = mL * Float64(uscale); d["margin_right_abs"] = mR * Float64(uscale)
    end
    oks = [im for side in (-1, 1) for im in imgs[side] if im[:ok]]
    if !isempty(oks)
        d["return_time_hull"] = fstr(reduce(hull, [im[:tret] for im in oks]))
        d["transversality_min_xdot"] = minimum(im[:xdot_min] for im in oks)
    end
    return d
end

# ---- condition (a) at one level ----
function check_a(M::HSet, N::HSet, n::Int)
    imgs = [image(r) for r in support_boxes(M, n)]
    allok = all(im[:ok] for im in imgs)
    pass = 0; viol = 0; strip_boxes = 0; max_s_all = 0.0; max_s_strip = 0.0; strong_all = true
    for im in imgs
        im[:ok] || continue
        U, S = to_frame(N, im[:y], im[:z])
        ms = max(abs(inf(S)), abs(sup(S)))
        max_s_all = max(max_s_all, ms)
        inside_s = (inf(S) > -1 && sup(S) < 1)
        strong_all &= inside_s
        outside_u = sup(U) < -1 || inf(U) > 1
        if !outside_u
            strip_boxes += 1; max_s_strip = max(max_s_strip, ms)
        end
        (outside_u || inside_s) && (pass += 1)
        (inf(U) >= -1 && sup(U) <= 1 && (inf(S) >= 1 || sup(S) <= -1)) && (viol += 1)
    end
    status = (allok && pass == length(imgs)) ? "PASS" : (viol > 0 ? "CERTIFIED_FAILURE" : "UNDECIDED")
    oks = [im for im in imgs if im[:ok]]
    d = Dict{String,Any}("boxes_per_side" => n, "n_boxes" => length(imgs), "status" => status,
        "all_boxes_computed" => allok, "n_failed_boxes" => count(!im[:ok] for im in imgs),
        "failure_reasons" => unique([im[:reason] for im in imgs if !im[:ok]]),
        "n_pass" => pass, "n_certified_violations" => viol,
        "n_boxes_meeting_strip_|uN|<=1" => strip_boxes,
        "strong_form_all_boxes_|sN|<1" => (allok && strong_all),
        "max_|sN|_upper_bound_all_boxes" => max_s_all,
        "max_|sN|_upper_bound_strip_boxes" => max_s_strip,
        "margin_a_strip" => 1 - max_s_strip)
    if !isempty(oks)
        d["return_time_hull"] = fstr(reduce(hull, [im[:tret] for im in oks]))
        d["transversality_min_xdot"] = minimum(im[:xdot_min] for im in oks)
        d["image_y_hull"] = fstr(reduce(hull, [im[:y] for im in oks])); d["image_z_hull"] = fstr(reduce(hull, [im[:z] for im in oks]))
    end
    return d
end

function run_cover(M::HSet, N::HSet, label)
    levels = Any[]; decision = "UNDECIDED"; dlevel = nothing; how = "ladder exhausted (level 3)"
    for (L, (K, n)) in enumerate(LADDER)
        t = @elapsed begin
            b = check_b(M, N, K)
            # (a) only when (b) has not already been refuted with a certified failure
            a = b["status"] == "CERTIFIED_FAILURE" ? nothing : check_a(M, N, n)
        end
        push!(levels, Dict("level" => L, "b" => b, "a" => a, "seconds" => t))
        println(now(), "  ", label, "  level ", L, ": (b) ", b["status"], " orient ", b["orientation"],
                "  (a) ", a === nothing ? "-" : a["status"], "  [", round(t, digits=1), " s, images computed so far ", NCOMPUTED[], "]")
        flush(stdout)
        if b["status"] == "PASS" && a !== nothing && a["status"] == "PASS"
            decision = "CERTIFIED"; dlevel = L; how = "every piece of (a) and (b) certified at this level"; break
        elseif b["status"] == "CERTIFIED_FAILURE"
            decision = "REJECTED"; dlevel = L; how = "certified failure of (b) (both orientations refuted)"; break
        elseif a !== nothing && a["status"] == "CERTIFIED_FAILURE"
            decision = "REJECTED"; dlevel = L; how = "certified failure of (a) (an image enclosure inside {|u|<=1, |s|>=1})"; break
        end
    end
    if decision == "UNDECIDED"
        decision = "REJECTED"; how = "UNDECIDED at the top of the ladder (level 3)"; dlevel = nothing
    end
    return Dict("cover" => label, "decision" => decision, "decided_at_level" => dlevel, "how" => how, "levels" => levels)
end

hset_json(H::HSet) = Dict("centre" => string.(H.c), "A_columns_u_s" => [string.(H.A[:, 1]), string.(H.A[:, 2])],
                          "Ainv_rows" => [string.(H.Ainv[1, :]), string.(H.Ainv[2, :])])

function main(configs)
    specs = Dict(s => parse_spec(joinpath(SPECDIR, s * ".spec")) for s in SPECS)
    sha = Dict(s => bytes2hex(sha256(read(joinpath(SPECDIR, s * ".spec")))) for s in SPECS)
    for s in SPECS
        p = specs[s]["params"]; @assert p["a"] == 57 // 10 && p["b"] == 1 // 5
        @assert specs[s]["system"] == ["rossler"] && specs[s]["iter"] == ["2"]
    end
    Mb = specs["r1_ex_coneM"]["ex_cone_box"]; Nb = specs["r1_ex_coneN"]["ex_cone_box"]
    Mb = HSet("M", Mb.c, Mb.A, Mb.Ainv); Nb = HSet("N", Nb.c, Nb.A, Nb.Ainv)
    cfg = Dict{String,Any}()
    cfg["base"] = (Dict("M" => Mb, "N" => Nb), [("M", "M"), ("M", "N"), ("N", "M"), ("N", "N")], "r1_ex_coneM + r1_ex_coneN boxes, u = y, s = z")
    for (k, s) in (("W1", "r1_W1_swap"), ("W2", "r1_W2_rot90"), ("W3", "r1_W3_shrink"))
        cfg[k] = (specs[s]["tsets"], specs[s]["covers"], s)
    end
    checks = Dict{String,Any}()
    for k in ("W1", "W2", "W3")
        N = cfg[k][1]["N"]; checks["$(k)_N_equals_base_N"] = (N.c == Nb.c && N.A == Nb.A)
    end
    M1 = cfg["W1"][1]["M"]
    checks["W1_M_support_equals_base_M_support"] = (piece_rect(M1, -1, 1, -1, 1) == piece_rect(Mb, -1, 1, -1, 1))
    for k in keys(cfg), H in values(cfg[k][1]); @assert is_monomial(H.A); end
    results = Dict{String,Any}()
    t0 = time()
    for k in configs
        sets, covers, src = cfg[k]
        results[k] = Dict("source" => src, "tsets" => Dict(n => hset_json(H) for (n, H) in sets),
                          "covers" => [run_cover(sets[a], sets[b], "$k: $a => $b") for (a, b) in covers])
    end
    deps = Dict(string(v.name) => string(v.version) for (u, v) in Pkg.dependencies() if v.is_direct_dep)
    out = Dict("gate" => "Q1", "configs" => results, "consistency_checks" => checks, "spec_sha256" => sha,
        "map" => "P^2, section {x = 0, x' > 0} (CAPD MinusPlus), section coordinates (y, z)",
        "system" => "x' = -(y+z), y' = x + b y, z' = b + z (x - a), a = 57/10, b = 1/5 (exact, as constant extra states)",
        "ladder" => LADDER, "integrator" => Dict("method" => "TaylorModels.validated_integ", "orderQ" => ORDER_Q,
            "orderT" => ORDER_T, "abstol" => ABSTOL, "root_isolation_bisection_depth" => ROOT_DEPTH),
        "time_label_widening" => "eps_n = 4 n eps(tmax) on return times",
        "julia" => string(VERSION), "packages" => deps,
        "git_commit" => readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`),
        "images_computed" => NCOMPUTED[], "wall_seconds" => time() - t0, "finished" => string(now()))
    fn = joinpath(OUTDIR, length(configs) == 4 ? "q1_rossler.json" : "q1_rossler_$(join(configs, "_")).json")
    open(fn, "w") do f; JSON.print(f, out, 1); end
    println("wrote ", fn)
end


main(isempty(ARGS) ? ["base", "W1", "W2", "W3"] : ARGS)
