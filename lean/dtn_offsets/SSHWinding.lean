import Mathlib

/-!
# Toward the bulk half of target T2 of axis 1: the two residue integrals of the SSH symbol

Target T2 (bulk half, `lean/README.md`) says: for real `v, w ≠ 0` with `|v| ≠ |w|`, the winding number of `h(z) = v + w z` around `0`
along the unit circle traversed counter-clockwise (the orientation of Mathlib's `circleMap`), `ν = (2πi)⁻¹ ∮_{|z|=1} h'(z)/h(z) dz`, is `0` when
`|v| > |w|` and `1` when `|w| > |v|`.

This module proves only the two residue integrals that the plan reduces T2 to. Taking for granted (not formalised here) that `h'(z) = w` and
that `h` does not vanish on the circle when `‖v‖ ≠ ‖w‖`, the pointwise identity `SSH.log_deriv_eq` rewrites `h'/h` as `(z - p)⁻¹` with the pole
`p = -v/w`; `SSH.winding_topological` evaluates `∮ (z - p)⁻¹` to `2πi` when the pole is inside the disc (Mathlib's
`circleIntegral.integral_sub_inv_of_mem_ball`), and `SSH.winding_trivial` evaluates it to `0` when the pole is outside the closed disc
(Cauchy–Goursat, `DiffContOnCl.circleIntegral_eq_zero`).

Not formalised: `h' = w`; the non-vanishing of `h` on the circle; the transfer of the pointwise identity under the integral
(`circleIntegral.integral_congr`); the normalisation by `(2πi)⁻¹` and the name "winding number"; the identification of the integral with the degree of
the map; the boundary half of T2 (the finite open chain, decided in exact arithmetic on instances by `experiments/axis1_topological_waves/ssh_exact.py`,
not in Lean); and the correspondence between the two halves. The hypotheses here are over `ℂ` with `w ≠ 0` and a strict norm inequality, which is more
general than the README's real nonzero `v, w` (in particular `v = 0` is allowed). The names `winding_*` refer to the plan, not to a formalised winding number.
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
  have hzp : z - (-v / w) ≠ 0 := by
    intro h0
    apply hz
    rw [h, h0, mul_zero]
  rw [h, div_mul_eq_div_div, div_self hw, one_div]

/-- Topological phase: `|v| < |w|` puts the pole `-v/w` inside the unit disc and the circle integral is `2πi`. -/
theorem winding_topological (v w : ℂ) (hw : w ≠ 0) (h : ‖v‖ < ‖w‖) :
    (∮ z in C((0 : ℂ), 1), (z - (-v / w))⁻¹) = 2 * Real.pi * I := by
  apply circleIntegral.integral_sub_inv_of_mem_ball
  rw [mem_ball_zero_iff, neg_div, norm_neg, norm_div]
  exact (div_lt_one (norm_pos_iff.mpr hw)).mpr h

/-- Trivial phase: `|w| < |v|` puts the pole outside the closed unit disc and the circle integral vanishes. -/
theorem winding_trivial (v w : ℂ) (hw : w ≠ 0) (h : ‖w‖ < ‖v‖) :
    (∮ z in C((0 : ℂ), 1), (z - (-v / w))⁻¹) = 0 := by
  set p : ℂ := -v / w with hp
  have hpn : 1 < ‖p‖ := by
    rw [hp, neg_div, norm_neg, norm_div]
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
  exact hdiff.diffContOnCl_ball (subset_refl _)

end SSH
