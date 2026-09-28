# Preregistration 8: localising a single-node defect from the difference of two boundary maps (roadmap H-3)

**Date:** 2026-09-28, committed before the run. Predictions use the noiseless signal-vs-contrast curve
(`data/contrast_signal.json`, exploratory, ledger H3-X-0004) and the noise floors of preregistration 6/7.

## Task
Two Neumann-to-Dirichlet maps of the same board are measured, each with independent i.i.d. Gaussian noise ε = 3×10⁻⁴
(relative to the rms entry of P). One of them has a defect: every edge of one interior node multiplied by a contrast
f. Decoder (a dictionary matched filter, assuming a single-node defect and a **known finite contrast set**):
for every interior node v and every f in D = {0.1, 0.5, 0.8, 1.25, 2, 5, 10, 100}, precompute the noiseless
difference ΔP_dict(v, f) = P_defect(v, f) − P_ideal from the ideal model; the estimate is the (v, f) minimising
‖ΔP_meas − ΔP_dict(v, f)‖_F. The board is the ideal unit-conductance network (tolerance is not included; it cancelled
in the differential detection regime of prereg 7, but its effect on localisation is untested).

## Cases
Four lattices ({7,3} L=2 and L=3; square R=6 and R=10). Depth classes: depth 1, mid (⌊d_max/2⌋), maximal. True
contrast f ∈ {0.8, 1.25, 2, 10, 100} (all in D). 20 trials per (lattice, depth, contrast): the defect node cycles
through the nodes of that depth class, with a fresh noise realisation per trial (seeded).
Metrics: **top-1** = fraction of trials in which the estimated node is exactly the true node; mean graph distance
(hops) between estimate and truth; contrast accuracy.

## Predictions (fixed now)
- **L1 (strong contrast, shallow or mid depth: works everywhere).** For f ∈ {10, 100} at depth 1 and mid depth,
  top-1 ≥ 0.9 on all four lattices.
- **L2 (deep, moderate contrast: geometry separates the lattices).** At maximal depth and f = 2:
  top-1 ≥ 0.8 on {7,3} L=3 and top-1 ≤ 0.5 on square R=10.
- **L3 (deep, weak contrast).** At maximal depth and f ∈ {0.8, 1.25}: top-1 ≤ 0.2 on square R=10 (its signal,
  ≈5×10⁻⁴, is only ≈3× the noise floor) and ≥ 0.5 on {7,3} L=3 (signal ≈5×10⁻³).

**Refutation:** any of L1–L3 failing as stated. Because chance level is 1/(number of interior nodes) ≈ 0.4–0.9 %,
top-1 values near 0.1–0.2 already indicate real (partial) localisation, which is why the flat-lattice threshold in
L3 is set as ≤ 0.2 and not ≈ 0.

## Not claimed
Localisation under tolerance, of multi-node or extended defects, of unknown contrast outside D, or with hardware
(non-i.i.d.) noise. Nothing about holography.
