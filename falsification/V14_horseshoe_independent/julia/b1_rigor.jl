# V14 Amendment B1 shared helper: the fixed (rigorous) integration step and its evaluation.
#
# B1 option 1, as found feasible in the pinned TaylorModels 0.13.1 (see results/b1_note.md):
#   `validated_integ3` (same package, same version) validates each step with an interval Picard operator:
#   the Float64 Taylor polynomial p1 from TaylorIntegration is only a candidate; it is copied exactly into
#   Interval{Float64} coefficients, f! is evaluated in TaylorModel1{TaylorModelN{Interval{Float64}}} arithmetic
#   (every coefficient operation is an interval operation; neglected sigma-degrees above orderQ are bounded into
#   the TaylorModelN remainders), and the self-map test is  Δ2 + R(p2 - p1) ⊆ Δ1,  with R an interval-Horner range
#   of the difference between the interval Picard image p2 and the stored Float64 polynomial p1. So every rounding
#   of the Float64 polynomial is inside the stored remainder. Steps are exactly representable (t_k + h_k exact),
#   and the step-to-step transfer is a rigorous QR (Lohner) preconditioning with verified inverses.
#   Pre-stated choice (made before any B1 Q1 result): `midrad = false`, i.e. the products use the generic
#   IntervalArithmetic.jl directed-rounding operations, not the package's midpoint-radius kernel. This is the
#   literal B1 reading ("every coefficient operation is enclosed" by interval arithmetic). Q0 is also recorded with
#   the package default (`midrad = true`) as data.
#
# The stored solution xTM[i, k] is a TaylorModel1 in τ ∈ [0, h_k] whose coefficients are TaylorModelN (Float64
# polynomial + interval remainder) in σ ∈ [-1, 1]^5, plus an interval remainder. The state set at time t_k + τ is
# enclosed by { p(τ, σ) + Δ : σ ∈ B } (a set enclosure; σ is not the original ξ after step 1).
using TaylorModels, TaylorIntegration, IntervalArithmetic, TaylorSeries
using TaylorModels.ValidatedInteg
include(joinpath(@__DIR__, "v14_rigor.jl"))     # tlabel_widen (the Q0 time-label rule, kept)

const B1_ORDER_Q = 2
const B1_ORDER_T = 16
const B1_ABSTOL = 1e-20
const B1_MAXSTEPS = 20000
const B1_MIDRAD = false

b1_integ(f!, X0, t0, tmax, sp; midrad::Bool = B1_MIDRAD) =
    validated_integ3(f!, X0, t0, tmax, B1_ORDER_Q, B1_ORDER_T, B1_ABSTOL, sp; maxsteps = B1_MAXSTEPS, midrad = midrad)

# Rigorous range of one TaylorModelN coefficient over σ ∈ B: interval evaluation of its (exact Float64)
# polynomial on the box, plus its remainder.
function tmn_range(c, box::Vector{Interval{Float64}})
    return evaluate(polynomial(c) * interval(1.0), box) + remainder(c)
end
coeff_ranges3(tm, box) = [tmn_range(tm[k], box) for k in 0:TaylorSeries.order(polynomial(tm))]

# Interval Horner over the time offset δt (must lie in the step's validated domain [0, h]), plus the TM1 remainder.
function rig_eval3(tm, δt::Interval{Float64})
    issubset_interval(δt, domain(tm)) || error("rig_eval3: δt = $δt outside the validated domain $(domain(tm))")
    box = collect(symmetric_box(length(tm[0].pol.coeffs[2].coeffs), Float64))
    C = coeff_ranges3(tm, box)
    acc = interval(0.0)
    for k in length(C):-1:1
        acc = acc * δt + C[k]
    end
    return acc + remainder(tm)
end

# Time labels: validated_integ3 makes every step exactly representable. This returns max |label_k - Σ_{j<k} h_j|
# computed in BigFloat (0 means the labels are exact elapsed times).
function tdrift3(sol)
    xTM = get_xTM(sol); tv = expansion_point(sol)
    s = BigFloat(tv[1]); d = BigFloat(0)
    for k in 2:lastindex(sol)
        d = max(d, abs(BigFloat(tv[k]) - s))
        s += BigFloat(sup(domain(xTM[1, k])))
    end
    return Float64(d)
end

# Widened time offset (the registered ε_n rule), intersected with the step's validated domain. Intersection is
# sound because the labels are verified exact (tdrift3 == 0), so the true offset lies in [0, h].
function offset_in_step(T::Float64, tk::Float64, n::Integer, Tmax::Float64, dom::Interval{Float64})
    ε = tlabel_widen(n, Tmax)
    δt = interval(T) - interval(tk) + interval(-ε, ε)
    return intersect_interval(δt, dom)
end
