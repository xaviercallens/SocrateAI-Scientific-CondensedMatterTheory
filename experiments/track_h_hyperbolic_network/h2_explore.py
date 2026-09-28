#!/usr/bin/env python3
"""EXPLORATORY (post-hoc, not preregistered) extension of H2.

The preregistered H2 test (PREREGISTRATION_2.md part C) REFUTED the claim
that lambda_min(L_ii) of the {7,3} tiling is bounded below at L = 2..4 (it
fell by 2.37x between L=2 and L=4, past the stated 2x threshold). This
script asks the question that refutation leaves open -- is the decrease
slowing toward a positive limit, or not? -- by computing L = 5, 6 with a
sparse eigensolver. It is labelled exploratory everywhere it is reported:
it cannot rescue the refuted prediction, only inform the next one.

Reference value, cited not derived: the infinite 3-regular tree's
combinatorial Laplacian has bottom of spectrum 3 - 2*sqrt(2) ~ 0.1716, and
the {7,3} graph, being covered by that tree, has bottom of spectrum at most
that value [EXTERNE: covering/Brooks-type comparison]; nonamenability of the
{7,3} graph implies its bottom of spectrum is strictly positive [EXTERNE:
Kesten; Dodziuk; Mohar]. Neither fact is used as evidence below -- only as
the scale against which the measured values are read.

Outputs: data/h2_explore.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import build_hyperbolic, boundary_nodes  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "h2_explore.json"


def lambda_min_sparse(g):
    n = len(g["nodes"])
    rows, cols, vals = [], [], []
    deg = np.zeros(n)
    for u, v in g["edges"]:
        rows += [u, v]; cols += [v, u]; vals += [-1.0, -1.0]
        deg[u] += 1; deg[v] += 1
    L = sp.csr_matrix((vals, (rows, cols)), shape=(n, n)) + sp.diags(deg)
    interior = np.setdiff1d(np.arange(n), boundary_nodes(g))
    Lii = L[interior][:, interior].tocsc()
    val = eigsh(Lii, k=1, sigma=0.0, which="LM", return_eigenvectors=False)[0]
    return float(val), int(len(interior))


def main() -> int:
    rows = []
    for L in (2, 3, 4, 5, 6):
        t0 = time.time()
        g = build_hyperbolic(7, 3, L)
        lam, ni = lambda_min_sparse(g)
        rows.append({"L": L, "N": len(g["nodes"]), "interior": ni, "lambda_min": lam,
                     "seconds": round(time.time() - t0, 1)})
        print(f"  L={L}  N={len(g['nodes']):6d}  interior={ni:6d}  lambda_min={lam:.5f}  "
              f"({rows[-1]['seconds']}s)")
    ratios = [rows[i + 1]["lambda_min"] / rows[i]["lambda_min"] for i in range(len(rows) - 1)]
    print("  successive ratios:", [round(r, 3) for r in ratios])
    print(f"  reference: 3-2*sqrt(2) = {3 - 2 * np.sqrt(2):.5f} (upper bound on the infinite-graph limit, cited)")
    OUT.write_text(json.dumps({"exploratory": True, "rows": rows, "ratios": ratios}, indent=1))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
