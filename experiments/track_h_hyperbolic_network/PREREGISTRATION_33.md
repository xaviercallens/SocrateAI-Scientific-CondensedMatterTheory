# Preregistration 33: do learned persistence features of the Jacobian column cloud predict conditioning, and do they transfer between geometries? (task Q18)

**Date:** 2026-10-10, committed before the run. **Roadmap item:** H-2, topology thread (GUDHI / machine learning). **Why:** preregistrations 30 and 32 found that nearest-neighbour persistent homology of the
Jacobian column cloud sees depth as a power law while the depth-ordered residual and σ_min fall exponentially. Two questions remain that only a learned representation can answer: (1) does the *whole* persistence diagram
of a layer (not its median death time) carry the exponential information, once vectorised (persistence image, landscape, Atol quantisation) and fed to a regressor; (2) do features learned on flat geometries transfer to
the hyperbolic tiling and to other flat tilings, or is the map from topology to conditioning geometry-specific? A negative answer to (1) closes the topological route for conditioning; a negative answer to (2) says the proxy cannot replace the certificate.

## Objects (fixed now)
Unit-normalised direct-current Jacobian columns, grouped into depth layers as before. Per layer two clouds: (a) the column cloud with sine distance (as preregistration 30); (b) the residual cloud (columns projected off the span of
strictly shallower layers, renormalised, sine distance). Vietoris–Rips H₀ and H₁ diagrams (GUDHI, all pairs). Features per layer and cloud: persistence image (bandwidth 0.05, 10×10 on [0,1]², H₀ and H₁), persistence landscape (5 landscapes, 20 samples, H₀ and H₁), Atol
quantisation (8 centres fitted on the training set, H₀ and H₁), and the scalar from preregistration 30 (median H₀ death time). Concatenated feature vector length is fixed by these choices and not tuned.
Targets per layer: y₁ = log₁₀ σ_min(J_{≤k}) and y₂ = log₁₀ ρ_k (minimum depth-ordered residual of the layer, preregistration 32); both are computed with the same codes as before (SVD / Householder QR on flat disks, Gram/Cholesky on {7,3}).
Geometries: flat training set = square disks of radius 8, 10, 12, 14, 16 (layers 2 up to the floor rule σ_min ≥ 1e-12) and triangular disks of radius 8, 10, 12 (same rule); held-out flat test = square disk radius 18; hyperbolic test = {7,3} with 5 layers (layers 1 to 4) and {5,4} with 4 layers (all layers with σ_min ≥ 1e-12).
Model: ridge regression (regularisation chosen by leave-one-geometry-out cross-validation within the training set, grid 10⁻³…10³) and a gradient-boosted tree regressor (scikit-learn, 200 trees, depth 3, fixed). Scores: coefficient of determination R² and root-mean-square error in decades on held-out data.
Baselines: (i) depth k alone (a one-feature ridge on k), (ii) the median death time alone, (iii) layer size alone.

## Pilot (disclosed; square disk radius 8; excluded from scoring)
Script `exp33_pilot_filtrations.py`, run before this commit. Per layer 1 to 6: H₀ median death of the column cloud 0.94, 0.90, 0.73, 0.54, 0.44, 0.38 (monotone); H₁ total persistence 0.36, 0.57, 0.61, 0.49, 0.85, 0.50 (non-monotone); residual-cloud H₀ median 0.89, 0.64, 0.51, 0.36, 0.42, 0.48 (non-monotone after layer 4);
log₁₀ median residual −0.30, −0.66, −1.01, −1.47, −2.18, −3.11 (exponential). This fixed the choice of targets and the decision not to score H₁ scalars; no model was trained before this commit.

## No run before this commit
No persistence image, landscape or Atol feature of any layer has been computed except in the pilot above (radius 8 only, no model); no regressor has been fitted.

## Validity gates
- G1 (leak check): a regressor trained on randomly permuted targets within the training set has held-out R² ≤ 0.1 on the flat test disk (otherwise the features encode the target by construction, e.g. through layer size).
- G2 (reproducibility): two runs with different random seeds for the tree model change the flat-test RMSE by less than 0.1 decades.
- G3 (targets): the σ_min and ρ values for the radius-16 square disk reproduce those stored by preregistration 32 to 1e-9 relative.

## Predictions (fixed now, before the run)
- **P1 (the diagram does not beat the residual).** On the flat test disk the best topological model's RMSE for y₁ is at least 0.3 decades, while predicting y₁ from y₂ by a one-feature ridge gives RMSE below 0.2 decades (the certificate is the better predictor).
- **P2 (the diagram does beat depth alone).** On the flat test disk the best topological model's RMSE for y₁ is below that of the depth-only baseline by at least 0.1 decades.
- **P3 (no transfer to hyperbolic).** Trained on flat geometries, the best topological model's R² for y₁ on the {7,3} test is ≤ 0.5, and its RMSE exceeds the flat-test RMSE by at least a factor 2.
- **P4 (the residual cloud is not more informative).** Features of the residual cloud (b) alone do not improve the flat-test RMSE over features of the column cloud (a) alone by more than 0.05 decades.
- **P5 (ordering of geometries).** For every model, held-out RMSE ordered: flat square < hyperbolic {7,3}; and the {5,4} tiling behaves like {7,3} (R² ≤ 0.5).

## What a refutation would mean (written now)
P1 refuted: the full diagram carries the exponential information that its median did not, and the topological route is competitive with the certificate. P2 refuted: topology adds nothing beyond depth, and the route is closed. P3 refuted: the topology-to-conditioning map
transfers to hyperbolic geometry, which would be a real and unexpected regularity. P4 refuted: the principal-angle (residual) cloud is where the information is, and preregistration 32's reading needs a topological counterpart. P5 refuted: the hyperbolic geometries are not harder, or {5,4} differs from {7,3}.
G1 failed: features leak the target and nothing is read. G2 failed: the models are unstable and only ridge is reported.

## Not claimed
Anything about noisy data; that persistence features are a practical conditioning estimator (the certificate is cheaper); a topological invariant of the inverse problem; that the tiling list is representative; anything about holography.

## Amendment 1 (2026-10-10, written after the literature review and before any feature or model was computed)
The review (docs/LITERATURE_REVIEW_TDA.md, section 4) found that the persistent-Laplacian literature (Memoli-Wan-Wang arXiv:2012.02808; Wang-Nguyen-Wei arXiv:1912.04135) states that persistent homology is blind by design to the non-harmonic
spectral content of a filtration, and that the persistent Laplacian carries it. That is the natural objection to paper 2. It is pre-empted here by one more measured quantity and one more prediction, fixed now.
**Quantity.** For the column cloud (a) of each layer, the weighted graph Laplacian of the complete graph with edge weights w_ef = 1 − δ(e,f)² = c_ef² (the squared cosine between column lines; w = 1 for identical lines, 0 for orthogonal ones), and its spectrum. Its smallest
non-zero eigenvalue λ₂ (the algebraic connectivity of the cosine-squared graph) is a zero-dimensional spectral quantity in the sense of the persistent-Laplacian framework at the full filtration level; it depends on the whole weighted graph and not on nearest neighbours. Feature: log₁₀ λ₂ and the lowest five non-zero eigenvalues, appended as a fourth feature block "L".
**Prediction P6 (spectral features carry more than persistence).** On the flat test disk, ridge regression on the block L alone predicts y₁ with RMSE at least 0.1 decades lower than the best persistence-only model (A, B or AB); and its hyperbolic R² is also ≤ 0.5 (the geometry dependence is not removed by the spectral route).
**What a refutation would mean.** First clause refuted: the spectral quantity of the column graph does no better than persistence, and the objection is answered the other way (the information is not in the pairwise structure at all, spectral or topological, but in the ordered span). Second clause refuted: the spectral features transfer, which would be a regularity worth its own card.
No other prediction, gate or band is changed. Gate G1 (leak check) is applied to the best model over all blocks.
