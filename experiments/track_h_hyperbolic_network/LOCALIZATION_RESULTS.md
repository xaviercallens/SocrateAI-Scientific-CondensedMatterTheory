# Localising a single-node defect: results (2026-09-28)

Preregistration: `PREREGISTRATION_8.md` (1ba49a0, before the run). Script: `localize_defect.py`. Data:
`data/localize_defect.json`. Ledger: H3-X-0005.

**Setup.** Two NtD maps of the same ideal board, each with independent i.i.d. Gaussian noise 3×10⁻⁴; one map has
a defect (every edge of one interior node × f). A dictionary matched filter over all interior nodes and
f ∈ {0.1, 0.5, 0.8, 1.25, 2, 5, 10, 100} picks the (node, contrast) that best explains the difference. Four lattices
× three depth classes (1, mid, max) × five true contrasts {0.8, 1.25, 2, 10, 100} × 20 trials = 60 cells.

**Result: top-1 node accuracy and contrast accuracy are 1.00 in all 60 cells; mean hop error 0.**

| Prediction | Verdict |
|---|---|
| L1: f ∈ {10, 100}, depth 1 and mid, top-1 ≥ 0.9 on all four lattices | **held** |
| L2: deep, ×2: hyperbolic L=3 ≥ 0.8 *and* square R=10 ≤ 0.5 | **refuted** (square R=10: 1.00) |
| L3: deep, ×0.8 / ×1.25: square R=10 ≤ 0.2 *and* hyperbolic L=3 ≥ 0.5 | **refuted** (square R=10: 1.00) |

**What this means.** The hyperbolic lattice's larger boundary signal (up to ~8–10× at the deepest node, H3-X-0004)
gives **no localisation advantage** at this noise level and these sizes: a flat 317-node board localises even a
±20–25 % single-node defect at its deepest point without error. This cuts against using localisation as the
motivation for a hyperbolic build; the conditioning advantage of the paper is real, but at N≈100–300 and
3×10⁻⁴ noise it is not the limiting factor for this task.

**Why my predictions failed (hypothesis, not tested).** I predicted decoder performance from the SNR of the
*detection* statistic (a single norm, ≈3× the noise floor for the flat lattice). A matched filter combines all m²
correlated entries of the m×m map, so its effective sensitivity is higher by a factor of order m (76 boundary probes
on square R=10). The lesson is LL-A10.

**Limits.**
1. A 60/60 result cannot separate "solved" from "saturated": the failure boundary is unknown. A noise sweep is
   preregistered next (`PREREGISTRATION_9.md`).
2. **Oracle assumptions:** ideal board (no component tolerance, which was harmless for detection but untested
   for localisation), a known single-node defect model, and a known finite contrast set.
3. The maximal-depth class has one node on both square lattices (20 noise draws of one location) and 7 on {7,3}.
4. i.i.d. Gaussian noise is not hardware noise; multi-node and extended defects are untested.
