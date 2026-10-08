#!/usr/bin/env python3
"""PILOT for PREREGISTRATION_32.md (disclosed, excluded from scoring): depth-ordered Gram-Schmidt residuals on the square disk of radius 10.
Householder QR of the explicit Jacobian with columns sorted by depth; R_jj = distance of column j to the span of earlier columns."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth, jac_s  # noqa: E402
from hyperbolic_network import build_square_disk  # noqa: E402

R = int(sys.argv[1]) if len(sys.argv) > 1 else 10
g = build_square_disk(R)
dep = edge_depth(g)
J = jac_s(g, 0.0)
order = np.argsort(dep, kind="stable")
Js, ds = J[:, order], dep[order]
Rm = np.linalg.qr(Js, mode="r")
rjj = np.abs(np.diag(Rm))
norms = np.linalg.norm(Js, axis=0)
print("R", R, "N", len(g["nodes"]), "E", len(dep), "dmax", dep.max(), "||J||", np.linalg.norm(J, 2))
for k in range(1, int(dep.max()) + 1):
    cols = np.where(ds <= k)[0]
    sv = np.linalg.svd(Js[:, cols], compute_uv=False)
    lay = np.where(ds == k)[0]
    rl = rjj[lay]
    # leave-one-out residual within J_{<=k}: 1/sqrt(diag(G^-1)) via QR-based inverse of R
    Rk = np.linalg.qr(Js[:, cols], mode="r")
    Rinv = np.linalg.inv(Rk)
    loo = 1.0 / np.linalg.norm(Rinv, axis=1)
    print(f"k={k:2d} n_layer={len(lay):4d} log10 sigma_min={np.log10(sv[-1]):8.3f} log10 min ordered resid (layer)={np.log10(rl.min()):8.3f} "
          f"median={np.log10(np.median(rl)):8.3f} log10 min LOO={np.log10(loo.min()):8.3f}")
