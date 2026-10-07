#!/usr/bin/env python3
"""PREREGISTRATION_3.md part C: is the probe-matched gap a dimensionality effect?

For the square lattice at the matched probe count, sigma_1 / sigma_r is the
condition number of its BEST-conditioned r-dimensional parameter subspace (top-r
right singular vectors), with r = the hyperbolic identifiable dimension from
data/identifiability.json. Compared with the hyperbolic identifiable-subspace
kappa. Outputs: data/subspace_control.json
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_square_disk  # noqa: E402
from probe_matched import jacobian_matrices  # noqa: E402

D = Path(__file__).resolve().parent / "data"


def singular_values(g):
    n = len(g["nodes"]); bnd = boundary_nodes(g)
    mats = jacobian_matrices(n, g["edges"], bnd)
    iu = np.triu_indices(len(bnd), k=1)
    return np.linalg.svd(np.stack([M[iu] for M in mats], axis=1), compute_uv=False)


def main():
    ident = {r["name"]: r for r in json.loads((D / "identifiability.json").read_text())}
    out = []
    for hyp, R in (("{7,3} L=2, 44 probes", 6), ("{7,3} L=3, 76 probes", 10)):
        h = ident[hyp]
        r = next(iter(h["exact_ranks"].values()))
        s = singular_values(build_square_disk(R))
        flat_r = math.log10(s[0] / s[r - 1])
        out.append({"hyperbolic": hyp, "r": r, "hyp_log10_kappa_identifiable": h["log10_kappa_identifiable"],
                    "square": f"R={R}", "square_E": int(len(s)), "square_log10_sigma1_over_sigma_r": flat_r,
                    "square_full_log10_kappa": math.log10(s[0] / s[-1]),
                    "flat_best_subspace_worse_than_hyperbolic": flat_r > h["log10_kappa_identifiable"]})
        print(f"  r={r}: hyperbolic kappa_id={h['log10_kappa_identifiable']:.2f}  square best-{r} subspace "
              f"sigma1/sigma_r={flat_r:.2f}  (full {out[-1]['square_full_log10_kappa']:.2f})")
    (D / "subspace_control.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
