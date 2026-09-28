#!/usr/bin/env python3
"""Ledger entry for PREREGISTRATION_7 (defect detection vs component tolerance). Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "tolerance_null.json").read_bytes()
    res = {r["lattice"]: r["tau"] for r in json.loads(raw)["results"]}
    B = lambda l, t: res[l][t]["B_detected"]
    A = lambda l, t: res[l][t]["A_detected"]
    b1 = all(B(l, "0.001") for l in res)
    b2 = all(B(l, "0.01") for l in res)
    b3 = B("{7,3} L=2", "0.05") and B("{7,3} L=3", "0.05") and not B("square R=10", "0.05")
    a1 = all(A(l, t) for l in res for t in res[l])
    r10 = res["square R=10"]["0.05"]
    c = {
        "id": "H3-X-0003", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0002"],
        "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
        "statement": (
            "PREREGISTRATION_7 (deep x100 defect vs component tolerance g=1+tau*U[-1,1], 20 boards per condition, "
            "detected iff min defect statistic > max null statistic). Model-based regime (compare with the ideal "
            f"simulation): B1 tau=0.1% all four lattices detect ({b1}); B2 tau=1% all four detect ({b2}); B3 tau=5%: "
            "{7,3} L=2 and L=3 detect (margins 6.2x and 5.3x), square R=10 does not (defect min "
            f"{r10['B_defect_min']:.1e} < null max {r10['B_null_max']:.1e}) ({b3}). Differential regime (board vs its own "
            f"3e-4-noise baseline): A1 detected on all four lattices at every tau ({a1}); worst margin 40x (square R=10, "
            "tau=1%). Quantitative miss: the linear-response scaling of the prereg-5 null overestimated the 5% null "
            "by ~1.7x (predicted p95 ~1.1e-2; observed max 6.5-7.8e-3), so square R=6, left unpredicted, detects."),
        "notes": ("experiments/track_h_hyperbolic_network/tolerance_null.py. LIMIT: only extreme contrasts are tested "
                  "(x100 on all edges of one node: a near short circuit). Signal is roughly linear in the conductance "
                  "change, so a x2 defect would be ~100x weaker, near or below the tolerance/noise floor on the deep "
                  "nodes of these lattices; the minimum detectable contrast is untested and is the next preregistration."),
    }
    led = json.loads(LEDGER.read_text())
    if c["id"] not in {x["id"] for x in led["claims"]}:
        led["claims"].append(c); print("added", c["id"], "| b1 b2 b3 a1:", b1, b2, b3, a1)
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
