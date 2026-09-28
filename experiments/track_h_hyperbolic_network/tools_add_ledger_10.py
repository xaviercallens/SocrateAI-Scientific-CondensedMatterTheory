#!/usr/bin/env python3
"""Ledger entry for PREREGISTRATION_8 (localisation of a single-node defect). Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "localize_defect.json").read_bytes()
    res = {r["lattice"]: r["cells"] for r in json.loads(raw)["results"]}
    top = lambda l, k: res[l][k]["top1"]
    cells = [c for l in res for c in res[l].values()]
    all_perfect = all(c["top1"] == 1.0 and c["contrast_acc"] == 1.0 for c in cells)
    L1 = all(top(l, f"{d} x{f}") >= 0.9 for l in res for d in ("depth1", "mid") for f in ("10", "100"))
    L2 = top("{7,3} L=3", "max x2") >= 0.8 and top("square R=10", "max x2") <= 0.5
    L3 = (top("square R=10", "max x0.8") <= 0.2 and top("square R=10", "max x1.25") <= 0.2
          and top("{7,3} L=3", "max x0.8") >= 0.5 and top("{7,3} L=3", "max x1.25") >= 0.5)
    c = {
        "id": "H3-X-0005", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0004"],
        "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
        "statement": (
            "PREREGISTRATION_8 (single-node defect localisation from the difference of two NtD maps, i.i.d. noise 3e-4 on each, "
            "dictionary matched filter over all interior nodes x contrasts {0.1,0.5,0.8,1.25,2,5,10,100}, 20 trials per cell, "
            "4 lattices x 3 depth classes x 5 true contrasts {0.8,1.25,2,10,100} = 60 cells). Result: top-1 node accuracy and "
            f"contrast accuracy are 1.00 in every cell ({all_perfect}); mean hop error 0. L1 HELD ({L1}). L2 REFUTED ({L2}): "
            f"square R=10 at maximal depth and x2 localises perfectly (predicted <= 0.5). L3 REFUTED ({L3}): square R=10 at x0.8 "
            "and x1.25, maximal depth, localises perfectly (predicted <= 0.2). The hyperbolic lattice's larger boundary signal "
            "(H3-X-0004) gives NO localisation advantage at this noise level and these sizes with an oracle-dictionary decoder."),
        "notes": ("experiments/track_h_hyperbolic_network/localize_defect.py. LIMITS: ideal board only (no tolerance); known "
                  "single-node model and a known finite contrast set (oracle dictionary); i.i.d. Gaussian noise; the maximal-depth "
                  "class has one node on square R=6/R=10 (20 noise draws of one location); no ceiling/floor separation is possible "
                  "from a 60/60 result. Hypothesis, NOT tested: the matched filter combines all m^2 correlated matrix entries, "
                  "giving a processing gain of order m over the single norm statistic used for detection (H3-X-0002), so "
                  "localisation is limited only at much larger noise; the failure boundary needs a noise sweep."),
    }
    led = json.loads(LEDGER.read_text())
    if c["id"] not in {x["id"] for x in led["claims"]}:
        led["claims"].append(c); print("added", c["id"], "| L1 L2 L3 held:", L1, L2, L3, "| all 60 perfect:", all_perfect)
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
