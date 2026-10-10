# Preregistration 32: depth-ordered residuals of the Jacobian columns against σ_min and against the column-cloud topology (task Q16, next step)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2, topology thread. **Why:** preregistration 30 found that the nearest-neighbour topology of the Jacobian
column cloud collapses only like 1/depth while σ_min collapses exponentially, and concluded that the ill-conditioning lives in the linear dependence among many columns.
This card tests that reading directly with the quantity that measures that dependence: the distance of a column to the span of the columns that precede it, and asks how much of σ_min's exponential rate it captures.

## Exact facts (not predictions; two are checked as gates, the first is formalised in Lean)
For a matrix with columns a_i and a lower bound σ on ‖Ax‖/‖x‖: σ ≤ distance of any column a_j to the span of the other columns (`le_residual` in `lean/dtn_offsets/GramSchmidtBound.lean`;
the identification of σ with σ_min is standard linear algebra and not formalised). With r_j the leave-one-out residual, r_j² = 1/(G⁻¹)_jj, G = JᵀJ, hence min_j r_j / √n ≤ σ_min ≤ min_j r_j.
The depth-ordered residual |R_jj| of Householder QR with columns sorted by depth (distance to the span of the columns before j) is at least r_j, because its span is smaller.
So for J_{≤k}: σ_min(J_{≤k}) ≤ min_j r_j ≤ min_j |R_jj|. Also, the distance s_e to the span of strictly shallower layers is at least |R_ee|.
Not found yet in a reference I could verify (alphaXiv was unavailable): the identity r_j² = 1/(G⁻¹)_jj is standard; no citation is claimed.

## Pilot (disclosed; square disk radius 10; excluded from scoring)
Before this card I ran the quantities below on the radius-10 square disk (`exp32_pilot_residuals.py`, `exp32_pilot_residual_cloud.py`; outputs in the commit message of this card). Layers 1 to 8: log₁₀ σ_min(J_{≤k}) falls from −2.84 to −9.71 (about 0.98 per layer),
the layer minimum of the ordered residual ρ_k falls from −2.54 to −9.30 (about 0.97 per layer) and stays 0.3 to 0.9 decades above σ_min; the leave-one-out minimum stays 0.25 to 0.5 decades above σ_min; the minimum shallower-span residual s_k stays 0.2 to 1.2 decades above ρ_k;
the median of s_e/‖J_e‖ falls from 0.50 to 1e-4 over layers 1 to 7 (about 0.6 to 0.8 decades per layer); the H₀ median death time of the residual cloud is below that of the original cloud for layers 1 to 5 and about equal or above for layers 6 to 8 (not scored). No computation at radius 16 or on {7,3} was made before this commit.

## Design
Householder QR (`numpy.linalg.qr`, mode `r`) of the explicit Jacobian (direct current, `jac_s(g, 0)`) with columns stably sorted by depth. Square disk radius 16; {7,3} with 5 layers. For every layer k: σ_min(J_{≤k}) by SVD; ρ_k = min over the layer of |R_ee|;
the leave-one-out minimum from R⁻¹ (r_j = 1/‖row j of R⁻¹‖); s_k = min over the layer of the distance to the span of strictly shallower layers (QR of J_{<k}, projection); the median of s_e/‖J_e‖ over the layer.
**Window rule (fixed now):** the scored layers are those k ≥ 2 with σ_min(J_{≤k}) ≥ 1e-12 (about four decades above the double-precision resolution of an SVD with ‖J‖ ≈ 1); at least five layers are required, otherwise the card reports a Deviation.
Slopes are least-squares slopes of log₁₀ quantity against k over the scored layers. Data file: `data/depth_ordered_residuals_of_jacobian_columns.json`.

## Validity gates
- G1: the exact chain σ_min(J_{≤k}) ≤ min_j r_j ≤ ρ_k ≤ s_k holds on every scored layer, with relative slack 1e-9 (a violation means a numerical or coding error).
- G2: ‖QR − J_sorted‖_F / ‖J‖_F ≤ 1e-12 for the explicit QR used.
- G3: on the radius-4 square disk, r_j from R⁻¹ equals 1/sqrt(diag((JᵀJ)⁻¹)) within 1e-8 relative.

## Predictions (fixed now, before the radius-16 and {7,3} runs)
- **P1 (the ordered residual carries the rate).** On the square disk, the slope of log₁₀ ρ_k lies in [0.85, 1.15] times the slope of log₁₀ σ_min(J_{≤k}).
- **P2 (bounded looseness).** For every scored layer, 0 ≤ log₁₀ρ_k − log₁₀σ_min(J_{≤k}) ≤ 1.5 (the lower bound is exact).
- **P3 (depth costs more than the same layer).** For every scored layer, 0 ≤ log₁₀ s_k − log₁₀ ρ_k ≤ 1.5 (the lower bound is exact), and the mean over the scored layers is at least 0.5.
- **P4 (the dependence is exponential).** The slope of log₁₀(median over layer of s_e/‖J_e‖) against k is between −1.2 and −0.4 per layer, with Pearson correlation ≤ −0.98.
- **P5 (hyperbolic).** On {7,3} (layers 1 to 4, all scored regardless of the floor rule if σ_min ≥ 1e-12): |slope of log₁₀ρ_k| is smaller than the square disk's, and 0 ≤ log₁₀ρ_k − log₁₀σ_min ≤ 1.5 on every layer.
- **P6 (the contrast with preregistration 30).** On the square disk, |slope of log₁₀ median s_e/‖J_e‖| is at least 5 times |slope of log₁₀ m_k| of the nearest-neighbour cloud over the same layers (m_k from `data/jacobian_column_cloud_homology.json`).

## What a refutation would mean (written now)
P1 refuted: the depth-ordered Gram–Schmidt residual misses a part of σ_min's rate (the small singular direction is not aligned with the last column of an ordering by depth). P2 refuted: the certificate is looser than 1.5 decades and cannot serve as a proxy.
P3 refuted: same-layer dependence is a larger part of the loss than the pilot suggested, or the loss is nearly all depth. P4 refuted: the distance to the span of shallower columns is not exponential in depth at radius 16. P5 refuted: the hyperbolic tiling shows the same collapse at this size (or the proxy breaks there).
P6 refuted: the nearest-neighbour topology is not much weaker than the dependence measure, contrary to the reading of preregistration 30. G1 failed: a numerical error and nothing is read.

## Not claimed
That the residual is a topological invariant; that the result holds with noise; any statement beyond double precision and these two geometries; that the H₀ comparison of the residual and original clouds (reported unscored) means anything; anything about holography.

## Deviation 1 (2026-10-08, written after two launches were killed for memory and before any residual number existed)
Both launches (the first while a Lean build was running, the second alone with about 22 GB available) were killed by the system (exit status 137) after gate G3 passed (1.6e-14) and before any layer table was printed; no data file exists.
Cause, my design error: the preregistration asked for Householder QR of the explicit Jacobian on the {7,3} tiling with 5 layers, but `build_hyperbolic(7, 3, 5)` is a network of several thousand nodes whose boundary has on the order of a thousand nodes, so the explicit Jacobian has
about a million rows and tens of gigabytes. (Preregistration 30 used the Gram matrix on this tiling for that reason, and I did not carry the lesson over.)
Change, made now: on {7,3} (and only there) the quantities are computed from the column Gram matrix G = JᵀJ (entries ½[(d_e·d_f)² − Σ d_e,i² d_f,i²], E×E) by Cholesky: with G_sorted = RᵀR (columns sorted by depth), ρ_j = R_jj, the leave-one-out residuals come from R⁻¹ as before,
σ_min(J_{≤k}) = sqrt(λ_min of the leading block of G), and the distance to the span of strictly shallower layers is the square root of the Schur complement G_ee − G_e,prev G_prev⁻¹ G_prev,e. This squares the condition number, so it is valid only while κ(J)² is well below 1/eps; on {7,3} log10 κ is about 4 (preregistration 29), far inside that.
The square disk keeps Householder QR as preregistered. New gate G4 (added now): on the radius-6 square disk the Gram/Cholesky route reproduces ρ_k, σ_min and the median relative shallower residual of the Householder route within 1e-6 relative for layers 1 to 3.
The floor rule is applied on {7,3} as preregistered (σ_min ≥ 1e-12 is trivially met). Predictions P1 to P6 and gates G1 to G3 are unchanged.
