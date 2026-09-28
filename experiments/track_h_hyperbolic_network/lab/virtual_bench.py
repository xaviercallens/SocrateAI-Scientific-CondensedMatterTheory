#!/usr/bin/env python3
"""Virtual bench for the minimal viable experiment (MVE): simulate what the ADC will record and test the
tau-fitting pipeline BEFORE building anything. Fixes the acceptance thresholds of PREREGISTRATION_13.md.

Physics (per board): resistors R_e = R(1 + tol_R u_e), capacitors C_i = C(1 + tol_C u_i), u ~ U[-1,1]; all boundary
nodes tied to one rail stepped 0 -> V0 at t=0 through a driver of output resistance R_s; interior dynamics
C_i dV_i/dt = -(L_ii V)_i - (L_ib V_b)_i, solved exactly by the generalised eigenproblem. Measurement: k probe
nodes (one per depth class) read through unity-gain buffers by an ADC of `bits` resolution over V_ref, at fs
samples/s, with additive noise of `noise_lsb` LSB rms. Analysis (fit_tau): the slowest mode is fitted from the tail
of y(t) = V0 - V(t) by weighted log-linear regression on samples with y/V0 in [Y_LO, Y_HI], averaged over probes.

Outputs lab/out/virtual_bench.json and lab/out/virtual_bench.pdf; prints the recovered-tau error percentiles per
configuration, and the spread of the TRUE tau of tolerance-perturbed boards around the nominal prediction.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.linalg import eigh  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, laplacian  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
R, C, V0, VREF = 100e3, 1e-6, 3.3, 4.096
Y_LO, Y_HI = 0.01, 0.10  # protocol window (chosen from this bench: bias <= 0.3 % at >= 12 bits); see WINDOWS for the sweep
BOARDS = (("{7,3} L=2", lambda: build_hyperbolic(7, 3, 2)), ("square R=6", lambda: build_square_disk(6)))
CONFIGS = [  # (label, bits, fs, noise_lsb, tol_R, tol_C)
    ("ideal 16b 860S/s 1%", 16, 860, 1.0, 0.01, 0.01),
    ("16b 860S/s 5%R 10%C", 16, 860, 1.0, 0.05, 0.10),
    ("12b 1kS/s 1%", 12, 1000, 1.0, 0.01, 0.01),
    ("10b 1kS/s 4LSB noise 1%", 10, 1000, 4.0, 0.01, 0.01),
    ("16b 100S/s 1%", 16, 100, 1.0, 0.01, 0.01),
]
SEEDS = 40


def board_response(g, rng, tol_R, tol_C, R_s=10.0):
    """Return (t, V_probe[k, t], tau_true, tau_nominal, probes)."""
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd)
    interior = np.setdiff1d(np.arange(n), bnd)
    gvals = 1.0 / (R * (1 + tol_R * rng.uniform(-1, 1, len(edges))))
    Cv = C * (1 + tol_C * rng.uniform(-1, 1, len(interior)))
    L = laplacian(n, edges, gvals)
    Lii, Lib = L[np.ix_(interior, interior)], L[np.ix_(interior, bnd)]
    # driver output resistance: the rail is one node between the source and all boundary nodes (Thevenin);
    # for R_s << R its effect is a rail voltage V0 * (1 - R_s * I_total/V0) ~ 1e-4 here; kept for completeness
    lam, U = eigh(Lii, np.diag(Cv))          # Lii u = lam C u ; modes decay as exp(-lam t)
    Vinf = np.linalg.solve(Lii, -(Lib @ np.full(len(bnd), V0)))
    tau_true = 1.0 / lam[0]
    # nominal prediction from the same code path with nominal parts
    Ln = laplacian(n, edges, np.full(len(edges), 1.0 / R))
    lam_n = eigh(Ln[np.ix_(interior, interior)], np.diag(np.full(len(interior), C)), eigvals_only=True)
    tau_nom = 1.0 / lam_n[0]
    probes = [int(interior[np.argmax(d[interior] == pd)]) for pd in (1, 2, 3) if (d[interior] == pd).any()]
    pidx = [int(np.where(interior == p)[0][0]) for p in probes]
    t = np.arange(0.0, 8 * tau_nom, 1.0 / 20000)  # fine grid; resampled by the ADC model
    # V(t) = Vinf + sum_k c_k u_k exp(-lam_k t) with c from V(0) = 0: coefficients in the C-orthonormal basis
    coef = U.T @ (np.diag(Cv) @ (0 - Vinf))
    V = Vinf[pidx][:, None] + (U[pidx] * coef) @ np.exp(-np.outer(lam, t))
    return t, V, tau_true, tau_nom, probes


def adc(t, V, fs, bits, noise_lsb, rng):
    ts = np.arange(0.0, t[-1], 1.0 / fs)
    Vs = np.stack([np.interp(ts, t, v) for v in V])
    lsb = VREF / 2 ** bits
    Vs = Vs + noise_lsb * lsb * rng.standard_normal(Vs.shape)
    return ts, np.clip(np.round(Vs / lsb) * lsb, 0, VREF)


WINDOWS = {"w[0.02,0.30]": (0.02, 0.30), "w[0.01,0.10]": (0.01, 0.10), "w[0.005,0.05]": (0.005, 0.05)}


def fit_tau(ts, Vs, window=(Y_LO, Y_HI)):
    """Weighted log-linear fit of y = V0 - V on the tail window; average across probes. Returns tau, per-probe list."""
    lo, hi = window
    taus = []
    for v in Vs:
        y = (V0 - v) / V0
        m = (y > lo) & (y < hi)
        if m.sum() < 8:
            continue
        w = y[m]  # weights ~ y: the log of small noisy values is noisier
        A = np.vstack([ts[m], np.ones(m.sum())]).T * w[:, None]
        slope, _ = np.linalg.lstsq(A, np.log(y[m]) * w, rcond=None)[0]
        if slope < 0:
            taus.append(-1.0 / slope)
    return (float(np.mean(taus)) if taus else float("nan")), taus


def fit_tau_2exp(ts, Vs, y_min=0.005, y_max=0.6):
    """Two-exponential fit y = a1 exp(-t/t1) + a2 exp(-t/t2) by variable projection over a grid of (t1, t2);
    returns the slower time constant averaged across probes."""
    taus = []
    for v in Vs:
        y = (V0 - v) / V0
        m = (y > y_min) & (y < y_max)
        if m.sum() < 12:
            continue
        t, yy = ts[m], y[m]
        t0 = -1.0 / np.polyfit(t, np.log(np.maximum(yy, 1e-9)), 1)[0]
        best = (np.inf, t0)
        for t1 in t0 * np.exp(np.linspace(-0.4, 0.4, 41)):
            for r in np.linspace(0.1, 0.8, 15):
                B = np.vstack([np.exp(-t / t1), np.exp(-t / (r * t1))]).T
                a, res, *_ = np.linalg.lstsq(B, yy, rcond=None)
                sse = float(res[0]) if len(res) else float(np.sum((B @ a - yy) ** 2))
                if a[0] > 0 and sse < best[0]:
                    best = (sse, t1)
        taus.append(best[1])
    return (float(np.mean(taus)) if taus else float("nan")), taus


def main():
    OUT.mkdir(exist_ok=True)
    report = {"R": R, "C": C, "V0": V0, "fit_window": [Y_LO, Y_HI], "seeds": SEEDS, "configs": []}
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for bi, (bname, build) in enumerate(BOARDS):
        g = build()
        # mode separation, nominal parts: the bias of a single-exponential tail fit is set by lambda_2/lambda_1
        n = len(g["nodes"]); bnd = boundary_nodes(g); interior = np.setdiff1d(np.arange(n), bnd)
        Ln = laplacian(n, g["edges"], np.full(len(g["edges"]), 1.0 / R))
        lam_n = eigh(Ln[np.ix_(interior, interior)], np.diag(np.full(len(interior), C)), eigvals_only=True)
        report.setdefault("mode_ratio_lambda2_over_lambda1", {})[bname] = float(lam_n[1] / lam_n[0])
        print("%s: lambda_2/lambda_1 = %.2f (second mode is exp(-%.2f t/tau))" % (bname, lam_n[1] / lam_n[0], lam_n[1] / lam_n[0]))
        for cname, bits, fs, nl, tr, tc in CONFIGS:
            errs = {k: [] for k in list(WINDOWS) + ["2exp"]}; spread = []
            for s in range(SEEDS):
                rng = np.random.default_rng(1000 + s)
                t, V, tau_true, tau_nom, probes = board_response(g, rng, tr, tc)
                ts, Vs = adc(t, V, fs, bits, nl, rng)
                for wname, win in WINDOWS.items():
                    errs[wname].append(fit_tau(ts, Vs, win)[0] / tau_true - 1)
                errs["2exp"].append(fit_tau_2exp(ts, Vs)[0] / tau_true - 1)
                spread.append(tau_true / tau_nom - 1)
                if s == 0 and cname.startswith("ideal"):
                    for k, p in enumerate(probes):
                        axes[bi].plot(ts, Vs[k], lw=0.8, label="probe node %d" % p)
                    axes[bi].axvline(tau_nom, color="grey", lw=0.6); axes[bi].text(tau_nom, 0.2, r"$\tau$", fontsize=8)
            spread = np.array(spread)
            row = {"board": bname, "config": cname, "bits": bits, "fs": fs, "noise_lsb": nl, "tol_R": tr, "tol_C": tc,
                   "tau_nominal_s": tau_nom, "true_tau_spread_p95_abs": float(np.percentile(np.abs(spread), 95)), "fits": {}}
            line = "%-11s %-26s" % (bname, cname)
            for k, e in errs.items():
                e = np.array(e, float)
                row["fits"][k] = {"err_median": float(np.nanmedian(e)), "err_p95_abs": float(np.nanpercentile(np.abs(e), 95)),
                                  "failures": int(np.isnan(e).sum())}
                line += "  %s: %+.2f%% (p95 %.2f%%)" % (k, 100 * row["fits"][k]["err_median"], 100 * row["fits"][k]["err_p95_abs"])
            report["configs"].append(row)
            print(line + "  | true-tau spread p95 %.2f%%" % (100 * row["true_tau_spread_p95_abs"]))
        axes[bi].set_title(bname + ": simulated ADC record (16 bit, 860 S/s, 1 % parts)", fontsize=9)
        axes[bi].set_xlabel("t (s)"); axes[bi].set_ylabel("V (V)"); axes[bi].legend(fontsize=7, frameon=False)
    fig.tight_layout(); fig.savefig(OUT / "virtual_bench.pdf")
    (OUT / "virtual_bench.json").write_text(json.dumps(report, indent=1))
    print("wrote", OUT / "virtual_bench.json")


if __name__ == "__main__":
    main()
