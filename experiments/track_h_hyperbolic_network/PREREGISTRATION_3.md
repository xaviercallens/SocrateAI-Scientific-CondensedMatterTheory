# Preregistration 3: revisions requested by the v1.0 peer review

**Date:** 2026-09-27, committed before any of the computations below were run.
**Trigger:** the peer review of v1.0 (`paper/reviews/REVIEW_2026-09-27_v1.0.md`), recommendations 1–4.
**Inputs used to set predictions:** only the published v1.0 data (`data/h0.json`, `data/identifiability.json`); the fit numbers are in `data/prereg3_predictions.json`, produced by `prereg3_predictions.py`.

Rules as before: rival forms and refutation criteria are fixed here; a deviation is reported as a deviation; every number in the paper is regenerated from the data files.

---

## A. Flat-lattice scaling law beyond double precision (review recommendation 1)

**Question.** For square and triangular disks, does log₁₀κ grow like c·√N (the paper's depth mechanism, since d_max ~ √N and log κ grows linearly with depth) or like a power law p·log₁₀N?

**Method.** Ball arithmetic (python-flint / Arb, 512 bits). The harmonic extension H is solved in Arb from the integer Laplacian; the Gram matrix G = JᵀJ of the sensitivity Jacobian is formed in Arb by the closed form
G_ef = ½[(d_e·d_f)² − (d_e²·d_f²)] (d_e = h_a − h_b restricted to the boundary), so J is never materialised; λ_min(G) is obtained as 1/λ_max(G⁻¹) with G⁻¹ computed in Arb, λ_max(G) in float64 from G. κ = √(λ_max/λ_min). The Arb radii are checked: a result is reported only if the relative radius of every G⁻¹ entry is below 1e-20; otherwise the precision is doubled and the run repeated.

**Control (must pass before any saturated size is reported).** On the unsaturated cases square R=10 (N=317) and triangular R=6.45 (N=151), the Arb value of log₁₀κ must agree with the float64 value of v1.0 (9.7178, 8.6724) to within 1e-6.

**Predictions** (fits on unsaturated points only; `data/prereg3_predictions.json`):

| Case | N | exp(c√N) predicts log₁₀κ | power law predicts (global fit / last local exponent) |
|---|---|---|---|
| square R=16 | 797 | **16.42** (c = 0.644) | 12.30 / 13.87 |
| triangular R=10.75 | 421 | **15.63** (c = 0.846) | 12.5 / 12.5 |
| triangular R=17.2 | 1069 | **25.94** | 15.98 / 15.98 |

**Prediction:** the exp(c√N) form. **Decision rule:** for each family, the form is *supported* if every measured value lies within ±2.0 decades of its extrapolation and the other form's extrapolation misses by more than 2.0 decades at the largest size. The exp form is **refuted** if the local exponent d log κ / d log N between the last unsaturated point and the first saturated point is *not larger* than the previous local exponent (a power law has a constant exponent; the depth mechanism requires it to keep increasing), or if any measured value misses 16.42 / 15.63 / 25.94 by more than 2.0 decades. If both forms miss, neither is claimed and the numbers are reported as-is.

**Sizes.** All three saturated instances. If the N=1069 run exceeds 6 h or 20 GB it is reported as not run.

## B. Inhomogeneous conductances (review recommendation 2)

**Question.** Does the hyperbolic conditioning advantage survive disorder and a high-contrast defect?

**Parametrisation.** Primary metric: κ of the *log-parametrised* Jacobian ∂Λ/∂ln g_e = g_e ∂Λ/∂g_e (relative perturbations, the standard EIT choice and what "0.1 % components" means). The unscaled κ is also stored. Float64, same SINGULAR rule as v1.0.

**Cases.** Pairs ({7,3} L=2, square R=6) at N≈112 and ({7,3} L=3, square R=10) at N≈316; triangular R=6.45 added as a second flat control at N≈151.
1. Mild disorder: g_e ~ U[0.5, 1.5], 5 seeds (0–4).
2. Strong disorder: g_e ~ log-uniform on [0.1, 10] (two orders of magnitude), 5 seeds.
3. Defect: every edge incident to one interior node at maximal depth multiplied by 100 (and, separately, by 0.01), unit background. The node is the first, by index, at maximal depth.

**Predictions.** (1) The median gap at N≈316 remains ≥ 5 decades (v1.0 unit value: 6.4); hyperbolic κ changes by < 1 decade. **Refuted** if the median gap < 3 decades. (2) Both κ increase; the median gap remains ≥ 3 decades; **refuted** if < 2 decades. If square R=10 becomes SINGULAR, the gap is reported as a lower bound and the N≈112 pair is the decisive one. (3) The hyperbolic κ increases by < 2 decades for either defect; **refuted** if it increases by > 3 decades (that would mean the advantage is fragile to a single anomaly).

## C. Dimensionality in the probe-matched control (review recommendation 3)

**Question.** Is the 6.7-decade probe-matched gap explained by the hyperbolic side recovering fewer parameters (306 of 399 at L=3; 117 of 140 at L=2)?

**Method.** For the square lattice at the same probe count, take the *best-conditioned* r-dimensional parameter subspace, spanned by the top-r right singular vectors of its full Jacobian, with r equal to the hyperbolic identifiable dimension; its condition number is σ₁/σ_r. This is the most favourable r-dimensional comparison for the flat lattice.

**Prediction.** log₁₀(σ₁/σ₃₀₆) for square R=10 lies between 4 and 7, i.e. above the hyperbolic identifiable-subspace value 2.97; similarly log₁₀(σ₁/σ₁₁₇) for square R=6 is above 2.70. **Refuted** if either flat value is ≤ the corresponding hyperbolic value; then dimensionality reduction cannot be excluded as the driver and §3.3 must say so.

## D. Proposition 1's premise for general L (review recommendation 4)

Not a computation. The argument to be written into §3.5: (i) the union of the heptagons within L dual steps of the central tile is a closed topological disk, certified for every tested instance by the Euler characteristic V − E + F = 1 (already checked by `hyperbolic_network.py` for each build; a connected planar union of tiles with χ = 1 is a disk); (ii) each vertex of the {7,3} tiling lies on exactly three heptagons whose closed neighbourhoods cover a neighbourhood of the vertex; if all three are included, the vertex's three edges are included (each edge is shared by two of them) and the vertex is not on the outer face; if one is missing, the missing sector belongs to the complement, which is connected by (i), hence to the outer face, so the vertex is a boundary node. Therefore interior ⟹ degree 3. Nesting: a vertex whose three heptagons lie within L layers has them within L + 1, so int(G_L) ⊂ int(G_{L+1}); exhaustion is immediate. The stronger statement int(G_L) = G_{L−1} stays certified only for L ≤ 6 and is not needed by the proposition.

## What is not preregistered

The wording of the response to the reviewer and the placement of new material in the paper.
