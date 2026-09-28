# Preregistration 11: conditioning across hyperbolic tilings (roadmap H-2): is depth the whole mechanism?

**Date:** 2026-09-28, committed before any new tiling was computed. Only the {7,3} and flat values already in
`data/h0.json` were known when the predictions were written.

## Question
The paper says "the mechanism is the scaling of depth with size" (§3.1). Two readings: (i) κ is set by the maximal
boundary depth d_max alone, and hyperbolic lattices win because d_max grows only as log N; (ii) κ depends on d_max
*and* on the branching structure, so at equal d_max different tilings differ. The existing data already hint at (ii):
at d_max = 5, square R=6 has log₁₀κ = 5.07 and triangular 8.67, {7,3} L=3 has 3.27.

## Design
Tilings {7,3} (L=1..4), {8,3} (L=1..4), {5,4} (L=1..5), {6,4} (L=1..4), {4,5} (L=1..6); unit conductances, full boundary,
the DtN sensitivity Jacobian J as in the paper. κ = σ_max/σ_min from the Gram matrix G = JᵀJ formed in closed form,
G_ef = ½[(d_e·d_f)² − (d_e²·d_f²)] (d_e = h_a − h_b on the boundary), κ = √(λ_max(G)/λ_min(G)), in float64. A value is
reported only if λ_min(G) > 1e-13·λ_max(G); otherwise it is marked unresolved. d_max = maximal graph distance to the
boundary (same function as in v1.0).
**Validity gates (a tiling's results are reported only if both pass):** (a) every interior node has degree q;
(b) control: this method reproduces the v1.0 direct-SVD log₁₀κ of {7,3} L=3 (3.2722) and square R=6 (5.0724) to 1e-6.

## Predictions (fixed now)
- **P1 (concavity in depth).** For {7,3} and {8,3}, the increments of log₁₀κ between consecutive layers L=1..4 are
  strictly decreasing (log κ is concave in L; v1.0's {7,3} increments are 1.08, 0.81, 0.62).
- **P2 (faster branching is better conditioned).** log₁₀κ({8,3}, L) < log₁₀κ({7,3}, L) at each of L = 2, 3, 4.
- **P3a (depth is *nearly* universal among hyperbolic tilings).** At each d_max ∈ {1, 2, 3, 5} that at least two
  hyperbolic tilings reach, the spread (max − min) of log₁₀κ across hyperbolic tilings is ≤ 1.0 decade.
- **P3b (but not across geometries).** At d_max = 5, both flat lattices (square R=6: 5.07, triangular R=6.45: 8.67)
  exceed every hyperbolic tiling's log₁₀κ at d_max = 5 by ≥ 1.0 decade.
- **P4 (polynomial growth in N for every tiling).** The local exponent d log κ / d log N between the two largest
  sizes is ≤ 1.5 for {8,3} and ≤ 1.0 for {5,4}, {6,4}, {4,5}.

**Refutation:** any of P1–P4 failing as stated. If P3a fails while P3b holds, "depth alone" is refuted *within* the
hyperbolic family too, and the paper's mechanism sentence must be rewritten. If P3b fails, the flat/hyperbolic
difference at equal depth in v1.0 is not robust.

## Not claimed
An exact scaling law, or anything about tilings with q ≥ 6 or p > 8; nothing about holography.
