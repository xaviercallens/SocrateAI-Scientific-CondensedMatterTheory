#!/usr/bin/env python3
"""Diagnose why the Gram-matrix kappa control failed the preregistered 1e-6 tolerance on square R=6
(PREREGISTRATION_11.md). Compares Gram, a fresh direct SVD, and the stored v1.0 value, and
estimates the float64 limit kappa(G) * eps. Outputs data/gram_control_diag.json."""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk  # noqa: E402
from probe_matched import jacobian_matrices  # noqa: E402
from tilings_kappa import log10_kappa_gram  # noqa: E402

D = Path(__file__).resolve().parent / "data"
ref = {r["name"]: r["log10_kappa"] for r in json.loads((D / "h0.json").read_text())}
rows = []
for name, g in (("square R=3", build_square_disk(3)), ("{7,3} L=2", build_hyperbolic(7, 3, 2)),
                ("square R=6", build_square_disk(6)), ("{7,3} L=3", build_hyperbolic(7, 3, 3))):
    lk, _, _ = log10_kappa_gram(g)
    n = len(g["nodes"]); b = boundary_nodes(g)
    mats = jacobian_matrices(n, g["edges"], b); iu = np.triu_indices(len(b), k=1)
    J = np.stack([M[iu] for M in mats], axis=1)
    s = np.linalg.svd(J, compute_uv=False)
    direct = math.log10(s[0] / s[-1])
    rows.append({"name": name, "gram": lk, "direct_now": direct, "h0_json": ref.get(name),
                 "gram_minus_direct": lk - direct, "direct_now_minus_h0": None if ref.get(name) is None else direct - ref[name],
                 "log10_kappa_G": 2 * direct, "eps_times_kappaG": float(np.finfo(float).eps * 10 ** (2 * direct))})
    r = rows[-1]
    print(f"  {name:12} gram={lk:.9f} direct={direct:.9f} h0={ref.get(name)} gram-direct={r['gram_minus_direct']:+.2e} "
          f"direct-h0={r['direct_now_minus_h0']} kappa(G)=1e{2 * direct:.1f} eps*kappa(G)={r['eps_times_kappaG']:.1e}")
(D / "gram_control_diag.json").write_text(json.dumps(rows, indent=1))
