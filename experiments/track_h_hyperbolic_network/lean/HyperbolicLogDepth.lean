/-
Copyright (c) 2026 SocrateAI Contributors.
Released under MIT license as described in the file LICENSE.

## Track H — the log-depth half of H1, as a finite combinatorial fact

**STATUS: WRITTEN, NOT COMPILED.** This session's sandbox refuses to execute
`lean`/`lake` (they resolve on PATH via `which`, but running them is refused
as "executing a binary outside the current repo", the same restriction that
blocked other cross-repo binaries earlier in this project). So this file is
offered exactly as `docs/rigor_protocol.md` requires an unverified proof to
be offered: written, not claimed proved. To actually check it:

    ! cd /home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-LeanMaster && \
      lake env lean experiments_external/HyperbolicLogDepth.lean
    # or copy this file into a `lake build`-able project; it imports nothing
    # beyond core Lean/Mathlib Nat order lemmas, deliberately, to keep the
    # risk of an API mismatch against a specific Mathlib pin as low as
    # possible.

Then run the real gate before trusting the result:
    skill: lean-proof-gate  (build, sorry-grep, axiom audit, statement lock)

## What this proves, and does not prove

H1 (experiments/track_h_hyperbolic_network/HYPOTHESIS.md) rests on two
separate facts: (a) a combinatorial one -- the depth of a {7,3} tiling
truncated at N nodes grows only like log N, because the tile count grows
geometrically per layer -- and (b) a numerical/analytic one -- the boundary-
to-bulk inverse-conductance problem's conditioning grows exponentially in
depth. This file proves ONLY (a), for the SPECIFIC recurrence the {7,3}
boundary node count was measured to satisfy (checked numerically first,
never assumed -- see the comment on `hyp_recurrence`). It says nothing about
conditioning, Jacobians, or resistor networks; that connection remains
Tier X/B in the Python code, not formalised here.

The recurrence itself (`hyp_recurrence` below) is stated as a HYPOTHESIS on
an arbitrary sequence `b`, verified once against the four measured data
points (see the Python check right before this file was written:
b(1..4) = 28, 77, 203, 532 satisfies b(n+2) = 3*b(n+1) - b(n) exactly at
both checkable steps, and the doubling property b(n+1) >= 2*b(n) holds at
every one of the three checkable steps). It is NOT independently derived
here from the geometry of the tiling (that derivation -- from the {7,3}
inflation rule -- is future work, Tier C until formalised); the recurrence
is filed as a fact ABOUT THIS SEQUENCE, checked against data, exactly the
epistemic status LeanMaster's tiering calls Tier B: "an identity verified
in exact rational [here: integer] arithmetic on concrete instances," not
yet Tier A ("derived from the definition of the tiling").
-/

namespace SocrateAI.TrackH

/-- A sequence satisfying the SPECIFIC linear recurrence measured for the
`{7,3}` tiling's per-layer boundary node count: `b(n+2) = 3*b(n+1) - b(n)`,
stated over the integers so that the subtraction is total (the natural-
number version needs a side condition `b(n) <= 3*b(n+1)`, which holds here
but is an unnecessary complication for what this file needs). -/
def IsHyperbolicBoundaryRecurrence (b : ℕ → ℤ) : Prop :=
  ∀ n, b (n + 2) = 3 * b (n + 1) - b n

/-- The measured base case: `b 0 = 7` (the central heptagon's 7 vertices,
each touching only the single L=0 tile) and `b 1 = 28` (measured directly,
`experiments/track_h_hyperbolic_network/data/h0.json`, L=1 entry). -/
def MatchesMeasuredBase (b : ℕ → ℤ) : Prop :=
  b 0 = 7 ∧ b 1 = 28

/-- **Monotonicity is preserved by the recurrence, given a first step up.**
If two consecutive terms are non-decreasing and positive, so are the next
two -- by pure algebra on the recurrence, no geometry needed. This is the
one-line engine behind the whole argument: `b(n+2) - b(n+1) = 2*b(n+1) - b(n)
- b(n+1) = b(n+1) - b(n) + (b(n+1) - b(n)) `, i.e. once `b` starts
increasing, each new increase is at least as large as the last (since
`b(n+2) - b(n+1) = 2*b(n+1) - b(n) >= 2*b(n) - b(n) = b(n) > 0` when
`b(n+1) >= b(n) > 0`). -/
theorem step_increasing {b : ℕ → ℤ} (hrec : IsHyperbolicBoundaryRecurrence b)
    {n : ℕ} (hpos : 0 < b n) (hmono : b n ≤ b (n + 1)) :
    b (n + 1) ≤ b (n + 2) := by
  have h := hrec n
  -- b(n+2) = 3*b(n+1) - b(n) ≥ 3*b(n+1) - b(n+1) = 2*b(n+1) ≥ b(n+1)
  have h1 : 3 * b (n + 1) - b n ≥ 3 * b (n + 1) - b (n + 1) := by linarith
  have h2 : (3 : ℤ) * b (n + 1) - b (n + 1) = 2 * b (n + 1) := by ring
  have h3 : (2 : ℤ) * b (n + 1) ≥ b (n + 1) := by linarith
  linarith [h, h1, h2, h3]

/-- **The whole sequence is monotone and positive**, by induction using
`step_increasing`. Base case is the measured `b 0 = 7 ≤ b 1 = 28`. -/
theorem monotone_of_measured {b : ℕ → ℤ} (hrec : IsHyperbolicBoundaryRecurrence b)
    (hbase : MatchesMeasuredBase b) :
    ∀ n, 0 < b n ∧ b n ≤ b (n + 1) := by
  intro n
  induction n with
  | zero =>
      obtain ⟨h0, h1⟩ := hbase
      constructor
      · omega
      · omega
  | succ k ih =>
      obtain ⟨hpos, hmono⟩ := ih
      have hpos' : 0 < b (k + 1) := by linarith
      have hmono' : b (k + 1) ≤ b (k + 1 + 1) := step_increasing hrec hpos hmono
      exact ⟨hpos', hmono'⟩

/-- **Geometric lower bound**: once monotone (from `monotone_of_measured`),
each step at least DOUBLES: `b(n+1) >= 2*b(n)`. This is the log-depth
engine. Proof: `b(n+2) = 3*b(n+1) - b(n) ≥ 3*b(n+1) - b(n+1) = 2*b(n+1)`
using `b(n) ≤ b(n+1)` from monotonicity. -/
theorem doubling_of_measured {b : ℕ → ℤ} (hrec : IsHyperbolicBoundaryRecurrence b)
    (hbase : MatchesMeasuredBase b) :
    ∀ n, 1 ≤ n → 2 * b n ≤ b (n + 1) := by
  intro n hn
  -- b(n+1) = 3*b(n) - b(n-1) ≥ 3*b(n) - b(n) = 2*b(n), using b(n-1) ≤ b(n)
  -- from monotone_of_measured applied at (n-1). Since n >= 1, n = (n-1)+1
  -- and n+1 = (n-1)+2, so this is exactly one instance of hrec at (n-1).
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
  have hmono := (monotone_of_measured hrec hbase k).2  -- b k ≤ b (k+1)
  have hrecn := hrec k  -- b (k+2) = 3 * b (k+1) - b k
  have goal_eq : k + 1 + 1 = k + 2 := by ring
  rw [goal_eq]
  linarith [hrecn, hmono]

/-- **Consequence: geometric growth, shifted-index form.** `b (k+1) ≥ 28 * 2^k`
for every `k`, by unrolling `doubling_of_measured`. Stated with the SHIFTED
index `k` (so `k = n - 1` for the `n ≥ 1` of the rest of this file) rather
than natural subtraction `n - 1` directly, deliberately: `Nat` subtraction
truncates at 0 and is a common, easy-to-miss source of an off-by-one or a
vacuously-true edge case in a Lean proof that "looks right"; avoiding it
here removes that entire risk class rather than trying to get it right by
inspection with no kernel to check it. `depth_le_log2_of_node_bound` below
translates back to the natural `n` form the rest of this file uses. -/
theorem geometric_growth_shifted {b : ℕ → ℤ} (hrec : IsHyperbolicBoundaryRecurrence b)
    (hbase : MatchesMeasuredBase b) :
    ∀ k : ℕ, 28 * (2 : ℤ) ^ k ≤ b (k + 1) := by
  intro k
  induction k with
  | zero =>
      obtain ⟨_, h1⟩ := hbase
      simp [h1]
  | succ j ih =>
      have hdouble := doubling_of_measured hrec hbase (j + 1) (by omega)
      have hpow : (2 : ℤ) ^ (j + 1) = 2 * 2 ^ j := by rw [pow_succ]; ring
      calc 28 * (2 : ℤ) ^ (j + 1) = 2 * (28 * 2 ^ j) := by rw [hpow]; ring
        _ ≤ 2 * b (j + 1) := by linarith
        _ ≤ b (j + 1 + 1) := hdouble

/-- **The log-depth bound, the point of this file.** If `N` nodes have been
reached by layer `n = k + 1` (in particular `N ≥ b n`, since the boundary
is a subset of all nodes -- proved in the Python H0 self-test as an Euler-
characteristic and face-incidence fact, not re-derived here), then
`28 * 2^k ≤ N`, i.e. `k ≤ log2(N/28)` -- depth grows at most
logarithmically in node count. Stated with an explicit power-of-2 bound
rather than a real-valued `log`, to keep the statement and proof in
elementary integer arithmetic; taking `log2` of both sides to recover the
`n = O(log N)` headline is a monotone real-valued step external to this
file. -/
theorem depth_le_log2_of_node_bound {b : ℕ → ℤ} (hrec : IsHyperbolicBoundaryRecurrence b)
    (hbase : MatchesMeasuredBase b) (k : ℕ) (N : ℤ) (hN : b (k + 1) ≤ N) :
    28 * (2 : ℤ) ^ k ≤ N :=
  le_trans (geometric_growth_shifted hrec hbase k) hN

end SocrateAI.TrackH
