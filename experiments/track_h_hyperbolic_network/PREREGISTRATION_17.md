# Preregistration 17: localisation under correlated hardware noise (task Q8)

**Date:** 2026-09-28, committed before the run. **Roadmap item:** H-4 phase 2 (measurement-chain requirements).
**Why:** localisation results (H3-X-0005..0008) used i.i.d. Gaussian noise. Real chains add three correlated errors:
a common-mode offset per measurement, a gain drift between the two maps, and ADC quantisation. This card measures
which of them a single-node localisation survives, on the two phase-1 boards ({7,3} L=2 and square R=6).

## Design
Decoder and dictionary as `localize_defect.py` (ideal board, matched filter over all interior nodes, contrasts
{0.1, 0.5, 0.8, 1.25, 2, 5, 10, 100}), deepest class, true contrast f = 2, 20 trials per cell. Two maps P₁ (baseline)
and P₂ (defect) of the same board, each with i.i.d. noise 3×10⁻⁴ (the budget) plus ONE of:
- **Offset:** P_k + c_k·s·𝟙𝟙ᵀ, c_k ~ N(0, ε_o) independently per map, s = rms entry; ε_o ∈ {1e-4, 1e-3, 1e-2, 1e-1}.
  Decoded twice: as is, and after **mean removal** (subtract the mean entry of ΔP and of every dictionary entry).
- **Gain drift:** P₂ → (1 + δ)P₂, δ ~ N(0, ε_g); ε_g ∈ {1e-4, 3e-4, 1e-3, 3e-3, 1e-2}. Decoded twice: as is, and with a
  **gain-fitted** decoder (for each dictionary entry, the best scalar gain on P₁ is fitted by least squares before the
  residual is taken).
- **Quantisation:** each entry of P_k rounded to a grid of step q·s, q = 2^(−bits), bits ∈ {10, 12, 14, 16}.
Metric: top-1. Data file: `data/localisation_under_correlated_hardware_n.json`.

## Validity gates
- G1: with none of the three (i.i.d. 3×10⁻⁴ only) both boards give top-1 ≥ 0.9 (reproduces H3-X-0005).
- G2: mean removal and gain fitting change nothing in the G1 condition (top-1 ≥ 0.9 with them as well).

## Predictions (fixed now)
- **P1 (quantisation).** 12 bits (q = 2.4×10⁻⁴, at the budget) leaves both boards at top-1 ≥ 0.9; 10 bits (q = 9.8×10⁻⁴)
  drops square R=6 below 0.9 while {7,3} L=2 stays ≥ 0.9 (its noise margin at f = 2 is 10⁻¹, H3-X-0006).
  **Refuted if** either half fails.
- **P2 (offset).** The offset adds a rank-one term of relative size ε_o to ΔP, whose own relative size at f = 2 is about
  6×10⁻² on {7,3} L=2 and 2×10⁻² on square R=6 (H3-X-0004 signal curve). Without mean removal: square R=6 < 0.9 at
  ε_o = 1e-2 and ≥ 0.9 at 1e-3; {7,3} L=2 ≥ 0.9 at 1e-2 and < 0.9 at 1e-1. With mean removal both boards stay ≥ 0.9 at
  every ε_o up to 1e-1. **Refuted if** any of these fails.
- **P3 (drift).** Without gain fitting: at ε_g = 1e-3 square R=6 < 0.9 and {7,3} L=2 ≥ 0.9; at ε_g = 1e-2 both < 0.9.
  With gain fitting both boards stay ≥ 0.9 up to ε_g = 1e-2. **Refuted if** any part fails.

## Not claimed
Localisation on real hardware; noise with time structure inside one map; multi-node defects; nothing about holography.
