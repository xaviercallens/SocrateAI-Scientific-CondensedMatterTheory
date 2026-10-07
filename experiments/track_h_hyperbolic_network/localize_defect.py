#!/usr/bin/env python3
"""PREREGISTRATION_8.md: localise a single-node defect from the difference of two noisy NtD maps
with a dictionary matched filter. Outputs data/localize_defect.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import shortest_path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, dtn  # noqa: E402
from tda_noise import noisy  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "localize_defect.json"
DICT_F = [0.1, 0.5, 0.8, 1.25, 2.0, 5.0, 10.0, 100.0]
TRUE_F = [0.8, 1.25, 2.0, 10.0, 100.0]
EPS = 3e-4
TRIALS = 20


def run(name, g):
    n, E = len(g["nodes"]), len(g["edges"])
    bnd = boundary_nodes(g)
    dep = depths(g, bnd)
    interior = np.setdiff1d(np.arange(n), bnd)
    P0 = np.linalg.pinv(dtn(n, g["edges"], np.ones(E), bnd), rcond=1e-12)
    masks = {int(v): np.array([v in e for e in g["edges"]]) for v in interior}
    dic = np.empty((len(interior), len(DICT_F), *P0.shape))
    for i, v in enumerate(interior):
        for j, f in enumerate(DICT_F):
            dic[i, j] = np.linalg.pinv(dtn(n, g["edges"], np.where(masks[int(v)], f, 1.0), bnd), rcond=1e-12) - P0
    flat = dic.reshape(len(interior) * len(DICT_F), -1)
    ij = np.array([[a, b] for a, b in g["edges"]])
    A = coo_matrix((np.ones(len(ij)), (ij[:, 0], ij[:, 1])), shape=(n, n))
    hops = shortest_path(A + A.T, unweighted=True, directed=False)
    dmax = int(dep[interior].max())
    classes = {"depth1": 1, "mid": dmax // 2, "max": dmax}
    rng = np.random.default_rng(0)
    res = {"lattice": name, "N": n, "interior_nodes": int(len(interior)), "d_max": dmax, "cells": {}}
    for cname, d in classes.items():
        nodes = [int(v) for v in interior if dep[v] == d]
        for f in TRUE_F:
            j_true = DICT_F.index(f)
            hit = 0; dist = []; chit = 0
            for t in range(TRIALS):
                v = nodes[t % len(nodes)]
                i_true = int(np.where(interior == v)[0][0])
                Pd = np.linalg.pinv(dtn(n, g["edges"], np.where(masks[v], f, 1.0), bnd), rcond=1e-12)
                dP = noisy(Pd, EPS, rng) - noisy(P0, EPS, rng)
                k = int(np.argmin(np.linalg.norm(flat - dP.reshape(1, -1), axis=1)))
                i_est, j_est = divmod(k, len(DICT_F))
                hit += int(i_est == i_true); chit += int(j_est == j_true)
                dist.append(hops[int(interior[i_est]), v])
            res["cells"][f"{cname} x{f:g}"] = {"depth": d, "nodes_in_class": len(nodes), "top1": hit / TRIALS,
                                               "mean_hops": float(np.mean(dist)), "contrast_acc": chit / TRIALS}
            c = res["cells"][f"{cname} x{f:g}"]
            print(f"  {name:12} {cname:7} d={d} x{f:<5g} nodes={len(nodes):3d}  top1={c['top1']:.2f}  "
                  f"hops={c['mean_hops']:.2f}  contrast_acc={c['contrast_acc']:.2f}", flush=True)
    return res


def main():
    out = []
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
                    ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10))):
        out.append(run(name, g))
        OUT.write_text(json.dumps({"eps": EPS, "trials": TRIALS, "dictionary_contrasts": DICT_F, "results": out}, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
