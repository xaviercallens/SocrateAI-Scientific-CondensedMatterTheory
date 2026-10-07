#!/usr/bin/env python3
"""PREREGISTRATION_2.md parts A and B.

A. Probe-matched control. The hyperbolic tiling has proportionally many more
   boundary probes than a flat disk of equal N. Here its boundary is
   subsampled to exactly the flat disk's probe count (probes evenly spaced in
   angle); the unused boundary nodes are reclassified as interior, i.e.
   zero-current nodes -- the correct model of an unconnected electrode --
   and the exact Jacobian is recomputed.

B. Neumann-to-Dirichlet map. Hardware that injects currents and reads
   voltages measures Lambda^+ (Moore-Penrose inverse, which is the inverse on
   the zero-sum subspace), whose Jacobian is -Lambda^+ (dLambda/dg_e) Lambda^+.

Outputs: data/probe_matched.json
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    build_hyperbolic, build_square_disk, boundary_nodes, dtn, harmonic_extension,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "probe_matched.json"
EPS = np.finfo(float).eps


def jacobian_matrices(n, edges, probes):
    """List of dLambda/dg_e as full (m x m) matrices, via the exact formula."""
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), probes)
    return [np.outer(H[a] - H[b], H[a] - H[b]) for a, b in edges]


def kappa_of(mats):
    m = mats[0].shape[0]
    iu = np.triu_indices(m, k=1)
    J = np.stack([M[iu] for M in mats], axis=1)
    s = np.linalg.svd(J, compute_uv=False)
    if s.min() <= s.max() * EPS:
        return None
    return math.log10(s.max() / s.min())


def analyse(name, g, probes):
    n = len(g["nodes"])
    edges = g["edges"]
    mats = jacobian_matrices(n, edges, probes)
    lam = dtn(n, edges, np.ones(len(edges)), probes)
    lam_pinv = np.linalg.pinv(lam, rcond=1e-12)
    ntd_mats = [-(lam_pinv @ M @ lam_pinv) for M in mats]
    return {
        "name": name, "N": n, "E": len(edges), "probes": int(len(probes)),
        "log10_kappa_DtN": kappa_of(mats),
        "log10_kappa_NtD": kappa_of(ntd_mats),
    }


def subsample_by_angle(g, bnd, k):
    """k boundary nodes evenly spaced in polar angle around the disk."""
    ang = np.angle(g["nodes"][bnd])
    order = bnd[np.argsort(ang)]
    idx = np.round(np.linspace(0, len(order), k, endpoint=False)).astype(int)
    return np.sort(order[idx])


def main() -> int:
    results = []
    pairs = [(2, 6), (3, 10)]  # hyperbolic layer, square radius (N=113, N=317)
    for L, R in pairs:
        gh = build_hyperbolic(7, 3, L)
        gs = build_square_disk(R)
        bh, bs = boundary_nodes(gh), boundary_nodes(gs)
        full = analyse(f"{{7,3}} L={L} full boundary", gh, bh)
        matched = analyse(f"{{7,3}} L={L} subsampled to {len(bs)} probes", gh,
                          subsample_by_angle(gh, bh, len(bs)))
        flat = analyse(f"square R={R}", gs, bs)
        for r in (full, matched, flat):
            results.append(r)
            k1 = "SINGULAR" if r["log10_kappa_DtN"] is None else f"{r['log10_kappa_DtN']:.2f}"
            k2 = "SINGULAR" if r["log10_kappa_NtD"] is None else f"{r['log10_kappa_NtD']:.2f}"
            print(f"  {r['name']:40} N={r['N']:4d} probes={r['probes']:4d} "
                  f"log10k DtN={k1:>8}  NtD={k2:>8}")
        if matched["log10_kappa_DtN"] is not None and flat["log10_kappa_DtN"] is not None:
            gap = flat["log10_kappa_DtN"] - matched["log10_kappa_DtN"]
            print(f"  -> probe-matched DtN gap at N~{flat['N']}: {gap:.2f} decades\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
