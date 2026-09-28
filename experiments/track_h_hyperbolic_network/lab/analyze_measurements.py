#!/usr/bin/env python3
"""Analyse the real step-response records of the garage build (PREREGISTRATION_13.md) with the SAME fit as the
virtual bench, and score the predictions from the data alone.

Input: CSV files written by the logger (one per record): header `t_s,ch0,ch1,ch2[,...]`, t in seconds from the
step, channels in volts (already converted from ADC codes by the logger), plus a small JSON of metadata:
  lab/data/h4_records.json = {"V0": 3.3, "boards": {"{7,3} L=2": {"records": ["lab/data/hyp_run01.csv", ...],
                              "calibration_records": ["lab/data/hyp_cal01.csv", ...], "probe_nodes": [8, 7, 0]},
                              "square R=6": {...}}, "static_ohms": {"{7,3} L=2": [{"boundary_i":..,"boundary_j":..,"R_meas_ohm":..}, ...]}}
Output: lab/data/h4_step_response.json with per-record tau, per-board tau (median over records), tau_cal, ratios,
static comparisons and the verdicts of PREREGISTRATION_13.md. Run `python3 lab/analyze_measurements.py --demo`
to exercise the pipeline on virtual-bench records (writes lab/data/demo_*.csv first).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
from virtual_bench import Y_HI, Y_LO, adc, board_response, fit_tau  # noqa: E402

DATA = HERE / "data"
META = DATA / "h4_records.json"
OUT = DATA / "h4_step_response.json"
PRED = json.loads((HERE / "out" / "predictions_static.json").read_text())


def read_csv(path):
    with open(path) as f:
        rows = list(csv.reader(f))
    hdr, body = rows[0], np.array(rows[1:], float)
    return body[:, 0], body[:, 1:].T


def tau_of_record(path, V0):
    ts, Vs = read_csv(path)
    import virtual_bench as vb
    vb.V0 = V0
    return fit_tau(ts, Vs, (Y_LO, Y_HI))[0]


def score(d):
    b = d["boards"]; p = PRED["boards"]
    hyp, sq = b["{7,3} L=2"], b["square R=6"]
    ratio = hyp["tau_s"] / sq["tau_s"]
    T1 = abs(ratio / PRED["tau_ratio_hyp_over_square"] - 1) <= 0.03
    T2 = all(abs(b[k]["tau_s"] / (p[k]["tau_factor"] * b[k]["tau_cal_s"]) - 1) <= 0.03 for k in b if b[k].get("tau_cal_s"))
    S1 = all(abs(m["R_meas_ohm"] / m["R_pred_ohm"] - 1) <= 0.03 for k in d["static"] for m in d["static"][k]) if d["static"] else None
    return {"T1_ratio": T1, "T2_absolute_vs_calibration": T2, "S1_static": S1, "tau_ratio_measured": ratio,
            "tau_ratio_predicted": PRED["tau_ratio_hyp_over_square"]}


def main():
    demo = "--demo" in sys.argv
    DATA.mkdir(exist_ok=True)
    global META, OUT
    if demo:  # synthetic records from the virtual bench, 16 bit, 860 S/s, 1 % parts; never the real data paths
        META, OUT = DATA / "demo_h4_records.json", DATA / "demo_h4_step_response.json"
        from hyperbolic_network import build_hyperbolic, build_square_disk
        meta = {"V0": 3.3, "boards": {}, "static_ohms": {}}
        for name, build, tag in (("{7,3} L=2", build_hyperbolic, "hyp"), ("square R=6", build_square_disk, "sq")):
            g = build(7, 3, 2) if tag == "hyp" else build(6)
            recs = []
            for i in range(3):
                rng = np.random.default_rng(500 + i)
                t, V, *_ = board_response(g, rng, 0.01, 0.01)
                ts, Vs = adc(t, V, 860, 16, 1.0, rng)
                pth = DATA / ("demo_%s_run%02d.csv" % (tag, i))
                with open(pth, "w", newline="") as f:
                    w = csv.writer(f); w.writerow(["t_s"] + ["ch%d" % k for k in range(len(Vs))]); w.writerows(np.column_stack([ts, Vs.T]))
                recs.append(str(pth.relative_to(HERE.parent)))
            # calibration cell: single RC with 1 % parts, same ADC
            rng = np.random.default_rng(900); rc = 0.1 * (1 + 0.01 * rng.uniform(-1, 1)) * (1 + 0.01 * rng.uniform(-1, 1))
            t = np.arange(0, 1.0, 1 / 20000); V = (3.3 * (1 - np.exp(-t / rc)))[None, :]
            ts, Vs = adc(t, V, 860, 16, 1.0, rng)
            pth = DATA / ("demo_%s_cal.csv" % tag)
            with open(pth, "w", newline="") as f:
                w = csv.writer(f); w.writerow(["t_s", "ch0"]); w.writerows(np.column_stack([ts, Vs.T]))
            meta["boards"][name] = {"records": recs, "calibration_records": [str(pth.relative_to(HERE.parent))]}
        META.write_text(json.dumps(meta, indent=1))
    meta = json.loads(META.read_text())
    out = {"boards": {}, "static": {}}
    for name, m in meta["boards"].items():
        taus = [tau_of_record(HERE.parent / r, meta["V0"]) for r in m["records"]]
        cals = [tau_of_record(HERE.parent / r, meta["V0"]) for r in m.get("calibration_records", [])]
        out["boards"][name] = {"tau_per_record_s": taus, "tau_s": float(np.median(taus)),
                               "tau_cal_s": float(np.median(cals)) if cals else None,
                               "tau_nominal_s": PRED["boards"][name]["tau_s_nominal"]}
        print("%-11s tau = %.4f s (records: %s)  tau_cal = %s  nominal %.4f s  tau/tau_cal = %s (predicted factor %.3f)" % (
            name, out["boards"][name]["tau_s"], ", ".join("%.4f" % x for x in taus),
            ("%.4f" % out["boards"][name]["tau_cal_s"]) if cals else "n/a", PRED["boards"][name]["tau_s_nominal"],
            ("%.3f" % (out["boards"][name]["tau_s"] / out["boards"][name]["tau_cal_s"])) if cals else "n/a", PRED["boards"][name]["tau_factor"]))
    for name, rows in meta.get("static_ohms", {}).items():
        pred = {(q["boundary_i"], q["boundary_j"]): q["R_eff_ohm"] for q in PRED["boards"][name]["static_pairs"]}
        out["static"][name] = [{**r, "R_pred_ohm": pred.get((r["boundary_i"], r["boundary_j"]))} for r in rows]
    out["verdicts"] = score(out)
    OUT.write_text(json.dumps(out, indent=1))
    print("verdicts:", out["verdicts"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
