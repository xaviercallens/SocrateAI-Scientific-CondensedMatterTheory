#!/usr/bin/env python3
"""PREREGISTRATION_11.md: log10 kappa of the DtN sensitivity Jacobian across {p,q} tilings, via the
closed-form Gram matrix (float64). Outputs data/tilings_kappa.json."""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, build_triangular_disk, degrees, depths, harmonic_extension,
)

OUT = Path(__file__).resolve().parent / "data" / "tilings_kappa.json"
FAMILIES = [((7, 3), range(1, 5)), ((8, 3), range(1, 5)), ((5, 4), range(1, 6)), ((6, 4), range(1, 5)), ((4, 5), range(1, 7))]
RES_TOL = 1e-13


def log10_kappa_gram(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)   # n x m
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    D = (H[ea] - H[eb]).T                                          # m x E
    M1 = D.T @ D
    M2 = (D ** 2).T @ (D ** 2)
    G = 0.5 * (M1 ** 2 - M2)
    ev = np.linalg.eigvalsh((G + G.T) / 2)
    lmin, lmax = float(ev[0]), float(ev[-1])
    if lmin <= RES_TOL * lmax:
        return None, lmin, lmax
    return 0.5 * math.log10(lmax / lmin), lmin, lmax


def record(name, g, q=None):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    interior = np.setdiff1d(np.arange(n), bnd)
    deg_ok = None if q is None else bool(np.all(degrees(n, edges)[interior] == q))
    t0 = time.time()
    lk, lmin, lmax = log10_kappa_gram(g)
    err = None if lk is None else float(0.5 * np.finfo(float).eps * (lmax / lmin) / math.log(10))
    row = {"name": name, "N": n, "E": len(edges), "boundary": int(len(bnd)),
           "d_max": int(depths(g, bnd).max()), "interior_degree_q": deg_ok,
           "log10_kappa": lk, "log10_kappa_error_bound": err, "lambda_min": lmin, "lambda_max": lmax,
           "seconds": round(time.time() - t0, 1)}
    print(f"  {name:12} N={n:5d} E={len(edges):5d} m={len(bnd):5d} d_max={row['d_max']:2d} "
          f"deg_ok={deg_ok} log10k={'UNRESOLVED' if lk is None else format(lk, '.4f')} ({row['seconds']}s)", flush=True)
    return row


def main():
    rows = []
    # controls first (v1.0 direct-SVD values)
    h0 = {r["name"]: r["log10_kappa"] for r in json.loads((OUT.parent / "h0.json").read_text())}
    ctrl = []
    for name, g, ref in (("{7,3} L=3", build_hyperbolic(7, 3, 3), h0["{7,3} L=3"]),
                         ("square R=6", build_square_disk(6), h0["square R=6"])):
        r = record(name + " (control)", g)
        r["v1_direct_svd"] = ref
        # Deviation 1 of PREREGISTRATION_11.md: Gram squares the condition number, so allow the float64 floor
        tol = max(1e-6, 10 * np.finfo(float).eps * 10 ** (2 * ref))
        r["control_tolerance"] = tol
        r["control_tolerance"] = float(tol)
        r["control_pass"] = bool(r["log10_kappa"] is not None and abs(r["log10_kappa"] - ref) < tol)
        ctrl.append(r)
        print(f"     control vs direct SVD {ref:.6f}: |diff| = {abs(r['log10_kappa'] - ref):.1e}, tol {tol:.1e}: "
              f"{'pass' if r['control_pass'] else 'FAIL'}")
    OUT.write_text(json.dumps({"controls": ctrl, "rows": rows}, indent=1))
    if not all(c["control_pass"] for c in ctrl):
        print("control failed: no tiling results reported"); return 1
    for (p, q), Ls in FAMILIES:
        for L in Ls:
            g = build_hyperbolic(p, q, L)
            if len(g["nodes"]) > 3500:
                print(f"  {{{p},{q}}} L={L}: N={len(g['nodes'])} > 3500, skipped"); break
            rows.append({**record(f"{{{p},{q}}} L={L}", g, q), "p": p, "q": q, "L": L})
            OUT.write_text(json.dumps({"controls": ctrl, "rows": rows}, indent=1))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
