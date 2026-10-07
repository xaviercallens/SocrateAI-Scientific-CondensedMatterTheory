#!/usr/bin/env python3
"""Generate the paper forms of the garage protocol (lab/PROTOCOL_H4.md) from the design files, so that no node
number, pair or nominal value is typed by hand. Reads lab/out/*_edges.csv, *_nodes.csv, predictions_static.json;
writes lab/forms/. Re-run after any change to lab/bom_and_netlist.py."""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT, FORMS = HERE / "out", HERE / "forms"
BOARDS = {"{7,3} L=2": ("hyp73_L2", [8, 7, 0]), "square R=6": ("square_R6", [10, 20, 31])}
PRED = json.loads((OUT / "predictions_static.json").read_text())


def rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def components_form():
    """One line per part, to be filled with the DMM reading before soldering (gate G1)."""
    lines = [["board", "part", "kind", "nominal", "tolerance_gate", "measured", "pass", "pile"]]
    for board, (slug, _) in BOARDS.items():
        for r in rows(OUT / (slug + "_edges.csv")):
            lines.append([board, r["resistor"], "R", r["R_nominal_ohm"], "2 %", "", "", ""])
        for r in rows(OUT / (slug + "_nodes.csv")):
            if r["capacitor"]:
                lines.append([board, r["capacitor"], "C", "%g" % PRED["C_nominal_F"], "10 %", "", "", ""])
        lines.append([board, "Rcal", "R", "%g" % PRED["R_nominal_ohm"], "2 %", "", "", "calibration cell"])
        lines.append([board, "Ccal", "C", "%g" % PRED["C_nominal_F"], "10 %", "", "", "calibration cell"])
    return lines


def static_form():
    """The boundary pairs of gate G2 with their predicted effective resistance; the measured column is blank."""
    lines = [["board", "boundary_i", "boundary_j", "R_eff_predicted_ohm", "gate", "R_meas_ohm", "rel_error", "pass"]]
    for board in BOARDS:
        for p in PRED["boards"][board]["static_pairs"]:
            lines.append([board, p["boundary_i"], p["boundary_j"], "%.0f" % p["R_eff_ohm"], "3 %", "", "", ""])
    return lines


def records_template():
    return {"V0": 3.3, "boards": {
        board: {"records": ["lab/data/%s_run%02d.csv" % (slug, i) for i in range(5)],
                "calibration_records": ["lab/data/%s_cal%02d.csv" % (slug, i) for i in range(5)],
                "probe_nodes": probes, "temperature_C": None, "humidity_pct": None,
                "tau_s_nominal": PRED["boards"][board]["tau_s_nominal"]}
        for board, (slug, probes) in BOARDS.items()},
        "static_ohms": {board: [{"boundary_i": p["boundary_i"], "boundary_j": p["boundary_j"], "R_meas_ohm": None}
                                for p in PRED["boards"][board]["static_pairs"]] for board in BOARDS}}


def session_log():
    return "\n".join([
        "# Session log (one block per session; fill in before leaving the bench)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Date, start, end | |",
        "| Session (protocol §) | |",
        "| Temperature °C / humidity % | |",
        "| Supply voltage at the rail (DMM) | |",
        "| Gate attempted (G1–G4) and outcome | |",
        "| Anything unexpected (symptom → PROTOCOL §6 row) | |",
        "| Files written under lab/data/ | |",
        "| Next session starts with | |",
        "",
    ])


def main():
    FORMS.mkdir(exist_ok=True)
    for name, lines in (("components_form.csv", components_form()), ("static_pairs_form.csv", static_form())):
        with open(FORMS / name, "w", newline="") as f:
            csv.writer(f).writerows(lines)
    (FORMS / "h4_records_template.json").write_text(json.dumps(records_template(), indent=1) + "\n")
    (FORMS / "session_log_template.md").write_text(session_log())
    nR = sum(1 for l in components_form()[1:] if l[2] == "R"); nC = sum(1 for l in components_form()[1:] if l[2] == "C")
    print("wrote lab/forms/: components_form.csv (%d R, %d C), static_pairs_form.csv (%d pairs), h4_records_template.json, session_log_template.md"
          % (nR, nC, len(static_form()) - 1))


if __name__ == "__main__":
    main()
