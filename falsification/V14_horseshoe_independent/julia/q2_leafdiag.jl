include(joinpath(@__DIR__, "q2_hh_cover.jl"))
sp = parse_spec(joinpath(SPECDIR, "hh1_M3M4.spec")); M = sp["tsets"]["M3"]; N = sp["tsets"]["M4"]
c = (Rat(127, 256), Rat(1, 2), Rat(-111, 128), Rat(-221, 256))
rect = piece_rect(M, c...)
im = image_compute(rect)
println("leaf rect (y1,y2,py1,py2) = ", Float64.(collect(rect)))
println("ok=", im[:ok], " reason=", im[:reason], " t1_est=", get(im, :t1_est, nothing))
if im[:ok]
    U, S = to_frame(N, im[:y], im[:z]); println("U=", U, " S=", S, " widths y ", diam(im[:y]), " py ", diam(im[:z]))
end
