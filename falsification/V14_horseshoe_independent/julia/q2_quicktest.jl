include(joinpath(@__DIR__, "q2_hh_cover.jl"))
sp = parse_spec(joinpath(SPECDIR, "hh1_M2M3.spec")); T = sp["tsets"]
println("M3 special: ", T["M3"].special, " capL ", T["M3"].capL, " capR ", T["M3"].capR)
for (a, b) in (("M0", "M0"), ("M2", "M3"))
    sp2 = parse_spec(joinpath(SPECDIR, "hh1_$(a)$(b).spec")); S = sp2["tsets"]
    t = @elapsed (bb = check_b(S[a], S[b], 8); aa = check_a(S[a], S[b], 4))
    println(a, "=>", b, " level1: (b) ", bb["status"], " orient ", bb["orientation"], " failed ", bb["n_failed_pieces"], " reasons ", bb["failure_reasons"],
            " | (a) ", aa["status"], " pass ", aa["n_pass"], "/", aa["n_boxes"], " failed ", aa["n_failed_boxes"], " ", aa["failure_reasons"], "  [", round(t, digits=1), " s]")
end
