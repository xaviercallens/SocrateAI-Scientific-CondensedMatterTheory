#!/usr/bin/env python3
"""PREREGISTRATION_33.md, post hoc diagnostic of the failed gate G1 (leak check), from the stored data only.
Why can a model trained on permuted targets predict the held-out disk? Checks: (i) correlation of layer size and depth with the target across the
training set; (ii) the permuted-target model's predictions against layer size; (iii) the leak check repeated with depth-stratified permutation (permute targets
within groups of equal depth), which is the correct null when depth is a nuisance shared by features and target. Writes data/learned_persistence_features_leak_diag.json."""
import json
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent / "data"
r = json.loads((D / "learned_persistence_features_of_jacobian_columns.json").read_text())
tr = r["sets"]["train"]
te = r["sets"]["test_flat"]
k_tr = np.array([x["k"] for x in tr], float)
n_tr = np.array([x["n"] for x in tr], float)
y_tr = np.array([np.log10(x["sigma_min"]) for x in tr])
out = {"corr_depth_target_train": float(np.corrcoef(k_tr, y_tr)[0, 1]), "corr_size_target_train": float(np.corrcoef(n_tr, y_tr)[0, 1]),
       "corr_logsize_target_train": float(np.corrcoef(np.log(n_tr), y_tr)[0, 1]),
       "n_train": len(tr), "n_test_flat": len(te), "note": "features were not stored; the permutation test is rerun by exp33 only; this file records the nuisance correlations"}
# within-depth variance of the target: how much of y is explained by depth alone (train)
ks = sorted(set(k_tr))
resid = y_tr - np.array([y_tr[k_tr == k].mean() for k in k_tr])
out["target_var_explained_by_depth_train"] = float(1 - resid.var() / y_tr.var())
# the depth-only ridge on the flat test (from the table)
out["depth_only_flat_rmse"] = r["table"]["depth|y1|ridge"]["test_flat"]["rmse"]
out["size_only_flat_rmse"] = r["table"]["size|y1|ridge"]["test_flat"]["rmse"]
out["median_only_flat_rmse"] = r["table"]["median|y1|ridge"]["test_flat"]["rmse"]
(D / "learned_persistence_features_leak_diag.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
