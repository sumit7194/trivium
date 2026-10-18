# V14 Amendment B3: the B1 rigorous step (validated_integ3, interval Picard validation, midrad = false) with the one
# V14 Amendment B3: B2 adaptive refinement at orderQ = 2 (B1 setting); orderT 16, abstol 1e-20, maxsteps 20000 unchanged.
# The JetSpace order is 2*orderQ = 6 (validated_integ3's TaylorModelN products assert 2*orderQ <= space order).
# Item 3 of B2 (pivoted QR) is dropped: TaylorModels 0.13.1 hard-codes `qr(Amid)` without pivoting
# (valid_integ/qrprecondition.jl:224) and offers no option for it.
include(joinpath(@__DIR__, "b1_rigor.jl"))     # rig_eval3, coeff_ranges3, tdrift3, offset_in_step, tlabel_widen
const B3_ORDER_Q = 2
const B3_ORDER_T = B1_ORDER_T
const B3_ABSTOL = B1_ABSTOL
const B3_MAXSTEPS = B1_MAXSTEPS
const B3_MIDRAD = B1_MIDRAD
b3_integ(f!, X0, t0, tmax, sp; midrad::Bool = B3_MIDRAD) =
    validated_integ3(f!, X0, t0, tmax, B3_ORDER_Q, B3_ORDER_T, B3_ABSTOL, sp; maxsteps = B3_MAXSTEPS, midrad = midrad)
