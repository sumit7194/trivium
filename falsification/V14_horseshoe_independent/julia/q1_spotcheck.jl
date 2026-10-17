# V14 Q1 spot check (non-gating sanity data): for sampled pieces at ladder level 2, the validated P^2 enclosure must
# contain a non-rigorous float P^2 (RK4, dt = 1e-4, crossing refined by Newton on the RK4 step) at the piece's
# centre and 4 corners. Catches gross errors (wrong crossing counted, wrong branch), not ulp-level ones.
using JSON, Random
include(joinpath(@__DIR__, "q1_poincare.jl"))
const PB = ratI(1 // 5); const PA = ratI(57 // 10)
f(u) = (-(u[2] + u[3]), u[1] + 0.2*u[2], 0.2 + u[3]*(u[1] - 5.7))
function rk4(u, dt)
    k1 = f(u); k2 = f(u .+ (dt/2) .* k1); k3 = f(u .+ (dt/2) .* k2); k4 = f(u .+ dt .* k3)
    u .+ (dt/6) .* (k1 .+ 2 .* k2 .+ 2 .* k3 .+ k4)
end
function float_p2(y0, z0; dt=1e-4)
    u = (0.0, y0, z0); t = 0.0; ups = 0
    while t < 40
        un = rk4(u, dt)
        if t > 0.1 && u[1] < 0 && un[1] >= 0
            ups += 1
            if ups == 2
                τ = dt * (-u[1]) / (un[1] - u[1])
                for _ in 1:6
                    w = rk4(u, τ); τ -= w[1] / f(w)[1]
                end
                w = rk4(u, τ); return (w[2], w[3], t + τ)
            end
        end
        u = un; t += dt
    end
    error("no return")
end
# sources (section rectangles, from the specs' boxes): base M, base N, W2 M', W3 M
srcs = Dict("M" => (-42//5, -38//5, 7//250, 17//500), "N" => (-57//10, -23//5, 7//250, 17//500),
            "W2_Mprime" => (-8003//1000, -7997//1000, -369//1000, 431//1000), "W3_M" => (-20001//2500, -19999//2500, 7//250, 17//500))
rng = MersenneTwister(20261017)
out = []; nbad = 0
for (name, (y1, y2, z1, z2)) in sort(collect(srcs))
    for trial in 1:6
        n = 16; i = rand(rng, 1:n); j = rand(rng, 1:n)
        dy = (y2 - y1) / n; dz = (z2 - z1) / n
        r = (y1 + (i-1)*dy, y1 + i*dy, z1 + (j-1)*dz, z1 + j*dz)
        im = p2_box(hull(ratI(r[1]), ratI(r[2])), hull(ratI(r[3]), ratI(r[4])), PB, PA)
        im[:ok] || (push!(out, Dict("src" => name, "rect" => string.(r), "ok" => false, "reason" => im[:reason])); continue)
        pts = [(Float64((r[1]+r[2])/2), Float64((r[3]+r[4])/2))]
        for a in (r[1], r[2]), b in (r[3], r[4]); push!(pts, (Float64(a), Float64(b))); end
        inside = Bool[]
        for (y0, z0) in pts
            yf, zf, tf = float_p2(y0, z0)
            push!(inside, in_interval(yf, im[:y]) && in_interval(zf, im[:z]) && in_interval(tf, im[:tret]))
        end
        global nbad += count(!, inside)
        push!(out, Dict("src" => name, "rect" => string.(r), "ok" => true, "all_inside" => all(inside),
                        "y" => [inf(im[:y]), sup(im[:y])], "z" => [inf(im[:z]), sup(im[:z])]))
        println(name, " ", r, " inside: ", inside)
    end
end
open(joinpath(@__DIR__, "..", "results", "q1_spotcheck.json"), "w") do io
    JSON.print(io, Dict("check" => "float P^2 inside validated enclosure (centre + 4 corners), level-2 boxes",
                        "n_outside" => nbad, "samples" => out, "julia" => string(VERSION)), 1)
end
println("points outside enclosure: ", nbad)
