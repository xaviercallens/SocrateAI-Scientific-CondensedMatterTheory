# Bulk defect vs boundary persistent homology: results (2026-09-28)

Preregistration: `PREREGISTRATION_5.md` (committed 379b49f before the run). Script: `tda_defect.py`. Data:
`data/tda_defect.json`. Ledger: H3-X-0001. Inputs: the published v1.1 DtN matrices (bit-identical to the local
build), Gudhi 3.13, null = U[0.5,1.5] disorder over all edges, 20 seeds, 95th percentile.

Statistic vs the unit configuration; **DET** = above the null's 95th percentile.

| Lattice | Config (node depth) | H₀ bottleneck | H₁ bottleneck | ‖ΔR‖/‖R‖ |
|---|---|---|---|---|
| {7,3} L=3 (null p95) | | 0.684 | 0.707 | 0.109 |
| | deep ×100 (5) | 0.0005 | 0.314 | 0.038 |
| | deep ×0.01 (5) | 0.0006 | 0.216 | 0.052 |
| | shallow ×100 (1) | 0.130 | **0.786 DET** | 0.028 |
| | shallow ×0.01 (1) | 0.074 | 0.074 | 0.043 |
| square R=10 (null p95) | | 0.983 | 0.398 | 0.113 |
| | deep ×100 (9) | 0.0001 | 0.017 | 0.006 |
| | deep ×0.01 (9) | 0.0001 | 0.010 | 0.004 |
| | shallow ×100 (1) | 0.320 | 0.289 | 0.049 |
| | shallow ×0.01 (1) | 0.123 | 0.123 | 0.035 |
| {7,3} L=2 (null p95) | | 0.658 | 0.682 | 0.135 |
| | deep ×100 (3) | 0.002 | 0.335 | 0.059 |
| | deep ×0.01 (3) | 0.003 | 0.297 | 0.081 |
| | shallow ×100 (1) | 0.125 | **0.752 DET** | 0.061 |
| | shallow ×0.01 (1) | 0.075 | 0.118 | 0.092 |
| square R=6 (null p95) | | 0.791 | 0.359 | 0.131 |
| | deep ×100 (5) | 0.0008 | 0.054 | 0.020 |
| | deep ×0.01 (5) | 0.0005 | 0.032 | 0.012 |
| | shallow ×100 (1) | 0.322 | 0.323 | 0.077 |
| | shallow ×0.01 (1) | 0.125 | 0.125 | 0.056 |

Every unit configuration has exactly one H₁ class (the boundary loop).

## Verdicts

- **P1 held.** A deep defect leaves no H₀/H₁ signature above the null on any lattice, for either contrast. The
  hypothesis "a bulk defect is a topological invariant readable on the boundary" fails for deep defects at these
  sizes.
- **P2 refuted.** The direct metric detector does not pick up the deep defect on the hyperbolic lattices either.
  The hyperbolic signal is 6–9× the square's at matched N (0.038 vs 0.006; 0.059 vs 0.020), as the depth mechanism
  predicts, but the null, a 50 % disorder on *every* edge, is a far larger perturbation than one node's edges.
  The threshold was not matched to the effect size; that is a design flaw of this preregistration, not a property of
  the lattices.
- **P3 partial.** The shallow ×100 defect is detected by H₁ on both hyperbolic lattices and on neither square
  lattice; the direct metric detects it nowhere; ×0.01 is detected nowhere. The pipeline is sensitive to a
  near-boundary short circuit, and only on the hyperbolic geometry, which is an exploratory observation.

## What follows (to be preregistered, not done)

A null with matched perturbation energy (e.g. the same total Σ|Δln g| spread over random edges, or a single random
node with the same contrast), more seeds, and the L=4 / R=16 pair. Until then the honest summary is: topological
detection of a deep defect from boundary resistance data is not supported; metric detection is geometry-dependent
in signal size but was not established against this null.
