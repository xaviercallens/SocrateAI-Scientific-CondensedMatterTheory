# Preregistration 20: test of the coherence-mechanism argument on new instances (task Q5d)

**Date:** 2026-10-07, committed before the run. **Roadmap item:** H-2. **Argument under test:** `MECHANISM_NOTE.md`
(Tier C), written from H0-X-0009/0010/0011 and from the square R=10 values of H0-X-0010. **Those instances are
therefore excluded here**; every prediction below is tested on instances the argument has not seen.

## Design
Instances: hyperbolic {7,3} L=5 (N=2240, E=2856) and {4,5} L=7 (N=2320, E=3696); flat square R=16 (N=797, E=1528)
and triangular R=10.75 (N=421, E=1176), unit conductances, full boundary. Columns, edge depth and the closed-form
Gram matrix as in preregistration 18. Per instance and depth class (n_d ≥ 2): the full-class effective dimension
fraction f_d = PR_d/n_d. Per instance and d = 0 … d_max: log₁₀ κ_d of the Jacobian restricted to columns of depth ≤ d,
from the explicit Jacobian when it has ≤ 2×10⁸ entries (the two flat instances), otherwise from the Gram matrix
(κ_d = √κ(G_d); the two hyperbolic instances). On the flat instances only depths with log₁₀ κ_d ≤ 13 are usable in
double precision; d* is the largest such depth and Δ̄ = (log₁₀ κ_{d*} − log₁₀ κ_1)/(d* − 1). On the hyperbolic
instances Δ̄ uses d_max. Reference values read from `data/coherence_mechanism_at_matched_size.json` (H0-X-0011):
Δ̄(square R=10) and Δ̄({7,3} L=4). Data file: `data/coherence_mechanism_prediction_test.json`; figure
`data/fig_mechanism_test.pdf`.

## Validity gates
- G1 (closed form): on square R=6 the closed-form cosines agree with the explicit Jacobian to 1e-10 at every depth.
- G2 (flat precision): d* ≥ 4 on both flat instances (otherwise Δ̄ has fewer than three increments and P3a is void).
- G3 (Gram floor): on both hyperbolic instances 10·ε_mach·κ(G_{d_max}) ≤ 1e-5, so the Gram route resolves κ.

## Predictions (numbers fixed now; from `MECHANISM_NOTE.md`)
- **P1 (flat: d·f_d constant).** On square R=16 and on triangular R=10.75, over 2 ≤ d ≤ d_max − 2 (edge depth), the
  ratio max(d·f_d)/min(d·f_d) ≤ 1.5. **Refuted if** either ratio exceeds 1.5.
- **P2 (hyperbolic: f_d stays O(1)).** On {7,3} L=5 and {4,5} L=7, f_d ≥ 0.75 at every depth d ≥ 2.
  **Refuted if** any class is below 0.75.
- **P3a (flat growth rate, size-independent).** Δ̄ ∈ [0.7, 1.5] on both flat instances, and
  |Δ̄(square R=16) − Δ̄(square R=10)| ≤ 0.2. **Refuted if** any of the three fails.
- **P3b (hyperbolic growth rate, does not increase with L).** Δ̄ ≤ 0.5 on both hyperbolic instances, and
  Δ̄({7,3} L=5) ≤ Δ̄({7,3} L=4) + 0.05. **Refuted if** either fails.

## What each refutation means (written now)
P1 refuted: the Fourier-band argument (effective rank ≈ R/d) is wrong or too crude; P2 refuted: the overlap number on
hyperbolic disks is not O(1) at larger L; P3a refuted: the per-depth rate depends on R, so it is not set by the lattice
cutoff alone; P3b refuted: hyperbolic growth has an L-dependent part the argument misses.

## Not claimed
A proof; the value of the flat rate constant; depth 0 and 1; the degree-3 depth-1 dip; anything about holography.
