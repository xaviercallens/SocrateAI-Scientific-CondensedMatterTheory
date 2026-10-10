# Preregistration N1-L: the limit of bulk–boundary protection in the finite SSH chain (node N1 of docs/TOPOLOGY_PROGRAMME.md)

**Date:** 2026-10-10, committed before the run. **Why:** the thesis node N1 says the winding ν of the bulk symbol determines a zero mode at the left end of the odd open chain,
robust to a class P of perturbations and not outside it. The theorem (bulk half in Lean, boundary half in exact arithmetic) says nothing about P. This card measures P on the finite chain:
which perturbations leave the end mode, at which strength they remove it, and whether that strength scales with the gap, as the symmetry argument predicts.

## Objects (fixed now)
Open SSH chain with 2N+1 sites, N = 20 (41 sites), intra-cell coupling v, inter-cell coupling w; topological phase v = 1/2, w = 1 (gap 2(|w| − |v|) = 1), and trivial phase v = 1, w = 1/2 as the control.
Perturbations, each with strength ε and 50 random draws (seeds fixed in the script):
- **P_chiral**: coupling disorder, every hopping multiplied by (1 + ε u), u ~ U[−1, 1]; preserves chiral symmetry.
- **P_onsite**: on-site energies ε u on every site; breaks chiral symmetry.
- **P_nnn**: next-nearest-neighbour hopping ε (uniform); breaks chiral symmetry (same-sublattice hopping).
Observables per draw: |E₀| the smallest |eigenvalue|; the end weight W_L = Σ_{n<N/4} |ψ₀(n)|² of the corresponding eigenvector on the left quarter; the sublattice polarisation Π = Σ_A |ψ₀|² − Σ_B |ψ₀|².
Arithmetic: double precision (`numpy.linalg.eigh`); the unperturbed cases are also checked in exact rational arithmetic by the existing `ssh_exact.py` harness (gate G1).
Strength grid: ε ∈ {0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0}. Statistic per cell: median over draws, and the fraction of draws with W_L ≥ 0.9.

## Exact facts (gates, not predictions)
- G1: at ε = 0, |E₀| = 0 to 1e-12, W_L ≥ 0.99, Π = 1 to 1e-12 in the topological phase; in the trivial phase |E₀| ≥ 0.4 (the gap edge) and W_L < 0.5. The exact harness `ssh_exact.py` passes (exit 0).
- G2: under P_chiral at any ε < 1 the spectrum is symmetric about 0 to 1e-12 (chiral symmetry is preserved by construction); under P_onsite it is not (at ε = 0.5 the asymmetry exceeds 1e-3). This checks that the perturbations do what they are meant to do.

## Predictions (fixed now)
- **P1 (protection inside the symmetry class).** Under P_chiral, for every ε ≤ 0.5 the median |E₀| is ≤ 1e-6 (an exact zero mode survives: the odd chain's chiral block stays rank-deficient whatever the couplings, as long as no coupling vanishes) and the fraction of draws with W_L ≥ 0.9 is ≥ 0.9 for ε ≤ 0.3.
- **P2 (the mode leaves the end before it leaves zero energy).** Under P_chiral the first ε at which the W_L fraction drops below 0.5 is at least 0.5 (couplings must come close to closing the gap |w|(1−ε) < |v|(1+ε), i.e. ε ≥ 1/3, before the localisation length reaches the chain).
- **P3 (loss outside the class scales with the gap).** Under P_onsite the median |E₀| grows linearly in ε with slope between 0.2 and 0.8 (the end mode acquires the local on-site energy, of order ε times a fraction), and W_L stays ≥ 0.9 up to ε = 0.3 (on-site disorder shifts the energy but does not delocalise a mode whose localisation length ξ = 1/ln(w/v) ≈ 1.4 sites is far below N).
- **P4 (next-nearest-neighbour hopping is the harsher breaking).** Under P_nnn the median |E₀| at ε = 0.1 exceeds the P_onsite median at the same ε, and the W_L fraction falls below 0.5 at some ε ≤ 0.5.
- **P5 (trivial control).** In the trivial phase no perturbation at any ε ≤ 0.3 produces a draw with |E₀| < 0.1 and W_L ≥ 0.9 (no accidental end mode).

## What a refutation would mean (written now)
P1 refuted: the finite-chain zero mode is not protected by chiral symmetry alone, and the theorem's hypothesis is incomplete (coupling signs or a vanishing coupling matter). P2 refuted: delocalisation precedes the gap closing, contrary to the localisation-length argument. P3 refuted: the symmetry-breaking response is not linear, or on-site disorder delocalises.
P4 refuted: same-sublattice hopping is no worse than on-site terms. P5 refuted: the end-mode detector fires in the trivial phase and the observable is not specific.

## Not claimed
That the physical channel of axis 1a is described by this Hamiltonian (that is the experiment's own question); anything about the infinite chain (Toeplitz index, T3); interacting systems; anything about the quantum Hall or Chern cases; anything about holography.
