#!/usr/bin/env python3
"""One-off: append the exploratory Q5 results block (prereg 16) to TILINGS_RESULTS.md from the data file.
Idempotent: does nothing if the heading is already present."""
import json
import re
from pathlib import Path

T = Path(__file__).resolve().parents[1]
res = T / "TILINGS_RESULTS.md"
head = "## Sensitivity versus depth across tilings (PREREGISTRATION_16.md, EXPLORATORY, committed before the run; ledger H0-X-0009)"
if head in res.read_text():
    print("block already present"); raise SystemExit
d = json.loads((T / "data" / "sensitivity_versus_depth_across_tilings.json").read_text())
pre = (T / "PREREGISTRATION_16.md").read_text()
design = re.search(r"## Design\n(.*?)\n\n", pre, re.S).group(1).strip()
dev = re.search(r"(\*\*Deviation 1.*?)\n\n", pre, re.S).group(1).strip()
notc = re.search(r"## Not claimed\n(.*?)\n*$", pre, re.S).group(1).strip()
maxd = max(int(k) for r in d["rows"] for k in r["by_depth"])
lines = [head, "", design, "", dev, "",
         "| Instance | N | " + " | ".join("depth %d" % k for k in range(maxd + 1)) + " | slope (all) | slope (d>=1) |",
         "|---|---|" + "---|" * (maxd + 1) + "---|---|"]
for r in d["rows"]:
    y0 = r["by_depth"]["0"]["mean_log10"]
    cells = ["%.2f" % (r["by_depth"][str(k)]["mean_log10"] - y0) if str(k) in r["by_depth"] else "" for k in range(maxd + 1)]
    sl = lambda v: "n/a" if v is None else "%.3f" % v
    lines.append("| %s %s | %d | %s | %s | %s |" % (r["family"], r["param"], r["N"], " | ".join(cells), sl(r["slope_per_depth"]), sl(r["slope_per_depth_from_1"])))
v = d["verdicts"]
lines += ["", "| Gate | Threshold | Verdict |", "|---|---|---|",
          "| G1 (amended, Deviation 1) | the script reproduces h0's median column norm per depth to 1e-6 | %s |" % ("held" if v["G1"] else "refuted"),
          "| G2 | every instance's edge count per depth sums to E | %s |" % ("held" if v["G2"] else "refuted"),
          "", "**Limits:** " + notc, "",
          "*Recorded by the orchestrator from the data file (the low-tier recorder had not reported); audited with `tools/audit_low_tier.py`.*", "",
          "**Reading (exploratory).** The per-edge sensitivity profile is nearly the same on every lattice: all curves are "
          "concave in depth, and at depth 3 the hyperbolic tilings lie at −2.0 to −2.4 decades relative to depth 0 while the flat "
          "lattices lie at −2.4; the per-depth increments (about −1.1, −0.7, −0.4, −0.3, …) are alike. The amplitude decay of a "
          "single edge's boundary signal therefore does not explain why log κ is concave in depth on hyperbolic tilings and "
          "linear on flat ones (H0-X-0008). What differs between the geometries must be how many edges share a boundary "
          "signature and how collinear those signatures are, the *coherence* that version 1.0 sampled but did not analyse; "
          "that is task Q5b. Nothing here is a prediction or a claim."]
res.write_text(res.read_text().rstrip("\n") + "\n\n" + "\n".join(lines) + "\n")
print("appended", len(d["rows"]), "rows")
