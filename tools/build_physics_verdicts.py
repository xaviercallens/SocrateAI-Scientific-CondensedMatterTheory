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
