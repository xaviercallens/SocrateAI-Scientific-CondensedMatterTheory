#!/usr/bin/env python3
"""PREREGISTRATION_30.md: persistent homology (GUDHI Vietoris-Rips, H0) of the Jacobian column cloud per depth layer.
Writes data/jacobian_column_cloud_homology.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import gudhi
import numpy as np
from scipy.stats import pearsonr, spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth, jac_s  # noqa: E402
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, harmonic_extension  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "jacobian_column_cloud_homology.json"
FLOOR = 1e-6
SQ_LAYERS = list(range(2, 10))
HYP_LAYERS = [1, 2, 3, 4]


def gram_columns(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    D = H[ea] - H[eb]
    M1 = D @ D.T
    M2 = (D ** 2) @ (D ** 2).T
    return 0.5 * (M1 ** 2 - M2)


def sine_distance(G):
    nrm = np.sqrt(np.clip(np.diag(G), 0, None))
    c = G / np.outer(nrm, nrm)
    c2 = c ** 2
    clipped = float(np.mean(c2 > 1.0))
    return np.sqrt(np.clip(1.0 - np.clip(c2, 0.0, 1.0), 0.0, 1.0)), clipped


def h0_deaths(dist):
    rc = gudhi.RipsComplex(distance_matrix=dist, max_edge_length=2.0)
    st = rc.create_simplex_tree(max_dimension=1)
    st.compute_persistence()
    return np.array([d for (dim, (b, d)) in st.persistence() if dim == 0 and np.isfinite(d)])


def h1_total(dist):
    if dist.shape[0] > 250:
        return None
    rc = gudhi.RipsComplex(distance_matrix=dist, max_edge_length=2.0)
    st = rc.create_simplex_tree(max_dimension=2)
    st.compute_persistence()
    return float(sum(d - b for (dim, (b, d)) in st.persistence() if dim == 1 and np.isfinite(d)))


def layer_stats(dist_full, dep, layers):
    out = {}
    for k in layers:
        idx = np.where(dep == k)[0]
        if len(idx) < 4:
            out[k] = {"n": int(len(idx)), "median_death": None}
            continue
        d = dist_full[np.ix_(idx, idx)]
        deaths = h0_deaths(d)
        out[k] = {"n": int(len(idx)), "median_death": float(np.median(deaths)), "max_death": float(deaths.max()),
                  "h1_total_persistence": h1_total(d)}
    return out


def fit(stats, layers):
    ks = [k for k in layers if stats[k]["median_death"] is not None and stats[k]["median_death"] >= FLOOR]
    ys = [np.log10(stats[k]["median_death"]) for k in ks]
    if len(ks) < 3:
        return {"ks": ks, "slope": None, "spearman": None}
    return {"ks": ks, "log10_m": ys, "slope": float(np.polyfit(ks, ys, 1)[0]), "spearman": float(spearmanr(ks, ys)[0])}


def main():
    res = {"floor": FLOOR}
    # --- G2 toy: duplicated columns
    g4 = build_square_disk(4)
    G4 = gram_columns(g4)
    dep4 = edge_depth(g4)
    idx = np.arange(len(dep4))
    G2m = np.block([[G4, G4], [G4, G4]])
    dep2 = np.concatenate([dep4, dep4])
    dist2, _ = sine_distance(G2m)
    toy = layer_stats(dist2, dep2, [k for k in range(1, int(dep4.max()) + 1)])
    toy_max = max((v["median_death"] for v in toy.values() if v["median_death"] is not None), default=None)
    res["G2"] = {"max_median_death": toy_max, "pass": bool(toy_max is not None and toy_max <= 1e-12)}

    # --- square disk
    g = build_square_disk(16)
    dep = edge_depth(g)
    G = gram_columns(g)
    dist, clipped = sine_distance(G)
    st = layer_stats(dist, dep, SQ_LAYERS)
    f = fit(st, SQ_LAYERS)
    J = jac_s(g, 0.0)
    sig = {}
    for k in SQ_LAYERS:
        cols = np.where(dep <= k)[0]
        sv = np.linalg.svd(J[:, cols], compute_uv=False)
        sig[k] = {"sigma_min": float(sv[-1]), "log10_kappa": float(np.log10(sv[0] / sv[-1]))}
    ks = f["ks"]
    p3 = float(pearsonr(f["log10_m"], [np.log10(sig[k]["sigma_min"]) for k in ks])[0]) if len(ks) >= 3 else None
    res["square"] = {"R": 16, "layers": st, "fit": f, "sigma": sig, "pearson_vs_log10_sigma_min": p3, "clipped_fraction": clipped}

    # --- random control, same layer sizes, same ambient dimension
    rng = np.random.default_rng(30)
    m = len(boundary_nodes(g))
    dim = m * (m - 1) // 2
    ctrl = {}
    for k in SQ_LAYERS:
        n_k = int((dep == k).sum())
        X = rng.standard_normal((n_k, dim))
        X /= np.linalg.norm(X, axis=1, keepdims=True)
        c2 = np.clip((X @ X.T) ** 2, 0, 1)
        ctrl[k] = {"n": n_k, "median_death": float(np.median(h0_deaths(np.sqrt(1 - c2))))}
    fc = fit(ctrl, SQ_LAYERS)
    res["control"] = {"layers": ctrl, "fit": fc}
    res["G1"] = {"slope": fc["slope"], "pass": bool(fc["slope"] is not None and abs(fc["slope"]) < 0.02)}

    # --- hyperbolic {7,3}, 5 layers
    h = build_hyperbolic(7, 3, 5)
    deph = edge_depth(h)
    Gh = gram_columns(h)
    disth, clipped_h = sine_distance(Gh)
    sth = layer_stats(disth, deph, HYP_LAYERS)
    fh = fit(sth, HYP_LAYERS)
    res["hyperbolic_73_L5"] = {"N": len(h["nodes"]), "E": len(h["edges"]), "m": int(len(boundary_nodes(h))), "d_max": int(deph.max()),
                               "layers": sth, "fit": fh, "clipped_fraction": clipped_h}
    res["G3_clipped_below_1pct"] = bool(max(clipped, clipped_h) < 0.01)

    # --- verdicts
    res["P1"] = {"spearman": f["spearman"], "pass": bool(f["spearman"] is not None and f["spearman"] <= -0.9)}
    res["P2"] = {"slope_hyp": fh["slope"], "slope_sq": f["slope"],
                 "pass": bool(fh["slope"] is not None and f["slope"] is not None and abs(fh["slope"]) < abs(f["slope"]))}
    res["P3"] = {"pearson": p3, "pass": bool(p3 is not None and p3 >= 0.9)}
    res["P4"] = {"slope": f["slope"], "pass": bool(f["slope"] is not None and -1.5 <= f["slope"] <= -0.3)}
    OUT.write_text(json.dumps(res, indent=2, default=float), encoding="utf-8")
    for k in ("G1", "G2", "G3_clipped_below_1pct", "P1", "P2", "P3", "P4"):
        print(k, res[k])
    print("square", {k: (None if v["median_death"] is None else round(v["median_death"], 6)) for k, v in st.items()}, f["slope"])
    print("hyper ", {k: (None if v["median_death"] is None else round(v["median_death"], 6)) for k, v in sth.items()}, fh["slope"])
    print("control", {k: round(v["median_death"], 4) for k, v in ctrl.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
