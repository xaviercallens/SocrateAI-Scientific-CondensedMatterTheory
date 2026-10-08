#!/usr/bin/env python3
"""PREREGISTRATION_32.md: depth-ordered Gram-Schmidt residuals of the Jacobian columns against sigma_min and the column-cloud topology.
Writes data/depth_ordered_residuals_of_jacobian_columns.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp29_laplace_resolved_jacobian_conditioning import edge_depth, jac_s  # noqa: E402
from hyperbolic_network import build_hyperbolic, build_square_disk  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "depth_ordered_residuals_of_jacobian_columns.json"
FLOOR = 1e-12
MIN_LAYERS = 5
SLACK = 1e-9


def layer_table(g, layers=None):
    dep = edge_depth(g)
    J = jac_s(g, 0.0)
    order = np.argsort(dep, kind="stable")
    Js, ds = J[:, order], dep[order]
    Q, Rm = np.linalg.qr(Js)
    recon = float(np.linalg.norm(Q @ Rm - Js) / np.linalg.norm(Js))
    rjj = np.abs(np.diag(Rm))
    out = {}
    for k in range(1, int(dep.max()) + 1):
        cols = np.where(ds <= k)[0]
        lay = np.where(ds == k)[0]
        if len(lay) < 2:
            continue
        sv = np.linalg.svd(Js[:, cols], compute_uv=False)
        Rk = np.linalg.qr(Js[:, cols], mode="r")
        loo = 1.0 / np.linalg.norm(np.linalg.inv(Rk), axis=1)
        prev = np.where(ds < k)[0]
        if len(prev):
            Qp, _ = np.linalg.qr(Js[:, prev])
            Y = Js[:, lay] - Qp @ (Qp.T @ Js[:, lay])
        else:
            Y = Js[:, lay]
        s_e = np.linalg.norm(Y, axis=0)
        out[k] = {"n_layer": int(len(lay)), "sigma_min": float(sv[-1]), "rho": float(rjj[lay].min()), "loo_min": float(loo.min()),
                  "s_min": float(s_e.min()), "median_rel_s": float(np.median(s_e / np.linalg.norm(Js[:, lay], axis=0)))}
    return out, recon, float(np.linalg.norm(J, 2))


def slope(ks, ys):
    return float(np.polyfit(ks, ys, 1)[0])


def window(tab):
    return [k for k in tab if k >= 2 and tab[k]["sigma_min"] >= FLOOR]


def main():
    res = {"floor": FLOOR, "min_layers": MIN_LAYERS}
    # G3 known answer on a small disk
    g4 = build_square_disk(4)
    J4 = jac_s(g4, 0.0)
    G = J4.T @ J4
    loo_ref = 1.0 / np.sqrt(np.diag(np.linalg.inv(G)))
    Rm = np.linalg.qr(J4, mode="r")
    loo = 1.0 / np.linalg.norm(np.linalg.inv(Rm), axis=1)
    err = float(np.max(np.abs(loo - loo_ref) / loo_ref))
    res["G3"] = {"max_rel_err": err, "pass": bool(err <= 1e-8)}
    print("G3", res["G3"], flush=True)

    gsq = build_square_disk(16)
    tab, recon, jn = layer_table(gsq)
    res["square"] = {"R": 16, "table": tab, "recon_rel": recon, "J_norm": jn}
    res["G2"] = {"recon_rel": recon, "pass": bool(recon <= 1e-12)}
    w = window(tab)
    res["window"] = w
    if len(w) < MIN_LAYERS:
        res["WINDOW_TOO_SMALL"] = True
    lw = lambda key: [np.log10(tab[k][key]) for k in w]  # noqa: E731
    sl = {key: slope(w, lw(key)) for key in ("sigma_min", "rho", "loo_min", "s_min", "median_rel_s")}
    res["slopes"] = sl
    chain = []
    for k in w:
        t = tab[k]
        chain.append(bool(t["sigma_min"] <= t["loo_min"] * (1 + SLACK) and t["loo_min"] <= t["rho"] * (1 + SLACK) and t["rho"] <= t["s_min"] * (1 + SLACK)))
    res["G1"] = {"chain_per_layer": chain, "pass": bool(all(chain))}
    res["P1"] = {"ratio": sl["rho"] / sl["sigma_min"], "pass": bool(0.85 <= sl["rho"] / sl["sigma_min"] <= 1.15)}
    gap2 = [np.log10(tab[k]["rho"]) - np.log10(tab[k]["sigma_min"]) for k in w]
    res["P2"] = {"gaps": gap2, "pass": bool(all(-1e-9 <= x <= 1.5 for x in gap2))}
    gap3 = [np.log10(tab[k]["s_min"]) - np.log10(tab[k]["rho"]) for k in w]
    res["P3"] = {"gaps": gap3, "mean": float(np.mean(gap3)), "pass": bool(all(-1e-9 <= x <= 1.5 for x in gap3) and np.mean(gap3) >= 0.5)}
    y4 = lw("median_rel_s")
    pear = float(np.corrcoef(w, y4)[0, 1])
    res["P4"] = {"slope": sl["median_rel_s"], "pearson": pear, "pass": bool(-1.2 <= sl["median_rel_s"] <= -0.4 and pear <= -0.98)}

    h = build_hyperbolic(7, 3, 5)
    th, reconh, _ = layer_table(h)
    hk = [k for k in (1, 2, 3, 4) if k in th and th[k]["sigma_min"] >= FLOOR]
    slh = slope(hk, [np.log10(th[k]["rho"]) for k in hk]) if len(hk) >= 3 else None
    gaph = [np.log10(th[k]["rho"]) - np.log10(th[k]["sigma_min"]) for k in hk]
    res["hyperbolic_73_L5"] = {"table": th, "recon_rel": reconh, "layers": hk, "slope_rho": slh,
                               "slope_sigma_min": slope(hk, [np.log10(th[k]["sigma_min"]) for k in hk]) if len(hk) >= 3 else None, "gaps": gaph}
    res["P5"] = {"slope_hyp": slh, "slope_sq": sl["rho"],
                 "pass": bool(slh is not None and abs(slh) < abs(sl["rho"]) and all(-1e-9 <= x <= 1.5 for x in gaph))}

    c30 = json.loads((HERE / "data" / "jacobian_column_cloud_homology.json").read_text())
    lay30 = c30["square"]["layers"]
    ks30 = [k for k in w if str(k) in lay30 and lay30[str(k)]["median_death"]]
    m_slope = slope(ks30, [np.log10(lay30[str(k)]["median_death"]) for k in ks30]) if len(ks30) >= 3 else None
    res["P6"] = {"slope_residual": sl["median_rel_s"], "slope_nn_cloud": m_slope, "ratio": (abs(sl["median_rel_s"]) / abs(m_slope)) if m_slope else None,
                 "pass": bool(m_slope and abs(sl["median_rel_s"]) >= 5 * abs(m_slope))}
    OUT.write_text(json.dumps(res, indent=2, default=float), encoding="utf-8")
    print("window", w, "slopes", {k: round(v, 4) for k, v in sl.items()})
    for key in ("G1", "G2", "G3", "P1", "P2", "P3", "P4", "P5", "P6"):
        print(key, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in res[key].items() if a not in ("chain_per_layer",)})
    print("hyper layers", hk, "slope rho", slh)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
