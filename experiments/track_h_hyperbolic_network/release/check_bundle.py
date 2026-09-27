#!/usr/bin/env python3
"""Sanity checks on release/build before upload. Exit 1 on any failure.

- every DtN matrix is symmetric with zero row sums (a Laplacian Schur complement)
- every graph: edge endpoints in range, boundary non-empty, N matches the index
  (Euler's relation is checked by hyperbolic_network.py --self-test, not here)
- the CSVs load and the dataset card lists every CSV config
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

B = Path(__file__).resolve().parent / "build"
DS = B / "hf_dataset"


def main():
    bad = []
    idx = list(csv.DictReader(open(DS / "graphs_index.csv")))
    for r in idx:
        g = json.loads((DS / r["graph_file"]).read_text())
        n = len(g["x"])
        if n != int(r["N"]) or not g["boundary"] or max(max(e) for e in g["edges"]) >= n:
            bad.append(f"graph {r['graph_id']}")
        if r["dtn_file"]:
            lam = np.load(DS / r["dtn_file"])["Lambda"]
            if not (np.allclose(lam, lam.T, atol=1e-10) and np.abs(lam.sum(1)).max() < 1e-9):
                bad.append(f"dtn {r['graph_id']}")
    card = (DS / "README.md").read_text()
    for f in DS.glob("*.csv"):
        rows = list(csv.DictReader(open(f)))
        if not rows or f"data_files: {f.name}" not in card:
            bad.append(f"csv {f.name}")
    sizes = {p.name: p.stat().st_size for p in (B / "zenodo").iterdir()}
    print("graphs:", len(idx), "| dtn:", sum(1 for r in idx if r["dtn_file"]), "| zenodo files (bytes):", sizes)
    print("FAIL:" if bad else "all checks pass", bad if bad else "")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
