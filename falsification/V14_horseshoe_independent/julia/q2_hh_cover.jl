# V14 gate Q2 (HH, blind): Def. 2 coverings for AZ 2001's M0..M4 (eq. 5.1) and the wrong configurations W-AZ1/W-AZ2,
# on the QUALIFIED rigorous pipeline (B3t: validated_integ3, midrad = false, orderQ 2, adaptive refinement, threaded
# image prefetch). Mechanical adaptation of b3t_q1_cover.jl: system (q2_hh_poincare.jl, P1 on Θ1, coordinates
# (y, p_y)), specs (quantum's hh1_*.spec, read as INPUTS only), t-sets are general parallelograms (the source piece's
# axis-aligned hull is integrated: conservative), and AZ's special M3 sides (spec "special capL capR"):
# left = {u <= -1} ∪ {p_y >= capL}, right = {u >= 1} ∩ {p_y <= capR}; Def. 2(a) for a special target passes a box iff
# it lies in left ∪ right ∪ {|s|<1, u<1} ∪ {|s|<1, p_y<capR} (the spec semantics). For special targets, certified
# (a)-violations are not claimed (such a box counts as a failing leaf), and a (b) refutation needs the image to be
# certainly outside the side region. Decisions are committed BEFORE any quantum HH result is read.
using JSON, SHA, Dates, Pkg
include(joinpath(@__DIR__, "q2_hh_poincare.jl"))

const SPECDIR = "/Users/sumit/Github/quantum/qsim/capd/horseshoe_results"
const SPECS = ["hh1_M0M0", "hh1_M0M1", "hh1_M1M2", "hh1_M2M3", "hh1_M3M4", "hh1_M4M0", "hh1_M4M1",
                "hh1_W_AZ1_swap", "hh1_W_AZ2_shrink"]
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
    special::Bool
    capL::Rat
    capR::Rat
end
HSet(n, c, A, Ai) = HSet(n, c, A, Ai, false, Rat(0), Rat(0))
# Spec reading (stated in the report): "tset NAME c1 c2 U1 U2 S1 S2 I11 I12 I21 I22": centre (y, z), u-column U,
# s-column S, and the inverse of A = [U S] row-major. Verified exactly below (A * Ainv = I) for every tset.
function parse_spec(path)
    d = Dict{String,Any}("tsets" => Dict{String,HSet}(), "covers" => Tuple{String,String}[], "params" => Dict{String,Rat}())
    for ln in eachline(path)
        w = split(strip(ln)); isempty(w) && continue
        if w[1] == "param"
            d["params"][w[2]] = parse_rat(w[3])
        elseif w[1] == "tset"
            sp = findfirst(==("special"), w)
            v = parse_rat.(w[3:(sp === nothing ? end : sp - 1)]); @assert length(v) == 10
            A = [v[3] v[5]; v[4] v[6]]; Ai = [v[7] v[8]; v[9] v[10]]
            @assert A * Ai == [1 0; 0 1] "inverse check failed in $path"
            if sp === nothing
                d["tsets"][w[2]] = HSet(w[2], v[1:2], A, Ai)
            else
                d["tsets"][w[2]] = HSet(w[2], v[1:2], A, Ai, true, parse_rat(w[sp+1]), parse_rat(w[sp+2]))
            end
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
const CACHE_LOCK = ReentrantLock()     # B3t: threaded image prefetch (same images, computed in parallel)
function image_compute(rect::NTuple{4,Rat})
    Y = hull(ratI(rect[1]), ratI(rect[2])); Z = hull(ratI(rect[3]), ratI(rect[4]))
    r = p1_box(Y, Z)
    r[:rect] = string.(rect)
    r
end
function image(rect::NTuple{4,Rat})
    hit = lock(CACHE_LOCK) do; get(CACHE, rect, nothing); end
    hit === nothing || return hit
    r = image_compute(rect)
    lock(CACHE_LOCK) do
        haskey(CACHE, rect) && return CACHE[rect]
        NCOMPUTED[] += 1; CACHE[rect] = r
    end
end
function prefetch!(rects)
    todo = lock(CACHE_LOCK) do; unique([r for r in rects if !haskey(CACHE, r)]); end
    Threads.@threads :dynamic for r in todo
        image(r)
    end
    nothing
end

fstr(I) = [inf(I), sup(I)]


# ---- side tests (AZ special M3 sides; w = image p_y) ----
capLI(N::HSet) = ratI(N.capL); capRI(N::HSet) = ratI(N.capR)
in_left(N::HSet, U, W) = sup(U) < -1 || (N.special && inf(W) > sup(capLI(N)))
in_right(N::HSet, U, W) = inf(U) > 1 && (!N.special || sup(W) < inf(capRI(N)))
not_left(N::HSet, U, W) = inf(U) >= -1 && (!N.special || sup(W) <= inf(capLI(N)))
not_right(N::HSet, U, W) = sup(U) <= 1 || (N.special && inf(W) >= sup(capRI(N)))
function miss_F(N::HSet, U, S, W)
    s_in = inf(S) > -1 && sup(S) < 1
    N.special || return sup(U) < -1 || inf(U) > 1 || s_in
    return (s_in && sup(U) < 1) || in_left(N, U, W) || in_right(N, U, W) || (s_in && sup(W) < inf(capRI(N)))
end
violates_a(N::HSet, U, S) = !N.special && inf(U) >= -1 && sup(U) <= 1 && (inf(S) >= 1 || sup(S) <= -1)

# ---- condition (b) at one level ----
function check_b(M::HSet, N::HSet, K::Int)
    prefetch!(vcat(edge_pieces(M, -1, K), edge_pieces(M, 1, K)))
    imgs = Dict(side => [image(r) for r in edge_pieces(M, side, K)] for side in (-1, 1))
    fr = Dict(side => [im[:ok] ? (to_frame(N, im[:y], im[:z])..., im[:z]) : nothing for im in imgs[side]] for side in (-1, 1))
    allok = all(im[:ok] for side in (-1, 1) for im in imgs[side])
    L = fr[-1]; R = fr[1]
    okL(f, test) = f !== nothing && test(f)
    lft(f) = in_left(N, f[1], f[3]); rgt(f) = in_right(N, f[1], f[3])
    nlft(f) = not_left(N, f[1], f[3]); nrgt(f) = not_right(N, f[1], f[3])
    orient_p = allok && all(okL(f, lft) for f in L) && all(okL(f, rgt) for f in R)
    orient_m = allok && all(okL(f, rgt) for f in L) && all(okL(f, lft) for f in R)
    some(fs, test) = any(f !== nothing && test(f) for f in fs)
    refute_p = some(L, nlft) || some(R, nrgt)
    refute_m = some(L, nrgt) || some(R, nlft)
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
    prefetch!(support_boxes(M, n))
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
        miss_F(N, U, S, im[:z]) && (pass += 1)
        violates_a(N, U, S) && (viol += 1)
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


# ---------------------------------------------------------------- B2 refinement ----------------------------------
const MAXDEPTH = 6
const LEAF_CAP = 2^16
const Chart = NTuple{4,Rat}          # (u1, u2, s1, s2) in the source t-set's chart
image_chart(M::HSet, c::Chart) = image(piece_rect(M, c...))
function bisect(c::Chart)
    u1, u2, s1, s2 = c
    if u2 - u1 >= s2 - s1
        m = (u1 + u2) / 2; return ((u1, m, s1, s2), (m, u2, s1, s2))
    else
        m = (s1 + s2) / 2; return ((u1, u2, s1, m), (u1, u2, m, s2))
    end
end
# (b) leaf status for orientation σ: :pass, :refute (certainly on the wrong side), :fail
function b_status(M::HSet, N::HSet, c::Chart, σ::Int)
    side = Int(c[1])                               # u1 == u2 == ±1 for edge pieces
    im = image_chart(M, c)
    im[:ok] || return :fail
    U, _ = to_frame(N, im[:y], im[:z]); W = im[:z]
    wantleft = (σ == 1) == (side == -1)            # σ = +1: left edge -> left side; σ = -1: reversed
    if wantleft
        in_left(N, U, W) && return :pass
        not_left(N, U, W) && return :refute
    else
        in_right(N, U, W) && return :pass
        not_right(N, U, W) && return :refute
    end
    return :fail
end
function a_status(M::HSet, N::HSet, c::Chart)
    im = image_chart(M, c)
    im[:ok] || return :fail
    U, S = to_frame(N, im[:y], im[:z])
    miss_F(N, U, S, im[:z]) && return :pass
    violates_a(N, U, S) && return :violation
    return :fail
end
# Breadth-first refinement of the failing pieces `fails` (depth 0 = level-3 pieces) with status function `st`
# (:pass / :fail / anything else = certified contradiction). `leaves` is the running leaf count (Ref).
function refine!(fails::Vector{Chart}, st, leaves::Ref{Int}; pre = nothing)
    # Breadth-first, as before; `pre` (optional) prefetches the images of each new batch of children in parallel
    # before they are evaluated in the original queue order (same leaves, same decisions; only faster).
    queue = [(c, 0) for c in fails]; maxd = 0; nnew = 0; head = 1; fetched = 0
    while head <= length(queue)
        if pre !== nothing && head > fetched
            batch = [ch for (c, d) in queue[head:end] for ch in bisect(c)]
            pre(batch); fetched = length(queue)
        end
        c, d = queue[head]; head += 1
        d >= MAXDEPTH && return Dict("outcome" => "UNDECIDED", "reason" => "failing leaf at depth $MAXDEPTH", "leaf" => string.(c),
                                     "max_depth" => maxd, "new_pieces" => nnew, "unrefined_in_queue" => length(queue) - head + 1)
        leaves[] + 1 > LEAF_CAP && return Dict("outcome" => "UNDECIDED", "reason" => "leaf cap 2^16 reached", "max_depth" => maxd,
                                              "new_pieces" => nnew, "unrefined_in_queue" => length(queue) - head + 2)
        leaves[] += 1
        for ch in bisect(c)
            nnew += 1; maxd = max(maxd, d + 1)
            s = st(ch)
            s == :pass && continue
            s == :fail && (push!(queue, (ch, d + 1)); continue)
            return Dict("outcome" => "CONTRADICTION", "status" => string(s), "leaf" => string.(ch), "max_depth" => maxd, "new_pieces" => nnew)
        end
    end
    return Dict("outcome" => "ALL_LEAVES_PASS", "max_depth" => maxd, "new_pieces" => nnew)
end
level3_edges(K) = [(Rat(side), Rat(side), Rat(-1) + Rat(2(k - 1), K), Rat(-1) + Rat(2k, K)) for side in (-1, 1) for k in 1:K]
level3_boxes(n) = [(Rat(-1) + Rat(2(i - 1), n), Rat(-1) + Rat(2i, n), Rat(-1) + Rat(2(j - 1), n), Rat(-1) + Rat(2j, n)) for i in 1:n for j in 1:n]

function refine_cover(M::HSet, N::HSet, lev3)
    K, n = LADDER[end]
    t = @elapsed begin
        rec = Dict{String,Any}()
        b3 = lev3["b"]
        cands = [σ for σ in (1, -1) if !b3["refutes_orientation_$(σ == 1 ? "+1" : "-1")"]]
        rec["b_candidate_orientations"] = cands
        nbox = n^2
        borient = 0; bleaves = 0; bmaxd = 0; brec = Any[]
        for σ in cands
            edges = level3_edges(K)
            fails = Chart[]; refuted = false
            for c in edges
                s = b_status(M, N, c, σ)
                s == :refute && (refuted = true; break)
                s == :fail && push!(fails, c)
            end
            if refuted
                push!(brec, Dict("orientation" => σ, "outcome" => "REFUTED at level 3")); continue
            end
            leaves = Ref(2K + nbox)
            r = refine!(fails, c -> b_status(M, N, c, σ), leaves; pre = cs -> prefetch!([piece_rect(M, c...) for c in cs]))
            r["orientation"] = σ; r["level3_failing_edge_pieces"] = length(fails); r["edge_leaves"] = leaves[] - nbox
            push!(brec, r)
            if r["outcome"] == "ALL_LEAVES_PASS"
                borient = σ; bleaves = leaves[] - nbox; bmaxd = r["max_depth"]; break
            end
        end
        rec["b"] = brec
        if borient == 0
            allref = all(x -> x["outcome"] in ("REFUTED at level 3", "CONTRADICTION"), brec)
            rec["decision"] = allref ? "REJECTED" : "UNDECIDED"
            rec["how"] = allref ? "B2 refinement: certified failure of (b) (all candidate orientations refuted)" :
                                  "B2 refinement: (b) not certified within depth $MAXDEPTH / cap (a not refined)"
            rec["leaves"] = isempty(brec) ? 2K + nbox : maximum(get(x, "edge_leaves", 2K) for x in brec) + nbox
            rec["max_depth"] = maximum(get(x, "max_depth", 0) for x in brec; init = 0)
        else
            rec["b_orientation"] = borient
            fails = Chart[]; viol = nothing
            for c in level3_boxes(n)
                s = a_status(M, N, c)
                s == :violation && (viol = c; break)
                s == :fail && push!(fails, c)
            end
            if viol !== nothing
                rec["a"] = Dict("outcome" => "CONTRADICTION", "status" => "violation", "leaf" => string.(viol))
            else
                leaves = Ref(bleaves + nbox)
                ra = refine!(fails, c -> a_status(M, N, c), leaves; pre = cs -> prefetch!([piece_rect(M, c...) for c in cs]))
                ra["level3_failing_boxes"] = length(fails); ra["support_leaves"] = leaves[] - bleaves
                rec["a"] = ra
            end
            ra = rec["a"]
            rec["leaves"] = bleaves + get(ra, "support_leaves", nbox)
            rec["max_depth"] = max(bmaxd, get(ra, "max_depth", 0))
            if ra["outcome"] == "ALL_LEAVES_PASS"
                rec["decision"] = "CERTIFIED"; rec["how"] = "B2 refinement: every leaf of (a) and (b) certified"
            elseif ra["outcome"] == "CONTRADICTION"
                rec["decision"] = "REJECTED"; rec["how"] = "B2 refinement: certified failure of (a) (a leaf inside {|u|<=1, |s|>=1})"
            else
                rec["decision"] = "UNDECIDED"; rec["how"] = "B2 refinement: " * ra["reason"]
            end
        end
    end
    rec["seconds"] = t
    return rec
end

function run_cover_b2(M::HSet, N::HSet, label)
    levels = Any[]; decision = "UNDECIDED"; dlevel = nothing; how = "ladder exhausted (level 3)"
    for (L, (K, n)) in enumerate(LADDER)
        t = @elapsed begin
            b = check_b(M, N, K)
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
    out = Dict{String,Any}("cover" => label, "levels" => levels)
    if decision == "UNDECIDED"
        ref = refine_cover(M, N, levels[end])
        out["refinement"] = ref
        decision = ref["decision"]; how = ref["how"]; dlevel = "3+refinement"
        out["leaves"] = ref["leaves"]; out["max_depth"] = ref["max_depth"]
        println(now(), "  ", label, "  refinement: ", decision, "  leaves ", ref["leaves"], "  max depth ", ref["max_depth"],
                "  [", round(ref["seconds"], digits=1), " s, images computed so far ", NCOMPUTED[], "]  ", how)
        flush(stdout)
    else
        K, n = LADDER[dlevel]; out["leaves"] = 2K + n^2; out["max_depth"] = 0
    end
    out["decision"] = decision; out["decided_at_level"] = dlevel; out["how"] = how
    return out
end

hset_json(H::HSet) = Dict("centre" => string.(H.c), "A_columns_u_s" => [string.(H.A[:, 1]), string.(H.A[:, 2])],
                          "Ainv_rows" => [string.(H.Ainv[1, :]), string.(H.Ainv[2, :])],
                          "special" => H.special, "capL" => string(H.capL), "capR" => string(H.capR))

# Worker groups: coverings sharing a source set share its images (cache keyed by section rectangle).
const GROUPS = Dict(
    "A" => [("AZ", "M0", "M0"), ("AZ", "M0", "M1"), ("AZ", "M1", "M2"), ("W1", "M1", "M2"), ("W2", "M1", "M2"), ("AZ", "M2", "M3")],
    "C" => [("AZ", "M2", "M3")],
    "B" => [("AZ", "M3", "M4"), ("AZ", "M4", "M0"), ("AZ", "M4", "M1"), ("W1", "M2", "M3"), ("W2", "M2", "M3")])

function main_q2(group)
    specs = Dict(s => parse_spec(joinpath(SPECDIR, s * ".spec")) for s in SPECS)
    sha = Dict(s => bytes2hex(sha256(read(joinpath(SPECDIR, s * ".spec")))) for s in SPECS)
    for s in SPECS
        @assert specs[s]["system"] == ["hh"] && specs[s]["iter"] == ["1"] && specs[s]["params"]["level"] == 1 // 6
    end
    az = ["hh1_M0M0", "hh1_M0M1", "hh1_M1M2", "hh1_M2M3", "hh1_M3M4", "hh1_M4M0", "hh1_M4M1"]
    ref = specs[az[1]]["tsets"]
    for g in az, (n, H) in specs[g]["tsets"]       # every AZ spec defines the same M0..M4
        @assert ref[n].c == H.c && ref[n].A == H.A && ref[n].special == H.special && ref[n].capL == H.capL && ref[n].capR == H.capR
    end
    @assert [only(specs[g]["covers"]) for g in az] == [("M0","M0"),("M0","M1"),("M1","M2"),("M2","M3"),("M3","M4"),("M4","M0"),("M4","M1")]
    sets = Dict("AZ" => ref, "W1" => specs["hh1_W_AZ1_swap"]["tsets"], "W2" => specs["hh1_W_AZ2_shrink"]["tsets"])
    covs = Dict("AZ" => [only(specs[g]["covers"]) for g in az], "W1" => specs["hh1_W_AZ1_swap"]["covers"], "W2" => specs["hh1_W_AZ2_shrink"]["covers"])
    for (k, a, b) in GROUPS[group]; @assert (a, b) in covs[k] "$k $a => $b not a cover line"; end
    deps = Dict(string(v.name) => string(v.version) for (u, v) in Pkg.dependencies() if v.is_direct_dep)
    git = readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`)
    results = Dict{String,Any}(); t0 = time()
    fn = joinpath(OUTDIR, "q2_hh_$(group).json")
    for (k, a, b) in GROUPS[group]
        r = run_cover_b2(sets[k][a], sets[k][b], "$k: $a => $b")
        results["$k: $a => $b"] = r
        out = Dict("gate" => "Q2 (HH, blind)", "group" => group, "covers" => results, "spec_sha256" => sha,
            "tsets" => Dict(k => Dict(n => hset_json(H) for (n, H) in v) for (k, v) in sets),
            "map" => "P1 (iter 1), section Θ1 = {x = 0, x' > 0, H = 1/6}, coordinates (y, p_y); px from the energy (positive branch)",
            "ladder" => LADDER, "refinement" => Dict("max_depth_below_level3" => MAXDEPTH, "leaf_cap" => LEAF_CAP),
            "integrator" => Dict("method" => "TaylorModels.ValidatedInteg.validated_integ3", "orderQ" => ORDER_Q,
                "orderT" => ORDER_T, "abstol" => ABSTOL, "maxsteps" => MAXSTEPS, "midrad" => B3_MIDRAD),
            "threads" => Threads.nthreads(), "julia" => string(VERSION), "packages" => deps, "git_commit" => git,
            "images_computed" => NCOMPUTED[], "wall_seconds" => time() - t0, "complete" => length(results) == length(GROUPS[group]),
            "updated" => string(now()))
        open(fn * ".tmp", "w") do f; JSON.print(f, out, 1); end
        mv(fn * ".tmp", fn; force = true)
    end
    println("wrote ", fn)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main_q2(only(ARGS))
end
