#!/usr/bin/env python3
"""PREREGISTRATION_3.md part A: the flat-lattice condition number beyond
double precision, in Arb ball arithmetic (python-flint).

Why float64 fails: kappa(J) ~ 1e16+ means sigma_min is below the rounding of
J's own entries. Why this works: the harmonic extension and the Gram matrix
G = J^T J are formed at 512-bit precision from the INTEGER Laplacian, then
G^-1 is computed in Arb (certified error radii); lambda_max(G^-1) is a
well-conditioned quantity and is read off in float64 after casting the
midpoints. J itself is never materialised: with d_e = h_a - h_b on the
boundary and J rows indexed by boundary pairs i<j,
    G_ef = sum_{i<j} d_e,i d_e,j d_f,i d_f,j = 1/2 [ (d_e . d_f)^2 - (d_e^2 . d_f^2) ].

Every reported value carries the maximal relative radius of G^-1; a run whose
radius exceeds 1e-20 is repeated at double precision (bits), never reported.

Order: two unsaturated controls (must match float64 to 1e-6 in log10 kappa),
then the float64-singular instances. Results are appended to
data/flat_scaling_mp.json as each case finishes (resume-safe).
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from flint import arb, arb_mat, ctx, fmpz_mat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_square_disk, build_triangular_disk, laplacian,
)

OUT = Path(__file__).resolve().parent / "data" / "flat_scaling_mp.json"
RAD_TOL = 1e-20
CASES = [  # (name, builder, float64 reference log10 kappa from h0.json or None)
    ("square R=10 (control)", lambda: build_square_disk(10), "square R=10"),
    ("triangular R=6.45 (control)", lambda: build_triangular_disk(6.45), "triangular R=6.449999999999999"),
    ("triangular R=10.75", lambda: build_triangular_disk(10.75), "triangular R=10.75"),
    ("square R=16", lambda: build_square_disk(16), "square R=16"),
    ("triangular R=17.2", lambda: build_triangular_disk(17.2), "triangular R=17.2"),
]


def gram_arb(g, prec):
    ctx.prec = prec
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    interior = np.setdiff1d(np.arange(n), bnd)
    m, E = len(bnd), len(edges)
    L = laplacian(n, edges, np.ones(E)).astype(int)
    Lii = arb_mat(fmpz_mat(L[np.ix_(interior, interior)].tolist()))
    Lib = arb_mat(fmpz_mat(L[np.ix_(interior, bnd)].tolist()))
    Hi = Lii.solve(Lib)  # = L_ii^-1 L_ib ; harmonic extension is -Hi
    pos_b = {int(v): k for k, v in enumerate(bnd)}
    pos_i = {int(v): k for k, v in enumerate(interior)}
    zero = arb(0)

    def hrow(v):
        if v in pos_b:
            return [arb(1) if k == pos_b[v] else zero for k in range(m)]
        r = pos_i[v]
        return [-Hi[r, k] for k in range(m)]

    D = [[zero] * E for _ in range(m)]  # m x E, column e = h_a - h_b
    for e, (a, b) in enumerate(edges):
        ha, hb = hrow(int(a)), hrow(int(b))
        for k in range(m):
            D[k][e] = ha[k] - hb[k]
    Dm = arb_mat(D)
    D2 = arb_mat([[x * x for x in row] for row in D])
    M1 = Dm.transpose() * Dm
    M2 = D2.transpose() * D2
    half = arb(1) / 2
    G = arb_mat([[half * (M1[i, j] * M1[i, j] - M2[i, j]) for j in range(E)] for i in range(E)])
    return G, E, m


def kappa_from_gram(G, E):
    Ginv = G.inv()
    mid = np.empty((E, E)); rel = 0.0
    for i in range(E):
        for j in range(E):
            x = Ginv[i, j]
            mv = float(x.mid()); mid[i, j] = mv
            r = float(x.rad())
            if mv != 0.0:
                rel = max(rel, r / abs(mv))
    mid = (mid + mid.T) / 2
    lam_max_inv = float(np.linalg.eigvalsh(mid)[-1])
    Gf = np.array([[float(G[i, j].mid()) for j in range(E)] for i in range(E)])
    lam_max = float(np.linalg.eigvalsh((Gf + Gf.T) / 2)[-1])
    lam_min = 1.0 / lam_max_inv
    return math.log10(math.sqrt(lam_max / lam_min)), rel, lam_max, lam_min


def main() -> int:
    ref = {r["name"]: r for r in json.loads((OUT.parent / "h0.json").read_text())}
    rows = json.loads(OUT.read_text()) if OUT.exists() else []
    done = {r["case"] for r in rows}
    for name, build, refname in CASES:
        if name in done:
            print(f"  skip {name} (done)"); continue
        g = build()
        prec = 512
        while True:
            t0 = time.time()
            G, E, m = gram_arb(g, prec)
            lk, rel, lmax, lmin = kappa_from_gram(G, E)
            dt = time.time() - t0
            if rel <= RAD_TOL:
                break
            print(f"  {name}: max rel radius {rel:.1e} > {RAD_TOL} at {prec} bits; doubling")
            prec *= 2
        f64 = ref.get(refname, {}).get("log10_kappa")
        row = {"case": name, "N": len(g["nodes"]), "E": E, "boundary": m, "prec_bits": prec,
               "log10_kappa_arb": lk, "max_rel_radius_Ginv": rel, "lambda_max_G": lmax, "lambda_min_G": lmin,
               "float64_log10_kappa": f64, "control_pass": (abs(lk - f64) < 1e-6) if f64 is not None else None,
               "seconds": round(dt, 1)}
        rows.append(row)
        OUT.write_text(json.dumps(rows, indent=1))
        ctrl = "" if f64 is None else f"  float64={f64:.6f} control={'pass' if row['control_pass'] else 'FAIL'}"
        print(f"  {name:28} N={row['N']:5d} E={E:5d}  log10 kappa = {lk:.4f}  (radius {rel:.1e}, {prec} bits, {dt:.0f}s){ctrl}",
              flush=True)
        if row["control_pass"] is False:
            print("  control failed: stopping before any saturated case"); return 1
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
