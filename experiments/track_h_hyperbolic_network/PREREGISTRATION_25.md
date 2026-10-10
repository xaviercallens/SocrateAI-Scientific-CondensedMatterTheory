# Preregistration 25: exact semi-infinite blocks and the asymptotic rates (task Q5h)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2. **Why:** preregistration 24 measured the
conditioning rate of the momentum blocks of the square-cylinder Jacobian in double precision at a finite height, and the
result was ambiguous: the zigzag block's rate over d = 3…6 came out at 1.85 (against my closed form 1.833) but the
per-row increments were still *rising* (1.74, 1.84, 1.97), the other blocks missed by 14–22 %, and the cylinder height
turned out to change the numbers by tenths of a decade (post-hoc diagnostic: the explicit SVD at H = 14 reproduces the
block values exactly and at H = 18 gives up to 0.34 decades less at d = 6). A finite height and double precision cannot give an
asymptotic rate. For a **semi-infinite** cylinder each block is a closed-form matrix, so the asymptotics can be followed
to depth 30 in 140-digit arithmetic. This card does that and decides between two rival closed forms.

## The two rival closed forms (both fixed now)
At total momentum q = 2πi/W the block is V[n, r] = a_n z_n^r with z_n = z₁(k_n)z₁(q − k_n), z₁(k) = e^(−acosh(2 − cos k)),
a_n = (1 − z₁(k_n))(1 − z₁(q − k_n)), k_n = 2πn/W, and with the position-diagonal direction (the uniform vector over n)
projected out, because the data are the strictly upper-triangular entries of the boundary map (checked during
preparation: the projected exact block reproduces the explicit double-precision increments at H = 40 and d ≤ 5 to
0.005, W = 96; the unprojected one does not).
- **Rival A (the closed form of preregistration 24, post-hoc):** rate = log₁₀(1/z_max) + log₁₀ρ(a), a = z_min/z_max,
  ρ = x + √(x²−1), x = (3+a)/(1−a). It evaluated the Chebyshev growth at t = −1 after rescaling the interval. For W = 96:
  1.019, 1.237, 1.425, 1.583, 1.716, 1.833 at q = π/6, π/3, π/2, 2π/3, 5π/6, π.
- **Rival B (potential theory, found while diagnosing; I had mis-placed the evaluation point in A):** the smallest
  sup-norm on the nodes of a polynomial with unit *coefficient 2-norm* decays like e^(−dG), G = max over |ζ| = 1 of the Green
  function of ℂ∖[z_min, z_max]; for a real interval this is log|w + √(w²−1)| at ζ = −1, w = (2ζ − z_max − z_min)/(z_max − z_min).
  For W = 96: **0.9605, 1.1381, 1.2984, 1.4352, 1.5508, 1.6527** at the same six momenta; the maximum over all blocks
  i = 0…48 is at the zigzag block (1.6527), and the same at W = 192. Rival B is the standard result for this problem, found
  after the fact; I state it as a prediction because nothing computed so far reaches depth 20.

## Design
Exact blocks as above (mpmath, 140 digits), W = 96, depths 0…30. σ_min of the first d+1 columns is obtained as
1/√λ_max(G⁻¹), G = VᵀV, by power iteration. **Rate** = (log₁₀σ_min(20) − log₁₀σ_min(30))/10. Computed for the six
momenta (i = 8, 16, 24, 32, 40, 48); σ_min at depth 20 for all blocks i = 0…48; and the zigzag block at W = 192. Data file:
`data/exact_semi_infinite_blocks_asymptotic_ra.json`.

**Deviation 1 (2026-10-08, after the first run, which crashed before any verdict existed; thresholds unchanged).** The
first run stopped with a numerically singular Gram matrix at depth 24, at 140 and at 400 digits, so not a precision effect.
At W = 96 the zigzag block has only 25 distinct nodes (z_n is invariant under k → −k and k → π − k, so the 96 mode indices
collapse to 25 values), and with the diagonal direction projected out the block has rank at most 24: depth 24 and
beyond are rank-deficient, and the window 20 to 30 of the Design was impossible by construction. (This is also a physical
statement: a boundary of W sites carries finitely many data per momentum, so the restricted Jacobian loses rank at a depth set
by W.) Amended design, fixed before the rerun: the six momenta, the depth-20 comparison over all blocks, and the rates use
**W = 384** (97 distinct nodes at the zigzag momentum; block indices i = 32, 64, 96, 128, 160, 192, the same momenta as
i = 8, …, 48 at W = 96), with the **rate window 15 to 25**, i.e. (log₁₀σ_min(15) − log₁₀σ_min(25))/10; P4 compares the zigzag
rate at **W = 768** with the one at W = 384; G1 and P5 stay at W = 96 (they use depths ≤ 6). P3 now asks for block
i = 192 at W = 384. All thresholds (3 %, 5 %, 1 %, 0.02, 0.15) and the Green values are unchanged; the Green values for W = 384
evaluate to the same four digits as for W = 96 (checked by the prediction function only).

## Validity gate
- G1: the exact zigzag block's per-row increments of log₁₀σ_min for d = 1…5 agree with the explicit double-precision
  block of the Jacobian of a W = 96, H = 40 cylinder (the script recomputes it) within 0.02 each.

## Predictions (fixed now)
- **P1 (zigzag rate, rival B).** The zigzag block's rate is within 3 % of 1.6527. (The result also records whether it falls
  within 2 % of rival A's 1.8327; the two intervals are disjoint, so at most one can hold.)
- **P2 (rate as a function of momentum, rival B).** The six block rates are each within 5 % of the Green values above.
- **P3 (where the minimum is).** At depth 20 the block with the smallest σ_min, among i = 0…48, is the zigzag block i = 48.
- **P4 (width).** The zigzag rate at W = 192 is within 1 % of the one at W = 96.
- **P5 (the finite height explains the acceleration).** The per-row increment of the zigzag block between d = 5 and d = 6
  in the H = 14 double-precision data of preregistration 24 exceeds the exact semi-infinite increment between the same
  depths by at least 0.15.

## What a refutation would mean (written now)
P1 refuted with rival A fitting: the correct asymptotic exponent is not the potential-theory one (the weights a_n or the
projection matter at the exponential level). P1 refuted with neither fitting: the asymptotic rate of the semi-infinite
block is something else again and the nodes-in-an-interval picture is incomplete. P2 refuted only for small q: slow
convergence in d at small q. P3 refuted: another block dominates at depth 20 (the picture's identification of the dominant
momentum is wrong). P4 refuted: the continuum limit needs larger W. P5 refuted: the acceleration seen in preregistration
24 is not a finite-height effect.

## Not claimed
Anything about the disk or hyperbolic geometry; triangular lattices; the closed-height cylinder beyond P5; a proof (this
is a computation on a closed-form block, plus a standard potential-theory estimate); anything about holography.
