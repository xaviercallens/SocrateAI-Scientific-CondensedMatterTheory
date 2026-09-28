# Preregistration 6: defect detection against measurement noise (replaces the mis-sized null of prereg 5)

**Date:** 2026-09-28, committed before the run. **Why:** PREREGISTRATION_5 used a global 50 % disorder null against a
single-node defect (lesson LL-A8), so its P2 was refuted by the design. The physically meaningful null for a
tabletop experiment is *measurement noise* on the measured map, at the paper's precision budget.

## Design
- Boundary data: the Neumann-to-Dirichlet map P = Λ⁺ (what hardware measures). Noisy data: P + ε·s·E, with E a
  symmetric standard-normal matrix and s = rms entry of P; ε = 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1.
- From the (noisy) P: boundary effective-resistance metric R_ij = P_ii + P_jj − 2P_ij (clipped ≥ 0), as in prereg 5.
- Statistics against the noiseless unit configuration: relative metric change ‖R − R₀‖_F/‖R₀‖_F and H₁ bottleneck
  distance of Vietoris–Rips diagrams (Gudhi).
- For each ε: the noise null is 10 realisations of *unit* P + noise; the threshold is its maximum. A defect
  configuration is *detected at ε* if all 10 independent noisy realisations of P_defect exceed the threshold.
  ε_max = the largest grid ε at which it is detected (0 if none).
- Configurations, lattices: as prereg 5 (deep ×100, deep ×0.01, shallow ×100), on {7,3} L=3 / square R=10
  (N≈316) and {7,3} L=2 / square R=6 (N≈112).

## Predictions (fixed now)
- **Q1 (geometry sets sensitivity).** For the metric detector and the deep ×100 defect,
  ε_max(hyperbolic) ≥ 3 × ε_max(square) at N≈316 (the depth mechanism gives a 6× larger boundary signal).
  **Refuted** if the ratio is below 3 or the square lattice's ε_max is the larger.
- **Q2 (topology is less sensitive than the metric).** For deep ×100, ε_max(H₁) ≤ ε_max(metric)/3 on both
  hyperbolic lattices (H₁ never detecting counts as satisfying it). **Refuted** if H₁ detects at an ε within a
  factor 3 of the metric's.
- **Q3 (hardware adequacy).** At ε = 3e-4 (the paper's precision budget) the deep ×100 defect is detected by the
  metric on all four lattices. **Refuted** if any lattice fails at 3e-4.

## Not claimed
Nothing here bears on holography; effective resistance is classical. Localising *where* the defect is remains
untested (roadmap H-3).
