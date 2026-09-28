#!/usr/bin/env python3
"""PREREGISTRATION_12.md: minimum detectable single-node contrast vs noise, deepest class, four lattices.
Writes data/minimum_detectable_contrast.json; score() returns the verdicts P1..P4 from the file alone."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, dtn  # noqa: E402
from tda_noise import noisy  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "minimum_detectable_contrast.json"
DICT_F = [0.1, 0.5, 0.8, 0.9, 1.1, 1.25, 1.5, 2.0, 5.0, 10.0, 100.0]
TRUE_F = [0.5, 0.8, 0.9, 1.1, 1.25, 1.5, 2.0]
EPS = [1e-4, 3e-4, 1e-3, 3e-3]
TRIALS = 20
LATTICES = (("{7,3} L=2", lambda: build_hyperbolic(7, 3, 2)), ("square R=6", lambda: build_square_disk(6)),
            ("{7,3} L=3", lambda: build_hyperbolic(7, 3, 3)), ("square R=10", lambda: build_square_disk(10)))


def run_lattice(name, g):
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
    Pd = {(v, f): np.linalg.pinv(dtn(n, g["edges"], np.where(masks[v], f, 1.0), bnd), rcond=1e-12) for v in nodes for f in TRUE_F}
    rng = np.random.default_rng(0)
    cells = {}
    for f in TRUE_F:
        for eps in EPS:
            hit = 0
            for t in range(TRIALS):
                v = nodes[t % len(nodes)]
                i_true = int(np.where(interior == v)[0][0])
                dP = noisy(Pd[(v, f)], eps, rng) - noisy(P0, eps, rng)
                k = int(np.argmin(np.linalg.norm(flat - dP.reshape(1, -1), axis=1)))
                hit += int(k // len(DICT_F) == i_true)
            cells["f%g eps%g" % (f, eps)] = {"f": f, "eps": eps, "top1": hit / TRIALS}
            print("  %-12s f=%-5g eps=%.0e top1=%.2f" % (name, f, eps, hit / TRIALS), flush=True)
    return {"lattice": name, "N": n, "nodes_in_class": len(nodes), "cells": cells}


def run() -> dict:
    return {"dict_f": DICT_F, "true_f": TRUE_F, "eps": EPS, "trials": TRIALS,
            "results": [run_lattice(name, build()) for name, build in LATTICES]}


def score(d: dict) -> dict:
    res = {r["lattice"]: r["cells"] for r in d["results"]}
    top = lambda l, f, e: res[l]["f%g eps%g" % (f, e)]["top1"]
    G1 = all(top(l, 2.0, 3e-4) >= 0.9 for l in res)
    G2 = all(f in DICT_F for f in TRUE_F)
    P1 = top("{7,3} L=3", 1.1, 3e-4) >= 0.9 and top("{7,3} L=3", 0.9, 3e-4) >= 0.9
    P2 = top("square R=10", 1.1, 3e-4) <= 0.5 and top("square R=10", 0.9, 3e-4) <= 0.5
    P3 = all(abs(top(l, a, e) - top(l, b, e)) <= 0.2 for l in res for e in EPS for a, b in ((0.9, 1.1), (0.8, 1.25)))
    P4 = all(top("{7,3} L=3", f, e) >= top("square R=10", f, e) - 0.1 for f in TRUE_F for e in EPS)
    fmin = {}
    for l in res:
        for e in EPS:
            below = [f for f in TRUE_F if f < 1 and top(l, f, e) >= 0.9]
            above = [f for f in TRUE_F if f > 1 and top(l, f, e) >= 0.9]
            fmin["%s eps%g" % (l, e)] = {"below": max(below) if below else None, "above": min(above) if above else None}
    return {"G1": G1, "G2": G2, "P1": P1, "P2": P2, "P3": P3, "P4": P4, "f_min": fmin}


def main() -> int:
    d = run()
    d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", {k: v for k, v in d["verdicts"].items() if k != "f_min"})
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
