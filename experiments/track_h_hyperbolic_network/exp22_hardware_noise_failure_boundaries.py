#!/usr/bin/env python3
"""PREREGISTRATION_22.md: where does single-node localisation fail under hardware-like perturbations?
Offsets (exactly invisible, by the zero row sums of every signature), scalar gain drift between the two maps (curve
predicted by the noiseless decode integrated over the drift law), ADC quantisation (white-noise-equivalent brackets),
and per-channel gain mismatch (exploratory). Writes data/hardware_noise_failure_boundaries.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import build_hyperbolic, build_square_disk  # noqa: E402
from localize_defect import DICT_F  # noqa: E402
from tda_noise import noisy  # noqa: E402
import exp17_localisation_under_correlated_hardware_n as e17  # noqa: E402  (Board: dictionary, deepest class, decoder)

OUT = Path(__file__).resolve().parent / "data" / "hardware_noise_failure_boundaries.json"
EPS0, TRIALS, SEED = 3e-4, 40, 22
FS = [2.0, 1.25]
OFFSETS = [1.0, 10.0, 100.0]                       # in units of the rms entry s; three offset structures
DRIFTS = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]
BITS = [1, 2, 3, 4, 5, 6, 7, 8, 10]
CHANNEL_GAINS = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1]
BOARDS = [("{7,3} L=2", lambda: build_hyperbolic(7, 3, 2)), ("square R=6", lambda: build_square_disk(6))]
ND = len(DICT_F)
# preregistered (PREREGISTRATION_22.md): predicted top-1 under scalar gain drift sigma, from `predicted_drift` below
PREREG_DRIFT = {   # computed by `predicted_drift` alone (no Monte Carlo), before this file was committed
    "{7,3} L=2|2": [1.0, 1.0, 1.0, 0.9431, 0.6822, 0.5626, 0.3596],
    "{7,3} L=2|1.25": [1.0, 1.0, 0.9172, 0.6777, 0.5552, 0.518, 0.3466],
    "square R=6|2": [1.0, 1.0, 0.9398, 0.805, 0.5561, 0.2209, 0.0687],
    "square R=6|1.25": [1.0, 0.9996, 0.9246, 0.9316, 0.6101, 0.239, 0.0727]}
# first bit count at which the white-noise equivalence eps_eq = 2^-b / sqrt(12) is no larger than the measured eps_loc
# of H3-X-0006 (f=2: 1e-1 / 1e-2, f=1.25: 3e-2 / 3e-3 for {7,3} L=2 / square R=6)
PREREG_BHI = {"{7,3} L=2|2": 2, "square R=6|2": 5, "{7,3} L=2|1.25": 4, "square R=6|1.25": 7}


def truth_index(b, v, f):
    return int(np.where(b.interior == v)[0][0]) * ND + DICT_F.index(f)


def predicted_drift(b, f, sigma, zgrid=np.linspace(-6, 6, 4801)):
    """Noiseless expected top-1 under x = (1+delta)(P0+d_v) - P0, delta ~ N(0, sigma^2), averaged over the deepest class.
    ||x-d_k||^2 = ||x||^2 - 2 x.d_k + ||d_k||^2 is linear in delta, so the decode is a scan; the decoder returns the NODE
    after minimising over contrasts."""
    p = b.P0.ravel(); w = np.exp(-0.5 * zgrid ** 2); w /= w.sum()
    delta = sigma * zgrid
    c = np.einsum("ij,ij->i", b.flat, b.flat); bk = b.flat @ p
    total = 0.0
    for v in b.nodes:
        i_true = int(np.where(b.interior == v)[0][0]); dv = b.flat[truth_index(b, v, f)]
        a = b.flat @ (p + dv)
        S = c[None, :] - 2.0 * ((1.0 + delta)[:, None] * a[None, :] - bk[None, :])
        node_best = S.reshape(len(delta), -1, ND).min(axis=2).argmin(axis=1)
        total += float(w[node_best == i_true].sum())
    return total / len(b.nodes)


def trial_maps(b, bi, fi, v, f, t):
    rn = np.random.default_rng([SEED, bi, fi, t])                 # common random numbers across cells
    P1 = noisy(b.P0, EPS0, rn)
    P2 = noisy(b.P0 + b.flat[truth_index(b, v, f)].reshape(b.P0.shape), EPS0, rn)
    return P1, P2


def decode_plain(b, P1, P2):
    return int(np.argmin(np.linalg.norm(b.flat - (P2 - P1).ravel(), axis=1))) // ND


def cell(b, bi, fi, f, perturb, mode="plain", cell_id=0, baseline=None):
    """Returns (top1, number of trials whose decision differs from the unperturbed decision with the same noise)."""
    hit, differ, nodes = 0, 0, []
    for t in range(TRIALS):
        v = b.nodes[t % len(b.nodes)]; i_true = int(np.where(b.interior == v)[0][0])
        P1, P2 = trial_maps(b, bi, fi, v, f, t)
        if perturb is not None:
            P1, P2 = perturb(P1, P2, np.random.default_rng([SEED + 1, bi, fi, t, cell_id]))
        k = decode_plain(b, P1, P2) if mode == "plain" else b.decode(P1, P2, mode)
        nodes.append(k); hit += int(k == i_true)
        if baseline is not None:
            differ += int(k != baseline[t])
    return hit / TRIALS, differ, nodes


def run() -> dict:
    out = {"eps_iid": EPS0, "trials": TRIALS, "seed": SEED, "grids": {"offsets": OFFSETS, "drifts": DRIFTS, "bits": BITS,
           "channel_gains": CHANNEL_GAINS}, "boards": {}}
    for bi, (name, build) in enumerate(BOARDS):
        b = e17.Board(build()); s = b.s; m = int(round(b.P0.size ** 0.5))
        rec = {"s_rms": s, "boundary": m, "zero_sum": {}, "f": {}}
        rec["zero_sum"] = {"max_abs_row_sum_rel": float(np.abs(b.flat.reshape(b.flat.shape[0], m, m).sum(axis=2)).max() / np.abs(b.flat).max()),
                           "max_abs_col_sum_rel": float(np.abs(b.flat.reshape(b.flat.shape[0], m, m).sum(axis=1)).max() / np.abs(b.flat).max())}
        for fi, f in enumerate(FS):
            r = {"cells": {}, "predicted_drift": {}, "noiseless_ok": {}}
            # noiseless decode at zero perturbation, every node of the class (G3)
            r["noiseless_ok"] = all(decode_plain(b, b.P0, b.P0 + b.flat[truth_index(b, v, f)].reshape(b.P0.shape)) == int(np.where(b.interior == v)[0][0]) for v in b.nodes)
            base_hit, _, base_nodes = cell(b, bi, fi, f, None)
            r["cells"]["baseline"] = {"top1": base_hit}
            cid = 1
            for kind in ("row", "col", "both"):
                for eo in OFFSETS:
                    def off(P1, P2, rg, eo=eo, kind=kind):
                        outp = []
                        for P in (P1, P2):
                            u = rg.normal(0, eo * s, m); w = rg.normal(0, eo * s, m)
                            Q = P + (u[:, None] if kind in ("row", "both") else 0) + (w[None, :] if kind in ("col", "both") else 0)
                            outp.append(Q)
                        return outp[0], outp[1]
                    top1, differ, _ = cell(b, bi, fi, f, off, cell_id=cid, baseline=base_nodes); cid += 1
                    r["cells"]["offset_%s_%g" % (kind, eo)] = {"top1": top1, "differs_from_baseline": differ}
            for sg in DRIFTS:
                def drift(P1, P2, rg, sg=sg):
                    return P1, (1.0 + rg.normal(0, sg)) * P2
                top1, _, _ = cell(b, bi, fi, f, drift, cell_id=cid); cid += 1
                r["cells"]["drift_%g" % sg] = {"top1": top1}
                r["predicted_drift"]["%g" % sg] = predicted_drift(b, f, sg)
            if f == 2.0:
                for sg in (0.1, 0.3):
                    def drift(P1, P2, rg, sg=sg):
                        return P1, (1.0 + rg.normal(0, sg)) * P2
                    top1, _, _ = cell(b, bi, fi, f, drift, mode="gain_fitted", cell_id=cid); cid += 1
                    r["cells"]["drift_gainfit_%g" % sg] = {"top1": top1}
            for bits in BITS:
                q = 2.0 ** (-bits) * s
                def quant(P1, P2, rg, q=q):
                    return np.round(P1 / q) * q, np.round(P2 / q) * q
                top1, _, _ = cell(b, bi, fi, f, quant, cell_id=cid); cid += 1
                r["cells"]["bits_%d" % bits] = {"top1": top1}
            for eg in CHANNEL_GAINS:      # exploratory: independent per-channel row gains on the two maps
                def chan(P1, P2, rg, eg=eg):
                    return (1 + rg.normal(0, eg, m))[:, None] * P1, (1 + rg.normal(0, eg, m))[:, None] * P2
                top1, _, _ = cell(b, bi, fi, f, chan, cell_id=cid); cid += 1
                r["cells"]["channel_gain_%g" % eg] = {"top1": top1}
            rec["f"]["%g" % f] = r
            print("  %-11s f=%-4g baseline %.2f | drift top1 %s | predicted %s | bits %s | channel gain %s" % (
                name, f, base_hit, " ".join("%.2f" % r["cells"]["drift_%g" % x]["top1"] for x in DRIFTS),
                " ".join("%.2f" % r["predicted_drift"]["%g" % x] for x in DRIFTS),
                " ".join("%.2f" % r["cells"]["bits_%d" % x]["top1"] for x in BITS),
                " ".join("%.2f" % r["cells"]["channel_gain_%g" % x]["top1"] for x in CHANNEL_GAINS)), flush=True)
        out["boards"][name] = rec
    return out


def tol(pred, n):
    return 3.0 * (max(pred * (1.0 - pred), 0.0) / n) ** 0.5 + 0.05


def score(d: dict) -> dict:
    n = d["trials"]; cells = lambda bn, f: d["boards"][bn]["f"]["%g" % f]["cells"]
    keys = [(bn, f) for bn, _ in BOARDS for f in FS]
    G1 = all(cells(bn, f)["baseline"]["top1"] >= 0.9 for bn, f in keys)
    G2 = all(max(d["boards"][bn]["zero_sum"].values()) <= 1e-9 for bn, _ in BOARDS)
    G3 = all(d["boards"][bn]["f"]["%g" % f]["noiseless_ok"] for bn, f in keys)
    G4 = all(abs(d["boards"][bn]["f"]["%g" % f]["predicted_drift"]["%g" % sg] - PREREG_DRIFT["%s|%g" % (bn, f)][i]) <= 2e-3
             for bn, f in keys for i, sg in enumerate(DRIFTS))
    P1 = all(cells(bn, f)["offset_%s_%g" % (k, eo)]["differs_from_baseline"] == 0 for bn, f in keys for k in ("row", "col", "both") for eo in OFFSETS)
    worst_drift = 0.0; drift_ok = True
    for bn, f in keys:
        for i, sg in enumerate(DRIFTS):
            pred = PREREG_DRIFT["%s|%g" % (bn, f)][i]; meas = cells(bn, f)["drift_%g" % sg]["top1"]
            worst_drift = max(worst_drift, abs(meas - pred)); drift_ok &= abs(meas - pred) <= tol(pred, n)
    P2 = drift_ok
    P3 = all(cells(bn, 2.0)["drift_gainfit_0.3"]["top1"] >= 0.9 for bn, _ in BOARDS)
    # the edge cell b = b_hi sits at the measured eps_loc, where top-1 fluctuates around 0.9: it only needs 0.8
    P4 = all(cells(bn, f)["bits_%d" % b]["top1"] >= (0.8 if b == PREREG_BHI["%s|%g" % (bn, f)] else 0.9)
             for bn, f in keys for b in BITS if b >= PREREG_BHI["%s|%g" % (bn, f)])
    S = "square R=6"
    P5 = any(cells(S, 2.0)["bits_%d" % b]["top1"] < 0.9 for b in (1, 2, 3)) and any(cells(S, 1.25)["bits_%d" % b]["top1"] < 0.9 for b in (1, 2, 3, 4))

    def first_fail(bn, f, prefix, grid, ascending):
        seq = grid if ascending else sorted(grid, reverse=True)
        for x in seq:
            if cells(bn, f)["%s%g" % (prefix, x)]["top1"] < 0.9:
                return x
        return None
    return {"G1": bool(G1), "G2": bool(G2), "G3": bool(G3), "G4": bool(G4), "P1": bool(P1), "P2": bool(P2), "P3": bool(P3),
            "P4": bool(P4), "P5": bool(P5), "max_abs_drift_deviation": round(worst_drift, 4),
            "drift_first_fail": {"%s|%g" % (bn, f): first_fail(bn, f, "drift_", DRIFTS, True) for bn, f in keys},
            "bits_first_fail_descending": {"%s|%g" % (bn, f): first_fail(bn, f, "bits_", BITS, False) for bn, f in keys},
            "channel_gain_first_fail": {"%s|%g" % (bn, f): first_fail(bn, f, "channel_gain_", CHANNEL_GAINS, True) for bn, f in keys}}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
