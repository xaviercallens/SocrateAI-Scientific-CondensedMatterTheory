# dtn_offsets: machine-checked linear-algebra facts related to the offset-invisibility result

Date: 2026-10-08. Toolchain Lean v4.34.0-rc2, Mathlib v4.34.0-rc2, reused from LeanMaster (recipe A of its `docs/USING_LEANMASTER.md`).

## What is proved (Tier A, kernel-checked, declaration names)

| Declaration | Statement in words |
|---|---|
| `DtN.dtn_mulVec_one` | A Laplacian on boundary plus interior nodes with zero row sums and an invertible interior block has a Schur-complement DtN matrix with zero row sums. |
| `row_offset_orthogonal` | A matrix with zero row sums is Frobenius-orthogonal to every offset constant along rows. |
| `col_offset_orthogonal` | The same for offsets constant along columns, given zero column sums. |
| `decision_invariant` | In a real inner product space, an additive disturbance orthogonal to two candidate signatures leaves the difference of their squared distances to the data unchanged. |

## What is not proved, and what this does not show

- Nothing here concerns hyperbolic geometry, Jacobian conditioning, the strip rate, or holography.
- The connection to the garage measurement (unchecked assertion: the signatures are columns of the Jacobian, which are of the form d dᵀ built from the DtN map) is the Tier C step that
  identifies these lemmas with the hardware statement. It is not formalised.
- The Jacobian-column zero-row-sum property is assumed as a hypothesis (`M *ᵥ 1 = 0`), not derived from the network model.

## Gates (exit codes read from the tools, not from a pipe)

| Gate | Command | Result |
|---|---|---|
| G1 build | `lake build DtNOffsets` | exit 0, no warnings, 8764 jobs |
| G2 sorry | `sorry_grep.py DtNOffsets.lean` | exit 0, clean |
| G3 axioms | `axiom_audit.py DtNOffsets.lean` with `LEAN_PROJECT_ROOT` set | exit 0, 4 theorems, each depends only on propext, Classical.choice, Quot.sound |
| G4 statements | `statement_lock.py --update` then `--check` | locked 5 declarations, check exit 0 |
| G5 producer is not verifier | read-only audit by a separate agent, files read, gates not re-run | verdict: statements correct; docstring wording overstated in three places and the title; fixed in this revision (comments only, statement lock unchanged) |

Pitfall met on the way: `axiom_audit.py DtNOffsets` (a library name) audited 0 theorems and exited 0 (an empty report). Passing the module file `DtNOffsets.lean` audited 4.

## Side effect to know about

The first `lake build` rebuilt the shared Mathlib and dependency packages under the LeanMaster data directory (about 14 minutes, thousands of oleans rewritten).
The sources are unchanged, so the content should be identical, but a LeanMaster session that runs concurrently may have been slowed.


## Second module `GramSchmidtBound.lean` (2026-10-08)

| Declaration | Statement in words |
|---|---|
| `DtN2.dtn_transpose` | For any symmetric matrix `L` (in particular a symmetric Laplacian) the Schur complement onto the first block is symmetric. |
| `DtN2.dtn_vecMul_one` | For symmetric `L` with zero row sums and an invertible interior block, the column sums of the Schur complement vanish (this provides the column-sum hypothesis of `col_offset_orthogonal` for `M = DtN2.dtn L`). |
| `le_residual` | Any `σ` with `σ‖x‖ ≤ ‖∑ xᵢ • aᵢ‖` for all Euclidean coefficient vectors `x` is at most every residual `‖aⱼ − ∑ yᵢ • aᵢ‖` with `yⱼ = 0`. |

Not formalised: that such a `σ` is a lower bound for the smallest singular value of the matrix with columns `aᵢ`; the passage from these residuals to the distance to the span; the leave-one-out identity; the nesting of spans.
`DtN2.dtn` duplicates `DtN.dtn` (same definition, different constant).

Gates for both modules together, exit codes read from the tools: build `lake build DtNOffsets` exit 0 with no warnings (8765 jobs); `sorry_grep.py` on both files exit 0; `axiom_audit.py` on both files exit 0, 7 theorems, each depending only on propext, Classical.choice, Quot.sound;
`statement_lock.py --update` locked 9 declarations, then `--check` exit 0. Separate read-only audit of the wording by another agent: statements correct, three docstring overstatements and one miscount, all fixed (comments only) and the gates rerun after the fix.
Two compile errors on the first attempt (a rewrite in the wrong direction for the inverse of a transpose; a renamed Mathlib constant) were repaired before any statement was locked.


## Third module `SSHWinding.lean` (2026-10-10): bulk half of target T2 of axis 1

| Declaration | Statement in words |
|---|---|
| `SSH.log_deriv_eq` | For `w ≠ 0` and `v + w z ≠ 0`, `w / (v + w z) = (z − (−v/w))⁻¹` (the logarithmic derivative of the symbol through its pole). |
| `SSH.winding_topological` | For `w ≠ 0` and `‖v‖ < ‖w‖`, `∮_{|z|=1} (z − (−v/w))⁻¹ dz = 2πi` (counter-clockwise, Mathlib's `circleMap`). |
| `SSH.winding_trivial` | For `w ≠ 0` and `‖w‖ < ‖v‖`, the same integral is `0`. |

Hypotheses are over `ℂ` with strict norm inequalities, which include the README's real nonzero `v, w` with `|v| ≠ |w|`. Not formalised: the normalisation by `(2πi)⁻¹` as a named winding number, the identification of the integral with the degree of the map, the boundary half of T2 (exact arithmetic on instances in `ssh_exact.py`, Tier B), and the correspondence between the two halves.
First attempt had four errors (a rewrite on `w / w` that was not in the goal, two `norm_neg` rewrites on `−v / w` which parses as `(−v)/w`, and a missing subset argument to `diffContOnCl_ball`), repaired before any statement was locked.

Gates for the three modules together: `lake build DtNOffsets` exit 0, no warnings (8766 jobs); `sorry_grep.py` on the three files exit 0; `axiom_audit.py` on the three files exit 0, 10 theorems, each depending only on propext, Classical.choice, Quot.sound; `statement_lock.py --update SSHWinding.lean` locked 3, `--check` on all three files exit 0. Independent read-only wording audit: see the entry appended below once received.
