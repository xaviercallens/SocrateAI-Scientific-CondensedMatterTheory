import Mathlib

/-!
# The DtN matrix kills constants, and offsets constant along a row or column are invisible

Elementary facts behind the offset-invisibility result of PREREGISTRATION_22 / H3-X-0010 of the Track H programme.
They are *finite-dimensional linear algebra*; nothing here concerns the physics of any particular network, the
conditioning of Jacobians, or holography.

Setting. A weighted graph Laplacian `L` on boundary nodes `ι` and interior nodes `κ` (index type `ι ⊕ κ`),
with `L *ᵥ 1 = 0` (rows sum to zero), and an invertible interior block. The Dirichlet-to-Neumann (DtN) matrix is the
Schur complement `Λ = L₁₁ - L₁₂ L₂₂⁻¹ L₂₁`.

* `dtn_mulVec_one` : `Λ *ᵥ 1 = 0`.
* `row_offset_orthogonal` : for any `M` with `M *ᵥ 1 = 0` and any `u`, `∑ i, ∑ j, u i * M i j = 0`
  (an offset of the form `u 1ᵀ`, constant along each row, is orthogonal to `M` in the Frobenius pairing).
* `col_offset_orthogonal` : the same for offsets `1 wᵀ` when `1ᵀ M = 0`.
* `decision_invariant` : in any real inner product space, if `O` is orthogonal to two candidate signatures `d₁, d₂`,
  then the difference of squared distances `‖x + O - d₁‖² - ‖x + O - d₂‖²` does not depend on `O`.
-/

open Matrix

namespace DtN

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

/-- The Dirichlet-to-Neumann matrix: Schur complement of the interior block. -/
noncomputable def dtn (L : Matrix (ι ⊕ κ) (ι ⊕ κ) ℝ) : Matrix ι ι ℝ :=
  L.toBlocks₁₁ - L.toBlocks₁₂ * (L.toBlocks₂₂)⁻¹ * L.toBlocks₂₁

omit [DecidableEq ι] in
/-- If the Laplacian kills the all-ones vector and the interior block is invertible, so does the DtN matrix. -/
theorem dtn_mulVec_one (L : Matrix (ι ⊕ κ) (ι ⊕ κ) ℝ)
    (hL : L *ᵥ (fun _ => (1 : ℝ)) = 0) (hU : IsUnit L.toBlocks₂₂.det) :
    dtn L *ᵥ (fun _ => (1 : ℝ)) = 0 := by
  have h1 : L.toBlocks₁₁ *ᵥ (fun _ => (1 : ℝ)) + L.toBlocks₁₂ *ᵥ (fun _ => (1 : ℝ)) = 0 := by
    funext i
    have h := congrFun hL (Sum.inl i)
    simpa [Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.toBlocks₁₁, Matrix.toBlocks₁₂] using h
  have h2 : L.toBlocks₂₁ *ᵥ (fun _ => (1 : ℝ)) + L.toBlocks₂₂ *ᵥ (fun _ => (1 : ℝ)) = 0 := by
    funext k
    have h := congrFun hL (Sum.inr k)
    simpa [Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.toBlocks₂₁, Matrix.toBlocks₂₂] using h
  have h3 : (L.toBlocks₂₂)⁻¹ *ᵥ (L.toBlocks₂₁ *ᵥ (fun _ => (1 : ℝ))) = -(fun _ => (1 : ℝ)) := by
    have e : L.toBlocks₂₁ *ᵥ (fun _ => (1 : ℝ)) = -(L.toBlocks₂₂ *ᵥ (fun _ => (1 : ℝ))) :=
      eq_neg_of_add_eq_zero_left h2
    rw [e, Matrix.mulVec_neg, Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hU, Matrix.one_mulVec]
  unfold dtn
  rw [Matrix.sub_mulVec, ← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, h3, Matrix.mulVec_neg]
  have : L.toBlocks₁₂ *ᵥ (fun _ => (1 : ℝ)) = -(L.toBlocks₁₁ *ᵥ (fun _ => (1 : ℝ))) :=
    eq_neg_of_add_eq_zero_right h1
  rw [this]
  simp

end DtN

section Offsets

variable {ι : Type*} [Fintype ι]

/-- A perturbation `M` of the DtN matrix has zero row sums; an offset `u 1ᵀ` is Frobenius-orthogonal to it. -/
theorem row_offset_orthogonal (M : Matrix ι ι ℝ) (hM : M *ᵥ (fun _ => (1 : ℝ)) = 0) (u : ι → ℝ) :
    ∑ i, ∑ j, u i * M i j = 0 := by
  have h : ∀ i, ∑ j, M i j = 0 := by
    intro i
    have := congrFun hM i
    simpa [Matrix.mulVec, dotProduct] using this
  calc ∑ i, ∑ j, u i * M i j = ∑ i, u i * ∑ j, M i j := by
        refine Finset.sum_congr rfl (fun i _ => ?_)
        rw [Finset.mul_sum]
    _ = 0 := by simp [h]

/-- Dual statement for offsets `1 wᵀ`, when the column sums vanish (for a symmetric `M`, the same hypothesis). -/
theorem col_offset_orthogonal (M : Matrix ι ι ℝ) (hM : (fun _ => (1 : ℝ)) ᵥ* M = 0) (w : ι → ℝ) :
    ∑ i, ∑ j, M i j * w j = 0 := by
  have h : ∀ j, ∑ i, M i j = 0 := by
    intro j
    have := congrFun hM j
    simpa [Matrix.vecMul, dotProduct] using this
  calc ∑ i, ∑ j, M i j * w j = ∑ j, (∑ i, M i j) * w j := by
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl (fun j _ => ?_)
        rw [Finset.sum_mul]
    _ = 0 := by simp [h]

end Offsets

section Decision

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- If an additive disturbance `O` is orthogonal to two candidate signatures, the comparison of their squared
distances to the data does not depend on `O`: the matched-filter decision between the two candidates is unchanged. -/
theorem decision_invariant (x O d₁ d₂ : E) (h₁ : inner ℝ O d₁ = 0) (h₂ : inner ℝ O d₂ = 0) :
    ‖x + O - d₁‖ ^ 2 - ‖x + O - d₂‖ ^ 2 = ‖x - d₁‖ ^ 2 - ‖x - d₂‖ ^ 2 := by
  rw [norm_sub_sq_real (x + O) d₁, norm_sub_sq_real (x + O) d₂, norm_sub_sq_real x d₁, norm_sub_sq_real x d₂,
    inner_add_left, inner_add_left, h₁, h₂]
  ring

end Decision
