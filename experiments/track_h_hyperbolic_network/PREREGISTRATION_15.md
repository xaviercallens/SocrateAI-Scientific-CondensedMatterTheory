# Preregistration 15: RC benchmark on other tilings, two integrators (task Q7)

**Date:** 2026-09-28, committed before the run. **Roadmap items:** H-4 (alternative boards) and H-7 (rusty-SUNDIALS).
**Why:** the RC relaxation time and stiffness were computed for {7,3} and flat lattices only (H2-X-0001, H2-X-0004).
The garage build could use another tiling; its predictions must be computed and cross-validated the same way.

## Design
Networks: {8,3} L=2 (N=200), {5,4} L=3 (N=165), {6,4} L=2 (N=120), {4,5} L=4 (N=188), and {7,3} L=2 as control
(N=112). Unit conductances, C = 1 per interior node, boundary as in the paper. For each: λ_min, λ_max of L_ii,
τ = 1/λ_min, stiffness λ_max/λ_min. Integrator controls exactly as in `rc_network.py`: K1 (matrix-exponential known
answer at t ∈ {0.25, 1, 4, 16}τ, max-norm relative error < 1e-5) and K2 (steady state after 40τ equals the Schur
complement column for 3 probes, < 1e-6), rtol 1e-8, atol 1e-10, seed 3, with SciPy BDF and, if `rusty_sundials` is
importable, rusty-SUNDIALS CVODE (BDF); a backend that is not importable is reported NOT RUN, never passed.
Data file: `data/rc_benchmark_on_other_tilings.json`.

## Validity gates
- G1: {7,3} L=2 reproduces τ = 2.7503 and stiffness 14.94 of `data/rc_network.json` to 1e-3 relative.
- G2: SciPy passes K1 and K2 on {7,3} L=2.

## Predictions (fixed now)
- **P1:** K1 and K2 pass on every network for every backend that runs. **Refuted if** any fails.
- **P2 (ordering from the depth picture of H0-X-0008):** τ is ordered by maximal depth: the q = 4, 5 tilings (d_max ≤ 2
  at these sizes) have τ < τ({7,3} L=2) = 2.75, and {8,3} L=2 (d_max = 3) has τ within 25 % of {7,3} L=2.
  **Refuted if** any q = 4, 5 network has τ ≥ 2.75, or {8,3} L=2 is outside [2.06, 3.44].
- **P3:** every stiffness is below that of square R=6 (35.4, `data/rc_network.json`). **Refuted if** any is ≥ 35.4.

## Not claimed
Physical boards, larger sizes, other boundary conditions; nothing about holography.
