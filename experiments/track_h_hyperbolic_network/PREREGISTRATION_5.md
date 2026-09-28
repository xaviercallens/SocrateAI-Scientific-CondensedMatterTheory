# Preregistration 5: is a bulk defect a topological signature on the boundary?

**Date:** 2026-09-28, committed before the computation was run.
**Trigger:** an external suggestion (received 2026-09-28) that a conductance defect in the bulk should appear as a
change of persistent homology (Betti numbers) computed from the boundary Dirichlet-to-Neumann data, i.e. "a
topological invariant readable on the boundary". This is a hypothesis, and here it is tested against a null.

**Inputs.** The published v1.1 DtN matrices (Hugging Face dataset `dtn/*.npz`, verified bit-identical to the
local build) for unit conductances; defect and disorder configurations recomputed with the same code.

## Design

**Boundary metric.** Effective resistance between boundary nodes, R_ij = Λ⁺_ii + Λ⁺_jj − 2Λ⁺_ij, where Λ⁺ is the
pseudo-inverse of the DtN map (Kron reduction preserves effective resistances among retained nodes, so this is the
network's own resistance metric restricted to the boundary). R is a metric.

**Topology.** Vietoris–Rips persistence on the boundary points with metric R (Gudhi 3.13, complete filtration,
simplices up to dimension 2), giving H₀ and H₁ persistence diagrams. Comparison of a configuration with the unit
configuration by the bottleneck distance of H₀ and of H₁ diagrams.

**Direct (non-topological) detector, for contrast.** Relative change of the metric itself, ‖R − R₀‖_F / ‖R₀‖_F.

**Configurations** (each lattice: {7,3} L=3, N=315, 203 boundary nodes; square R=10, N=317, 76 boundary nodes;
replicated on {7,3} L=2 / square R=6):
- *deep defect*: every edge of the first interior node at maximal depth multiplied by 100, and separately by 0.01
  (the defect of v1.1 Table 4);
- *shallow defect (positive control)*: same, on the first interior node at depth 1;
- *null*: g_e ~ U[0.5, 1.5], 20 seeds; the 95th percentile of each statistic over seeds is the detection threshold.

A statistic "detects" a defect if it exceeds the null's 95th percentile.

## Predictions (fixed now)

- **P1 (the tested hypothesis fails).** The deep defect is **not** detected by H₁ bottleneck distance on either
  lattice: a localised change of conductances deforms the resistance metric smoothly and creates or destroys no
  cycle; the diagram shift stays inside the disorder null. Same for H₀.
- **P2 (metric detection, geometry-dependent).** The direct detector ‖ΔR‖/‖R₀‖ detects the deep defect on the
  hyperbolic lattice (maximal depth 5) but not on the square lattice (maximal depth 9), because boundary
  sensitivity decays with depth and the hyperbolic defect is shallower in absolute terms.
- **P3 (positive control).** The shallow defect is detected by the direct detector on both lattices, and by at
  least one of H₀/H₁ on at least one lattice (a strongly perturbed boundary neighbourhood can change the birth of
  short-lived classes).

**Refutation.** P1 is refuted if the deep defect's H₁ (or H₀) bottleneck distance exceeds the null's 95th
percentile on either lattice for either contrast; then the topological-signature hypothesis gains support and gets
a follow-up with more seeds and sizes. P2 is refuted if the square lattice detects the deep defect or the hyperbolic
does not. P3 failing means the pipeline is insensitive and P1 cannot be interpreted.

## What this is not

A test of holography. Effective resistance on a resistor network is classical; nothing here concerns entanglement,
quantum states or gravity.
