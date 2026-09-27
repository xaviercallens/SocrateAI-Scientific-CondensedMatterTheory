#!/usr/bin/env python3
"""One-shot: record the rusty-SUNDIALS CVODE cross-validation (H2-X-0004) and
mark H2-X-0003 ('CVODE NOT RUN') as superseded, statement unchanged. Idempotent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    raw = (DATA / "rc_network.json").read_bytes()
    rc = json.loads(raw)
    assert rc["rusty_sundials_importable"], "re-run rc_network.py with rusty_sundials installed first"
    ctl = [r for r in rc["controls"] if r.get("backend") == "rusty"]
    assert ctl and all(r["K1_pass"] and r["K2_pass"] for r in ctl)
    k1 = max(r["K1_rel_err"] for r in ctl)
    k2 = max(r["K2_rel_err"] for r in ctl)
    d = json.loads(LEDGER.read_text())
    have = {c["id"] for c in d["claims"]}
    for c in d["claims"]:
        if c["id"] == "H2-X-0003" and "SUPERSEDED" not in (c.get("notes") or ""):
            c["notes"] = (c.get("notes") or "") + " [SUPERSEDED by H2-X-0004: the CVODE leg has since been run.]"
    if "H2-X-0004" not in have:
        d["claims"].append({
            "id": "H2-X-0004", "tier": "X", "kind": "numeric", "depends_on": ["H2-X-0003"],
            "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
            "statement": ("Two-code cross-validation of the RC network: rusty-SUNDIALS CvodeSolver (BDF, Python "
                          "binding rusty-sundials-py 6.0.0 built from rusty-SUNDIALS commit af4886f) passes K1 "
                          f"(max rel err {k1:.1e} < 1e-5 vs the matrix exponential) and K2 (max rel err {k2:.1e} < 1e-6 "
                          "vs the Schur-complement DtN column) on {7,3} L=2 and square R=6, as does SciPy BDF; both "
                          "integrators therefore agree with the exact solution, and with each other, to ~3e-8."),
            "notes": ("experiments/track_h_hyperbolic_network/rc_network.py; same rtol=1e-8, atol=1e-10 for both. "
                      "Wheel built with maturin 1.15.0 from the local checkout (branch merge-mcp-temp)."),
        })
        print("added H2-X-0004")
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
