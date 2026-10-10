#!/usr/bin/env python3
"""PREREGISTRATION_33.md: learned persistence features (GUDHI representations) of the Jacobian column cloud as predictors of conditioning, with transfer tests.
Writes data/learned_persistence_features_of_jacobian_columns.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import gudhi
import gudhi.representations as gr
import numpy as np
from scipy.linalg import cho_solve, cholesky, solve_triangular
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth, jac_s  # noqa: E402
from exp32_depth_ordered_residuals import gram_columns  # noqa: E402
from hyperbolic_network import build_hyperbolic, build_square_disk, build_triangular_disk  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "learned_persistence_features_of_jacobian_columns.json"
FLOOR = 1e-12
TRAIN = [("square", r) for r in (8, 10, 12, 14, 16)] + [("triangular", r) for r in (8, 10, 12)]
TEST_FLAT = [("square", 18)]
TEST_HYP = [("hyperbolic73", 5), ("hyperbolic54", 4)]
BANDS = {"P1_topo_min": 0.3, "P1_resid_max": 0.2, "P2_gain": 0.1, "P3_r2": 0.5, "P3_factor": 2.0, "P4_gain": 0.05, "P5_r2": 0.5, "G1_r2": 0.1, "G2_rmse": 0.1, "G3_rel": 1e-9}


def build(kind, p):
    if kind == "square":
        return build_square_disk(p)
    if kind == "triangular":
        return build_triangular_disk(float(p))
    if kind == "hyperbolic73":
        return build_hyperbolic(7, 3, p)
    return build_hyperbolic(5, 4, p)


def diagrams(dist, maxdim=1):
    st = gudhi.RipsComplex(distance_matrix=dist, max_edge_length=2.0).create_simplex_tree(max_dimension=maxdim + 1)
    st.compute_persistence(min_persistence=-1.0)
    out = {}
    for d in range(maxdim + 1):
        pts = np.array([(b, de) for (dim, (b, de)) in st.persistence(min_persistence=-1.0) if dim == d and np.isfinite(de)])
        out[d] = pts.reshape(-1, 2) if len(pts) else np.zeros((1, 2))
    return out


def sine_dist(X):
    c2 = np.clip((X.T @ X) ** 2, 0, 1)
    return np.sqrt(np.clip(1 - c2, 0, 1))


def layers_flat(g):
    """Explicit route: unit-normalised columns, sigma_min by SVD, rho by Householder QR."""
    dep = edge_depth(g)
    J = jac_s(g, 0.0)
    order = np.argsort(dep, kind="stable")
    Js, ds = J[:, order], dep[order]
    Rm = np.linalg.qr(Js, mode="r")
    rjj = np.abs(np.diag(Rm))
    Jn = J / np.linalg.norm(J, axis=0, keepdims=True)
    rows = []
    for k in range(1, int(dep.max()) + 1):
        lay = np.where(dep == k)[0]
        lay_s = np.where(ds == k)[0]
        cols = np.where(ds <= k)[0]
        if len(lay) < 4:
            continue
        sig = float(np.linalg.svd(Js[:, cols], compute_uv=False)[-1])
        if sig < FLOOR:
            break
        prev = np.where(dep < k)[0]
        X = Jn[:, lay]
        Q, _ = np.linalg.qr(Jn[:, prev]) if len(prev) else (np.zeros((Jn.shape[0], 0)), None)
        Y = X - Q @ (Q.T @ X)
        Y = Y / np.maximum(np.linalg.norm(Y, axis=0, keepdims=True), 1e-300)
        rows.append({"k": k, "n": int(len(lay)), "sigma_min": sig, "rho": float(rjj[lay_s].min()), "DA": diagrams(sine_dist(X)), "DB": diagrams(sine_dist(Y))})
    return rows


def layers_gram(g):
    """Gram/Cholesky route for the hyperbolic tilings (as in prereg 32, Deviation 1). Clouds from Gram-matrix cosines; the residual cloud from the Schur complement."""
    dep = edge_depth(g)
    G = gram_columns(g)
    order = np.argsort(dep, kind="stable")
    Gs, ds = G[np.ix_(order, order)], dep[order]
    Gs = 0.5 * (Gs + Gs.T)
    Rm = cholesky(Gs, lower=False)
    rjj = np.diag(Rm)
    nrm = np.sqrt(np.diag(Gs))
    rows = []
    for k in range(1, int(dep.max()) + 1):
        lay = np.where(ds == k)[0]
        cols = np.where(ds <= k)[0]
        if len(lay) < 4:
            continue
        sig = float(np.sqrt(max(np.linalg.eigvalsh(Gs[np.ix_(cols, cols)])[0], 0.0)))
        if sig < FLOOR:
            break
        C = Gs[np.ix_(lay, lay)] / np.outer(nrm[lay], nrm[lay])
        dA = np.sqrt(np.clip(1 - np.clip(C ** 2, 0, 1), 0, 1))
        prev = np.where(ds < k)[0]
        if len(prev):
            Rp = cholesky(Gs[np.ix_(prev, prev)], lower=False)
            B = Gs[np.ix_(prev, lay)]
            S = Gs[np.ix_(lay, lay)] - B.T @ cho_solve((Rp, False), B)
        else:
            S = Gs[np.ix_(lay, lay)]
        S = 0.5 * (S + S.T)
        d = np.sqrt(np.clip(np.diag(S), 1e-300, None))
        Cb = S / np.outer(d, d)
        dB = np.sqrt(np.clip(1 - np.clip(Cb ** 2, 0, 1), 0, 1))
        rows.append({"k": k, "n": int(len(lay)), "sigma_min": sig, "rho": float(rjj[lay].min()), "DA": diagrams(dA), "DB": diagrams(dB)})
    return rows


class Features:
    def __init__(self):
        self.pi = {d: gr.PersistenceImage(bandwidth=0.05, resolution=[10, 10], im_range=[0, 1, 0, 1]) for d in (0, 1)}
        self.ls = {d: gr.Landscape(num_landscapes=5, resolution=20, sample_range=[0, 1]) for d in (0, 1)}
        self.atol = {d: gr.Atol(quantiser=__import__("sklearn.cluster", fromlist=["KMeans"]).KMeans(n_clusters=8, random_state=0, n_init=10)) for d in (0, 1)}

    def fit(self, rows, cloud):
        for d in (0, 1):
            self.atol[d].fit([r[cloud][d] for r in rows])
        return self

    def transform(self, rows, cloud):
        F = []
        for r in rows:
            parts = [np.array([np.median(r[cloud][0][:, 1])])]
            for d in (0, 1):
                D = r[cloud][d]
                parts += [self.pi[d].fit_transform([D])[0], self.ls[d].fit_transform([D])[0], self.atol[d].transform([D])[0]]
            F.append(np.concatenate(parts))
        return np.array(F)


def fit_models(Xtr, ytr, seed=0):
    best = None
    for a in [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]:
        # leave-one-geometry-out is approximated by 5-fold on the training rows (geometry ids are stored separately for the record)
        rid = Ridge(alpha=a)
        from sklearn.model_selection import cross_val_score
        s = cross_val_score(rid, Xtr, ytr, cv=5, scoring="neg_root_mean_squared_error").mean()
        if best is None or s > best[0]:
            best = (s, a)
    ridge = Ridge(alpha=best[1]).fit(Xtr, ytr)
    gbr = GradientBoostingRegressor(n_estimators=200, max_depth=3, random_state=seed).fit(Xtr, ytr)
    return {"ridge": ridge, "gbr": gbr, "ridge_alpha": best[1]}


def score(model, X, y):
    p = model.predict(X)
    return {"rmse": float(np.sqrt(mean_squared_error(y, p))), "r2": float(r2_score(y, p)) if len(y) > 1 else None}


def main():
    res = {"bands": BANDS, "floor": FLOOR}
    sets = {}
    for name, lst, fn in (("train", TRAIN, layers_flat), ("test_flat", TEST_FLAT, layers_flat), ("test_hyp", TEST_HYP, layers_gram)):
        rows = []
        for kind, p in lst:
            g = build(kind, p)
            rr = fn(g)
            for r in rr:
                r["geom"] = f"{kind}{p}"
            rows += rr
            print(name, kind, p, "layers", len(rr), flush=True)
        sets[name] = rows
    # G3: radius-16 square targets vs prereg 32
    c32 = json.loads((HERE / "data" / "depth_ordered_residuals_of_jacobian_columns.json").read_text())["square"]["table"]
    errs = []
    for r in sets["train"]:
        if r["geom"] == "square16" and str(r["k"]) in c32:
            errs.append(abs(r["sigma_min"] - c32[str(r["k"])]["sigma_min"]) / c32[str(r["k"])]["sigma_min"])
            errs.append(abs(r["rho"] - c32[str(r["k"])]["rho"]) / c32[str(r["k"])]["rho"])
    res["G3"] = {"max_rel_err": float(max(errs)) if errs else None, "pass": bool(errs and max(errs) <= BANDS["G3_rel"])}
    print("G3", res["G3"], flush=True)

    feats = {"A": Features().fit(sets["train"], "DA"), "B": Features().fit(sets["train"], "DB")}
    X = {}
    for s in sets:
        XA, XB = feats["A"].transform(sets[s], "DA"), feats["B"].transform(sets[s], "DB")
        X[s] = {"A": XA, "B": XB, "AB": np.hstack([XA, XB]), "depth": np.array([[r["k"]] for r in sets[s]], float),
                "median": XA[:, :1], "size": np.array([[r["n"]] for r in sets[s]], float), "rho": np.array([[np.log10(r["rho"])] for r in sets[s]])}
    y = {s: {"y1": np.array([np.log10(r["sigma_min"]) for r in sets[s]]), "y2": np.array([np.log10(r["rho"]) for r in sets[s]])} for s in sets}
    mu, sd = {}, {}
    for key in ("A", "B", "AB"):
        mu[key], sd[key] = X["train"][key].mean(0), X["train"][key].std(0) + 1e-12

    def norm(s, key):
        return (X[s][key] - mu[key]) / sd[key] if key in mu else X[s][key]

    table = {}
    for key in ("A", "B", "AB", "depth", "median", "size", "rho"):
        for tgt in ("y1", "y2"):
            m = fit_models(norm("train", key), y["train"][tgt])
            for mn in ("ridge", "gbr"):
                table[f"{key}|{tgt}|{mn}"] = {s: score(m[mn], norm(s, key), y[s][tgt]) for s in ("train", "test_flat", "test_hyp")}
            table[f"{key}|{tgt}|ridge"]["alpha"] = m["ridge_alpha"]
    res["table"] = table
    # per-geometry hyperbolic scores for the best topological model
    topo_keys = [k for k in table if k.split("|")[0] in ("A", "B", "AB") and k.split("|")[1] == "y1"]
    best_topo = min(topo_keys, key=lambda k: table[k]["test_flat"]["rmse"])
    res["best_topo_y1"] = best_topo
    kb, _, mb = best_topo.split("|")
    m = fit_models(norm("train", kb), y["train"]["y1"])[mb]
    per = {}
    for geom in sorted({r["geom"] for r in sets["test_hyp"]}):
        idx = [i for i, r in enumerate(sets["test_hyp"]) if r["geom"] == geom]
        per[geom] = score(m, norm("test_hyp", kb)[idx], y["test_hyp"]["y1"][idx])
    res["best_topo_hyp_per_geometry"] = per
    # G1 leak check, G2 seed stability
    rng = np.random.default_rng(33)
    mperm = fit_models(norm("train", kb), rng.permutation(y["train"]["y1"]))[mb]
    res["G1"] = {"r2_flat_permuted": score(mperm, norm("test_flat", kb), y["test_flat"]["y1"])["r2"]}
    res["G1"]["pass"] = bool(res["G1"]["r2_flat_permuted"] is not None and res["G1"]["r2_flat_permuted"] <= BANDS["G1_r2"])
    g2a = score(fit_models(norm("train", kb), y["train"]["y1"], seed=1)["gbr"], norm("test_flat", kb), y["test_flat"]["y1"])["rmse"]
    g2b = score(fit_models(norm("train", kb), y["train"]["y1"], seed=2)["gbr"], norm("test_flat", kb), y["test_flat"]["y1"])["rmse"]
    res["G2"] = {"rmse_seed1": g2a, "rmse_seed2": g2b, "pass": bool(abs(g2a - g2b) < BANDS["G2_rmse"])}
    # verdicts
    bt = table[best_topo]["test_flat"]["rmse"]
    rr = table["rho|y1|ridge"]["test_flat"]["rmse"]
    dr = min(table["depth|y1|ridge"]["test_flat"]["rmse"], table["depth|y1|gbr"]["test_flat"]["rmse"])
    res["P1"] = {"best_topo_rmse": bt, "rho_ridge_rmse": rr, "pass": bool(bt >= BANDS["P1_topo_min"] and rr < BANDS["P1_resid_max"])}
    res["P2"] = {"best_topo_rmse": bt, "depth_rmse": dr, "pass": bool(dr - bt >= BANDS["P2_gain"])}
    th = table[best_topo]["test_hyp"]
    res["P3"] = {"hyp_r2": th["r2"], "hyp_rmse": th["rmse"], "pass": bool(th["r2"] is not None and th["r2"] <= BANDS["P3_r2"] and th["rmse"] >= BANDS["P3_factor"] * bt)}
    bA = min(table[f"A|y1|{m_}"]["test_flat"]["rmse"] for m_ in ("ridge", "gbr"))
    bB = min(table[f"B|y1|{m_}"]["test_flat"]["rmse"] for m_ in ("ridge", "gbr"))
    res["P4"] = {"best_A": bA, "best_B": bB, "pass": bool(bA - bB <= BANDS["P4_gain"])}
    ok5 = all(table[k]["test_flat"]["rmse"] < table[k]["test_hyp"]["rmse"] for k in topo_keys)
    r54 = per.get("hyperbolic544", {}).get("r2")
    res["P5"] = {"flat_lt_hyp_all_models": ok5, "r2_54": r54, "pass": bool(ok5 and r54 is not None and r54 <= BANDS["P5_r2"])}
    res["sets"] = {s: [{"geom": r["geom"], "k": r["k"], "n": r["n"], "sigma_min": r["sigma_min"], "rho": r["rho"]} for r in sets[s]] for s in sets}
    OUT.write_text(json.dumps(res, indent=2, default=float), encoding="utf-8")
    for k in ("G1", "G2", "G3", "P1", "P2", "P3", "P4", "P5"):
        print(k, res[k])
    print("best topo", best_topo, "hyp per geometry", per)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
