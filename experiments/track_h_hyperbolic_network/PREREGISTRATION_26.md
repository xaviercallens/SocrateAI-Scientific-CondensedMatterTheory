# Preregistration 26: a boundary along the lattice diagonal, and the growth rate (task Q5i, first step)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2. **Why:** preregistration 25 gave an exact, verified rate for
the square lattice with a boundary *along a lattice axis*: 1.65 decades per row for the zigzag block. The square *disk* has
rates of 1.1 to 1.2 decades per graph step (H0-X-0013), well below that, and a disk's boundary contains every orientation
and curvature. Before attacking curvature, this card isolates one ingredient that is exactly separable: **the boundary
orientation**. A boundary along the diagonal (the lattice rotated by 45° relative to the boundary) is a periodic strip, and
the graph depth is then the L1 distance to the boundary.

## The geometry and the picture (fixed now)
Square lattice nodes (x, y), identified along the diagonal, (x, y) ~ (x + W, y + W). Rows s = x − y = 0, 1, 2, …, each with W
nodes (j = x mod W); the boundary is row 0, whose nodes have no edges among them; node (s, j) is joined to the nodes (s+1, j)
(**type B**) and (s+1, j+1) (**type A**) of the next row. Boundary modes e^(ikj) have the harmonic extension λ(k)^s e^(ikj),
where λ is the root with |λ| < 1 of (1+e^(ik))λ² − 4λ + (1+e^(−ik)) = 0 (|λ(k)| = ρ(k) = (1 − sin(|k|/2))/cos(k/2); the zigzag mode
k = π decouples, λ = 0). A type-B edge between rows s and s+1 has signature λ(k)^s(1 − λ(k)) per mode, so at total momentum
q = 2πi/W the type-B columns form the block V[n, r] = a_n z_n^r with z_n = λ(k_n)λ(q−k_n), a_n = (1−λ(k_n))(1−λ(q−k_n)), with the
position-diagonal direction projected out as in preregistration 25. The smallest singular value of block q then decays at the
Green-function exponent of the interval of the node moduli |z_n|; evaluated by prediction functions only, for the six
momenta of preregistration 25 (labels 8, …, 48 at W = 96, evaluated at W = 384): **0.8488, 0.9384, 1.0361, 1.1439, 1.2647,
1.4027** decades per row (per graph step).
**Rival form (a naive geometric guess):** graph depth along a diagonal boundary is the L1 distance, which is √2 times the
Euclidean depth, so the rate per graph step is the aligned value divided by √2: 0.6792, 0.8048, 0.9181, 1.0148, 1.0966,
**1.1686** (the last falls inside the disk's measured 1.08–1.23, which is why it needs to be ruled in or out).

## Design
Exact blocks of the type-B edge columns in 140-digit arithmetic (mpmath), W = 384, depths 0…25; σ_min as in preregistration
25 (inverse Gram and power iteration; here the Gram is Hermitian). **Rate** = (log₁₀σ_min(15) − log₁₀σ_min(25))/10. Six momenta
(i = 4 × label); σ_min at depth 20 for all blocks i = 0…192; the zigzag block at W = 768. Width and window follow the amended
design of preregistration 25 (97 and 193 distinct nodes at the zigzag momentum). Data file:
`data/diagonal_boundary_orientation_and_the_gr.json`.

## Validity gate
- G1: the exact zigzag block (W = 96) has per-row increments of log₁₀σ_min for d = 1…5 within 0.02 of those of the explicit
  double-precision block of the Jacobian of a W = 96, height-40 diagonal strip (the script recomputes it). A failure means
  the block formula (the amplitudes a_n, the roots λ) is wrong, and no further prediction is evaluated.

## Predictions (fixed now)
- **P1 (zigzag rate, Green form).** The zigzag block's rate is within 3 % of 1.4027. The result also records whether it is
  within 5 % of the rival 1.1686 (disjoint intervals).
- **P2 (rate as a function of momentum).** The six block rates are each within 5 % of the Green values above.
- **P3 (dominant block).** At depth 20 the block with the smallest σ_min among i = 0…192 is the zigzag block i = 192.
- **P4 (orientation matters).** The diagonal zigzag rate differs from the aligned boundary's 1.6527 (preregistration 25) by at
  least 8 % (the prediction is 15 %).

## What a refutation would mean (written now)
G1 failing: an error in the block derivation for this geometry; nothing else is read. P1 refuted with the rival fitting:
the L1-depth scaling is the real mechanism and the Green exponent needs a geometric factor. P1 refuted with neither: the node
picture is incomplete for the diagonal strip (a missing structure beyond the interval of node moduli, for example the
complex phases of the amplitudes). P3 refuted: the dominant momentum is not the zigzag one for a diagonal boundary. P4 refuted:
orientation does not change the rate to within 8 %, so the disk's lower constant cannot come from boundary orientation.

## Not claimed
That any of this is the disk's constant (a disk also has curvature and a staircase boundary; if the diagonal rate comes out
at 1.40 it is still above the disk's 1.1–1.2, so orientation alone would not explain the disk); the type-A columns (same
nodes, different amplitudes: not computed); the triangular lattice; hyperbolic geometry; anything about holography.
