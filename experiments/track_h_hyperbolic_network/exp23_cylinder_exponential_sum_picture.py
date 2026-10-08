#!/usr/bin/env python3
"""PREREGISTRATION_23.md: growth rate of the depth-restricted condition number of the DtN Jacobian on lattice
cylinders (periodic in one direction, measurement on row 0), where the problem separates by Fourier mode.
Square cylinder: full columns and vertical-edge columns only (Vandermonde-type system, closed-form rate);
triangular cylinder: full columns. Writes data/cylinder_exponential_sum_picture.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import depths, jacobian, jacobian_finite_diff  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "cylinder_exponential_sum_picture.json"
LOG_KAPPA_FLOOR, D_FIT_MIN = 12.5, 3
PLAN = [("square", 64, 18), ("square", 96, 18), ("triangular", 64, 12), ("triangular", 96, 12)]
PRED_VERT_SQUARE = 0.7838   # log10(x + sqrt(x^2-1)), x = (3+a)/(1-a), a = exp(-2 acosh 3): closed form, PREREGISTRATION_23.md


def build_cylinder(kind: str, W: int, H: int):
    """Rows 0..H, W columns periodic; row 0 is the boundary. Returns graph dict, edge list, edge type labels."""
    idx = lambda r, j: r * W + (j % W)
    edges, types = {}, {}

    def add(a, b, t):
        e = (min(a, b), max(a, b))
        if e not in edges:
            edges[e] = len(edges); types[e] = t
    for r in range(H + 1):
        for j in range(W):
            add(idx(r, j), idx(r, j + 1), "h")
            if r < H:
                if kind == "square":
                    add(idx(r, j), idx(r + 1, j), "v")
                else:   # triangular: odd rows shifted by half a column
                    if r % 2 == 0:
                        add(idx(r, j), idx(r + 1, j - 1), "d"); add(idx(r, j), idx(r + 1, j), "d")
                    else:
                        add(idx(r, j), idx(r + 1, j), "d"); add(idx(r, j), idx(r + 1, j + 1), "d")
    el = sorted(edges, key=edges.get)
    return {"nodes": np.arange((H + 1) * W), "edges": el}, el, [types[e] for e in el]


def gate_fd(kind):
    g, el, _ = build_cylinder(kind, 8, 3)
    bnd = np.arange(8); n = len(g["nodes"]); gv = np.ones(len(el))
    J, Jf = jacobian(n, el, gv, bnd), jacobian_finite_diff(n, el, gv, bnd)
    return float(np.abs(J - Jf).max() / np.abs(J).max())


def rate(ds, lk):
    ds = np.array(ds, float); lk = np.array(lk, float)
    sel = ds >= D_FIT_MIN
    if sel.sum() < 3:
        return None
    return float(np.polyfit(ds[sel], lk[sel], 1)[0])


def one(kind, W, H):
    g, el, types = build_cylinder(kind, W, H)
    n, E = len(g["nodes"]), len(el); bnd = np.arange(W)
    d = depths(g, bnd); ed = np.minimum(d[[a for a, _ in el]], d[[b for _, b in el]])
    J = jacobian(n, el, np.ones(E), bnd); rows = J.shape[0]
    types = np.array(types); res = {"kind": kind, "W": W, "H": H, "N": n, "E": E, "data_rows": rows, "series": {}}
    for label, mask in (("full", np.ones(E, bool)), ("vertical_only", types == "v")):
        if label == "vertical_only" and kind != "square":
            continue
        ds, lk = [], []
        for dd in range(0, H + 1):
            cols = np.where((ed <= dd) & mask)[0]
            if len(cols) == 0 or len(cols) > rows:
                break
            s = np.linalg.svd(J[:, cols], compute_uv=False)
            val = float(np.log10(s[0] / s[-1])) if s[-1] > 0 else float("inf")
            if val > LOG_KAPPA_FLOOR:
                break
            ds.append(dd); lk.append(val)
        res["series"][label] = {"d": ds, "log10_kappa": lk, "rate": rate(ds, lk), "d_star": ds[-1] if ds else None}
        print("  %-10s W=%3d %-13s d*=%s rate=%s  log10 kappa_d: %s" % (kind, W, label, ds[-1] if ds else None,
              "%.3f" % res["series"][label]["rate"] if res["series"][label]["rate"] is not None else "n/a", " ".join("%.1f" % x for x in lk)), flush=True)
    return res


def run() -> dict:
    out = {"gate_fd": {k: gate_fd(k) for k in ("square", "triangular")}, "runs": []}
    print("  finite-difference check:", out["gate_fd"], flush=True)
    for kind, W, H in PLAN:
        out["runs"].append(one(kind, W, H))
    return out


def score(d: dict) -> dict:
    R = {(r["kind"], r["W"]): r for r in d["runs"]}
    rt = lambda kind, W, lab="full": R[(kind, W)]["series"][lab]["rate"]
    G1 = all(v <= 1e-5 for v in d["gate_fd"].values())
    G2 = True
    for W in (64, 96):
        full, vert = R[("square", W)]["series"]["full"], R[("square", W)]["series"]["vertical_only"]
        for dd, lk in zip(vert["d"], vert["log10_kappa"]):
            if dd in full["d"] and full["log10_kappa"][full["d"].index(dd)] < lk - 1e-6:
                G2 = False
    G3 = all(R[k]["series"]["full"]["d_star"] is not None and R[k]["series"]["full"]["d_star"] >= 6 for k in R)
    P1 = all(0.63 <= rt("square", W, "vertical_only") <= 0.94 for W in (64, 96))
    P2 = abs(rt("square", 96, "vertical_only") - rt("square", 64, "vertical_only")) <= 0.10
    P3 = all(0.9 <= rt("square", W) <= 1.5 for W in (64, 96))
    P4 = all(1.3 <= rt("triangular", W) <= 2.3 for W in (64, 96)) and all(rt("triangular", W) / rt("square", W) >= 1.2 for W in (64, 96))
    return {"G1": bool(G1), "G2": bool(G2), "G3": bool(G3), "P1": bool(P1), "P2": bool(P2), "P3": bool(P3), "P4": bool(P4),
            "rates": {"%s W=%d %s" % (k[0], k[1], lab): R[k]["series"][lab]["rate"] for k in R for lab in R[k]["series"]},
            "d_star": {"%s W=%d %s" % (k[0], k[1], lab): R[k]["series"][lab]["d_star"] for k in R for lab in R[k]["series"]},
            "predicted_vertical_square": PRED_VERT_SQUARE}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
