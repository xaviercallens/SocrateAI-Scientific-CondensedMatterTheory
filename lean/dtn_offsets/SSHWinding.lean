import Mathlib

/-!
# The winding number of the SSH symbol `z ↦ v + w z` on the unit circle

Target T2 (bulk half) of axis 1 of the programme (`lean/README.md`). For real `v, w ≠ 0` with `|v| ≠ |w|`, the winding
number of `h(z) = v + w z` around `0` along the unit circle traversed counter-clockwise (the orientation of Mathlib's
`circleMap`), `ν = (2πi)⁻¹ ∮_{|z|=1} h'(z)/h(z) dz`, is `0` when `|v| > |w|` and `1` when `|w| > |v|`.

Since `h'(z)/h(z) = (z - (-v/w))⁻¹`, the integral is `∮ (z - p)⁻¹` with the pole `p = -v/w`: inside the disc in the
topological phase (Mathlib's `circleIntegral.integral_sub_inv_of_mem_ball`), outside it in the trivial phase, where the
integrand is holomorphic on the closed disc and the Cauchy–Goursat theorem (`DiffContOnCl.circleIntegral_eq_zero`) gives zero.

What is proved: exactly the two integrals. Not proved here: the identity of this integral with the degree of the map
`S¹ → ℂ∖{0}`, the boundary half of T2 (the finite open chain, decided in exact arithmetic by
`experiments/axis1_topological_waves/ssh_exact.py` on instances, not in Lean), and the correspondence between the two.
Nothing here concerns a physical system.
-/

open Complex Metric

namespace SSH

/-- The logarithmic derivative of the symbol `v + w z` as a function of `z`, written through its pole `p = -v/w`. -/
theorem log_deriv_eq (v w z : ℂ) (hw : w ≠ 0) (hz : v + w * z ≠ 0) :
    w / (v + w * z) = (z - (-v / w))⁻¹ := by
  have h : v + w * z = w * (z - (-v / w)) := by
    field_simp
    ring
  rw [h, mul_comm, ← div_div, div_self hw, one_div]
  -- `z - (-v/w) ≠ 0` follows from `hz`
  · exact (mul_ne_zero_iff.mp (h ▸ hz)).2

/-- Topological phase: `|v| < |w|` puts the pole `-v/w` inside the unit disc and the circle integral is `2πi`. -/
theorem winding_topological (v w : ℂ) (hw : w ≠ 0) (h : ‖v‖ < ‖w‖) :
    (∮ z in C((0 : ℂ), 1), (z - (-v / w))⁻¹) = 2 * Real.pi * I := by
  apply circleIntegral.integral_sub_inv_of_mem_ball
  rw [mem_ball_zero_iff, norm_neg, norm_div]
  exact (div_lt_one (norm_pos_iff.mpr hw)).mpr h

/-- Trivial phase: `|w| < |v|` puts the pole outside the closed unit disc and the circle integral vanishes. -/
theorem winding_trivial (v w : ℂ) (hw : w ≠ 0) (h : ‖w‖ < ‖v‖) :
    (∮ z in C((0 : ℂ), 1), (z - (-v / w))⁻¹) = 0 := by
  set p : ℂ := -v / w with hp
  have hpn : 1 < ‖p‖ := by
    rw [hp, norm_neg, norm_div]
    exact (one_lt_div (norm_pos_iff.mpr hw)).mpr h
  have hne : ∀ z ∈ closedBall (0 : ℂ) 1, z - p ≠ 0 := by
    intro z hz hzp
    rw [mem_closedBall_zero_iff] at hz
    have : z = p := sub_eq_zero.mp hzp
    rw [this] at hz
    exact absurd hz (not_le.mpr hpn)
  have hdiff : DifferentiableOn ℂ (fun z : ℂ => (z - p)⁻¹) (closedBall (0 : ℂ) 1) :=
    (differentiableOn_id.sub_const p).inv hne
  apply DiffContOnCl.circleIntegral_eq_zero zero_le_one
  exact hdiff.diffContOnCl_ball

end SSH
