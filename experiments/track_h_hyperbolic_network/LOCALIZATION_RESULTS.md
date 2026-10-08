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

## Localisation under correlated hardware noise (PREREGISTRATION_17.md, committed before the run; ledger H3-X-0009)

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

### {7,3} L=2

| Cell | top-1 |
|---|---|
| none plain | 1.00 |
| none mean_removed | 1.00 |
| none gain_fitted | 1.00 |
| offset0.0001 plain | 1.00 |
| offset0.0001 mean_removed | 1.00 |
| offset0.001 plain | 1.00 |
| offset0.001 mean_removed | 1.00 |
| offset0.01 plain | 1.00 |
| offset0.01 mean_removed | 1.00 |
| offset0.1 plain | 1.00 |
| offset0.1 mean_removed | 1.00 |
| drift0.0001 plain | 1.00 |
| drift0.0001 gain_fitted | 1.00 |
| drift0.0003 plain | 1.00 |
| drift0.0003 gain_fitted | 1.00 |
| drift0.001 plain | 1.00 |
| drift0.001 gain_fitted | 1.00 |
| drift0.003 plain | 1.00 |
| drift0.003 gain_fitted | 1.00 |
| drift0.01 plain | 1.00 |
| drift0.01 gain_fitted | 1.00 |
| bits10 plain | 1.00 |
| bits12 plain | 1.00 |
| bits14 plain | 1.00 |
| bits16 plain | 1.00 |

### square R=6

| Cell | top-1 |
|---|---|
| none plain | 1.00 |
| none mean_removed | 1.00 |
| none gain_fitted | 1.00 |
| offset0.0001 plain | 1.00 |
| offset0.0001 mean_removed | 1.00 |
| offset0.001 plain | 1.00 |
| offset0.001 mean_removed | 1.00 |
| offset0.01 plain | 1.00 |
| offset0.01 mean_removed | 1.00 |
| offset0.1 plain | 1.00 |
| offset0.1 mean_removed | 1.00 |
| drift0.0001 plain | 1.00 |
| drift0.0001 gain_fitted | 1.00 |
| drift0.0003 plain | 1.00 |
| drift0.0003 gain_fitted | 1.00 |
| drift0.001 plain | 1.00 |
| drift0.001 gain_fitted | 1.00 |
| drift0.003 plain | 1.00 |
| drift0.003 gain_fitted | 1.00 |
| drift0.01 plain | 0.95 |
| drift0.01 gain_fitted | 1.00 |
| bits10 plain | 1.00 |
| bits12 plain | 1.00 |
| bits14 plain | 1.00 |
| bits16 plain | 1.00 |

| Prediction | Threshold | Verdict |
|---|---|---|
| G1 | with none of the three (i.i.d. 3×10⁻⁴ only) both boards give top-1 ≥ 0.9 | **held** |
| G2 | mean removal and gain fitting change nothing in the G1 condition (top-1 ≥ 0.9 with them as well) | **held** |
| P1 | 12 bits (q = 2.4×10⁻⁴, at the budget) leaves both boards at top-1 ≥ 0.9; 10 bits (q = 9.8×10⁻⁴) drops square R=6 below 0.9 while {7,3} L=2 stays ≥ 0.9 | **refuted** |
| P2 | Without mean removal: square R=6 < 0.9 at ε_o = 1e-2 and ≥ 0.9 at 1e-3; {7,3} L=2 ≥ 0.9 at 1e-2 and < 0.9 at 1e-1. With mean removal both boards stay ≥ 0.9 at every ε_o up to 1e-1 | **refuted** |
| P3 | Without gain fitting: at ε_g = 1e-3 square R=6 < 0.9 and {7,3} L=2 ≥ 0.9; at ε_g = 1e-2 both < 0.9. With gain fitting both boards stay ≥ 0.9 up to ε_g = 1e-2 | **refuted** |

**Limits:** Localisation on real hardware; noise with time structure inside one map; multi-node defects; nothing about holography.

*Recorded by a low-tier agent (runbook steps 6–8); audited with `tools/audit_low_tier.py` (pass). The reading below is mid-tier.*

**Reading.** All three predictions are refuted in the safe direction: 49 of 50 cells are at 1.00 and the lowest, square
R=6 under 1 % gain drift without correction, is 0.95. At N≈112 and contrast ×2, a common-mode offset of up to 10 % of
the rms entry, a gain drift of up to 1 % between the two maps, and a 10-bit ADC all leave single-node localisation
intact, on either board, with the plain decoder; the mean-removal and gain-fitting corrections were never needed. I
predicted failures from the size of the perturbation relative to the defect signal (H3-X-0004); that reasoning ignores
that the matched filter decides by *differences between candidate signatures*, which a rank-one offset or a common
gain barely changes (hypothesis, untested). This is a ceiling result (LL-A10): the grid did not reach the failure
boundary, so it bounds the hardware requirements from below without locating them. For the build (H-4 phase 2) the
consequence is practical: for defect localisation the measurement chain of phase 1 (16-bit ADC) is more than enough,
and even the excluded 10-bit ADC would do for this task; the 12-bit requirement of the virtual bench applies to the
τ measurement, not to localisation. The other direction of the question, the smallest contrast the chain can localise
under these perturbations, is untested.

## Hardware-like perturbations driven to failure (`PREREGISTRATION_22.md`, c044fd8 before the run; ledger H3-X-0010)
Design: Boards: {7,3} L=2 and square R=6 (the two boards of the garage build); contrasts f ∈ {2, 1.25}; deepest depth class
(7 equivalent nodes on {7,3}, 1 node on the square); i.i.d. noise 3×10⁻⁴ (the budget) on each map as in H3-X-0009;
**40 trials per cell**, noise draws common to all cells of a (board, contrast), so that decisions can be compared
trial by trial; decoder, dictionary and node list from `exp17_localisation_under_correlated_hardware_n.py` (matched
filter over all interior nodes, contrasts {0.1, 0.5, 0.8, 1.25, 2, 5, 10, 100}). Perturbation families:
- **Offsets** u1ᵀ, 1wᵀ and u1ᵀ + 1wᵀ with entries N(0, (k·s)²), independent per map, k ∈ {1, 10, 100}, plain decoder.
- **Scalar drift** σ ∈ {10⁻³, 3×10⁻³, 10⁻², 3×10⁻², 10⁻¹, 3×10⁻¹, 1}: second map scaled by (1 + δ), δ ~ N(0, σ²),
  plain decoder; and the gain-fitted decoder at σ ∈ {0.1, 0.3} for f = 2.
- **Quantisation** to 1, 2, 3, 4, 5, 6, 7, 8, 10 bits (step 2^(−bits)·s), plain decoder.
- **Per-channel gain mismatch (exploratory, no prediction):** row gains (1 + g_i), g_i ~ N(0, σ_g²) independent per
  channel and per map, σ_g ∈ {10⁻³, 3×10⁻³, 10⁻², 3×10⁻², 10⁻¹, 3×10⁻¹}, plain decoder. This is what channel-to-channel
  gain differences between two measurements would look like; it is not invisible (a diagonal scaling of P).
Data file: `data/hardware_noise_failure_boundaries.json`.
Data: `data/hardware_noise_failure_boundaries.json`.

**(a) Offsets** (`differs_from_baseline`, trials whose decoded node differs from the unperturbed decode)

| Board | f | structure | scale 1 | scale 10 | scale 100 |
|---|---|---|---|---|---|
| {7,3} L=2 | 2 | row | 0 | 0 | 0 |
| {7,3} L=2 | 2 | col | 0 | 0 | 0 |
| {7,3} L=2 | 2 | both | 0 | 0 | 0 |
| {7,3} L=2 | 1.25 | row | 0 | 0 | 0 |
| {7,3} L=2 | 1.25 | col | 0 | 0 | 0 |
| {7,3} L=2 | 1.25 | both | 0 | 0 | 0 |
| square R=6 | 2 | row | 0 | 0 | 0 |
| square R=6 | 2 | col | 0 | 0 | 0 |
| square R=6 | 2 | both | 0 | 0 | 0 |
| square R=6 | 1.25 | row | 0 | 0 | 0 |
| square R=6 | 1.25 | col | 0 | 0 | 0 |
| square R=6 | 1.25 | both | 0 | 0 | 0 |

**(b) Scalar drift** (top-1, measured and preregistered/predicted, by σ)

| Board | f | quantity | σ 0.001 | σ 0.003 | σ 0.01 | σ 0.03 | σ 0.1 | σ 0.3 | σ 1 |
|---|---|---|---|---|---|---|---|---|---|
| {7,3} L=2 | 2 | measured | 1.00 | 1.00 | 1.00 | 0.975 | 0.650 | 0.600 | 0.250 |
| {7,3} L=2 | 2 | predicted | 1.00 | 1.00 | 1.00 | 0.943 | 0.682 | 0.563 | 0.360 |
| {7,3} L=2 | 1.25 | measured | 1.00 | 1.00 | 0.925 | 0.550 | 0.625 | 0.500 | 0.325 |
| {7,3} L=2 | 1.25 | predicted | 1.00 | 1.00 | 0.917 | 0.678 | 0.555 | 0.518 | 0.347 |
| square R=6 | 2 | measured | 1.00 | 1.00 | 0.975 | 0.700 | 0.500 | 0.175 | 0.0500 |
| square R=6 | 2 | predicted | 1.00 | 1.00 | 0.940 | 0.805 | 0.556 | 0.221 | 0.0687 |
| square R=6 | 1.25 | measured | 1.00 | 1.00 | 0.900 | 0.950 | 0.525 | 0.275 | 0.0750 |
| square R=6 | 1.25 | predicted | 1.00 | 1.00 | 0.925 | 0.932 | 0.610 | 0.239 | 0.0727 |

Gain-fitted decoder (f = 2 only):

| Board | f | gain-fitted top-1 σ 0.1 | σ 0.3 |
|---|---|---|---|
| {7,3} L=2 | 2 | 1.00 | 1.00 |
| square R=6 | 2 | 1.00 | 1.00 |

**(c) Quantisation** (top-1 by bit count)

| Board | f | bits 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| {7,3} L=2 | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| {7,3} L=2 | 1.25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 2 | 1.00 | 0.875 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| square R=6 | 1.25 | 1.00 | 0.175 | 0.600 | 0.975 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

**(d) Per-channel gain mismatch (EXPLORATORY, no prediction)** (top-1 by σ_g)

| Board | f | sigma_g=0.001 | 0.003 | 0.01 | 0.03 | 0.1 | 0.3 |
|---|---|---|---|---|---|---|---|
| {7,3} L=2 | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 0.725 | 0.0500 |
| {7,3} L=2 | 1.25 | 1.00 | 1.00 | 1.00 | 0.800 | 0.0500 | 0.00 |
| square R=6 | 2 | 1.00 | 1.00 | 0.650 | 0.0750 | 0.00 | 0.00 |
| square R=6 | 1.25 | 1.00 | 0.575 | 0.0250 | 0.00 | 0.00 | 0.00 |

**(e) First failure** (first grid value with top-1 < 0.9)

| Board | f | first drift sigma with top-1<0.9 | first bit count (descending from 10) with top-1<0.9 | first per-channel sigma_g with top-1<0.9 |
|---|---|---|---|---|
| {7,3} L=2 | 2 | 0.1 | none | 0.1 |
| {7,3} L=2 | 1.25 | 0.03 | none | 0.03 |
| square R=6 | 2 | 0.03 | 2 | 0.01 |
| square R=6 | 1.25 | 0.1 | 3 | 0.003 |

**Verdicts**

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | top-1 ≥ 0.9 with i.i.d. noise only, all four (board, contrast) cells | baseline top-1 1.00 in all four cells | PASS |
| G2 | largest absolute row sum and column sum ≤ 10⁻⁹ of the largest entry, both boards | {7,3} L=2: row 2.58e-12, col 7.24e-13; square R=6: row 4.24e-12, col 2.36e-13 | PASS |
| G3 | noiseless decode returns the true node for every node, both contrasts, both boards | noiseless_ok true in all four cells | PASS |
| G4 | recomputed drift predictions agree with the preregistered table to 2×10⁻³ | agreement verdict true (the recomputed deviation itself is not in the data file) | PASS |
| P1 | 0 trials whose decoded node differs from the unperturbed decode, every offset structure, scale, board and contrast | differs_from_baseline 0 in every offset cell | held |
| P2 | every (board, contrast, σ) cell within 3·√(p(1 − p)/40) + 0.05 of the predicted p | max_abs_drift_deviation 0.128 | held |
| P3 | gain-fitted top-1 ≥ 0.9 at σ = 0.3, f = 2, both boards | {7,3} L=2: 1.00; square R=6: 1.00 | held |
| P4 | top-1 ≥ 0.9 at every bit count above b_hi and ≥ 0.8 at b_hi ({7,3} L=2 f=2 b_hi 2; square R=6 f=2 b_hi 5; {7,3} L=2 f=1.25 b_hi 4; square R=6 f=1.25 b_hi 7) | {7,3} L=2 f=2: all bit counts 1.00; square R=6 f=2 bits 5–10: all 1.00; {7,3} L=2 f=1.25 bits 4–10: all 1.00; square R=6 f=1.25 bits 7–10: all 1.00 | held |
| P5 | square R=6 top-1 < 0.9 at some bit count in {1, 2, 3} for f = 2 and in {1, 2, 3, 4} for f = 1.25 | square R=6 f=2: lowest top-1 0.875 (bits 1–3); square R=6 f=1.25: lowest top-1 0.175 (bits 1–4) | held |

Deviations: none.

Limits: Hardware (everything here is simulation); correlations inside one map; multi-node defects; contrasts outside {1.25, 2}; boards larger than N ≈ 113; anything about holography.

*Recorded by a low-tier agent (Haiku) from the data file; audited with `tools/audit_low_tier.py` (pass, no correction). The reading below is the orchestrator's. A post-hoc diagnostic (`exp22_diag_quantisation.py`, `data/quantisation_diagnostic.json`, not part of the preregistered tests) supports the quantisation paragraph.*

**Reading.** This is the first card of the series in which every preregistered prediction held, and the reason is that the predictions were derived from the decoder's geometry instead of guessed from perturbation sizes (LL-A16). Four findings, one qualifier each.

*Offsets cannot matter.* Every dictionary signature has zero row and column sums to 10⁻¹¹ of its largest entry (current conservation), so offsets of the form u1ᵀ, 1wᵀ or both are orthogonal to every candidate, and the decoded node was identical to the unperturbed one in every offset cell, up to 100 times the rms entry. The three refuted predictions of H3-X-0009 were therefore not luck in the safe direction; they were wrong for a reason I could have derived. Per-channel and per-injection offsets are the physically relevant ones, and they are invisible. Qualifier: only offsets that vary in both indices matter, and those are noise.

*Gain drift between the two maps is the real hazard of this family, and it is computable.* The plain decoder keeps top-1 ≥ 0.9 up to 1 % drift in all four cells (0.900 on square R=6 at f = 1.25, exactly at the threshold) and fails by 3–10 %; the gain-fitted decoder is unaffected up to 30 %. The curves predicted by integrating the noiseless decode over the drift law agree with the simulated ones within the preregistered tolerance in all 28 cells (largest deviation 0.128). Qualifier: the tolerance (three binomial standard errors plus 0.05) is generous, and two of the 28 cells were known to agree before the prediction was computed.

*Quantisation is nearly harmless on the hyperbolic board and cheap to avoid on the square.* The hyperbolic board localises at every tested bit count down to 1 bit relative to the rms entry, at both contrasts. The square board fails only at 2 bits (f = 2: 0.875, which is 35 of 40 trials, one short of the threshold, so a marginal failure) and at 2 and 3 bits (f = 1.25: 0.175 and 0.600; 0.975 at 4 bits). The failures begin one bit later than the white-noise equivalence predicted (it said at 3 bits or fewer for f = 2 and 4 bits or fewer for f = 1.25), consistent with undithered rounding being gentler than white noise. The curve is not monotone: the square board is perfect at 1 bit and poor at 2. The post-hoc diagnostic explains why: at 1 bit the quantised difference is a sparse deterministic fingerprint of the defect node (814 flipped entries on {7,3}, 80 on the square, norm several times the true signature), which an ideal undithered quantiser with aligned grids preserves, and noiselessly the decode is correct at every tested bit count on both boards, so the failures at 2 to 3 bits are the 3×10⁻⁴ noise flipping the roundings. For a converter spanning ±max|P| the step relative to the rms entry is 2^(3.10−N) on {7,3} and 2^(3.74−N) on the square (diagnostic data), so the square board needs about N ≥ 8 bits with margin and the hyperbolic board far less; the phase-1 chain (16 bits) is more than enough. Qualifier: ideal rounding only, no converter nonlinearity, no dither, both maps on the same grid.

*Per-channel gain mismatch is the requirement worth writing down (exploratory).* Independent row gains on the two maps break localisation first at σ_g = 0.003 (square, f = 1.25), 0.01 (square, f = 2), 0.03 ({7,3}, f = 1.25) and 0.1 ({7,3}, f = 2). For the phase-2 chain (a 77-channel multiplexed map), the channel-to-channel gains of the baseline and defect measurements must therefore repeat to about 0.3 % on the square board and about 1 % on the hyperbolic one; taking both maps through the same chain in one session makes that easy, and a changing amplifier between the two would not.

Limits of the whole card: simulation with an ideal dictionary at N ≈ 112, two boards, 40 trials per cell (standard error up to 0.08), one i.i.d. noise level, single-node defects, contrasts 1.25 and 2, and no joint worst case of component tolerance with these perturbations. Nothing here concerns holography.
