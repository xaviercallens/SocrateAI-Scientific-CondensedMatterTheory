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

**Result: 45 of 48 cells are exactly 1.00.** The three exceptions are square R=10 at ×1.25 and ε = 3×10⁻³, at
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

## Minimum detectable contrast (PREREGISTRATION_12.md, committed before the run; ledger H3-X-0008)

Same decoder and dictionary construction as `localize_noise.py` (ideal board, matched filter over all interior nodes, dictionary contrasts D = {0.1, 0.5, 0.8, 0.9, 1.1, 1.25, 1.5, 2, 5, 10, 100}, differential measurement with independent i.i.d. Gaussian noise ε on each map). Deepest class of each of the four lattices ({7,3} L=2, square R=6, {7,3} L=3, square R=10). True contrasts f ∈ {0.5, 0.8, 0.9, 1.1, 1.25, 1.5, 2}; noise ε ∈ {1e-4, 3e-4, 1e-3, 3e-3}; 20 trials per cell (node cycles through the class, fresh noise per trial, seeded). Metric: top-1 node accuracy. **f_min(ε)** = the smallest |log f| among tested contrasts on each side of 1 with top-1 ≥ 0.9 at that ε.

| Lattice | f | eps=1e-4 | eps=3e-4 | eps=1e-3 | eps=3e-3 |
|---|---|---|---|---|---|
| {7,3} L=2 | 0.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 0.8 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 0.9 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 1.1 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 1.25 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 1.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 2.0 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 0.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 0.8 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 0.9 | 1.00 | 1.00 | 1.00 | 0.85 |
| square R=6 | 1.1 | 1.00 | 1.00 | 1.00 | 0.90 |
| square R=6 | 1.25 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 1.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 2.0 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 0.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 0.8 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 0.9 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 1.1 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 1.25 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 1.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=3 | 2.0 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=10 | 0.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=10 | 0.8 | 1.00 | 1.00 | 1.00 | 0.55 |
| square R=10 | 0.9 | 1.00 | 1.00 | 0.70 | 0.10 |
| square R=10 | 1.1 | 1.00 | 1.00 | 0.90 | 0.05 |
| square R=10 | 1.25 | 1.00 | 1.00 | 1.00 | 0.60 |
| square R=10 | 1.5 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=10 | 2.0 | 1.00 | 1.00 | 1.00 | 1.00 |

| Prediction | Threshold | Verdict |
|---|---|---|
| G1 | every lattice top-1 ≥ 0.9 at ε=3e-4, f=2 | **held** |
| G2 | dictionary contains every true contrast | **held** |
| P1 | {7,3} L=3 top-1 ≥ 0.9 at f ∈ {0.9, 1.1}, ε=3e-4 | **held** |
| P2 | square R=10 top-1 ≤ 0.5 at f ∈ {0.9, 1.1}, ε=3e-4 | **refuted** (both 1.00) |
| P3 | abs(top-1(f=0.9) − top-1(f=1.1)) ≤ 0.2 and abs(top-1(f=0.8) − top-1(f=1.25)) ≤ 0.2 for every lattice, ε | **refuted** by `score()`; see the scorer correction below |
| P4 | top-1({7,3} L=3) ≥ top-1(square R=10) − 0.1 for every f, ε | **held** |

**Limits:** Anything with component tolerance (H3-X-0007 covered it for f ≥ 1.25 only), multi-node defects, contrasts outside D, non-Gaussian noise, or sizes beyond N ≈ 317. Nothing about holography.

*Recorded by a low-tier agent (runbook steps 6–8); audited with `tools/audit_low_tier.py` (pass). The reading below is mid-tier.*

**Scorer correction (P3).** The only cell that made `score()` return P3 = false is square R=10 at ε = 10⁻³: 0.70 at
f = 0.9 against 0.90 at f = 1.1, i.e. 14 against 18 correct trials out of 20, a difference of exactly 4/20 = 0.2, which
the preregistered rule (≤ 0.2) allows. The script compared floats and got 0.20000000000000007 > 0.2. Applied to the
trial counts, the preregistered rule **holds** in every cell. The data file and the ledger statement keep the
script's output (statements are never edited); the correction is appended to the notes of H3-X-0008 (lesson LL-D11).

**Reading.** P2 is refuted, as the audit anticipated before the run: at the 3×10⁻⁴ budget the flat R=10 board localises
a ±10 % single-node change perfectly, just like the hyperbolic one. The difference appears only above the budget: at
3×10⁻³ the smallest contrast the flat R=10 board still localises (top-1 ≥ 0.9) is f = 0.5 or 1.5, against 0.9 or 1.1 for
{7,3} L=3 and {7,3} L=2. This fits H3-X-0006: at ideal noise both geometries localise; the hyperbolic advantage is noise
margin, now also measured in contrast (≈ 5× smaller detectable |log f| at 3×10⁻³). For the garage build, a ±10 %
component fault at the deepest node is localisable on either board at the budget noise, and only the hyperbolic board
keeps that resolution with ten times more noise.
