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
