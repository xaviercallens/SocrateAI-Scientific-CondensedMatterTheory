#!/usr/bin/env python3
"""Unit check of the row-subset certificate of exp14 on an instance OUTSIDE its preregistered list ({7,3} L=1):
subset rank must equal E = 42 for both primes, and equal the full-matrix rank of hyperbolic_exact.jacobian_mod."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp14_exact_rank_certificates_for_other_tiling import subset_rank  # noqa: E402
from hyperbolic_exact import PRIMES, jacobian_mod, rank_mod  # noqa: E402
from hyperbolic_network import boundary_nodes, build_hyperbolic  # noqa: E402

g = build_hyperbolic(7, 3, 1)
n, edges = len(g["nodes"]), g["edges"]
bnd = boundary_nodes(g)
ok = True
for p in PRIMES:
    sub = subset_rank(n, edges, bnd, p, len(edges) + 20, 14)
    full = rank_mod(jacobian_mod(n, edges, bnd, p), p)
    good = sub[0] == len(edges) == full
    ok &= good
    print("p=%d subset rank %d (rows %d of %d), full-matrix rank %d, E=%d: %s" % (p, sub[0], sub[1], sub[2], full, len(edges), "ok" if good else "FAIL"))
# negative control: probe-subsampled {7,3} L=2 (44 probes) is certified rank 117 < E=140 (H0-B-0002)
from probe_matched import subsample_by_angle  # noqa: E402
g2 = build_hyperbolic(7, 3, 2)
probes = subsample_by_angle(g2, boundary_nodes(g2), 44)
for p in PRIMES:
    r = subset_rank(len(g2["nodes"]), g2["edges"], probes, p, len(g2["edges"]) + 20, 14)[0]
    good = r == 117
    ok &= good
    print("negative control p=%d: rank %d (expected 117 of 140): %s" % (p, r, "ok" if good else "FAIL"))
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
