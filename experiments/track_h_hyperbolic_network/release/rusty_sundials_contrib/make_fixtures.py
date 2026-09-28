#!/usr/bin/env python3
"""Regenerate examples/python/rc_network/fixtures/*.json from the Track H builders."""
import json
import sys
from pathlib import Path

import numpy as np

TRACK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TRACK))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk  # noqa: E402

OUT = Path(__file__).resolve().parent / "examples" / "python" / "rc_network" / "fixtures"


def dump(g, name, desc):
    z = np.asarray(g["nodes"])
    OUT.joinpath(name).write_text(json.dumps({
        "description": desc, "N": len(z),
        "x": z.real.round(12).tolist(), "y": z.imag.round(12).tolist(),
        "edges": [list(map(int, e)) for e in g["edges"]],
        "boundary": [int(b) for b in boundary_nodes(g)]}))
    print("wrote", name, len(z))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    dump(build_hyperbolic(7, 3, 2), "hyperbolic_7_3_L2.json", "{7,3} tiling, 2 tile layers, Poincare disk coordinates")
    dump(build_square_disk(6), "square_R6.json", "square-lattice disk, radius 6")
