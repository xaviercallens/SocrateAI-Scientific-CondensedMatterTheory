#!/usr/bin/env python3
"""PREREGISTRATION_25.md: exact semi-infinite momentum blocks of the square-cylinder Jacobian in high precision.
Block at total momentum q = 2 pi i / W: V[n, r] = a_n z_n^r with z_n = z1(k_n) z1(q - k_n), a_n = (1 - z1(k_n))(1 - z1(q - k_n)),
z1(k) = exp(-acosh(2 - cos k)), k_n = 2 pi n / W, with the position-diagonal direction (uniform in n) projected out
(strictly upper-triangular data). Rates = mean per-row decay of sigma_min at depths 20..30. Writes
data/exact_semi_infinite_blocks_asymptotic_ra.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "exact_semi_infinite_blocks_asymptotic_ra.json"
CARD24 = HERE / "data" / "momentum_resolved_rates_on_the_cylinder.json"
DPS, DMAX, D_LO, D_HI = 140, 30, 20, 30
SIX = [(8, "pi/6"), (16, "pi/3"), (24, "pi/2"), (32, "2pi/3"), (40, "5pi/6"), (48, "pi")]
# preregistered: potential-theory (Green function) value G(q) of the interval [zmin, zmax] of the block's nodes, evaluated
# before the run by the prediction function in this file (green_rate); and the rival closed form of PREREGISTRATION_24
PREREG_GREEN = {"8": 0.9605, "16": 1.1381, "24": 1.2984, "32": 1.4352, "40": 1.5508, "48": 1.6527}
RIVAL_OLD = {"8": 1.0192, "16": 1.2369, "24": 1.4249, "32": 1.5827, "40": 1.7158, "48": 1.8327}


def z1(k):
    return mp.e ** (-mp.acosh(2 - mp.cos(k)))


def block(W, i, dmax):
    """Rows n = 0..W-1, columns r = 0..dmax, diagonal direction projected out."""
    q = 2 * mp.pi * i / W
    rows = []
    for n in range(W):
        k = 2 * mp.pi * n / W
        za, zb = z1(k), z1(q - k)
        a = (1 - za) * (1 - zb); z = za * zb
        rows.append([a * z ** r for r in range(dmax + 1)])
    colmean = [sum(rows[n][r] for n in range(W)) / W for r in range(dmax + 1)]
    return mp.matrix([[rows[n][r] - colmean[r] for r in range(dmax + 1)] for n in range(W)])


def log10_sigma_min(V, d):
    """sigma_min of the first d+1 columns = 1/sqrt(lambda_max(G^-1)), G = V^T V; the largest eigenvalue of G^-1 is well
    separated (geometric spectrum), so power iteration converges in a few steps."""
    Vd = V[:, : d + 1]
    G = Vd.T * Vd
    Gi = mp.inverse(G)
    v = mp.matrix([1] * (d + 1))
    lam = mp.mpf(1)
    for _ in range(60):
        w = Gi * v
        nrm = mp.norm(w)
        v = w / nrm
        lam_new = nrm
        if abs(lam_new - lam) < mp.mpf(10) ** (-30) * lam_new:
            lam = lam_new
            break
        lam = lam_new
    return float(-mp.log10(lam) / 2)


def green_rate(zmin, zmax):
    th = np.linspace(0, np.pi, 4001); zeta = np.exp(1j * th)
    w = (2 * zeta - (zmax + zmin)) / (zmax - zmin); s = np.sqrt(w * w - 1 + 0j)
    big = np.where(np.abs(w + s) >= np.abs(w - s), w + s, w - s)
    return float(np.log(np.abs(big)).max() / np.log(10))


def explicit_block_increments(W=96, H=40, dd=5):
    """Explicit double-precision pi block of the vertical-edge Jacobian at a large height: log10 sigma_min(d), d = 0..dd."""
    from hyperbolic_network import jacobian
    import exp24_momentum_resolved_rates_on_the_cylinder as e24
    from exp23_cylinder_exponential_sum_picture import build_cylinder
    g, el, types = build_cylinder("square", W, H)
    J = jacobian(len(g["nodes"]), el, np.ones(len(el)), np.arange(W))
    C = e24.columns_by_depth(el, types, W, "v")[: dd + 1]
    M = e24.block_matrices(J, C, W)[W // 2]
    return [float(np.log10(s[1])) for s in e24.sigma_min_by_depth(M, dd)]


def run() -> dict:
    mp.mp.dps = DPS
    out = {"dps": DPS, "dmax": DMAX, "window": [D_LO, D_HI], "W96": {}, "W192_pi": {}}
    # G1: exact block against the explicit double-precision block at a large height, d <= 5
    exact_pi = []
    V = block(96, 48, DMAX)
    sig = {d: log10_sigma_min(V, d) for d in range(0, DMAX + 1)}
    expl = explicit_block_increments()
    out["G1"] = {"explicit_H40_log10_sigma_min": expl, "exact_log10_sigma_min_d0_5": [sig[d] for d in range(6)]}
    print("  G1 increments exact   :", [round(sig[d] - sig[d + 1], 3) for d in range(5)])
    print("  G1 increments explicit:", [round(expl[d] - expl[d + 1], 3) for d in range(5)], flush=True)
    out["W96"]["48"] = {"log10_sigma_min": [sig[d] for d in range(DMAX + 1)], "rate": (sig[D_LO] - sig[D_HI]) / (D_HI - D_LO)}
    print("  pi block (W=96): increments d=1..30:", [round(sig[d - 1] - sig[d], 3) for d in range(1, DMAX + 1)], flush=True)
    for i, _ in SIX[:-1]:
        Vi = block(96, i, DMAX)
        s = {d: log10_sigma_min(Vi, d) for d in range(D_LO, D_HI + 1)}
        out["W96"][str(i)] = {"log10_sigma_min": {str(d): s[d] for d in s}, "rate": (s[D_LO] - s[D_HI]) / (D_HI - D_LO)}
        print("  block i=%d rate %.4f" % (i, out["W96"][str(i)]["rate"]), flush=True)
    # P3: which block has the smallest sigma_min at depth D_LO, all i = 0..48
    at20 = {}
    for i in range(0, 49):
        Vi = block(96, i, D_LO) if str(i) not in ("48",) else V
        at20[i] = log10_sigma_min(Vi, D_LO)
    out["sigma_min_at_depth20_all_blocks"] = {str(i): v for i, v in at20.items()}
    out["argmin_block_depth20"] = int(min(at20, key=at20.get))
    print("  smallest sigma_min at depth 20 is block", out["argmin_block_depth20"], flush=True)
    # P4: W = 192, pi block
    V2 = block(192, 96, DMAX)
    s2 = {d: log10_sigma_min(V2, d) for d in range(D_LO, D_HI + 1)}
    out["W192_pi"] = {"log10_sigma_min": {str(d): s2[d] for d in s2}, "rate": (s2[D_LO] - s2[D_HI]) / (D_HI - D_LO)}
    print("  W=192 pi block rate %.4f" % out["W192_pi"]["rate"], flush=True)
    return out


def score(d: dict) -> dict:
    ex, gi = d["G1"]["exact_log10_sigma_min_d0_5"], d["G1"]["explicit_H40_log10_sigma_min"]
    G1 = all(abs((ex[k] - ex[k + 1]) - (gi[k] - gi[k + 1])) <= 0.02 for k in range(5))
    r = {k: d["W96"][k]["rate"] for k in d["W96"]}
    pi = r["48"]
    P1 = abs(pi - PREREG_GREEN["48"]) / PREREG_GREEN["48"] <= 0.03
    rival_old = abs(pi - RIVAL_OLD["48"]) / RIVAL_OLD["48"] <= 0.02
    rel = {k: abs(r[k] - PREREG_GREEN[k]) / PREREG_GREEN[k] for k in PREREG_GREEN}
    P2 = all(v <= 0.05 for v in rel.values())
    P3 = d["argmin_block_depth20"] == 48
    P4 = abs(d["W192_pi"]["rate"] - pi) / pi <= 0.01
    # P5: finite height explains card 24's acceleration: H = 14 increment d=5->6 minus the exact increment at 5->6 >= 0.15
    c24 = json.loads(CARD24.read_text())["runs"]["v W=96"]["blocks"]["48"]
    l24 = c24["log10_sigma_min"]; inc_h14 = l24[5] - l24[6]
    inc_exact = d["W96"]["48"]["log10_sigma_min"][5] - d["W96"]["48"]["log10_sigma_min"][6]
    P5 = (inc_h14 - inc_exact) >= 0.15
    return {"G1": bool(G1), "P1": bool(P1), "P1_rival_old_formula_fits": bool(rival_old), "P2": bool(P2), "P3": bool(P3), "P4": bool(P4), "P5": bool(P5),
            "rates_W96": {k: round(v, 4) for k, v in r.items()}, "predicted_green": PREREG_GREEN, "rival_old": RIVAL_OLD,
            "relative_error_vs_green": {k: round(v, 4) for k, v in rel.items()}, "rate_W192_pi": round(d["W192_pi"]["rate"], 4),
            "argmin_block_depth20": d["argmin_block_depth20"], "increment_H14_5to6": round(inc_h14, 4), "increment_exact_5to6": round(inc_exact, 4)}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
