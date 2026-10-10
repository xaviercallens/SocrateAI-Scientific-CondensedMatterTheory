# Protocol H4, phase 1: bench-ready procedure (companion to `LAB_GUIDE_H4.md` and `PREREGISTRATION_13.md`)

The guide says *why*; this file says *what to do, in which order, and what to write down*. Every number you need is in
a generated form under `lab/forms/` (made by `python3 lab/make_forms.py` from the design files; never typed by hand).
Each session ends by filling a copy of `forms/session_log_template.md` into `lab/data/session_log.md`.

**Rule of the whole protocol:** a gate that fails stops the sequence. You may diagnose (§6 of the guide), fix, and
re-run the gate; you may not skip it, and you may not look at the τ predictions while measuring (the script compares).
Predictions are frozen in `PREREGISTRATION_13.md`, committed before any part was bought.

## Session 0 · Simulation and dry run (laptop only, ~1 h)
- [ ] `python3 lab/bom_and_netlist.py` → regenerates `lab/out/` (BOM, wiring tables, schematics, `.cir`, `predictions_static.json`).
- [ ] `python3 lab/virtual_bench.py` → `lab/out/virtual_bench.pdf`: fit window and ADC requirement.
- [ ] `python3 lab/analyze_measurements.py --demo` → must print `T1_ratio: True`, `T2_absolute_vs_calibration: True` on synthetic records.
- [ ] `python3 lab/make_forms.py` → `lab/forms/` (components form, static-pairs form, records template, session log).
- [ ] Print: both schematics (`lab/out/*_schematic.pdf`), both wiring tables (`*_wiring.md`), `forms/components_form.csv`, `forms/static_pairs_form.csv`.
- [ ] Optional: load `lab/out/hyp73_L2_mve.cir` in ngspice/LTspice; the step response τ must match `predictions_static.json` (`tau_s_nominal`).
- Gate: the demo verdicts are both `True`. **Nothing is bought before this line is ticked.**

## Session 1 · Parts and sorting (DMM, ~2 h for 342 R + 106 C)
- [ ] Buy per `lab/out/BOM.md`. Resistors and capacitors for both boards and both calibration cells from the **same batches**.
- [ ] For every line of `forms/components_form.csv`: measure, write `measured`, write `pass` (R within 2 % of 100 kΩ; C within 10 % of 1 µF), assign a `pile` (board name or "calibration cell"). Parts that fail go to a "reject" pile, not back in the bag.
- [ ] Save the filled form as `lab/data/components.csv` (same columns).
- Gate **G1**: every part used passes. Count: 140 + 200 + 2 resistors, 35 + 69 + 2 capacitors.

## Session 2 · Build {7,3} L=2 (~4 h)
- [ ] Place per `lab/out/hyp73_L2_schematic.pdf`; solder per `lab/out/hyp73_L2_wiring.md`, deepest class first, one row at a time.
- [ ] After each row: DMM between the row's two nodes reads the resistor (not a short, not open). Tick the row on the printed table.
- [ ] Capacitors: one per interior node to the ground bus (`hyp73_L2_nodes.csv`, column `capacitor`). Boundary contacts (role `boundary`) to the rail bus.
- [ ] Calibration cell: Rcal from the rail to a pad, Ccal from the pad to ground (same chain as a probe).
- [ ] Probe pads on nodes **8, 7, 0** (depths 1, 2, 3).
- [ ] Static check: for the six `{7,3} L=2` rows of `forms/static_pairs_form.csv`, DMM between the two boundary contacts **with the rail bus disconnected** (otherwise everything is shorted); write `R_meas_ohm`.
- Gate **G2**: at least 5 of 6 pairs within 3 % of `R_eff_predicted_ohm`. A failure localises a wiring error: the pairs share nodes, so the pair that fails names the region; check that region's rows against the wiring table.

## Session 3 · Build square R=6 (~5 h)
- Same procedure with `square_R6_*`; probe pads on nodes **10, 20, 31**; six static pairs; gate **G2** on this board.

## Session 4 · Measurement chain and calibration (~3 h)
- [ ] Buffers: one op-amp follower driving the rail from the MCU step pin; one follower per probe into ADS1115 channels 0, 1, 2. Supply the op-amp from the same 3.3 V as the step. Decouple (100 nF at each supply pin).
- [ ] Flash `lab/firmware/step_logger.ino`; connect over USB; it logs `t_s,ch0,ch1,ch2` at ~280 S/s per channel for 8 s after the step, then holds 0 V.
- [ ] **Calibration cell alone** (probe channel on the cell pad): five records, saved as `lab/data/hyp73_L2_cal00.csv` … `cal04.csv` (and likewise for the square board's cell).
- [ ] Fill `lab/data/h4_records.json` from `forms/h4_records_template.json` (file names, probe nodes, temperature, humidity).
- Gate **G4**: `python3 lab/analyze_measurements.py` reports τ_cal within 5 % of 0.100 s and the five records within 1 % of each other. If not, the chain is wrong, not the boards: check supply rails at the op-amp, ADC gain setting, the cell's C.

## Session 5 · Measure both boards (~2 h, same temperature for both)
- [ ] Per board, five step records: rail 0 → 3.3 V, record 8 s, hold 0 V ≥ 8 s before the next. Save as `lab/data/hyp73_L2_run00.csv` … `run04.csv` and `square_R6_run00.csv` … `run04.csv`.
- [ ] Write temperature and humidity into `h4_records.json` for each board. Do not open `predictions_static.json`.
- [ ] `python3 lab/analyze_measurements.py` → `lab/data/h4_step_response.json` with the verdicts.
- Gate **G3**: the three probes of each record agree on τ within 3 %, ≥ 8 samples in the fit window. The S-shaped onset of the deepest probe is expected.

## Session 6 · Record (laptop, ~1 h; RUNBOOK steps 6–8)
- [ ] Claim file for `H4-X-0001` (tier X, evidence `lab/data/h4_step_response.json`, statement built from its `verdicts`: T1_ratio, T2_absolute_vs_calibration, S1_static), then `python3 tools/ledger_add.py`.
- [ ] `python3 tools/experiment_gate.py` → `ALL PASS` (it checks that `PREREGISTRATION_13.md` was committed before the data file).
- [ ] Results block in `LAB_RESULTS.md` (RUNBOOK §4), numbers copied from the data file. A refuted prediction is written with the same prominence as a confirmed one.
- [ ] Commit `lab/data/*.csv`, `h4_records.json`, `h4_step_response.json`, `components.csv`, `session_log.md` (the `.gitignore` excludes only `demo_*`).

## Predictions being tested (copied from `PREREGISTRATION_13.md`; do not reread during sessions 4–5)
| Id | Statement | Band |
|---|---|---|
| T1 | τ({7,3} L=2) / τ(square R=6) | 0.604 ± 0.03 |
| T2 | τ / τ_cal, {7,3} L=2 and square R=6 | 2.750 ± 0.08 and 4.551 ± 0.14 |
| S1 | boundary-pair resistances (G2) | all within 3 % |

## Forms (generated)
| File | Used in | Becomes |
|---|---|---|
| `forms/components_form.csv` | session 1 | `lab/data/components.csv` |
| `forms/static_pairs_form.csv` | sessions 2–3 | the `static_ohms` block of `h4_records.json` |
| `forms/h4_records_template.json` | sessions 4–5 | `lab/data/h4_records.json` |
| `forms/session_log_template.md` | every session | `lab/data/session_log.md` |
