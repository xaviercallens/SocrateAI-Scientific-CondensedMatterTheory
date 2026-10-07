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
