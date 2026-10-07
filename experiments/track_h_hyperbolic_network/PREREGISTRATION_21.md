# Preregistration 21: the flat growth rate over matched relative depth windows (task Q5e, EXPLORATORY)

**Date:** 2026-10-07, committed before the run. **Roadmap item:** H-2. **Why:** H0-X-0012 refuted an R-independent
growth rate of the depth-restricted condition number on flat disks, and LL-A15 traced part of that to mismatched
depth windows. This card measures the rate the right way, over windows fixed in relative depth, as a function of R on
both flat families. It is **exploratory**: the argument of `MECHANISM_NOTE.md` does not yet predict the rate, and the
two predictions below are extrapolations of the two points already measured, stated so that they can fail.

## Design
Instances: square R ∈ {6, 10, 16, 22}; triangular R ∈ {3.225, 6.45, 10.75, 17.2}; unit conductances, full boundary.
Columns and edge depth as in preregistration 18; log₁₀ κ_d of the Jacobian restricted to depth ≤ d from the explicit
Jacobian (every instance has ≤ 2×10⁸ entries), usable only while log₁₀ κ_d ≤ 13 (d* = largest usable depth).
Window: W = {d : 0.2·d_max ≤ d ≤ 0.5·d_max, d ≤ d*}, and the rate r = (log₁₀ κ_{max W} − log₁₀ κ_{min W})/(max W − min W),
reported with the window actually used and a flag when the window was truncated by d*. Also recorded, per depth
class: the smallest eigenvalue λ_min of the normalised Gram matrix and f_d (exploratory, not scored).
Data file: `data/flat_growth_rate_over_matched_relative_w.json`; figure `data/fig_flat_rate.pdf`.

## Validity gates
- G1: the window W contains at least three depths (two increments) on every instance.
- G2: for square R=10 and triangular R=6.45, log₁₀ κ_{d_max} reproduces `data/h0.json` within 1e-5.

## Predictions (weak; extrapolated from H0-X-0011 and H0-X-0012)
- **P1 (rate grows with R).** On each family, r is strictly increasing along the four values of R. **Refuted if** it
  decreases anywhere on either family.
- **P2 (triangular above square).** At every matched pair (square R=6 vs triangular R=3.225, 10 vs 6.45, 16 vs 10.75,
  22 vs 17.2) the triangular rate exceeds the square rate. **Refuted if** any pair is reversed.

## Not claimed
Any mechanism for the rate; hyperbolic tilings (their rate does not grow with L, H0-X-0012); depths beyond d*;
anything about holography.
