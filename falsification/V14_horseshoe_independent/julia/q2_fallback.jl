# V14 Q2-R3 helper: poincare1 with a pluggable integrator, generated TEXTUALLY from q2_hh_poincare.jl's poincare1 so
# that the section, root-isolation, transversality, departure/window, S9 and time-label logic are byte-identical;
# only the call `b3_integ(hh!, X0, 0.0, tmax, SP)` is replaced by `integ(hh!, X0, 0.0, tmax, SP)`.
include(joinpath(@__DIR__, "q2_hh_cover.jl"))
let src = read(joinpath(@__DIR__, "q2_hh_poincare.jl"), String)
    i = findfirst("function poincare1(", src); j = findfirst("\n# Driver for one initial box", src)
    body = src[first(i):first(j)-1]
    @assert occursin("b3_integ(hh!, X0, 0.0, tmax, SP)", body)
    body = replace(body, "function poincare1(Y::Interval{Float64}, PY::Interval{Float64}; tmax::Float64)" =>
                         "function poincare1_fb(integ, Y::Interval{Float64}, PY::Interval{Float64}; tmax::Float64)")
    body = replace(body, "b3_integ(hh!, X0, 0.0, tmax, SP)" => "integ(hh!, X0, 0.0, tmax, SP)")
    @assert occursin("function poincare1_fb(integ,", body)
    include_string(@__MODULE__, body)
end
# Candidate fallback integrators: same validated_integ3, orderQ 2, midrad = false, abstol, maxsteps; only orderT varies.
fb_integ(orderT) = (f!, X0, t0, tmax, sp) -> validated_integ3(f!, X0, t0, tmax, B3_ORDER_Q, orderT, B3_ABSTOL, sp;
                                                             maxsteps = B3_MAXSTEPS, midrad = B3_MIDRAD)
function p1_box_fb(integ, Y, PY)       # same tmax rule as p1_box
    t1 = est_t1(mid(Y), mid(PY))
    isnan(t1) && return Dict(:ok => false, :reason => "no_float_return_estimate")
    r = poincare1_fb(integ, Y, PY; tmax = t1 + 0.5)
    if !r[:ok] && (r[:reason] in ("window_not_closed_by_tmax", "first_upcrossing_not_reached"))
        r = poincare1_fb(integ, Y, PY; tmax = t1 + 1.5)
    end
    r[:t1_est] = t1
    return r
end
