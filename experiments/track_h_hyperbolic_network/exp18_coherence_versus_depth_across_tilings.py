#!/usr/bin/env python3
"""PREREGISTRATION_18.md: exhaustive |cos| between Jacobian columns of equal-depth edges, and the effective
dimension fraction per depth, across tilings and flat lattices. Writes data/coherence_versus_depth_across_tilings.json
and data/fig_coherence_depth.pdf; score() returns G1, G2, P1..P4 from the data alone."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, build_triangular_disk, depths, harmonic_extension, jacobian,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "coherence_versus_depth_across_tilings.json"
FIG = HERE / "data" / "fig_coherence_depth.pdf"
INSTANCES = ([("{%d,%d}" % (p, q), "L=%d" % L, lambda p=p, q=q, L=L: build_hyperbolic(p, q, L))
              for (p, q), Ls in (((7, 3), range(1, 5)), ((8, 3), range(1, 5)), ((5, 4), range(1, 6)), ((6, 4), range(1, 5)), ((4, 5), range(1, 7)))
              for L in Ls]
             + [("square", "R=%g" % R, lambda R=R: build_square_disk(R)) for R in (3, 6, 10)]
             + [("triangular", "R=%g" % R, lambda R=R: build_triangular_disk(R)) for R in (3.225, 6.45)])
LARGEST = {"{7,3}": "L=4", "{8,3}": "L=4", "{5,4}": "L=5", "{6,4}": "L=4", "{4,5}": "L=6", "square": "R=10", "triangular": "R=6.45"}


def signatures(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    return (H[ea] - H[eb]).T, np.minimum(d[ea], d[eb])      # D: m x E ; edge depth


def cos_matrix(D):
    """Closed-form cosines between the upper-triangular Jacobian columns of the edges whose signatures are the
    columns of D (m x n): <J_e, J_f> = 1/2 [ (d_e.d_f)^2 - sum_i d_e,i^2 d_f,i^2 ]."""
    M1 = D.T @ D
    M2 = (D ** 2).T @ (D ** 2)
    G = 0.5 * (M1 ** 2 - M2)
    nrm = np.sqrt(np.diag(G))
    return G / np.outer(nrm, nrm)


def per_depth(D, ed):
    out = {}
    for k in sorted(set(int(x) for x in ed)):
        idx = np.where(ed == k)[0]
        n = len(idx)
        if n < 2:
            continue
        C = cos_matrix(D[:, idx])
        iu = np.triu_indices(n, k=1)
        a = np.abs(C[iu])
        ev = np.linalg.eigvalsh((C + C.T) / 2)
        pr = float(ev.sum() ** 2 / np.sum(ev ** 2))
        out[str(k)] = {"n_edges": int(n), "n_pairs": int(len(a)), "median_abs_cos": float(np.median(a)),
                       "mean_abs_cos": float(np.mean(a)), "p90_abs_cos": float(np.percentile(a, 90)),
                       "participation_ratio": pr, "eff_dim_fraction": pr / n}
    return out


def gate_closed_form(g):
    """Max |difference| between closed-form cosines and cosines of the explicit Jacobian columns."""
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    J = jacobian(n, edges, np.ones(len(edges)), bnd)
    Jn = J / np.linalg.norm(J, axis=0)
    D, ed = signatures(g)
    worst = 0.0
    for k in sorted(set(int(x) for x in ed)):
        idx = np.where(ed == k)[0]
        if len(idx) < 2:
            continue
        C1 = cos_matrix(D[:, idx]); C2 = Jn[:, idx].T @ Jn[:, idx]
        worst = max(worst, float(np.max(np.abs(C1 - C2))))
    return worst


def run() -> dict:
    rows = []
    for fam, par, build in INSTANCES:
        g = build(); D, ed = signatures(g)
        r = {"family": fam, "param": par, "N": len(g["nodes"]), "E": len(g["edges"]), "by_depth": per_depth(D, ed)}
        rows.append(r)
        print("  %-10s %-7s N=%5d  median|cos| by depth: %s" % (fam, par, r["N"], " ".join(
            "%s:%.3f" % (k, v["median_abs_cos"]) for k, v in r["by_depth"].items())), flush=True)
    g1 = {name: gate_closed_form(build()) for name, build in (("{7,3} L=2", lambda: build_hyperbolic(7, 3, 2)),
                                                            ("square R=6", lambda: build_square_disk(6)))}
    print("  closed-form check (max |diff|):", g1)
    return {"rows": rows, "closed_form_max_abs_diff": g1}


def score(d: dict) -> dict:
    rows = {(r["family"], r["param"]): r for r in d["rows"]}
    G1 = all(v <= 1e-10 for v in d["closed_form_max_abs_diff"].values())
    G2 = all(v["n_pairs"] == v["n_edges"] * (v["n_edges"] - 1) // 2 for r in d["rows"] for v in r["by_depth"].values())
    big = {fam: rows[(fam, par)]["by_depth"] for fam, par in LARGEST.items()}
    med = lambda fam, k: big[fam][str(k)]["median_abs_cos"] if str(k) in big[fam] else None
    hyp = ["{7,3}", "{8,3}", "{5,4}", "{6,4}", "{4,5}"]
    P1 = True
    for k in (3, 4, 5):
        hs = [med(h, k) for h in hyp if med(h, k) is not None]
        for fl in ("square", "triangular"):
            if med(fl, k) is not None and hs:
                P1 &= med(fl, k) > max(hs)
    ratios = [med("square", k) / med("{7,3}", k) for k in range(1, 6)]
    P2 = all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1))
    f3 = lambda fam: big[fam]["3"]["eff_dim_fraction"]
    P3 = all(f3(h) >= 1.5 * max(f3("square"), f3("triangular")) for h in hyp if "3" in big[h])
    m1 = [med(f, 1) for f in LARGEST]
    P4 = max(m1) / min(m1) < 2
    return {"G1": G1, "G2": G2, "P1": P1, "P2": P2, "P3": P3, "P4": P4,
            "ratio_square_over_73_by_depth": [round(x, 3) for x in ratios],
            "eff_dim_fraction_depth3": {f: round(f3(f), 4) for f in LARGEST if "3" in big[f]},
            "median_abs_cos_depth1_spread": round(max(m1) / min(m1), 3)}


def figure(d):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    col = {"{7,3}": "C0", "{8,3}": "C3", "{5,4}": "C4", "{6,4}": "C5", "{4,5}": "C6", "square": "C1", "triangular": "C2"}
    for r in d["rows"]:
        if r["param"] != LARGEST[r["family"]]:
            continue
        ks = sorted(int(k) for k in r["by_depth"]); hyp = r["family"].startswith("{")
        st = dict(color=col[r["family"]], ls="-" if hyp else "--", marker="o" if hyp else "s", ms=4, lw=0.9, label=r["family"] + " " + r["param"])
        axes[0].plot(ks, [r["by_depth"][str(k)]["median_abs_cos"] for k in ks], **st)
        axes[1].plot(ks, [r["by_depth"][str(k)]["eff_dim_fraction"] for k in ks], **st)
    axes[0].set_xlabel("edge depth"); axes[0].set_ylabel("median |cos| between equal-depth Jacobian columns"); axes[0].set_yscale("log")
    axes[1].set_xlabel("edge depth"); axes[1].set_ylabel("effective dimension fraction PR/n"); axes[1].set_yscale("log")
    axes[0].legend(fontsize=7, frameon=False); fig.tight_layout(); fig.savefig(FIG)


def main() -> int:
    d = run(); d["verdicts"] = score(d); figure(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
