# Preregistration 19: the coherence mechanism at matched size, and its link to κ (task Q5c)

**Date:** 2026-10-07, committed before the run. **Roadmap item:** H-2 (mechanism of concave-vs-linear κ in depth).
**Why:** H0-X-0010 found that equal-depth Jacobian columns keep an effective dimension fraction PR/n ≥ 0.79 on the
hyperbolic tilings while it falls to 0.14–0.39 on flat disks. Two gaps remain before this counts as the mechanism:
(i) the depth classes compared had different sizes (n = 6 to 152), and PR/n of a random set of columns depends on n;
(ii) the step from "columns of deep flat edges are collinear" to "κ grows linearly in depth" was argued, not measured.
This card closes both with matched-size subsampling and with the condition number of the Jacobian restricted to the
columns of depth ≤ d.

## Dry run (declared)
Per LL-A13, the statistics were tried on {7,3} L=2, square R=6 and triangular R=3.225 before the thresholds were set
(`$CLAUDE_JOB_DIR/tmp/dry19.py`, not part of the repository). **Those three instances are excluded from every prediction
below.** Dry-run values that informed the thresholds: matched PR/n at n = 6, depth 3: square 0.71, {7,3} 0.94;
κ(J restricted to depth ≤ d) on square R=6: 34, 397, 2.4×10³, 3.1×10⁴, 1.2×10⁵ for d = 0…4; on {7,3} L=2: 11, 98, 98,
290 for d = 0…3.

## Design
Scored instances: the largest of each family, {7,3} L=4, {8,3} L=4, {5,4} L=5, {6,4} L=4, {4,5} L=6, square R=10,
triangular R=6.45 (unit conductances, full boundary). Columns and depth classes as in preregistration 18.
1. **Matched-size coherence.** For every depth class with n_d ≥ 6, draw 50 random subsets of n_match = 6 columns
   (seed 0, NumPy default generator, draws in instance order) and record the median over draws of PR/6 of the
   normalised Gram of the subset. n_match = 6 is the smallest depth-3 class among the scored instances ({6,4} L=4).
2. **Restricted condition number.** κ_d = σ_max/σ_min of J restricted to the columns of edges of depth ≤ d, for
   d = 0 … d_max. Computed from the explicit Jacobian when it has ≤ 2×10⁸ entries, otherwise from the closed-form Gram
   matrix G = JᵀJ (κ_d = √κ(G_d)); the method is recorded per instance. Statistic: the mean per-depth increment
   beyond depth 1, Δ̄ = (log₁₀ κ_{d_max} − log₁₀ κ_1)/(d_max − 1) (depth 0 → 1 is a ≈1-decade jump everywhere and is
   not what distinguishes the classes). Also recorded: every log₁₀ κ_d, and λ_min of the normalised Gram per depth
   (not scored).
Data file: `data/coherence_mechanism_at_matched_size.json`; figure `data/fig_coherence_matched.pdf`.

## Validity gates
- G1 (consistency with H0-X-0008 and v1.0): every scored instance is matched by (N, E) to a row of
  `data/tilings_kappa.json` (the five hyperbolic ones; tolerance max(1e-6, 100 × its `log10_kappa_error_bound`)) or
  of `data/h0.json` (square R=10, triangular R=6.45; tolerance 1e-5 on log₁₀ κ, no error bound stored there), and
  log₁₀ κ_{d_max} agrees with the stored `log10_kappa`. All 7 must match.
- G2: every scored depth class used for prediction P1/P3 has n_d ≥ 6, and exactly 50 draws were made for it.

## Predictions (fixed now)
- **P1 (coherence at matched size).** At depth 3 with n_match = 6: median matched PR/n ≥ 0.85 for every hyperbolic
  scored instance, and ≤ 0.80 for square R=10 and triangular R=6.45. **Refuted if** any hyperbolic value < 0.85 or
  any flat value > 0.80.
- **P2a (κ growth per depth, absolute).** Δ̄ ≥ 0.8 decades per depth for square R=10 and triangular R=6.45;
  Δ̄ ≤ 0.5 for {7,3} L=4 and {8,3} L=4. **Refuted if** any of the four is on the wrong side.
- **P2b (κ growth per depth, ordering).** Every hyperbolic scored instance has Δ̄ below both flat values.
  **Refuted if** any hyperbolic Δ̄ ≥ either flat Δ̄.
- **P3 (deepest class).** At the deepest class with n_d ≥ 6, median matched PR/n < 0.6 for square R=10 and for
  triangular R=6.45, and ≥ 0.8 for every hyperbolic scored instance. **Refuted if** any value is on the wrong side.

## Not claimed
A derivation of Δ̄ from PR/n; the depth-0 → 1 jump; probe-subsampled boundaries; the {7,3}/{8,3} depth-1 dip of
H0-X-0010; anything about holography.
