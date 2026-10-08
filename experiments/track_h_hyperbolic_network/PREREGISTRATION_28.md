# Preregistration 28: curvature on a polar-grid disk (task Q5i, curvature step)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2. **Why:** the square disk loses 1.1–1.2 decades per graph step (H0-X-0013), below the
aligned strip's 1.65 (H0-X-0016), and the diagonal strip's 1.07 (H0-X-0017) shows that boundary orientation can lower the rate. A disk also has
curvature. This card isolates **curvature** in a geometry that is exactly separable and whose large-radius limit is the aligned strip.

## Geometry and the local-strip argument (fixed now)
A polar-grid disk: W angular sites, angle step Δθ = 2π/W, radial step h = RΔθ (square cells at the boundary), levels l = 0…H at radii
r_l = R − lh, boundary = level 0, insulating inner end at level H. Conductances from the continuum Laplacian: tangential at level l, R/r_l;
radial between levels l and l+1, r_{l+1/2}/R. The network is rotation-invariant, so the Jacobian blocks are indexed by total angular
momentum and the harmonic extension of angular mode m solves a tridiagonal radial recurrence (exact, 140 digits). The radial-edge columns
of the zigzag block (total angular momentum W/2) have entries α_{m}(l)α_{W/2−m}(l), α_m(l) = A_m(l) − A_m(l+1), with the position-diagonal
direction projected out (as in preregistrations 25–27). As R → ∞ the network becomes the aligned strip with equal conductances.
**Local-strip (WKB) argument.** At level l the network looks locally like an aligned strip with lateral-to-vertical conductance ratio
λ_l = R²/(r_l r_{l+1/2}), which grows with depth, and the aligned strip's zigzag rate G(λ) (preregistration 27) is increasing in λ for λ ≥ 1
(1.653 at λ = 1, 1.958 at λ = 4). So smooth curvature should **raise** the per-row loss with depth, by the amount
g_w(R, l) = G(λ_l)/G(λ_3) − 1 relative to level 3. Evaluated by prediction functions only (W = 384 node sets, Green exponent): at R = 48
(W = 304): g_w = **0.0474** at l = 12 and **0.172** at l = 24; at R = 96 (W = 608): **0.0529** at l = 24 (0.0185 at l = 12, not scored).

## Pilots (disclosed; excluded from scoring)
Before this card I ran the exact block at R = 24 (W = 152) and R = 32 (W = 202), declared excluded. They showed: the inner end matters a lot
(R = 24, level-12 increment 2.60, 1.97, 1.85 and 1.79 for inner radii 10.1, 6.1, 4.2 and 2.2; a first pilot mistook this for curvature); at
inner radius about two cell sizes the sensitivity is below 1 % per level of H; and the exact growth of the increment is **0.68 to 0.75 of g_w**
(four cells), i.e. the local-strip argument has the right sign and shape and overestimates the size. The band below is informed by that.
No block at R = 48 or 96 was computed before this commit.

## Design
Exact zigzag blocks (mpmath, 140 digits, σ_min as in preregistration 25): R = 48 with W = 304, H = 46 (inner radius 2.4) and R = 96 with W = 608,
H = 94 (inner radius 2.8), levels 0…24; and R = 48 with H = 44 as the inner-end check. Increments I(l) = log₁₀σ_min(l−1) − log₁₀σ_min(l); growth
g(R, l) = I(l)/I(3) − 1. Data file: `data/curvature_on_a_polar_grid_disk.json`.

## Validity gates
- G1: on a small disk (R = 10, W = 64, H = 8) the exact zigzag block's per-row increments for d = 1…5 agree with those of the explicit
  double-precision block of the Jacobian of the same network within 0.005 (pilot: identical to four decimals).
- G2: at R = 48, I(12)/I(3) changes by at most 2 % when H goes from 46 to 44 (the inner end is not driving the result).

## Predictions (fixed now)
- **P1 (size of the effect).** The ratio of exact growth to g_w lies in [0.55, 0.90] for the three cells (R, l) = (48, 12), (48, 24), (96, 24).
- **P2 (scaling).** The growth at l = 12 for R = 48 and at l = 24 for R = 96 (both at l/R = 0.25, the same λ_l) agree within 20 %.
- **P3 (flat limit).** The level-3 increment at R = 96 is within 2 % of the aligned unit-conductance strip's level-3 increment (1.611, preregistration 25).
- **P4 (curvature raises the rate).** The measured growth is above 0.01 in all three cells (the opposite sign would mean curvature lowers the rate).

## What a refutation would mean (written now)
P1 refuted below the band: the local-strip argument overestimates more than the pilots suggested; above: the effect is stronger than local.
P2 refuted: the effect does not scale with l/R (non-adiabatic or discrete-node effects). P3 refuted: the flat limit of the polar network
differs from the strip (a boundary-layer effect). P4 refuted: curvature of this kind lowers the rate and the pilots misled. G2 failed: the
inner end still contaminates and the polar network needs a regular centre.

## Not claimed
That this explains the square disk's constant: the polar network has no boundary roughness and no orientation dependence; the effect of
curvature is small here (a few percent over the first quarter radius) and has the sign opposite to what the disk's low rate would need;
the triangular lattice; hyperbolic geometry; a proof; anything about holography.
