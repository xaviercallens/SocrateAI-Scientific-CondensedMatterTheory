#!/usr/bin/env python3
"""PREREGISTRATION_27.md: the aligned square strip (boundary along a lattice axis) with lateral conductance lambda and
vertical conductance 1. Exact semi-infinite momentum blocks of the vertical-edge columns in 220-digit arithmetic, for
lambda in {0.05, 16}; the explicit double-precision reference is the validity gate. Writes
data/aligned_strip_with_unequal_conductances.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "aligned_strip_with_unequal_conductances.json"
DPS, DMAX, D_LO, D_HI = 220, 25, 15, 25
W0, W1, W2, DEPTH_ALL = 96, 384, 768, 20
LAMS = [0.05, 16.0]
SIX = [8, 16, 24, 32, 40, 48]           # labels = indices at W = 96; scaled by W1 / W0
# preregistered, evaluated before the run by prediction functions only: Green exponent of the interval of the (positive) nodes
PREREG_GREEN = {"0.05": {"8": 1.1406, "16": 1.2331, "24": 1.3393, "32": 1.4606, "40": 1.6005, "48": 1.7649},
                "16": {"8": 1.4232, "16": 1.87, "24": 2.1442, "32": 2.314, "40": 2.4112, "48": 2.4505}}
UNIVERSAL = 1.6527                       # the lambda = 1 zigzag value (preregistration 25): the null "the rate does not depend on lambda"


def key(lam):
    return "%g" % lam


def z1(k, lam):
    return mp.e ** (-mp.acosh(1 + lam * (1 - mp.cos(k))))


def block(W, i, dmax, lam):
    q = 2 * mp.pi * i / W
    rows = []
    for n in range(W):
        k = 2 * mp.pi * n / W
        za, zb = z1(k, lam), z1(q - k, lam)
        a = (1 - za) * (1 - zb); z = za * zb
        rows.append([a * z ** r for r in range(dmax + 1)])
    colmean = [sum(rows[n][r] for n in range(W)) / W for r in range(dmax + 1)]
    return mp.matrix([[rows[n][r] - colmean[r] for r in range(dmax + 1)] for n in range(W)])


def log10_sigma_min(V, d):
    Vd = V[:, : d + 1]
    G = Vd.T * Vd
    Gi = mp.inverse(G)
    v = mp.matrix([1] * (d + 1)); lam_max = mp.mpf(1)
    for _ in range(80):
        w = Gi * v
        nrm = mp.norm(w)
        v = w / nrm
        if abs(nrm - lam_max) < mp.mpf(10) ** (-30) * nrm:
            lam_max = nrm
            break
        lam_max = nrm
    return float(-mp.log10(lam_max) / 2)


def explicit_block(lam, W=96, H=40, dd=5):
    from hyperbolic_network import jacobian
    import exp24_momentum_resolved_rates_on_the_cylinder as e24
    from exp23_cylinder_exponential_sum_picture import build_cylinder
    g, el, types = build_cylinder("square", W, H)
    gv = np.where(np.array(types) == "h", lam, 1.0)
    J = jacobian(len(g["nodes"]), el, gv, np.arange(W))
    C = e24.columns_by_depth(el, types, W, "v")[: dd + 1]
    M = e24.block_matrices(J, C, W)[W // 2]
    return [float(np.log10(s[1])) for s in e24.sigma_min_by_depth(M, dd)]


def run() -> dict:
    mp.mp.dps = DPS
    out = {"dps": DPS, "window": [D_LO, D_HI], "widths": [W0, W1, W2], "lams": {}}
    for lam in LAMS:
        rec = {"W384": {}, "W768_pi": {}}
        V0 = block(W0, W0 // 2, 5, lam)
        sig0 = [log10_sigma_min(V0, d) for d in range(6)]
        expl = explicit_block(lam)
        rec["G1"] = {"explicit_H40_log10_sigma_min": expl, "exact_log10_sigma_min_d0_5": sig0}
        print("  lambda=%g G1 increments exact %s | explicit %s" % (lam, [round(sig0[d] - sig0[d + 1], 3) for d in range(5)], [round(expl[d] - expl[d + 1], 3) for d in range(5)]), flush=True)
        for i0 in SIX:
            i = i0 * W1 // W0
            s = [log10_sigma_min(block(W1, i, DMAX, lam), d) for d in range(DMAX + 1)]
            rec["W384"][str(i0)] = {"i": i, "log10_sigma_min": s, "rate": (s[D_LO] - s[D_HI]) / (D_HI - D_LO)}
            print("  lambda=%g W=%d label %d: rate %.4f ; increments d=1..%d: %s" % (lam, W1, i0, rec["W384"][str(i0)]["rate"], DMAX, [round(s[d - 1] - s[d], 3) for d in range(1, DMAX + 1)]), flush=True)
        at20 = {i: log10_sigma_min(block(W1, i, DEPTH_ALL, lam), DEPTH_ALL) for i in range(0, W1 // 2 + 1)}
        rec["sigma_min_at_depth20_all_blocks"] = {str(i): v for i, v in at20.items()}
        rec["argmin_block_depth20"] = int(min(at20, key=at20.get))
        V2 = block(W2, W2 // 2, DMAX, lam)
        s2 = {d: log10_sigma_min(V2, d) for d in range(D_LO, D_HI + 1)}
        rec["W768_pi"] = {"log10_sigma_min": {str(d): s2[d] for d in s2}, "rate": (s2[D_LO] - s2[D_HI]) / (D_HI - D_LO)}
        print("  lambda=%g: argmin block at depth %d = %d (zigzag %d); W=%d zigzag rate %.4f" % (lam, DEPTH_ALL, rec["argmin_block_depth20"], W1 // 2, W2, rec["W768_pi"]["rate"]), flush=True)
        out["lams"][key(lam)] = rec
    return out


def score(d: dict) -> dict:
    res = {"G1": True, "P1": True, "P2": True, "P3": True, "P4": True, "P5": True}
    detail = {}
    for lam in LAMS:
        k = key(lam); rec = d["lams"][k]; pre = PREREG_GREEN[k]
        ex, gi = rec["G1"]["exact_log10_sigma_min_d0_5"], rec["G1"]["explicit_H40_log10_sigma_min"]
        res["G1"] &= all(abs((ex[j] - ex[j + 1]) - (gi[j] - gi[j + 1])) <= 0.02 for j in range(5))
        r384 = {lab: rec["W384"][lab]["rate"] for lab in rec["W384"]}; r768 = rec["W768_pi"]["rate"]
        res["P1"] &= abs(r768 - pre["48"]) / pre["48"] <= 0.03
        rel = {lab: abs(r384[lab] - pre[lab]) / pre[lab] for lab in pre}
        res["P2"] &= all(v <= 0.06 for v in rel.values())
        res["P3"] &= rec["argmin_block_depth20"] == W1 // 2
        res["P4"] &= abs(r768 - r384["48"]) / r384["48"] <= 0.03
        res["P5"] &= (r768 >= UNIVERSAL * 1.04)
        detail[k] = {"rates_W384": {a: round(b, 4) for a, b in r384.items()}, "rate_W768_zigzag": round(r768, 4), "predicted": pre,
                     "relative_error_vs_green_W384": {a: round(b, 4) for a, b in rel.items()}, "argmin_block_depth20": rec["argmin_block_depth20"]}
    return {**{a: bool(b) for a, b in res.items()}, "detail": detail, "universal_null": UNIVERSAL}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
