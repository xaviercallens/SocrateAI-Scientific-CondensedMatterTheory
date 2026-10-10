# Preregistration 18: coherence versus depth across tilings (task Q5b)

**Date:** 2026-10-07, committed before the run. **Roadmap item:** H-2 (mechanism of concave-vs-linear κ in depth).
**Why:** H0-X-0008 found log κ concave in maximal depth on five hyperbolic tilings and linear on flat ones, and the
exploratory profile H0-X-0009 showed that the per-edge sensitivity *amplitude* decays alike on all of them. What
remains is the *direction* of the signatures: if many equal-depth edges have nearly collinear boundary signatures, the
Jacobian's smallest singular values shrink regardless of amplitude. Version 1.0 sampled this ("coherence_by_depth",
30 pairs per depth) but never analysed it. This card measures it exhaustively and tests the hypothesis that flat
lattices are more coherent at depth, increasingly so with depth.

## Design
Instances as in preregistration 16 ({7,3} L=1–4, {8,3} L=1–4, {5,4} L=1–5, {6,4} L=1–4, {4,5} L=1–6; square R ∈ {3, 6, 10};
triangular R ∈ {3.225, 6.45}), unit conductances, full boundary. For edges e, f with boundary signatures d_e, d_f
(d_e = H[a] − H[b] restricted to the boundary), the Jacobian columns are the upper-triangular parts of d_e d_eᵀ and
d_f d_fᵀ, and their inner product is ⟨J_e, J_f⟩ = ½[(d_e·d_f)² − Σ_i d_e,i² d_f,i²], so the cosine between columns is
computed in closed form without forming J. Edge depth = min(depth(a), depth(b)). For every depth class with n_d ≥ 2
edges, **all** n_d(n_d − 1)/2 pairs are used. Statistics per depth: median |cos|, mean |cos|, 90th percentile of |cos|,
and the **effective dimension fraction** f_d = PR_d / n_d, PR_d = (Σλ)²/Σλ² the participation ratio of the eigenvalues
of the n_d × n_d Gram matrix of the *normalised* columns (f_d = 1 for orthogonal columns, 1/n_d for collinear ones).
Data file: `data/coherence_versus_depth_across_tilings.json`; figure `data/fig_coherence_depth.pdf`.

## Validity gates
- G1 (closed form): on {7,3} L=2 and square R=6 the closed-form cosines agree with cosines computed from the explicit
  Jacobian of `hyperbolic_network.jacobian` to 1e-10 for every pair at every depth.
- G2: the number of pairs per depth equals n_d(n_d − 1)/2 for every instance.

## Predictions (fixed now; comparisons use the largest instance of each family that reaches the depth)
- **P1 (flat is more coherent at depth).** At every depth d ∈ {3, 4, 5}, the median |cos| of square R=10 and of
  triangular R=6.45 exceeds the median |cos| of every hyperbolic tiling that reaches d. **Refuted if** any flat
  instance is at or below any hyperbolic one at any of these depths.
- **P2 (the gap grows with depth).** The ratio median|cos|(square R=10, d) / median|cos|({7,3} L=4, d) is strictly
  increasing over d = 1, …, 5. **Refuted if** it decreases anywhere on that range.
- **P3 (effective dimension).** At depth 3, f_d of every hyperbolic tiling exceeds f_d of square R=10 and of
  triangular R=6.45 by at least a factor 1.5. **Refuted if** any hyperbolic tiling is below 1.5× either flat value.
- **P4 (depth 1 is not where the difference is).** At depth 1 the spread of median |cos| across all seven families is
  less than a factor 2 (max/min < 2). **Refuted if** ≥ 2.

## Not claimed
A derivation; the role of amplitude (H0-X-0009); probe-subsampled boundaries; anything about holography.
