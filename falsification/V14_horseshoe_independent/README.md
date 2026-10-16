# V14: the bridge's independent replay of the chaos-proof covering relations (quantum S6)

Not started. Pre-registration to come, after quantum's Rössler and HH results. Planned engine: TaylorModels.jl
(validated Taylor-model integration via IntervalArithmetic.jl, Float64 intervals), which is library-independent of
quantum's CAPD/MPFR. It must reproduce quantum's Rössler and HH covering decisions, including the wrong-configuration
rejections, before it replays any MN covering.

Environment (installed 2026-10-16 with the user's approval):
- Julia 1.13.2 (aarch64-apple-darwin), via Homebrew juliaup 1.22.7, channel `release`.
- Packages are pinned in `julia/Project.toml` and `julia/Manifest.toml`: TaylorModels 0.13.1, TaylorIntegration 0.18.19,
  IntervalArithmetic 1.0.12, TaylorSeries 0.23.1.
- Reproduce with `julia --project=julia -e 'using Pkg; Pkg.instantiate()'`.
- `julia/smoke.jl` integrates the harmonic oscillator over 2π, and the enclosure contains the exact image (1, 0).
  Note: `flowpipe(sol)[end]` encloses the whole last time step, not the endpoint, so its width is not the endpoint
  error.
