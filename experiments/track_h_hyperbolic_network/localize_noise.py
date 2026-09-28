#!/usr/bin/env python3
"""PREREGISTRATION_9.md: localisation top-1 vs noise level (deepest class, contrasts 1.25 and 2).
Same decoder and dictionary as localize_defect.py. Outputs data/localize_noise.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, dtn  # noqa: E402
from localize_defect import DICT_F  # noqa: E402
from tda_noise import noisy  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "localize_noise.json"
EPS = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1]
TRUE_F = [1.25, 2.0]
TRIALS = 20


def eps_loc(tops):
    best = 0.0
    for e, t in zip(EPS, tops):
        if t >= 0.9:
            best = e
        else:
            return best
    return "> 3e-1"


def run(name, g):
    n, E = len(g["nodes"]), len(g["edges"])
    bnd = boundary_nodes(g); dep = depths(g, bnd)
    interior = np.setdiff1d(np.arange(n), bnd)
    P0 = np.linalg.pinv(dtn(n, g["edges"], np.ones(E), bnd), rcond=1e-12)
    masks = {int(v): np.array([v in e for e in g["edges"]]) for v in interior}
    flat = np.empty((len(interior) * len(DICT_F), P0.size))
    for i, v in enumerate(interior):
        for j, f in enumerate(DICT_F):
            flat[i * len(DICT_F) + j] = (np.linalg.pinv(dtn(n, g["edges"], np.where(masks[int(v)], f, 1.0), bnd),
                                                        rcond=1e-12) - P0).ravel()
    dmax = int(dep[interior].max())
    nodes = [int(v) for v in interior if dep[v] == dmax]
    Pd = {(v, f): np.linalg.pinv(dtn(n, g["edges"], np.where(masks[v], f, 1.0), bnd), rcond=1e-12)
          for v in nodes for f in TRUE_F}
    rng = np.random.default_rng(0)
    res = {"lattice": name, "N": n, "d_max": dmax, "nodes_in_class": len(nodes), "cells": {}}
    for f in TRUE_F:
        tops = []
        for eps in EPS:
            hit = 0
            for t in range(TRIALS):
                v = nodes[t % len(nodes)]
                i_true = int(np.where(interior == v)[0][0])
                dP = noisy(Pd[(v, f)], eps, rng) - noisy(P0, eps, rng)
                k = int(np.argmin(np.linalg.norm(flat - dP.reshape(1, -1), axis=1)))
                hit += int(k // len(DICT_F) == i_true)
            tops.append(hit / TRIALS)
        res["cells"][f"x{f:g}"] = {"eps": EPS, "top1": tops, "eps_loc": eps_loc(tops)}
        print(f"  {name:12} x{f:<5g} top1 by eps " + " ".join(f"{t:.2f}" for t in tops) + f"   eps_loc={eps_loc(tops)}", flush=True)
    return res


def main():
    out = []
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
                    ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10))):
        out.append(run(name, g))
        OUT.write_text(json.dumps({"eps": EPS, "trials": TRIALS, "results": out}, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
