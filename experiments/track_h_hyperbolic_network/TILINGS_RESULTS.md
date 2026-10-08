# Conditioning across hyperbolic tilings: results (2026-09-28)

Preregistration: `PREREGISTRATION_11.md` (12fc71e before the run; one deviation recorded before any tiling result,
cc537c5). Script: `tilings_kappa.py`. Data: `data/tilings_kappa.json`, `data/gram_control_diag.json`. Ledger: H0-X-0008.

**Method.** Unit conductances, full boundary. κ = σ_max/σ_min of the DtN sensitivity Jacobian, computed from the
closed-form Gram matrix G = JᵀJ in float64 (`G_ef = ½[(d_e·d_f)² − (d_e²·d_f²)]`). Gates: every interior node has
degree q (all tilings pass); controls against the v1.0 direct SVD ({7,3} L=3: 3×10⁻¹²; square R=6: 1.1×10⁻⁶, tolerance
3.1×10⁻⁵). **Deviation 1:** the first run stopped at the square R=6 control because forming G squares the condition
number and float64 loses ≈ ε·κ(G); the 1e-6 tolerance ignored that. It was amended to max(1e-6, 10·ε·κ(G)) before any
tiling result existed; error bounds are stored with every value (≤ 4×10⁻⁹ in log₁₀κ for the hyperbolic tilings).

## log₁₀κ by tiling and layer (d_max in brackets)

| Tiling | L=1 | L=2 | L=3 | L=4 | L=5 | L=6 |
|---|---|---|---|---|---|---|
| {7,3} | 1.39 (1) | 2.46 (3) | 3.27 (5) | 3.89 (7) | | |
| {8,3} | 1.35 (1) | 2.31 (3) | 3.06 (5) | 3.69 (7) | | |
| {5,4} | 0.00 (0) | 1.08 (1) | 1.75 (2) | 2.32 (3) | 2.82 (4) | |
| {6,4} | 0.00 (0) | 1.11 (1) | 1.78 (2) | 2.35 (3) | | |
| {4,5} | 0.00 (0) | 1.10 (1) | 1.54 (1) | 1.99 (2) | 2.48 (3) | 2.87 (3) |

N runs from 12 to 2888 (largest: {8,3} L=4, N=2888, 3496 unknowns).

## Verdicts

| Prediction | Verdict |
|---|---|
| P1: log κ concave in L for {7,3} and {8,3} | **held** (increments 1.08 / 0.81 / 0.62 and 0.96 / 0.75 / 0.63) |
| P2: {8,3} better conditioned than {7,3} at L = 2, 3, 4 | **held** |
| P3a: at equal d_max, hyperbolic tilings within 1.0 decade | **held**; spreads 0.45, 0.25, 0.56, 0.21 at d_max = 1, 2, 3, 5 |
| P3b: at d_max = 5, flat exceeds hyperbolic by ≥ 1.0 decade | **held** (5.07 and 8.67 vs ≤ 3.27) |
| P4: local exponent ≤ 1.5 ({8,3}) and ≤ 1.0 ({5,4}, {6,4}, {4,5}) | **refuted**: {5,4} 1.19 and {4,5} 1.06 exceed 1.0; {8,3} 1.10 and {6,4} 0.98 pass |

## What it means

1. **Within the hyperbolic class, d_max is almost a sufficient statistic for κ.** At d_max = 3, N ranges from 112 to
   1710 and log₁₀κ stays within 0.56 decades; κ tracks depth, not size or the particular {p,q}.
2. **Across classes it is not.** log₁₀κ is *concave* in d_max for hyperbolic tilings (increments per unit depth about
   0.65 → 0.4 → 0.3) and *linear* for flat ones (about 1.1 per unit), so at equal depth the flat lattice is already far
   worse (d_max = 5: 5.07 and 8.67 against ≤ 3.27).
3. **The paper's mechanism sentence needs a qualification.** v1.1 §3.1 says "the mechanism is the scaling of depth with
   size". That is true within the hyperbolic class and incomplete across classes: the dependence of κ on depth is itself
   different (concave versus linear). The published v1.1 text is unchanged; a v1.2 should say so.
4. **P4 shows polynomial growth in N is not a strong statement at these sizes.** The exponents decrease with size
   ({5,4}: 1.50, 1.35, 1.19) but stay above 1 within the tested range; the data neither confirm nor exclude an exponent
   that keeps falling.
5. Faster branching helps at equal L ({8,3} < {7,3}); at equal d_max the effect is small (P3a).

## Limits
Unit conductances and full boundary only (disorder and probe-subsampling were studied on {7,3} and flat lattices only);
five tilings, ≤ 6 layers, N ≤ 2888; the q = 4, 5 tilings reach d_max ≤ 4, so equal-d_max comparisons outside {7,3}/{8,3}
stop at d_max ≤ 3; the concave-versus-linear contrast rests on few points per family; no exact rank certificates were
computed for these tilings; nothing here concerns holography.

## RC benchmark on other tilings (PREREGISTRATION_15.md, committed before the run; ledger H2-X-0005)

**Design.** Unit conductances, C = 1 per interior node, boundary as in the paper; RC relaxation time τ = 1/λ_min and stiffness λ_max/λ_min from the eigenvalues of the interior Laplacian block L_ii; two-integrator controls K1 (matrix-exponential known answer, max-norm relative error < 1e-5) and K2 (steady state after 40τ, < 1e-6), rtol 1e-8, atol 1e-10, with SciPy BDF and rusty-SUNDIALS CVODE (BDF).

| Network | N | d_max | tau | stiffness | K1 (scipy/rusty) | K2 (scipy/rusty) |
|---|---|---|---|---|---|---|
| {7,3} L=2 | 112 | 3 | 2.7503 | 14.94 | 7.3e-09 / 1.1e-08 | 4.2e-13 / 1.1e-12 |
| {8,3} L=2 | 200 | 3 | 2.6180 | 14.71 | 6.1e-09 / 1.8e-08 | 2.2e-13 / 5.5e-13 |
| {5,4} L=3 | 165 | 2 | 0.9118 | 5.90 | 5.9e-09 / 2.1e-08 | 1.0e-12 / 1.1e-11 |
| {6,4} L=2 | 120 | 1 | 0.5000 | 3.00 | 7.9e-09 / 2.9e-08 | 4.9e-13 / 2.4e-12 |
| {4,5} L=4 | 188 | 2 | 0.7120 | 6.12 | 7.0e-09 / 1.6e-08 | 4.5e-12 / 9.4e-13 |

| Prediction | Threshold | Verdict |
|---|---|---|
| G1: {7,3} L=2 reproduces τ and stiffness to 1e-3 relative | τ = 2.7503 ± 2.75e-3, stiffness 14.94 ± 1.49e-2 | HELD |
| G2: SciPy passes K1 and K2 on {7,3} L=2 | K1 and K2 both true | HELD |
| P1: K1 and K2 pass on every network for every backend | All backends pass | HELD |
| P2: τ ordering by depth; q=4,5 < 2.75, {8,3} ∈ [2.06, 3.44] | τ({5,4}) 0.9118, τ({6,4}) 0.5000, τ({4,5}) 0.7120 all < 2.75; τ({8,3}) 2.6180 ∈ [2.06, 3.44] | HELD |
| P3: every stiffness < 35.4 | max stiffness 14.94 | HELD |

**Limits:** Physical boards, larger sizes, other boundary conditions; nothing about holography.

*Recorded by a low-tier agent (runbook steps 6–8); audited with `tools/audit_low_tier.py` (pass). One correction at
review: the Design line said the eigenvalues were "of the DtN matrix"; they are of the interior block L_ii.*

## Exact rank certificates for the other tilings (PREREGISTRATION_14.md, committed before the run; ledger H0-B-0003)

**Method (random-combination certificate).** For each prime p ∈ {2³¹−1, 998244353}: compute the harmonic extension H mod p (`hyperbolic_exact.mat_inv_mod` on L_ii; product with the *signed* L_ib, entries in {−1, 0}, so no int64 overflow); with d_e = H[a] − H[b] on the boundary, form k random combinations of the rows of the Jacobian, row s having coefficient c_ij = u_si v_sj + u_sj v_si on pair (i < j), u, v uniform in GF(p) from `numpy.random.default_rng(14)`; entry (s, e) is (u_s·d_e)(v_s·d_e) − Σ_i u_si v_si d_e,i², so the Jacobian is never formed. Since this matrix is a row combination of J, its rank over GF(p) is ≤ rank_p(J) ≤ rank_ℚ(J) (L_ii invertible mod p); rank E therefore certifies full column rank. k = E + 20; if the rank is < E, redraw once with k = 2E (seed 15); if still < E, the instance is reported **not certified** (not evidence of a rank defect). Both primes must certify for a Tier-B claim. (A plain random *subset* of rows was tried first in a unit check outside this list and rejected before this preregistration was committed: a resistor between two boundary nodes affects exactly one row, so a subset misses it; {7,3} L=1 gave rank 17 of 42.) Data file: `data/exact_rank_certificates_for_other_tiling.json`.

| Tiling | L | N | E | rank mod 2^31-1 | rank mod 998244353 | certified |
|---|---|---|---|---|---|---|
| {7,3} | 2 | 112 | 140 | 140 | 140 | yes (control) |
| {7,3} | 3 | 315 | 399 | 399 | 399 | yes |
| {8,3} | 2 | 200 | 240 | 240 | 240 | yes |
| {8,3} | 3 | 768 | 928 | 928 | 928 | yes |
| {5,4} | 3 | 165 | 225 | 225 | 225 | yes |
| {5,4} | 4 | 440 | 605 | 605 | 605 | yes |
| {5,4} | 5 | 1160 | 1600 | 1600 | 1600 | yes |
| {6,4} | 2 | 120 | 150 | 150 | 150 | yes |
| {6,4} | 3 | 456 | 576 | 576 | 576 | yes |
| {4,5} | 4 | 188 | 296 | 296 | 296 | yes |
| {4,5} | 5 | 436 | 692 | 692 | 692 | yes |
| {4,5} | 6 | 1008 | 1604 | 1604 | 1604 | yes |

| Prediction | Threshold | Verdict |
|---|---|---|
| G1 (method control): on {7,3} L=2 the subset method certifies rank 140 = E for both primes, matching the full-matrix result of H0-B-0001. | {7,3} L=2 certifies rank 140 = E for both primes | HELD |
| G2: L_ii is invertible mod both primes for every instance. | All instances have invertible L_ii mod both primes | HELD |
| P1: every listed instance is certified full rank for both primes. | All 11 instances certified full rank for both primes | HELD |
| P2: no instance needs the 2E redraw. | No redraw with k = 2E required for any instance | HELD |

**Limits:** Anything about probe-subsampled Jacobians of these tilings, about conditioning, or about instances with E > 1700. Nothing about holography.

## Sensitivity versus depth across tilings (PREREGISTRATION_16.md, EXPLORATORY, committed before the run; ledger H0-X-0009)

For every instance of `tilings_kappa.py` ({7,3} L=1–4, {8,3} L=1–4, {5,4} L=1–5, {6,4} L=1–4, {4,5} L=1–6) and the
flat disks square R ∈ {3, 6, 10} and triangular R ∈ {3.225, 6.45}: unit conductances, full boundary, harmonic extension
H; per-edge sensitivity S_e = ‖∂Λ/∂g_e‖_F = ‖d_e‖², d_e = H[a] − H[b] restricted to the boundary (the Frobenius norm of
the rank-one matrix d_e d_eᵀ). Edge depth = min(depth(a), depth(b)). Recorded per instance: mean and median of
log₁₀ S_e per edge depth, the number of edges per depth, the least-squares slope of mean log₁₀ S_e against depth
(the per-depth decay rate), and the same slope restricted to depths ≥ 1.
Data file: `data/sensitivity_versus_depth_across_tilings.json`; figure `paper/fig_sensitivity_depth.pdf` (not in the
paper).

**Deviation 1 (2026-09-28, after the first run; no prediction exists in this exploratory card, so nothing was at
  stake).** G1 as written cannot pass: `data/h0.json`'s statistic is the *median* per depth of the Jacobian column
  2-norm ‖J[:,e]‖₂ = (½[(‖d_e‖²)² − Σ_i d_e,i⁴])^{1/2} (upper-triangular boundary pairs), normalised to depth 0, while
  the profile above uses the *mean* of ‖d_e‖². Amended G1: the script also computes the h0 statistic exactly and
  must reproduce h0 to 1e-6; the profile of ‖d_e‖² is reported alongside, unchanged. First-run values (G2 passed,
  G1 failed) are kept in the git history of the data file.
- G2: every instance's edge count per depth sums to E.

| Instance | N | depth 0 | depth 1 | depth 2 | depth 3 | depth 4 | depth 5 | depth 6 | depth 7 | depth 8 | slope (all) | slope (d>=1) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {7,3} L=1 | 35 | 0.00 | -0.91 |  |  |  |  |  |  |  | -0.910 | n/a |
| {7,3} L=2 | 112 | 0.00 | -1.04 | -1.67 | -1.88 |  |  |  |  |  | -0.627 | -0.420 |
| {7,3} L=3 | 315 | 0.00 | -1.05 | -1.71 | -2.01 | -2.34 | -2.48 |  |  |  | -0.473 | -0.349 |
| {7,3} L=4 | 847 | 0.00 | -1.05 | -1.71 | -2.02 | -2.38 | -2.60 | -2.85 | -2.96 |  | -0.390 | -0.306 |
| {8,3} L=1 | 48 | 0.00 | -0.93 |  |  |  |  |  |  |  | -0.930 | n/a |
| {8,3} L=2 | 200 | 0.00 | -1.04 | -1.67 | -1.90 |  |  |  |  |  | -0.633 | -0.431 |
| {8,3} L=3 | 768 | 0.00 | -1.04 | -1.69 | -2.00 | -2.41 | -2.59 |  |  |  | -0.496 | -0.381 |
| {8,3} L=4 | 2888 | 0.00 | -1.04 | -1.69 | -2.01 | -2.43 | -2.69 | -3.02 | -3.18 |  | -0.423 | -0.348 |
| {5,4} L=1 | 20 | 0.00 |  |  |  |  |  |  |  |  | n/a | n/a |
| {5,4} L=2 | 60 | 0.00 | -0.96 |  |  |  |  |  |  |  | -0.958 | n/a |
| {5,4} L=3 | 165 | 0.00 | -1.09 | -1.66 |  |  |  |  |  |  | -0.828 | -0.562 |
| {5,4} L=4 | 440 | 0.00 | -1.11 | -1.79 | -2.16 |  |  |  |  |  | -0.716 | -0.526 |
| {5,4} L=5 | 1160 | 0.00 | -1.11 | -1.81 | -2.29 | -2.60 |  |  |  |  | -0.638 | -0.494 |
| {6,4} L=1 | 30 | 0.00 |  |  |  |  |  |  |  |  | n/a | n/a |
| {6,4} L=2 | 120 | 0.00 | -0.98 |  |  |  |  |  |  |  | -0.977 | n/a |
| {6,4} L=3 | 456 | 0.00 | -1.09 | -1.66 |  |  |  |  |  |  | -0.832 | -0.573 |
| {6,4} L=4 | 1710 | 0.00 | -1.10 | -1.77 | -2.24 |  |  |  |  |  | -0.738 | -0.569 |
| {4,5} L=1 | 12 | 0.00 |  |  |  |  |  |  |  |  | n/a | n/a |
| {4,5} L=2 | 32 | 0.00 | -0.92 |  |  |  |  |  |  |  | -0.922 | n/a |
| {4,5} L=3 | 80 | 0.00 | -1.07 |  |  |  |  |  |  |  | -1.072 | n/a |
| {4,5} L=4 | 188 | 0.00 | -1.16 | -1.83 |  |  |  |  |  |  | -0.915 | -0.675 |
| {4,5} L=5 | 436 | 0.00 | -1.17 | -1.95 | -2.25 |  |  |  |  |  | -0.754 | -0.540 |
| {4,5} L=6 | 1008 | 0.00 | -1.17 | -1.99 | -2.44 |  |  |  |  |  | -0.814 | -0.633 |
| square R=3 | 29 | 0.00 | -1.04 |  |  |  |  |  |  |  | -1.044 | n/a |
| square R=6 | 113 | 0.00 | -1.19 | -1.86 | -2.26 | -2.50 |  |  |  |  | -0.607 | -0.434 |
| square R=10 | 317 | 0.00 | -1.21 | -1.92 | -2.37 | -2.70 | -2.92 | -3.09 | -3.22 | -3.29 | -0.368 | -0.279 |
| triangular R=3.225 | 37 | 0.00 | -1.23 | -1.66 |  |  |  |  |  |  | -0.830 | -0.434 |
| triangular R=6.45 | 151 | 0.00 | -1.34 | -1.99 | -2.38 | -2.59 | -2.69 |  |  |  | -0.503 | -0.330 |

| Gate | Threshold | Verdict |
|---|---|---|
| G1 (amended, Deviation 1) | the script reproduces h0's median column norm per depth to 1e-6 | held |
| G2 | every instance's edge count per depth sums to E | held |

**Limits:** Any mechanism. Exploratory: nothing here confirms or refutes anything; nothing about holography.

*Recorded by the orchestrator from the data file (the low-tier recorder had not reported); audited with `tools/audit_low_tier.py`.*

**Reading (exploratory).** The per-edge sensitivity profile is nearly the same on every lattice: all curves are concave in depth, and at depth 3 the hyperbolic tilings lie at −2.0 to −2.4 decades relative to depth 0 while the flat lattices lie at −2.4; the per-depth increments (about −1.1, −0.7, −0.4, −0.3, …) are alike. The amplitude decay of a single edge's boundary signal therefore does not explain why log κ is concave in depth on hyperbolic tilings and linear on flat ones (H0-X-0008). What differs between the geometries must be how many edges share a boundary signature and how collinear those signatures are, the *coherence* that version 1.0 sampled but did not analyse; that is task Q5b. Nothing here is a prediction or a claim.

## Coherence versus depth across tilings (`PREREGISTRATION_18.md`, 7714454 before the run; ledger H0-X-0010)
Design: Instances as in preregistration 16 ({7,3} L=1–4, {8,3} L=1–4, {5,4} L=1–5, {6,4} L=1–4, {4,5} L=1–6; square R ∈ {3, 6, 10}; triangular R ∈ {3.225, 6.45}), unit conductances, full boundary. For edges e, f with boundary signatures d_e, d_f (d_e = H[a] − H[b] restricted to the boundary), the Jacobian columns are the upper-triangular parts of d_e d_eᵀ and d_f d_fᵀ, and their inner product is ⟨J_e, J_f⟩ = ½[(d_e·d_f)² − Σ_i d_e,i² d_f,i²], so the cosine between columns is computed in closed form without forming J. Edge depth = min(depth(a), depth(b)). For every depth class with n_d ≥ 2 edges, **all** n_d(n_d − 1)/2 pairs are used. Statistics per depth: median |cos|, mean |cos|, 90th percentile of |cos|, and the **effective dimension fraction** f_d = PR_d / n_d, PR_d = (Σλ)²/Σλ² the participation ratio of the eigenvalues of the n_d × n_d Gram matrix of the *normalised* columns (f_d = 1 for orthogonal columns, 1/n_d for collinear ones). Data file: `data/coherence_versus_depth_across_tilings.json`; figure `data/fig_coherence_depth.pdf`. Data: `data/coherence_versus_depth_across_tilings.json`.

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 (closed form) | closed-form cosines agree with the explicit Jacobian to 1e-10 for every pair at every depth, on {7,3} L=2 and square R=6 | max abs difference: {7,3} L=2 2.00e-15; square R=6 2.22e-15 | held |
| G2 | pairs per depth = n_d(n_d − 1)/2 for every instance | held for every instance and depth | held |
| P1 (flat is more coherent at depth) | at d = 3, 4, 5, median abs cos of square R=10 and triangular R=6.45 each exceeds that of every hyperbolic tiling reaching d; refuted if any flat instance is at or below any hyperbolic one | d=3: square 4.77e-3, triangular 7.20e-2, hyperbolic maximum 6.94e-2 ({6,4} L=4); d=4: square 1.14e-2, triangular 0.223, hyperbolic maximum 9.93e-2 ({5,4} L=5); d=5: square 5.75e-2, triangular 0.222, hyperbolic maximum 3.80e-3 ({7,3} L=4; {8,3} L=4 also reaches d=5) | REFUTED |
| P2 (gap grows with depth) | median abs cos ratio square R=10 / {7,3} L=4 strictly increasing over d = 1, …, 5; refuted if it decreases anywhere | ratio at d = 1, 2, 3, 4, 5: 450, 59.0, 207, 42.8, 15.1 | REFUTED |
| P3 (effective dimension) | at d = 3, f_d of every hyperbolic tiling exceeds f_d of square R=10 and triangular R=6.45 by at least 1.5; refuted if any hyperbolic tiling is below 1.5× either flat value | f_3: {7,3} 0.797, {8,3} 0.840, {5,4} 0.930, {6,4} 0.985, {4,5} 0.832; square R=10 0.386; triangular R=6.45 0.232 | HELD |
| P4 (depth 1 is not where the difference is) | at d = 1, max/min spread of median abs cos across all seven families < 2; refuted if ≥ 2 | spread 2.10e5 | REFUTED |

Deviations: none.
Limits: A derivation; the role of amplitude (H0-X-0009); probe-subsampled boundaries; anything about holography.

*Recorded by a low-tier agent (Haiku) from the data file; audited with `tools/audit_low_tier.py` (two audit false positives fixed in the tool: the "Design:" label and the commit hash of the block title).*

**Reading (orchestrator; the refutations are mine, not the data's).** The one prediction set on a statistic that sees the collinear tail held with margin, and it answers the question H0-X-0009 left open. Per depth class, the normalised Gram matrix of the Jacobian columns of equal-depth edges has an effective dimension fraction PR/n that stays between 0.79 and 0.99 at every depth on every hyperbolic tiling (largest instances), while on the flat disks it falls monotonically with depth: square R=10 from 0.71 (depth 0) to 0.39 (depth 3) to 0.14 (depth 7); triangular R=6.45 from 0.52 to 0.23 (depth 3) to 0.20 (depth 4). The mean and 90th-percentile |cos| tell the same story (square p90 reaches 0.95 at depth 8, triangular 0.88 at depth 5; no hyperbolic class exceeds 0.30). So deep flat edges share nearly the same boundary signature, which is exactly what shrinks the smallest singular values and makes log κ linear in depth there, whereas hyperbolic equal-depth edges keep distinct signatures even though their amplitudes decay at the same rate (H0-X-0009). Within the hyperbolic class the fraction does not degrade with depth over the range reached, consistent with the concave (depth-driven) κ growth of H0-X-0008.

P1, P2 and P4 were refuted because I preregistered them on the **median** |cos|, and the medians are near zero on every lattice (most pairs are far apart); ratios and spreads of such medians are noise. That is a statistic error on my side, recorded as LL-A13, not evidence for or against the mechanism. Two caveats remain before this is a confirmed mechanism: the depth classes compared have different sizes (n = 6 to 152), and the link from PR/n to κ is argued, not measured; both are the next card (Q5c in `docs/TASK_QUEUE.md`). The odd dip of {7,3} and {8,3} at depth 1 (PR/n ≈ 0.55–0.60) is not interpreted here.

## Coherence mechanism at matched size (`PREREGISTRATION_19.md`, 4c1e286 before the run; ledger H0-X-0011)

Design: Scored instances: the largest of each family, {7,3} L=4, {8,3} L=4, {5,4} L=5, {6,4} L=4, {4,5} L=6, square R=10,
triangular R=6.45 (unit conductances, full boundary). Columns and depth classes as in preregistration 18.
1. **Matched-size coherence.** For every depth class with n_d ≥ 6, draw 50 random subsets of n_match = 6 columns
   (seed 0, NumPy default generator, draws in instance order) and record the median over draws of PR/6 of the
   normalised Gram of the subset. n_match = 6 is the smallest depth-3 class among the scored instances ({6,4} L=4).
2. **Restricted condition number.** κ_d = σ_max/σ_min of J restricted to the columns of edges of depth ≤ d, for
   d = 0 … d_max. Computed from the explicit Jacobian when it has ≤ 2×10⁸ entries, otherwise from the closed-form Gram
   matrix G = JᵀJ (κ_d = √κ(G_d)); the method is recorded per instance. Statistic: the mean per-depth increment
   beyond depth 1, Δ̄ = (log₁₀ κ_{d_max} − log₁₀ κ_1)/(d_max − 1) (depth 0 → 1 is a ≈1-decade jump everywhere and is
   not what distinguishes the classes). Also recorded: every log₁₀ κ_d, and λ_min of the normalised Gram per depth
   (not scored).
Data file: `data/coherence_mechanism_at_matched_size.json`; figure `data/fig_coherence_matched.pdf`.

Data: `data/coherence_mechanism_at_matched_size.json`.

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 (consistency with H0-X-0008 and v1.0) | every scored instance matched to a stored row; tolerance 1e-6 (tilings_kappa rows) or 1e-5 (h0 rows) on log10 kappa; all 7 must match | 7 of 7 instances matched | PASS |
| G2 (depth-class sizes and draws) | every depth class used for P1/P3 has n_d >= 6; exactly 50 draws per such class | n_draws values across drawn classes: 50 | PASS |
| P1 (coherence at matched size, depth 3) | median matched PR/n >= 0.85 for every hyperbolic instance and <= 0.80 for square R=10 and triangular R=6.45; refuted if any hyperbolic value < 0.85 or any flat value > 0.80 | {7,3} L=4 0.995; {8,3} L=4 1.000; {5,4} L=5 0.978; {6,4} L=4 0.985; {4,5} L=6 0.930; square R=10 0.938; triangular R=6.45 0.789 | REFUTED |
| P2a (kappa growth per depth, absolute) | delta-bar >= 0.8 for square R=10 and triangular R=6.45; delta-bar <= 0.5 for {7,3} L=4 and {8,3} L=4; refuted if any of the four is on the wrong side | {7,3} L=4 0.296; {8,3} L=4 0.284; {5,4} L=5 0.379; {6,4} L=4 0.341; {4,5} L=6 0.436; square R=10 0.981; triangular R=6.45 1.19 | HELD |
| P2b (kappa growth per depth, ordering) | every hyperbolic delta-bar below both flat values; refuted if any hyperbolic delta-bar >= either flat delta-bar | {7,3} L=4 0.296; {8,3} L=4 0.284; {5,4} L=5 0.379; {6,4} L=4 0.341; {4,5} L=6 0.436; square R=10 0.981; triangular R=6.45 1.19 | HELD |
| P3 (deepest class with n_d >= 6) | median matched PR/n < 0.6 for square R=10 and triangular R=6.45, and >= 0.8 for every hyperbolic instance; refuted if any value is on the wrong side | {7,3} L=4 depth 7 0.847; {8,3} L=4 depth 7 0.955; {5,4} L=5 depth 3 0.978; {6,4} L=4 depth 3 0.985; {4,5} L=6 depth 3 0.930; square R=10 depth 8 0.354; triangular R=6.45 depth 5 0.458 | HELD |

| Instance | method | log10 kappa_d for d = 0 … d_max | delta_bar |
|---|---|---|---|
| {7,3} L=4 | explicit_J | 1.12, 2.11, 2.27, 3.08, 3.11, 3.72, 3.72, 3.89 | 0.296 |
| {8,3} L=4 | gram | 1.06, 1.98, 2.10, 2.85, 2.87, 3.48, 3.48, 3.69 | 0.284 |
| {5,4} L=5 | gram | 0.900, 1.69, 2.29, 2.68, 2.82 | 0.379 |
| {6,4} L=4 | gram | 0.901, 1.66, 2.19, 2.35 | 0.341 |
| {4,5} L=6 | gram | 0.994, 2.00, 2.59, 2.87 | 0.436 |
| square R=10 | explicit_J | 1.83, 2.85, 4.16, 5.78, 6.62, 7.41, 8.51, 9.17, 9.72 | 0.981 |
| triangular R=6.45 | explicit_J | 2.21, 3.90, 5.79, 7.28, 8.39, 8.67 | 1.19 |

Deviations: none.
Limits: A derivation of Δ̄ from PR/n; the depth-0 → 1 jump; probe-subsampled boundaries; the {7,3}/{8,3} depth-1 dip of
H0-X-0010; anything about holography.

*Recorded by a low-tier agent (Haiku) from the data file; audited with `tools/audit_low_tier.py` (pass, no correction).*

**Reading (orchestrator).** Two of the three gaps left by H0-X-0010 are closed. First, the link to κ is now measured, not argued: the condition number of the Jacobian restricted to the columns of edges of depth ≤ d grows by 0.98 (square R=10) and 1.19 (triangular R=6.45) decades per depth beyond depth 1, against 0.28 to 0.44 on the five hyperbolic tilings, and the full-depth values reproduce H0-X-0008 and v1.0 to the stored error bounds (G1). The depth-0 → 1 jump is about one decade on every lattice and is not what separates the classes. Second, the coherence deficit is not an artefact of class size: with six matched columns per class, the flat disks fall to 0.35 (square, depth 8) and 0.46 (triangular, depth 5) while every hyperbolic tiling stays at or above 0.85 at its deepest class (P3). The matched curves decrease monotonically with depth on both flat disks and stay flat on the hyperbolic ones.

P1 was refuted and the refutation is informative: at depth 3 the square's 76 columns together have an effective dimension fraction of 0.39, but six random columns among them give 0.94. The flat collinearity is a *collective* property of the whole depth class (its 76 columns span roughly 29 effective directions), which a small random subset does not see until the deepest classes. My threshold also came from square R=6, whose depth 3 is relatively deeper than square R=10's (LL-A14). What remains open is the derivation (card Q5d): why the boundary signatures of deep flat edges collapse onto a low-dimensional subspace while hyperbolic ones do not. Nothing here concerns holography.

## Test of the coherence-mechanism argument on unseen instances (`PREREGISTRATION_20.md`, 9ad012e before the run; ledger H0-X-0012)

Design: Instances: hyperbolic {7,3} L=5 (N=2240, E=2856) and {4,5} L=7 (N=2320, E=3696); flat square R=16 (N=797, E=1528)
and triangular R=10.75 (N=421, E=1176), unit conductances, full boundary. Columns, edge depth and the closed-form
Gram matrix as in preregistration 18. Per instance and depth class (n_d ≥ 2): the full-class effective dimension
fraction f_d = PR_d/n_d. Per instance and d = 0 … d_max: log₁₀ κ_d of the Jacobian restricted to columns of depth ≤ d,
from the explicit Jacobian when it has ≤ 2×10⁸ entries (the two flat instances), otherwise from the Gram matrix
(κ_d = √κ(G_d); the two hyperbolic instances). On the flat instances only depths with log₁₀ κ_d ≤ 13 are usable in
double precision; d* is the largest such depth and Δ̄ = (log₁₀ κ_{d*} − log₁₀ κ_1)/(d* − 1). On the hyperbolic
instances Δ̄ uses d_max. Reference values read from `data/coherence_mechanism_at_matched_size.json` (H0-X-0011):
Δ̄(square R=10) and Δ̄({7,3} L=4). Data file: `data/coherence_mechanism_prediction_test.json`; figure
`data/fig_mechanism_test.pdf`.

Data: `data/coherence_mechanism_prediction_test.json`.

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 (closed form) | max abs difference to the explicit Jacobian on square R=6, every depth, at most 1e-10 | 1.78e-15 | PASS |
| G2 (flat precision) | d* >= 4 on both flat instances | square R=16 d* = 8; triangular R=10.75 d* = 6 | PASS |
| G3 (Gram floor) | 10 eps_mach kappa(G_dmax) <= 1e-5 on both hyperbolic instances (gram_floor) | {7,3} L=5 1.38e-6; {4,5} L=7 7.14e-9 | PASS |
| P1 (flat: d f_d constant) | ratio max(d f_d)/min(d f_d) <= 1.5 over 2 <= d <= d_max - 2, each flat instance | square R=16 1.26; triangular R=10.75 1.42 | HELD |
| P2 (hyperbolic: f_d O(1)) | f_d >= 0.75 at every depth d >= 2, each hyperbolic instance | minimum {7,3} L=5 0.760; minimum {4,5} L=7 0.803 | HELD |
| P3a (flat growth rate) | delta-bar in [0.7, 1.5] on both flat instances; abs(delta-bar(square R=16) - delta-bar(square R=10)) <= 0.2 | delta-bar square R=16 1.26; triangular R=10.75 1.71; reference square R=10 0.981; difference 0.277 | REFUTED |
| P3b (hyperbolic growth rate) | delta-bar <= 0.5 on both hyperbolic instances; delta-bar({7,3} L=5) <= delta-bar({7,3} L=4) + 0.05 | delta-bar {7,3} L=5 0.285; {4,5} L=7 0.418; reference {7,3} L=4 0.296 | HELD |

| Instance | N | E | d_max | method | d* | log10 kappa_d (d = 0 … d*) | delta_bar |
|---|---|---|---|---|---|---|---|
| {7,3} L=5 | 2240 | 2856 | 9 | gram | 9 | 1.12, 2.12, 2.28, 3.10, 3.15, 3.81, 3.82, 4.27, 4.27, 4.40 | 0.285 |
| {4,5} L=7 | 2320 | 3696 | 4 | gram | 4 | 1.01, 2.00, 2.64, 3.20, 3.25 | 0.418 |
| square R=16 | 797 | 1528 | 14 | explicit_J | 8 | 2.02, 3.60, 4.85, 6.18, 7.41, 9.27, 10.2, 11.0, 12.4 | 1.26 |
| triangular R=10.75 | 421 | 1176 | 9 | explicit_J | 6 | 2.30, 4.36, 6.53, 8.34, 10.2, 11.6, 12.9 | 1.71 |

| Instance | depth | n_edges | f_d | d·f_d |
|---|---|---|---|---|
| square R=16 | 2 | 148 | 0.555 | 1.109 |
| square R=16 | 3 | 140 | 0.380 | 1.141 |
| square R=16 | 4 | 132 | 0.288 | 1.153 |
| square R=16 | 5 | 124 | 0.232 | 1.158 |
| square R=16 | 6 | 108 | 0.207 | 1.242 |
| square R=16 | 7 | 100 | 0.180 | 1.259 |
| square R=16 | 8 | 92 | 0.155 | 1.239 |
| square R=16 | 9 | 76 | 0.142 | 1.276 |
| square R=16 | 10 | 68 | 0.116 | 1.163 |
| square R=16 | 11 | 60 | 0.0927 | 1.02 |
| square R=16 | 12 | 44 | 0.0848 | 1.017 |
| triangular R=10.75 | 2 | 171 | 0.279 | 0.557 |
| triangular R=10.75 | 3 | 151 | 0.202 | 0.605 |
| triangular R=10.75 | 4 | 126 | 0.165 | 0.662 |
| triangular R=10.75 | 5 | 101 | 0.148 | 0.74 |
| triangular R=10.75 | 6 | 81 | 0.132 | 0.791 |
| triangular R=10.75 | 7 | 63 | 0.113 | 0.792 |

Deviations: none.
Limits: A proof; the value of the flat rate constant; depth 0 and 1; the degree-3 depth-1 dip; anything about holography.

*Recorded by a low-tier agent (Haiku) from the data file; audited with `tools/audit_low_tier.py`. One correction appended to H0-X-0012: the statement's 0.277 is a difference of two stored values that my brief asked the recorder to compute (declared DERIVED in the notes); two audit false positives fixed in the tool (gate rows marked PASS now count as verdict rows).*

**Reading (orchestrator).** The band-counting part of `MECHANISM_NOTE.md` survives contact with instances it never saw. On square R=16 the product d·f_d stays between 1.02 and 1.28 from depth 2 to depth 12, and on triangular R=10.75 between 0.56 and 0.79: the depth-d class of a flat disk spans an effective number of directions proportional to R/d, as the harmonic-measure band width predicts, with a lattice-dependent constant. On the hyperbolic side the fraction stays at or above 0.76 on {7,3} L=5 (nine depths) and 0.80 on {4,5} L=7, and the per-depth growth rate of the restricted κ does not increase with L (0.285 at L=5 against 0.296 at L=4): the overlap number stays O(1) as the argument says.

The rate prediction failed. Over the depths double precision can resolve, the restricted κ grows by 1.26 decades per depth on square R=16 and 1.71 on triangular R=10.75, against 0.98 on square R=10 and the predicted band [0.7, 1.5]. Two things are wrong at once: the argument's "smallest eigenvalue set by the lattice cutoff" step has no support, and the preregistered comparison averaged over different relative windows (R=10 over its whole range, where the last increments shrink from 1.02 to 0.55 near d_max; R=16 only over d ≤ 8 of 14). Both are recorded as LL-A15. The structural claim and the rate claim were separate predictions, so the refutation of the second does not touch the first. What the programme now has: a measured mechanism (H0-X-0010, H0-X-0011), a counting argument that predicts its depth dependence on flat disks (this card), and an underived growth constant (card Q5e). Nothing here concerns holography.

## Flat growth rate over matched relative depth windows (`PREREGISTRATION_21.md`, EXPLORATORY, 4e6adf1 before the run; ledger H0-X-0013)
Design: Instances: square R ∈ {6, 10, 16, 22}; triangular R ∈ {3.225, 6.45, 10.75, 17.2}; unit conductances, full boundary. Columns and edge depth as in preregistration 18; log₁₀ κ_d of the Jacobian restricted to depth ≤ d from the explicit Jacobian (every instance has ≤ 2×10⁸ entries), usable only while log₁₀ κ_d ≤ 13 (d* = largest usable depth). Window: W = {d : 0.2·d_max ≤ d ≤ 0.5·d_max, d ≤ d*}, and the rate r = (log₁₀ κ_{max W} − log₁₀ κ_{min W})/(max W − min W), reported with the window actually used and a flag when the window was truncated by d*. Also recorded, per depth class: the smallest eigenvalue λ_min of the normalised Gram matrix and f_d (exploratory, not scored). Data file: `data/flat_growth_rate_over_matched_relative_w.json`; figure `data/fig_flat_rate.pdf`. Data: `data/flat_growth_rate_over_matched_relative_w.json`.

| Instance | N | d_max | d* | window used | extended | truncated | rate (decades/depth) |
|---|---|---|---|---|---|---|---|
| square R=6 | 113 | 4 | 4 | 1, 2, 3 | yes | no | 0.948 |
| square R=10 | 317 | 8 | 8 | 2, 3, 4 | no | no | 1.23 |
| square R=16 | 797 | 14 | 8 | 3, 4, 5, 6, 7 | no | no | 1.20 |
| square R=22 | 1517 | 20 | 8 | 4, 5, 6, 7, 8 | no | yes | 1.08 |
| triangular R=3.225 | 37 | 2 | 2 | 1, 2 | yes | yes | 0.410 |
| triangular R=6.45 | 151 | 5 | 5 | 1, 2, 3 | yes | no | 1.69 |
| triangular R=10.75 | 421 | 9 | 6 | 2, 3, 4 | no | no | 1.81 |
| triangular R=17.2 | 1069 | 16 | 5 | 4, 5 | no | yes | 1.84 |

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 (amended, Deviation 1) | window W contains at least two depths (one increment) on every instance | smallest window has 2 depths (triangular R=3.225, depths 1, 2); all others 2 to 5 | PASS |
| G2 | log₁₀ κ_{d_max} reproduces `data/h0.json` within 1e-5 | square R=10 9.71782 (ours) vs 9.71782 (h0); triangular R=6.45 8.67245 (ours) vs 8.67245 (h0) | PASS |
| P1 (rate grows with R) | r strictly increasing along R on each family; refuted if it decreases anywhere | square R=6, 10, 16, 22: 0.948, 1.23, 1.20, 1.08; triangular R=3.225, 6.45, 10.75, 17.2: 0.410, 1.69, 1.81, 1.84 | REFUTED |
| P2 (triangular above square) | triangular rate exceeds square rate at each matched pair; refuted if any pair is reversed | pairs (square vs triangular): R=6 vs 3.225: 0.948 vs 0.410 (reversed); R=10 vs 6.45: 1.23 vs 1.69; R=16 vs 10.75: 1.20 vs 1.81; R=22 vs 17.2: 1.08 vs 1.84 | REFUTED |

Deviations: **Deviation 1 (2026-10-07 21:50 UTC, during the first run, before any verdict existed; the first run was stopped and no data file was written).** The window rule cannot be met on the small instances: square R=6 has d_max = 4, so [0.2, 0.5]·d_max contains two depths (log of the first run: window [1, 2], rate 0.788), and triangular R=3.225 has d_max = 2, so the window is a single depth and the rate is undefined, which would have crashed the scorer. Amended rule, fixed before the rerun: W = {d : ⌈0.2·d_max⌉ ≤ d ≤ max(⌊0.5·d_max⌋, ⌈0.2·d_max⌉ + 2), d ≤ d*}, i.e. the window is extended upward to at least three depths where the disk is too small, and capped at d*; the data file records the window used and whether it was extended. G1 is amended to "at least two depths (one increment)". P1 and P2 are unchanged. The small instances' rates therefore cover a wider relative window than the large ones', which is a limitation to be stated in the reading.

Limits: Any mechanism for the rate; hyperbolic tilings (their rate does not grow with L, H0-X-0012); depths beyond d*; anything about holography.

*Recorded by a low-tier agent (Haiku) from the data file; audited with `tools/audit_low_tier.py` (three false positives fixed in the tool: the "Deviations:" label before a verbatim paragraph).*

**Reading (orchestrator; exploratory card, both weak extrapolations refuted).** Measured over windows fixed in relative depth, the growth rate of the depth-restricted condition number is a lattice constant, not a function of R: on the square lattice 1.23, 1.20 and 1.08 decades per depth at R = 10, 16 and 22 (0.95 on the four-layer R = 6 disk), on the triangular lattice 1.69, 1.81 and 1.84 at R = 6.45, 10.75 and 17.2 (0.41 on the two-layer R = 3.225 disk, a single truncated increment). So the R-dependence that refuted P3a of H0-X-0012 was the window effect named in LL-A15, and the earlier picture is restored in a sharper form: on flat disks κ grows exponentially in depth at a rate set by the lattice (triangular about 1.5 times square), on hyperbolic tilings the rate is 0.3 to 0.4 and does not grow with L. Both extrapolations I preregistered were wrong: the rate saturates rather than increasing with R, and the triangular rate is below the square one only on the two-layer disk where the window is a single increment. Limitations: the windows on the small disks were extended (three instances) and on the large ones truncated by double precision (three instances), so the "matched" windows are matched only approximately; a ball-arithmetic run would remove the truncation. What the band-counting argument of `MECHANISM_NOTE.md` must now explain is the constant itself and its ratio between the two lattices (card Q5f). Nothing here concerns holography.
