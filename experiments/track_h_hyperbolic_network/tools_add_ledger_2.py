#!/usr/bin/env python3
"""One-shot: append the PREREGISTRATION_2 claims to docs/elenchus/ledger.json.

Evidence hashes are sha256 of the data files the claims are read from.
Idempotent: claims whose id already exists are skipped.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def h(name):
    return "sha256:" + hashlib.sha256((DATA / name).read_bytes()).hexdigest()


NEW = [
    {"id": "H0-B-0002", "tier": "B", "kind": "exact_harness", "depends_on": ["H0-B-0001"],
     "evidence": h("identifiability.json"),
     "statement": "In the probe-matched control (PREREGISTRATION_2 part A), making unused {7,3} boundary nodes "
                  "zero-current interior nodes creates structural non-identifiability: the exact GF(p) rank "
                  "deficiency (two primes, agreeing) equals the number of unmeasured degree-2 nodes "
                  "(L=2, 44 probes: 23 = 23; L=3, 76 probes: 93 = 93). Full-boundary square disks R=6, R=10 are "
                  "exactly full rank.",
     "notes": "experiments/track_h_hyperbolic_network/identifiability.py. The series-resistor mechanism "
              "(g1 g2/(g1+g2) is the only observable) explains the count; the equality is certified only at these two sizes."},
    {"id": "H0-X-0003", "tier": "X", "kind": "numeric", "depends_on": ["H0-B-0002"],
     "evidence": h("identifiability.json"),
     "statement": "DEVIATION FROM PREREGISTRATION_2 part A: the preregistered probe-matched kappa is SINGULAR by "
                  "design (H0-B-0002), so the prediction as written is untestable. Corrected comparison, "
                  "chosen after seeing the singularity: kappa restricted to the identifiable subspace "
                  "(dropping exactly the certified deficiency). log10 kappa: {7,3} L=2/44 probes 2.70 vs square "
                  "R=6 5.07; {7,3} L=3/76 probes 2.97 vs square R=10 9.72 (gap 6.75 decades). The advantage "
                  "survives probe matching at these two sizes.",
     "notes": "float64 SVD; post hoc metric; must be reported as a deviation everywhere it is cited."},
    {"id": "H0-X-0004", "tier": "X", "kind": "numeric", "depends_on": [],
     "evidence": h("probe_matched.json"),
     "statement": "PREREGISTRATION_2 part B (confirmed as predicted): for the Neumann-to-Dirichlet map "
                  "(Moore-Penrose inverse of the DtN map, what current-injection hardware measures), the "
                  "conditioning ordering is preserved at full boundary: log10 kappa {7,3} L=2 1.99, L=3 2.42 "
                  "vs square R=6 5.41, R=10 10.08.",
     "notes": "experiments/track_h_hyperbolic_network/probe_matched.py; float64, two sizes."},
    {"id": "H2-X-0001", "tier": "X", "kind": "numeric", "depends_on": [],
     "evidence": h("rc_network.json"),
     "statement": "PREREGISTRATION_2 part C, H2 prediction (i) REFUTED at the tested sizes: lambda_min(L_ii) of "
                  "the {7,3} tiling fell 2.37x between L=2 and L=4, past the preregistered 2x refutation "
                  "threshold. Prediction (ii) holds: flat square/triangular lambda_min scales as ~1/N.",
     "notes": "experiments/track_h_hyperbolic_network/rc_network.py (dense eigvalsh)."},
    {"id": "H2-X-0002", "tier": "X", "kind": "numeric", "depends_on": ["H2-X-0001"],
     "evidence": h("h2_explore.json"),
     "statement": "EXPLORATORY, post hoc (cannot rescue H2-X-0001): {7,3} lambda_min at L=2..6 = 0.3636, 0.2133, "
                  "0.1534, 0.1232, 0.1058; successive ratios 0.587, 0.719, 0.803, 0.859 -- the decrease is "
                  "slowing, consistent with a positive limit or ~1/log N, and far slower than 1/N. At N~800: "
                  "tau 6.52 vs 39.06 (flat), stiffness 36 vs 311.",
     "notes": "experiments/track_h_hyperbolic_network/h2_explore.py (sparse eigsh). Five points cannot discriminate "
              "a positive limit from 1/log N."},
    {"id": "H2-X-0003", "tier": "X", "kind": "numeric", "depends_on": [],
     "evidence": h("rc_network.json"),
     "statement": "RC integrator controls: K1 (expm known answer, max rel err < 1e-5) and K2 (integrated steady "
                  "state equals the Schur-complement DtN column, < 1e-6) PASS with scipy BDF on {7,3} L=2 and "
                  "square R=6. The rusty-SUNDIALS CVODE backend is NOT RUN (Python extension not built); no "
                  "cross-code agreement is claimed.",
     "notes": "Re-run rc_network.py after `maturin develop` in ~/rusty-SUNDIALS/crates/rusty-sundials-py."},
]


def main():
    d = json.loads(LEDGER.read_text())
    have = {c["id"] for c in d["claims"]}
    for c in NEW:
        c.setdefault("audit", None)
        if c["id"] not in have:
            d["claims"].append(c)
            print("added", c["id"])
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
