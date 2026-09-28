#!/usr/bin/env python3
"""PREREGISTRATION_17.md: single-node localisation (f=2, deepest class) under offset, gain drift and quantisation,
with and without the matching decoder corrections. Writes data/localisation_under_correlated_hardware_n.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, depths, dtn  # noqa: E402
from localize_defect import DICT_F  # noqa: E402
from tda_noise import noisy  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "localisation_under_correlated_hardware_n.json"
EPS0, F, TRIALS = 3e-4, 2.0, 20
OFFSETS = [1e-4, 1e-3, 1e-2, 1e-1]
DRIFTS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
BITS = [10, 12, 14, 16]


class Board:
    def __init__(self, g):
        n, E = len(g["nodes"]), len(g["edges"])
        self.bnd = boundary_nodes(g); dep = depths(g, self.bnd)
        self.interior = np.setdiff1d(np.arange(n), self.bnd)
        self.P0 = np.linalg.pinv(dtn(n, g["edges"], np.ones(E), self.bnd), rcond=1e-12)
        self.s = float(np.sqrt(np.mean(self.P0 ** 2)))
        masks = {int(v): np.array([v in e for e in g["edges"]]) for v in self.interior}
        self.flat = np.empty((len(self.interior) * len(DICT_F), self.P0.size))
        for i, v in enumerate(self.interior):
            for j, f in enumerate(DICT_F):
                self.flat[i * len(DICT_F) + j] = (np.linalg.pinv(dtn(n, g["edges"], np.where(masks[int(v)], f, 1.0), self.bnd), rcond=1e-12) - self.P0).ravel()
        self.flat_c = self.flat - self.flat.mean(axis=1, keepdims=True)
        self.nodes = [int(v) for v in self.interior if dep[v] == int(dep[self.interior].max())]
        self.Pd = {v: np.linalg.pinv(dtn(n, g["edges"], np.where(masks[v], F, 1.0), self.bnd), rcond=1e-12) for v in self.nodes}

    def decode(self, P1, P2, mode):
        dP = (P2 - P1).ravel()
        if mode == "plain":
            k = int(np.argmin(np.linalg.norm(self.flat - dP, axis=1)))
        elif mode == "mean_removed":
            k = int(np.argmin(np.linalg.norm(self.flat_c - (dP - dP.mean()), axis=1)))
        elif mode == "gain_fitted":
            # P2 ~ g (P1 + D_k): fit g per entry by least squares on the full map, residual on the difference
            p1 = P1.ravel(); best, k = np.inf, -1
            p2 = P2.ravel()
            for i in range(self.flat.shape[0]):
                m = p1 + self.flat[i]
                g = float(m @ p2 / (m @ m))
                r = float(np.linalg.norm(p2 - g * m))
                if r < best:
                    best, k = r, i
        return k // len(DICT_F)

    def cell(self, rng, perturb, mode):
        hit = 0
        for t in range(TRIALS):
            v = self.nodes[t % len(self.nodes)]
            i_true = int(np.where(self.interior == v)[0][0])
            P1 = noisy(self.P0, EPS0, rng); P2 = noisy(self.Pd[v], EPS0, rng)
            P1, P2 = perturb(P1, P2, rng)
            hit += int(self.decode(P1, P2, mode) == i_true)
        return hit / TRIALS


def run() -> dict:
    out = {"f": F, "eps_iid": EPS0, "trials": TRIALS, "boards": {}}
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6))):
        b = Board(g); rng = np.random.default_rng(17); res = {"cells": {}}
        ident = lambda P1, P2, r: (P1, P2)
        for mode in ("plain", "mean_removed", "gain_fitted"):
            res["cells"]["none " + mode] = b.cell(rng, ident, mode)
        for eo in OFFSETS:
            def off(P1, P2, r, eo=eo):
                return P1 + r.normal(0, eo) * b.s, P2 + r.normal(0, eo) * b.s
            for mode in ("plain", "mean_removed"):
                res["cells"]["offset%g %s" % (eo, mode)] = b.cell(rng, off, mode)
        for eg in DRIFTS:
            def drift(P1, P2, r, eg=eg):
                return P1, (1 + r.normal(0, eg)) * P2
            for mode in ("plain", "gain_fitted"):
                res["cells"]["drift%g %s" % (eg, mode)] = b.cell(rng, drift, mode)
        for bits in BITS:
            q = 2.0 ** (-bits) * b.s
            def quant(P1, P2, r, q=q):
                return np.round(P1 / q) * q, np.round(P2 / q) * q
            res["cells"]["bits%d plain" % bits] = b.cell(rng, quant, "plain")
        out["boards"][name] = res
        for k, v in res["cells"].items():
            print("  %-11s %-22s top1=%.2f" % (name, k, v), flush=True)
    return out


def score(d: dict) -> dict:
    c = lambda board, key: d["boards"][board]["cells"][key]
    H, S = "{7,3} L=2", "square R=6"
    G1 = c(H, "none plain") >= 0.9 and c(S, "none plain") >= 0.9
    G2 = all(c(b, "none " + m) >= 0.9 for b in (H, S) for m in ("mean_removed", "gain_fitted"))
    P1 = (c(H, "bits12 plain") >= 0.9 and c(S, "bits12 plain") >= 0.9 and c(S, "bits10 plain") < 0.9 and c(H, "bits10 plain") >= 0.9)
    P2 = (c(S, "offset0.001 plain") < 0.9 and c(H, "offset0.001 plain") >= 0.9 and c(H, "offset0.01 plain") < 0.9
          and all(c(b, "offset%g mean_removed" % eo) >= 0.9 for b in (H, S) for eo in OFFSETS))
    P3 = (c(S, "drift0.001 plain") < 0.9 and c(H, "drift0.001 plain") >= 0.9 and c(S, "drift0.01 plain") < 0.9 and c(H, "drift0.01 plain") < 0.9
          and all(c(b, "drift%g gain_fitted" % eg) >= 0.9 for b in (H, S) for eg in DRIFTS))
    return {"G1": G1, "G2": G2, "P1": P1, "P2": P2, "P3": P3}


def main() -> int:
    d = run(); d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
