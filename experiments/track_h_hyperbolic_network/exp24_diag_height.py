#!/usr/bin/env python3
"""POST-HOC diagnostic for PREREGISTRATION_24 (not part of the preregistered tests). Gate G2 failed: the block machinery
(H = 14 rows below the boundary) gave condition numbers up to 0.34 decades larger than preregistration 23's explicit SVD
(H = 18). This script recomputes the explicit SVD of the vertical-edge Jacobian at W = 64 for H = 14 and H = 18 and
compares both with the block-implied values stored in data/momentum_resolved_rates_on_the_cylinder.json.
Writes data/momentum_height_diagnostic.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import depths, jacobian  # noqa: E402
from exp23_cylinder_exponential_sum_picture import build_cylinder  # noqa: E402

HERE = Path(__file__).resolve().parent
W, DMAX = 64, 7
blocks = json.loads((HERE / "data" / "momentum_resolved_rates_on_the_cylinder.json").read_text())["runs"]["v W=64"]["blocks"]
pi = blocks[str(W // 2)]
gmax = {d: max(b["log10_sigma_max"][b["d"].index(d)] for b in blocks.values() if d in b["d"]) for d in range(DMAX + 1)}
block_kappa = {d: gmax[d] - pi["log10_sigma_min"][pi["d"].index(d)] for d in pi["d"] if d in gmax}
out = {"post_hoc": True, "W": W, "block_implied_log10_kappa_H14": block_kappa, "explicit": {}}
for H in (14, 18):
    g, el, types = build_cylinder("square", W, H)
    n = len(g["nodes"]); bnd = np.arange(W)
    d = depths(g, bnd); ed = np.minimum(d[[a for a, _ in el]], d[[b for _, b in el]]); types = np.array(types)
    J = jacobian(n, el, np.ones(len(el)), bnd)
    ser = {}
    for dd in range(DMAX + 1):
        cols = np.where((ed <= dd) & (types == "v"))[0]
        s = np.linalg.svd(J[:, cols], compute_uv=False)
        ser[dd] = float(np.log10(s[0] / s[-1]))
    out["explicit"]["H=%d" % H] = ser
    print("explicit H=%d log10 kappa_d:" % H, " ".join("%.3f" % ser[k] for k in sorted(ser)))
print("block-implied (H=14, pi block):", " ".join("%.3f" % block_kappa[k] for k in sorted(block_kappa)))
(HERE / "data" / "momentum_height_diagnostic.json").write_text(json.dumps(out, indent=1))
print("wrote data/momentum_height_diagnostic.json")
