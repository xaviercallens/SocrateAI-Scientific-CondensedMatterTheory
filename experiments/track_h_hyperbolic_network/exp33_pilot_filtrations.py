#!/usr/bin/env python3
"""PILOT for PREREGISTRATION_33.md (disclosed, excluded from scoring): three filtrations of the Jacobian column cloud on the square disk of radius R
and persistence-image / landscape features per depth layer. Prints per-layer statistics only; writes nothing in data/."""
import sys
from pathlib import Path

import gudhi
import gudhi.representations as gr
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth, jac_s  # noqa: E402
from hyperbolic_network import build_square_disk  # noqa: E402

R = int(sys.argv[1]) if len(sys.argv) > 1 else 8
g = build_square_disk(R)
dep = edge_depth(g)
J = jac_s(g, 0.0)
J = J / np.linalg.norm(J, axis=0, keepdims=True)


def diagrams(dist, maxdim=1):
    st = gudhi.RipsComplex(distance_matrix=dist, max_edge_length=2.0).create_simplex_tree(max_dimension=maxdim + 1)
    st.compute_persistence(min_persistence=-1.0)
    out = {}
    for d in range(maxdim + 1):
        pts = np.array([(b, de) for (dim, (b, de)) in st.persistence(min_persistence=-1.0) if dim == d and np.isfinite(de)])
        out[d] = pts.reshape(-1, 2)
    return out


def sine_dist(X):
    c2 = np.clip((X.T @ X) ** 2, 0, 1)
    return np.sqrt(np.clip(1 - c2, 0, 1))


def principal_angle_filtration(J, dep, k):
    """Sublevel filtration on the complete graph of layer k: vertex value = sine of the angle of the column to the span of strictly shallower layers;
    edge value = max of the two vertex values. Persistence of H0 then records at which residual level columns join."""
    lay = np.where(dep == k)[0]
    prev = np.where(dep < k)[0]
    Q, _ = np.linalg.qr(J[:, prev])
    Y = J[:, lay] - Q @ (Q.T @ J[:, lay])
    s = np.linalg.norm(Y, axis=0)
    st = gudhi.SimplexTree()
    for i, v in enumerate(s):
        st.insert([i], filtration=float(v))
    n = len(lay)
    for i in range(n):
        for j in range(i + 1, n):
            st.insert([i, j], filtration=float(max(s[i], s[j])))
    st.compute_persistence(min_persistence=-1.0)
    return s


print("R", R, "E", len(dep), "dmax", dep.max())
PI = gr.PersistenceImage(bandwidth=0.05, resolution=[10, 10], im_range=[0, 1, 0, 1])
for k in range(1, int(dep.max()) + 1):
    lay = np.where(dep == k)[0]
    if len(lay) < 4:
        continue
    X = J[:, lay]
    # (a) pairwise sine distance (as prereg 30)
    da = diagrams(sine_dist(X), maxdim=1)
    # (b) residual cloud: columns projected off the shallower span, renormalised, pairwise sine distance
    prev = np.where(dep < k)[0]
    Q, _ = np.linalg.qr(J[:, prev])
    Y = X - Q @ (Q.T @ X)
    s = np.linalg.norm(Y, axis=0)
    Yn = Y / s[None, :]
    db = diagrams(sine_dist(Yn), maxdim=1)
    # (c) principal-angle sublevel values
    h1_a = float(np.sum(da[1][:, 1] - da[1][:, 0])) if len(da[1]) else 0.0
    h1_b = float(np.sum(db[1][:, 1] - db[1][:, 0])) if len(db[1]) else 0.0
    img = PI.fit_transform([da[0]])[0]
    print(f"k={k} n={len(lay)} | (a) H0 med death {np.median(da[0][:,1]):.3f} H1 total {h1_a:.3f} n_H1 {len(da[1])} | "
          f"(b) residual cloud H0 med {np.median(db[0][:,1]):.3f} H1 total {h1_b:.3f} n_H1 {len(db[1])} | "
          f"(c) log10 median s {np.log10(np.median(s)):.3f} min {np.log10(s.min()):.3f} | PI norm {np.linalg.norm(img):.3f}")
