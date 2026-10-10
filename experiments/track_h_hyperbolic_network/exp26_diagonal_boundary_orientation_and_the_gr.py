#!/usr/bin/env python3
"""PREREGISTRATION_26.md: the square lattice with a boundary along the diagonal. Periodic strip along (1,1): rows s = x - y,
W nodes per row (j = x mod W), node (s,j) joined to (s+1,j) [edge type B] and (s+1,j+1) [edge type A], no edges inside a row.
Exact semi-infinite momentum blocks of the type-B edge columns in 140-digit arithmetic, with the explicit double-precision
reference as validity gate. Writes data/diagonal_boundary_orientation_and_the_gr.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "diagonal_boundary_orientation_and_the_gr.json"
DPS, DMAX, D_LO, D_HI = 140, 25, 15, 25
W0, W1, W2, DEPTH_ALL = 96, 384, 768, 20
SIX = [8, 16, 24, 32, 40, 48]           # labels = indices at W = 96; scaled by W1 / W0 (as in PREREGISTRATION_25)
# preregistered, evaluated before the run by prediction functions only (Green exponent of the interval of node moduli):
PREREG_GREEN_DIAG = {"8": 0.8488, "16": 0.9384, "24": 1.0361, "32": 1.1439, "40": 1.2647, "48": 1.4027}
# rival: the aligned-boundary Green values of PREREGISTRATION_25 divided by sqrt(2) (graph depth is the L1 distance)
RIVAL_SQRT2 = {"8": 0.6792, "16": 0.8048, "24": 0.9181, "32": 1.0148, "40": 1.0966, "48": 1.1686}
ALIGNED = {"8": 0.9605, "16": 1.1381, "24": 1.2984, "32": 1.4352, "40": 1.5508, "48": 1.6527}


def lam(k):
    """Root with |lam| < 1 of (1 + e^{ik}) lam^2 - 4 lam + (1 + e^{-ik}) = 0, in the numerically stable form 2C/(4 + sqrt(16 - 4AC))."""
    A = 1 + mp.e ** (1j * k); C = 1 + mp.e ** (-1j * k)
    disc = mp.sqrt(16 - 4 * A * C)
    if mp.re(disc) < 0:
        disc = -disc
    return 2 * C / (4 + disc)


def block(W, i, dmax):
    """Type-B edge columns, momentum i: V[n, r] = a_n z_n^r, a_n = (1 - lam(k_n))(1 - lam(q - k_n)), z_n = lam(k_n) lam(q - k_n);
    the position-diagonal direction (uniform in n) is projected out."""
    q = 2 * mp.pi * i / W
    rows = []
    for n in range(W):
        k = 2 * mp.pi * n / W
        la, lb = lam(k), lam(q - k)
        a = (1 - la) * (1 - lb); z = la * lb
        rows.append([a * z ** r for r in range(dmax + 1)])
    colmean = [sum(rows[n][r] for n in range(W)) / W for r in range(dmax + 1)]
    return mp.matrix([[rows[n][r] - colmean[r] for r in range(dmax + 1)] for n in range(W)])


def log10_sigma_min(V, d):
    Vd = V[:, : d + 1]
    G = Vd.H * Vd
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


def build_strip(W, H):
    """Rows 0..H of W nodes; node (s,j) -> (s+1,j) [type B] and (s+1,(j+1) mod W) [type A]. Boundary = row 0."""
    idx = lambda s, j: s * W + (j % W)
    edges, types = [], []
    for s in range(H):
        for j in range(W):
            edges.append((idx(s, j), idx(s + 1, j))); types.append("B")
            a, b = idx(s, j), idx(s + 1, j + 1)
            edges.append((min(a, b), max(a, b))); types.append("A")
    return {"nodes": np.arange((H + 1) * W), "edges": edges}, edges, types


def explicit_block(W=96, H=40, dd=5):
    """Explicit double-precision zigzag block of the type-B columns: log10 sigma_min(d), d = 0..dd."""
    from hyperbolic_network import jacobian
    g, el, types = build_strip(W, H)
    J = jacobian(len(g["nodes"]), el, np.ones(len(el)), np.arange(W))
    cols = np.zeros((dd + 1, W), dtype=int)
    for e, ((a, b), t) in enumerate(zip(el, types)):
        if t == "B" and a // W <= dd:
            cols[a // W, a % W] = e
    F = np.fft.fft(J[:, cols], axis=2) / np.sqrt(W)           # rows x (dd+1) x W
    M = F[:, :, W // 2]
    return [float(np.log10(np.linalg.svd(M[:, : d + 1], compute_uv=False)[-1])) for d in range(dd + 1)]


def run() -> dict:
    mp.mp.dps = DPS
    out = {"dps": DPS, "window": [D_LO, D_HI], "widths": [W0, W1, W2], "W384": {}, "W768_pi": {}}
    V0 = block(W0, W0 // 2, 6)
    sig0 = [log10_sigma_min(V0, d) for d in range(7)]
    expl = explicit_block()
    out["G1"] = {"explicit_H40_log10_sigma_min": expl, "exact_log10_sigma_min_d0_5": sig0[:6]}
    print("  G1 increments exact   :", [round(sig0[d] - sig0[d + 1], 3) for d in range(5)])
    print("  G1 increments explicit:", [round(expl[d] - expl[d + 1], 3) for d in range(5)], flush=True)
    for i0 in SIX:
        i = i0 * W1 // W0
        Vi = block(W1, i, DMAX)
        s = [log10_sigma_min(Vi, d) for d in range(DMAX + 1)]
        out["W384"][str(i0)] = {"i": i, "log10_sigma_min": s, "rate": (s[D_LO] - s[D_HI]) / (D_HI - D_LO)}
        print("  W=%d i=%d (label %d): rate %.4f ; increments d=1..%d: %s" % (W1, i, i0, out["W384"][str(i0)]["rate"], DMAX, [round(s[d - 1] - s[d], 3) for d in range(1, DMAX + 1)]), flush=True)
    at20 = {i: log10_sigma_min(block(W1, i, DEPTH_ALL), DEPTH_ALL) for i in range(0, W1 // 2 + 1)}
    out["sigma_min_at_depth20_all_blocks"] = {str(i): v for i, v in at20.items()}
    out["argmin_block_depth20"] = int(min(at20, key=at20.get))
    print("  smallest sigma_min at depth %d is block %d (zigzag is %d)" % (DEPTH_ALL, out["argmin_block_depth20"], W1 // 2), flush=True)
    V2 = block(W2, W2 // 2, DMAX)
    s2 = {d: log10_sigma_min(V2, d) for d in range(D_LO, D_HI + 1)}
    out["W768_pi"] = {"log10_sigma_min": {str(d): s2[d] for d in s2}, "rate": (s2[D_LO] - s2[D_HI]) / (D_HI - D_LO)}
    print("  W=%d zigzag rate %.4f" % (W2, out["W768_pi"]["rate"]), flush=True)
    return out


def score(d: dict) -> dict:
    ex, gi = d["G1"]["exact_log10_sigma_min_d0_5"], d["G1"]["explicit_H40_log10_sigma_min"]
    G1 = all(abs((ex[k] - ex[k + 1]) - (gi[k] - gi[k + 1])) <= 0.02 for k in range(5))
    r = {k: d["W384"][k]["rate"] for k in d["W384"]}
    pi = r["48"]
    P1 = abs(pi - PREREG_GREEN_DIAG["48"]) / PREREG_GREEN_DIAG["48"] <= 0.03
    rival_fits = abs(pi - RIVAL_SQRT2["48"]) / RIVAL_SQRT2["48"] <= 0.05
    rel = {k: abs(r[k] - PREREG_GREEN_DIAG[k]) / PREREG_GREEN_DIAG[k] for k in PREREG_GREEN_DIAG}
    P2 = all(v <= 0.05 for v in rel.values())
    P3 = d["argmin_block_depth20"] == W1 // 2
    P4 = abs(pi - ALIGNED["48"]) / ALIGNED["48"] >= 0.08          # the diagonal zigzag rate differs from the aligned one by >= 8 %
    return {"G1": bool(G1), "P1": bool(P1), "P1_rival_sqrt2_fits": bool(rival_fits), "P2": bool(P2), "P3": bool(P3), "P4": bool(P4),
            "rates_W384": {k: round(v, 4) for k, v in r.items()}, "predicted_green_diag": PREREG_GREEN_DIAG, "rival_sqrt2": RIVAL_SQRT2,
            "aligned_green": ALIGNED, "relative_error_vs_green": {k: round(v, 4) for k, v in rel.items()},
            "rate_W768_zigzag": round(d["W768_pi"]["rate"], 4), "argmin_block_depth20": d["argmin_block_depth20"]}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
