# V14 Amendment B3 (PREREGISTRATION.md, "Amendment B3"): Q1 re-qualification on the rigorous pipeline with
#   (1) adaptive refinement below ladder level 3, (2) orderQ = 2 (b3_rigor.jl; B3 keeps the B1 order), (3) pivoted QR: dropped (not in the
#   pinned package). Lines up to check_a are copied verbatim from b1_q1_cover.jl (only the include changed); the
#   ladder (run_cover_b2, levels 1-3) is B1's run_cover unchanged; refinement and the worker driver are new.
#
# Refinement rules (stated here before any B2 covering result; B2 text: "Any support box or edge piece that fails
# validation or a check is bisected (in its longer side, in the t-set's (u, s) chart), recursively to depth <= 6 below
# the level-3 ladder, with a cap of 2^16 leaves per covering. A covering is CERTIFIED only if every leaf certifies."):
#  - Applied only to coverings still UNDECIDED after ladder level 3; it starts from the level-3 pieces.
#  - Pieces live in the SOURCE t-set's (u, s) chart, rect [u1,u2] x [s1,s2]. Bisection at the midpoint of the longer
#    chart side; ties split u. Edge pieces (u fixed at -1 or +1) therefore always split s.
#  - (b): the candidate orientations are those NOT refuted at level 3 (an orientation is refuted by any computed
#    piece whose enclosure lies certainly on the wrong side, as in check_b). Each candidate is refined separately; a
#    leaf passes for orientation σ iff its image is computed and lies strictly on the required side. A leaf that
#    refutes σ kills σ. (b) is certified iff some candidate has every leaf passing. If no candidate is left: REJECTED
#    (certified failure of (b)).
#  - (a): a leaf passes iff its image is computed and (sup|u| side: outside {|u_N| <= 1}) or |s_N| < 1, as check_a.
#    A leaf inside {|u_N| <= 1, |s_N| >= 1} (certified violation) makes the covering REJECTED.
#  - (b) is refined first. If (b) cannot be certified, (a) is not refined and the covering is UNDECIDED.
#  - Breadth-first by depth. A failing leaf at depth 6 makes the covering UNDECIDED (refinement stops there). The
#    leaf count is the size of the final partition of the (b) edge pieces (for the candidate being refined) plus the
#    (a) support boxes; starting at 2*128 + 64^2 = 4352. A bisection that would exceed 2^16 leaves stops refinement:
#    UNDECIDED (cap).
#  - Images are the same validated P^2 enclosures (b3_poincare.jl), cached by section rectangle (shared between
#    coverings in a worker).
# Usage: julia --project=julia julia/b3_q1_cover.jl GROUP   (GROUP = N or M; see GROUPS below)
using JSON, SHA, Dates, Pkg
include(joinpath(@__DIR__, "b3_poincare.jl"))

const SPECDIR = "/Users/sumit/Github/quantum/qsim/capd/horseshoe_results"
const SPECS = ["r1_ex_coneM", "r1_ex_coneN", "r1_generic_MM", "r1_generic_MN", "r1_generic_NM", "r1_generic_NN",
                "r1_W1_swap", "r1_W2_rot90", "r1_W3_shrink"]
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
    U, _ = to_frame(N, im[:y], im[:z])
    wantleft = (σ == 1) == (side == -1)            # σ = +1: left edge -> left side; σ = -1: reversed
    if wantleft
        sup(U) < -1 && return :pass
        inf(U) >= -1 && return :refute
    else
        inf(U) > 1 && return :pass
        sup(U) <= 1 && return :refute
    end
    return :fail
end
function a_status(M::HSet, N::HSet, c::Chart)
    im = image_chart(M, c)
    im[:ok] || return :fail
    U, S = to_frame(N, im[:y], im[:z])
    (sup(U) < -1 || inf(U) > 1 || (inf(S) > -1 && sup(S) < 1)) && return :pass
    (inf(U) >= -1 && sup(U) <= 1 && (inf(S) >= 1 || sup(S) <= -1)) && return :violation
    return :fail
end
# Breadth-first refinement of the failing pieces `fails` (depth 0 = level-3 pieces) with status function `st`
# (:pass / :fail / anything else = certified contradiction). `leaves` is the running leaf count (Ref).
function refine!(fails::Vector{Chart}, st, leaves::Ref{Int})
    queue = [(c, 0) for c in fails]; maxd = 0; nnew = 0; head = 1
    while head <= length(queue)
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
            r = refine!(fails, c -> b_status(M, N, c, σ), leaves)
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
                ra = refine!(fails, c -> a_status(M, N, c), leaves)
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
                          "Ainv_rows" => [string.(H.Ainv[1, :]), string.(H.Ainv[2, :])])

# Worker groups, cheapest first (coordinator's order): N-source coverings share the N images; the M group runs
# M => N and the cheap W rejections before M => M and W2 M' => N.
const GROUPS = Dict(
    "N" => [("base", "N", "M"), ("base", "N", "N"), ("W1", "N", "M"), ("W1", "N", "N"), ("W2", "N", "M"), ("W2", "N", "N"),
            ("W3", "N", "M"), ("W3", "N", "N")],
    "M" => [("base", "M", "N"), ("W1", "M", "M"), ("W1", "M", "N"), ("W3", "M", "M"), ("W3", "M", "N"), ("W2", "M", "M"),
            ("base", "M", "M"), ("W2", "M", "N")])

function main_b2(group)
    specs = Dict(s => parse_spec(joinpath(SPECDIR, s * ".spec")) for s in SPECS)
    sha = Dict(s => bytes2hex(sha256(read(joinpath(SPECDIR, s * ".spec")))) for s in SPECS)
    for s in SPECS
        p = specs[s]["params"]; @assert p["a"] == 57 // 10 && p["b"] == 1 // 5
        @assert specs[s]["system"] == ["rossler"] && specs[s]["iter"] == ["2"]
    end
    Mb = specs["r1_ex_coneM"]["ex_cone_box"]; Nb = specs["r1_ex_coneN"]["ex_cone_box"]
    gen = ["r1_generic_MM", "r1_generic_MN", "r1_generic_NM", "r1_generic_NN"]
    gM = specs[gen[1]]["tsets"]["M"]; gN = specs[gen[1]]["tsets"]["N"]
    for g in gen
        @assert specs[g]["tsets"]["M"].c == gM.c && specs[g]["tsets"]["M"].A == gM.A && specs[g]["tsets"]["N"].c == gN.c && specs[g]["tsets"]["N"].A == gN.A
    end
    @assert gM.c == Mb.c && gM.A == Mb.A && gN.c == Nb.c && gN.A == Nb.A
    @assert [only(specs[g]["covers"]) for g in gen] == [("M", "M"), ("M", "N"), ("N", "M"), ("N", "N")]
    sets = Dict("base" => Dict("M" => gM, "N" => gN))
    covs = Dict("base" => [("M", "M"), ("M", "N"), ("N", "M"), ("N", "N")])
    for (k, s) in (("W1", "r1_W1_swap"), ("W2", "r1_W2_rot90"), ("W3", "r1_W3_shrink"))
        sets[k] = specs[s]["tsets"]; covs[k] = specs[s]["covers"]
    end
    for (k, a, b) in GROUPS[group]; @assert (a, b) in covs[k] "$k $a => $b not a cover line"; end
    deps = Dict(string(v.name) => string(v.version) for (u, v) in Pkg.dependencies() if v.is_direct_dep)
    git = readchomp(`git -C /Users/sumit/Github/TheBridge rev-parse HEAD`)
    results = Dict{String,Any}(); t0 = time()
    fn = joinpath(OUTDIR, "b3_q1_$(group).json")
    for (k, a, b) in GROUPS[group]
        r = run_cover_b2(sets[k][a], sets[k][b], "$k: $a => $b")
        results["$k: $a => $b"] = r
        out = Dict("gate" => "Q1 (B2 re-qualification)", "group" => group, "covers" => results, "spec_sha256" => sha,
            "tsets" => Dict(k => Dict(n => hset_json(H) for (n, H) in v) for (k, v) in sets),
            "map" => "P^2, section {x = 0, x' > 0}, section coordinates (y, z); confirmed by quantum as a spec fact",
            "ladder" => LADDER, "refinement" => Dict("max_depth_below_level3" => MAXDEPTH, "leaf_cap" => LEAF_CAP,
                "bisection" => "midpoint of the longer side of the source (u, s) chart rect; ties split u"),
            "integrator" => Dict("method" => "TaylorModels.ValidatedInteg.validated_integ3", "orderQ" => ORDER_Q,
                "orderT" => ORDER_T, "abstol" => ABSTOL, "maxsteps" => MAXSTEPS, "midrad" => B3_MIDRAD,
                "jetspace_order" => 2 * ORDER_Q, "root_isolation_bisection_depth" => ROOT_DEPTH,
                "pivoted_QR" => "dropped: not available in TaylorModels 0.13.1 (qrprecondition.jl:224, qr(Amid) unpivoted)"),
            "julia" => string(VERSION), "packages" => deps, "git_commit" => git,
            "images_computed" => NCOMPUTED[], "wall_seconds" => time() - t0, "complete" => length(results) == length(GROUPS[group]),
            "updated" => string(now()))
        open(fn * ".tmp", "w") do f; JSON.print(f, out, 1); end
        mv(fn * ".tmp", fn; force = true)
    end
    println("wrote ", fn)
end

main_b2(only(ARGS))
