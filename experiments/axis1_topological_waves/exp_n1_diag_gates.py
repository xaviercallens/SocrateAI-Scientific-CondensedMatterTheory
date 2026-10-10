#!/usr/bin/env python3
"""PREREGISTRATION_N1_LIMIT.md, post hoc diagnostic of the two failed gates. (i) G1: where is the zero mode of the unperturbed TRIVIAL odd chain (right end, by the
same theorem with v and w exchanged)? (ii) G2: the asymmetry statistic was coded as max |sort(ev) + sort(-ev)|, which compares the k-th smallest with the k-th smallest of
the negated list, i.e. the k-th largest, so it never vanishes; the correct statistic is max |sort(ev) + sort(-ev)[::-1]|... i.e. ev_k + ev_{n-1-k}. Recomputes both. Writes evidence/n1_limit_gate_diag.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp_n1_limit import SITES, chain  # noqa: E402

out = {}
for ph, (v, w) in (("topological", (0.5, 1.0)), ("trivial", (1.0, 0.5))):
    H = chain(v, w, 0.0, "none", np.random.default_rng(0))
    ev, U = np.linalg.eigh(H)
    j = int(np.argmin(np.abs(ev)))
    psi = U[:, j]
    q = SITES // 4
    out[ph] = {"E0": float(abs(ev[j])), "weight_left_quarter": float(np.sum(psi[:q] ** 2)), "weight_right_quarter": float(np.sum(psi[-q:] ** 2))}
# correct chiral asymmetry at eps = 0.5
rng = np.random.default_rng(1000 + 500 + 7)
asym_ok, asym_bad = [], []
for _ in range(20):
    ev = np.linalg.eigvalsh(chain(0.5, 1.0, 0.5, "chiral", rng))
    s = np.sort(ev)
    asym_ok.append(float(np.max(np.abs(s + s[::-1]))))
    asym_bad.append(float(np.max(np.abs(np.sort(ev) + np.sort(-ev)))))
rng = np.random.default_rng(1000 + 500 + 14)
asym_on = []
for _ in range(20):
    s = np.sort(np.linalg.eigvalsh(chain(0.5, 1.0, 0.5, "onsite", rng)))
    asym_on.append(float(np.max(np.abs(s + s[::-1]))))
out["asym_chiral_correct_max"] = max(asym_ok)
out["asym_chiral_as_coded_max"] = max(asym_bad)
out["asym_onsite_correct_max"] = max(asym_on)
Path(__file__).resolve().parent.joinpath("evidence", "n1_limit_gate_diag.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
