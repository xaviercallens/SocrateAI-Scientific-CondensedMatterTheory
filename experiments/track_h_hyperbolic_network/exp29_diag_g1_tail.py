#!/usr/bin/env python3
"""PREREGISTRATION_29.md Deviation 1 (post hoc): gate G1' = G1 with the tail I(T) e^{-sT}/s added. Writes data/laplace_link_tail_corrected.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import (BANDS, CvodeSolver, HAVE_RUSTY, build_square_disk,  # noqa: E402
                                                          parts, response_and_h)

OUT = Path(__file__).resolve().parent / "data" / "laplace_link_tail_corrected.json"


def main():
    if not HAVE_RUSTY:
        OUT.write_text(json.dumps({"status": "NOT RUN"}), encoding="utf-8")
        print("NOT RUN")
        return 1
    g = build_square_disk(4)
    n, edges, bnd, interior, L = parts(g)
    Lii, Lib = L[np.ix_(interior, interior)], L[np.ix_(interior, bnd)]
    Lbb, Lbi = L[np.ix_(bnd, bnd)], L[np.ix_(bnd, interior)]
    lam_min = float(np.linalg.eigvalsh(Lii)[0])
    T = 40.0 / lam_min
    t = np.linspace(0.0, T, 4001)
    ej = np.zeros(len(bnd)); ej[0] = 1.0
    drive = Lib @ ej

    def rhs(_t, y):
        return list(-(Lii @ np.array(y) + drive))

    solver = CvodeSolver(method="bdf", rtol=1e-10, atol=1e-12, max_steps=200000)
    y, tc, V = [0.0] * len(interior), 0.0, [np.zeros(len(interior))]
    for tk in t[1:]:
        tc, y = solver.solve(rhs, tc, y, float(tk))
        V.append(np.array(y))
    V = np.array(V)
    I = (Lbb @ ej)[None, :] + V @ Lbi.T
    out = {"status": "RUN", "T": T, "lambda_min": lam_min, "tolerance": BANDS["G1_tol"], "per_s": {}}
    ok = True
    for s in (0.1, 0.3, 1.0):
        w = np.exp(-s * t)[:, None]
        F = I * w
        h = t[1] - t[0]
        simpson = h / 3 * (F[0] + F[-1] + 4 * F[1:-1:2].sum(axis=0) + 2 * F[2:-1:2].sum(axis=0))
        tail = I[-1] * np.exp(-s * T) / s
        Lam, _ = response_and_h(g, s)
        ref = Lam[:, 0] / s
        rel = float(np.abs(simpson + tail - ref).max() / np.abs(ref).max())
        rel_notail = float(np.abs(simpson - ref).max() / np.abs(ref).max())
        out["per_s"][str(s)] = {"rel_with_tail": rel, "rel_without_tail": rel_notail}
        ok = ok and rel <= BANDS["G1_tol"]
    out["pass"] = bool(ok)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
