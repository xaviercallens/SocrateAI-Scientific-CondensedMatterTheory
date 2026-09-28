# Localising a single-node defect: results (2026-09-28)

Preregistration: `PREREGISTRATION_8.md` (1ba49a0, before the run). Script: `localize_defect.py`. Data:
`data/localize_defect.json`. Ledger: H3-X-0005.

**Setup.** Two NtD maps of the same ideal board, each with independent i.i.d. Gaussian noise 3×10⁻⁴; one map has
a defect (every edge of one interior node × f). A dictionary matched filter over all interior nodes and
f ∈ {0.1, 0.5, 0.8, 1.25, 2, 5, 10, 100} picks the (node, contrast) that best explains the difference. Four lattices
× three depth classes (1, mid, max) × five true contrasts {0.8, 1.25, 2, 10, 100} × 20 trials = 60 cells.

**Result: top-1 node accuracy and contrast accuracy are 1.00 in all 60 cells; mean hop error 0.**

| Prediction | Verdict |
|---|---|
| L1: f ∈ {10, 100}, depth 1 and mid, top-1 ≥ 0.9 on all four lattices | **held** |
| L2: deep, ×2: hyperbolic L=3 ≥ 0.8 *and* square R=10 ≤ 0.5 | **refuted** (square R=10: 1.00) |
| L3: deep, ×0.8 / ×1.25: square R=10 ≤ 0.2 *and* hyperbolic L=3 ≥ 0.5 | **refuted** (square R=10: 1.00) |

**What this means.** The hyperbolic lattice's larger boundary signal (up to ~8–10× at the deepest node, H3-X-0004)
gives **no localisation advantage** at this noise level and these sizes: a flat 317-node board localises even a
±20–25 % single-node defect at its deepest point without error. This cuts against using localisation as the
motivation for a hyperbolic build; the conditioning advantage of the paper is real, but at N≈100–300 and
3×10⁻⁴ noise it is not the limiting factor for this task.

> **Update (same day, after the noise sweep below): the sentence above is too strong.** "No localisation advantage"
> holds only at the 3×10⁻⁴ noise budget, where both lattices are at the ceiling. At higher noise the flat lattice
> fails and the hyperbolic one does not (next section). The advantage is a *noise margin*, not an accuracy gap at
> the paper's budget.

**Why my predictions failed (hypothesis, not tested).** I predicted decoder performance from the SNR of the
*detection* statistic (a single norm, ≈3× the noise floor for the flat lattice). A matched filter combines all m²
correlated entries of the m×m map, so its effective sensitivity is higher by a factor of order m (76 boundary probes
on square R=10). The lesson is LL-A10.

**Limits.**
1. A 60/60 result cannot separate "solved" from "saturated": the failure boundary was unknown. The noise sweep
   (`PREREGISTRATION_9.md`, next section) measures it.
2. **Oracle assumptions:** ideal board (no component tolerance, which was harmless for detection but untested
   for localisation), a known single-node defect model, and a known finite contrast set.
3. The maximal-depth class has one node on both square lattices (20 noise draws of one location) and 7 on {7,3}.
4. i.i.d. Gaussian noise is not hardware noise; multi-node and extended defects are untested.

## Noise sweep: where localisation fails (`PREREGISTRATION_9.md`, f10477f before the run; ledger H3-X-0006)

Same decoder; deepest class; noise from 1e-3 to 3e-1; 20 trials per cell. **ε_loc** = largest grid noise that keeps
top-1 ≥ 0.9.

| ε_loc | {7,3} L=3 (N=315) | square R=10 (N=317) | {7,3} L=2 (N=112) | square R=6 (N=113) |
|---|---|---|---|---|
| ×2, deepest node | > 3×10⁻¹ (never fails) | 3×10⁻³ | 10⁻¹ | 10⁻² |
| ×1.25, deepest node | 10⁻¹ | 10⁻³ | 3×10⁻² | 3×10⁻³ |

Top-1 by ε (1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1): square R=10 ×2: 1.00 1.00 0.70 0.00 0.00 0.00; {7,3} L=3 ×2:
1.00 at every noise level up to 3e-1.

- **S1 held:** the flat lattice fails at 3×10⁻³ (×2) and 10⁻³ (×1.25); the matched-filter estimate (4×10⁻³) was close.
- **S2 held:** {7,3} L=3 at ×2 is perfect at 10⁻² and never fails within the grid, at least 10× better than my
  estimate (3×10⁻²).
- **S3 held:** at N≈316 the hyperbolic noise tolerance is ≥ 100× the flat lattice's at both contrasts, and ≈ 10× at
  N≈112.

**Reading.** At the paper's 3×10⁻⁴ precision budget both lattices localise a single-node defect perfectly, but the
flat board has only 3–10× of headroom (ε_loc ÷ 3×10⁻⁴) and the hyperbolic board more than 300×. Real hardware noise
is correlated and drifts, and any model mismatch adds error, so a 3–10× margin is thin and a 300× margin is not. The
advantage is far larger than the 8–10× ratio of boundary signals, which suggests (untested) that separating
neighbouring deep nodes, not raw amplitude, limits the flat lattice.

**Honest limits.** Twenty trials and a half-decade grid; the deepest class is a single node on the two square
lattices; oracle dictionary and known contrast set; ideal board (no tolerance); i.i.d. Gaussian noise. These limits
apply to every number in this section.

## Component tolerance (`PREREGISTRATION_10.md`, 079c835 before the run; ledger H3-X-0007)

Each trial draws a fresh random board g = 1 + τ·U[−1, 1]; baseline and defect maps come from that same board, each
with noise ε; the decoder still assumes the ideal model. τ ∈ {0.1 %, 1 %, 5 %}, ε ∈ {3×10⁻⁴, 3×10⁻³}, deepest
class, ×1.25 and ×2, 20 trials per cell, four lattices (48 cells).

**Result: 44 of 48 cells are exactly 1.00.** The four exceptions are square R=10 at ×1.25 and ε = 3×10⁻³, at
**0.60 / 0.60 / 0.55** for τ = 0.1 % / 1 % / 5 % (the ideal-board value from the noise sweep was 0.50; the standard error
at 20 trials is ≈ 0.11). Tolerance does not change them.

| Prediction | Verdict |
|---|---|
| T1: τ = 0.1 %, ε = 3×10⁻⁴, ×2: top-1 ≥ 0.9 on all four lattices | **held** |
| T2: τ = 5 %, ε = 3×10⁻⁴, ×2: square R=10 < 0.9 and {7,3} L=3 ≥ 0.9 | **refuted** (square R=10: 1.00) |
| T3: hyperbolic never noticeably worse, and ahead by ≥ 0.3 somewhere | **held** (largest lead 0.45) |

**Reading.** Component tolerance up to 5 % does not degrade single-node localisation on either geometry; the
failures that exist are set by measurement noise alone. I had reused the result that tolerance breaks *model-based
detection* (H3-X-0003, B3), but localisation here is *differential*: the tolerance is common to both maps of one
board and cancels to first order in their difference (a probable reason, not tested; lesson LL-A11). For the
physical build this removes the tolerance worry for localisation: cheap 5 % resistors are enough, provided the same
board is measured before and after and the defect is one node.

**Limits.** Tolerance only up to 5 %; noise only 3×10⁻⁴ and 3×10⁻³; 20 trials; oracle dictionary and known contrast
set; single-node defects; i.i.d. noise; a board-adapted decoder was not tried.
