# Preregistration 12: minimum detectable contrast (task Q3)

**Date:** 2026-09-28, committed before the run (script unrun at commit time). **Roadmap item:** H-3.
**Why:** localisation results so far used contrasts f ≥ 0.8 or ≤ 1.25 at most (H3-X-0005..0007); realistic faults
(a drifted or mis-valued component) are ±10–50 %. This card finds the smallest single-node contrast that a board can
still localise, at the precision budget and around it, following H3-X-0004 (the signal is antisymmetric in log f near
f = 1 and saturates for large f) and H3-X-0006 (noise margins).

## Design
Same decoder and dictionary construction as `localize_noise.py` (ideal board, matched filter over all interior nodes,
dictionary contrasts D = {0.1, 0.5, 0.8, 0.9, 1.1, 1.25, 1.5, 2, 5, 10, 100}, differential measurement with independent
i.i.d. Gaussian noise ε on each map). Deepest class of each of the four lattices ({7,3} L=2, square R=6, {7,3} L=3,
square R=10). True contrasts f ∈ {0.5, 0.8, 0.9, 1.1, 1.25, 1.5, 2}; noise ε ∈ {1e-4, 3e-4, 1e-3, 3e-3}; 20 trials per
cell (node cycles through the class, fresh noise per trial, seeded). Metric: top-1 node accuracy.
**f_min(ε)** = the smallest |log f| among tested contrasts on each side of 1 with top-1 ≥ 0.9 at that ε.
Data file: `data/minimum_detectable_contrast.json`.

## Validity gates (results are reported only if all pass)
- G1: at ε = 3e-4 and f = 2 every lattice has top-1 ≥ 0.9 (reproduces H3-X-0005 within sampling error).
- G2: the dictionary contains every true contrast (no decoder mismatch by construction).

## Predictions (fixed now; from the H3-X-0004 signal curve and the H3-X-0006 margins)
- **P1 (budget, hyperbolic):** at ε = 3e-4, {7,3} L=3 localises f = 1.1 and f = 0.9 with top-1 ≥ 0.9.
  **Refuted if** either is < 0.9.
- **P2 (budget, flat):** at ε = 3e-4, square R=10 has top-1 ≤ 0.5 at f = 1.1 and at f = 0.9 (its f = 1.25 signal is
  ≈ 5e-4, only ≈ 3× its noise floor, and a ±10 % contrast is ≈ 2.4× weaker). **Refuted if** either is > 0.5.
- **P3 (symmetry):** for every lattice and ε, top-1 at f = 0.9 and at f = 1.1 differ by ≤ 0.2, and likewise at 0.8 vs
  1.25 (the log-antisymmetry of H3-X-0004). **Refuted if** any pair differs by > 0.2.
- **P4 (ordering):** at every ε and every f, top-1({7,3} L=3) ≥ top-1(square R=10) − 0.1. **Refuted if** any cell
  violates it.

## Not claimed
Anything with component tolerance (H3-X-0007 covered it for f ≥ 1.25 only), multi-node defects, contrasts outside D,
non-Gaussian noise, or sizes beyond N ≈ 317. Nothing about holography.
