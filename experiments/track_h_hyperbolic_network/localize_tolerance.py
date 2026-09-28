#!/usr/bin/env python3
"""PREREGISTRATION_10.md: localisation top-1 with random component tolerance on the board
(decoder assumes the ideal model). Outputs data/localize_tolerance.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, dtn  # noqa: E402
from localize_defect import DICT_F  # noqa: E402
from tda_noise import noisy  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "localize_tolerance.json"
TAUS = [1e-3, 1e-2, 5e-2]
EPSS = [3e-4, 3e-3]
TRUE_F = [1.25, 2.0]
TRIALS = 20


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
    nodes = [int(v) for v in interior if dep[v] == int(dep[interior].max())]
    rng = np.random.default_rng(0)
    res = {"lattice": name, "N": n, "nodes_in_class": len(nodes), "cells": {}}
    for tau in TAUS:
        for eps in EPSS:
            for f in TRUE_F:
                hit = 0
                for t in range(TRIALS):
                    v = nodes[t % len(nodes)]
                    i_true = int(np.where(interior == v)[0][0])
                    gb = 1 + tau * rng.uniform(-1, 1, E)
                    Pb = np.linalg.pinv(dtn(n, g["edges"], gb, bnd), rcond=1e-12)
                    Pd = np.linalg.pinv(dtn(n, g["edges"], np.where(masks[v], gb * f, gb), bnd), rcond=1e-12)
                    dP = noisy(Pd, eps, rng) - noisy(Pb, eps, rng)
                    k = int(np.argmin(np.linalg.norm(flat - dP.reshape(1, -1), axis=1)))
                    hit += int(k // len(DICT_F) == i_true)
                res["cells"][f"tau{tau:g} eps{eps:g} x{f:g}"] = {"tau": tau, "eps": eps, "f": f, "top1": hit / TRIALS}
                print(f"  {name:12} tau={tau:.0e} eps={eps:.0e} x{f:<5g} top1={hit / TRIALS:.2f}", flush=True)
    return res


def main():
    out = []
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
                    ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10))):
        out.append(run(name, g))
        OUT.write_text(json.dumps({"taus": TAUS, "eps": EPSS, "trials": TRIALS, "results": out}, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
