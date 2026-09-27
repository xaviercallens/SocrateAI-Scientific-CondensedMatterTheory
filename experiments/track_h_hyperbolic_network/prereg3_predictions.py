#!/usr/bin/env python3
"""Numbers for PREREGISTRATION_3.md part A, derived from the already-published
unsaturated flat-lattice data (data/h0.json), BEFORE any high-precision run.

Two rival forms for the flat-lattice condition number, fitted on the
unsaturated points only:
  (exp)  log10 kappa = a + c*sqrt(N)      (the paper's depth mechanism: depth ~ sqrt N)
  (pow)  log10 kappa = a + p*log10(N)     (steep power law)
Each is extrapolated to the float64-singular sizes. Written to
data/prereg3_predictions.json and quoted in the preregistration.
"""
import json
import math
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent / "data"
h0 = json.loads((D / "h0.json").read_text())
out = {}
for fam in ("square", "triangular"):
    rows = [r for r in h0 if r["name"].startswith(fam)]
    fin = [(r["N"], r["log10_kappa"]) for r in rows if r["log10_kappa"] is not None]
    sing = [r["N"] for r in rows if r["log10_kappa"] is None]
    N = np.array([n for n, _ in fin], float); y = np.array([k for _, k in fin])
    ce = np.polyfit(np.sqrt(N), y, 1)          # exp(c sqrt N)
    cp = np.polyfit(np.log10(N), y, 1)         # power law (global fit)
    # local power-law exponent from the last two unsaturated points
    p_last = (y[-1] - y[-2]) / (math.log10(N[-1]) - math.log10(N[-2]))
    pred = {}
    for n in sing:
        pred[str(n)] = {
            "exp_sqrtN": round(float(np.polyval(ce, math.sqrt(n))), 2),
            "power_global": round(float(np.polyval(cp, math.log10(n))), 2),
            "power_last_exponent": round(float(y[-1] + p_last * (math.log10(n) - math.log10(N[-1]))), 2),
        }
    out[fam] = {"unsaturated": fin, "fit_exp": {"a": round(float(ce[1]), 3), "c": round(float(ce[0]), 4)},
                "fit_power": {"a": round(float(cp[1]), 3), "p": round(float(cp[0]), 3)},
                "local_exponent_last": round(p_last, 2), "predictions": pred}
    print(fam, json.dumps(out[fam], indent=1))
(D / "prereg3_predictions.json").write_text(json.dumps(out, indent=1))
