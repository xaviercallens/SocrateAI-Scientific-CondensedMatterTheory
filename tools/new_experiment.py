#!/usr/bin/env python3
"""Scaffold a new preregistered experiment in experiments/track_h_hyperbolic_network/:
PREREGISTRATION_<n>.md (template with mandatory sections), exp<n>_<slug>.py (script stub that writes
data/<slug>.json), and a line in experiments.json (prereg -> data file), which experiment_gate.py uses to check
that the preregistration was COMMITTED BEFORE the data file. Nothing here decides predictions: the template
leaves fields the gate refuses while they still say TODO.

  python3 tools/new_experiment.py 12 "minimum detectable contrast"
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "experiments" / "track_h_hyperbolic_network"
MANIFEST = TRACK / "experiments.json"

PREREG = """# Preregistration {n}: {title}

**Date:** TODO (YYYY-MM-DD), committed before the run. **Roadmap item:** TODO (H-x).
**Why:** TODO one paragraph: which open question, and which earlier result (ledger id) it follows from.

## Design
TODO: lattices, sizes, quantities, statistic, null/control, number of trials, seed policy, tools. Every quantity
must be computable by `exp{n}_{slug}.py` with no manual step. Name the data file: `data/{slug}.json`.

## Validity gates (results are reported only if all pass)
- G1: TODO (e.g. a control reproduces a known value to a tolerance derived from the method's error model)
- G2: TODO

## Predictions (fixed now; each with a numeric threshold)
- **P1:** TODO. **Refuted if:** TODO.
- **P2:** TODO. **Refuted if:** TODO.

## Not claimed
TODO: what this experiment cannot show (model assumptions, sizes, noise model). Nothing about holography.
"""

SCRIPT = '''#!/usr/bin/env python3
"""PREREGISTRATION_{n}.md: {title}. Writes data/{slug}.json.
Every printed number comes from the data written; predictions are scored by score() from the file alone."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, dtn  # noqa: E402,F401

OUT = Path(__file__).resolve().parent / "data" / "{slug}.json"


def run() -> dict:
    # TODO: compute; return a JSON-serialisable dict; cast numpy types with float()/int()/bool()
    return {{"todo": True}}


def score(d: dict) -> dict:
    """Return {{"P1": True/False, ...}} from the data alone, using the thresholds of PREREGISTRATION_{n}.md."""
    return {{"P1": None}}


def main() -> int:
    d = run()
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", score(d))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def main():
    n = int(sys.argv[1]); title = sys.argv[2]
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:40]
    prereg = TRACK / ("PREREGISTRATION_%d.md" % n)
    script = TRACK / ("exp%d_%s.py" % (n, slug))
    if prereg.exists() or script.exists():
        raise SystemExit("exists: " + str(prereg if prereg.exists() else script))
    prereg.write_text(PREREG.format(n=n, title=title, slug=slug))
    script.write_text(SCRIPT.format(n=n, title=title, slug=slug))
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    man["PREREGISTRATION_%d.md" % n] = {"title": title, "script": script.name, "data": ["data/%s.json" % slug]}
    MANIFEST.write_text(json.dumps(man, indent=1) + "\n")
    print("created", prereg.name, script.name, "and a manifest entry")
    print("next: fill every TODO, then `git add` + commit BOTH files (message: 'prereg %d: ...; script unrun'), then run the script." % n)


if __name__ == "__main__":
    main()
