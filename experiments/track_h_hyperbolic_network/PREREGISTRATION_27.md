# Preregistration 27: the aligned strip with unequal conductances, an out-of-sample test of the node picture (task Q5j)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2. **Why:** the node picture (the smallest singular value of
the momentum block decays at the Green-function exponent of the set of node values) has now been fitted twice after the
fact: the aligned boundary (preregistration 25, where the Green form was found while diagnosing a wrong closed form) and the
diagonal boundary (preregistration 26, where a signed-node correction was found after the data; LL-A17, LL-A20). A
parameter-free picture that has only been checked on cases it was adjusted to has not been tested. This card applies it,
unchanged, to a family it has not seen: the aligned strip with lateral conductance λ and vertical conductance 1, where the
dispersion relation becomes cosh κ(k) = 1 + λ(1 − cos k) and the node values stay real and positive, so the interval formula
applies exactly as in preregistration 25. (The diagonal strip with unequal conductances is not usable: its nodes are
complex, imaginary parts up to 0.16 against moduli up to 0.2, checked before this card.)

## The picture and the predictions (fixed now)
Blocks as in preregistration 25 with z₁(k) = e^(−acosh(1 + λ(1 − cos k))): V[n, r] = a_n z_n^r, z_n = z₁(k_n)z₁(q − k_n),
a_n = (1 − z₁(k_n))(1 − z₁(q − k_n)), the position-diagonal direction projected out. The block's rate is the Green exponent
of [z_min, z_max] on |ζ| = 1, evaluated by the prediction function before this card was written, W = 384 (the same to four digits
at W = 768 for the zigzag block), momenta labelled as in preregistrations 25 and 26 (i = 8, …, 48 at W = 96 ↔ q = π/6 … π):
- λ = 0.05: **1.1406, 1.2331, 1.3393, 1.4606, 1.6005, 1.7649**
- λ = 16: **1.4232, 1.8700, 2.1442, 2.3140, 2.4112, 2.4505**
- (for reference, λ = 1, preregistration 25: 0.9605, 1.1381, 1.2984, 1.4352, 1.5508, 1.6527.)
The dependence on λ is non-monotone (the zigzag rate is 1.765 at λ = 0.05, 1.653 at λ = 1, 2.451 at λ = 16), which is what makes
it a test. **Rival (null):** the zigzag rate does not depend on λ and equals 1.6527.

## Design
Exact blocks (mpmath, **220 digits** because the λ = 16 rates are near 2.5 decades per row), vertical-edge columns, W = 384,
depths 0…25; σ_min by inverse Gram and power iteration as in preregistration 25; rate = (log₁₀σ_min(15) − log₁₀σ_min(25))/10; six
momenta; σ_min at depth 20 for every block i = 0…192; the zigzag block at W = 768. Both λ in one run. Data file:
`data/aligned_strip_with_unequal_conductances.json`.

**Disclosure.** Before this card was committed I ran the block code once at λ = 16, W = 96 for depths up to 4 as an infrastructure
check; the per-row increments were 2.41, 2.40, 2.46 and 2.54, consistent in size with the prediction of 2.45 but outside the
test window (depths 15 to 25) and at a width where the window is impossible. No other λ = 0.05 or λ = 16 block was computed.

## Validity gate
- G1: for each λ, the exact zigzag block (W = 96) has per-row increments of log₁₀σ_min for d = 1…5 within 0.02 of those of the
  explicit double-precision block of the Jacobian of a W = 96, height-40 cylinder with lateral conductances λ (the script
  recomputes it). Failure means the block formula is wrong for λ ≠ 1 and nothing else is read.

## Predictions (fixed now)
- **P1 (zigzag rate).** For both λ the zigzag rate at W = 768 is within 3 % of the Green value (1.7649, 2.4505).
- **P2 (rate as a function of momentum).** For both λ the six rates at W = 384 are each within 6 % of the Green values above
  (the tolerance allows for the discrete-node drift seen in preregistration 25, up to 1.6 % there).
- **P3 (dominant block).** For both λ the block with the smallest σ_min at depth 20 is the zigzag block i = 192.
- **P4 (width).** For both λ the zigzag rate at W = 768 is within 3 % of the one at W = 384 (looser than the 1 % of
  preregistration 25, which was missed at 1.5 %).
- **P5 (the null fails).** For both λ the zigzag rate at W = 768 exceeds 1.6527 by at least 4 % (predicted +6.8 % and +48 %).

## What a refutation would mean (written now)
G1: block formula wrong off λ = 1. P1 or P2 refuted: the node picture does not carry over to a different dispersion relation
and the earlier agreement was specific to λ = 1 (so far, two fitted cases). P3 refuted: the dominant block moves with λ.
P4 refuted: stronger anisotropy needs wider strips. P5 refuted: the rate is insensitive to λ and the Green form's
λ-dependence is spurious.

## Not claimed
The diagonal strip with unequal conductances (complex nodes); the horizontal-edge columns; the disk or curvature; hyperbolic
geometry; a proof; anything about holography.
