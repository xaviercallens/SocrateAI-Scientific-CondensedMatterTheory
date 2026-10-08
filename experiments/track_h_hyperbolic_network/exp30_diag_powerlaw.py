#!/usr/bin/env python3
"""PREREGISTRATION_30.md, post hoc (not preregistered): power-law versus exponential form of the square-disk median death time, from the stored data.
Writes data/jacobian_column_cloud_homology_posthoc.json."""
import json
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent / "data"
r = json.loads((D / "jacobian_column_cloud_homology.json").read_text())
layers = r["square"]["layers"]
ks = np.array([int(k) for k in layers if layers[k]["median_death"] is not None])
m = np.array([layers[str(k)]["median_death"] for k in ks])
out = {"layers": [int(k) for k in ks], "median_death": [float(x) for x in m], "k_times_m": [float(k * x) for k, x in zip(ks, m)]}
sel = ks >= 3
out["loglog_slope_k3_to_9"] = float(np.polyfit(np.log(ks[sel]), np.log(m[sel]), 1)[0])
out["semilog_slope_k3_to_9"] = float(np.polyfit(ks[sel], np.log10(m[sel]), 1)[0])
res_pl = np.log(m[sel]) - np.polyval(np.polyfit(np.log(ks[sel]), np.log(m[sel]), 1), np.log(ks[sel]))
res_ex = np.log(m[sel]) - np.polyval(np.polyfit(ks[sel], np.log(m[sel]), 1), ks[sel])
out["rms_residual_powerlaw"] = float(np.sqrt(np.mean(res_pl ** 2)))
out["rms_residual_exponential"] = float(np.sqrt(np.mean(res_ex ** 2)))
out["g2_floor_note"] = "identical columns give a sine distance of about 1.5e-8 (sqrt of double rounding of 1 - c^2); G2 limit 1e-12 was unattainable"
out["g2_max_median_death_rerun"] = r["G2"]["max_median_death"]
(D / "jacobian_column_cloud_homology_posthoc.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
