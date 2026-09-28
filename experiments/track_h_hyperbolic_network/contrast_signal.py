#!/usr/bin/env python3
"""EXPLORATORY (not preregistered): boundary-metric signal of a single-node defect
as a function of contrast, noiseless, at maximal and unit depth. Written to check
a claim about linearity made in TDA_RESULTS.md. Outputs data/contrast_signal.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, dtn  # noqa: E402
from tda_defect import defect_g  # noqa: E402
from tda_noise import metric_from_P  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "contrast_signal.json"
FACTORS = [0.01, 0.1, 0.5, 0.8, 1.25, 2.0, 5.0, 10.0, 100.0]


def main():
    out = []
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
                    ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10))):
        E = len(g["edges"]); bnd = boundary_nodes(g); n = len(g["nodes"])
        R0 = metric_from_P(np.linalg.pinv(dtn(n, g["edges"], np.ones(E), bnd), rcond=1e-12))
        row = {"lattice": name, "N": n, "depths": {}}
        for label, target in (("max", "max"), ("depth1", 1)):
            v, dv = defect_g(g, bnd, target)
            mask = np.array([v in e for e in g["edges"]])
            sig = {}
            for f in FACTORS:
                R = metric_from_P(np.linalg.pinv(dtn(n, g["edges"], np.where(mask, f, 1.0), bnd), rcond=1e-12))
                sig[str(f)] = float(np.linalg.norm(R - R0) / np.linalg.norm(R0))
            row["depths"][label] = {"node": v, "depth": dv, "signal": sig}
            print(f"  {name:12} {label:6} depth {dv}: " + "  ".join(f"x{f:g}:{sig[str(f)]:.2e}" for f in FACTORS))
        out.append(row)
    OUT.write_text(json.dumps({"exploratory": True, "factors": FACTORS, "results": out}, indent=1))


if __name__ == "__main__":
    main()
