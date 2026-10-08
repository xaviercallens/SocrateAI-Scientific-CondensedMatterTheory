import Mathlib

/-!
# Symmetry of the DtN matrix, and a residual bound on the smallest singular value

Two elementary facts used by the Track H programme. Both are finite-dimensional linear algebra; neither concerns a particular network,
conditioning of any particular Jacobian, or holography.

* `DtN2.dtn_transpose` : the Schur complement of a symmetric matrix onto a block is symmetric; hence the DtN matrix of a symmetric Laplacian is symmetric.
* `DtN2.dtn_vecMul_one` : for a symmetric `L` with zero row sums and an invertible interior block, the column sums of the DtN matrix vanish too.
  This discharges the column-sum hypothesis of `col_offset_orthogonal` in `DtNOffsets`.
* `le_residual` : if `σ ‖x‖ ≤ ‖∑ xᵢ • aᵢ‖` for all `x` in Euclidean space (the defining property of a lower bound `σ` on the smallest singular value of the
  matrix with columns `aᵢ`), then `σ ≤ ‖aⱼ - ∑ yᵢ • aᵢ‖` for every `j` and every `y` with `yⱼ = 0`: the smallest singular value is at most the distance of
  any column to the span of the other columns. The link between the hypothesis and the smallest singular value of the matrix is a standard fact that is
  not formalised here (the hypothesis is stated directly).
-/

open Matrix

namespace DtN2

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

/-- The same Schur complement as `DtN.dtn`, restated so that this module stands alone. -/
noncomputable def dtn (L : Matrix (ι ⊕ κ) (ι ⊕ κ) ℝ) : Matrix ι ι ℝ :=
  L.toBlocks₁₁ - L.toBlocks₁₂ * (L.toBlocks₂₂)⁻¹ * L.toBlocks₂₁

theorem dtn_transpose (L : Matrix (ι ⊕ κ) (ι ⊕ κ) ℝ) (hL : Lᵀ = L) : (dtn L)ᵀ = dtn L := by
  have h11 : L.toBlocks₁₁ᵀ = L.toBlocks₁₁ := by
    ext i j
    have := congrFun (congrFun hL (Sum.inl i)) (Sum.inl j)
    simpa [Matrix.toBlocks₁₁, Matrix.transpose_apply] using this
  have h22 : L.toBlocks₂₂ᵀ = L.toBlocks₂₂ := by
    ext i j
    have := congrFun (congrFun hL (Sum.inr i)) (Sum.inr j)
    simpa [Matrix.toBlocks₂₂, Matrix.transpose_apply] using this
  have h12 : L.toBlocks₁₂ᵀ = L.toBlocks₂₁ := by
    ext k i
    have := congrFun (congrFun hL (Sum.inr k)) (Sum.inl i)
    simpa [Matrix.toBlocks₁₂, Matrix.toBlocks₂₁, Matrix.transpose_apply] using this
  have h21 : L.toBlocks₂₁ᵀ = L.toBlocks₁₂ := by
    rw [← h12, Matrix.transpose_transpose]
  unfold dtn
  rw [Matrix.transpose_sub, Matrix.transpose_mul, Matrix.transpose_mul, h21, ← Matrix.transpose_nonsing_inv, h22, h11, h12]
  simp [Matrix.mul_assoc]

omit [DecidableEq ι] in
theorem dtn_vecMul_one (L : Matrix (ι ⊕ κ) (ι ⊕ κ) ℝ) (hL : Lᵀ = L)
    (hR : L *ᵥ (fun _ => (1 : ℝ)) = 0) (hU : IsUnit L.toBlocks₂₂.det) :
    (fun _ => (1 : ℝ)) ᵥ* dtn L = 0 := by
  classical
  have hsym := dtn_transpose L hL
  have h1 : dtn L *ᵥ (fun _ => (1 : ℝ)) = 0 := by
    -- reuse the argument of `DtN.dtn_mulVec_one`
    have e1 : L.toBlocks₁₁ *ᵥ (fun _ => (1 : ℝ)) + L.toBlocks₁₂ *ᵥ (fun _ => (1 : ℝ)) = 0 := by
      funext i
      have h := congrFun hR (Sum.inl i)
      simpa [Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.toBlocks₁₁, Matrix.toBlocks₁₂] using h
    have e2 : L.toBlocks₂₁ *ᵥ (fun _ => (1 : ℝ)) + L.toBlocks₂₂ *ᵥ (fun _ => (1 : ℝ)) = 0 := by
      funext k
      have h := congrFun hR (Sum.inr k)
      simpa [Matrix.mulVec, dotProduct, Fintype.sum_sum_type, Matrix.toBlocks₂₁, Matrix.toBlocks₂₂] using h
    have h3 : (L.toBlocks₂₂)⁻¹ *ᵥ (L.toBlocks₂₁ *ᵥ (fun _ => (1 : ℝ))) = -(fun _ => (1 : ℝ)) := by
      have e : L.toBlocks₂₁ *ᵥ (fun _ => (1 : ℝ)) = -(L.toBlocks₂₂ *ᵥ (fun _ => (1 : ℝ))) :=
        eq_neg_of_add_eq_zero_left e2
      rw [e, Matrix.mulVec_neg, Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hU, Matrix.one_mulVec]
    unfold dtn
    rw [Matrix.sub_mulVec, ← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, h3, Matrix.mulVec_neg]
    have : L.toBlocks₁₂ *ᵥ (fun _ => (1 : ℝ)) = -(L.toBlocks₁₁ *ᵥ (fun _ => (1 : ℝ))) :=
      eq_neg_of_add_eq_zero_right e1
    rw [this]
    simp
  calc (fun _ => (1 : ℝ)) ᵥ* dtn L = (fun _ => (1 : ℝ)) ᵥ* (dtn L)ᵀ := by rw [hsym]
    _ = dtn L *ᵥ (fun _ => (1 : ℝ)) := Matrix.vecMul_transpose _ _
    _ = 0 := h1

end DtN2

section Residual

variable {ι E : Type*} [Fintype ι] [DecidableEq ι] [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- A lower bound `σ` on `‖∑ xᵢ • aᵢ‖ / ‖x‖` (Euclidean norm on the coefficients) is at most the distance of any column `aⱼ` to the span of the others,
in the form `‖aⱼ - ∑ yᵢ • aᵢ‖` for coefficients `y` with `yⱼ = 0`. -/
theorem le_residual (a : ι → E) (σ : ℝ)
    (hσ : ∀ x : EuclideanSpace ℝ ι, σ * ‖x‖ ≤ ‖∑ i, x i • a i‖)
    (j : ι) (y : ι → ℝ) (hy : y j = 0) :
    σ ≤ ‖a j - ∑ i, y i • a i‖ := by
  set x : EuclideanSpace ℝ ι := WithLp.toLp 2 (fun i => (if i = j then (1 : ℝ) else 0) - y i) with hx
  have hsum : ∑ i, x i • a i = a j - ∑ i, y i • a i := by
    simp only [hx, WithLp.toLp_apply, sub_smul, Finset.sum_sub_distrib, ite_smul, zero_smul, Finset.sum_ite_eq', Finset.mem_univ, if_true, one_smul]
  have hcoord : (1 : ℝ) ≤ ‖x‖ := by
    have h := PiLp.norm_apply_le x j
    have hxj : x j = 1 := by simp [hx, hy]
    simpa [hxj] using h
  have key := hσ x
  rw [hsum] at key
  by_cases hs : σ ≤ 0
  · exact le_trans hs (norm_nonneg _)
  · push_neg at hs
    calc σ = σ * 1 := by ring
      _ ≤ σ * ‖x‖ := mul_le_mul_of_nonneg_left hcoord hs.le
      _ ≤ _ := key

end Residual
