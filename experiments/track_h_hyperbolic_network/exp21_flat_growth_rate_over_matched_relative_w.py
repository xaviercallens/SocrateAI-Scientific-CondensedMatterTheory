#!/usr/bin/env python3
"""PREREGISTRATION_21.md (exploratory): growth rate of the depth-restricted condition number over a window fixed in
relative depth (0.2 to 0.5 of d_max), on square R in {6,10,16,22} and triangular R in {3.225,6.45,10.75,17.2}.
Writes data/flat_growth_rate_over_matched_relative_w.json and data/fig_flat_rate.pdf; score() reads the file alone."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_square_disk, build_triangular_disk, depths, harmonic_extension, jacobian  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "flat_growth_rate_over_matched_relative_w.json"
FIG = HERE / "data" / "fig_flat_rate.pdf"
H0 = HERE / "data" / "h0.json"
LOG_KAPPA_FLOOR = 13.0
SQ, TR = [6, 10, 16, 22], [3.225, 6.45, 10.75, 17.2]
INSTANCES = [("square R=%g" % R, "square", R, lambda R=R: build_square_disk(R)) for R in SQ] + \
            [("triangular R=%g" % R, "triangular", R, lambda R=R: build_triangular_disk(R)) for R in TR]


def one_instance(name, fam, R, g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    D = (H[ea] - H[eb]).T; ed = np.minimum(d[ea], d[eb])
    J = jacobian(n, edges, np.ones(len(edges)), bnd)
    Jn = J / np.linalg.norm(J, axis=0)
    dmax = int(ed.max())
    log_kappa = []
    for k in range(dmax + 1):
        s = np.linalg.svd(J[:, np.where(ed <= k)[0]], compute_uv=False)
        log_kappa.append(float(np.log10(s[0] / s[-1])) if s[-1] > 0 else float("inf"))
    usable = [k for k in range(dmax + 1) if log_kappa[k] <= LOG_KAPPA_FLOOR]
    d_star = max(usable)
    lo, hi = math.ceil(0.2 * dmax), math.floor(0.5 * dmax)
    W = [k for k in range(lo, hi + 1) if k <= d_star]
    rate = (log_kappa[W[-1]] - log_kappa[W[0]]) / (W[-1] - W[0]) if len(W) >= 2 else None
    classes = {}
    for k in range(dmax + 1):
        idx = np.where(ed == k)[0]
        if len(idx) < 2:
            continue
        C = Jn[:, idx].T @ Jn[:, idx]; ev = np.linalg.eigvalsh((C + C.T) / 2)
        classes[str(k)] = {"n_edges": int(len(idx)), "lambda_min_normalised_gram": float(max(ev.min(), 0.0)),
                           "eff_dim_fraction": float(ev.sum() ** 2 / np.sum(ev ** 2) / len(ev))}
    r = {"name": name, "family": fam, "R": R, "N": n, "E": len(edges), "boundary": len(bnd), "d_max": dmax, "d_star": d_star,
         "log10_kappa_by_depth": log_kappa, "window_nominal": [lo, hi], "window_used": W, "window_truncated": bool(hi > d_star),
         "rate": rate, "by_depth": classes}
    print("  %-19s N=%5d d_max=%2d d*=%2d window=%s%s rate=%s" % (name, n, dmax, d_star, W, " (truncated)" if r["window_truncated"] else "",
          "%.3f" % rate if rate is not None else "n/a"), flush=True)
    print("      log10 kappa_d:", " ".join("%.2f" % x for x in log_kappa[: d_star + 1]), flush=True)
    return r


def run() -> dict:
    rows = [one_instance(name, fam, R, build()) for name, fam, R, build in INSTANCES]
    h0 = {(r["N"], r["E"]): r["log10_kappa"] for r in json.load(open(H0)) if r.get("log10_kappa") is not None}
    g2 = []
    for r in rows:
        if r["name"] in ("square R=10", "triangular R=6.45"):
            ref = h0.get((r["N"], r["E"]))
            g2.append({"name": r["name"], "ours": r["log10_kappa_by_depth"][-1], "h0": ref, "ok": ref is not None and abs(r["log10_kappa_by_depth"][-1] - ref) <= 1e-5})
    print("  G2:", g2)
    return {"rows": rows, "g2": g2}


def score(d: dict) -> dict:
    R = {r["name"]: r for r in d["rows"]}
    G1 = all(len(r["window_used"]) >= 3 for r in d["rows"])
    G2 = len(d["g2"]) == 2 and all(x["ok"] for x in d["g2"])
    sq = [R["square R=%g" % x]["rate"] for x in SQ]; tr = [R["triangular R=%g" % x]["rate"] for x in TR]
    P1 = all(a < b for a, b in zip(sq, sq[1:])) and all(a < b for a, b in zip(tr, tr[1:]))
    P2 = all(t > s for s, t in zip(sq, tr))
    return {"G1": bool(G1), "G2": bool(G2), "P1": bool(P1), "P2": bool(P2),
            "rate_square": {str(x): round(v, 4) for x, v in zip(SQ, sq)}, "rate_triangular": {str(x): round(v, 4) for x, v in zip(TR, tr)},
            "windows": {r["name"]: r["window_used"] for r in d["rows"]}, "truncated": [r["name"] for r in d["rows"] if r["window_truncated"]]}


def figure(d):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for r in d["rows"]:
        st = dict(ls="--" if r["family"] == "square" else ":", marker="s" if r["family"] == "square" else "^", ms=4, lw=0.9, label=r["name"])
        ks = list(range(r["d_star"] + 1)); axes[0].plot(np.array(ks) / r["d_max"], r["log10_kappa_by_depth"][: r["d_star"] + 1], **st)
    axes[0].set_xlabel("relative depth d / d_max"); axes[0].set_ylabel("log10 kappa of J restricted to depth <= d"); axes[0].legend(fontsize=6, frameon=False)
    v = d["verdicts"]
    axes[1].plot(SQ, [v["rate_square"][str(x)] for x in SQ], "s--", label="square"); axes[1].plot(TR, [v["rate_triangular"][str(x)] for x in TR], "^:", label="triangular")
    axes[1].set_xlabel("R"); axes[1].set_ylabel("rate over d/d_max in [0.2, 0.5] (decades per depth)"); axes[1].legend(frameon=False)
    fig.tight_layout(); fig.savefig(FIG)


def main() -> int:
    d = run(); d["verdicts"] = score(d); figure(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
