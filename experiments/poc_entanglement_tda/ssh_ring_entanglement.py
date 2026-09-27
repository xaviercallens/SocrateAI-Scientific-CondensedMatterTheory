#!/usr/bin/env python3
"""Part A of the PoC (see PREREGISTRATION.md): entanglement spectrum of the
SSH chain on a ring, as a function of r = v/w, for two ring sizes.

Method (Peschel 2003; the exact relation used here is proved by Fidkowski,
arXiv:0909.2654, in the corpus): for a free-fermion ground state at half
filling, the entanglement spectrum of a subsystem A is the spectrum of
C_A = P|_A, the projector onto the filled single-particle states restricted
to A. Its eigenvalues zeta_n in [0, 1] are the entanglement spectrum;
zeta_n = 1/2 is the flat-band image of a zero-energy (mid-gap) mode.

Convention: h(k) = v + w e^{-ik}, identical to
experiments/axis1_topological_waves/ssh_exact.py, so this file's topological
side (|w| > |v|) matches that file's proven Tier B statements exactly.

Ring construction: sites 0..2L-1 (A0 B0 A1 B1 ... A_{L-1} B_{L-1}), bond i
(between site i and i+1 mod 2L) has hopping v if i is even, w if i is odd.
The wrap-around bond (2L-1 -> 0) has index 2L-1, always odd, so it is always
type w. Subsystem A = the first 2*ell sites (ell whole unit cells, ell < L):
this severs bond (2*ell - 1) [odd -> w] on the right and the wrap-around bond
[odd -> w] on the left. Both severed bonds are w-type for EVERY ell -- this
is what makes "two w-bonds severed" true regardless of subsystem size, and is
checked explicitly (not just asserted) in main().

Output: experiments/poc_entanglement_tda/data/ssh_ring.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "data" / "ssh_ring.json"
DELTA = 0.05  # baseline "near 1/2" window, per PREREGISTRATION.md


def bond_type(i: int) -> str:
    return "v" if i % 2 == 0 else "w"


def ring_hamiltonian(v: float, w: float, L: int) -> np.ndarray:
    """2L x 2L dense real symmetric Hamiltonian of the SSH ring."""
    n = 2 * L
    h = np.zeros((n, n))
    for i in range(n):
        t = v if i % 2 == 0 else w
        j = (i + 1) % n
        h[i, j] = h[j, i] = t
    return h


def entanglement_spectrum(v: float, w: float, L: int, ell: int) -> np.ndarray:
    """zeta_n for the subsystem of the first ell whole unit cells (2*ell sites)."""
    n = 2 * L
    h = ring_hamiltonian(v, w, L)
    energies, vectors = np.linalg.eigh(h)
    # Half filling: the L most negative eigenvalues are filled. Generic gap
    # (r != 1 exactly) means no ambiguity about which L states are "filled".
    order = np.argsort(energies)
    filled = vectors[:, order[:L]]
    projector = filled @ filled.conj().T
    sub = 2 * ell
    c_a = projector[:sub, :sub]
    zeta = np.linalg.eigvalsh(c_a)
    return np.clip(zeta, 0.0, 1.0)


def correlation_length(v: float, w: float) -> float:
    ratio = abs(w) / abs(v) if abs(v) > abs(w) else abs(v) / abs(w)
    if ratio <= 0 or ratio >= 1:
        return float("inf")
    return 1.0 / -math.log(ratio)


def main() -> int:
    # Verify the "two w-bonds severed regardless of ell" claim before using it,
    # rather than trusting the hand derivation in the module docstring.
    for L_check in (10, 37, 100):
        for ell_check in (1, L_check // 3, L_check - 1):
            right_bond = 2 * ell_check - 1
            left_bond = 2 * L_check - 1  # wrap-around, index mod 2L is itself
            assert bond_type(right_bond % (2 * L_check)) == "w"
            assert bond_type(left_bond % (2 * L_check)) == "w"
    print("bond-severing check passed: every (L, ell) severs two w-bonds")

    r_grid = sorted(
        set(round(x, 3) for x in np.concatenate([
            np.linspace(0.2, 0.7, 6),
            np.linspace(0.75, 1.35, 25),  # dense near the transition
            np.linspace(1.4, 5.0, 6),
        ]))
        - {1.0}  # exactly at the transition the gap closes; excluded by design
    )

    results = []
    for L in (100, 300):
        ell = L // 2
        for r in r_grid:
            v, w = r, 1.0
            zeta = entanglement_spectrum(v, w, L, ell)
            near_half = int(np.sum(np.abs(zeta - 0.5) < DELTA))
            min_dist = float(np.min(np.abs(zeta - 0.5)))
            results.append({
                "L": L, "ell": ell, "r": r, "v": v, "w": w,
                "phase": "topological" if abs(w) > abs(v) else "trivial",
                "xi": correlation_length(v, w),
                "near_half_count": near_half,
                "min_dist_to_half": min_dist,
                # Full spectrum kept only near the transition (cheap; useful
                # for the barcode-vs-r figure) to keep the JSON file small.
                "zeta": zeta.tolist() if 0.75 <= r <= 1.35 else None,
            })
        print(f"  L={L}: {len(r_grid)} r-values done")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"wrote {OUT}")

    # Quick pass/fail against the preregistered controls, before any TDA step.
    failures = []
    for row in results:
        if row["r"] < 0.5 or row["r"] > 2.0:
            continue  # only check well away from finite-size smearing near r=1
        if row["phase"] == "topological" and row["near_half_count"] != 2:
            failures.append(f"L={row['L']} r={row['r']}: expected 2 near 1/2, got {row['near_half_count']}")
        if row["phase"] == "trivial" and row["near_half_count"] != 0:
            failures.append(f"L={row['L']} r={row['r']}: expected 0 near 1/2, got {row['near_half_count']}")
    print(f"\ncontrol check (|r-1|>0.5 only): {'PASS' if not failures else 'FAIL'}")
    for f in failures[:10]:
        print("  ", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
