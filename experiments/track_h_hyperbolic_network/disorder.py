#!/usr/bin/env python3
"""PREREGISTRATION_3.md part B: conditioning under inhomogeneous conductances.

Primary metric: kappa of the log-parametrised Jacobian dLambda/d(ln g_e) =
g_e dLambda/dg_e (relative perturbations). The unscaled kappa is stored too.
Cases: mild disorder U[0.5,1.5], strong disorder log-uniform [0.1,10] (5 seeds
each), and a x100 / x0.01 defect on all edges of one interior node at maximal
depth (first by index). Float64; SINGULAR rule as in v1.0.

Outputs: data/disorder.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, build_triangular_disk, depths, harmonic_extension,
)

OUT = Path(__file__).resolve().parent / "data" / "disorder.json"
EPS = np.finfo(float).eps
SEEDS = range(5)


def kappa_pair(g, gvals):
    """(log10 kappa of log-parametrised J, log10 kappa of unscaled J); None if SINGULAR."""
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    H, _ = harmonic_extension(n, edges, gvals, bnd)
    m = len(bnd)
    iu = np.triu_indices(m, k=1)
    cols = []
    for a, b in edges:
        d = H[a] - H[b]
        cols.append(np.outer(d, d)[iu])
    J = np.stack(cols, axis=1)
    out = []
    for M in (J * gvals[None, :], J):
        s = np.linalg.svd(M, compute_uv=False)
        out.append(None if s[-1] <= s[0] * EPS else math.log10(s[0] / s[-1]))
    return out


def defect_g(g, factor):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    d = depths(g, bnd)
    interior = np.setdiff1d(np.arange(n), bnd)
    v = int(interior[np.argmax(d[interior])])  # first index at maximal depth
    gv = np.ones(len(edges))
    for e, (a, b) in enumerate(edges):
        if v in (a, b):
            gv[e] = factor
    return gv, v, int(d[v])


def main() -> int:
    graphs = [("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)),
              ("triangular R=6.45", build_triangular_disk(6.45)),
              ("{7,3} L=3", build_hyperbolic(7, 3, 3)), ("square R=10", build_square_disk(10))]
    rows = []
    for name, g in graphs:
        E = len(g["edges"])
        rows.append({"graph": name, "N": len(g["nodes"]), "regime": "unit", "seed": None,
                     "log10_kappa_log": kappa_pair(g, np.ones(E))[0], "log10_kappa_raw": kappa_pair(g, np.ones(E))[1]})
        for regime, sampler in (("U[0.5,1.5]", lambda r, E=E: r.uniform(0.5, 1.5, E)),
                                ("logU[0.1,10]", lambda r, E=E: 10 ** r.uniform(-1, 1, E))):
            for s in SEEDS:
                kl, kr = kappa_pair(g, sampler(np.random.default_rng(s)))
                rows.append({"graph": name, "N": len(g["nodes"]), "regime": regime, "seed": s,
                             "log10_kappa_log": kl, "log10_kappa_raw": kr})
        for factor in (100.0, 0.01):
            gv, v, dv = defect_g(g, factor)
            kl, kr = kappa_pair(g, gv)
            rows.append({"graph": name, "N": len(g["nodes"]), "regime": f"defect x{factor:g}", "seed": None,
                         "defect_node": v, "defect_depth": dv, "log10_kappa_log": kl, "log10_kappa_raw": kr})
        print(f"  {name} done", flush=True)

    def med(name, regime):
        v = [r["log10_kappa_log"] for r in rows if r["graph"] == name and r["regime"] == regime]
        return None if any(x is None for x in v) else float(np.median(v))

    summary = {}
    for regime in ("unit", "U[0.5,1.5]", "logU[0.1,10]", "defect x100", "defect x0.01"):
        summary[regime] = {n: med(n, regime) for n, _ in graphs}
        gap112 = None if None in (summary[regime]["{7,3} L=2"], summary[regime]["square R=6"]) else \
            summary[regime]["square R=6"] - summary[regime]["{7,3} L=2"]
        gap316 = None if None in (summary[regime]["{7,3} L=3"], summary[regime]["square R=10"]) else \
            summary[regime]["square R=10"] - summary[regime]["{7,3} L=3"]
        summary[regime]["gap_N112"] = gap112
        summary[regime]["gap_N316"] = gap316
        f = lambda x: "SING." if x is None else f"{x:.2f}"
        print(f"  {regime:13} hyp L2={f(summary[regime]['{7,3} L=2'])} sq R6={f(summary[regime]['square R=6'])} "
              f"gap={f(gap112)} | hyp L3={f(summary[regime]['{7,3} L=3'])} sq R10={f(summary[regime]['square R=10'])} gap={f(gap316)}")
    OUT.write_text(json.dumps({"rows": rows, "summary_median_logparam": summary}, indent=1))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
