#!/usr/bin/env python3
"""Ledger entries for PREREGISTRATION_3 (v1.0 peer-review revisions). Idempotent;
each part is recorded only when its data file exists, so the script is re-run
as results arrive. Statements of earlier claims are never edited; corrections
are appended to their notes.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def h(name):
    return "sha256:" + hashlib.sha256((DATA / name).read_bytes()).hexdigest()


def part_c():
    rows = json.loads((DATA / "subspace_control.json").read_text())
    r117, r306 = rows[0], rows[1]
    return {
        "id": "H0-X-0005", "tier": "X", "kind": "numeric", "depends_on": ["H0-X-0003"],
        "evidence": h("subspace_control.json"),
        "statement": (
            "PREREGISTRATION_3 part C, prediction REFUTED. The probe-matched gap of H0-X-0003 is mostly a "
            "dimensionality effect. Against the square lattice's best-conditioned r-dimensional parameter subspace "
            "(top-r right singular vectors, r = hyperbolic identifiable dimension): at N~112, r=117, square "
            f"log10(sigma_1/sigma_r) = {r117['square_log10_sigma1_over_sigma_r']:.2f} < hyperbolic kappa_id "
            f"{r117['hyp_log10_kappa_identifiable']:.2f} (flat BETTER by 0.56 decades); at N~316, r=306, square "
            f"{r306['square_log10_sigma1_over_sigma_r']:.2f} vs hyperbolic {r306['hyp_log10_kappa_identifiable']:.2f} "
            "(hyperbolic better by 0.48 decades, not the predicted 1-4). At matched probe count AND matched "
            "dimension the residual conditioning advantage is at most half a decade at these sizes."),
        "notes": ("experiments/track_h_hyperbolic_network/subspace_control.py. The full-boundary comparison "
                  "(H0-X-0002: 6.4 decades at N~316) is unaffected: the large boundary IS the geometry. What "
                  "is withdrawn is the v1.0 reading that the advantage is independent of probe count."),
    }


def part_b():
    d = json.loads((DATA / "disorder.json").read_text())["summary_median_logparam"]
    def f(x): return "SING." if x is None else f"{x:.2f}"
    u, lu, d100, d001, unit = d["U[0.5,1.5]"], d["logU[0.1,10]"], d["defect x100"], d["defect x0.01"], d["unit"]
    verdict1 = None if u["gap_N316"] is None else ("REFUTED" if u["gap_N316"] < 3 else "as predicted")
    verdict2 = None if lu["gap_N316"] is None else ("REFUTED" if lu["gap_N316"] < 2 else "as predicted")
    dh = max(abs((d100["{7,3} L=3"] or 0) - unit["{7,3} L=3"]), abs((d001["{7,3} L=3"] or 0) - unit["{7,3} L=3"]))
    return {
        "id": "H0-X-0006", "tier": "X", "kind": "numeric", "depends_on": [],
        "evidence": h("disorder.json"),
        "statement": (
            "PREREGISTRATION_3 part B (log-parametrised kappa, medians over 5 seeds). Mild disorder U[0.5,1.5]: "
            f"gap at N~316 = {f(u['gap_N316'])} decades ({verdict1}; prediction >= 5, refute < 3); {{7,3}} L=3 "
            f"moved from {f(unit['{7,3} L=3'])} to {f(u['{7,3} L=3'])}. Strong disorder logU[0.1,10]: gap at "
            f"N~316 = {f(lu['gap_N316'])} ({verdict2}; prediction >= 3, refute < 2), at N~112 = {f(lu['gap_N112'])}. "
            f"Defects x100 / x0.01 at maximal depth: {{7,3}} L=3 kappa {f(d100['{7,3} L=3'])} / {f(d001['{7,3} L=3'])} "
            f"(max change {dh:.2f} decades; prediction < 2, refute > 3)."),
        "notes": "experiments/track_h_hyperbolic_network/disorder.py; float64; SINGULAR rows excluded from medians.",
    }


def part_a():
    rows = json.loads((DATA / "flat_scaling_mp.json").read_text())
    pred = json.loads((DATA / "prereg3_predictions.json").read_text())
    ctrl = [r for r in rows if r["control_pass"] is not None]
    sat = [r for r in rows if r["control_pass"] is None]
    if len(sat) < 3:  # the run is still in progress; never record a partial claim
        return None
    txt = "; ".join(f"{r['case']}: log10 kappa = {r['log10_kappa_arb']:.2f} (radius {r['max_rel_radius_Ginv']:.0e})"
                    for r in sat)
    preds = "; ".join(f"{fam} N={n}: exp {p['exp_sqrtN']}, power {p['power_last_exponent']}"
                      for fam in pred for n, p in pred[fam]["predictions"].items())
    ctrl_txt = ", ".join(r["case"] + ": |d log10 kappa| < 1e-6" for r in ctrl)
    return {
        "id": "H0-X-0007", "tier": "X", "kind": "numeric", "depends_on": ["H0-X-0002"],
        "evidence": h("flat_scaling_mp.json"),
        "statement": (
            "PREREGISTRATION_3 part A: flat-lattice kappa beyond float64, Arb ball arithmetic (512 bits), "
            f"controls on unsaturated cases pass ({ctrl_txt}). "
            f"Results: {txt}. Preregistered extrapolations: {preds}. Verdict recorded in the paper's sec. 3.1 "
            "from the decision rule of PREREGISTRATION_3.A."),
        "notes": "experiments/track_h_hyperbolic_network/flat_scaling_mp.py; certified radii; lambda_max in float64.",
    }


def main():
    d = json.loads(LEDGER.read_text())
    have = {c["id"] for c in d["claims"]}
    for c in d["claims"]:
        if c["id"] == "H0-X-0003" and "CORRECTION" not in (c.get("notes") or "") and (DATA / "subspace_control.json").exists():
            c["notes"] = (c.get("notes") or "") + (" CORRECTION (2026-09-27, appended; statement unchanged): the 6.75-decade "
                                                   "gap compares subspaces of different dimension; see H0-X-0005 -- "
                                                   "against the flat lattice's best r-dimensional subspace the residual is "
                                                   "<= 0.5 decades and reversed at N~112.")
            print("corrected notes of H0-X-0003")
    for fn, req in ((part_c, "subspace_control.json"), (part_b, "disorder.json"), (part_a, "flat_scaling_mp.json")):
        if not (DATA / req).exists():
            print(f"  {req} not yet available; skipped"); continue
        c = fn()
        if c is None:
            print(f"  {req} incomplete; skipped"); continue
        c.setdefault("audit", None)
        if c["id"] not in have:
            d["claims"].append(c); print("added", c["id"])
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
