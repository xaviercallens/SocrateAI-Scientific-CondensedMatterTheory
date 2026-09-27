#!/usr/bin/env python3
"""Part B of the PoC (see PREREGISTRATION.md): does the exact-degeneracy rate
of the Majorana SYK ground state depend on N mod 8?

Motivated by, but NOT derived from: Fidkowski-Kitaev (arXiv:0904.2197, corpus)
-- free Majorana chain's Z invariant collapses to Z8 under interactions --
and You-Ludwig-Xu (arXiv:1602.06964, corpus) -- SYK's level statistics cycle
through the three Wigner-Dyson classes with a period tied to a topological
index. This script does not attempt to identify the symmetry operator behind
either result; it only tests, empirically, whether an exact (to floating
precision) ground-state degeneracy appears more often at N = 12, 20 (N mod 8
= 4) than at N = 8, 16, 24 (N mod 8 = 0).

Method, to keep this correct and fast up to N=24 (dim 2^12=4096):
  - Represent each Majorana gamma_i (i = 0..N-1) as a SIGNED PERMUTATION of
    the computational basis of N/2 qubits (Jordan-Wigner), not a dense
    matrix: gamma_i |k> = phase_i[k] * |perm_i[k]>. A Pauli string has
    exactly one nonzero entry per row, so this is O(dim) per operator instead
    of O(dim^2).
  - A product of 4 distinct Majoranas composes to another signed permutation
    in O(dim) (function composition), and H is assembled by scatter-adding
    each term's O(dim) contribution into one dense (dim x dim) matrix, which
    is then diagonalized once with a standard dense eigensolver.
  - `--self-test` checks this construction against a brute-force dense
    Kronecker-product build on N=4 (dim 4), and checks {gamma_i, gamma_j} =
    2*delta_ij and [H, P] = 0 (P = total fermion parity) numerically, before
    any physics run is trusted.

Output: experiments/poc_entanglement_tda/data/syk.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "data" / "syk.json"
RNG_SEED = 20260927  # fixed, so a rerun reproduces the same disorder draws
DEGENERACY_REL_TOL = 1e-8  # gap / energy_scale below this => "degenerate"


def majorana_operator(i: int, nq: int) -> tuple[np.ndarray, np.ndarray]:
    """(perm, phase) for gamma_i on nq qubits (dim = 2**nq), JW convention:
    gamma_{2q}   = (prod_{j<q} Z_j) X_q
    gamma_{2q+1} = (prod_{j<q} Z_j) Y_q
    Qubit q is bit q of the basis index (q=0 least significant).
    """
    dim = 1 << nq
    k = np.arange(dim, dtype=np.int64)
    q, is_y = divmod(i, 2)
    mask_lower = (1 << q) - 1  # bits 0..q-1
    if hasattr(np, "bitwise_count"):
        popcount = np.bitwise_count(k & mask_lower).astype(np.int64)  # unsigned by
    else:                                                              # default: cast
        popcount = np.array([bin(x).count("1") for x in (k & mask_lower)], dtype=np.int64)
    z_sign = 1 - 2 * (popcount & 1)
    bit_q = (k >> q) & 1
    perm = k ^ (1 << q)
    if is_y:
        phase = z_sign * (1j * (1 - 2 * bit_q))
    else:
        phase = z_sign.astype(np.complex128)
    return perm, phase.astype(np.complex128)


def compose(perm_a, phase_a, perm_b, phase_b):
    """Operator "B after A": (BA)|k> = phase_a[k]*phase_b[perm_a[k]] * |perm_b[perm_a[k]]>."""
    return perm_b[perm_a], phase_a * phase_b[perm_a]


def parity_operator(nq: int) -> tuple[np.ndarray, np.ndarray]:
    """P = product_q Z_q (diagonal, +-1)."""
    dim = 1 << nq
    k = np.arange(dim, dtype=np.int64)
    if hasattr(np, "bitwise_count"):
        popcount = np.bitwise_count(k).astype(np.int64)
    else:
        popcount = np.array([bin(x).count("1") for x in k], dtype=np.int64)
    sign = 1 - 2 * (popcount & 1)
    return k, sign.astype(np.complex128)


def build_hamiltonian(N: int, couplings: dict[tuple, float]) -> np.ndarray:
    nq = N // 2
    dim = 1 << nq
    gammas = [majorana_operator(i, nq) for i in range(N)]
    h = np.zeros((dim, dim), dtype=np.complex128)
    cols = np.arange(dim)
    for (i, j, k, l), jval in couplings.items():
        perm, phase = gammas[i]
        for g in (gammas[j], gammas[k], gammas[l]):
            perm, phase = compose(perm, phase, g[0], g[1])
        h[perm, cols] += jval * phase
    return h


def self_test() -> int:
    failures = []

    def check(ok, label):
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failures.append(label)

    # 1. Brute-force dense build for N=4 (nq=2), compare to the fast construction.
    nq = 2
    dim = 1 << nq
    I2, X, Y, Z = np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])

    def kron_list(mats):
        out = mats[0]
        for m in mats[1:]:
            out = np.kron(out, m)
        return out

    # Qubit q is bit q of k (q=0 is the LSB). np.kron(A, B)'s LEFT factor is the
    # more-significant one, so with 2 qubits the kron order is (qubit1, qubit0).
    brute = [
        kron_list([I2, X]),      # gamma_0 = X_0
        kron_list([I2, Y]),      # gamma_1 = Y_0
        kron_list([X, Z]),       # gamma_2 = Z_0 X_1
        kron_list([Y, Z]),       # gamma_3 = Z_0 Y_1
    ]
    for idx in range(4):
        perm, phase = majorana_operator(idx, nq)
        fast = np.zeros((dim, dim), dtype=np.complex128)
        fast[perm, np.arange(dim)] = phase
        check(np.allclose(fast, brute[idx]), f"gamma_{idx} matches brute-force dense JW build")

    # 2. Anticommutation {gamma_i, gamma_j} = 2 delta_ij, for N=6 (nq=3).
    nq = 3
    N = 6
    dim = 1 << nq
    mats = []
    for idx in range(N):
        perm, phase = majorana_operator(idx, nq)
        m = np.zeros((dim, dim), dtype=np.complex128)
        m[perm, np.arange(dim)] = phase
        mats.append(m)
    ok = True
    for a, b in itertools.combinations_with_replacement(range(N), 2):
        anticomm = mats[a] @ mats[b] + mats[b] @ mats[a]
        expected = 2 * np.eye(dim) if a == b else np.zeros((dim, dim))
        if not np.allclose(anticomm, expected, atol=1e-10):
            ok = False
    check(ok, f"{{gamma_i, gamma_j}} = 2*delta_ij for all pairs, N={N}")
    check(all(np.allclose(m, m.conj().T) for m in mats), "each gamma_i is Hermitian")

    # 3. [H, P] = 0 for a random small SYK instance, and H is Hermitian.
    rng = np.random.default_rng(0)
    N = 8
    quads = list(itertools.combinations(range(N), 4))
    js = {q: float(rng.normal(0, 1.0)) for q in quads}
    h = build_hamiltonian(N, js)
    check(np.allclose(h, h.conj().T, atol=1e-9), f"H is Hermitian, N={N}")
    _, p_phase = parity_operator(N // 2)
    p = np.diag(p_phase)
    commutator = h @ p - p @ h
    check(np.allclose(commutator, 0, atol=1e-8), f"[H, P] = 0, N={N}")

    print(f"\n{'PASS' if not failures else f'FAILED ({len(failures)})'}")
    return 0 if not failures else 1


def draw_couplings(N: int, rng: np.random.Generator) -> dict[tuple, float]:
    """J_{ijkl}, i<j<k<l, Gaussian, variance 3!*J^2/N^3 (Maldacena-Stanford
    1604.07818 normalization, J=1 as the unit of energy). This is a Tier X
    numeric run: the qualitative question (does an exact degeneracy appear)
    does not depend on this normalization choice, only the energy scale used
    to set the degeneracy threshold does, and that scale is measured from the
    realized spectrum itself (see main()), not assumed from this variance.
    """
    variance = 6.0 / N**3
    quads = list(itertools.combinations(range(N), 4))
    return {q: float(rng.normal(0.0, np.sqrt(variance))) for q in quads}


def entanglement_spectrum_from_state(psi: np.ndarray, nq: int) -> np.ndarray:
    """Bipartition into the first nq//2 qubits (A) and the rest (B); exact
    reduced-density-matrix spectrum via SVD of the reshaped state vector.
    Requires nq even (N % 4 == 0).
    """
    n_a = nq // 2
    n_b = nq - n_a
    mat = psi.reshape(1 << n_a, 1 << n_b)
    singular_values = np.linalg.svd(mat, compute_uv=False)
    probs = singular_values**2
    probs = probs[probs > 0]
    return probs / probs.sum()


def run_one(N: int, seed: int) -> dict:
    nq = N // 2
    rng = np.random.default_rng(seed)
    couplings = draw_couplings(N, rng)
    h = build_hamiltonian(N, couplings)
    energies, vectors = np.linalg.eigh(h)
    energies = energies.real
    energy_scale = float(np.std(energies))

    _, p_phase = parity_operator(nq)
    # <psi_a | P | psi_a> for the lowest few states, to find each one's parity.
    parities = np.real(np.einsum("ka,k,ka->a", vectors[:, :8].conj(), p_phase, vectors[:, :8]))

    ground_parity = 1 if parities[0] > 0 else -1
    same_sector = [0]
    for a in range(1, len(parities)):
        if (parities[a] > 0) == (ground_parity > 0):
            same_sector.append(a)
        if len(same_sector) >= 2:
            break
    gap = float(energies[same_sector[1]] - energies[same_sector[0]]) if len(same_sector) >= 2 else float("nan")
    degenerate = bool(gap / energy_scale < DEGENERACY_REL_TOL) if energy_scale > 0 else False

    result = {
        "N": N, "seed": seed, "energy_scale": energy_scale,
        "ground_parity_purity": float(abs(parities[0])),  # should be ~1.0 (clean parity eigenstate)
        "same_sector_gap": gap, "gap_over_scale": gap / energy_scale if energy_scale > 0 else None,
        "degenerate": degenerate,
        "lowest_6_energies": energies[:6].tolist(),
    }
    if not degenerate:
        ent = entanglement_spectrum_from_state(vectors[:, 0], nq)
        result["entanglement_entropy"] = float(-np.sum(ent * np.log(ent)))
    else:
        result["entanglement_entropy"] = None
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--realizations", type=int, default=40)
    parser.add_argument("--N", type=int, nargs="*", default=[8, 12, 16, 20, 24])
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    rng = np.random.default_rng(RNG_SEED)
    results = []
    for N in args.N:
        if N % 4 != 0:
            print(f"skip N={N}: needs N % 4 == 0 for an even qubit bipartition")
            continue
        t0 = time.time()
        seeds = [int(rng.integers(0, 2**31 - 1)) for _ in range(args.realizations)]
        rows = [run_one(N, s) for s in seeds]
        n_degenerate = sum(r["degenerate"] for r in rows)
        results.append({
            "N": N, "N_mod_8": N % 8, "n_realizations": len(rows),
            "n_degenerate": n_degenerate,
            "degenerate_fraction": n_degenerate / len(rows),
            "realizations": rows,
        })
        print(f"  N={N:3d} (mod8={N % 8}): {n_degenerate}/{len(rows)} degenerate, "
              f"{time.time() - t0:.1f}s")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")

    print("\nsummary: degenerate fraction by N mod 8")
    for row in results:
        print(f"  N={row['N']:3d}  mod8={row['N_mod_8']}  fraction={row['degenerate_fraction']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
