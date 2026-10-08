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
