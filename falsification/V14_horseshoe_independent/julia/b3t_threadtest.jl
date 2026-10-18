# Thread-safety test for B3t: the same 16 small M-rectangles computed serially and threaded must give identical enclosures.
include(joinpath(@__DIR__, "b3t_q1_cover.jl"))
rects = NTuple{4,Rat}[]
for i in 0:3, j in 0:3
    y1 = Rat(-84, 10) + Rat(i, 50); z1 = Rat(28, 1000) + Rat(j, 1000)
    push!(rects, (y1, y1 + Rat(1, 100), z1, z1 + Rat(1, 2000)))
end
t = @elapsed ser = [image_compute(r) for r in rects]
empty!(CACHE)
t2 = @elapsed prefetch!(rects)
par = [CACHE[r] for r in rects]
eqI(x, y) = inf(x) == inf(y) && sup(x) == sup(y)
same(a, b) = a[:ok] == b[:ok] && (!a[:ok] || (eqI(a[:y], b[:y]) && eqI(a[:z], b[:z]) && eqI(a[:tret], b[:tret])))
println("threads=", Threads.nthreads(), " serial ", round(t, digits=1), " s, threaded ", round(t2, digits=1), " s; identical: ",
        all(same(ser[k], par[k]) for k in eachindex(rects)), "  ok-count ", count(x -> x[:ok], ser))
