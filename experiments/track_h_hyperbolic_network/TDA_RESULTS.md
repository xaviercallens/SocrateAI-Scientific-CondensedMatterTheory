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

## Follow-up run 2026-09-28: detection against measurement noise (`PREREGISTRATION_6.md`, ledger H3-X-0002)

The corrected question: up to what measurement noise ε (relative, i.i.d. Gaussian on the Neumann-to-Dirichlet map)
does a defect stay detectable? Detection = every one of 10 noisy defect realisations exceeds the maximum of a
10-realisation noise null. Detection was monotone in ε in every cell.

| Lattice | deep ×100: ε_max, metric | ε_max, H₁ | deep ×0.01 metric / H₁ | shallow ×100 metric / H₁ |
|---|---|---|---|---|
| {7,3} L=2 (N=112) | ≥ 10⁻¹ (grid top) | 3×10⁻² | ≥ 10⁻¹ / 3×10⁻² | ≥ 10⁻¹ / ≥ 10⁻¹ |
| square R=6 (N=113) | 3×10⁻² | 3×10⁻² | 3×10⁻² / 10⁻² | ≥ 10⁻¹ / ≥ 10⁻¹ |
| {7,3} L=3 (N=315) | ≥ 10⁻¹ (grid top) | 3×10⁻² | ≥ 10⁻¹ / 10⁻² | ≥ 10⁻¹ / ≥ 10⁻¹ |
| square R=10 (N=317) | 10⁻² | 3×10⁻³ | 10⁻² / 3×10⁻³ | ≥ 10⁻¹ / ≥ 10⁻¹ |

- **Q1 held:** at N≈316 a deep defect stays detectable up to at least 10× more noise on the hyperbolic lattice than on
  the square (the hyperbolic value is censored at the grid ceiling, so this is a lower bound). At N≈112 the ratio
  is ≥ 3.3. This is the depth mechanism of the paper seen from the detection side.
- **Q2 held:** the H₁ (topological) detector tolerates at least 3.3× less noise than the plain metric on both
  hyperbolic lattices. Topology adds sensitivity nowhere here; it is a coarser readout of the same information.
  (Not preregistered, observed: on square R=6, H₁ matches the metric.)
- **Q3 held:** all four lattices detect the deep ×100 defect at ε = 3×10⁻⁴, the paper's precision budget.

**Limits, all of which matter for the physical build (roadmap H-4):**
1. *Known baseline.* Detection is against the exact noiseless unit-conductance map. A real build has to measure its
   own baseline, and component tolerance (0.1 %–5 % per resistor) is a **fixed** perturbation of it, a small-amplitude
   version of the disorder null of the first run, not the white noise used here. This is the decisive next test.
2. *Detection, not localisation.* The tests say a change happened, not where, nor that two different defects
   differ. Localisation is roadmap H-3 and is untested.
3. Ten realisations, a half-decade grid, and a censored hyperbolic ε_max make the ratios coarse.
4. i.i.d. Gaussian noise is not hardware noise (correlated, drifting, quantised).

## What follows (to be preregistered, not done)

**Tolerance-matched null (next):** baseline perturbed by component tolerance at 0.1 %, 1 % and 5 % (uniform, random
per edge), detection of the deep ×100 defect against that null on all four lattices.

Earlier plan, from the first run:

A null with matched perturbation energy (e.g. the same total Σ|Δln g| spread over random edges, or a single random
node with the same contrast), more seeds, and the L=4 / R=16 pair. Until then the honest summary is: topological
detection of a deep defect from boundary resistance data is not supported; metric detection is geometry-dependent
in signal size but was not established against this null.
