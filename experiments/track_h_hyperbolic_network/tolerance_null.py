#!/usr/bin/env python3
"""PREREGISTRATION_7.md: defect detection against component tolerance
(model-based regime B) and differential detection at 3e-4 noise (regime A).
Outputs data/tolerance_null.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, dtn  # noqa: E402
from tda_defect import defect_g  # noqa: E402
from tda_noise import metric_from_P, noisy  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "tolerance_null.json"
TAUS = [1e-3, 1e-2, 5e-2]
NB = 20        # boards, regime B
NA = 10        # boards, regime A
EPS = 3e-4     # measurement noise, regime A
FACTOR = 100.0


def Rof(g, gv, bnd):
    P = np.linalg.pinv(dtn(len(g["nodes"]), g["edges"], gv, bnd), rcond=1e-12)
    return P, metric_from_P(P)


def rel(R, ref):
    return float(np.linalg.norm(R - ref) / np.linalg.norm(ref))


def run(name, g):
    E = len(g["edges"]); bnd = boundary_nodes(g)
    v, dv = defect_g(g, bnd, "max")
    mask = np.array([v in e for e in g["edges"]])
    _, R0 = Rof(g, np.ones(E), bnd)
    out = {"lattice": name, "N": len(g["nodes"]), "defect_node": v, "defect_depth": dv, "tau": {}}
    for tau in TAUS:
        rng = np.random.default_rng(1)
        nullB, defB = [], []
        for _ in range(NB):
            gv = 1 + tau * rng.uniform(-1, 1, E); nullB.append(rel(Rof(g, gv, bnd)[1], R0))
        for _ in range(NB):
            gv = 1 + tau * rng.uniform(-1, 1, E); gv = np.where(mask, gv * FACTOR, gv)
            defB.append(rel(Rof(g, gv, bnd)[1], R0))
        nullA, defA = [], []
        for _ in range(NA):
            gv = 1 + tau * rng.uniform(-1, 1, E)
            P, _ = Rof(g, gv, bnd)
            Pd, _ = Rof(g, np.where(mask, gv * FACTOR, gv), bnd)
            Rb = metric_from_P(noisy(P, EPS, rng))
            nullA.append(rel(metric_from_P(noisy(P, EPS, rng)), Rb))
            defA.append(rel(metric_from_P(noisy(Pd, EPS, rng)), Rb))
        out["tau"][str(tau)] = {
            "B_null_max": max(nullB), "B_defect_min": min(defB), "B_defect_median": float(np.median(defB)),
            "B_detected": bool(min(defB) > max(nullB)),
            "A_null_max": max(nullA), "A_defect_min": min(defA), "A_detected": bool(min(defA) > max(nullA))}
        t = out["tau"][str(tau)]
        print(f"  {name:12} tau={tau:.0e}  B: null max {t['B_null_max']:.2e} defect min {t['B_defect_min']:.2e} "
              f"{'DET' if t['B_detected'] else ' - '} | A: null max {t['A_null_max']:.2e} defect min {t['A_defect_min']:.2e} "
              f"{'DET' if t['A_detected'] else ' - '}", flush=True)
    return out


def main():
    res = [run(n, g) for n, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
                                   ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10)))]
    OUT.write_text(json.dumps({"taus": TAUS, "boards_B": NB, "boards_A": NA, "eps_A": EPS, "factor": FACTOR,
                               "results": res}, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
