# Preregistration 9: where does localisation fail? A noise sweep (follow-up to prereg 8's 60/60 ceiling)

**Date:** 2026-09-28, committed before the run. **Why:** prereg 8 returned top-1 = 1.00 in all 60 cells at noise
3×10⁻⁴, which is a ceiling and says nothing about the failure boundary (lesson LL-A10). Same decoder, same
dictionary, same setup as `PREREGISTRATION_8.md`; only the noise level changes.

## Design
Deepest interior nodes (the deepest class), contrasts f ∈ {1.25, 2}, four lattices, noise ε ∈ {1e-3, 3e-3, 1e-2, 3e-2,
1e-1, 3e-1}, 20 trials per cell (fresh noise each trial, seeded). Metric: top-1 node accuracy.
**ε_loc** = the largest grid ε at which top-1 ≥ 0.9 with every smaller grid ε also ≥ 0.9 (0 if even 1e-3 fails;
"> 3e-1" if none fails).

## Predictions (fixed now; from a matched-filter argument)
For minimum-distance decoding in i.i.d. Gaussian noise the error probability is governed by d/(2σ), d being the
Frobenius distance between hypotheses and σ the per-entry noise. The detection SNR of prereg 6/7 (signal ÷ norm-level
noise floor, ≈ 40× for the ×100 defect on square R=10) undercounts d/σ by a factor of order m (number of boundary
probes), and requiring a few thousand hypotheses to be separated needs d/(2σ) ≳ 4.5. Scaling from the ×2 deep signals
(1.4×10⁻² on {7,3} L=3, 1.7×10⁻³ on square R=10; H3-X-0004) gives order-of-magnitude thresholds ε_loc ≈ 4×10⁻³
(square R=10, ×2) and ≈ 3×10⁻² ({7,3} L=3, ×2), with a factor-3 uncertainty either way.
- **S1 (flat lattice fails at last).** Square R=10, ×2: top-1 ≥ 0.9 at ε = 1e-3 and ≤ 0.5 at ε = 1e-1, i.e.
  ε_loc ∈ [1e-3, 3e-2).
- **S2 (hyperbolic lattice tolerates more).** {7,3} L=3, ×2: top-1 ≥ 0.9 at ε = 1e-2.
- **S3 (the advantage is a ratio of noise tolerances).** ε_loc({7,3} L=3) ≥ 3 × ε_loc(square R=10) at both f = 2 and
  f = 1.25.

**Refutation:** any of S1–S3 failing; if the flat lattice never fails within the grid (top-1 ≥ 0.9 up to 3e-1) or
fails at 1e-3, the matched-filter scaling argument is wrong.

## Not claimed
Tolerance, extended or multi-node defects, unknown contrast sets, non-Gaussian noise (as in prereg 8). Nothing about
holography.
