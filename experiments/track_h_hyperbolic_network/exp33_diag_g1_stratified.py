#!/usr/bin/env python3
"""PREREGISTRATION_33.md Deviation 2 (post hoc): gate G1 recomputed as a depth-stratified permutation test with 200 permutations.
Recomputes the clouds and features by the same code as exp33 (same seeds), fits the best persistence model (AB, ridge) on permuted targets, and reports the distribution
of the held-out R2. Writes data/learned_persistence_features_g1_stratified.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exp33_learned_persistence_features as e  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "learned_persistence_features_g1_stratified.json"
NPERM = 200


def main():
    sets = {}
    for name, lst, fn in (("train", e.TRAIN, e.layers_flat), ("test_flat", e.TEST_FLAT, e.layers_flat)):
        rows = []
        for kind, p in lst:
            rr = fn(e.build(kind, p))
            for r in rr:
                r["geom"] = f"{kind}{p}"
            rows += rr
        sets[name] = rows
    fA, fB = e.Features().fit(sets["train"], "DA"), e.Features().fit(sets["train"], "DB")
    X = {s: np.hstack([fA.transform(sets[s], "DA"), fB.transform(sets[s], "DB")]) for s in sets}
    mu, sd = X["train"].mean(0), X["train"].std(0) + 1e-12
    Xtr, Xte = (X["train"] - mu) / sd, (X["test_flat"] - mu) / sd
    ytr = np.array([np.log10(r["sigma_min"]) for r in sets["train"]])
    yte = np.array([np.log10(r["sigma_min"]) for r in sets["test_flat"]])
    ktr = np.array([r["k"] for r in sets["train"]])
    real = e.score(e.fit_models(Xtr, ytr)["ridge"], Xte, yte)
    rng = np.random.default_rng(3301)
    r2_strat, r2_plain = [], []
    for _ in range(NPERM):
        yp = ytr.copy()
        for k in np.unique(ktr):
            idx = np.where(ktr == k)[0]
            yp[idx] = rng.permutation(ytr[idx])
        r2_strat.append(e.score(e.fit_models(Xtr, yp)["ridge"], Xte, yte)["r2"])
        r2_plain.append(e.score(e.fit_models(Xtr, rng.permutation(ytr))["ridge"], Xte, yte)["r2"])
    r2_strat, r2_plain = np.array(r2_strat, float), np.array(r2_plain, float)
    out = {"n_perm": NPERM, "real_r2_flat": real["r2"], "real_rmse_flat": real["rmse"],
           "stratified": {"median_r2": float(np.median(r2_strat)), "p95_r2": float(np.percentile(r2_strat, 95)), "max_r2": float(r2_strat.max()),
                          "fraction_above_0_1": float(np.mean(r2_strat > 0.1)), "fraction_ge_real": float(np.mean(r2_strat >= real["r2"]))},
           "plain": {"median_r2": float(np.median(r2_plain)), "p95_r2": float(np.percentile(r2_plain, 95)), "max_r2": float(r2_plain.max()),
                     "fraction_above_0_1": float(np.mean(r2_plain > 0.1)), "fraction_ge_real": float(np.mean(r2_plain >= real["r2"]))}}
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
