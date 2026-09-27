#!/usr/bin/env python3
"""Diagnose the SINGULAR result of the preregistered probe-matched control
(PREREGISTRATION_2.md, part A), and compute the corrected comparison.

Hypothesis for the singularity (stated before this script was run): turning
unused boundary nodes into zero-current interior nodes creates interior
nodes of degree 2. Two conductances in series through an unmeasured
degree-2 node enter the boundary data only through their series
combination g1*g2/(g1+g2), so each such node contributes exactly one
direction to the Jacobian's null space -- a STRUCTURAL non-identifiability
created by the control's design, not a conditioning effect. Prediction:
exact rank deficiency == number of unmeasured degree-2 nodes.

If that holds, the fair comparison is the condition number restricted to
the identifiable subspace: drop exactly `deficiency` singular values, where
`deficiency` comes from the EXACT modular-arithmetic rank (a certificate),
never from a floating-point tolerance.

Outputs: data/identifiability.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import build_hyperbolic, build_square_disk, boundary_nodes, degrees  # noqa: E402
from hyperbolic_exact import PRIMES, jacobian_mod, rank_mod  # noqa: E402
from probe_matched import jacobian_matrices, subsample_by_angle  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "identifiability.json"


def restricted_kappa(n, edges, probes, deficiency):
    mats = jacobian_matrices(n, edges, probes)
    m = mats[0].shape[0]
    iu = np.triu_indices(m, k=1)
    J = np.stack([M[iu] for M in mats], axis=1)
    s = np.linalg.svd(J, compute_uv=False)  # descending
    kept = s[: len(edges) - deficiency]
    return math.log10(kept[0] / kept[-1]), float(kept[-1] / kept[0])


def main() -> int:
    rows = []
    cases = [
        ("{7,3} L=2, 44 probes", build_hyperbolic(7, 3, 2), 44),
        ("{7,3} L=3, 76 probes", build_hyperbolic(7, 3, 3), 76),
        ("square R=6, all 44 probes", build_square_disk(6), None),
        ("square R=10, all 76 probes", build_square_disk(10), None),
    ]
    for name, g, k in cases:
        n, E = len(g["nodes"]), len(g["edges"])
        bnd = boundary_nodes(g)
        probes = subsample_by_angle(g, bnd, k) if k else bnd
        interior = np.setdiff1d(np.arange(n), probes)
        d2 = int(np.sum(degrees(n, g["edges"])[interior] == 2))
        ranks = {p: rank_mod(jacobian_mod(n, g["edges"], probes, p), p) for p in PRIMES}
        agree = len(set(ranks.values())) == 1
        rank = list(ranks.values())[0]
        deficiency = E - rank
        lk, _ = restricted_kappa(n, g["edges"], probes, deficiency) if agree else (None, None)
        row = {"name": name, "N": n, "E": E, "probes": int(len(probes)),
               "exact_ranks": {str(p): r for p, r in ranks.items()}, "primes_agree": agree,
               "deficiency": deficiency, "unmeasured_degree2_nodes": d2,
               "deficiency_equals_degree2": deficiency == d2,
               "log10_kappa_identifiable": lk}
        rows.append(row)
        print(f"  {name:28} N={n:4d} E={E:4d} rank={rank} (primes agree={agree}) "
              f"deficiency={deficiency} deg2={d2} -> log10k(identifiable)={lk:.2f}")
    OUT.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
