#!/usr/bin/env python3
"""Tier B harness for the finite SSH statements (Elenchus tier discipline).

`ssh_check.py` uses floating point, so under Elenchus it is Tier X: it may steer,
it may never support a claim. This harness decides the *finite* half of the Lean
T2 target in exact rational arithmetic (`fractions.Fraction`, no floats), on
concrete instances, and ships the controls Elenchus requires:

  claims (must hold on every instance)
    B1  odd open chain (2N+1 sites): nullity(H) = 1 exactly, and
        psi_A(n) = (-v/w)^n, psi_B = 0 satisfies H psi = 0 exactly
    B2  that zero mode sits at the LEFT end iff |w| > |v|
        (|psi_A(0)| > |psi_A(N)|, decided by exact comparison)
    B3  even open chain (2N sites): rank(H) = 2N, so no exact zero mode,
        and det of the sublattice block D equals v^N exactly

  negative controls (the checker must be DEMONSTRATED TO FAIL)
    NC1 the wrong-sign vector psi_A(n) = (+v/w)^n is not in the kernel
    NC2 a generic non-zero rational vector is not in the kernel

  positive control (the detector must be DEMONSTRATED TO FIRE)
    PC1 the zero-mode detector (nullity > 0) fires on an even chain with v = 0,
        which has decoupled end sites and hence zero modes by construction.
        Without this, "no zero mode" in B3 could be a detector that never fires.

The winding-number half of T2 is NOT decided here: it is an integral, and a
numeric evaluation is Tier X. It stays at L (argument principle, via the Mathlib
lemma quoted in the ledger) until it is proved in Lean (A).

Writes a deterministic evidence file (no timestamps) whose sha256 the ledger
cites. Exit 0 only if every claim holds, every negative control fails and every
positive control fires.

Usage:
    python3 experiments/axis1_topological_waves/ssh_exact.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent / "evidence" / "ssh_exact.json"

# Rational instances, v, w non-zero, |v| != |w|, both phases and both signs.
INSTANCES = [
    (Q(1, 2), Q(1)),
    (Q(1), Q(1, 2)),
    (Q(2, 3), Q(5, 4)),
    (Q(-3, 4), Q(1)),
    (Q(1), Q(-2, 5)),
    (Q(7, 5), Q(3, 5)),
]
CELLS = (2, 3, 5)


def chain(v: Q, w: Q, sites: int) -> list[list[Q]]:
    """Sites A0 B0 A1 B1 ...; bond i-(i+1) is v for even i (intra), w for odd i."""
    h = [[Q(0)] * sites for _ in range(sites)]
    for i in range(sites - 1):
        t = v if i % 2 == 0 else w
        h[i][i + 1] = h[i + 1][i] = t
    return h


def rank(matrix: list[list[Q]]) -> int:
    """Exact rank by Gaussian elimination over Q."""
    m = [row[:] for row in matrix]
    rows, cols = len(m), len(m[0]) if m else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][c] != 0), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


def apply(matrix: list[list[Q]], vec: list[Q]) -> list[Q]:
    return [sum((a * b for a, b in zip(row, vec)), Q(0)) for row in matrix]


def in_kernel(matrix: list[list[Q]], vec: list[Q]) -> bool:
    return any(x != 0 for x in vec) and all(x == 0 for x in apply(matrix, vec))


def has_zero_mode(matrix: list[list[Q]]) -> bool:
    """The detector whose firing PC1 demonstrates."""
    return rank(matrix) < len(matrix)


def odd_zero_mode(v: Q, w: Q, n_cells: int) -> list[Q]:
    """psi_A(n) = (-v/w)^n on A sites (even indices), 0 on B sites."""
    vec = [Q(0)] * (2 * n_cells + 1)
    for n in range(n_cells + 1):
        vec[2 * n] = (-v / w) ** n
    return vec


def sublattice_det(v: Q, w: Q, n_cells: int) -> Q:
    """det of the lower-bidiagonal block D (v on the diagonal, w below)."""
    d = [[Q(0)] * n_cells for _ in range(n_cells)]
    for n in range(n_cells):
        d[n][n] = v
        if n > 0:
            d[n][n - 1] = w
    # exact determinant by elimination
    m = [row[:] for row in d]
    det = Q(1)
    for c in range(n_cells):
        pivot = next((i for i in range(c, n_cells) if m[i][c] != 0), None)
        if pivot is None:
            return Q(0)
        if pivot != c:
            m[c], m[pivot] = m[pivot], m[c]
            det = -det
        det *= m[c][c]
        for i in range(c + 1, n_cells):
            f = m[i][c] / m[c][c]
            m[i] = [a - f * b for a, b in zip(m[i], m[c])]
    return det


def main() -> int:
    records: list[dict] = []
    failures: list[str] = []

    def record(tag: str, ok: bool, detail: str) -> None:
        records.append({"check": tag, "ok": ok, "detail": detail})
        print(f"  {'ok  ' if ok else 'FAIL'} {tag:4} {detail}")
        if not ok:
            failures.append(f"{tag}: {detail}")

    print("claims")
    for v, w in INSTANCES:
        for n in CELLS:
            odd = chain(v, w, 2 * n + 1)
            psi = odd_zero_mode(v, w, n)
            nullity = len(odd) - rank(odd)
            record("B1", nullity == 1 and in_kernel(odd, psi),
                   f"v={v}, w={w}, N={n}: odd chain nullity={nullity}, psi in kernel={in_kernel(odd, psi)}")

            left_heavy = abs(psi[0]) > abs(psi[2 * n])
            record("B2", left_heavy == (abs(w) > abs(v)),
                   f"v={v}, w={w}, N={n}: left end heavier={left_heavy}, |w|>|v|={abs(w) > abs(v)}")

            even = chain(v, w, 2 * n)
            det_d = sublattice_det(v, w, n)
            record("B3", rank(even) == 2 * n and det_d == v**n,
                   f"v={v}, w={w}, N={n}: even rank={rank(even)}/{2 * n}, det D={det_d} (v^N={v**n})")

    print("negative controls (must fail)")
    for v, w in INSTANCES[:3]:
        n = 3
        odd = chain(v, w, 2 * n + 1)
        wrong = [Q(0)] * (2 * n + 1)
        for k in range(n + 1):
            wrong[2 * k] = (v / w) ** k
        failed = not in_kernel(odd, wrong)
        record("NC1", failed, f"v={v}, w={w}: wrong-sign vector rejected={failed}")

        generic = [Q(k + 1, 3) for k in range(2 * n + 1)]
        failed = not in_kernel(odd, generic)
        record("NC2", failed, f"v={v}, w={w}: generic vector rejected={failed}")

    print("positive control (must fire)")
    for n in CELLS:
        fired = has_zero_mode(chain(Q(0), Q(1), 2 * n))
        record("PC1", fired, f"v=0, w=1, N={n}: zero-mode detector fired={fired}")

    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(
        json.dumps({"harness": "ssh_exact.py", "arithmetic": "fractions.Fraction",
                    "records": records}, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {EVIDENCE.relative_to(Path.cwd()) if EVIDENCE.is_relative_to(Path.cwd()) else EVIDENCE}")
    print(f"{len(records)} checks: {'PASS' if not failures else f'FAILED ({len(failures)})'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
