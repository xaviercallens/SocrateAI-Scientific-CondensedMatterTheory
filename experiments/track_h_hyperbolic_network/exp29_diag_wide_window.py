#!/usr/bin/env python3
"""PREREGISTRATION_29.md, post hoc (not preregistered): slopes over d = 3..9 for S1, S2, S5 and the offset in log10 kappa, from the stored data.
Writes data/laplace_wide_window_posthoc.json."""
import json
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent / "data"
res = json.loads((D / "laplace_resolved_jacobian_conditioning.json").read_text())
tab = res["square"]["table"]
ds = list(range(3, 10))
out = {"window": ds, "slope": {}, "offset_S1_minus_S5": {}, "note": "post hoc; S1 values above 9 decades are near the double-precision floor"}
for k in ("S1", "S2", "S5"):
    y = [tab[k][str(d)]["log10_kappa"] for d in ds]
    out["slope"][k] = float(np.polyfit(ds, y, 1)[0])
    out.setdefault("sigma_min_log10", {})[k] = [float(np.log10(tab[k][str(d)]["sigma_min"])) for d in ds]
out["offset_S1_minus_S5"] = {str(d): tab["S1"][str(d)]["log10_kappa"] - tab["S5"][str(d)]["log10_kappa"] for d in ds}
out["ratio_S5_over_S1"] = out["slope"]["S5"] / out["slope"]["S1"]
out["ratio_S2_over_S1"] = out["slope"]["S2"] / out["slope"]["S1"]
(D / "laplace_wide_window_posthoc.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
