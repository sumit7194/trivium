include(joinpath(@__DIR__, "q2_hh_poincare.jl"))
# float reference P1 by RK4 (dt 1e-4) from a point; then the validated image of a tiny box around it must contain it
function ref_p1(y0, py0; dt=1e-4)
    f(u) = (u[3], u[4], -u[1] - 2u[1]*u[2], -u[2] - u[1]^2 + u[2]^2)
    u = (0.0, y0, sqrt(2/6 - py0^2 - y0^2 + 2y0^3/3), py0); t = 0.0
    while t < 40
        k1 = f(u); k2 = f(u .+ (dt/2) .* k1); k3 = f(u .+ (dt/2) .* k2); k4 = f(u .+ dt .* k3)
        un = u .+ (dt/6) .* (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4)
        if t > 0.5 && u[1] < 0 && un[1] >= 0
            s = -u[1]/(un[1]-u[1]); return (u[2] + s*(un[2]-u[2]), u[4] + s*(un[4]-u[4]), t + s*dt)
        end
        u = un; t += dt
    end
end
for (y0, py0) in [(-0.2501, 0.00006), (0.1, 0.2), (-0.3, -0.1)]
    t = @elapsed r = p1_box(interval(y0 - 1e-6, y0 + 1e-6), interval(py0 - 1e-6, py0 + 1e-6))
    ref = ref_p1(y0, py0)
    if r[:ok]
        println((y0, py0), " ok  y=", r[:y], " py=", r[:z], " t=", r[:tret], "  ref=", ref, "  contains: ",
                in_interval(ref[1], r[:y]) && in_interval(ref[2], r[:z]), "  H width ", r[:H_width], "  [", round(t, digits=1), " s]")
    else
        println((y0, py0), " FAIL ", r[:reason], "  ref=", ref)
    end
end
