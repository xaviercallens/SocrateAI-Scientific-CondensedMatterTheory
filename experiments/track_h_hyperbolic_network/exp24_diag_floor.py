#!/usr/bin/env python3
"""POST-HOC diagnostic for PREREGISTRATION_24 (written after its data existed; not part of the preregistered tests).
Reads data/momentum_resolved_rates_on_the_cylinder.json only. Questions: (1) why did gate G2 fail (global rate from the
block machinery 1.65-1.67 against the explicit 1.78-1.79)? (2) what is the sigma_min rate of the q = pi block and of the
global minimum when the window is restricted to the depths at which the q = pi block is itself resolved? (3) how fast does
the global sigma_max grow, since kappa = sigma_max / sigma_min? Writes data/momentum_diagnostic.json."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / "data" / "momentum_resolved_rates_on_the_cylinder.json").read_text())
out = {"post_hoc": True, "runs": {}}
for key in ("v W=64", "v W=96", "h W=96"):
    run = d["runs"][key]; W = run["W"]; pi = str(W // 2) if key.startswith("v") else None
    blocks = run["blocks"]
    # the block carrying the global minimum over the depths 4..7 (preregistered P1 for vertical edges)
    ref = pi if pi is not None else str(max(blocks, key=lambda i: blocks[i]["rate"] if blocks[i]["rate"] is not None else -1))
    ds = [x for x in blocks[ref]["d"] if 3 <= x]
    smin = [blocks[ref]["log10_sigma_min"][blocks[ref]["d"].index(x)] for x in ds]
    rate_ref = float(np.polyfit(ds, [-v for v in smin], 1)[0])
    # global sigma_max (max over blocks that are resolved at that depth) and its slope over the same window
    smax = []
    for x in ds:
        smax.append(max(b["log10_sigma_max"][b["d"].index(x)] for b in blocks.values() if x in b["d"]))
    slope_smax = float(np.polyfit(ds, smax, 1)[0])
    out["runs"][key] = {"reference_block": ref, "window": ds, "sigma_min_rate_reference_block": rate_ref,
                        "global_sigma_max_slope_over_window": slope_smax, "kappa_rate_implied": rate_ref + slope_smax,
                        "last_resolved_depth_reference_block": blocks[ref]["d"][-1],
                        "last_resolved_depth_per_block": {i: blocks[i]["d"][-1] for i in ("8", "16", "24", "32", "40", "48") if i in blocks}}
    print("%s: reference block %s resolved to d=%d; sigma_min rate over d=%s: %.3f; global sigma_max slope %.3f; implied kappa rate %.3f" % (
        key, ref, blocks[ref]["d"][-1], ds, rate_ref, slope_smax, rate_ref + slope_smax))
(HERE / "data" / "momentum_diagnostic.json").write_text(json.dumps(out, indent=1))
print("wrote data/momentum_diagnostic.json")
