# Preregistration N1-L2: repeat of N1-L with corrected gates (node N1 of docs/TOPOLOGY_PROGRAMME.md)

**Date:** 2026-10-10, committed before the run. **Why:** the first run (PREREGISTRATION_N1_LIMIT.md) had both validity gates fail as written through errors of mine, so by the programme's rule its predictions P1 to P5 are unread. This card repeats the run with gates derived from the theorem and statistics tested on known cases; the objects, design, strength grid, draws and predictions P1 to P5 are **unchanged** from N1-L, copied here so that the card stands alone. Seeds are new (so that this is a fresh draw, not a re-read of the old one).

## Objects, design (unchanged)
Open SSH chain, 2N+1 = 41 sites, intra-cell coupling v, inter-cell w; topological phase v = 1/2, w = 1 (gap 1); trivial phase v = 1, w = 1/2 as control. Perturbations with strength ε and 50 draws (seed base 2000): P_chiral (every hopping times (1 + ε u), u ~ U[−1,1]); P_onsite (on-site energies ε u); P_nnn (next-nearest-neighbour hopping ε, uniform).
Observables per draw: |E₀| the smallest |eigenvalue|; W_L the weight of the corresponding eigenvector on the left quarter; W_R on the right quarter; Π the sublattice polarisation; A = max_k |ev_k + ev_{n−1−k}| the spectral asymmetry (eigenvalues sorted; this is the corrected statistic). Grid ε ∈ {0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0}.

## Gates (corrected; each derived from the theorem or tested on a known case before this commit)
- **G0 (statistic self-test, run first):** on the unperturbed topological chain A ≤ 1e-12 (chiral symmetry holds exactly, so the spectrum is symmetric); on a diagonal matrix diag(0.3, 0.1, −0.2) A = 0.1 (hand value: sorted −0.2, 0.1, 0.3; the pairs (−0.2, 0.3), (0.1, 0.1), (0.3, −0.2) give sums 0.1, 0.2, 0.1, so the max is 0.2). If G0 fails the statistic is wrong and nothing is run.
- **G1 (unperturbed chains, from the theorem):** `ssh_exact.py` exits 0; topological chain |E₀| ≤ 1e-12, W_L ≥ 0.99, Π = 1 to 1e-12; trivial chain |E₀| ≤ 1e-12 (the odd chain has an exact zero mode in both phases), **W_R ≥ 0.99 and W_L ≤ 0.01** (the mode is at the right end iff |v| > |w|, statement 3 of T2 with v and w exchanged).
- **G2 (the perturbations do what they are meant to):** under P_chiral at every ε < 1, A ≤ 1e-12 on every draw; under P_onsite at ε = 0.5, A > 1e-3 on every draw.

## Predictions (unchanged from N1-L, fixed again now)
- **P1:** under P_chiral, median |E₀| ≤ 1e-6 for all ε ≤ 0.5, and the fraction of draws with W_L ≥ 0.9 is ≥ 0.9 for all ε ≤ 0.3.
- **P2:** under P_chiral, the first ε with that fraction < 0.5 is ≥ 0.5 (or none on the grid).
- **P3:** under P_onsite, the median |E₀| over ε ≤ 0.5 has least-squares slope in [0.2, 0.8], and the fraction with W_L ≥ 0.9 is ≥ 0.9 for all ε ≤ 0.3.
- **P4:** under P_nnn, median |E₀| at ε = 0.1 exceeds P_onsite's at 0.1, and the fraction with W_L ≥ 0.9 falls below 0.5 at some ε ≤ 0.5.
- **P5:** in the trivial phase, no draw at any ε ≤ 0.3 has |E₀| < 0.1 and W_L ≥ 0.9.

## Disclosure
The first run's data (`evidence/n1_limit.json`) showed all five predictions holding; I know this. The repeat is not blind to the outcome; it is a fresh draw under valid gates, and its purpose is to make the record readable under the rule, not to learn the answer. If any prediction fails on the fresh draw, it is refuted and the first run's "would have held" is noted as a draw-to-draw discrepancy.

## What a refutation would mean (unchanged)
As in N1-L. G0 or G1 failed: the gate design is still wrong and the card is withdrawn, not patched.

## Not claimed
As in N1-L: nothing about the physical channel, the infinite chain, interacting systems, or holography. A diagonalisation is not a measurement.
