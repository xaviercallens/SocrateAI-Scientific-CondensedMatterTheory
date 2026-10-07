#!/usr/bin/env python3
"""(1) Append a CORRECTION to H3-X-0003's notes: its 'x2 would be ~100x weaker' remark was an unchecked linear
extrapolation and is wrong (the signal saturates). (2) Record the exploratory signal-vs-contrast curve as H3-X-0004.
Statements are never edited. Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "contrast_signal.json").read_bytes()
    res = {r["lattice"]: r["depths"]["max"]["signal"] for r in json.loads(raw)["results"]}
    led = json.loads(LEDGER.read_text())
    for c in led["claims"]:
        if c["id"] == "H3-X-0003" and "CORRECTION (2026-09-28" not in (c.get("notes") or ""):
            c["notes"] = (c.get("notes") or "") + (
                " CORRECTION (2026-09-28, appended; statement unchanged): the LIMIT sentence above claimed a x2 defect would be "
                "'~100x weaker' by linear scaling. That was an unchecked extrapolation and is WRONG: the signal saturates "
                "(H3-X-0004). At the deepest node the x2 signal is 37% ({7,3} L=3) and 27% (square R=10) of the x100 signal, "
                "and even x1.25 / x0.8 lie above the 3e-4 differential noise floor. The minimum detectable contrast is "
                "therefore far smaller than stated here.")
            print("corrected notes of H3-X-0003")
    if "H3-X-0004" not in {c["id"] for c in led["claims"]}:
        s3, s10 = res["{7,3} L=3"], res["square R=10"]
        led["claims"].append({
            "id": "H3-X-0004", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0003"],
            "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
            "statement": (
                "EXPLORATORY (not preregistered; computed to check a claim in H3-X-0003): noiseless relative change of the "
                "boundary resistance metric for a single-node conductance defect (all edges of the node scaled by f), deepest "
                f"node. {{7,3}} L=3: f=0.8: {s3['0.8']:.1e}, 1.25: {s3['1.25']:.1e}, 2: {s3['2.0']:.1e}, 10: {s3['10.0']:.1e}, "
                f"100: {s3['100.0']:.1e}. Square R=10: 0.8: {s10['0.8']:.1e}, 1.25: {s10['1.25']:.1e}, 2: {s10['2.0']:.1e}, "
                f"10: {s10['10.0']:.1e}, 100: {s10['100.0']:.1e}. The response saturates for f >> 1 (x2 is 37% / 27% of x100), "
                "is roughly antisymmetric in log f near f = 1 (x0.8 and x1.25 are within 5% of each other), and is a factor "
                "~7.5-10 larger on the hyperbolic lattice at the deepest node."),
            "notes": "experiments/track_h_hyperbolic_network/contrast_signal.py; four lattices, depths max and 1 in the data file."})
        print("added H3-X-0004")
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
