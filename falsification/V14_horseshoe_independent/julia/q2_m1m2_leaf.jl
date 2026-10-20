# V14 Q2-R2 post-hoc leaf diagnosis: the single depth-10 failing leaf of AZ M1 => M2 (q2_hh_F.json).
include(joinpath(@__DIR__, "q2_m1m2_diag.jl"))
sp = parse_spec(joinpath(SPECDIR, "hh1_M1M2.spec")); M = sp["tsets"]["M1"]; N = sp["tsets"]["M2"]
c = (Rat(-631, 1024), Rat(-315, 512), Rat(887, 1024), Rat(111, 128))
rect = piece_rect(M, c...)
im = image_compute(rect)
println("leaf chart (u1,u2,s1,s2) = ", Float64.(collect(c)), "  rect (y1,y2,py1,py2) = ", Float64.(collect(rect)))
println("ok=", im[:ok], " reason=", im[:reason], " t1_est=", get(im, :t1_est, nothing), " nsteps=", get(im, :nsteps, nothing))
if im[:ok]
    U, S = to_frame(N, im[:y], im[:z]); println("U=", U, " S=", S, "  widths U ", diam(U), " S ", diam(S), "  tret ", im[:tret])
end
Ni = Float64.(N.Ainv); Nc = Float64.(N.c); r = Float64.(collect(rect)); us = Tuple{Float64,Float64}[]
for a in range(r[1], r[2], length = 9), b in range(r[3], r[4], length = 9)
    y1, p1 = p1_float(a, b); isnan(y1) && continue
    push!(us, (Ni[1,1]*(y1-Nc[1]) + Ni[1,2]*(p1-Nc[2]), Ni[2,1]*(y1-Nc[1]) + Ni[2,2]*(p1-Nc[2])))
end
println("float image: u in ", extrema(first.(us)), "  s in ", extrema(last.(us)), "  margin ", minimum(max(1-abs(s), abs(u)-1) for (u,s) in us))
