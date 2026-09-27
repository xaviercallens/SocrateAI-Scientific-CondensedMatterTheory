#!/usr/bin/env python3
"""Premise check for the domain-monotonicity bound on H2.

If every interior node of a {7,3} truncation has its full degree 3, then
L_ii is the restriction of the infinite {7,3} graph Laplacian to finitely
supported functions on the interior, so by the Rayleigh quotient
lambda_min(L_ii) >= lambda_0({7,3}), the bottom of the infinite graph's
spectrum. Outputs data/interior_degree.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import build_hyperbolic, boundary_nodes, degrees  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "interior_degree.json"


def main() -> int:
    rows = []
    for L in (1, 2, 3, 4, 5, 6):
        g = build_hyperbolic(7, 3, L)
        n = len(g["nodes"])
        interior = np.setdiff1d(np.arange(n), boundary_nodes(g))
        d = degrees(n, g["edges"])[interior]
        rows.append({"L": L, "N": n, "interior": int(len(interior)),
                     "min_deg": int(d.min()), "max_deg": int(d.max()),
                     "all_degree_3": bool(np.all(d == 3))})
        print(rows[-1])
    OUT.write_text(json.dumps(rows, indent=1))
    return 0 if all(r["all_degree_3"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
