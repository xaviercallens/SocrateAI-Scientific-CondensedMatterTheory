#!/usr/bin/env python3
"""PILOT 2 for PREREGISTRATION_32.md (disclosed, excluded from scoring): residual to the span of strictly shallower layers, and H0 of the residual cloud, square disk radius 10."""
import sys
from pathlib import Path

import gudhi
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth, jac_s  # noqa: E402
from hyperbolic_network import build_square_disk  # noqa: E402

R = int(sys.argv[1]) if len(sys.argv) > 1 else 10
g = build_square_disk(R)
dep = edge_depth(g)
J = jac_s(g, 0.0)


def med_death(X):
    Xn = X / np.linalg.norm(X, axis=0, keepdims=True)
    c2 = np.clip((Xn.T @ Xn) ** 2, 0, 1)
    d = np.sqrt(np.clip(1 - c2, 0, 1))
    st = gudhi.RipsComplex(distance_matrix=d, max_edge_length=2.0).create_simplex_tree(max_dimension=1)
    st.compute_persistence(min_persistence=-1.0)
    return float(np.median([b for (dim, (a, b)) in st.persistence(min_persistence=-1.0) if dim == 0 and np.isfinite(b)]))


for k in range(1, int(dep.max()) + 1):
    lay = np.where(dep == k)[0]
    if len(lay) < 4:
        continue
    prev = np.where(dep < k)[0]
    Q, _ = np.linalg.qr(J[:, prev])
    Y = J[:, lay] - Q @ (Q.T @ J[:, lay])
    s_k = np.linalg.norm(Y, axis=0)
    print(f"k={k} n={len(lay)} log10 min s_k={np.log10(s_k.min()):8.3f} median s_k/||J_e||={np.median(s_k / np.linalg.norm(J[:, lay], axis=0)):.4f} "
          f"H0 median death original={med_death(J[:, lay]):.4f} residual={med_death(Y):.4f}")
