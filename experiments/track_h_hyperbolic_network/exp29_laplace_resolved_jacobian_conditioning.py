#!/usr/bin/env python3
"""PREREGISTRATION_29.md: Laplace-resolved Jacobian conditioning. Stacked Jacobian over real Laplace variables s of the RC network
(conductance 1 per edge, capacitance 1 per interior node); G1 checks the time-to-frequency link with rusty-SUNDIALS CVODE.
Writes data/laplace_resolved_jacobian_conditioning.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (boundary_nodes, build_hyperbolic, build_square_disk, depths,  # noqa: E402
                                laplacian)

try:
    from rusty_sundials import CvodeSolver
    HAVE_RUSTY = True
except Exception:  # noqa: BLE001
    HAVE_RUSTY = False

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "laplace_resolved_jacobian_conditioning.json"
S1, S2, S5 = [0.0], [0.0, 0.3], [0.0, 0.1, 0.3, 1.0, 3.0]
RADIUS = 16
WINDOW = range(3, 8)
LOG_FLOOR = 9.0          # use only d with log10 kappa(S1) <= this (double-precision floor)
BANDS = {"P1_min_ratio": 0.5, "P2_max_ratio": 1.0, "P3_max_diff": 0.15, "P4_max_diff": 1.0,
         "G1_tol": 1e-5, "G3_range": (0.9, 1.3)}


def parts(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    interior = np.setdiff1d(np.arange(n), bnd)
    L = laplacian(n, edges, np.ones(len(edges)))
    return n, edges, bnd, interior, L


def response_and_h(g, s):
    """Lambda(s) and the n x m harmonic extension H(s)."""
    n, edges, bnd, interior, L = parts(g)
    Lii, Lib = L[np.ix_(interior, interior)], L[np.ix_(interior, bnd)]
    Lbb, Lbi = L[np.ix_(bnd, bnd)], L[np.ix_(bnd, interior)]
    X = np.linalg.solve(Lii + s * np.eye(len(interior)), Lib)
    H = np.zeros((n, len(bnd)))
    H[bnd, :] = np.eye(len(bnd))
    H[interior, :] = -X
    return Lbb - Lbi @ X, H


def jac_s(g, s):
    n, edges, bnd, _, _ = parts(g)
    _, H = response_and_h(g, s)
    m = len(bnd)
    iu = np.triu_indices(m, k=1)
    ea = np.array([a for a, _ in edges])
    eb = np.array([b for _, b in edges])
    D = H[ea] - H[eb]                       # E x m
    return np.stack([np.outer(D[e], D[e])[iu] for e in range(len(edges))], axis=1)


def edge_depth(g):
    bnd = boundary_nodes(g)
    dn = depths(g, bnd)
    return np.array([min(dn[a], dn[b]) for a, b in g["edges"]])


def stacked_stats(g, S, dmax_list):
    Js = [jac_s(g, s) for s in S]
    J = np.vstack(Js)
    dep = edge_depth(g)
    rows = {}
    for d in dmax_list:
        cols = np.where(dep <= d)[0]
        sv = np.linalg.svd(J[:, cols], compute_uv=False)
        rows[int(d)] = {"n_cols": int(len(cols)), "sigma_max": float(sv[0]), "sigma_min": float(sv[-1]),
                        "log10_kappa": float(np.log10(sv[0] / sv[-1]))}
    return rows


def slope(rows, ds):
    x = np.array(ds, float)
    y = np.array([rows[d]["log10_kappa"] for d in ds])
    return float(np.polyfit(x, y, 1)[0])


def gate_g1():
    if not HAVE_RUSTY:
        return {"status": "NOT RUN", "reason": "rusty_sundials not importable"}
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
    V = np.array(V)                                   # (nt, n_int)
    I = (Lbb @ ej)[None, :] + V @ Lbi.T               # (nt, m) boundary currents
    out = {"status": "RUN", "T": T, "lambda_min": lam_min, "per_s": {}}
    ok = True
    for s in (0.1, 0.3, 1.0):
        w = np.exp(-s * t)[:, None]
        F = I * w
        h = t[1] - t[0]
        simpson = h / 3 * (F[0] + F[-1] + 4 * F[1:-1:2].sum(axis=0) + 2 * F[2:-1:2].sum(axis=0))
        Lam, _ = response_and_h(g, s)
        ref = Lam[:, 0] / s
        rel = float(np.abs(simpson - ref).max() / np.abs(ref).max())
        out["per_s"][str(s)] = rel
        ok = ok and rel <= BANDS["G1_tol"]
    out["pass"] = bool(ok)
    return out


def main():
    res = {"bands": {k: (list(v) if isinstance(v, tuple) else v) for k, v in BANDS.items()}, "sets": {"S1": S1, "S2": S2, "S5": S5}}
    print("G1 (CVODE link) ...", flush=True)
    res["G1"] = gate_g1()
    print("  ", res["G1"], flush=True)

    g = build_square_disk(RADIUS)
    dep = edge_depth(g)
    dmax = int(dep.max())
    print(f"square R={RADIUS}: N={len(g['nodes'])} E={len(g['edges'])} m={len(boundary_nodes(g))} d_max={dmax}", flush=True)
    ds_all = list(range(1, min(dmax, 9) + 1))
    tab = {name: stacked_stats(g, S, ds_all) for name, S in (("S1", S1), ("S2", S2), ("S5", S5))}
    res["square"] = {"R": RADIUS, "N": len(g["nodes"]), "E": len(g["edges"]), "d_max": dmax, "table": tab}
    window = [d for d in WINDOW if d in tab["S1"] and tab["S1"][d]["log10_kappa"] <= LOG_FLOOR]
    res["window_used"] = window
    sl = {k: slope(tab[k], window) for k in tab}
    res["slopes"] = sl
    res["G2_sigma_min_monotone"] = bool(all(tab["S5"][d]["sigma_min"] >= tab["S1"][d]["sigma_min"] * (1 - 1e-8) for d in ds_all))
    res["G3_pass"] = bool(BANDS["G3_range"][0] <= sl["S1"] <= BANDS["G3_range"][1])
    res["P1"] = {"ratio": sl["S5"] / sl["S1"], "pass": bool(sl["S5"] / sl["S1"] >= BANDS["P1_min_ratio"])}
    res["P2"] = {"ratio": sl["S5"] / sl["S1"], "pass": bool(sl["S5"] / sl["S1"] <= BANDS["P2_max_ratio"])}
    res["P3"] = {"diff": abs(sl["S5"] - sl["S2"]), "pass": bool(abs(sl["S5"] - sl["S2"]) < BANDS["P3_max_diff"])}

    h = build_hyperbolic(7, 3, 4)
    hd = int(edge_depth(h).max())
    ht = {name: stacked_stats(h, S, [hd]) for name, S in (("S1", S1), ("S5", S5))}
    diff = abs(ht["S5"][hd]["log10_kappa"] - ht["S1"][hd]["log10_kappa"])
    res["hyperbolic_73_L4"] = {"N": len(h["nodes"]), "E": len(h["edges"]), "d_max": hd, "table": ht}
    res["P4"] = {"diff": diff, "pass": bool(diff <= BANDS["P4_max_diff"])}

    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print("window", window, "slopes", {k: round(v, 4) for k, v in sl.items()})
    for k in ("G2_sigma_min_monotone", "G3_pass", "P1", "P2", "P3", "P4"):
        print(k, res[k])
    for name in ("S1", "S2", "S5"):
        print(name, {d: round(tab[name][d]["log10_kappa"], 3) for d in ds_all})
    print("hyperbolic", {k: round(v[hd]["log10_kappa"], 3) for k, v in ht.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
