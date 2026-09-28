#!/usr/bin/env python3
"""Build a supervised / RL / JEPA-style physics dataset from this project's
verified record: preregistered predictions paired with what was measured, and
every ledger claim with its tier and verdict.

Outputs (committed; small, reviewable):
  training/physics_predictions.jsonl  one record per preregistered prediction:
        context (setup), prediction (value/band/rival forms), outcome (measured,
        read from data/*.json), verdict, energy (0 = confirmed inside band,
        1 = refuted; ANSE convention: lower is better), source files.
  training/ledger_claims.jsonl        every Elenchus claim: statement, tier, kind,
        dependencies, verdict label, evidence digest.

Rules: every number comes from a data file or the ledger, never typed here;
refutations and deviations are kept (they are the most informative labels).

    python3 tools/build_physics_verdicts.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACK = ROOT / "experiments" / "track_h_hyperbolic_network"
D = TRACK / "data"
OUT = ROOT / "training"


def load(name):
    return json.loads((D / name).read_text())


def verdict_of(statement: str, notes: str) -> str:
    s = (statement + " " + (notes or "")).upper()
    for key, label in (("RETRACTS", "retraction"), ("SUPERSEDED", "superseded"), ("REFUTED", "refuted"),
                       ("DEVIATION", "deviation"), ("EXPLORATORY", "exploratory"), ("CORRECTS", "correction"),
                       ("CONFIRMED", "confirmed")):
        if key in s:
            return label
    return "asserted"


def predictions():
    h0 = {r["name"]: r for r in load("h0.json")}
    L4 = h0["{7,3} L=4"]
    rc = load("rc_network.json")
    lam = {(r["family"], r["N"]): r["lambda_min"] for r in rc["H2"]}
    ident = {r["name"]: r for r in load("identifiability.json")}
    pm = {r["name"]: r for r in load("probe_matched.json")}
    recs = []

    k = L4["log10_kappa"]
    recs.append({
        "id": "H1-L4", "source": ["PREREGISTRATION.md", "data/h0.json"],
        "context": "Resistor network on a layer-4 truncation of the hyperbolic {7,3} tiling, unit conductances, "
                   "full boundary probes; sensitivity Jacobian of the Dirichlet-to-Neumann map.",
        "prediction": {"max_depth": 7, "N_range": [800, 900], "log10_kappa": {"center": 4.2, "band": 0.5}},
        "outcome": {"max_depth": L4["max_depth"], "N": L4["N"], "log10_kappa": round(k, 3)},
        "verdict": "confirmed" if abs(k - 4.2) <= 0.5 and L4["max_depth"] == 7 and 800 <= L4["N"] <= 900 else "refuted",
        "energy": 0.0 if abs(k - 4.2) <= 0.5 else 1.0,
    })
    r0, r1 = lam[("{7,3}", 112)], lam[("{7,3}", 847)]
    recs.append({
        "id": "H2-i", "source": ["PREREGISTRATION_2.md", "data/rc_network.json"],
        "context": "RC network (C=1 to ground) on {7,3} truncations L=2..4; Dirichlet spectral gap lambda_min(L_ii).",
        "prediction": {"form": "constant (bounded below)", "rivals": ["1/log^2 N", "1/N"],
                       "refuted_if": "lambda_min drops by >= 2x between L=2 and L=4"},
        "outcome": {"lambda_min_L2": round(r0, 5), "lambda_min_L4": round(r1, 5), "ratio": round(r0 / r1, 3)},
        "verdict": "refuted" if r0 / r1 >= 2 else "confirmed",
        "energy": 1.0 if r0 / r1 >= 2 else 0.0,
        "note": "Asymptotically lambda_min -> lambda_0 > 0 (domain monotonicity, ledger H2-C-0001): the refutation "
                "concerns the finite-size rate, not the existence of the limit.",
    })
    sq = [(n, v) for (f, n), v in lam.items() if f == "square"]
    sq.sort()
    slope = (__import__("math").log(sq[-1][1]) - __import__("math").log(sq[1][1])) / \
            (__import__("math").log(sq[-1][0]) - __import__("math").log(sq[1][0]))
    recs.append({
        "id": "H2-ii", "source": ["PREREGISTRATION_2.md", "data/rc_network.json"],
        "context": "Same RC model on square-lattice disks.",
        "prediction": {"form": "lambda_min ~ 1/N", "loglog_slope": -1.0},
        "outcome": {"loglog_slope_N113_to_N797": round(slope, 3)},
        "verdict": "confirmed" if abs(slope + 1) < 0.25 else "refuted",
        "energy": round(min(1.0, abs(slope + 1)), 3),
    })
    a = pm["{7,3} L=2 full boundary"]["log10_kappa_NtD"], pm["square R=6"]["log10_kappa_NtD"]
    b = pm["{7,3} L=3 full boundary"]["log10_kappa_NtD"], pm["square R=10"]["log10_kappa_NtD"]
    ok = a[0] < a[1] and b[0] < b[1]
    recs.append({
        "id": "NtD-order", "source": ["PREREGISTRATION_2.md", "data/probe_matched.json"],
        "context": "Neumann-to-Dirichlet map (what current-injection hardware measures), hyperbolic vs square.",
        "prediction": {"ordering": "kappa_NtD(hyperbolic) < kappa_NtD(square) at matched N"},
        "outcome": {"N~112": [round(x, 2) for x in a], "N~316": [round(x, 2) for x in b]},
        "verdict": "confirmed" if ok else "refuted", "energy": 0.0 if ok else 1.0,
    })
    i2, i3 = ident["{7,3} L=2, 44 probes"], ident["{7,3} L=3, 76 probes"]
    recs.append({
        "id": "probe-matched", "source": ["PREREGISTRATION_2.md", "data/identifiability.json"],
        "context": "{7,3} boundary subsampled to the square disk's probe count; unused boundary nodes carry zero current.",
        "prediction": {"log10_kappa_L3_max": 7.7, "refuted_if": "gap to square < 1 decade"},
        "outcome": {"full_jacobian": "SINGULAR by design",
                    "exact_deficiency_vs_degree2": [[i2["deficiency"], i2["unmeasured_degree2_nodes"]],
                                                    [i3["deficiency"], i3["unmeasured_degree2_nodes"]]],
                    "log10_kappa_identifiable_L3": round(i3["log10_kappa_identifiable"], 2)},
        "verdict": "deviation",
        "energy": None,
        "note": "Preregistered metric undefined (series-resistor non-identifiability); replacement metric is post hoc. "
                "Label as deviation, not as confirmation.",
    })
    # ---- PREREGISTRATION_3 (peer-review revisions, v1.1) ----
    sub = D / "subspace_control.json"
    if sub.exists():
        rows = json.loads(sub.read_text())
        r117, r306 = rows[0], rows[1]
        recs.append({
            "id": "P3-C-dimension", "source": ["PREREGISTRATION_3.md", "data/subspace_control.json"],
            "context": "Probe-matched control: square lattice's best-conditioned r-dimensional parameter subspace "
                       "(sigma_1/sigma_r) vs hyperbolic identifiable-subspace kappa, r = hyperbolic identifiable dimension.",
            "prediction": {"square_log10_sigma1_over_sigma306": "between 4 and 7", "ordering": "flat > hyperbolic at both r"},
            "outcome": {"r117": [round(r117["square_log10_sigma1_over_sigma_r"], 2), r117["hyp_log10_kappa_identifiable"]],
                        "r306": [round(r306["square_log10_sigma1_over_sigma_r"], 2), r306["hyp_log10_kappa_identifiable"]]},
            "verdict": "refuted", "energy": 1.0,
            "note": "Flat is BETTER at r=117; only 0.48 decades worse at r=306. Corrects v1.0's probe-matching claim.",
        })
    dis = D / "disorder.json"
    if dis.exists():
        s = json.loads(dis.read_text())["summary_median_logparam"]
        for regime, pred, refute, key in (("U[0.5,1.5]", ">= 5 decades", "< 3", "gap_N316"),
                                          ("logU[0.1,10]", ">= 3 decades", "< 2", "gap_N316")):
            gap = s[regime][key]
            ok = gap is not None and gap >= float(pred.split()[1])
            recs.append({
                "id": f"P3-B-{regime}", "source": ["PREREGISTRATION_3.md", "data/disorder.json"],
                "context": f"Conditioning gap (square R=10 minus {{7,3}} L=3, log-parametrised kappa, median of 5 seeds) "
                           f"under conductances {regime}.",
                "prediction": {"gap_N316": pred, "refuted_if": refute},
                "outcome": {"gap_N316": None if gap is None else round(gap, 2),
                            "hyp_L3": round(s[regime]["{7,3} L=3"], 2), "square_R10": round(s[regime]["square R=10"], 2)},
                "verdict": "confirmed" if ok else "refuted", "energy": 0.0 if ok else 1.0,
            })
        unit = s["unit"]["{7,3} L=3"]
        change = max(abs(s["defect x100"]["{7,3} L=3"] - unit), abs(s["defect x0.01"]["{7,3} L=3"] - unit))
        recs.append({
            "id": "P3-B-defect", "source": ["PREREGISTRATION_3.md", "data/disorder.json"],
            "context": "x100 and x0.01 contrast on every edge of one interior node at maximal depth, {7,3} L=3.",
            "prediction": {"hyperbolic_log10_kappa_change": "< 2 decades", "refuted_if": "> 3"},
            "outcome": {"max_change_decades": round(change, 2)},
            "verdict": "confirmed" if change < 2 else "refuted", "energy": round(min(1.0, change / 3), 3),
        })
    mp = D / "flat_scaling_mp.json"
    if mp.exists():
        pred = json.loads((D / "prereg3_predictions.json").read_text())
        for r in json.loads(mp.read_text()):
            if r["control_pass"] is not None:
                continue
            fam = "square" if r["case"].startswith("square") else "triangular"
            p = pred[fam]["predictions"][str(r["N"])]
            k = r["log10_kappa_arb"]
            recs.append({
                "id": f"P3-A-{fam}-{r['N']}", "source": ["PREREGISTRATION_3.md", "data/flat_scaling_mp.json"],
                "context": f"{r['case']}: log10 kappa in 512-bit ball arithmetic (float64-singular instance).",
                "prediction": {"exp_sqrtN": p["exp_sqrtN"], "power_law": p["power_last_exponent"],
                               "favoured": "exp_sqrtN", "window_decades": 2.0},
                "outcome": {"log10_kappa_arb": round(k, 3), "max_rel_radius": r["max_rel_radius_Ginv"]},
                "verdict": "confirmed" if abs(k - p["exp_sqrtN"]) <= 2.0 else "refuted",
                "energy": round(min(1.0, abs(k - p["exp_sqrtN"]) / 2.0), 3),
            })
    # ---- PREREGISTRATION_5 (bulk defect vs boundary persistent homology) ----
    tda = D / "tda_defect.json"
    if tda.exists():
        res = {r["lattice"]: r for r in json.loads(tda.read_text())["results"]}
        def det(l, c, m): return res[l]["configs"][c]["detected"][m]
        deep_topo = any(det(l, c, m) for l in res for c in ("deep x100", "deep x0.01") for m in ("bottleneck_H0", "bottleneck_H1"))
        recs.append({"id": "P5-P1-deep-topological", "source": ["PREREGISTRATION_5.md", "data/tda_defect.json"],
                     "context": "Deep bulk defect; H0/H1 bottleneck distance of boundary resistance-metric Rips diagrams vs unit; "
                                "null = U[0.5,1.5] disorder p95.",
                     "prediction": {"detected": False}, "outcome": {"detected_any_lattice": deep_topo},
                     "verdict": "confirmed" if not deep_topo else "refuted", "energy": 1.0 if deep_topo else 0.0})
        hyp = any(det(l, c, "rel_metric_change") for l in ("{7,3} L=3", "{7,3} L=2") for c in ("deep x100", "deep x0.01"))
        sq = any(det(l, c, "rel_metric_change") for l in ("square R=10", "square R=6") for c in ("deep x100", "deep x0.01"))
        ok = hyp and not sq
        recs.append({"id": "P5-P2-deep-metric", "source": ["PREREGISTRATION_5.md", "data/tda_defect.json"],
                     "context": "Deep bulk defect; direct detector ||dR||/||R|| vs disorder null p95.",
                     "prediction": {"hyperbolic_detected": True, "square_detected": False},
                     "outcome": {"hyperbolic_detected": hyp, "square_detected": sq,
                                 "hyp_over_square_signal_ratio_N316": round(res["{7,3} L=3"]["configs"]["deep x100"]["rel_metric_change"]
                                                                            / res["square R=10"]["configs"]["deep x100"]["rel_metric_change"], 1)},
                     "verdict": "confirmed" if ok else "refuted", "energy": 0.0 if ok else 1.0,
                     "note": "Null amplitude (global 50% disorder) exceeded the single-node effect; threshold not matched to effect size."})
        sh_topo = any(det(l, "shallow x100", m) or det(l, "shallow x0.01", m) for l in res for m in ("bottleneck_H0", "bottleneck_H1"))
        sh_metric_all = all(det(l, "shallow x100", "rel_metric_change") or det(l, "shallow x0.01", "rel_metric_change") for l in res)
        recs.append({"id": "P5-P3-shallow-control", "source": ["PREREGISTRATION_5.md", "data/tda_defect.json"],
                     "context": "Shallow (depth-1) defect as positive control.",
                     "prediction": {"metric_detected_all_lattices": True, "topological_detected_somewhere": True},
                     "outcome": {"metric_detected_all_lattices": sh_metric_all, "topological_detected_somewhere": sh_topo,
                                 "H1_detects_on": [l for l in res if det(l, "shallow x100", "bottleneck_H1")]},
                     "verdict": "confirmed" if (sh_metric_all and sh_topo) else "partial",
                     "energy": 0.0 if (sh_metric_all and sh_topo) else 0.5})
    # ---- PREREGISTRATION_6 (defect detection vs measurement noise) ----
    tn = D / "tda_noise.json"
    if tn.exists():
        d = json.loads(tn.read_text()); res = {r["lattice"]: r for r in d["results"]}
        em = lambda l, k: res[l]["configs"]["deep x100"]["eps_max"][k]
        q1 = em("{7,3} L=3", "metric") >= 3 * em("square R=10", "metric") > 0
        q2 = all(em(l, "H1") <= em(l, "metric") / 3 for l in ("{7,3} L=2", "{7,3} L=3"))
        i3 = d["eps"].index(3e-4)
        q3 = all(res[l]["configs"]["deep x100"]["detected"]["metric"][i3] for l in res)
        for pid, ok, ctx, pred, out in (
            ("P6-Q1-geometry", q1, "Deep x100 defect, metric detector: noise level up to which it stays detected, N~316.",
             {"eps_max_ratio_hyperbolic_over_square": ">= 3"},
             {"hyperbolic": em("{7,3} L=3", "metric"), "square": em("square R=10", "metric"), "censored_at_grid_ceiling": True}),
            ("P6-Q2-topology-less-sensitive", q2, "Deep x100 defect: H1 bottleneck eps_max vs metric eps_max, hyperbolic lattices.",
             {"eps_max_H1_over_metric": "<= 1/3"},
             {"L2": [em("{7,3} L=2", "H1"), em("{7,3} L=2", "metric")], "L3": [em("{7,3} L=3", "H1"), em("{7,3} L=3", "metric")]}),
            ("P6-Q3-hardware-budget", q3, "Deep x100 defect detected by the metric at noise 3e-4 (the paper's precision budget) on all four lattices.",
             {"detected_all": True}, {"detected_all": q3}),
        ):
            recs.append({"id": pid, "source": ["PREREGISTRATION_6.md", "data/tda_noise.json"], "context": ctx,
                         "prediction": pred, "outcome": out,
                         "verdict": "confirmed" if ok else "refuted", "energy": 0.0 if ok else 1.0,
                         "note": "Baseline assumed known and noiseless; detection of change only, not localisation."})
    return recs


def main():
    OUT.mkdir(exist_ok=True)
    preds = predictions()
    (OUT / "physics_predictions.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in preds))
    ledger = json.loads((ROOT / "docs" / "elenchus" / "ledger.json").read_text())["claims"]
    rows = [{"id": c["id"], "tier": c["tier"], "kind": c["kind"], "statement": c["statement"],
             "depends_on": c["depends_on"], "verdict": verdict_of(c["statement"], c.get("notes", "")),
             "evidence": c["evidence"], "notes": c.get("notes")} for c in ledger]
    (OUT / "ledger_claims.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    for r in preds:
        print(f"  {r['id']:14} {r['verdict']:10} energy={r['energy']}")
    print(f"wrote {len(preds)} predictions, {len(rows)} ledger claims to {OUT}")


if __name__ == "__main__":
    main()
