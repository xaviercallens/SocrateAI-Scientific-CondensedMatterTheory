# Preregistration 10: localisation with component tolerance (model mismatch)

**Date:** 2026-09-28, committed before the run. **Why:** localisation so far (prereg 8, 9) used an ideal board and an
ideal-model dictionary. A real board has resistor tolerance; the decoder does not know the board. This is the
open limit that decides whether the design of roadmap H-4 works as drawn.

## Design
Same decoder and dictionary as `PREREGISTRATION_8.md` (ideal-model dictionary, contrasts {0.1, 0.5, 0.8, 1.25, 2, 5,
10, 100}, matched filter over all interior nodes). Each trial draws a **fresh random board** g = 1 + τ·U[−1, 1] per
edge; baseline and defect maps are measured on that same board (differential regime), each with independent
i.i.d. noise ε. The defect: all edges of one node of the deepest class × f (node cycles through the class).
τ ∈ {0.1 %, 1 %, 5 %}, ε ∈ {3×10⁻⁴, 3×10⁻³}, f ∈ {1.25, 2}, 20 trials per cell, four lattices. Metric: top-1.

## Predictions (fixed now)
- **T1 (small tolerance is harmless).** τ = 0.1 %, ε = 3×10⁻⁴, f = 2: top-1 ≥ 0.9 on all four lattices.
- **T2 (large tolerance breaks the flat lattice first).** τ = 5 %, ε = 3×10⁻⁴, f = 2: square R=10 top-1 < 0.9 and
  {7,3} L=3 top-1 ≥ 0.9.
- **T3 (ordering).** At τ = 1 % and at τ = 5 %, for both contrasts and both noise levels,
  top-1({7,3} L=3) ≥ top-1(square R=10) − 0.1 (the hyperbolic lattice is never noticeably worse), and at least one
  cell has it higher by ≥ 0.3.

**Refutation:** any of T1–T3 failing. In particular, if square R=10 at τ = 5 % still localises (≥ 0.9), then
tolerance mismatch is harmless for localisation at this size and the tolerance concern of prereg 7 does not
transfer to localisation.

## Not claimed
Board-adapted decoders (estimating the board from the baseline map is itself an ill-posed inverse problem),
multi-node defects, unknown contrast sets, hardware noise.
