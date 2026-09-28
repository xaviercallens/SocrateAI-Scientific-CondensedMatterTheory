#!/usr/bin/env python3
"""Ledger entry for PREREGISTRATION_10 (localisation with component tolerance). Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "localize_tolerance.json").read_bytes()
    res = {r["lattice"]: r["cells"] for r in json.loads(raw)["results"]}
    top = lambda l, tau, eps, f: res[l]["tau{} eps{} x{}".format(tau, eps, f)]["top1"]
    T1 = all(top(l, "0.001", "0.0003", "2") >= 0.9 for l in res)
    T2 = top("square R=10", "0.05", "0.0003", "2") < 0.9 and top("{7,3} L=3", "0.05", "0.0003", "2") >= 0.9
    cells = [(tau, eps, f) for tau in ("0.01", "0.05") for eps in ("0.0003", "0.003") for f in ("1.25", "2")]
    diffs = [top("{7,3} L=3", *c) - top("square R=10", *c) for c in cells]
    T3 = all(d >= -0.1 for d in diffs) and any(d >= 0.3 for d in diffs)
    r10 = "R10 x1.25 at eps 3e-3: tau 0.1%/1%/5% = {}/{}/{}".format(
        top("square R=10", "0.001", "0.003", "1.25"), top("square R=10", "0.01", "0.003", "1.25"),
        top("square R=10", "0.05", "0.003", "1.25"))
    n_perfect = sum(1 for l in res for c in res[l].values() if c["top1"] == 1.0)
    c = {
        "id": "H3-X-0007", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0006"],
        "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
        "statement": (
            "PREREGISTRATION_10 (single-node localisation on random boards g=1+tau*U[-1,1], ideal-model dictionary, "
            "differential regime, deepest class, 20 trials per cell, 4 lattices x tau in (0.1, 1, 5)% x eps in (3e-4, 3e-3) x "
            "contrast in (1.25, 2) = 48 cells). T1 HELD ({}): tau=0.1%, eps=3e-4, x2 localises perfectly on all four lattices. "
            "T2 REFUTED ({}): square R=10 at tau=5%, eps=3e-4, x2 stays at top-1 1.00 (predicted < 0.9). T3 HELD ({}): the "
            "hyperbolic lattice is never noticeably worse and leads by up to {:.2f} (R10 x1.25, eps 3e-3). {}/48 cells "
            "are exactly 1.00; the only cells below 0.9 are square R=10 x1.25 at eps=3e-3 ({}), the same value as on an ideal "
            "board within sampling error (0.50, H3-X-0006). Component tolerance up to 5% does not degrade "
            "localisation; the failures are noise-limited."
        ).format(T1, T2, T3, max(diffs), n_perfect, r10),
        "notes": ("experiments/track_h_hyperbolic_network/localize_tolerance.py. LIMITS: tolerance up to 5% only (larger "
                  "untested); noise 3e-4 and 3e-3 only; 20 trials (standard error ~0.11 near 0.5); single node on the square "
                  "lattices' deepest class; oracle dictionary (known contrast set), single-node model, i.i.d. noise. Probable "
                  "reason for the null effect, NOT tested: tolerance is common to the two maps of one board, so it cancels to "
                  "first order in their difference; the model-based detection regime (H3-X-0003, B3) does not have this property."),
    }
    led = json.loads(LEDGER.read_text())
    if c["id"] not in {x["id"] for x in led["claims"]}:
        led["claims"].append(c); print("added", c["id"], "| T1 T2 T3:", T1, T2, T3, "| max lead", max(diffs), "|", r10)
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
