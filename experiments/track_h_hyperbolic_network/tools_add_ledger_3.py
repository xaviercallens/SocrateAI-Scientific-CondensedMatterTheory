#!/usr/bin/env python3
"""One-shot: record the domain-monotonicity bound for H2 in the ledger.

Appends a correction to H2-X-0002's notes (statement unchanged) and adds the
exact degree check (B), the cited spectral-gap facts (L), and the argument
combining them (C). Idempotent.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"
CORR = (" CORRECTION (appended, statement unchanged): '~1/log N' is NOT an open alternative. "
        "Every interior node of every tested truncation has full degree 3 (H2-B-0001), so lambda_min(L_ii) "
        ">= lambda_0({7,3}) > 0 by domain monotonicity (H2-C-0001); the sequence decreases toward lambda_0.")


def h(name):
    return "sha256:" + hashlib.sha256((DATA / name).read_bytes()).hexdigest()


NEW = [
    {"id": "H2-B-0001", "tier": "B", "kind": "exact_harness", "depends_on": [],
     "evidence": h("interior_degree.json"),
     "statement": "For the {7,3} truncations L=1..6 (N=35..5887), every interior node (not on the outer face) "
                  "has degree exactly 3, and the interior node count at layer L equals N at layer L-1 "
                  "(7, 35, 112, 315, 847, 2240).",
     "notes": "experiments/track_h_hyperbolic_network/interior_degree.py; integer degree counts, no floating point."},
    {"id": "H2-L-0001", "tier": "L", "kind": "citation", "depends_on": [],
     "evidence": "sha256:" + hashlib.sha256(b"Dodziuk1984;Mohar1988;HaggstromJonassonLyons2002").hexdigest(),
     "statement": "The bottom of the spectrum lambda_0 of the combinatorial Laplacian of an infinite graph of bounded "
                  "degree is positive iff its edge-isoperimetric (Cheeger) constant is positive "
                  "[Dodziuk, Trans. AMS 284 (1984) 787-794; Mohar, Linear Algebra Appl. 103 (1988) 119-131]; the "
                  "{7,3} tiling graph has an explicit positive isoperimetric constant [Haggstrom, Jonasson & Lyons, "
                  "Ann. Probab. 30 (2002) 443-473].",
     "notes": "Cited, not re-derived. Upper bound lambda_0 <= 3 - 2 sqrt 2 follows from the 3-regular tree covering."},
    {"id": "H2-C-0001", "tier": "C", "kind": "argument", "depends_on": ["H2-B-0001", "H2-L-0001"],
     "statement": "For every tested {7,3} truncation, lambda_min(L_ii) is the Rayleigh-quotient minimum of the infinite "
                  "{7,3} Laplacian over functions supported on the interior (by H2-B-0001), hence lambda_min(L_ii) >= "
                  "lambda_0 > 0 and the RC relaxation time tau = C/lambda_min(L_ii) <= C/lambda_0 uniformly; since the "
                  "interiors are nested and exhaust the tiling, lambda_min(L_ii) is non-increasing in L and converges "
                  "to lambda_0. Flat disks have lambda_min -> 0.",
     "evidence": "sha256:" + hashlib.sha256(b"domain-monotonicity argument, paper sec. H2").hexdigest(),
     "notes": "The degree premise is checked only for L<=6; for general L it follows from the face-incidence "
              "boundary definition but that step is argued, not certified. Does NOT rescue the refuted "
              "finite-size prediction H2-X-0001."},
]


def main():
    d = json.loads(LEDGER.read_text())
    have = {c["id"] for c in d["claims"]}
    for c in d["claims"]:
        if c["id"] == "H2-X-0002" and "CORRECTION" not in (c.get("notes") or ""):
            c["notes"] = (c.get("notes") or "") + CORR
            print("corrected notes of H2-X-0002")
    for c in NEW:
        c.setdefault("audit", None)
        if c["id"] not in have:
            d["claims"].append(c)
            print("added", c["id"])
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
