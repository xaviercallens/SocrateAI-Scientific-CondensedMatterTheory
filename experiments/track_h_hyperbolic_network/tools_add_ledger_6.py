#!/usr/bin/env python3
"""Ledger entry for PREREGISTRATION_5 (bulk defect vs boundary persistent homology). Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "tda_defect.json").read_bytes()
    res = {r["lattice"]: r for r in json.loads(raw)["results"]}
    def det(lat, cfg, m): return res[lat]["configs"][cfg]["detected"][m]
    deep_any = any(det(l, c, m) for l in res for c in ("deep x100", "deep x0.01")
                   for m in ("bottleneck_H0", "bottleneck_H1"))
    metric_hyp = any(det(l, c, "rel_metric_change") for l in ("{7,3} L=3", "{7,3} L=2") for c in ("deep x100", "deep x0.01"))
    metric_sq = any(det(l, c, "rel_metric_change") for l in ("square R=10", "square R=6") for c in ("deep x100", "deep x0.01"))
    h3 = res["{7,3} L=3"]["configs"]; s10 = res["square R=10"]["configs"]
    c = {
        "id": "H3-X-0001", "tier": "X", "kind": "numeric", "depends_on": [],
        "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
        "statement": (
            "PREREGISTRATION_5 (boundary effective-resistance metric -> Vietoris-Rips H0/H1, Gudhi 3.13; null = "
            "U[0.5,1.5] disorder, 20 seeds, 95th percentile). P1 HELD: a deep defect (x100 / x0.01 on every edge of "
            f"a maximal-depth node) gives no H0/H1 bottleneck signature above the null on any of 4 lattices "
            f"(deep_detected_topologically={deep_any}). P2 REFUTED: the direct metric change ||dR||/||R|| does not "
            f"detect the deep defect on the hyperbolic lattices either (hyperbolic={metric_hyp}, square={metric_sq}); "
            f"the hyperbolic signal is larger ({h3['deep x100']['rel_metric_change']:.3f} vs {s10['deep x100']['rel_metric_change']:.3f} "
            "at N~316) but below the null. P3 PARTIAL: the shallow x100 defect is detected by H1 on both hyperbolic "
            f"lattices ({h3['shallow x100']['bottleneck_H1']:.3f} > {res['{7,3} L=3']['null_p95']['bottleneck_H1']:.3f}; "
            f"L=2: {res['{7,3} L=2']['configs']['shallow x100']['bottleneck_H1']:.3f}) and on neither square lattice; "
            "the direct metric detects it nowhere. The 'bulk defect = boundary topological invariant' hypothesis "
            "fails for deep defects at these sizes."),
        "notes": ("experiments/track_h_hyperbolic_network/tda_defect.py; unit DtN matrices taken from the published "
                  "v1.1 dataset (asserted equal to recomputed). Design caveat, recorded for the follow-up: the null "
                  "(global 50% disorder) is a much larger perturbation than one node's edges, so P2's threshold was "
                  "not matched to the effect size; a null with matched perturbation energy is the next preregistration."),
    }
    d = json.loads(LEDGER.read_text())
    if c["id"] not in {x["id"] for x in d["claims"]}:
        d["claims"].append(c); print("added", c["id"])
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
