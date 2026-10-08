#!/usr/bin/env python3
"""PREREGISTRATION_24.md: momentum-resolved conditioning of the DtN Jacobian on the square cylinder. Translation
invariance makes the Jacobian block-diagonal in total momentum q = 2 pi i / W; the picture of PREREGISTRATION_23.md
(refined after its first run) predicts, for every block, the rate at which its smallest singular value decays with depth,
and that the global minimum sits at q = pi. Writes data/momentum_resolved_rates_on_the_cylinder.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import jacobian  # noqa: E402
from exp23_cylinder_exponential_sum_picture import build_cylinder  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "momentum_resolved_rates_on_the_cylinder.json"
H = 14
FLOOR = 12.5                    # block-wise log10 kappa limit
D_FIT_MIN = 3
QFRACS = [(8, "pi/6"), (16, "pi/3"), (24, "pi/2"), (32, "2pi/3"), (40, "5pi/6"), (48, "pi")]   # W = 96 indices i: q = 2 pi i / W
# preregistered: refined exponential-sum rate per block, from `predicted_rate` below (evaluated before the run)
PREREG_RATE = {"8": 1.0192, "16": 1.2369, "24": 1.4249, "32": 1.5827, "40": 1.7158, "48": 1.8327}   # evaluated by predicted_rate(96, i), no measurement
PRED_GLOBAL = 1.8327            # predicted global rate = rate at q = pi (W = 64 gives the same: 1.8327)


def kappa_k(k):
    return np.arccosh(2.0 - np.cos(k))


def predicted_rate(W: int, i: int) -> float:
    """log10(1/zmax) + log10(rho(a)), nodes z_n = exp(-(kappa(k_n) + kappa(q - k_n))) on the discrete mode set k_n = 2 pi n / W,
    a = zmin/zmax, rho = x + sqrt(x^2 - 1), x = (3 + a)/(1 - a) (Chebyshev growth on [a, 1])."""
    n = np.arange(W); k = 2 * np.pi * n / W; q = 2 * np.pi * i / W
    z = np.exp(-(kappa_k(k) + kappa_k(q - k)))
    zmax, zmin = z.max(), z.min(); a = zmin / zmax; x = (3 + a) / (1 - a)
    return float(np.log10(1.0 / zmax) + np.log10(x + np.sqrt(x * x - 1)))


def columns_by_depth(el, types, W, kind):
    """Index array C[r, j] of the columns of the given edge type at depth r and lateral position j."""
    sel = {}
    for e, ((a, b), t) in enumerate(zip(el, types)):
        if t != kind:
            continue    # (kind "v": vertical edges; kind "h": horizontal edges, including the boundary row's own)
        r = a // W
        # horizontal edge (r, j)-(r, j+1 mod W): the wrap-around edge is stored as (r*W, r*W + W - 1) and carries label j = W - 1
        j = (W - 1) if (t == "h" and b - a == W - 1) else a % W
        sel[(r, j)] = e
    R = 1 + max(r for r, _ in sel)
    assert len(sel) == R * W == len(set(sel.values())), "column labelling is not one-to-one"
    return np.array([[sel[(r, j)] for j in range(W)] for r in range(R)])


def block_matrices(J, C, W):
    """M[i] = (rows x R) complex matrix: J restricted to the columns at depth r, Fourier-transformed over the lateral
    position with wave number i. Its singular values are those of block i; the union over i is the spectrum of J[:, C]."""
    Jr = J[:, C]                               # rows x R x W
    F = np.fft.fft(Jr, axis=2) / np.sqrt(W)
    return [F[:, :, i] for i in range(W)]


def sigma_min_by_depth(Mi, dmax):
    out = []
    for d in range(dmax + 1):
        s = np.linalg.svd(Mi[:, : d + 1], compute_uv=False)
        out.append((float(s[0]), float(s[-1])))
    return out


def slope(ds, vals):
    ds = np.array(ds, float); vals = np.array(vals, float)
    sel = ds >= D_FIT_MIN
    return float(np.polyfit(ds[sel], vals[sel], 1)[0]) if sel.sum() >= 3 else None


def analyse(W, kind, with_all_blocks=True):
    g, el, types = build_cylinder("square", W, H)
    n = len(g["nodes"]); J = jacobian(n, el, np.ones(len(el)), np.arange(W))
    C = columns_by_depth(el, types, W, kind)
    dmax = min(C.shape[0] - 1, 11)
    Ms = block_matrices(J, C, W)
    res = {"W": W, "kind": kind, "blocks": {}}
    for i in range(0, W // 2 + 1):          # q and W - i have identical singular values
        sm = sigma_min_by_depth(Ms[i], dmax)
        ds = [d for d, (smax, smin) in enumerate(sm) if smin > 0 and np.log10(smax / smin) <= FLOOR]
        res["blocks"][str(i)] = {"d": ds, "log10_sigma_min": [float(np.log10(sm[d][1])) for d in ds],
                                 "log10_sigma_max": [float(np.log10(sm[d][0])) for d in ds],
                                 "rate": slope(ds, [-np.log10(sm[d][1]) for d in ds])}
    # global minimum over blocks at every depth
    res["argmin_q_by_depth"] = {}
    for d in range(dmax + 1):
        vals = {i: np.log10(sigma_min_by_depth_cached(Ms[i], d)) for i in range(W // 2 + 1)}
        res["argmin_q_by_depth"][str(d)] = int(min(vals, key=vals.get))
    return res, J, C


_cache = {}


def sigma_min_by_depth_cached(Mi, d):
    key = (id(Mi), d)
    if key not in _cache:
        _cache[key] = float(np.linalg.svd(Mi[:, : d + 1], compute_uv=False)[-1])
    return _cache[key]


def gate_union(W=32, dd=4):
    """The union of block singular values equals the explicit SVD of the vertical-edge Jacobian restricted to depth <= dd."""
    g, el, types = build_cylinder("square", W, 8)
    n = len(g["nodes"]); J = jacobian(n, el, np.ones(len(el)), np.arange(W))
    C = columns_by_depth(el, types, W, "v")[: dd + 1]
    full = np.sort(np.linalg.svd(J[:, C.ravel()], compute_uv=False))
    Ms = block_matrices(J, C, W)
    blk = np.sort(np.concatenate([np.linalg.svd(Mi, compute_uv=False) for Mi in Ms]))
    return float(np.abs(full - blk).max() / full.max())


def run() -> dict:
    out = {"gate_union": gate_union(), "runs": {}}
    print("  union-of-blocks check:", out["gate_union"], flush=True)
    for W, kind in ((64, "v"), (96, "v"), (96, "h")):
        res, _, _ = analyse(W, kind)
        out["runs"]["%s W=%d" % (kind, W)] = res
        print("  %s W=%d: argmin q by depth %s | block rates %s" % (kind, W, res["argmin_q_by_depth"], {i: (None if res["blocks"][str(i)]["rate"] is None else round(res["blocks"][str(i)]["rate"], 3)) for i in ([8, 16, 24, 32, 40, 48] if W == 96 else [W // 2])}), flush=True)
    return out


def score(d: dict) -> dict:
    R = d["runs"]
    G1 = d["gate_union"] <= 1e-8
    # global rate from the block machinery on vertical edges, W = 96: slope of the minimum over blocks of log10 sigma_min
    def global_rate(key):
        res = R[key]; ds = sorted(int(x) for x in res["argmin_q_by_depth"])
        vals = []
        for dd in ds:
            vals.append(min(res["blocks"][str(i)]["log10_sigma_min"][res["blocks"][str(i)]["d"].index(dd)] for i in range(len(res["blocks"])) if dd in res["blocks"][str(i)]["d"]))
        sel = [x for x in ds if x >= D_FIT_MIN and x <= 7]
        return float(np.polyfit(sel, [-v for x, v in zip(ds, vals) if x in sel], 1)[0])
    gr = {k: global_rate(k) for k in R}
    G2 = all(abs(gr[k] - e) <= 0.08 for k, e in (("v W=64", 1.7928), ("v W=96", 1.7829)))   # explicit-SVD rates of PREREGISTRATION_23's run
    P1 = all(int(R["v W=%d" % W]["argmin_q_by_depth"][str(dd)]) == W // 2 for W in (64, 96) for dd in range(4, 8) if str(dd) in R["v W=%d" % W]["argmin_q_by_depth"])
    meas = {str(i): R["v W=96"]["blocks"][str(i)]["rate"] for i, _ in QFRACS}
    rel = {k: (None if meas[k] is None else abs(meas[k] - PREREG_RATE[k]) / PREREG_RATE[k]) for k in PREREG_RATE}
    P2 = all(v is not None and v <= 0.15 for v in rel.values())
    P3 = abs(gr["h W=96"] - PRED_GLOBAL) / PRED_GLOBAL <= 0.10
    return {"G1": bool(G1), "G2": bool(G2), "P1": bool(P1), "P2": bool(P2), "P3": bool(P3), "global_rates": {k: round(v, 4) for k, v in gr.items()},
            "block_rates_W96": {k: (None if v is None else round(v, 4)) for k, v in meas.items()}, "relative_error_W96": {k: (None if v is None else round(v, 4)) for k, v in rel.items()},
            "predicted_W96": PREREG_RATE, "predicted_global": PRED_GLOBAL,
            "argmin_q_W96": R["v W=96"]["argmin_q_by_depth"], "argmin_q_W64": R["v W=64"]["argmin_q_by_depth"]}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
