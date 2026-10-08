#!/usr/bin/env python3
"""PREREGISTRATION_31.md: CVODE (rusty-SUNDIALS) check of the garage virtual bench's modal solution and of the tolerance spread of the tau ratio.
Writes data/cvode_check_of_the_garage_virtual_bench.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "lab"))
import virtual_bench as vb  # noqa: E402
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, laplacian  # noqa: E402

try:
    from rusty_sundials import CvodeSolver
    HAVE = True
except Exception:  # noqa: BLE001
    HAVE = False

OUT = HERE / "data" / "cvode_check_of_the_garage_virtual_bench.json"
NT = 2000
BANDS = {"P1": 1e-6, "P2": 1e-4, "P3_center": 0.604, "P3_half": 0.03, "P3_spread": 0.02, "G1": 1e-8}
SEED_WAVE = 3100
SEED_RATIO = 3200


def draw_board(g, rng, tol_R, tol_C):
    """Same random draws, in the same order, as vb.board_response; returns the system and the modal waveform on the grid."""
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    d = depths(g, bnd)
    interior = np.setdiff1d(np.arange(n), bnd)
    gvals = 1.0 / (vb.R * (1 + tol_R * rng.uniform(-1, 1, len(edges))))
    Cv = vb.C * (1 + tol_C * rng.uniform(-1, 1, len(interior)))
    L = laplacian(n, edges, gvals)
    Lii, Lib = L[np.ix_(interior, interior)], L[np.ix_(interior, bnd)]
    Ln = laplacian(n, edges, np.full(len(edges), 1.0 / vb.R))
    lam_n = eigh(Ln[np.ix_(interior, interior)], np.diag(np.full(len(interior), vb.C)), eigvals_only=True)
    tau_nom = 1.0 / lam_n[0]
    probes = [int(interior[np.argmax(d[interior] == pd)]) for pd in (1, 2, 3) if (d[interior] == pd).any()]
    pidx = [int(np.where(interior == p)[0][0]) for p in probes]
    t = np.linspace(0.0, 8 * tau_nom, NT, endpoint=False)
    lam, U = eigh(Lii, np.diag(Cv))
    Vinf = np.linalg.solve(Lii, -(Lib @ np.full(len(bnd), vb.V0)))
    coef = U.T @ (np.diag(Cv) @ (0 - Vinf))
    Vmodal = Vinf[pidx][:, None] + (U[pidx] * coef) @ np.exp(-np.outer(lam, t))
    return {"Lii": Lii, "Lib": Lib, "Cv": Cv, "t": t, "pidx": pidx, "Vmodal": Vmodal, "n_int": len(interior), "nb": len(bnd)}


def cvode_waveform(b):
    drive = b["Lib"] @ np.full(b["nb"], vb.V0)
    Cinv = 1.0 / b["Cv"]
    Lii = b["Lii"]

    def rhs(_t, y):
        return list(-Cinv * (Lii @ np.array(y) + drive))

    solver = CvodeSolver(method="bdf", rtol=1e-10, atol=1e-12, max_steps=200000)
    y, tc, out = [0.0] * b["n_int"], 0.0, [np.zeros(b["n_int"])]
    for tk in b["t"][1:]:
        tc, y = solver.solve(rhs, tc, y, float(tk))
        out.append(np.array(y))
    return np.array(out)[:, b["pidx"]].T


def run_pair(g, seed, tol_R, tol_C):
    b = draw_board(g, np.random.default_rng(seed), tol_R, tol_C)
    Vc = cvode_waveform(b)
    wave = float(np.abs(Vc - b["Vmodal"]).max() / vb.V0)
    tc, _ = vb.fit_tau(b["t"], Vc)
    tm, _ = vb.fit_tau(b["t"], b["Vmodal"])
    return wave, tc, tm


def main():
    if not HAVE:
        OUT.write_text(json.dumps({"status": "NOT RUN"}))
        print("NOT RUN")
        return 1
    res = {"bands": BANDS, "NT": NT}
    # G1
    b = draw_board(build_square_disk(4), np.random.default_rng(1), 0.0, 0.0)
    g1 = float(np.abs(cvode_waveform(b) - b["Vmodal"]).max() / vb.V0)
    res["G1"] = {"max_rel_diff": g1, "pass": bool(g1 <= BANDS["G1"])}
    print("G1", res["G1"], flush=True)

    boards = (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6)))
    wave_rows = []
    for name, g in boards:
        for i in range(6):
            w, tc, tm = run_pair(g, SEED_WAVE + i, 0.05, 0.10)
            wave_rows.append({"board": name, "seed": SEED_WAVE + i, "max_rel_waveform_diff": w, "tau_cvode": tc, "tau_modal": tm,
                              "tau_rel_diff": abs(tc - tm) / tm})
        print(name, "waveform draws done", flush=True)
    res["waveform_draws"] = wave_rows
    res["P1"] = {"max": max(r["max_rel_waveform_diff"] for r in wave_rows), "pass": bool(max(r["max_rel_waveform_diff"] for r in wave_rows) <= BANDS["P1"])}
    res["P2"] = {"max": max(r["tau_rel_diff"] for r in wave_rows), "pass": bool(max(r["tau_rel_diff"] for r in wave_rows) <= BANDS["P2"])}

    ratios = []
    for i in range(12):
        th = run_pair(boards[0][1], SEED_RATIO + i, 0.01, 0.01)[1]
        ts = run_pair(boards[1][1], SEED_RATIO + 100 + i, 0.01, 0.01)[1]
        ratios.append(th / ts)
    ratios = np.array(ratios)
    spread = float((ratios.max() - ratios.min()) / ratios.mean())
    inband = bool(np.all(np.abs(ratios - BANDS["P3_center"]) <= BANDS["P3_half"]))
    res["ratios"] = [float(x) for x in ratios]
    res["P3"] = {"mean": float(ratios.mean()), "min": float(ratios.min()), "max": float(ratios.max()), "spread": spread,
                 "all_in_band": inband, "pass": bool(inband and spread <= BANDS["P3_spread"])}
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    for k in ("G1", "P1", "P2", "P3"):
        print(k, res[k])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
