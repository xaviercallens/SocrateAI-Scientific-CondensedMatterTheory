# Preregistration 14: exact rank certificates for the other tilings (task Q6)

**Date:** 2026-09-28, committed before the run. **Roadmap item:** H-2 (limit "no exact rank certificates for these
tilings" in `TILINGS_RESULTS.md`, ledger H0-X-0008).
**Why:** full column rank of the DtN sensitivity Jacobian was certified over two finite fields for {7,3} and flat
lattices (H0-B-0001). The conditioning results for {8,3}, {5,4}, {6,4}, {4,5} (H0-X-0008) are only meaningful if
those Jacobians are also full rank, i.e. the problem is identifiable and κ measures conditioning, not a rank defect.

## Design
Instances (E ≤ 1700): {7,3} L=3 (E=399; new, not certified before), {8,3} L=2, L=3 (E=240, 928), {5,4} L=3, L=4, L=5
(E=225, 605, 1600), {6,4} L=2, L=3 (E=150, 576), {4,5} L=4, L=5, L=6 (E=296, 692, 1604). Unit conductances, full boundary.
**Method (random-combination certificate).** For each prime p ∈ {2³¹−1, 998244353}: compute the harmonic extension
H mod p (`hyperbolic_exact.mat_inv_mod` on L_ii; product with the *signed* L_ib, entries in {−1, 0}, so no int64
overflow); with d_e = H[a] − H[b] on the boundary, form k random combinations of the rows of the Jacobian,
row s having coefficient c_ij = u_si v_sj + u_sj v_si on pair (i < j), u, v uniform in GF(p) from
`numpy.random.default_rng(14)`; entry (s, e) is (u_s·d_e)(v_s·d_e) − Σ_i u_si v_si d_e,i², so the Jacobian is never
formed. Since this matrix is a row combination of J, its rank over GF(p) is ≤ rank_p(J) ≤ rank_ℚ(J) (L_ii invertible
mod p); rank E therefore certifies full column rank. k = E + 20; if the rank is < E, redraw once with k = 2E (seed 15);
if still < E, the instance is reported **not certified** (not evidence of a rank defect). Both primes must certify for
a Tier-B claim. (A plain random *subset* of rows was tried first in a unit check outside this list and rejected before
this preregistration was committed: a resistor between two boundary nodes affects exactly one row, so a subset misses
it; {7,3} L=1 gave rank 17 of 42.)
Data file: `data/exact_rank_certificates_for_other_tiling.json`.

## Validity gates (results are reported only if all pass)
- G1 (method control): on {7,3} L=2 the subset method certifies rank 140 = E for both primes, matching the full-matrix
  result of H0-B-0001.
- G2: L_ii is invertible mod both primes for every instance (otherwise that instance is skipped and reported).

## Predictions (fixed now)
- **P1:** every listed instance is certified full rank for both primes. **Refuted if** any instance is not certified
  (reported as "not certified", with its subset rank; not as a proven deficiency).
- **P2:** no instance needs the 2E redraw. **Refuted if** any does (would mean E + 20 combinations are not generic enough).

## Not claimed
Anything about probe-subsampled Jacobians of these tilings, about conditioning, or about instances with E > 1700.
Nothing about holography.
