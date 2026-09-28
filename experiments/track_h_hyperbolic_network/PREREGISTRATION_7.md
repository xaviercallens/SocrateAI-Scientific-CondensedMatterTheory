# Preregistration 7: defect detection against component tolerance (roadmap H-4 precondition)

**Date:** 2026-09-28, committed before the run. **Why:** prereg 6 detected defects against measurement noise
around a *known noiseless baseline*. A real board has resistor tolerance, a fixed random perturbation of every
conductance. Two regimes, which answer different questions:
- **Model-based (B):** the measured board is compared with the *ideal* unit-conductance simulation; tolerance is the
  null. This is what one does when a board is built once and checked against theory.
- **Differential (A):** the board is compared with *its own* earlier measurement; tolerance cancels to first order
  and measurement noise (3e-4, the paper's budget) is the null.

## Design
Metric detector only (prereg 5/6 showed the H₁ detector is less sensitive). Statistic: ‖R − R_ref‖_F / ‖R_ref‖_F,
R the boundary effective-resistance metric from the Neumann-to-Dirichlet map. Tolerance τ ∈ {0.1 %, 1 %, 5 %}:
g_e = 1 + τ·u_e, u_e ~ U[−1, 1] independent per edge. Defect: every edge of the first maximal-depth interior node
×100 (same node as before), on top of the tolerance. Four lattices as before. 20 boards per condition.
- **B:** null = 20 tolerance boards vs ideal; defect = 20 (other) tolerance boards with the defect, vs ideal.
  *Detected* iff min(defect statistics) > max(null statistics).
- **A:** 10 boards; each measured twice with independent 3e-4 noise. Null = statistic between two noisy measurements
  of the same board; defect = statistic between a noisy baseline and a noisy measurement with the defect.
  Detected iff min(defect) > max(null).

## Predictions (fixed now, from linear response of the prereg-5 disorder null)
The prereg-5 null p95 (U[0.5,1.5], sd 0.289) was 0.109 / 0.113 / 0.135 / 0.131 for {7,3} L=3 / square R=10 /
{7,3} L=2 / square R=6; the statistic scales with the sd of the perturbation, so the tolerance null is ≈ 2τ times
those: τ=0.1 % → ≈2×10⁻⁴; 1 % → ≈2×10⁻³; 5 % → ≈1.1×10⁻² (L=3, R=10), 1.4×10⁻² (L=2), 1.3×10⁻² (R=6). The deep
×100 signals (prereg 5) are 0.038 / 0.0061 / 0.059 / 0.020.
- **B1:** at τ = 0.1 % all four lattices detect.
- **B2:** at τ = 1 % all four detect. (Marginal case: square R=10, signal 0.0061 against a null max near 0.003.)
- **B3:** at τ = 5 %: {7,3} L=2 and L=3 detect; square R=10 does **not** (null ≈ 0.011 > 0.0061). Square R=6 is
  marginal (signal 0.020 vs null max ≈ 0.017) and carries no prediction.
- **A1:** in the differential regime the defect is detected on all four lattices at every τ.

**Refutation:** any deviation from B1, B2, B3 (except square R=6 at 5 %) or A1. In particular, if the hyperbolic
lattices fail at 5 % or square R=10 succeeds at 5 %, the linear-response scaling argument is wrong.

## Not claimed
Localisation of the defect (roadmap H-3); anything about holography.
