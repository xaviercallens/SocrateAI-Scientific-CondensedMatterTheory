#!/usr/bin/env python3
"""PREREGISTRATION_5.md: persistent homology of the boundary resistance metric,
with and without a bulk defect, against a disorder null.

Pipeline per configuration g:
  Lambda = dtn(g)  ->  Lambda^+  ->  R_ij = L+_ii + L+_jj - 2 L+_ij (boundary
  effective resistances)  ->  Vietoris-Rips (Gudhi) H0/H1 diagrams.
Statistics vs the unit configuration: bottleneck(H0), bottleneck(H1),
||R - R0||_F / ||R0||_F. Null: U[0.5,1.5] disorder, 20 seeds; threshold = 95th
percentile. The unit Lambda is taken from the PUBLISHED dataset file when
present (and asserted equal to the recomputed one).

Outputs: data/tda_defect.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import gudhi
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, depths, dtn,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "tda_defect.json"
PUBLISHED = HERE / "release" / "build" / "hf_dataset" / "dtn"
SEEDS = 20
PCT = 95


def resistance_metric(lam):
    P = np.linalg.pinv(lam, rcond=1e-12)
    d = np.diag(P)
    R = d[:, None] + d[None, :] - 2 * P
    R = (R + R.T) / 2
    np.fill_diagonal(R, 0.0)
    return np.maximum(R, 0.0)


def diagrams(R):
    st = gudhi.RipsComplex(distance_matrix=R.tolist()).create_simplex_tree(max_dimension=2)
    st.persistence()
    h0 = np.array([p for p in st.persistence_intervals_in_dimension(0) if np.isfinite(p[1])])
    h1 = np.array(st.persistence_intervals_in_dimension(1))
    return h0.reshape(-1, 2), h1.reshape(-1, 2)


def bottleneck(a, b):
    if len(a) == 0 and len(b) == 0:
        return 0.0
    return float(gudhi.bottleneck_distance(a.tolist(), b.tolist()))


def defect_g(g, bnd, depth_target):
    n, edges = len(g["nodes"]), g["edges"]
    d = depths(g, bnd)
    interior = np.setdiff1d(np.arange(n), bnd)
    cand = interior[d[interior] == (d[interior].max() if depth_target == "max" else depth_target)]
    v = int(cand[0])
    return v, int(d[v])


def stats(g, bnd, gvals, ref):
    n = len(g["nodes"])
    R = resistance_metric(dtn(n, g["edges"], gvals, bnd))
    h0, h1 = diagrams(R)
    return {"bottleneck_H0": bottleneck(h0, ref["h0"]), "bottleneck_H1": bottleneck(h1, ref["h1"]),
            "rel_metric_change": float(np.linalg.norm(R - ref["R"]) / np.linalg.norm(ref["R"])),
            "n_H1_classes": int(len(h1))}


def run(name, g, tag):
    n, E = len(g["nodes"]), len(g["edges"])
    bnd = boundary_nodes(g)
    lam = dtn(n, g["edges"], np.ones(E), bnd)
    pub = PUBLISHED / f"{tag}.npz"
    published_identical = None
    if pub.exists():
        published_identical = bool(np.allclose(np.load(pub)["Lambda"], lam, atol=1e-12))
        if published_identical:
            lam = np.load(pub)["Lambda"]
    R0 = resistance_metric(lam)
    h0, h1 = diagrams(R0)
    ref = {"R": R0, "h0": h0, "h1": h1}
    out = {"lattice": name, "N": n, "boundary": int(len(bnd)), "published_matrix_used": published_identical,
           "unit_H1_classes": int(len(h1)),
           "unit_H1_max_persistence": float(np.max(h1[:, 1] - h1[:, 0])) if len(h1) else 0.0,
           "configs": {}, "null": []}
    for label, target in (("deep", "max"), ("shallow", 1)):
        v, dv = defect_g(g, bnd, target)
        for factor in (100.0, 0.01):
            gv = np.ones(E)
            for e, (a, b) in enumerate(g["edges"]):
                if v in (a, b):
                    gv[e] = factor
            s = stats(g, bnd, gv, ref)
            s.update({"node": v, "depth": dv, "factor": factor})
            out["configs"][f"{label} x{factor:g}"] = s
    for seed in range(SEEDS):
        gv = np.random.default_rng(seed).uniform(0.5, 1.5, E)
        out["null"].append(stats(g, bnd, gv, ref))
    thr = {k: float(np.percentile([r[k] for r in out["null"]], PCT))
           for k in ("bottleneck_H0", "bottleneck_H1", "rel_metric_change")}
    out["null_p95"] = thr
    for k, s in out["configs"].items():
        s["detected"] = {m: bool(s[m] > thr[m]) for m in thr}
    print(f"\n{name}: N={n}, boundary={len(bnd)}, unit H1 classes={out['unit_H1_classes']}, "
          f"published matrix used={published_identical}")
    print(f"  null p95: H0 {thr['bottleneck_H0']:.3g}  H1 {thr['bottleneck_H1']:.3g}  metric {thr['rel_metric_change']:.3g}")
    for k, s in out["configs"].items():
        d = s["detected"]
        print(f"  {k:12} (node {s['node']}, depth {s['depth']}): H0 {s['bottleneck_H0']:.3g} [{'DET' if d['bottleneck_H0'] else ' - '}]"
              f"  H1 {s['bottleneck_H1']:.3g} [{'DET' if d['bottleneck_H1'] else ' - '}]"
              f"  metric {s['rel_metric_change']:.3g} [{'DET' if d['rel_metric_change'] else ' - '}]")
    return out


def main() -> int:
    results = [run("{7,3} L=3", build_hyperbolic(7, 3, 3), "7_3_L3"),
               run("square R=10", build_square_disk(10), "square_R10"),
               run("{7,3} L=2", build_hyperbolic(7, 3, 2), "7_3_L2"),
               run("square R=6", build_square_disk(6), "square_R6")]
    OUT.write_text(json.dumps({"gudhi": gudhi.__version__, "seeds": SEEDS, "percentile": PCT,
                               "results": results}, indent=1))
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
