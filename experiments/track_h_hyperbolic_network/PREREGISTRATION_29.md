# Preregistration 29: do transient (Laplace-resolved) measurements slow the exponential depth growth of the Jacobian condition number? (task Q15)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2 and the garage protocol. **Why:** the garage board is read with a scope, so the data are
transients, not only the DC response matrix that every earlier preregistration used. A step response sampled at many times carries the DtN map at
many Laplace variables s. If those add information about deep edges, the exponential growth of κ(J_d) found at s = 0 would be pessimistic for what the
board can measure. This card asks that, and uses rusty-SUNDIALS (CVODE) to check the time-to-frequency link on which the claim rests.

## Model (fixed now)
Resistor network with conductance 1 on every edge and capacitance 1 from every interior node to ground; boundary nodes driven. For real s ≥ 0 the
response matrix is Λ(s) = L_bb − L_bi (L_ii + sI)⁻¹ L_ib. By the same envelope argument as at s = 0 (bilinear form, symmetric matrices),
∂Λ(s)/∂g_e = d_e(s) d_e(s)ᵀ with d_e(s) = H(s)[a] − H(s)[b], H(s)[interior] = −(L_ii + sI)⁻¹ L_ib, H[boundary] = I. The stacked Jacobian for a set S of
Laplace variables is the vertical concatenation of the strictly-upper-triangular Jacobians J(s), s ∈ S; J_d(S) keeps the columns of depth ≤ d. We use real s only,
so everything is real; a step response sampled at times t gives Î(s)/V̂(s) = Λ(s) at real s by Laplace transform.
Two sets: S2 = {0, 0.3} and S5 = {0, 0.1, 0.3, 1, 3}. DC is S1 = {0}.

## Exact consequence (not a prediction)
J_d(S)ᵀJ_d(S) = Σ_s J_d(s)ᵀJ_d(s) ≥ J_d(0)ᵀJ_d(0), so σ_min(J_d(S)) ≥ σ_min(J_d(0)) for every d: adding Laplace variables can only raise the smallest
singular value. κ also involves σ_max, which grows too, so the effect on κ is the open question.

## No run before this commit
No Jacobian with s > 0 has been computed. The DC baseline on the square disk (about 1.1–1.2 decades per graph step, H0-X-0013) is from earlier work.

## Design
Square disk of radius 16 (`build_square_disk(16)`), double precision, SVD of the stacked column-restricted matrix. Window: d = 3…7, using only those d for
which log₁₀κ at S1 is at most 9 (double-precision floor). Slope σ(S) is the least-squares slope of log₁₀κ(J_d(S)) against d over the window.
Also the {7,3} tiling with 4 layers (all depths). Data: `data/laplace_resolved_jacobian_conditioning.json`.

## Validity gates
- G1 (CVODE link). On the square disk of radius 4, for the step V_b = e_j at the first boundary node, integrate the interior ODE
  dv/dt = −(L_ii v + L_ib e_j) with rusty-SUNDIALS CVODE (BDF, rtol 1e-10, atol 1e-12) to T = 40/λ_min(L_ii) at 4001 output times; the boundary current
  I(t) = L_bb e_j + L_bi v(t). The Laplace transform ∫₀ᵀ I(t) e^{−st} dt (Simpson) must equal Λ(s)e_j/s within 1e-5 relative (max norm) for s = 0.1, 0.3, 1.
  A backend that cannot be imported is NOT RUN, never passed.
- G2 (exact consequence). σ_min(J_d(S5)) ≥ σ_min(J_d(S1)) within roundoff for every d in the window.
- G3 (DC baseline). The S1 slope on the window is between 0.9 and 1.3 decades per step.

## Predictions (fixed now, before the run)
Reasoning: in the strip picture the nodes of column d are products of per-row decay factors, and for s > 0 the factors shrink, so the s > 0 rows add
equations (more distinct nodes) whose deep-edge content is smaller than at s = 0. I expect a modest gain, not removal.
- **P1 (still exponential).** The S5 slope is at least 0.5 times the S1 slope.
- **P2 (some gain or none, not a loss).** The S5 slope is at most 1.0 times the S1 slope.
- **P3 (diminishing returns).** |σ(S5) − σ(S2)| < 0.15 decades per step.
- **P4 (hyperbolic).** On {7,3} with 4 layers, log₁₀κ(J(S5)) at the deepest depth is within 1.0 of log₁₀κ(J(S1)) in absolute value (no new blow-up and no collapse).

## What a refutation would mean (written now)
P1 refuted (S5 slope below half): transients carry much more deep-edge information than DC and the garage can expect a flatter conditioning curve than
the preprint predicts. P2 refuted (S5 slope above DC): extra rows inflate σ_max faster than σ_min and κ is the wrong summary for stacked data (report σ_min).
P3 refuted: the gain is not saturating in the number of Laplace variables. P4 refuted: the hyperbolic comparison changes with transient data.
G1 failed: the time-to-frequency link does not hold for the integrator as configured, and nothing above would be read as a statement about transients.

## Not claimed
That any of this applies to noisy data (this is conditioning in double precision, not recoverability with noise); complex s (real s only); the strip rate
with s > 0 (no closed form here); that κ of a stacked matrix is the right figure of merit; holography; any statement about the hardware beyond conditioning of the model.

## Deviation 1 (2026-10-08, written after G1 of the first run failed and before any rerun)
G1 as written **failed**: the Laplace transform of the CVODE current differs from Λ(s)e_j/s by 1.6e-3 at s = 0.1 (gate 1e-5), and by 3.9e-9 and 3.8e-10 at
s = 0.3 and 1. This is a design error of mine, not an integrator failure: with the step held, the boundary current tends to the steady value Λ(0)e_j, not to zero,
so truncating the transform at T = 40/λ_min leaves a tail I(T)e^{−sT}/s that is 1.6e-3 of the integral at s = 0.1 (e^{−sT} with sT = 6.45). The window T was set
from the interior relaxation time only. Variant **G1′**, labelled post hoc: add the tail from the integrator's own final current, I(T)e^{−sT}/s, to the Simpson
sum, tolerance unchanged at 1e-5, same three s. G1 as written stays recorded as failed. The stacked-Jacobian predictions P1–P4 do not use the integrator;
they are reported with the G1 status stated beside them, and the statement that the time-to-frequency link holds rests on G1′ only, which is post hoc.
Script for G1′: `exp29_diag_g1_tail.py`, data `data/laplace_link_tail_corrected.json`.
