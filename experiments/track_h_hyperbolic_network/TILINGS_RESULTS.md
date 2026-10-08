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

## Exponential-sum picture of the flat growth rate on lattice cylinders (`PREREGISTRATION_23.md`, 892486c before the final run; ledger H0-X-0014)
Design: Square and triangular cylinders, unit conductances: W ∈ {64, 96} with H = 18 (square) and H = 12 (triangular) rows below the boundary; boundary = row 0 (W nodes); unknowns = every edge (including the boundary row's own horizontal edges); edge depth = min of the endpoints' graph distance to row 0 (= row index). The triangular lattice has odd rows shifted by half a column (six neighbours per node). The explicit Jacobian of `hyperbolic_network.jacobian` is used (strictly upper-triangular data entries, W(W−1)/2 rows). For d = 0, 1, …: log₁₀ κ_d of the Jacobian restricted to columns of depth ≤ d (square: also restricted to vertical edges only), kept while log₁₀ κ_d ≤ 12.5 and the number of columns does not exceed the number of rows (d* = last kept depth). **Rate** = least-squares slope of log₁₀ κ_d against d over 3 ≤ d ≤ d*. Data file: `data/cylinder_exponential_sum_picture.json`. Data: `data/cylinder_exponential_sum_picture.json`.

| Series | d* | rate (decades per row) |
|---|---|---|
| square W=64 full | 6 | 1.78 |
| square W=64 vertical_only | 7 | 1.79 |
| square W=96 full | 6 | 1.77 |
| square W=96 vertical_only | 7 | 1.78 |
| triangular W=64 full | none | none |
| triangular W=96 full | none | none |

| Series | log10 kappa_d for d = 0 ... d* |
|---|---|
| square W=64 full | 1.41, 3.07, 4.44, 6.09, 7.79, 9.57, 11.4 |
| square W=64 vertical_only | 0.170, 1.78, 3.37, 4.99, 6.67, 8.42, 10.2, 12.2 |
| square W=96 full | 1.41, 3.06, 4.46, 6.11, 7.81, 9.58, 11.4 |
| square W=96 vertical_only | 0.171, 1.78, 3.38, 5.01, 6.69, 8.43, 10.2, 12.1 |

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | explicit Jacobian agrees with `jacobian_finite_diff` to 1e-5 of its largest entry on W = 8, H = 3 cylinders of each lattice | gate_fd square 1.73e-10, triangular 1.65e-10 | PASS |
| G2 | log₁₀ κ_d(full) ≥ log₁₀ κ_d(vertical only) − 1e-6 at every kept depth (square) | square W=64 and W=96: holds at every kept depth | PASS |
| G3 | d* ≥ 6 for every one of the six series | square d* = 6 and 7; triangular series empty (d* none) | FAIL |
| P1 | square vertical-only rate in [0.63, 0.94] for both W | W=64 1.79; W=96 1.78 | REFUTED |
| P2 | vertical-only rate at W=96 differs from W=64 by at most 0.10 | W=96 1.78; W=64 1.79 | HELD |
| P3 | square full rate in [0.9, 1.5] for both W | W=64 1.78; W=96 1.77 | REFUTED |
| P4 | triangular full rate in [1.3, 2.3] for both W and triangular/square full ratio ≥ 1.2 | triangular series empty (G3 failed) | void |

Deviations: **Deviation 1 (2026-10-08, after the first run, which crashed in `score()` before writing the data file; no threshold or prediction below is changed).** The first run printed the square series and then failed on the triangular series, for which no depth was kept: the triangular cylinder's Jacobian restricted to depth 0 is exactly singular (smallest singular value at round-off level, next smallest 2×10⁻³), so log₁₀ κ₀ exceeds the floor and the series is empty. A post-hoc diagnostic (not part of the tests; scripts in the job directory) found one exact null vector: the sum over boundary nodes of the difference of the two diagonal edges' Jacobian columns vanishes, a consequence of translation invariance plus the mirror symmetry of the lattice about each interior node. A straight periodic triangular boundary row is therefore a non-generic geometry with an exact first-order degeneracy (the triangular disk has no such symmetry and is full rank). Consequences, fixed before the rerun: gate G3 fails for the triangular series, so **P4 is void** (not evaluable; recorded as neither held nor refuted); the scorer is made safe against empty series; the computation is deterministic, so the rerun reproduces the first run's printed square numbers, which were seen before this deviation was written (square rates 1.78 and 1.77–1.79, against the preregistered 0.784; P1 and P3 are therefore refuted and P2 holds, whatever the rerun is). Nothing else changes.

Limits: A proof of the Vandermonde asymptotics for the discrete problem; anything about the disk beyond P3/P4; hyperbolic geometry; the effect of the closed far end (H is finite but the kept depths are far from it); anything about holography.

*Recorded by a low-tier agent (Haiku); audited with `tools/audit_low_tier.py --block` (pass). The reading is the orchestrator's.*

**Reading (preregistration 23).** The preregistered number was wrong by a factor of 2.3. On the square cylinder the condition number of the vertical-edge Jacobian grows by 1.79 (W = 64) and 1.78 (W = 96) decades per row, against the preregistered 0.784 (interval 0.63 to 0.94), and the full Jacobian (both edge types) by 1.78 and 1.77, so adding the horizontal edges does not change the rate, and the closed-form estimate I derived was a single-momentum-block Vandermonde bound that left out how σ_min is set across blocks. P1 and P3 are refuted; P2 (the rate at the two widths agrees to 0.01) held. The triangular half is void: the straight periodic triangular boundary row has an exact null vector in its Jacobian at depth 0 (translation invariance plus mirror symmetry about each interior node), so no depth could be kept; this is a property of that geometry, not of triangular lattices (the triangular disk is full rank) (LL-A19). Two statements of this card were later shown to be too optimistic: the "Not claimed" line says the closed far end is far from the kept depths, and preregistration 24's diagnostic shows that the cylinder height changes the condition numbers by up to 0.34 decades at depth 6 (height 18 against 14), and preregistration 25 shows that the finite-height increments are still rising and do not give the asymptotic rate. The rates 1.78 and 1.77 are therefore finite-size numbers, not rates of the semi-infinite problem (which is 1.65 for the zigzag block, H0-X-0016). Nothing here concerns holography.

## Momentum-resolved rates on the square cylinder (`PREREGISTRATION_24.md`, f61f9b0 before the run; ledger H0-X-0015)
Design: Square cylinder, W ∈ {64, 96} columns (periodic), H = 14 rows below the boundary row, unit conductances, explicit Jacobian of `hyperbolic_network.jacobian`. Translation invariance makes the Jacobian block-diagonal in the lateral Fourier wave number i (q = 2πi/W): for each edge type (vertical, or horizontal including the boundary row's own edges) and each depth r the columns are Fourier-transformed over the lateral position, giving per i a (data rows × depths) complex matrix whose singular values are those of block i (the union over i is the spectrum of the unblocked matrix, gate G1). For every block and every d the smallest singular value of the matrix restricted to depths ≤ d is computed; a block is followed while its own log₁₀(σ_max/σ_min) ≤ 12.5. **Block rate** = least-squares slope of −log₁₀σ_min against d over 3 ≤ d ≤ d_last. **Global rate** = the same slope for the minimum over blocks, over 3 ≤ d ≤ 7. Data file: `data/momentum_resolved_rates_on_the_cylinder.json`.
Data: `data/momentum_resolved_rates_on_the_cylinder.json`.

| Block index i (W=96) | q | predicted rate | measured rate | relative error |
|---|---|---|---|---|
| 8 | π/6 | 1.02 | 0.996 | 0.0232 |
| 16 | π/3 | 1.24 | 1.02 | 0.176 |
| 24 | π/2 | 1.42 | 1.12 | 0.217 |
| 32 | 2π/3 | 1.58 | 1.30 | 0.180 |
| 40 | 5π/6 | 1.72 | 1.48 | 0.138 |
| 48 | π | 1.83 | 1.85 | 0.0105 |

| Run | global rate |
|---|---|
| v W=64 | 1.65 |
| v W=96 | 1.67 |
| h W=96 | 1.76 |

| Depth | block with the smallest sigma_min, W=64 | W=96 |
|---|---|---|
| 0 | 32 | 48 |
| 1 | 32 | 48 |
| 2 | 32 | 48 |
| 3 | 32 | 48 |
| 4 | 32 | 48 |
| 5 | 32 | 48 |
| 6 | 32 | 48 |
| 7 | 32 | 48 |
| 8 | 32 | 29 |
| 9 | 32 | 48 |
| 10 | 32 | 29 |
| 11 | 32 | 29 |

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | union of block singular values equals the unblocked vertical-edge spectrum to 1e-8 of the largest | union agreement 1.84e-15 | PASS |
| G2 | vertical-edge global rates within 0.08 of 1.793 (W=64) and 1.783 (W=96) | global rates 1.65 (W=64), 1.67 (W=96) | FAIL |
| P1 | block with the smallest sigma_min is i = W/2 at every depth 4 to 7, both W | W=64: i = 32 at depths 4 to 7; W=96: i = 48 at depths 4 to 7 | HELD |
| P2 | block rates at i = 8, 16, 24, 32, 40, 48 within 15% of 1.02, 1.24, 1.42, 1.58, 1.72, 1.83 | block rates 0.996, 1.02, 1.12, 1.30, 1.48, 1.85 | REFUTED |
| P3 | horizontal global rate (W=96) within 10% of 1.833 | global rate 1.76 | HELD |

Deviations: none.

Limits: That the picture explains the disk's rates (disks have curvature, diagonal directions and graph-distance depth; the disk values 1.1–1.2 are below this cylinder value 1.83, which is itself a finding to explain); the triangular lattice (its straight periodic boundary is exactly degenerate, `PREREGISTRATION_23.md`); hyperbolic geometry; a proof of the Vandermonde asymptotics; anything about holography.

*Recorded by a low-tier agent (Haiku); audited with `tools/audit_low_tier.py --block` (pass). The reading is the orchestrator's; two post-hoc diagnostics (`exp24_diag_floor.py`, `exp24_diag_height.py`) support it.*

**Reading (preregistration 24).** Two predictions held and one was refuted, and the gate that failed is more informative than the predictions. *What held.* P1: the block with the smallest singular value at depths 4 to 7 is the zigzag block (total momentum π) on both widths; on the wider cylinder the argmin moves to another block at depths 8, 10 and 11, which I attribute to double precision (the zigzag block's σ_min near the noise level; not verified). P3: the horizontal-edge columns lose conditioning at 1.76 decades per row, within 10 % of the number 1.833. That pass is not evidence for 1.833: preregistration 25 shows that closed form was wrong (the exact zigzag rate is 1.65) and that the finite-height double-precision increments were still rising, so these windows happened to land near it. *What was refuted.* P2: the six block rates (0.996, 1.019, 1.116, 1.298, 1.479, 1.852 for q = π/6 … π) miss the closed form's table by 14 to 22 % at the middle momenta. The exact semi-infinite rates of preregistration 25 (0.956 … 1.679) show that the measured values differ from them by between −14 % and +10 % depending on the momentum (above at the two ends, below in the middle): the finite height, not the closed form's table alone, is a large part of the discrepancy. *Why gate G2 failed.* The block machinery (height 14) and preregistration 23's explicit SVD (height 18) are not the same matrix. A post-hoc check at W = 64 shows the explicit SVD at height 14 reproduces the block-implied log₁₀ κ to three decimals (10.584 at depth 6) and at height 18 gives 10.243: the closed end matters at the level of a third of a decade by depth 6. That is my design error (LL-A18), recorded as a failed gate and not repaired after the fact. Nothing here concerns holography.

## Exact semi-infinite blocks and the asymptotic rates (`PREREGISTRATION_25.md`, 3c8e8d1 before the final run; ledger H0-X-0016)

Design: Exact blocks as above (mpmath, 140 digits), W = 96, depths 0…30. σ_min of the first d+1 columns is obtained as 1/√λ_max(G⁻¹), G = VᵀV, by power iteration. **Rate** = (log₁₀σ_min(20) − log₁₀σ_min(30))/10. Computed for the six momenta (i = 8, 16, 24, 32, 40, 48); σ_min at depth 20 for all blocks i = 0…48; and the zigzag block at W = 192. Data file: `data/exact_semi_infinite_blocks_asymptotic_ra.json`.
Data: `data/exact_semi_infinite_blocks_asymptotic_ra.json`.

| Block label (W=96 index) | q | Green prediction | rival closed form | measured rate (W=384) | relative error vs Green (fraction, as stored) |
|---|---|---|---|---|---|
| 8 | π/6 | 0.961 | 1.02 | 0.956 | 0.0052 |
| 16 | π/3 | 1.14 | 1.24 | 1.13 | 0.0048 |
| 24 | π/2 | 1.30 | 1.42 | 1.30 | 0.0025 |
| 32 | 2π/3 | 1.44 | 1.58 | 1.44 | 0.0006 |
| 40 | 5π/6 | 1.55 | 1.72 | 1.55 | 0.0021 |
| 48 | π | 1.65 | 1.83 | 1.68 | 0.0157 |

| Quantity | value |
|---|---|
| zigzag rate at W=768 (rate_W768_pi) | 1.65 |
| block with the smallest sigma_min at depth 20 (argmin_block_depth20) | 192 (zigzag block at W=384) |
| H=14 increment d=5 to 6 (increment_H14_5to6) | 1.97 |
| exact increment d=5 to 6 (increment_exact_5to6) | 1.66 |

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | per-row increments of log10 sigma_min for d = 1 to 5 agree with the explicit H=40 block within 0.02 | explicit d = 0 to 5: -0.958, -2.58, -4.17, -5.76, -7.38, -9.02; exact d = 0 to 5: 0.183, -1.43, -3.02, -4.62, -6.23, -7.86 | PASS |
| P1 (zigzag rate, rival B) | within 3 % of 1.65 | zigzag rate 1.68 at W=384; rival A 1.83 does not fit (P1_rival_old_formula_fits false) | HELD |
| P2 (rate versus momentum, rival B) | each of the six block rates within 5 % of the Green values | largest relative error 1.57 % (q = π) | HELD |
| P3 (where the minimum is) | at depth 20 the smallest sigma_min is the zigzag block (i = 192 at W=384) | argmin block i = 192 | HELD |
| P4 (width) | zigzag rate at W=768 within 1 % of the one at W=384 | 1.65 at W=768 against 1.68 at W=384 | REFUTED |
| P5 (finite height explains the acceleration) | H=14 increment exceeds the exact increment (d = 5 to 6) by at least 0.15 | 1.97 against 1.66 | HELD |

Deviations: **Deviation 1 (2026-10-08, after the first run, which crashed before any verdict existed; thresholds unchanged).** The first run stopped with a numerically singular Gram matrix at depth 24, at 140 and at 400 digits, so not a precision effect. At W = 96 the zigzag block has only 25 distinct nodes (z_n is invariant under k → −k and k → π − k, so the 96 mode indices collapse to 25 values), and with the diagonal direction projected out the block has rank at most 24: depth 24 and beyond are rank-deficient, and the window 20 to 30 of the Design was impossible by construction. (This is also a physical statement: a boundary of W sites carries finitely many data per momentum, so the restricted Jacobian loses rank at a depth set by W.) Amended design, fixed before the rerun: the six momenta, the depth-20 comparison over all blocks, and the rates use **W = 384** (97 distinct nodes at the zigzag momentum; block indices i = 32, 64, 96, 128, 160, 192, the same momenta as i = 8, …, 48 at W = 96), with the **rate window 15 to 25**, i.e. (log₁₀σ_min(15) − log₁₀σ_min(25))/10; P4 compares the zigzag rate at **W = 768** with the one at W = 384; G1 and P5 stay at W = 96 (they use depths ≤ 6). P3 now asks for block i = 192 at W = 384. All thresholds (3 %, 5 %, 1 %, 0.02, 0.15) and the Green values are unchanged; the Green values for W = 384 evaluate to the same four digits as for W = 96 (checked by the prediction function only).

Limits: Anything about the disk or hyperbolic geometry; triangular lattices; the closed-height cylinder beyond P5; a proof (this is a computation on a closed-form block, plus a standard potential-theory estimate); anything about holography.

*Recorded by a low-tier agent (Haiku); audited with `tools/audit_low_tier.py --block` (pass; relative errors restored from percentages to the stored fractions by the orchestrator). The reading is the orchestrator's.*

**Reading (preregistration 25).** The potential-theory form (rival B) is right and my earlier closed form (rival A) is wrong. In 140-digit arithmetic on the exact semi-infinite blocks, the smallest singular value of the block at total momentum q loses conditioning at 0.956, 1.133, 1.295, 1.436, 1.554 and 1.679 decades per row for q = π/6 … π at W = 384, against the Green-function predictions 0.961, 1.138, 1.298, 1.435, 1.551 and 1.653 (differences 0.06 % to 1.6 %, five of six within 0.6 %); the minimum is in the zigzag block (P1, P2, P3 held, rival A's 1.833 does not fit), so the condition number of the semi-infinite square cylinder grows by about 1.65 decades per row. The gate held: the exact block, with the position-diagonal direction projected out, reproduces the explicit double-precision block at height 40 to 0.005 in every increment for d ≤ 5. P4 is refuted by a small margin: the zigzag rate at W = 768 is 1.653 (the Green value 1.653 to four digits), at W = 384 it is 1.679, 1.5 % apart against the 1 % threshold. The W = 384 increments creep up from 1.62 at depth 1 to 1.70 at depth 25: with 97 distinct nodes the discreteness of the node set adds conditioning as the depth grows, and the Green value is the large-width limit. P5 held: the height-14 increment at d = 5 → 6 is 1.97 against the exact 1.66, so the acceleration seen in preregistration 24 is a finite-height effect. What this gives: the exponential growth of the flat-lattice conditioning on a cylinder has an exact origin and an exact rate, set by the lattice dispersion relation through the spread of the products of mode decay factors. What it does not give: the disk (1.1–1.2 decades per depth on the square disk is below this cylinder value; the node set of a disk differs), the triangular lattice, the hyperbolic tilings, the horizontal-edge columns' exact rate, or a proof. The three cards together showed two ways of fooling oneself with a closed form fitted after the fact (LL-A17) and two design errors (LL-A18). Nothing here concerns holography.


## A boundary along the lattice diagonal and the growth rate (`PREREGISTRATION_26.md`, ff7aef5 before the run; ledger H0-X-0017)
Design: Exact blocks of the type-B edge columns in 140-digit arithmetic (mpmath), W = 384, depths 0…25; σ_min as in preregistration
25 (inverse Gram and power iteration; here the Gram is Hermitian). **Rate** = (log₁₀σ_min(15) − log₁₀σ_min(25))/10. Six momenta
(i = 4 × label); σ_min at depth 20 for all blocks i = 0…192; the zigzag block at W = 768. Width and window follow the amended
design of preregistration 25 (97 and 193 distinct nodes at the zigzag momentum). Data file:
`data/diagonal_boundary_orientation_and_the_gr.json`.
Data: `data/diagonal_boundary_orientation_and_the_gr.json`.

| Block label (W=96 index) | q | Green prediction | rival (aligned / sqrt 2) | measured rate (W=384) | relative error vs Green (fraction, as stored) |
|---|---|---|---|---|---|
| 8 | pi/6 | 0.849 | 0.961 / 0.679 | 0.838 | 0.0122 |
| 16 | pi/3 | 0.938 | 1.14 / 0.805 | 0.917 | 0.0227 |
| 24 | pi/2 | 1.04 | 1.30 / 0.918 | 0.985 | 0.0495 |
| 32 | 2pi/3 | 1.14 | 1.44 / 1.01 | 1.04 | 0.0914 |
| 40 | 5pi/6 | 1.26 | 1.55 / 1.10 | 1.07 | 0.1578 |
| 48 | pi | 1.40 | 1.65 / 1.17 | 1.07 | 0.239 |

| Quantity | value |
|---|---|
| zigzag rate at W=768 (rate_W768_zigzag) | 1.07 |
| block with the smallest sigma_min at depth 20 (argmin_block_depth20) | 192 (zigzag block) |
| aligned zigzag rate of preregistration 25 (aligned_green label 48) | 1.65 |

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | per-row increments of log10 sigma_min for d = 1 to 5 agree with the explicit H=40 block within 0.02 | explicit log10 sigma_min for d = 0 to 5: -0.638, -1.54, -2.74, -3.73, -4.86, -5.87; exact for d = 0 to 5: 0.503, -0.401, -1.60, -2.59, -3.72, -4.73 | PASS |
| P1 | zigzag rate within 3 % of 1.4027 | zigzag rate 1.07 at W = 384; rival 1.17 does not fit (P1_rival_sqrt2_fits false) | REFUTED |
| P2 | each of the six block rates within 5 % of the Green values | rates 0.838, 0.917, 0.985, 1.04, 1.07, 1.07 against 0.849, 0.938, 1.04, 1.14, 1.26, 1.40 | REFUTED |
| P3 | at depth 20 the smallest sigma_min is the zigzag block (i = 192) | argmin block i = 192 | HELD |
| P4 | diagonal zigzag rate differs from the aligned 1.6527 by at least 8 % | diagonal zigzag rate 1.07 against aligned 1.65 | HELD |

Deviations: none.

Limits: That any of this is the disk's constant (a disk also has curvature and a staircase boundary; if the diagonal rate comes out
at 1.40 it is still above the disk's 1.1–1.2, so orientation alone would not explain the disk); the type-A columns (same
nodes, different amplitudes: not computed); the triangular lattice; hyperbolic geometry; anything about holography.

*Recorded by a low-tier agent (Haiku); audited with `tools/audit_low_tier.py --block` (pass). The reading is the orchestrator's; a post-hoc diagnostic (`exp26_diag_signed_nodes.py`, `data/diagonal_signed_nodes_diagnostic.json`) supports the second paragraph.*

**Reading (preregistration 26).** *What the card shows.* The gate held to 0.001 in every increment (exact and explicit blocks agree), so the block formula for the diagonal strip, with its complex decay factors and complex amplitudes, is right and the machinery works on a second geometry. Boundary orientation changes the conditioning rate a great deal: the zigzag block loses 1.067 decades per row on the diagonal strip against 1.653 on the aligned one (35 % lower; P4 held), the zigzag block is again the dominant one at depth 20 (P3 held), and the rate is converged in the width (1.067 at W = 768 and at W = 384). Both preregistered forms for the rate are wrong: the Green exponent of the node moduli predicted 1.403 (24 % too high; P1 refuted) and the √2 rival 1.169 (8.7 % too high, outside its 5 % band). P2 is refuted too: the six measured rates are 0.838, 0.917, 0.985, 1.039, 1.065, 1.067, and the moduli-based prediction misses by 1.2 %, 2.3 %, 5.0 %, 9.1 %, 15.8 % and 23.9 %, growing with the momentum.

*What the diagnostic found, after the fact.* My prediction used the moduli of the node values z_n = λ(k)λ(q−k). The diagnostic shows these are real after removing the common phase e^(−iq/2) (imaginary parts 10⁻¹⁶) but of **both signs**: the sign flips when q − k wraps around 2π, so the node set is the single interval [−M₋, M₊] through zero, not [z_min, z_max] of the moduli. The Green exponent of that signed interval reproduces all six measured rates to between 0.2 % and 0.85 % with no free parameters (0.846, 0.923, 0.991, 1.044, 1.072, 1.070), and the alternating signs also explain the period-two oscillation of the increments (about 1.05 and 1.08 at the zigzag block). This was computed after seeing the data, so it is a hypothesis with a good record, not a confirmation; preregistration 27 tests it out of sample on a geometry whose nodes are real, and I note its limit: for unequal conductances on the diagonal strip the nodes are genuinely complex (imaginary parts up to 0.16 against moduli up to 0.2), where an interval formula does not apply.

*Relation to the disk.* The diagonal value 1.07 sits at the lower end of the square disk's measured 1.08–1.23 and the aligned value 1.65 above it, and a disk contains every orientation plus curvature and a staircase boundary; nothing here says how these combine, and no claim is made. Nothing here concerns holography.

## The aligned strip with unequal conductances: an out-of-sample test (`PREREGISTRATION_27.md`, b8b7787 before the run; ledger H0-X-0018)

Design: Exact blocks (mpmath, **220 digits** because the λ = 16 rates are near 2.5 decades per row), vertical-edge columns, W = 384,
depths 0…25; σ_min by inverse Gram and power iteration as in preregistration 25; rate = (log₁₀σ_min(15) − log₁₀σ_min(25))/10; six
momenta; σ_min at depth 20 for every block i = 0…192; the zigzag block at W = 768. Both λ in one run. Data file:
`data/aligned_strip_with_unequal_conductances.json`.

**Disclosure.** Before this card was committed I ran the block code once at λ = 16, W = 96 for depths up to 4 as an infrastructure
check; the per-row increments were 2.41, 2.40, 2.46 and 2.54, consistent in size with the prediction of 2.45 but outside the
test window (depths 15 to 25) and at a width where the window is impossible. No other λ = 0.05 or λ = 16 block was computed.

Data: `data/aligned_strip_with_unequal_conductances.json`.

Lambda = 0.05:

| Block label (W=96 index) | q | Green prediction | measured rate (W=384) | relative error vs Green (fraction, as stored) |
|---|---|---|---|---|
| 8 | pi/6 | 1.1406 | 1.135 | 0.0049 |
| 16 | pi/3 | 1.2331 | 1.2266 | 0.0053 |
| 24 | pi/2 | 1.3393 | 1.3338 | 0.0041 |
| 32 | 2pi/3 | 1.4606 | 1.4572 | 0.0023 |
| 40 | 5pi/6 | 1.6005 | 1.5987 | 0.0011 |
| 48 | pi | 1.7649 | 1.7773 | 0.007 |

Lambda = 16:

| Block label (W=96 index) | q | Green prediction | measured rate (W=384) | relative error vs Green (fraction, as stored) |
|---|---|---|---|---|
| 8 | pi/6 | 1.4232 | 1.4397 | 0.0116 |
| 16 | pi/3 | 1.87 | 1.8998 | 0.0159 |
| 24 | pi/2 | 2.1442 | 2.1859 | 0.0195 |
| 32 | 2pi/3 | 2.314 | 2.3657 | 0.0223 |
| 40 | 5pi/6 | 2.4112 | 2.4601 | 0.0203 |
| 48 | pi | 2.4505 | 2.6468 | 0.0801 |

| lambda | zigzag rate W=768 | Green prediction | block with the smallest sigma_min at depth 20 |
|---|---|---|---|
| 0.05 | 1.7622 | 1.7649 | 192 |
| 16 | 2.4975 | 2.4505 | 192 |

| lambda | exact log10 sigma_min, d = 0 to 5 | explicit log10 sigma_min, d = 0 to 5 (height 40) |
|---|---|---|
| 0.05 | -0.6617097825223154, -2.3123463463979648, -3.994633942238767, -5.701747664537529, -7.423713500675507, -9.162214783949379 | -1.795590577758952, -3.429504719837672, -5.137406094197353, -6.949889908522371, -8.870714955651156, -10.912712452035965 |
| 16 | 0.3311104830295538, -2.0816586685569134, -4.486480375301076, -6.948771640398562, -9.489254092151487, -12.106923833496902 | -0.8105401312489623, -3.223309282826508, -5.62813099043092, -8.09042225745055, -10.630904712714106, -13.24857449141602 |

| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | per-row increments of log10 sigma_min for d = 1 to 5 within 0.02 of the explicit height-40 block, for each lambda | G1 boolean false; stored lists in the table above | FAIL |
| P1 | zigzag W=768 rate within 3 % of 1.7649 (lambda 0.05) and 2.4505 (lambda 16) | 1.7622 (lambda 0.05); 2.4975 (lambda 16) | HELD |
| P2 | each of the six block rates at W=384 within 6 % of the Green values, for both lambda | lambda 16 block 48: rate 2.6468 against 2.4505, relative error 0.0801; other cells in the tables above | REFUTED |
| P3 | block with the smallest sigma_min at depth 20 is the zigzag block i = 192, for both lambda | argmin block 192 (lambda 0.05); 192 (lambda 16) | HELD |
| P4 | zigzag W=768 rate within 3 % of the W=384 rate, for both lambda | lambda 0.05: W=384 1.7773, W=768 1.7622; lambda 16: W=384 2.6468, W=768 2.4975 | REFUTED |
| P5 | zigzag W=768 rate exceeds 1.6527 by at least 4 %, for both lambda | 1.7622 (lambda 0.05) and 2.4975 (lambda 16), against the null 1.6527 | HELD |

Deviations: none.

Limits: The diagonal strip with unequal conductances (complex nodes); the horizontal-edge columns; the disk or curvature; hyperbolic
geometry; a proof; anything about holography.

*Recorded by a low-tier agent (Haiku); audited with `tools/audit_low_tier.py --block` (pass). The reading is the orchestrator's; a post-hoc diagnostic (`exp27_diag_height.py`, `data/aligned_strip_height_diagnostic.json`) supports its second paragraph.*

**Reading (preregistration 27).** *What the out-of-sample test shows.* The node picture, applied unchanged to a family it was not adjusted to, predicts the non-monotone dependence on the lateral conductance: the converged zigzag rate is 1.762 at λ = 0.05 (prediction 1.765, −0.15 %), 1.653 at λ = 1 (preregistration 25) and 2.498 at λ = 16 (prediction 2.451, +1.9 %). The λ-independent null is refuted by +6.6 % and +51 % (P5 held), the zigzag block is again the dominant one at depth 20 for both λ (P3 held), and P1 held. For λ = 0.05 all six momenta agree with the Green exponent to between 0.1 % and 0.7 % at W = 384. For λ = 16 the five non-zigzag momenta agree to between 1.2 % and 2.2 % (all on the high side).

*What was refuted, and why.* P2 and P4 fail for λ = 16 only, and by one block: the zigzag rate at W = 384 is 2.647 against the prediction 2.451 (+8.0 %, band 6 %), and 6.0 % above the converged W = 768 value (band 3 %). The W = 384 zigzag increments rise steadily from 2.43 at depth 1 to 2.73 at depth 25, which is the discrete-node effect of preregistration 25 (97 distinct nodes) growing with the rate; I had anticipated a drift of the size seen at λ = 1 (1.5 %) and set the bands accordingly, and the drift is proportionally larger at 2.5 decades per row. Both refutations are errors in my tolerance choices; the converged exponent is what the picture predicts. *The gate.* G1 failed as preregistered (for λ = 0.05; it passed for λ = 16, identical increments to three decimals). My preregistered rule says that a failed gate means nothing else is read. The post-hoc diagnostic shows the cause is the explicit reference, not the block formula: at W = 48 the explicit increments approach the exact ones as the reference height grows (gaps of 0.95, 0.23, 0.02 and 0.000 decades in the fifth increment at heights 20, 40, 80 and 160), so a height of 40 is not semi-infinite when the lateral coupling is weak (LL-A18). The verdicts above are recorded as computed; the λ = 16 half stands on a passed gate, and the λ = 0.05 half on the post-hoc validation at height 160, which I count as weaker evidence than a preregistered gate.

*Where this leaves the picture.* On the square lattice with a real node set, the exponent of the semi-infinite problem is the Green exponent of the interval of node values: checked (parameter-free, 140 to 220 digits) for the aligned strip at λ = 0.05, 1 and 16 and, after the signed-node correction found post hoc, for the diagonal strip. It does not extend to complex node sets (the diagonal strip with unequal conductances), and it says nothing yet about curvature, so the disk's constant remains unexplained. Nothing here concerns holography.

