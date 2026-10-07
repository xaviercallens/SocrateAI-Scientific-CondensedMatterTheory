# Preregistration 16: sensitivity versus depth across tilings (task Q5, EXPLORATORY)

**Date:** 2026-09-28, committed before the run. **Roadmap item:** H-2 (open question "why is log κ concave in depth
for hyperbolic tilings and linear for flat ones?", `TILINGS_RESULTS.md`, ledger H0-X-0008).
**Status:** exploratory. No prediction is made; the output is a measured profile that a later derivation attempt or
preregistration can use. The ledger entry will be marked EXPLORATORY and cannot support any claim on its own.

## Design
For every instance of `tilings_kappa.py` ({7,3} L=1–4, {8,3} L=1–4, {5,4} L=1–5, {6,4} L=1–4, {4,5} L=1–6) and the
flat disks square R ∈ {3, 6, 10} and triangular R ∈ {3.225, 6.45}: unit conductances, full boundary, harmonic extension
H; per-edge sensitivity S_e = ‖∂Λ/∂g_e‖_F = ‖d_e‖², d_e = H[a] − H[b] restricted to the boundary (the Frobenius norm of
the rank-one matrix d_e d_eᵀ). Edge depth = min(depth(a), depth(b)). Recorded per instance: mean and median of
log₁₀ S_e per edge depth, the number of edges per depth, the least-squares slope of mean log₁₀ S_e against depth
(the per-depth decay rate), and the same slope restricted to depths ≥ 1.
Data file: `data/sensitivity_versus_depth_across_tilings.json`; figure `paper/fig_sensitivity_depth.pdf` (not in the
paper).

## Validity gates
- G1: for {7,3} L=1–4 the mean sensitivity per depth reproduces `data/h0.json` ("sensitivity_by_depth", normalised to
  depth 0 = 1) to 1e-6 relative at every depth.
  **Deviation 1 (2026-09-28, after the first run; no prediction exists in this exploratory card, so nothing was at
  stake).** G1 as written cannot pass: `data/h0.json`'s statistic is the *median* per depth of the Jacobian column
  2-norm ‖J[:,e]‖₂ = (½[(‖d_e‖²)² − Σ_i d_e,i⁴])^{1/2} (upper-triangular boundary pairs), normalised to depth 0, while
  the profile above uses the *mean* of ‖d_e‖². Amended G1: the script also computes the h0 statistic exactly and
  must reproduce h0 to 1e-6; the profile of ‖d_e‖² is reported alongside, unchanged. First-run values (G2 passed,
  G1 failed) are kept in the git history of the data file.
- G2: every instance's edge count per depth sums to E.

## Not claimed
Any mechanism. Exploratory: nothing here confirms or refutes anything; nothing about holography.
