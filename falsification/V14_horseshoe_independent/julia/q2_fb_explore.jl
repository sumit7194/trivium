# POST HOC exploration (not a decision): which orderT lets the failing Q2-R2 leaf integrate? Also orderT 16 = primary.
include(joinpath(@__DIR__, "q2_fallback.jl"))
sp = parse_spec(joinpath(SPECDIR, "hh1_M1M2.spec")); M = sp["tsets"]["M1"]; N = sp["tsets"]["M2"]
c = (Rat(-631, 1024), Rat(-315, 512), Rat(887, 1024), Rat(111, 128)); rect = piece_rect(M, c...)
Y = hull(ratI(rect[1]), ratI(rect[2])); Z = hull(ratI(rect[3]), ratI(rect[4]))
for oT in (16, 12, 14, 18, 20, 24)
    t = @elapsed r = p1_box_fb(fb_integ(oT), Y, Z)
    s = r[:reason]
    if r[:ok]
        U, S = to_frame(N, r[:y], r[:z])
        s = "U=$(round.([inf(U),sup(U)],digits=4)) S=$(round.([inf(S),sup(S)],digits=4)) missF=$(miss_F(N,U,S,r[:z]))"
    end
    println("orderT ", oT, ": ok=", r[:ok], "  ", s, "  [", round(t, digits=1), " s]"); flush(stdout)
end
