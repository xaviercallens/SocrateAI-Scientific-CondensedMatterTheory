# Preregistration 30: persistent homology of the Jacobian column cloud as a topological proxy for ill-conditioning (task Q16)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2, topology and TDA thread. **Why:** earlier TDA work (preregistration 5, 6) applied persistent
homology to the boundary resistance metric and found that deep defects leave no topological signature. This card turns the tool on the object that carries the
conditioning result itself: the columns of the Jacobian J (one per edge). If the exponential growth of κ(J_d) with depth reflects columns of deep edges
becoming nearly parallel to those of shallower edges, a Vietoris–Rips filtration of the column cloud should show it as a collapse of the H₀ death times in deep layers,
and the polynomial growth on hyperbolic tilings should show as a slower collapse. This is a topological proxy, not a replacement for the singular values.

## Objects (fixed now)
Direct-current Jacobian columns J_e = upper(d_e d_eᵀ) as in the earlier cards, d_e the difference of the harmonic extension rows at the endpoints of e. The
inner product of two columns over the strictly upper triangle is ⟨J_e, J_f⟩ = ½[(d_e·d_f)² − Σ_i d_{e,i}² d_{f,i}²], so no J is formed. Distance between edges:
δ(e,f) = sqrt(1 − c²), c = ⟨J_e,J_f⟩ / (‖J_e‖‖J_f‖) (sine of the angle between the lines; sign-invariant); c² is clipped to [0,1].
For each depth k (depth = smaller of the endpoint distances to the boundary), the layer cloud is the edges of depth exactly k. GUDHI (3.13) Vietoris–Rips on the layer's
distance matrix gives the H₀ diagram; the death times of the finite H₀ classes are the single-linkage merge heights. The layer statistic is
**m_k = median H₀ death time of layer k**. H₁ is computed for diagnostics only (total persistence), not scored.
Geometries: square disk radius 16 (layers k = 2…9 scored) and the {7,3} tiling with 5 layers (layers k = 1…4 scored; the deepest layer is a thin boundary-adjacent set and is excluded).
Double precision; layers whose m_k falls below 1e-6 are flagged as at the precision floor and dropped from the fit (rule fixed now).
Reference quantities from the same run: log₁₀ σ_min(J_{≤k}) and log₁₀ κ(J_{≤k}) by SVD of the column-restricted Jacobian built explicitly for the square disk (size permitting) and via the Gram
matrix for {7,3}.
Control: a random cloud with the same layer sizes, columns drawn as independent unit Gaussian vectors in the same ambient dimension, should show no collapse.

## No run before this commit
No H₀ death time of a Jacobian column cloud has been computed. The depth profile of κ is known from earlier cards (about 1.1–1.2 decades per step on the square disk).

## Predictions (fixed now, before the run)
- **P1 (collapse on the square disk).** log₁₀ m_k decreases with k on the scored layers with Spearman correlation ≤ −0.9.
- **P2 (flat versus hyperbolic).** The fitted slope of log₁₀ m_k against k is smaller in magnitude on {7,3} than on the square disk: |slope_{7,3}| < |slope_square|.
- **P3 (tracks the conditioning).** On the square disk the Pearson correlation between log₁₀ m_k and log₁₀ σ_min(J_{≤k}) over the scored layers is at least 0.9.
- **P4 (magnitude).** The square-disk slope of log₁₀ m_k against k lies between −1.5 and −0.3 decades per layer (the exponential rate of σ_min is about −1.2 and the nearest-neighbour angle need not follow it exactly).

## Validity gates
- G1 (control): the random-cloud control has |slope of log₁₀ m_k against k| < 0.02 on the same layers.
- G2 (known answer): on a toy cloud of columns that are exactly duplicated in pairs (two copies of every column in a small square disk, R = 4), every layer's median death time is 0 within 1e-12.
- G3 (clipping): fewer than 1 % of the pairwise c² values need clipping.

## What a refutation would mean (written now)
P1 refuted: nearest-neighbour structure of the columns does not collapse with depth, so ill-conditioning is not a nearest-neighbour phenomenon and the single-linkage
H₀ is blind to it (it would sit in the global linear dependence among many columns). P2 refuted: the proxy does not separate flat from hyperbolic. P3 refuted:
the proxy and the singular values decouple. P4 refuted: the collapse is real but its size is not tied to the singular-value rate. G1 failed: the cloud's concentration of measure explains the collapse and nothing below is read.

## Not claimed
That persistent homology gives a stable estimate of κ; that H₁ means anything here; that the result transfers to noisy data; a topological invariant of the inverse problem; anything about holography.
