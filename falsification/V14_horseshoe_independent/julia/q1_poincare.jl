# V14 gate Q1 helper: validated second-return Poincaré map P^2 for Rössler on the section {x = 0, x' > 0},
# built from TaylorModels.jl's validated flowpipe, per the V14 pre-registration:
#   - per Taylor-model step, the section function x is bounded over the whole step (rig_eval);
#   - crossing times are enclosed by interval root isolation (bisection on the step's time polynomial + remainder);
#   - transversality (grad(x) . f = x' = -(y + z) excludes 0) is certified on every retained crossing subinterval,
#     else the piece FAILS closed;
#   - the image is the flowpipe evaluated on the crossing-time enclosure (hull over the retained subintervals).
# Parameters (b = 1/5, a = 57/10, spec naming) enter as constant extra states with boxes enclosing the exact
# rationals (the Q0 lesson). Return times carry the ε_n time-label widening (FINDINGS, Q0).
using TaylorModels, TaylorIntegration, IntervalArithmetic
using TaylorModels.ValidatedInteg
include(joinpath(@__DIR__, "v14_rigor.jl"))

# Rössler, spec naming: x' = -(y + z), y' = x + b y, z' = b + z (x - a); x[4] = b, x[5] = a.
function rossler!(dx, x, p, t)
    dx[1] = -(x[2] + x[3]); dx[2] = x[1] + x[4]*x[2]; dx[3] = x[4] + x[3]*(x[1] - x[5])
    dx[4] = zero(x[4]); dx[5] = zero(x[5]); nothing
end

const ORDER_Q = 2
const ORDER_T = 16
const ABSTOL = 1e-20
const MAXSTEPS = 20000
const SP = JetSpace(2*ORDER_Q, ["ξ1", "ξ2", "ξ3", "ξ4", "ξ5"])
const ROOT_DEPTH = 10            # bisection depth for crossing-time isolation within one step

# Rigorous Float64 interval enclosing a rational.
ratI(r::Rational) = interval(Float64, r)

# ---------- non-rigorous float estimate of the 2nd upcrossing time (only used to choose tmax) ----------
function est_t2(y0::Float64, z0::Float64, b::Float64, a::Float64; dt=1e-3, tcap=40.0)
    f(u) = (-(u[2] + u[3]), u[1] + b*u[2], b + u[3]*(u[1] - a))
    u = (0.0, y0, z0); t = 0.0; ups = 0
    while t < tcap
        k1 = f(u); k2 = f(u .+ (dt/2) .* k1); k3 = f(u .+ (dt/2) .* k2); k4 = f(u .+ dt .* k3)
        un = u .+ (dt/6) .* (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4)
        if t > 0.1 && u[1] < 0 && un[1] >= 0
            ups += 1
            ups == 2 && return t + dt * (-u[1]) / (un[1] - u[1])
        end
        u = un; t += dt
    end
    return NaN
end

# ---------- per-step coefficient enclosures (equivalent to rig_eval, cached) ----------
# For TM xTM[i, n]: C[k] = evaluate(coeff_k (as interval TaylorN), box); value at δt is Horner(C, δt) + rem.
# This is rig_eval with the coefficient enclosures computed once per step (identical result).
struct StepEval
    C::Vector{Vector{Interval{Float64}}}   # C[i][k], i = 1..3 (x, y, z), plus i = 4 for x' = -(y + z)
    R::Vector{Interval{Float64}}
    h::Float64                              # step length (domain sup)
    t0::Float64                             # package time label of step start
end
function coeff_encl(tm, box)
    c = polynomial(tm).coeffs
    return [evaluate(ck * interval(1.0), box) for ck in c]
end
function horner(C::Vector{Interval{Float64}}, δt::Interval{Float64})
    acc = interval(0.0)
    for k in length(C):-1:1
        acc = acc * δt + C[k]
    end
    return acc
end
function step_evals(sol)
    xTM = get_xTM(sol); tv = expansion_point(sol)
    box = collect(symmetric_box(5))
    out = StepEval[]
    for n in 2:lastindex(sol)
        tms = [xTM[i, n] for i in 1:3]
        Cx, Cy, Cz = (coeff_encl(tm, box) for tm in tms)
        # x' = -(y + z): combine the TaylorN coefficients first (interval sums), then enclose on the box.
        cy = polynomial(tms[2]).coeffs; cz = polynomial(tms[3]).coeffs
        Cxd = [evaluate(-(cy[k]*interval(1.0) + cz[k]*interval(1.0)), box) for k in eachindex(cy)]
        R = [remainder(tm) for tm in tms]
        Rxd = -(R[2] + R[3])
        # Transversality uses the vector field on the flowpipe enclosure: x' = -(y + z) at the enclosed state.
        dom = domain(xTM[1, n])
        push!(out, StepEval([Cx, Cy, Cz, Cxd], [R[1], R[2], R[3], Rxd], sup(dom), tv[n]))
    end
    return out
end
val(se::StepEval, i::Int, δt::Interval{Float64}) = horner(se.C[i], δt) + se.R[i]

# Retained crossing subintervals of one step: bisection of [0, h], keeping subintervals where 0 ∈ x-enclosure.
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

# Validated P^2 on an initial section box {x = 0} × Y × Z (Y, Z rigorous Float64 intervals).
# Returns a Dict with :ok, :reason, :y, :z (image enclosures), :tret (widened), :nsteps, :xdot_min.
function poincare2(Y::Interval{Float64}, Z::Interval{Float64}, PB::Interval{Float64}, PA::Interval{Float64};
                   tmax::Float64)
    X0 = [interval(0.0), Y, Z, PB, PA]
    # The package builds the initial polynomial as mid + rad*ξ in Float64; check it covers each X0[i] exactly.
    for v in X0
        m = BigFloat(mid(v)); r = BigFloat(radius(v))
        (m - r <= BigFloat(inf(v)) && m + r >= BigFloat(sup(v))) || return Dict(:ok => false, :reason => "init_poly_cover")
    end
    sol = validated_integ(rossler!, X0, 0.0, tmax, ORDER_Q, ORDER_T, ABSTOL, SP; maxsteps=MAXSTEPS)
    ses = step_evals(sol)
    tend = ses[end].t0 + ses[end].h
    nst = length(ses)
    if tend < tmax * (1 - 1e-12)
        return Dict(:ok => false, :reason => "integration_stopped_at_t=$(tend)", :nsteps => nst)
    end
    xr = [val(se, 1, interval(0.0, se.h)) for se in ses]     # x over each whole step
    # --- departure window: steps from the first, while 0 ∈ x-range; need x' > 0 on all of them.
    j = 1
    while j <= nst && in_interval(0.0, xr[j])
        sgn(val(ses[j], 4, interval(0.0, ses[j].h))) == 1 || return Dict(:ok => false, :reason => "departure_not_transversal", :nsteps => nst)
        j += 1
    end
    j > nst && return Dict(:ok => false, :reason => "departure_window_not_closed", :nsteps => nst)
    sgn(xr[j]) == 1 || return Dict(:ok => false, :reason => "departure_inconsistent", :nsteps => nst)
    ups = 0; xdmin = Inf
    while j <= nst
        if !in_interval(0.0, xr[j]); j += 1; continue; end
        # window [j, k]
        k = j
        while k <= nst && in_interval(0.0, xr[k]); k += 1; end
        k > nst && return Dict(:ok => false, :reason => "window_not_closed_by_tmax", :nsteps => nst, :ups => ups)
        sb = sgn(xr[j-1]); sa = sgn(xr[k])           # strict signs just before / after the window
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
            xd = val(ses[m], 4, D); s = sgn(xd)
            s == 0 && return Dict(:ok => false, :reason => "transversality_not_certified", :nsteps => nst, :ups => ups)
            push!(σs, s); xd_lo = min(xd_lo, s == 1 ? inf(xd) : -sup(xd))
        end
        all(==(σs[1]), σs) || return Dict(:ok => false, :reason => "mixed_crossing_directions", :nsteps => nst)
        σ = σs[1]
        if sb == sa
            j = k; continue                          # monotone on zero set, same end signs: no crossing
        end
        (sb, sa) == (-σ, σ) || return Dict(:ok => false, :reason => "direction_inconsistent", :nsteps => nst)
        if σ == 1
            ups += 1
            if ups == 2
                yI = reduce(hull, [val(ses[m], 2, D) for (m, D) in retained])
                zI = reduce(hull, [val(ses[m], 3, D) for (m, D) in retained])
                tI = reduce(hull, [interval(ses[m].t0) + D + interval(-tlabel_widen(m + 1, tmax), tlabel_widen(m + 1, tmax)) for (m, D) in retained])
                return Dict(:ok => true, :reason => "ok", :y => yI, :z => zI, :tret => tI, :nsteps => nst,
                            :xdot_min => xd_lo, :n_retained => length(retained))
            end
        end
        j = k
    end
    return Dict(:ok => false, :reason => "second_upcrossing_not_reached", :nsteps => nst, :ups => ups)
end

# Driver for one initial box with tmax from the float estimate (+0.5), one retry (+1.5) if the window is open.
function p2_box(Y, Z, PB, PA)
    t2 = est_t2(mid(Y), mid(Z), 0.2, 5.7)
    isnan(t2) && return Dict(:ok => false, :reason => "no_float_return_estimate")
    r = poincare2(Y, Z, PB, PA; tmax = t2 + 0.5)
    if !r[:ok] && (r[:reason] in ("window_not_closed_by_tmax", "second_upcrossing_not_reached"))
        r = poincare2(Y, Z, PB, PA; tmax = t2 + 1.5)
    end
    r[:t2_est] = t2
    return r
end
