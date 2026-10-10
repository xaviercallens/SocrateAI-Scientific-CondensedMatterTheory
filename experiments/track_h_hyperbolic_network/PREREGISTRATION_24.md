# Preregistration 24: momentum-resolved rates on the square cylinder (task Q5g)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2. **Why:** preregistration 23 predicted that the
vertical-edge columns of a square cylinder lose conditioning at 0.784 decades per row; the run gave 1.78–1.79
(P1 and P3 refuted, `PREREGISTRATION_23.md` Deviation 1). **After seeing that result** I found what the preregistered
number had left out, and the corrected picture reproduces the measurement to 3 %. That agreement is an explanation fitted
to one number, not a test. This card tests the corrected picture on quantities that were not used to build it.

## The corrected picture (post-hoc, stated before this card's run)
At total momentum q the vertical-edge columns of depth 0…d form a Vandermonde-type block whose nodes are
z_n = e^(−(κ(k_n)+κ(q−k_n))), k_n = 2πn/W, κ(k) = acosh(2 − cos k). The condition number of the whole Jacobian is
σ_max (shallow columns, O(1)) divided by σ_min, and **σ_min is set by the block with the smallest top node**, not by the
block with the widest node spread. Scaling a block's columns by its largest node z_max(q) costs log₁₀(1/z_max) per row, and
the remaining Vandermonde system on [a, 1], a = z_min/z_max, grows by log₁₀ρ, ρ = x + √(x²−1), x = (3+a)/(1−a). So block q
loses **rate(q) = log₁₀(1/z_max(q)) + log₁₀ρ(a_q) decades per row**, and the global rate is the maximum over q, attained
at q = π (z_max = e^(−acosh 3) = 0.172, a = 0.42): **1.833**. The preregistered 0.784 of preregistration 23 was the q = 0
block alone. The numbers for W = 96, evaluated by `predicted_rate` without any measurement: q = π/6: 1.019;
π/3: 1.237; π/2: 1.425; 2π/3: 1.583; 5π/6: 1.716; π: 1.833.

## Design
Square cylinder, W ∈ {64, 96} columns (periodic), H = 14 rows below the boundary row, unit conductances, explicit
Jacobian of `hyperbolic_network.jacobian`. Translation invariance makes the Jacobian block-diagonal in the lateral Fourier
wave number i (q = 2πi/W): for each edge type (vertical, or horizontal including the boundary row's own edges) and each
depth r the columns are Fourier-transformed over the lateral position, giving per i a (data rows × depths) complex matrix
whose singular values are those of block i (the union over i is the spectrum of the unblocked matrix, gate G1). For
every block and every d the smallest singular value of the matrix restricted to depths ≤ d is computed; a block is
followed while its own log₁₀(σ_max/σ_min) ≤ 12.5. **Block rate** = least-squares slope of −log₁₀σ_min against d over
3 ≤ d ≤ d_last. **Global rate** = the same slope for the minimum over blocks, over 3 ≤ d ≤ 7. Data file:
`data/momentum_resolved_rates_on_the_cylinder.json`.

## Validity gates
- G1: on W = 32, d ≤ 4, the sorted union of block singular values equals the sorted singular values of the unblocked
  vertical-edge Jacobian to 10⁻⁸ of the largest (checked once during preparation: 2×10⁻¹⁵; infrastructure validation).
- G2: the global rates from the block machinery for the vertical edges (W = 64, 96) are within 0.08 of the explicit-SVD
  rates of preregistration 23 (1.793 and 1.783; known data, used as a consistency check only).

## Predictions (fixed now)
- **P1 (where the minimum is).** For every depth d from 4 to 7, on both W, the block with the smallest σ_min is the
  zigzag block q = π (i = W/2). **Refuted if** any depth gives another block.
- **P2 (the rate as a function of momentum, vertical edges, W = 96).** The block rates at i = 8, 16, 24, 32, 40, 48
  (q = π/6 … π) agree with the six numbers above to within 15 % each. **Refuted if** any is outside.
- **P3 (the edge type does not matter).** For the horizontal-edge columns (W = 96) the global rate is within 10 % of
  1.833. **Refuted if** outside.

## What a refutation would mean (written now)
P1 refuted: the minimum is set by a block the picture does not identify (for example prefactors beating rates at small d,
or a block with extra structure). P2 refuted at some q: the node picture is right at q = π (where it was fitted) but the
dependence on q (the spread parameter a_q, the scaling by z_max) is wrong; refuted only at small q would point to slow
convergence in d. P3 refuted: the rate depends on the edge type through the weights, so it is not a property of the nodes
alone.

## Not claimed
That the picture explains the disk's rates (disks have curvature, diagonal directions and graph-distance depth; the
disk values 1.1–1.2 are below this cylinder value 1.83, which is itself a finding to explain); the triangular lattice
(its straight periodic boundary is exactly degenerate, `PREREGISTRATION_23.md`); hyperbolic geometry; a proof of the
Vandermonde asymptotics; anything about holography.
