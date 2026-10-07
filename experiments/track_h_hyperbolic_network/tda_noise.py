#!/usr/bin/env python3
"""PREREGISTRATION_6.md: defect detection against measurement noise on the
Neumann-to-Dirichlet map. Outputs data/tda_noise.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, dtn, depths  # noqa: E402
from tda_defect import bottleneck, defect_g, diagrams  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "tda_noise.json"
EPS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
REPS = 10
CONFIGS = (("deep", "max", 100.0), ("deep", "max", 0.01), ("shallow", 1, 100.0))


def metric_from_P(P):
    d = np.diag(P)
    R = d[:, None] + d[None, :] - 2 * P
    R = (R + R.T) / 2
    np.fill_diagonal(R, 0.0)
    return np.maximum(R, 0.0)


def noisy(P, eps, rng):
    E = rng.standard_normal(P.shape)
    E = (E + E.T) / np.sqrt(2)
    s = np.sqrt(np.mean(P ** 2))
    return P + eps * s * E


def stat_pair(R, ref):
    h1 = diagrams(R)[1]
    return (float(np.linalg.norm(R - ref["R"]) / np.linalg.norm(ref["R"])), bottleneck(h1, ref["h1"]))


def run(name, g):
    n, E = len(g["nodes"]), len(g["edges"])
    bnd = boundary_nodes(g)
    P0 = np.linalg.pinv(dtn(n, g["edges"], np.ones(E), bnd), rcond=1e-12)
    R0 = metric_from_P(P0)
    ref = {"R": R0, "h1": diagrams(R0)[1]}
    Ps = {}
    for label, target, factor in CONFIGS:
        v, dv = defect_g(g, bnd, target)
        gv = np.ones(E)
        for e, (a, b) in enumerate(g["edges"]):
            if v in (a, b):
                gv[e] = factor
        Ps[f"{label} x{factor:g}"] = (np.linalg.pinv(dtn(n, g["edges"], gv, bnd), rcond=1e-12), v, dv)
    rng = np.random.default_rng(0)
    res = {"lattice": name, "N": n, "boundary": int(len(bnd)), "eps": EPS, "configs": {}}
    thr = {}
    for eps in EPS:
        nulls = [stat_pair(metric_from_P(noisy(P0, eps, rng)), ref) for _ in range(REPS)]
        thr[eps] = (max(a for a, _ in nulls), max(b for _, b in nulls))
    res["null_threshold"] = {str(e): {"metric": thr[e][0], "H1": thr[e][1]} for e in EPS}
    for cfg, (P, v, dv) in Ps.items():
        det = {"metric": [], "H1": []}
        for eps in EPS:
            st = [stat_pair(metric_from_P(noisy(P, eps, rng)), ref) for _ in range(REPS)]
            det["metric"].append(all(a > thr[eps][0] for a, _ in st))
            det["H1"].append(all(b > thr[eps][1] for _, b in st))
        emax = {k: (max([e for e, d in zip(EPS, v_) if d], default=0.0)) for k, v_ in det.items()}
        res["configs"][cfg] = {"node": v, "depth": dv, "detected": det, "eps_max": emax}
        print(f"  {name:12} {cfg:14} depth {dv}: eps_max metric={emax['metric']:.0e} H1={emax['H1']:.0e}", flush=True)
    return res


def main():
    out = []
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
                    ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10))):
        out.append(run(name, g))
        OUT.write_text(json.dumps({"eps": EPS, "reps": REPS, "results": out}, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
