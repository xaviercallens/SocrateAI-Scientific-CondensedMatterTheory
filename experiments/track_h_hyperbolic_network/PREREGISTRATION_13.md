# Preregistration 13: the garage build, phase 1 (relaxation time of a physical {7,3} L=2 network)

**Date:** 2026-09-28, committed before any component is soldered. **Roadmap item:** H-4. **Guide:** `lab/LAB_GUIDE_H4.md`.
**Why:** the paper's RC result (H2-C-0001, Table 5) predicts that the slowest relaxation time of the {7,3} L=2 board
is τ = 2.750·RC and that of the square R=6 control 4.551·RC, ratio 0.604. This is the first measurement of anything
in this programme on a physical object. Phase 1 measures τ only (one driven rail, three probes); the static
Neumann-to-Dirichlet map and defect localisation are phase 2 (a later preregistration).

## Design (fixed by `lab/bom_and_netlist.py` and `lab/virtual_bench.py`)
Two boards from the same component batches: {7,3} L=2 (N=112, 140 resistors, 35 capacitors, 77 boundary contacts on
one rail) and square R=6 (N=113, 200 resistors, 69 capacitors, 44 contacts). R = 100 kΩ 1 % metal film, C = 1 µF film,
RC nominal 0.100 s. Each board carries a **calibration cell** (one R, one C from the same batches) measured the same
way, giving τ_cal ≈ RC without relying on the absolute values. Step 0 → 3.3 V on the rail through a unity-gain
buffer; three interior probes (depths 1, 2, 3: nodes 8, 7, 0 on {7,3}; 10, 20, 31 on the square) through unity-gain
buffers into a 16-bit ADC at ≥ 100 S/s per channel; records of 8 s; discharge ≥ 8 s between records; **5 records per
board**, temperature noted. Analysis: `lab/analyze_measurements.py` (tail window y/V0 ∈ [0.01, 0.10], weighted
log-linear fit, mean over probes, median over records).

## Validity gates (results are reported only if all pass)
- G1: every resistor measured within 2 % of 100 kΩ before soldering; every capacitor within 10 % of 1 µF (DMM).
- G2: continuity: the DMM resistance between each listed boundary pair matches `predictions_static.json` within 3 %
  for at least 5 of 6 pairs on each board (this also validates the wiring against the netlist).
- G3: the fit uses ≥ 8 samples in the window on every probe of every record; the three probes of a record agree on τ
  within 3 %.
- G4: the calibration-cell fit gives τ_cal within 5 % of the nominal 0.100 s (otherwise the components or the chain are wrong).

## Predictions (fixed now; thresholds from the virtual bench: fit p95 ≤ 0.6 %, tolerance spread ≤ 0.3 %, calibration cell ±1 %)
- **T1 (ratio, the main result):** τ({7,3}) / τ(square) = 0.604 ± 0.03 (i.e. within 5 %). **Refuted if** outside
  [0.574, 0.634].
- **T2 (absolute, per board):** τ / τ_cal = 2.750 ± 0.08 ({7,3}) and 4.551 ± 0.14 (square), i.e. within 3 %.
  **Refuted if** either is outside its band.
- **S1 (static):** the measured boundary-to-boundary resistances (G2) are all within 3 % of prediction.

**What a refutation would mean.** T1 outside the band with G1–G4 passing means the model of the board (ideal nodes,
no leakage, no stray capacitance) is wrong at the percent level; the first suspects are capacitor leakage (film
capacitors: > 10 GΩ, negligible; if ceramics were used, not) and perfboard leakage in a damp cellar (see the guide's
humidity note). The result is reported either way.

## Not claimed
Anything about the static map, defect detection or localisation (phase 2), about hyperbolic lattices beyond
{7,3} L=2, or about holography.
