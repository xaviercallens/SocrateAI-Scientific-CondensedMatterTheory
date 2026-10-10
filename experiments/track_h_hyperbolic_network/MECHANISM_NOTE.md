# Mechanism note (Q5d): why equal-depth boundary signatures collapse on flat disks and not on hyperbolic ones

**Status: Tier C (argument), written 2026-10-07 after H0-X-0009/0010/0011 and before any new computation.** It
makes one quantitative prediction, tested by `PREREGISTRATION_20.md` on instances not used to write it. Nothing here
is a result until that card has run. Nothing here concerns holography.

## What has to be explained
- Per-edge amplitude ‖d_e‖² decays with depth alike on all lattices (H0-X-0009).
- The effective dimension fraction f_d = PR/n of the normalised Gram matrix of the Jacobian columns of depth-d edges
  stays ≥ 0.79 on hyperbolic tilings and falls with depth on flat disks (H0-X-0010); the condition number of the
  Jacobian restricted to depth ≤ d grows ≈ 1 decade per unit depth on flat disks, 0.3–0.4 on hyperbolic ones (H0-X-0011).

## The argument
The boundary signature of edge e = (a, b) is d_e = ω_a − ω_b restricted to the boundary, where ω_x is the row of the
harmonic extension for node x: the **harmonic measure** of the boundary seen from x (the hitting distribution of a
random walk from x). The Jacobian column of e is the upper triangle of d_e d_eᵀ.

*Flat disk of radius R (square or triangular lattice).* For a node at depth d (graph distance d from the boundary,
with d ≪ R) the harmonic measure is a bump on the boundary circle of angular width ≈ d/R, i.e. **≈ d boundary sites**,
with Fourier coefficients ≈ (1 − d/R)^{|m|} ≈ e^{−|m| d/R}. The ≈ 2π(R − d) edges of depth d produce signatures that
are, up to lattice details, rotations of one kernel of width ≈ d (the derivative of the bump along the edge). The Gram
matrix of n rotated copies of one kernel on a circle of P ≈ 2πR sites is diagonalised by Fourier modes; its eigenvalues
are |k̂(m)|², which are O(1) for |m| ≲ P/w ≈ R/d and decay exponentially beyond. So the class of n_d ≈ 2πR columns
has **effective rank ≈ R/d** and
  f_d ≈ (R/d)/(2πR) ∝ 1/d,   i.e. d · f_d ≈ constant.
For the Jacobian columns (products d_e d_eᵀ) the kernel is squared, which halves its width and doubles the band,
leaving the 1/d law. The smallest eigenvalue of the class is set by the highest Fourier mode the lattice resolves,
|m| ≈ P/2 ≈ πR, with coefficient e^{−π d}: in decades, log₁₀ κ of the depth-≤d restriction grows by about
π/ln 10 ≈ 1.4 per unit depth for the signature, and for the squared kernel the growth is of the same order. The
measured rates are 0.98 (square) and 1.19 (triangular). The argument fixes the **form** (linear in d, O(1) decade per
unit depth), not the constant.

*Hyperbolic disk with L layers.* A node at depth d sits at hyperbolic distance ≈ d from the boundary, and its harmonic
measure covers a boundary arc of ≈ e^{d/ℓ} … but the number of depth-d nodes is ≈ |∂| · e^{−d/ℓ} (the boundary has
≈ |∂| sites and each deeper layer has a constant fraction fewer nodes, ℓ the layer-decay length). The **overlap
number** (width × count / boundary length) is therefore ≈ 1 at every depth: the bumps of the depth-d nodes tile the
boundary without piling up, their signatures stay nearly orthogonal, and f_d stays O(1) independent of d. On the flat
disk the same overlap number is ≈ d · 2πR / 2πR = d, growing linearly. This is the whole difference: on a flat disk the
boundary does not grow with the bulk, so the deeper edges share an ever-narrower band of boundary modes; on a
hyperbolic disk it does.

*Consequence for κ.* With the overlap number ≈ d, the flat class of depth d adds n_d columns but only ≈ R/d new
directions; each unit of depth therefore adds a full exponential factor to the smallest singular value, and log κ is
linear in d. On the hyperbolic tilings each depth adds new directions in proportion to its columns, and κ grows only
through the amplitude decay, which H0-X-0009 shows is concave: hence the concave profile of H0-X-0008.

## Numerical prediction (tested in PREREGISTRATION_20, on instances not used above)
1. On a flat disk, d · f_d is constant within a factor 1.5 over 2 ≤ d ≤ d_max − 2 (full-class f_d; H0-X-0010's
   square R=10 values give d·f_d = 1.16, 1.17, 1.28, 1.25, 1.02, 0.98 for d = 2…7, which prompted the argument and
   are therefore **not** evidence for it).
2. On a hyperbolic tiling, f_d ≥ 0.75 at every depth ≥ 2 of a larger instance than those used so far.
3. The restricted-κ growth rate on flat disks is between 0.7 and 1.5 decades per unit depth and independent of R
   (within ±0.2 between R = 10 and R = 16); on hyperbolic tilings it stays below 0.5 and does not increase with L.

## What would refute the argument
d · f_d drifting by more than a factor 1.5 across depths (the band argument is wrong), or a hyperbolic f_d falling
below 0.75 at a larger L (the overlap number is not O(1)), or a flat growth rate that changes with R.

## Not claimed
A theorem; the constant in the growth rate; the depth-1 dip of the degree-3 tilings; the behaviour of the q = 4, 5
tilings beyond the layers computed; anything about holography or AdS/CFT.

## Test outcome (2026-10-07, PREREGISTRATION_20, ledger H0-X-0012; appended after the run, nothing above edited)
- **P1 held.** On square R=16, d·f_d lies between 1.02 and 1.28 for every depth 2 ≤ d ≤ 12 (ratio 1.26); on
  triangular R=10.75 between 0.56 and 0.79 (ratio 1.42). The band argument (effective rank ∝ R/d) survives on
  instances it had not seen, with a lattice-dependent constant (≈ 1.2 square, ≈ 0.7 triangular).
- **P2 held.** f_d ≥ 0.76 ({7,3} L=5, d_max = 9) and ≥ 0.80 ({4,5} L=7) at every depth ≥ 2.
- **P3b held.** Hyperbolic Δ̄ = 0.285 ({7,3} L=5, against 0.296 at L=4) and 0.418 ({4,5} L=7): no growth with L.
- **P3a refuted.** Flat Δ̄ = 1.26 (square R=16, d* = 8 of 14) and 1.71 (triangular R=10.75, d* = 6 of 9), against
  0.98 for square R=10 (d* = d_max = 8) and the predicted [0.7, 1.5] band. The growth rate is **not** set by the
  lattice cutoff alone: it depends on R and on where in the disk the window sits (on R=10 the increments shrink as d
  approaches d_max, 1.02 → 0.55; on R=16 the window d ≤ 8 never reaches that regime). The "smallest eigenvalue at
  mode |m| ≈ πR" step of the argument is wrong or incomplete; the band-counting step (P1) is the part that holds.
- **Status after the test:** the overlap-number picture (flat: ∝ d; hyperbolic: O(1)) is supported by P1, P2, P3b.
  The quantitative rate of κ growth on flat disks remains underived. A better-posed rate prediction must compare
  matched windows in d/d_max (lesson LL-A15).

## Cylinder result (2026-10-08, PREREGISTRATIONS 23–25, ledger H0-X-0014 to H0-X-0016): the rate is exact where the problem separates
On a square lattice cylinder (periodic in one direction, measurement on one end) the Jacobian is block-diagonal in total
momentum q, and for the vertical edges each block is a Vandermonde-type matrix [a_n z_n^r] whose nodes are
z_n = z₁(k_n)z₁(q−k_n), z₁(k) = e^(−acosh(2−cos k)) (the per-row decay of a boundary mode), with the position-diagonal
direction projected out (the data are the strictly upper-triangular entries). The smallest singular value of block q decays
with depth at the rate **G(q) = max over |ζ| = 1 of the Green function of ℂ∖[z_min, z_max], in decades per row**. Verified in
140-digit arithmetic on the semi-infinite problem (W = 384; momenta π/6 … π): predicted 0.9605, 1.1381, 1.2984, 1.4352,
1.5508, 1.6527; computed 0.9555, 1.1326, 1.2952, 1.4360, 1.5540, 1.6786 (zigzag rate 1.6529 at W = 768); the minimum is in the
zigzag block q = π, so the cylinder's condition number grows by **1.65 decades per row**. The finite-height double-precision
data of the same blocks do not converge to this (increments still rising at 1.97 at d = 5 → 6 at height 14), and a closed
form I derived after seeing the first data (1.833) was wrong (LL-A17).
What this does and does not say. It explains the exponential-in-depth growth and a lattice constant on the cylinder: the
rate is set by the spread of the products of mode decay factors, i.e. by the lattice dispersion relation. It does **not**
explain the disk (1.1–1.2 decades per depth on the square disk, 1.7–1.8 on the triangular one: the square disk is below
the cylinder's 1.65): the disk has curvature, diagonal directions and graph-distance depth, and the triangular straight
periodic cylinder is exactly singular so it cannot even be compared (LL-A19). The structural statement of this note
(collective collapse of equal-depth signatures, f_d ∝ 1/d on flat disks, O(1) on hyperbolic tilings) is unaffected.
Open: the node set of the disk (angular momentum m with amplitude ((R−d)/R)^m instead of e^(−κ d)) and whether the same
Green-function exponent gives the disk's constant; whether the hyperbolic tilings' node structure explains their concave
growth. Neither is claimed.

## Orientation (2026-10-08, PREREGISTRATION_26, ledger H0-X-0017; post-hoc diagnostic marked)
The boundary orientation matters. For a square-lattice boundary along the diagonal (periodic strip, graph depth = L1 distance,
exact blocks verified against the explicit Jacobian to 0.001) the zigzag block loses 1.067 decades per row, against 1.653 for an
aligned boundary. The moduli-based Green exponent (1.403) and the naive 1/√2 scaling (1.169) are both wrong. A post-hoc
diagnostic finds that the node values are real after a common phase but of both signs, and the Green exponent of the signed
interval matches all six measured block rates to 0.85 % (LL-A20). This is a hypothesis to be tested out of sample
(preregistration 27: aligned strip with unequal conductances, positive real nodes, predictions fixed in advance). The disk's
constant (1.1–1.2 on the square disk) lies between the diagonal and the aligned values; how orientations, curvature and the
staircase boundary combine is not known.
**Out-of-sample test (PREREGISTRATION_27, H0-X-0018):** applied unchanged to the aligned strip with lateral conductance λ
(positive real nodes, new dispersion relation), the Green exponent predicts the converged zigzag rate at λ = 0.05 and 16 to
0.15 % and 1.9 % (1.762 and 2.498 against 1.765 and 2.451) and the six momenta of λ = 0.05 to 0.1–0.7 %; the zigzag rate is
non-monotone in λ (1.765, 1.653, 2.451 at λ = 0.05, 1, 16), and the λ-independent null is refuted. Two preregistered width
tolerances were too tight for the faster decay at λ = 16 (discrete-node drift), and the explicit reference gate failed at
λ = 0.05 because its height was too small (LL-A18); the post-hoc check shows exact = explicit at height 160. For complex
node sets (diagonal strip with unequal conductances) the interval formula does not apply.

## Curvature (2026-10-08, PREREGISTRATION_28, ledger H0-X-0019; pilots at R = 24 and 32 disclosed there)
On a polar-grid disk (square cells at the boundary, conductances from the continuum Laplacian; exact zigzag blocks verified against the
explicit Jacobian to four decimals) the per-row loss of σ_min **rises** with depth: at R = 48 from 1.605 at level 3 to 1.801 at level 24,
at R = 96 only to 1.675, and the level-3 value at R = 96 equals the aligned strip's (1.609 against 1.611). A local-strip argument
(lateral-to-vertical ratio λ_l = R²/(r_l r_{l+1/2}) and the aligned-strip rate G(λ)) predicts the sign and shape; the exact growth is 0.71
to 0.77 of the prediction (a band set from pilots, so a replication of a pilot regularity), and it scales with l/R to 13 %. So smooth curvature
of this type raises the rate by a few percent over the first quarter radius and cannot be why the square disk's constant (1.1–1.2) is below the
aligned strip's 1.65. The remaining candidates are the orientation dependence of the staircase boundary (the diagonal strip gives 1.07, the
aligned one 1.65, and the disk lies between) and boundary roughness; neither is tested here. An early pilot mistook the closed inner end of the
grid for curvature (LL-A18 again).

## Follow-up (2026-10-07, PREREGISTRATION_21, ledger H0-X-0013, exploratory)
Over windows fixed in relative depth (0.2 to 0.5 of d_max, extended to three depths on small disks), the rate is
flat in R from R = 10 upward: square 1.23, 1.20, 1.08 decades per depth (R = 10, 16, 22; 0.95 at R = 6), triangular
1.69, 1.81, 1.84 (R = 6.45, 10.75, 17.2; 0.41 on the two-layer R = 3.225 disk). So the R-dependence that refuted P3a
above was the window effect of LL-A15, and the rate is a **lattice constant**: about 1.1–1.2 on the square lattice,
1.7–1.8 on the triangular one. Both weak extrapolations of this card (rate increasing in R; triangular above square at
every size) were refuted, the first because the rate saturates, the second only on the two-layer disk. What the
argument above must now produce is this constant and its ratio (≈ 1.5) between the two lattices; the harmonic-measure
band argument fixes the form (1/d) but says nothing yet about the constant. Candidate next step (card Q5f): compute
the Fourier coefficients of the lattice harmonic measure on each disk and test whether the rate equals the decay
constant of the highest resolvable mode.
