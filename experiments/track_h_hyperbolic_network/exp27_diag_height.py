#!/usr/bin/env python3
"""POST-HOC diagnostic for PREREGISTRATION_27 (written after its data existed; not a preregistered test). Gate G1 failed for
lambda = 0.05: the explicit double-precision reference (W = 96, height 40) disagrees with the exact block increments at
depths >= 2. Hypothesis: with weak lateral coupling the slowest modes decay by only a few percent per row, so a height of 40 is
not semi-infinite. Test at W = 48, where the zigzag block is still well defined: exact block against explicit references of
increasing height. Writes data/aligned_strip_height_diagnostic.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exp27_aligned_strip_with_unequal_conductances as e27  # noqa: E402

import numpy as np  # noqa: E402
from hyperbolic_network import jacobian  # noqa: E402
import exp24_momentum_resolved_rates_on_the_cylinder as e24  # noqa: E402
from exp23_cylinder_exponential_sum_picture import build_cylinder  # noqa: E402

HERE = Path(__file__).resolve().parent
LAM, W, DD = 0.05, 48, 5
mp.mp.dps = 120
V = e27.block(W, W // 2, DD, LAM)
exact = [e27.log10_sigma_min(V, d) for d in range(DD + 1)]
out = {"post_hoc": True, "lambda": LAM, "W": W, "exact_increments": [exact[d] - exact[d + 1] for d in range(DD)], "explicit": {}}
print("exact increments       :", [round(x, 3) for x in out["exact_increments"]], flush=True)
for H in (20, 40, 80, 160):
    g, el, types = build_cylinder("square", W, H)
    gv = np.where(np.array(types) == "h", LAM, 1.0)
    J = jacobian(len(g["nodes"]), el, gv, np.arange(W))
    C = e24.columns_by_depth(el, types, W, "v")[: DD + 1]
    M = e24.block_matrices(J, C, W)[W // 2]
    ls = [float(np.log10(s[1])) for s in e24.sigma_min_by_depth(M, DD)]
    inc = [ls[d] - ls[d + 1] for d in range(DD)]
    out["explicit"]["H=%d" % H] = inc
    print("explicit H=%-3d increments:" % H, [round(x, 3) for x in inc], flush=True)
(HERE / "data" / "aligned_strip_height_diagnostic.json").write_text(json.dumps(out, indent=1))
print("wrote data/aligned_strip_height_diagnostic.json")
