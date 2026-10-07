#!/usr/bin/env python3
"""Ledger entry for PREREGISTRATION_6 (defect detection vs measurement noise). Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "tda_noise.json").read_bytes()
    d = json.loads(raw)
    res = {r["lattice"]: r for r in d["results"]}
    em = lambda lat, cfg, k: res[lat]["configs"][cfg]["eps_max"][k]
    at3e4 = all(res[l]["configs"]["deep x100"]["detected"]["metric"][d["eps"].index(3e-4)] for l in res)
    c = {
        "id": "H3-X-0002", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0001"],
        "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
        "statement": (
            "PREREGISTRATION_6 (defect detection against Gaussian measurement noise on the Neumann-to-Dirichlet map, "
            "10 realisations, detection = all defect realisations exceed the max of the noise null; eps grid "
            "1e-4..1e-1). Q1 HELD: deep x100 defect, metric detector, N~316: eps_max = "
            f"{em('{7,3} L=3', 'deep x100', 'metric'):.0e} (hyperbolic; top of the grid, so a lower bound) vs "
            f"{em('square R=10', 'deep x100', 'metric'):.0e} (square), ratio >= 10 (predicted >= 3); at N~112: "
            f"{em('{7,3} L=2', 'deep x100', 'metric'):.0e} vs {em('square R=6', 'deep x100', 'metric'):.0e}. Q2 HELD: "
            f"H1 bottleneck eps_max = {em('{7,3} L=2', 'deep x100', 'H1'):.0e} / {em('{7,3} L=3', 'deep x100', 'H1'):.0e} on the "
            "hyperbolic lattices, at least 3.3x below the metric's, i.e. topology is less sensitive than the plain "
            f"metric. Q3 HELD: the metric detects the deep x100 defect at eps = 3e-4 on all four lattices ({at3e4})."),
        "notes": ("experiments/track_h_hyperbolic_network/tda_noise.py. LIMITS: detection is against a KNOWN noiseless "
                  "baseline and tests only that something changed, not where or what; the hyperbolic metric eps_max is "
                  "censored at the grid ceiling; 10 realisations is crude; noise is i.i.d. Gaussian on P, not "
                  "correlated hardware error; component tolerance acts as fixed baseline disorder, which this null "
                  "does not include (next preregistration: tolerance-matched null)."),
    }
    led = json.loads(LEDGER.read_text())
    if c["id"] not in {x["id"] for x in led["claims"]}:
        led["claims"].append(c); print("added", c["id"])
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
