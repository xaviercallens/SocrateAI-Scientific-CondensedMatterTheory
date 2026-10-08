#!/usr/bin/env python3
"""PREREGISTRATION_30.md, post hoc diagnostic of the failed gate G2 (duplicated columns): which layers give a large median death and why."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth  # noqa: E402
from exp30_jacobian_column_cloud_homology import gram_columns, h0_deaths, sine_distance  # noqa: E402
from hyperbolic_network import build_square_disk  # noqa: E402

g = build_square_disk(4)
G = gram_columns(g)
dep = edge_depth(g)
dist, _ = sine_distance(np.block([[G, G], [G, G]]))
dep2 = np.concatenate([dep, dep])
print("min diag of G:", float(np.min(np.diag(G))), "n edges", len(dep))
for k in range(0, int(dep.max()) + 1):
    idx = np.where(dep2 == k)[0]
    if len(idx) < 4:
        print(k, "size", len(idx), "skipped")
        continue
    d = dist[np.ix_(idx, idx)]
    dth = np.sort(h0_deaths(d))
    pair = [float(d[i, i + len(idx) // 2]) for i in range(min(3, len(idx) // 2))]
    print(k, "size", len(idx), "n zero-ish deaths (<1e-6):", int((dth < 1e-6).sum()), "of", len(dth), "median", float(np.median(dth)), "pair dist", pair)
