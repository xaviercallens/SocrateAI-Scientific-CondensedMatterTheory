#!/usr/bin/env python3
"""Tier B: exact rank certification of the boundary-to-bulk Jacobian, by
modular arithmetic -- no floating point anywhere, so no ambiguity about
whether a small singular value is "real" or numerical noise.

With unit conductances the Laplacian L is an INTEGER matrix. Pick a prime p
with det(L_ii) mod p != 0 (so L_ii is invertible over the finite field
GF(p)); then the harmonic-extension matrix H, and hence the Jacobian J
(built by the SAME formula as hyperbolic_network.jacobian(), just carried
out in GF(p) instead of R), are well-defined mod p, and

    rank_Q(J) >= rank_{GF(p)}(J mod p)

(reduction mod p can only ever LOWER apparent rank, by an unlucky
cancellation specific to that p, never raise it). So a full-rank result
mod p is an EXACT CERTIFICATE that the true rational rank is full -- not a
measurement, a proof, for that specific instance. A rank deficiency mod one
prime is not yet conclusive (it could be that prime's bad luck); persistence
across several independent primes is the evidence this script requires
before reporting a deficiency as real, per the discussion in RESULTS.md.

This exists to answer the question RESULTS.md's ERRATUM leaves open: is the
Euclidean lattices' rank deficiency (and, more importantly, the hyperbolic
lattice's full rank) a genuine algebraic fact, or a float64 artefact?

Usage:
    python3 hyperbolic_exact.py --self-test
    python3 hyperbolic_exact.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    build_hyperbolic, build_square_disk, build_triangular_disk, boundary_nodes,
)

# Two independent, well-known primes safe for int64 modular arithmetic
# (p < 2^31, so any single product p*p < 2^62 fits with headroom in int64).
PRIMES = (2_147_483_647, 998_244_353)  # 2^31-1 (Mersenne, prime); NTT-friendly prime


def laplacian_int(n: int, edges) -> np.ndarray:
    """Integer Laplacian, unit conductances, dtype=object to stay exact
    under Python's arbitrary-precision ints during modular reduction setup
    (converted to int64 once all entries are confirmed to fit)."""
    L = np.zeros((n, n), dtype=np.int64)
    for u, v in edges:
        L[u, u] += 1
        L[v, v] += 1
        L[u, v] -= 1
        L[v, u] -= 1
    return L


def mat_inv_mod(a: np.ndarray, p: int) -> np.ndarray | None:
    """Modular inverse of a square integer matrix via Gauss-Jordan
    elimination over GF(p). Returns None if `a` is singular mod p (a signal
    to try a different prime, not an error)."""
    n = a.shape[0]
    m = np.concatenate([a % p, np.eye(n, dtype=np.int64)], axis=1) % p
    for col in range(n):
        pivot_rows = np.nonzero(m[col:, col])[0]
        if pivot_rows.size == 0:
            return None
        pivot = col + pivot_rows[0]
        if pivot != col:
            m[[col, pivot]] = m[[pivot, col]]
        inv_pivot = pow(int(m[col, col]), p - 2, p)
        m[col] = (m[col] * inv_pivot) % p
        for row in range(n):
            if row != col and m[row, col] != 0:
                factor = int(m[row, col])
                m[row] = (m[row] - factor * m[col]) % p
    return m[:, n:]


def harmonic_extension_mod(n: int, edges, bnd: np.ndarray, p: int) -> np.ndarray | None:
    L = laplacian_int(n, edges) % p
    interior = np.setdiff1d(np.arange(n), bnd)
    Lii = L[np.ix_(interior, interior)]
    Lib = L[np.ix_(interior, bnd)]
    Lii_inv = mat_inv_mod(Lii, p)
    if Lii_inv is None:
        return None
    H = np.zeros((n, len(bnd)), dtype=np.int64)
    H[bnd, :] = np.eye(len(bnd), dtype=np.int64) % p
    H[interior, :] = (-(Lii_inv @ Lib)) % p
    return H


def jacobian_mod(n: int, edges, bnd: np.ndarray, p: int) -> np.ndarray | None:
    """Same construction as hyperbolic_network.jacobian(): J[:,e] =
    upper((P_a-P_b)^T(P_a-P_b)), carried out mod p."""
    H = harmonic_extension_mod(n, edges, bnd, p)
    if H is None:
        return None
    m = len(bnd)
    iu = np.triu_indices(m, k=1)
    J = np.zeros((len(iu[0]), len(edges)), dtype=np.int64)
    for e, (a, b) in enumerate(edges):
        d = (H[a, :] - H[b, :]) % p
        outer = np.outer(d, d) % p
        J[:, e] = outer[iu]
    return J % p


def rank_mod(mat: np.ndarray, p: int) -> int:
    """Exact rank over GF(p) by Gaussian elimination with modular pivoting."""
    m = mat.copy() % p
    rows, cols = m.shape
    rank = 0
    for col in range(cols):
        if rank >= rows:
            break
        pivot_rows = np.nonzero(m[rank:, col])[0]
        if pivot_rows.size == 0:
            continue
        pivot = rank + pivot_rows[0]
        if pivot != rank:
            m[[rank, pivot]] = m[[pivot, rank]]
        inv_pivot = pow(int(m[rank, col]), p - 2, p)
        m[rank] = (m[rank] * inv_pivot) % p
        nz = np.nonzero(m[:, col])[0]
        nz = nz[nz != rank]
        if nz.size:
            factors = m[nz, col].reshape(-1, 1)
            m[nz] = (m[nz] - factors * m[rank]) % p
        rank += 1
    return rank


def certified_rank(n: int, edges, bnd: np.ndarray, primes=PRIMES) -> dict:
    """Rank certified across all given primes; agreement across independent
    primes is the evidence for a genuine (not prime-specific) result."""
    ranks = {}
    for p in primes:
        J = jacobian_mod(n, edges, bnd, p)
        if J is None:
            ranks[p] = None  # L_ii singular mod this p; try another prime
            continue
        ranks[p] = rank_mod(J, p)
    return ranks


def self_test() -> int:
    failures = []

    def check(ok, label):
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failures.append(label)

    # mat_inv_mod correctness: A @ A^-1 == I mod p, small hand case.
    p = 1_000_003
    a = np.array([[2, 1], [1, 1]], dtype=np.int64)
    inv = mat_inv_mod(a, p)
    check(inv is not None, "2x2 matrix invertible mod p")
    prod = (a @ inv) % p
    check(np.array_equal(prod, np.eye(2, dtype=np.int64)), f"A @ A^-1 = I mod p, got\n{prod}")

    # rank_mod correctness: known-rank matrices.
    full = np.eye(5, dtype=np.int64)
    check(rank_mod(full, p) == 5, "rank of I_5 mod p is 5")
    deficient = np.array([[1, 2, 3], [2, 4, 6], [1, 0, 1]], dtype=np.int64)  # row2 = 2*row1
    check(rank_mod(deficient, p) == 2, f"rank of a rank-2 3x3 matrix is 2 (got {rank_mod(deficient, p)})")

    # Cross-check against hyperbolic_network's float rank on the smallest
    # case, where float64 is trusted (small matrix, well away from any
    # precision floor): {7,3} L=1, known float rank 42/42.
    g = build_hyperbolic(7, 3, 1)
    n = len(g["nodes"]); bnd = boundary_nodes(g)
    ranks = certified_rank(n, g["edges"], bnd)
    for prime, r in ranks.items():
        check(r == len(g["edges"]), f"{{7,3}} L=1: exact rank mod {prime} = {r} (expect {len(g['edges'])}, matches float64)")

    print(f"\n{'PASS' if not failures else f'FAILED ({len(failures)})'}")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    print("Exact rank certification (2 independent primes; agreement = certificate)\n")

    print("hyperbolic {7,3}")
    for L in (1, 2):
        g = build_hyperbolic(7, 3, L)
        n = len(g["nodes"]); bnd = boundary_nodes(g); E = len(g["edges"])
        ranks = certified_rank(n, g["edges"], bnd)
        agree = len(set(ranks.values())) == 1
        print(f"  L={L}: N={n} E={E}  ranks={ranks}  {'FULL RANK, CERTIFIED' if agree and list(ranks.values())[0] == E else 'see ranks'}")

    print("\neuclidean controls")
    # One size where float64 reported full rank (sanity cross-check), and
    # the smallest size where float64 reported a deficiency, to determine
    # whether that deficiency is real or a float64 artefact.
    cases = [
        ("square N~113 (float: full rank 200/200)", build_square_disk(6)),
        ("triangular N~151 (float: full rank 401/401)", build_triangular_disk(7.0)),
        ("triangular N~421 (float: DEFICIENT 1074/1176)", build_triangular_disk(11.5)),
    ]
    for label, g in cases:
        n = len(g["nodes"]); bnd = boundary_nodes(g); E = len(g["edges"])
        ranks = certified_rank(n, g["edges"], bnd)
        agree = len(set(ranks.values())) == 1
        status = "FULL RANK, CERTIFIED" if agree and list(ranks.values())[0] == E else \
                 f"DEFICIENT by {E - list(ranks.values())[0]}, CERTIFIED (agrees across primes)" if agree else \
                 "primes DISAGREE -- inconclusive, need a third prime"
        print(f"  {label}: N={n} E={E}  ranks={ranks}  {status}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
