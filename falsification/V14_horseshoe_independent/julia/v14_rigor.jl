# V14 shared helper: rigorous evaluation of a validated-integration Taylor model at a time offset.
# xTM[i, n] is a TaylorModel1 in time whose coefficients are TaylorN{Float64} in the normalised initial-box variables,
# plus an interval remainder. Every coefficient is evaluated in interval arithmetic on the box, and the time
# polynomial by interval Horner; the remainder is added. Float64 coefficients are exact inputs, and every operation
# is an interval operation, so the result encloses the true value. (The package's nested `evaluate` on this type was
# found to round in non-interval arithmetic: Q0b diagnostic, results/q0_rossler.json history.)
using TaylorModels, IntervalArithmetic
function rig_eval(tm, δt::Interval{Float64}, box::Vector{Interval{Float64}})
    c = polynomial(tm).coeffs
    acc = interval(0.0)
    for k in length(c):-1:1
        ckI = c[k] * interval(1.0)          # TaylorN with interval coefficients (exact copy of the Float64 ones)
        val = evaluate(ckI, box)            # interval arithmetic throughout
        acc = acc * δt + val
    end
    return acc + remainder(tm)
end

# Time-label rule (Q0b finding): the package's step-start labels t_n are Float64 sums and can drift from the true
# elapsed time by ~n ulps (observed up to 1e-14 after 75 steps; containment restored at that widening). Every time
# offset is therefore widened by ε_n = 4·n·eps(T_max) before evaluation. The state enclosures themselves are rigorous
# as sets (the flowpipe boxes contained the reference in every case), and Poincaré images do not depend on time labels.
tlabel_widen(n::Integer, Tmax::Float64) = 4 * n * eps(Tmax)
