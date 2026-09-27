#!/usr/bin/env python3
"""Numerical witness for the SSH statements used as the Lean T2 target.

A Lean proof locks a *statement*. If the statement is false, the proof attempt
fails -- or, worse, someone weakens the statement until it compiles. So the
exact statement is checked numerically here first, and this script is the
first artifact of axis 1.

It checks four claims, and exits non-zero if any fails:

  1. Winding number of z -> v + w z on the COUNTERCLOCKWISE unit circle (the
     orientation of Mathlib's circleIntegral) is 0 for |v|>|w| and **+1** for
     |w|>|v|. With the other common convention h(k) = v + w e^{-ik} the
     circle runs clockwise and the answer is -1. The sign is not cosmetic
     under a statement lock: proving a "-1" statement through circleIntegral
     would push someone to flip it.
  2. An open chain with an EVEN number of sites (2N) has **no exact zero mode**
     for v != 0: its sublattice block is bidiagonal with v on the diagonal, so
     det D = v^N. Edge modes of the topological phase sit at energy ~ (v/w)^N,
     exponentially small but not zero. "Number of exact zero modes = |nu|" is
     therefore FALSE for a finite even chain.
  3. An open chain with an ODD number of sites (2N+1) has **exactly one** exact
     zero mode, psi_A(n) ∝ (-v/w)^n, localised at the LEFT end iff |w|>|v|.
     This is the finite, exactly true statement suitable for Lean T2.
  4. Lowest |E| of the even chain decays like (v/w)^N in the topological phase,
     so the near-zero edge modes are real, just not exact.

Also prints the first Bragg-gap frequency for a given lattice period in deep
water, since the preregistration's excitation frequency must come from here and
not from a guess.

Usage:
    python3 experiments/axis1_topological_waves/ssh_check.py
"""

from __future__ import annotations

import math
import sys

import numpy as np


def winding_number(v: float, w: float, samples: int = 4096, sign: int = +1) -> int:
    """Winding of h = v + w e^{sign*ik} around 0, k from 0 to 2pi.

    sign=+1 traverses the unit circle z = e^{ik} counterclockwise -- the
    orientation of Mathlib's circleIntegral / circleMap, and the convention
    locked for Lean. sign=-1 is the e^{-ik} convention, which reverses it.
    """
    k = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    h = v + w * np.exp(sign * 1j * k)
    phase = np.unwrap(np.angle(np.append(h, h[0])))
    return int(round((phase[-1] - phase[0]) / (2.0 * math.pi)))


def open_chain(v: float, w: float, sites: int) -> np.ndarray:
    """Tight-binding SSH chain, sites A0 B0 A1 B1 ... ; intra v, inter w."""
    hamiltonian = np.zeros((sites, sites))
    for i in range(sites - 1):
        hopping = v if i % 2 == 0 else w
        hamiltonian[i, i + 1] = hamiltonian[i + 1, i] = hopping
    return hamiltonian


def zero_modes(v: float, w: float, sites: int, tol: float = 1e-10) -> tuple[int, np.ndarray]:
    energies, vectors = np.linalg.eigh(open_chain(v, w, sites))
    mask = np.abs(energies) < tol
    return int(mask.sum()), vectors[:, mask]


def sublattice_block(v: float, w: float, n_cells: int) -> np.ndarray:
    """The A<-B block D of an even chain, so that H = [[0, D], [D^T, 0]].

    Row n is A_n: it couples to B_n with v (diagonal) and to B_{n-1} with w
    (sub-diagonal). D is lower bidiagonal, hence det D = v^N exactly.
    """
    block = np.zeros((n_cells, n_cells))
    for n in range(n_cells):
        block[n, n] = v
        if n > 0:
            block[n, n - 1] = w
    return block


def bragg_frequency(period_m: float, g: float = 9.81) -> float:
    """First Bragg gap: k = pi / a, deep-water dispersion omega^2 = g k."""
    k = math.pi / period_m
    return math.sqrt(g * k) / (2.0 * math.pi)


def main() -> int:
    failures: list[str] = []

    def check(ok: bool, label: str) -> None:
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failures.append(label)

    print("1. winding number of z -> v + w z on the unit circle")
    print("   locked convention: counterclockwise (z = e^{ik}), as in Mathlib circleIntegral")
    check(winding_number(1.0, 0.5, sign=+1) == 0, "|v|>|w| -> nu = 0")
    check(winding_number(0.5, 1.0, sign=+1) == 1, "|w|>|v| -> nu = +1 (counterclockwise)")
    print("   other convention: h(k) = v + w e^{-ik} runs clockwise and flips the sign")
    check(winding_number(0.5, 1.0, sign=-1) == -1, "|w|>|v| -> -1 with e^{-ik}")

    print("2. even open chain (2N sites): no exact zero mode, because det D = v^N")
    # Tested on det D itself, not by counting eigenvalues under a tolerance: for
    # v=0.2, N=20 the edge energy is 0.2^20 ~ 1e-14, which a 1e-10 threshold
    # would misread as an exact zero. That is floating point, not physics.
    n_cells = 20
    for v, w in [(1.0, 0.5), (0.5, 1.0), (0.2, 1.0)]:
        det = float(np.linalg.det(sublattice_block(v, w, n_cells)))
        expected = v**n_cells
        check(
            det != 0.0 and math.isclose(det, expected, rel_tol=1e-9),
            f"v={v}, w={w}: det D = {det:.3e} = v^N = {expected:.3e}  (non-zero)",
        )

    print("3. odd open chain (2N+1 sites): exactly one zero mode")
    for v, w, side in [(0.5, 1.0, "left"), (1.0, 0.5, "right")]:
        n_zero, vectors = zero_modes(v, w, sites=41)
        check(n_zero == 1, f"v={v}, w={w}: {n_zero} zero mode(s)")
        if n_zero == 1:
            psi = np.abs(vectors[:, 0]) ** 2
            left, right = psi[: len(psi) // 2].sum(), psi[len(psi) // 2 :].sum()
            located = "left" if left > right else "right"
            check(located == side, f"  localised at the {located} end (expected {side})")
            amplitudes_a = vectors[0::2, 0]
            ratios = amplitudes_a[1:6] / amplitudes_a[:5]
            check(
                bool(np.allclose(ratios, -v / w, rtol=1e-6)),
                f"  psi_A(n+1)/psi_A(n) = {ratios[0]:+.4f} (expected -v/w = {-v / w:+.4f})",
            )

    print("4. even chain, topological phase: lowest |E| ~ (v/w)^N")
    v, w = 0.5, 1.0
    for n_cells in (10, 15, 20):
        energies = np.linalg.eigvalsh(open_chain(v, w, 2 * n_cells))
        lowest = float(np.min(np.abs(energies)))
        expected = (v / w) ** n_cells
        check(
            0.1 < lowest / expected < 10.0,
            f"N={n_cells}: min|E| = {lowest:.2e}, (v/w)^N = {expected:.2e}",
        )

    print("\nfirst Bragg gap, deep water (provisional excitation frequency)")
    for period_cm in (5.0, 8.0, 10.0):
        f = bragg_frequency(period_cm / 100.0)
        print(f"  period {period_cm:4.1f} cm -> f_Bragg = {f:.2f} Hz, lambda = {2 * period_cm:.0f} cm")

    print(f"\n{'PASS' if not failures else f'FAILED ({len(failures)})'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
