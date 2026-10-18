# V14 gate Q2 helper: validated first-return Poincaré map P1 for Hénon–Heiles on Θ1 = {x = 0, ẋ > 0, H = 1/6},
# coordinates (y, p_y), built exactly as the qualified Rössler pipeline (b3_poincare.jl: validated_integ3,
# midrad = false, orderQ 2, interval root isolation, certified transversality, ε_n time-label widening), with:
#   - H = (px^2 + py^2)/2 + (x^2 + y^2)/2 + x^2 y − y^3/3 (AZ 2001 eq. 1.1), state (x, y, px, py);
#   - the eliminated momentum px on Θ1 enclosed from the energy (S9 analogue): px = +sqrt(2h − py^2 − y^2 + 2y^3/3)
#     on the positive branch, the radicand certified > 0 on the whole initial box (else the piece FAILS closed);
#   - transversality: ẋ = px, certified > 0 on every retained crossing subinterval;
#   - iterate 1 (first upcrossing after departure), as in quantum's hh1 specs ("iter 1");
#   - the S9 output check: H evaluated on the image enclosure (x, y, px, py at the crossing) must contain h.
# The initial set is the axis-aligned hull of the source piece (conservative: images of a superset).
include(joinpath(@__DIR__, "b3_rigor.jl"))

function hh!(dx, x, p, t)
    dx[1] = x[3]; dx[2] = x[4]
    dx[3] = -x[1] - 2 * x[1] * x[2]
    dx[4] = -x[2] - x[1] * x[1] + x[2] * x[2]
    nothing
end

const ORDER_Q = B3_ORDER_Q
const ORDER_T = B3_ORDER_T
const ABSTOL = B3_ABSTOL
const MAXSTEPS = B3_MAXSTEPS
const SP = JetSpace(2 * ORDER_Q, ["ξ1", "ξ2", "ξ3", "ξ4"])
const ROOT_DEPTH = 10

ratI(r::Rational) = interval(Float64, r)
const HLEV = ratI(1 // 6)

# non-rigorous RK4 estimate of the first return time (only to choose tmax)
function est_t1(y0::Float64, py0::Float64; dt = 1e-3, tcap = 40.0)
    r = 2 * (1 / 6) - py0^2 - y0^2 + 2 * y0^3 / 3
    r <= 0 && return NaN
    f(u) = (u[3], u[4], -u[1] - 2u[1] * u[2], -u[2] - u[1]^2 + u[2]^2)
    u = (0.0, y0, sqrt(r), py0); t = 0.0
    while t < tcap
        k1 = f(u); k2 = f(u .+ (dt / 2) .* k1); k3 = f(u .+ (dt / 2) .* k2); k4 = f(u .+ dt .* k3)
        un = u .+ (dt / 6) .* (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4)
        if t > 0.5 && u[1] < 0 && un[1] >= 0
            return t + dt * (-u[1]) / (un[1] - u[1])
        end
        u = un; t += dt
    end
    return NaN
end

struct StepEval
    C::Vector{Vector{Interval{Float64}}}   # i = 1..4: x, y, px, py   (ẋ = px = component 3)
    R::Vector{Interval{Float64}}
    h::Float64
    t0::Float64
end
coeff_encl(tm, box) = coeff_ranges3(tm, box)
function horner(C::Vector{Interval{Float64}}, δt::Interval{Float64})
    acc = interval(0.0)
    for k in length(C):-1:1
        acc = acc * δt + C[k]
    end
    return acc
end
function step_evals(sol)
    xTM = get_xTM(sol); tv = expansion_point(sol)
    box = collect(symmetric_box(4))
    out = StepEval[]
    for n in 2:lastindex(sol)
        tms = [xTM[i, n] for i in 1:4]
        dom = domain(xTM[1, n]); @assert inf(dom) == 0.0
        push!(out, StepEval([coeff_encl(tm, box) for tm in tms], [remainder(tm) for tm in tms], sup(dom), tv[n]))
    end
    return out
end
val(se::StepEval, i::Int, δt::Interval{Float64}) = horner(se.C[i], δt) + se.R[i]

function isolate_zeros(se::StepEval)
    keep = Interval{Float64}[]
    stack = [(interval(0.0, se.h), 0)]
    while !isempty(stack)
        D, d = pop!(stack)
        in_interval(0.0, val(se, 1, D)) || continue
        if d >= ROOT_DEPTH
            push!(keep, D)
        else
            m = (inf(D) + sup(D)) / 2
            push!(stack, (interval(inf(D), m), d + 1)); push!(stack, (interval(m, sup(D)), d + 1))
        end
    end
    return keep
end
sgn(I::Interval{Float64}) = inf(I) > 0 ? 1 : (sup(I) < 0 ? -1 : 0)

henergy(x, y, px, py) = (px * px + py * py) / interval(2.0) + (x * x + y * y) / interval(2.0) + x * x * y - y * y * y / interval(3.0)

# Validated P1 on an initial section box {x = 0} × Y × PY. Returns :ok, :reason, :y, :z (= p_y image), :tret, ...
function poincare1(Y::Interval{Float64}, PY::Interval{Float64}; tmax::Float64)
    rad = interval(2.0) * HLEV - PY * PY - Y * Y + interval(2.0) * Y * Y * Y / interval(3.0)
    inf(rad) > 0 || return Dict(:ok => false, :reason => "px_radicand_not_positive")
    PX = sqrt(rad)
    X0 = [interval(0.0), Y, PX, PY]
    for v in X0
        m = BigFloat(mid(v)); r = BigFloat(radius(v))
        (m - r <= BigFloat(inf(v)) && m + r >= BigFloat(sup(v))) || return Dict(:ok => false, :reason => "init_poly_cover")
    end
    sol = try
        b3_integ(hh!, X0, 0.0, tmax, SP)
    catch err
        (err isa UndefVarError && err.var == :t0) || rethrow()
        return Dict(:ok => false, :reason => "step_validation_failed_to_zero_step (package UndefVarError t0)")
    end
    lastindex(sol) < 2 && return Dict(:ok => false, :reason => "no_validated_step")
    tdrift3(sol) == 0.0 || return Dict(:ok => false, :reason => "time_labels_not_exact")
    ses = step_evals(sol)
    tend = ses[end].t0 + ses[end].h
    nst = length(ses)
    tend < tmax * (1 - 1e-12) && return Dict(:ok => false, :reason => "integration_stopped_at_t=$(tend)", :nsteps => nst)
    xr = [val(se, 1, interval(0.0, se.h)) for se in ses]
    j = 1
    while j <= nst && in_interval(0.0, xr[j])
        sgn(val(ses[j], 3, interval(0.0, ses[j].h))) == 1 || return Dict(:ok => false, :reason => "departure_not_transversal", :nsteps => nst)
        j += 1
    end
    j > nst && return Dict(:ok => false, :reason => "departure_window_not_closed", :nsteps => nst)
    sgn(xr[j]) == 1 || return Dict(:ok => false, :reason => "departure_inconsistent", :nsteps => nst)
    while j <= nst
        if !in_interval(0.0, xr[j]); j += 1; continue; end
        k = j
        while k <= nst && in_interval(0.0, xr[k]); k += 1; end
        k > nst && return Dict(:ok => false, :reason => "window_not_closed_by_tmax", :nsteps => nst)
        sb = sgn(xr[j-1]); sa = sgn(xr[k])
        retained = Tuple{Int,Interval{Float64}}[]
        for m in j:k-1, D in isolate_zeros(ses[m])
            push!(retained, (m, D))
        end
        if isempty(retained)
            sb == sa || return Dict(:ok => false, :reason => "sign_change_without_zero", :nsteps => nst)
            j = k; continue
        end
        σs = Int[]; xd_lo = Inf
        for (m, D) in retained
            xd = val(ses[m], 3, D); s = sgn(xd)
            s == 0 && return Dict(:ok => false, :reason => "transversality_not_certified", :nsteps => nst)
            push!(σs, s); xd_lo = min(xd_lo, s == 1 ? inf(xd) : -sup(xd))
        end
        all(==(σs[1]), σs) || return Dict(:ok => false, :reason => "mixed_crossing_directions", :nsteps => nst)
        σ = σs[1]
        if sb == sa
            j = k; continue
        end
        (sb, sa) == (-σ, σ) || return Dict(:ok => false, :reason => "direction_inconsistent", :nsteps => nst)
        if σ == 1          # first upcrossing after departure = P1
            yI = reduce(hull, [val(ses[m], 2, D) for (m, D) in retained])
            pyI = reduce(hull, [val(ses[m], 4, D) for (m, D) in retained])
            xI = reduce(hull, [val(ses[m], 1, D) for (m, D) in retained])
            pxI = reduce(hull, [val(ses[m], 3, D) for (m, D) in retained])
            HI = henergy(xI, yI, pxI, pyI)
            in_interval(1 / 6, HI) || return Dict(:ok => false, :reason => "S9_energy_not_contained", :nsteps => nst)
            tI = reduce(hull, [interval(ses[m].t0) + D + interval(-tlabel_widen(m + 1, tmax), tlabel_widen(m + 1, tmax)) for (m, D) in retained])
            return Dict(:ok => true, :reason => "ok", :y => yI, :z => pyI, :tret => tI, :nsteps => nst,
                        :xdot_min => xd_lo, :n_retained => length(retained), :H_width => diam(HI))
        end
        j = k
    end
    return Dict(:ok => false, :reason => "first_upcrossing_not_reached", :nsteps => nst)
end

# Driver for one initial box (Y, PY); tmax from the float estimate (+0.5), one retry (+1.5).
function p1_box(Y, PY)
    t1 = est_t1(mid(Y), mid(PY))
    isnan(t1) && return Dict(:ok => false, :reason => "no_float_return_estimate")
    r = poincare1(Y, PY; tmax = t1 + 0.5)
    if !r[:ok] && (r[:reason] in ("window_not_closed_by_tmax", "first_upcrossing_not_reached"))
        r = poincare1(Y, PY; tmax = t1 + 1.5)
    end
    r[:t1_est] = t1
    return r
end
