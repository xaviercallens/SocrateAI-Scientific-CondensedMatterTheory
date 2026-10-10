#!/usr/bin/env python3
"""PREREGISTRATION_28.md: curvature on a polar-grid disk. Levels l = 0..H at radii r_l = R - l h, h = R dtheta, dtheta = 2 pi / W;
tangential conductance at level l: R / r_l; radial conductance between l and l+1: r_{l+1/2} / R; boundary = level 0; insulating inner
end at level H. Exact zigzag block (total angular momentum W/2) of the radial-edge columns in 140-digit arithmetic. Writes
data/curvature_on_a_polar_grid_disk.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "curvature_on_a_polar_grid_disk.json"
CARD25 = HERE / "data" / "exact_semi_infinite_blocks_asymptotic_ra.json"
DPS = 140
# (R, W, H, deepest level): H puts the insulating inner end at about two cell sizes from the centre
RUNS = [(48, 304, 46, 24), (96, 608, 94, 24)]
H_ALT = (48, 304, 44, 24)               # inner-end sensitivity check (gate G2)
# preregistered, evaluated before the run by prediction functions only: local-strip (WKB) growth of the increment,
# g_w(R, l) = G(lambda_l) / G(lambda_3) - 1, lambda_l = R^2 / (r_l r_{l+1/2}), G = Green exponent of the aligned strip's zigzag block
G_WKB = {"48|12": 0.0474, "48|24": 0.172, "96|24": 0.0529}
BAND = (0.55, 0.90)                     # exact growth / WKB growth, informed by pilots at R = 24 and 32 (0.68 to 0.75)


def params(R, W, H):
    h = R * 2 * mp.pi / W
    r = [R - l * h for l in range(H + 1)]
    return r, [R / r[l] for l in range(H + 1)], [(r[l] + r[l + 1]) / 2 / R for l in range(H)]


def mode_amplitudes(R, W, H):
    r, gt, gr = params(R, W, H)
    A = []
    for m in range(W // 2 + 1):
        c = 2 * (1 - mp.cos(2 * mp.pi * m / W))
        diag, sub, sup, rhs = [], [], [], []
        for l in range(1, H + 1):
            if l < H:
                diag.append(gr[l - 1] + gr[l] + gt[l] * c); sup.append(-gr[l])
            else:
                diag.append(gr[H - 1] + gt[H] * c); sup.append(mp.mpf(0))
            sub.append(-gr[l - 1]); rhs.append(gr[0] if l == 1 else mp.mpf(0))
        n = H; cp = [mp.mpf(0)] * n; dp = [mp.mpf(0)] * n
        cp[0] = sup[0] / diag[0]; dp[0] = rhs[0] / diag[0]
        for i in range(1, n):
            den = diag[i] - sub[i] * cp[i - 1]
            cp[i] = sup[i] / den; dp[i] = (rhs[i] - sub[i] * dp[i - 1]) / den
        x = [mp.mpf(0)] * n; x[-1] = dp[-1]
        for i in range(n - 2, -1, -1):
            x[i] = dp[i] - cp[i] * x[i + 1]
        A.append([mp.mpf(1)] + x)
    return A


def block(A, W, M, dmax):
    fold = lambda m: min(m % W, (-m) % W)
    rows = []
    for n in range(W):
        a1, a2 = A[fold(n)], A[fold(M - n)]
        rows.append([(a1[l] - a1[l + 1]) * (a2[l] - a2[l + 1]) for l in range(dmax + 1)])
    mean = [sum(rows[n][l] for n in range(W)) / W for l in range(dmax + 1)]
    return mp.matrix([[rows[n][l] - mean[l] for l in range(dmax + 1)] for n in range(W)])


def log10_sigma_min(V, d):
    Vd = V[:, : d + 1]
    Gi = mp.inverse(Vd.T * Vd)
    v = mp.matrix([1] * (d + 1)); lam = mp.mpf(1)
    for _ in range(80):
        w = Gi * v; nrm = mp.norm(w); v = w / nrm
        if abs(nrm - lam) < mp.mpf(10) ** (-30) * nrm:
            lam = nrm; break
        lam = nrm
    return float(-mp.log10(lam) / 2)


def explicit_block(R, W, H, dd):
    from hyperbolic_network import jacobian
    import exp24_momentum_resolved_rates_on_the_cylinder as e24
    from exp23_cylinder_exponential_sum_picture import build_cylinder
    r, gt, gr = params(R, W, H)
    g, el, types = build_cylinder("square", W, H)
    gv = np.array([float(gt[a // W]) if t == "h" else float(gr[a // W]) for (a, b), t in zip(el, types)])
    J = jacobian(len(g["nodes"]), el, gv, np.arange(W))
    C = e24.columns_by_depth(el, types, W, "v")[: dd + 1]
    M = e24.block_matrices(J, C, W)[W // 2]
    return [float(np.log10(s[1])) for s in e24.sigma_min_by_depth(M, dd)]


def increments(R, W, H, dmax):
    A = mode_amplitudes(R, W, H)
    V = block(A, W, W // 2, dmax)
    s = [log10_sigma_min(V, d) for d in range(dmax + 1)]
    return s


def run() -> dict:
    mp.mp.dps = DPS
    out = {"dps": DPS, "runs": {}}
    # G1: exact against explicit on a small disk, increments d <= 5
    A = mode_amplitudes(10, 64, 8)
    ex = [log10_sigma_min(block(A, 64, 32, 5), d) for d in range(6)]
    ei = explicit_block(10, 64, 8, 5)
    out["G1"] = {"exact_log10_sigma_min": ex, "explicit_log10_sigma_min": ei}
    print("  G1 increments exact   :", [round(ex[d] - ex[d + 1], 4) for d in range(5)])
    print("  G1 increments explicit:", [round(ei[d] - ei[d + 1], 4) for d in range(5)], flush=True)
    for R, W, H, dmax in RUNS:
        s = increments(R, W, H, dmax)
        out["runs"]["%d" % R] = {"R": R, "W": W, "H": H, "log10_sigma_min": s}
        print("  R=%d W=%d H=%d: increments l=1..%d: %s" % (R, W, H, dmax, [round(s[l - 1] - s[l], 4) for l in range(1, dmax + 1)]), flush=True)
    R, W, H, dmax = H_ALT
    s = increments(R, W, H, dmax)
    out["inner_end_check"] = {"R": R, "W": W, "H": H, "log10_sigma_min": s}
    print("  R=%d H=%d (inner-end check) I(12)/I(3) = %.4f" % (R, H, (s[11] - s[12]) / (s[2] - s[3])), flush=True)
    return out


def score(d: dict) -> dict:
    ex, ei = d["G1"]["exact_log10_sigma_min"], d["G1"]["explicit_log10_sigma_min"]
    G1 = all(abs((ex[k] - ex[k + 1]) - (ei[k] - ei[k + 1])) <= 0.005 for k in range(5))
    inc = lambda s, l: s[l - 1] - s[l]
    runs = {k: v["log10_sigma_min"] for k, v in d["runs"].items()}
    alt = d["inner_end_check"]["log10_sigma_min"]
    g = lambda s, l: inc(s, l) / inc(s, 3) - 1
    main = runs["48"]
    G2 = abs((inc(main, 12) / inc(main, 3)) - (inc(alt, 12) / inc(alt, 3))) / (inc(main, 12) / inc(main, 3)) <= 0.02
    meas = {"48|12": g(runs["48"], 12), "48|24": g(runs["48"], 24), "96|24": g(runs["96"], 24)}
    ratio = {k: meas[k] / G_WKB[k] for k in meas}
    P1 = all(BAND[0] <= v <= BAND[1] for v in ratio.values())
    P2 = abs(g(runs["48"], 12) - g(runs["96"], 24)) / g(runs["48"], 12) <= 0.20
    cyl = json.loads(CARD25.read_text())["W384"]["48"]["log10_sigma_min"]
    flat3 = cyl[2] - cyl[3]
    P3 = abs(inc(runs["96"], 3) - flat3) / flat3 <= 0.02
    P4 = all(meas[k] > 0.01 for k in meas)
    return {"G1": bool(G1), "G2": bool(G2), "P1": bool(P1), "P2": bool(P2), "P3": bool(P3), "P4": bool(P4),
            "growth_measured": {k: round(v, 4) for k, v in meas.items()}, "growth_wkb": G_WKB, "ratio_exact_over_wkb": {k: round(v, 4) for k, v in ratio.items()},
            "band": list(BAND), "increment_l3_R96": round(inc(runs["96"], 3), 4), "increment_l3_cylinder": round(flat3, 4),
            "growth_R48_l12_vs_R96_l24": [round(g(runs["48"], 12), 4), round(g(runs["96"], 24), 4)],
            "inner_end_ratio_I12_over_I3": [round(inc(main, 12) / inc(main, 3), 4), round(inc(alt, 12) / inc(alt, 3), 4)]}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
