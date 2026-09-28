#!/usr/bin/env python3
"""PREREGISTRATION_16.md (EXPLORATORY): per-edge sensitivity ||dLambda/dg_e||_F = ||d_e||^2 versus edge depth for
every tiling and flat instance. Writes data/sensitivity_versus_depth_across_tilings.json and
paper/fig_sensitivity_depth.pdf. score() returns only the validity gates."""
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
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, build_triangular_disk, depths, harmonic_extension,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "sensitivity_versus_depth_across_tilings.json"
FIG = HERE / "paper" / "fig_sensitivity_depth.pdf"
INSTANCES = ([("{%d,%d}" % (p, q), "L=%d" % L, lambda p=p, q=q, L=L: build_hyperbolic(p, q, L))
              for (p, q), Ls in (((7, 3), range(1, 5)), ((8, 3), range(1, 5)), ((5, 4), range(1, 6)), ((6, 4), range(1, 5)), ((4, 5), range(1, 7)))
              for L in Ls]
             + [("square", "R=%g" % R, lambda R=R: build_square_disk(R)) for R in (3, 6, 10)]
             + [("triangular", "R=%g" % R, lambda R=R: build_triangular_disk(R)) for R in (3.225, 6.45)])


def profile(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    D = H[ea] - H[eb]
    S = np.sum(D ** 2, axis=1)                                # ||d_e||^2 per edge (profile statistic)
    col = np.sqrt(0.5 * (S ** 2 - np.sum(D ** 4, axis=1)))    # ||J[:,e]||_2 over boundary pairs i<j (h0 statistic)
    ed = np.minimum(d[ea], d[eb])
    rows = {}
    for k in sorted(set(int(x) for x in ed)):
        s = S[ed == k]
        rows[str(k)] = {"n_edges": int(len(s)), "mean_log10": float(np.mean(np.log10(s))), "median_log10": float(np.median(np.log10(s))),
                        "mean": float(np.mean(s)), "h0_median_colnorm": float(np.median(col[ed == k]))}
    ks = np.array([int(k) for k in rows]); ys = np.array([rows[str(k)]["mean_log10"] for k in ks])
    slope = float(np.polyfit(ks, ys, 1)[0]) if len(ks) >= 2 else None
    m1 = ks >= 1
    slope1 = float(np.polyfit(ks[m1], ys[m1], 1)[0]) if m1.sum() >= 2 else None
    return {"N": n, "E": len(edges), "d_max_node": int(d.max()), "by_depth": rows, "slope_per_depth": slope,
            "slope_per_depth_from_1": slope1}


def run() -> dict:
    out = []
    for fam, par, build in INSTANCES:
        r = profile(build()); r.update({"family": fam, "param": par})
        out.append(r)
        print("  %-10s %-8s N=%5d slope=%s slope(d>=1)=%s" % (fam, par, r["N"],
              "%.3f" % r["slope_per_depth"] if r["slope_per_depth"] is not None else "n/a",
              "%.3f" % r["slope_per_depth_from_1"] if r["slope_per_depth_from_1"] is not None else "n/a"), flush=True)
    return {"exploratory": True, "rows": out}


def score(d: dict) -> dict:
    h0 = {r["name"]: r for r in json.loads((HERE / "data" / "h0.json").read_text())}
    G1 = True
    for r in d["rows"]:
        if r["family"] == "{7,3}":
            ref = h0["{7,3} " + r["param"]]["sensitivity_by_depth"]
            m0 = r["by_depth"]["0"]["h0_median_colnorm"]     # Deviation 1: compare the h0 statistic itself
            for k, v in ref.items():
                if k in r["by_depth"]:
                    G1 &= abs(r["by_depth"][k]["h0_median_colnorm"] / m0 - v) <= 1e-6 * max(1.0, abs(v))
    G2 = all(sum(v["n_edges"] for v in r["by_depth"].values()) == r["E"] for r in d["rows"])
    return {"G1": G1, "G2": G2}


def figure(d):
    fig, ax = plt.subplots(figsize=(6, 4))
    seen = set()
    for r in d["rows"]:
        ks = sorted(int(k) for k in r["by_depth"]); ys = [r["by_depth"][str(k)]["mean_log10"] - r["by_depth"]["0"]["mean_log10"] for k in ks]
        hyp = r["family"].startswith("{")
        style = dict(color={"{7,3}": "C0", "{8,3}": "C3", "{5,4}": "C4", "{6,4}": "C5", "{4,5}": "C6", "square": "C1", "triangular": "C2"}[r["family"]],
                     ls="-" if hyp else "--", lw=0.8, marker="o" if hyp else "s", ms=3, mfc="none" if not hyp else None)
        ax.plot(ks, ys, label=r["family"] if r["family"] not in seen else None, **style); seen.add(r["family"])
    ax.set_xlabel("edge depth"); ax.set_ylabel(r"mean $\log_{10}$ sensitivity, relative to depth 0")
    ax.legend(fontsize=7, frameon=False, ncol=2); fig.tight_layout(); fig.savefig(FIG)


def main() -> int:
    d = run(); d["verdicts"] = score(d); figure(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
