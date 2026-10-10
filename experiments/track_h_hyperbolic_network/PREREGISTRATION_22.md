# Preregistration 22: where does localisation fail under hardware-like perturbations? (task Q8b)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-4 (what the measurement chain of the garage build
must achieve). **Why:** preregistration 17 (H3-X-0009) never reached a failure on 49 of 50 cells, so it bounded the
hardware requirements from below without locating them (a ceiling, LL-A10). Before running a wider grid, the
decoder geometry was worked out analytically, so that this card tests predictions instead of mapping blindly. The
derivations below were written, and their numbers computed, **before** the experiment script was run (no Monte Carlo
was run for them; the prediction function only evaluates the noiseless decode).

## What the geometry says (derived now)
Let P be the Neumann-to-Dirichlet map of a board and d_k = ΔP_k the dictionary signature of candidate k (node and
contrast). Current conservation gives P1 = 0 and Pᵀ1 = 0, hence **every d_k has zero row sums and zero column sums**
(checked numerically below, gate G2).
1. **Offsets are exactly invisible.** A perturbation of the form u1ᵀ (a per-measurement-channel offset), 1wᵀ (a
   per-injection offset), or their sum, added independently to the two maps, enters the decoder statistic
   ‖x − d_k‖² as 2 O·(d_v + n − d_k) + ‖O‖², with O·d_k = 0 for every k; the remaining terms (2 O·n, ‖O‖²) are the same for
   all candidates. So the **decoded node is identical, trial by trial, with the same noise draws**, at any offset size.
   Only offsets that vary in both indices (entry-wise patterns) matter, and those are noise. H3-X-0009's offset
   cells were a special case (u = constant), and the prediction I made there (that a 1 % offset breaks the flat board)
   was wrong for a reason derivable from the conservation law (LL-A16).
2. **Scalar gain drift is not invisible and its effect is computable.** With the second map scaled by (1 + δ),
   x = d_v + δ (P0 + d_v) + noise, and the node decision is the argmin over nodes of the minimum over contrasts of
   ‖x − d_{n,f'}‖², which is linear in δ for every candidate. Averaging the noiseless decision over δ ~ N(0, σ²) (an
   exact scan on a fine δ grid, over the whole deepest class) gives the expected top-1 as a function of σ. The decoder
   returns the node, so a contrast error at the right node is not a failure; this matters (my first analytic attempt
   forgot it and predicted failures several times too early).
3. **A gain-fitted decoder removes scalar drift exactly**, up to noise amplified by (1 + δ).
4. **Quantisation** to step q = 2^(−bits)·s (s the rms entry) of both maps adds, if treated as white noise, an equivalent
   relative noise ε_eq = 2^(−bits)/√12 per map. Undithered rounding of a small difference is gentler than white noise
   (only a fraction |δ|/q of entries flip), so ε_eq is a pessimistic estimate. With the measured noise margins of
   H3-X-0006 (ε_loc for f = 2: 1×10⁻¹ on {7,3} L=2, 1×10⁻² on square R=6; for f = 1.25: 3×10⁻², 3×10⁻³) this gives the
   bit counts b_hi below.

**Disclosure.** The 1 % drift cells of H3-X-0009 (plain decoder, f = 2: 1.00 on {7,3} L=2, 0.95 on square R=6) were known
before the predictions were computed, and they agree with them (1.0 and 0.94). Those two cells are therefore not
independent tests; the other 26 drift cells, all of f = 1.25 and everything beyond 1 %, are.

## Design
Boards: {7,3} L=2 and square R=6 (the two boards of the garage build); contrasts f ∈ {2, 1.25}; deepest depth class
(7 equivalent nodes on {7,3}, 1 node on the square); i.i.d. noise 3×10⁻⁴ (the budget) on each map as in H3-X-0009;
**40 trials per cell**, noise draws common to all cells of a (board, contrast), so that decisions can be compared
trial by trial; decoder, dictionary and node list from `exp17_localisation_under_correlated_hardware_n.py` (matched
filter over all interior nodes, contrasts {0.1, 0.5, 0.8, 1.25, 2, 5, 10, 100}). Perturbation families:
- **Offsets** u1ᵀ, 1wᵀ and u1ᵀ + 1wᵀ with entries N(0, (k·s)²), independent per map, k ∈ {1, 10, 100}, plain decoder.
- **Scalar drift** σ ∈ {10⁻³, 3×10⁻³, 10⁻², 3×10⁻², 10⁻¹, 3×10⁻¹, 1}: second map scaled by (1 + δ), δ ~ N(0, σ²),
  plain decoder; and the gain-fitted decoder at σ ∈ {0.1, 0.3} for f = 2.
- **Quantisation** to 1, 2, 3, 4, 5, 6, 7, 8, 10 bits (step 2^(−bits)·s), plain decoder.
- **Per-channel gain mismatch (exploratory, no prediction):** row gains (1 + g_i), g_i ~ N(0, σ_g²) independent per
  channel and per map, σ_g ∈ {10⁻³, 3×10⁻³, 10⁻², 3×10⁻², 10⁻¹, 3×10⁻¹}, plain decoder. This is what channel-to-channel
  gain differences between two measurements would look like; it is not invisible (a diagonal scaling of P).
Data file: `data/hardware_noise_failure_boundaries.json`.

## Validity gates
- G1: top-1 ≥ 0.9 with no perturbation (i.i.d. 3×10⁻⁴ only) in all four (board, contrast) cells.
- G2: for every dictionary signature the largest absolute row sum and column sum are ≤ 10⁻⁹ of the largest entry, on both boards.
- G3: the noiseless decode at zero perturbation returns the true node for every node of the class, both contrasts, both boards.
- G4: the drift predictions recomputed inside the run agree with the preregistered table (`PREREG_DRIFT` in the script) to 2×10⁻³.

## Predictions (fixed now)
- **P1 (offsets invisible).** For every offset structure and scale, on every board and contrast, the number of trials
  whose decoded node differs from the unperturbed decoded node (same noise draws) is **0**. **Refuted if** any cell has
  a difference.
- **P2 (drift curve).** For all 28 (board, contrast, σ) cells, the measured top-1 lies within 3·√(p(1 − p)/40) + 0.05 of
  the preregistered value p (table in the script; e.g. square R=6, f=2: 1.0, 1.0, 0.940, 0.805, 0.556, 0.221, 0.069 for
  the seven σ; {7,3} L=2, f=2: 1.0, 1.0, 1.0, 0.943, 0.682, 0.563, 0.360). **Refuted if** any cell lies outside.
- **P3 (gain fitting removes drift).** With the gain-fitted decoder, top-1 ≥ 0.9 at σ = 0.3 on both boards (f = 2).
  **Refuted if** either is below 0.9.
- **P4 (quantisation lower bound on the margin).** With b_hi = 2 ({7,3} L=2, f=2), 5 (square R=6, f=2), 4 ({7,3} L=2,
  f=1.25) and 7 (square R=6, f=1.25): top-1 ≥ 0.9 at every tested bit count above b_hi and ≥ 0.8 at b_hi itself.
  **Refuted if** any cell is below.
- **P5 (quantisation fails somewhere).** Square R=6 has top-1 < 0.9 at some bit count in {1, 2, 3} for f = 2 and in
  {1, 2, 3, 4} for f = 1.25 (where ε_eq exceeds the next noise grid point of H3-X-0006). **Refuted if** either is
  false; that would mean undithered quantisation is gentler than white noise, which the derivation above allows.

## What a refutation would mean (written now)
P1 refuted: an error in the invariance argument (for example a non-zero-sum signature, caught by G2) or float precision
at offset 100·s. P2 refuted: the decoder's behaviour under drift is not captured by the noiseless decode integrated
over δ (noise interacts with the drift error more than assumed), or contrast confusion is not benign. P3 refuted: the
fitted decoder is not exact under noise amplification. P4/P5: the white-noise equivalence is wrong in one direction
(P4: quantisation is worse than white noise; P5: it is better).

## Not claimed
Hardware (everything here is simulation); correlations inside one map; multi-node defects; contrasts outside
{1.25, 2}; boards larger than N ≈ 113; anything about holography.
