#!/usr/bin/env python3
"""PREREGISTRATION_14.md: row-subset exact rank certificates over two finite fields for other {p,q} tilings.
Writes data/exact_rank_certificates_for_other_tiling.json; score() returns verdicts from the file alone."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic  # noqa: E402
from hyperbolic_exact import PRIMES, laplacian_int, mat_inv_mod, rank_mod  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "exact_rank_certificates_for_other_tiling.json"
INSTANCES = [(7, 3, 2), (7, 3, 3), (8, 3, 2), (8, 3, 3), (5, 4, 3), (5, 4, 4), (5, 4, 5), (6, 4, 2), (6, 4, 3),
             (4, 5, 4), (4, 5, 5), (4, 5, 6)]
E_MAX = 1700


def harmonic_mod(n, edges, bnd, p):
    L = laplacian_int(n, edges)
    interior = np.setdiff1d(np.arange(n), bnd)
    inv = mat_inv_mod(L[np.ix_(interior, interior)] % p, p)
    if inv is None:
        return None
    Lib = L[np.ix_(interior, bnd)]            # signed entries in {-1, 0}: products stay below p, no overflow
    H = np.zeros((n, len(bnd)), dtype=np.int64)
    H[bnd, :] = np.eye(len(bnd), dtype=np.int64)
    H[interior, :] = (-(inv @ Lib)) % p
    return H


def matmul_mod(A, B, p):
    """(A @ B) mod p for int64 matrices with entries in [0, p), p < 2^31: accumulate one rank-1 term at a time so
    no intermediate exceeds 2^63."""
    out = np.zeros((A.shape[0], B.shape[1]), dtype=np.int64)
    for i in range(A.shape[1]):
        out = (out + (A[:, i:i + 1] * B[i:i + 1, :]) % p) % p
    return out


def sketch_rank(n, edges, bnd, p, k, seed):
    """Rank over GF(p) of R J, where row s of R has coefficients c_ij = u_i v_j + u_j v_i (i < j) for random u, v.
    Since R J is a row combination of J, rank_p(R J) = E certifies full column rank of J (and, by
    rank_Q >= rank_p, of the real Jacobian). Computed without forming J:
    (R J)[s, e] = (u_s . d_e)(v_s . d_e) - sum_i u_si v_si d_e,i^2."""
    H = harmonic_mod(n, edges, bnd, p)
    if H is None:
        return None
    m = len(bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    D = ((H[ea] - H[eb]) % p).T.copy()                          # m x E
    rng = np.random.default_rng(seed)
    U = rng.integers(0, p, size=(k, m), dtype=np.int64)
    V = rng.integers(0, p, size=(k, m), dtype=np.int64)
    A = matmul_mod(U, D, p)
    B = matmul_mod(V, D, p)
    C = matmul_mod((U * V) % p, (D * D) % p, p)
    RJ = ((A * B) % p - C) % p                                  # k x E
    return int(rank_mod(RJ, p)), int(k), int(m * (m - 1) // 2)


subset_rank = sketch_rank  # name used by the preregistration text and the unit check


def run() -> dict:
    rows = []
    for (pp, q, L) in INSTANCES:
        g = build_hyperbolic(pp, q, L)
        n, edges = len(g["nodes"]), g["edges"]
        E = len(edges)
        if E > E_MAX:
            continue
        bnd = boundary_nodes(g)
        row = {"tiling": "{%d,%d}" % (pp, q), "L": L, "N": n, "E": E, "boundary": int(len(bnd)), "primes": {}}
        t0 = time.time()
        for p in PRIMES:
            r = sketch_rank(n, edges, bnd, p, E + 20, 14)
            redraw = False
            if r is not None and r[0] < E:
                r = sketch_rank(n, edges, bnd, p, 2 * E, 15); redraw = True
            row["primes"][str(p)] = None if r is None else {"rank": r[0], "rows_used": r[1], "rows_total": r[2],
                                                            "redraw_4E": redraw, "certified_full": r[0] == E}
        row["certified_full_both"] = all(v is not None and v["certified_full"] for v in row["primes"].values())
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        print("  {%d,%d} L=%d E=%4d  %s  certified=%s (%.0fs)" % (pp, q, L, E, " ".join(
            "p%d:%s" % (i, "Linv-singular" if v is None else "%d/%d" % (v["rank"], E)) for i, v in enumerate(row["primes"].values())),
            row["certified_full_both"], row["seconds"]), flush=True)
    return {"primes": list(PRIMES), "method": "random row combinations c_ij = u_i v_j + u_j v_i, k = E+20 (seed 14), redraw k = 2E (seed 15)",
            "rows": rows}


def score(d: dict) -> dict:
    rows = d["rows"]
    ctrl = next(r for r in rows if r["tiling"] == "{7,3}" and r["L"] == 2)
    G1 = ctrl["certified_full_both"]
    G2 = all(v is not None for r in rows for v in r["primes"].values())
    test = [r for r in rows if not (r["tiling"] == "{7,3}" and r["L"] == 2)]
    P1 = all(r["certified_full_both"] for r in test)
    P2 = not any(v and v["redraw_4E"] for r in test for v in r["primes"].values())
    return {"G1": G1, "G2": G2, "P1": P1, "P2": P2, "n_instances": len(test),
            "not_certified": ["%s L=%d" % (r["tiling"], r["L"]) for r in test if not r["certified_full_both"]]}


def main() -> int:
    d = run()
    d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"])
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
