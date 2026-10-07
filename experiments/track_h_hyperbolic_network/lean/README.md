# Lean — Track H

## Status: **written, not compiled**

This sandbox's permission mode refuses to execute `lean`/`lake` (they
resolve on `PATH` via `which lean lake elan`, confirming the toolchain
exists at `~/.elan/bin/`, but *running* them is refused — the same
restriction that blocked invoking binaries under other repos' directories
earlier in this project). So [`HyperbolicLogDepth.lean`](HyperbolicLogDepth.lean)
has **not** been checked by the Lean kernel in this session. It is offered
exactly as [`../../../docs/rigor_protocol.md`](../../../docs/rigor_protocol.md)
requires: written, with its status stated plainly, not claimed proved.

**To actually verify it**, run this yourself:

```
! cd ~/SocrateAI-Scientific-Agora-LeanMaster && \
  cp ~/SocrateAI-Scientific-CondensedMatterTheory/experiments/track_h_hyperbolic_network/lean/HyperbolicLogDepth.lean . && \
  lake env lean HyperbolicLogDepth.lean
```

Then run the actual gate, not just a successful compile:

```
skill: lean-proof-gate
```

which checks build success, greps for `sorry` (a `sorry` does not fail
`lake build` — it's a warning, and the file compiles with a hole in it
unless this is checked separately), audits the printed axiom footprint,
and locks the statement so it can't be quietly weakened later.

## What this file proves, scoped honestly

**Only** the combinatorial half of H1: given the specific linear recurrence
the `{7,3}` tiling's per-layer boundary-node count was *measured* to
satisfy (`b(n+2) = 3*b(n+1) - b(n)`, checked against the four data points
in `../data/h0.json` before writing a single line of Lean — see the
Python check that precedes the file's creation in this session's history),
the boundary count grows at least geometrically (`b(k+1) ≥ 28·2^k`), hence
depth is `O(log N)`.

**Not proved here, and not claimed:**
- That the recurrence follows from the `{7,3}` inflation rule itself
  (geometry → recurrence). The recurrence is filed as a fact *about the
  measured sequence*, Tier B once compiled, not Tier A.
- Anything about conditioning, Jacobians, or resistor networks — the
  actual physical content of H1. That stays Tier X/B in the Python code.
- Mathlib's own Schur-complement machinery
  (`Mathlib.LinearAlgebra.Matrix.SchurComplement`, confirmed present in
  the LeanMaster Mathlib checkout — `Matrix.fromBlocks_eq_of_invertible₂₂`
  already gives the LDU/Schur-complement decomposition
  `D − C·A⁻¹·B` that `hyperbolic_network.jacobian()`'s harmonic-extension
  construction is an instance of) was deliberately **not** reproved here.
  Connecting the Python construction to that existing Mathlib lemma is
  future work, and is a *thinner*, more honest first Lean artifact than
  duplicating general linear algebra Mathlib already has.

## Design choices made to reduce compilation risk (since it can't be checked here)

- Integer (`ℤ`) arithmetic throughout, not `ℕ` with its truncating
  subtraction — a frequent, easy-to-miss source of an off-by-one that
  "looks right" without a kernel to check it.
- The geometric-growth theorem is stated with a *shifted* index (`b(k+1)`
  in terms of `k`) specifically to avoid `n - 1` anywhere in a `Nat`
  position.
- No dependency beyond core `Nat`/`Int` order lemmas and `linarith`/`omega`
  — nothing from a specific, potentially-version-sensitive area of Mathlib.
