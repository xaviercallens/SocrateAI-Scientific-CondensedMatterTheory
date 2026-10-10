#!/usr/bin/env python3
"""PREREGISTRATION_20.md: tests the coherence-mechanism argument (MECHANISM_NOTE.md) on instances it has not seen:
full-class effective dimension fraction per depth and the depth-restricted condition number on {7,3} L=5, {4,5} L=7,
square R=16, triangular R=10.75. Writes data/coherence_mechanism_prediction_test.json and data/fig_mechanism_test.pdf;
score() reads the data file (and the H0-X-0011 reference values stored in it) alone."""
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
OUT = HERE / "data" / "coherence_mechanism_prediction_test.json"
FIG = HERE / "data" / "fig_mechanism_test.pdf"
REF = HERE / "data" / "coherence_mechanism_at_matched_size.json"
MAX_J_ENTRIES, LOG_KAPPA_FLOOR, EPS = int(2e8), 13.0, np.finfo(float).eps
INSTANCES = [("{7,3} L=5", lambda: build_hyperbolic(7, 3, 5)), ("{4,5} L=7", lambda: build_hyperbolic(4, 5, 7)),
             ("square R=16", lambda: build_square_disk(16)), ("triangular R=10.75", lambda: build_triangular_disk(10.75))]
HYP, FLAT = ["{7,3} L=5", "{4,5} L=7"], ["square R=16", "triangular R=10.75"]


def signatures(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    return (H[ea] - H[eb]).T, np.minimum(d[ea], d[eb]), bnd


def gram(D):
    M1 = D.T @ D; M2 = (D ** 2).T @ (D ** 2)
    return 0.5 * (M1 ** 2 - M2)


def eff_dim_fraction(Gsub):
    nrm = np.sqrt(np.diag(Gsub)); C = Gsub / np.outer(nrm, nrm)
    ev = np.linalg.eigvalsh((C + C.T) / 2)
    return float(ev.sum() ** 2 / np.sum(ev ** 2) / len(ev))


def gate_closed_form(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    J = jacobian(n, edges, np.ones(len(edges)), bnd); Jn = J / np.linalg.norm(J, axis=0)
    D, ed, _ = signatures(g); G = gram(D)
    worst = 0.0
    for k in sorted(set(int(x) for x in ed)):
        idx = np.where(ed == k)[0]
        if len(idx) < 2:
            continue
        Gs = G[np.ix_(idx, idx)]; nrm = np.sqrt(np.diag(Gs))
        worst = max(worst, float(np.max(np.abs(Gs / np.outer(nrm, nrm) - Jn[:, idx].T @ Jn[:, idx]))))
    return worst


def one_instance(name, g):
    D, ed, bnd = signatures(g)
    m, E = D.shape
    G = gram(D)
    use_J = m * (m + 1) // 2 * E <= MAX_J_ENTRIES
    J = jacobian(len(g["nodes"]), g["edges"], np.ones(E), bnd) if use_J else None
    dmax = int(ed.max())
    log_kappa, gram_floor = [], None
    for k in range(dmax + 1):
        sub = np.where(ed <= k)[0]
        if use_J:
            s = np.linalg.svd(J[:, sub], compute_uv=False); log_kappa.append(float(np.log10(s[0] / s[-1])))
        else:
            ev = np.linalg.eigvalsh(G[np.ix_(sub, sub)]); log_kappa.append(float(0.5 * np.log10(ev[-1] / ev[0])))
            if k == dmax:
                gram_floor = float(10 * EPS * ev[-1] / ev[0])
    f = {}
    for k in range(dmax + 1):
        idx = np.where(ed == k)[0]
        if len(idx) >= 2:
            f[str(k)] = {"n_edges": int(len(idx)), "eff_dim_fraction": eff_dim_fraction(G[np.ix_(idx, idx)])}
    if use_J:
        usable = [k for k in range(dmax + 1) if log_kappa[k] <= LOG_KAPPA_FLOOR]
        d_star = max(usable)
    else:
        d_star = dmax
    delta_bar = (log_kappa[d_star] - log_kappa[1]) / (d_star - 1) if d_star >= 2 else None
    r = {"name": name, "N": len(g["nodes"]), "E": int(E), "boundary": int(m), "d_max": dmax, "kappa_method": "explicit_J" if use_J else "gram",
         "log10_kappa_by_depth": log_kappa, "d_star": d_star, "delta_bar": delta_bar, "gram_floor": gram_floor, "by_depth": f}
    print("  %-19s N=%5d E=%5d d_max=%2d method=%-10s d*=%2d delta_bar=%s" % (name, r["N"], E, dmax, r["kappa_method"], d_star,
          "%.3f" % delta_bar if delta_bar is not None else "n/a"), flush=True)
    print("      log10 kappa_d:", " ".join("%.2f" % x for x in log_kappa))
    print("      f_d:", " ".join("%s:%.3f" % (k, v["eff_dim_fraction"]) for k, v in f.items()), flush=True)
    return r


def run() -> dict:
    rows = [one_instance(name, build()) for name, build in INSTANCES]
    ref = {r["name"]: r["delta_bar"] for r in json.load(open(REF))["rows"]}
    g1 = gate_closed_form(build_square_disk(6))
    print("  closed-form check square R=6:", g1)
    return {"rows": rows, "closed_form_max_abs_diff_square_R6": g1,
            "reference_H0_X_0011": {"delta_bar_square_R10": ref["square R=10"], "delta_bar_73_L4": ref["{7,3} L=4"]}}


def score(d: dict) -> dict:
    R = {r["name"]: r for r in d["rows"]}
    G1 = d["closed_form_max_abs_diff_square_R6"] <= 1e-10
    G2 = all(R[f]["d_star"] >= 4 for f in FLAT)
    G3 = all(R[h]["gram_floor"] is not None and R[h]["gram_floor"] <= 1e-5 for h in HYP)
    dfd = {}
    for f in FLAT:
        bd, dmax = R[f]["by_depth"], R[f]["d_max"]
        vals = {k: int(k) * v["eff_dim_fraction"] for k, v in bd.items() if 2 <= int(k) <= dmax - 2}
        dfd[f] = {"values": {k: round(v, 3) for k, v in vals.items()}, "ratio": round(max(vals.values()) / min(vals.values()), 3)}
    P1 = all(dfd[f]["ratio"] <= 1.5 for f in FLAT)
    fmin = {h: round(min(v["eff_dim_fraction"] for k, v in R[h]["by_depth"].items() if int(k) >= 2), 4) for h in HYP}
    P2 = all(fmin[h] >= 0.75 for h in HYP)
    db = {n: R[n]["delta_bar"] for n in R}
    ref = d["reference_H0_X_0011"]
    P3a = all(0.7 <= db[f] <= 1.5 for f in FLAT) and abs(db["square R=16"] - ref["delta_bar_square_R10"]) <= 0.2
    P3b = all(db[h] <= 0.5 for h in HYP) and db["{7,3} L=5"] <= ref["delta_bar_73_L4"] + 0.05
    return {"G1": bool(G1), "G2": bool(G2), "G3": bool(G3), "P1": bool(P1), "P2": bool(P2), "P3a": bool(P3a), "P3b": bool(P3b),
            "d_times_f": dfd, "min_f_depth_ge_2": fmin, "delta_bar": {n: round(v, 4) for n, v in db.items()},
            "d_star": {n: R[n]["d_star"] for n in R}}


def figure(d):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for r in d["rows"]:
        hyp = r["name"].startswith("{")
        st = dict(ls="-" if hyp else "--", marker="o" if hyp else "s", ms=4, lw=0.9, label=r["name"])
        ks = sorted(int(k) for k in r["by_depth"])
        axes[0].plot(ks, [r["by_depth"][str(k)]["eff_dim_fraction"] for k in ks], **st)
        ks2 = list(range(r["d_star"] + 1))
        axes[1].plot(ks2, r["log10_kappa_by_depth"][: r["d_star"] + 1], **st)
    ks = np.arange(1, 15); axes[0].plot(ks, np.minimum(1, 1.2 / ks), "k:", lw=0.8, label="1.2/d (guide)")
    axes[0].set_xlabel("edge depth"); axes[0].set_ylabel("full-class effective dimension fraction f_d"); axes[0].set_yscale("log")
    axes[1].set_xlabel("d"); axes[1].set_ylabel("log10 kappa of J restricted to depth <= d")
    axes[0].legend(fontsize=7, frameon=False); fig.tight_layout(); fig.savefig(FIG)


def main() -> int:
    d = run(); d["verdicts"] = score(d); figure(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
