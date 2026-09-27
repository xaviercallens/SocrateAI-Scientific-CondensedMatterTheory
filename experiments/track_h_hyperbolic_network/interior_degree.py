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


TOL = 1e-9


def interior_is_previous(g, prev, interior):
    """True iff the interior of g, with its induced edges, is the graph prev
    (nodes matched by Poincare-disk coordinates to within TOL)."""
    zi = np.asarray(g["nodes"])[interior]
    zp = np.asarray(prev["nodes"])
    if len(zi) != len(zp):
        return False
    dist = np.abs(zi[:, None] - zp[None, :])
    match = dist.argmin(axis=1)
    if dist[np.arange(len(zi)), match].max() > TOL or len(set(match.tolist())) != len(zp):
        return False
    pos = {int(v): int(match[k]) for k, v in enumerate(interior)}
    induced = {frozenset((pos[a], pos[b])) for a, b in g["edges"] if a in pos and b in pos}
    return induced == {frozenset(map(int, e)) for e in prev["edges"]}


def main() -> int:
    rows = []
    prev = None
    for L in (1, 2, 3, 4, 5, 6):
        g = build_hyperbolic(7, 3, L)
        n = len(g["nodes"])
        interior = np.setdiff1d(np.arange(n), boundary_nodes(g))
        d = degrees(n, g["edges"])[interior]
        rows.append({"L": L, "N": n, "interior": int(len(interior)),
                     "min_deg": int(d.min()), "max_deg": int(d.max()),
                     "all_degree_3": bool(np.all(d == 3)),
                     "interior_equals_previous_graph": None if prev is None
                     else bool(interior_is_previous(g, prev, interior))})
        print(rows[-1])
        prev = g
    OUT.write_text(json.dumps(rows, indent=1))
    ok = all(r["all_degree_3"] and r["interior_equals_previous_graph"] is not False for r in rows)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
