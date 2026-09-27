# Conditioning of the boundary-to-bulk inverse conductance problem on hyperbolic lattices

**Status: DRAFT. Not submitted anywhere.** Written as a first, working
manuscript draft — content and claims are ready for the author's review,
not for a journal or preprint server. Submission is the author's decision.

**Author:** Xavier Callens.
**AI-assistance disclosure (for arXiv / journal policy compliance):** the
code, numerical experiments, and this manuscript draft were developed with
the assistance of Claude (Anthropic) as a research and coding assistant.
All scientific claims, results, and conclusions were reviewed against
their evidence and are the author's responsibility. Two measurement bugs
in this work's own pipeline were found and corrected during drafting (see
§5); this disclosure and that correction history are left in the record
rather than smoothed over.

---

## Abstract

We study the inverse problem of recovering interior edge conductances of a
resistor network from boundary voltage/current measurements — the discrete
analogue of electrical impedance tomography (EIT) — on layer-truncated
hyperbolic $\{7,3\}$ tilings, compared to matched Euclidean square and
triangular lattice disks. Using an exact (non-finite-difference)
computation of the Dirichlet-to-Neumann map's sensitivity Jacobian via the
harmonic-extension identity, we show that the problem's condition number
grows only polynomially with the number of nodes $N$ on the hyperbolic
lattice — because the maximal graph distance from any node to the boundary
grows only as $O(\log N)$ — while on Euclidean lattices, where boundary
depth grows as $O(\sqrt N)$, the condition number becomes numerically
unrepresentable in IEEE double precision by $N\sim 10^3$. A preregistered
confirmatory measurement at $N=847$ matches the prediction exactly (depth
$7$, predicted; condition number within the predicted band). Separately,
using exact modular-arithmetic rank certification (no floating point), we
show that both lattice families remain algebraically full-rank at these
sizes: the phenomenon is one of numerical conditioning, not structural
identifiability. We report this distinction, and the two measurement bugs
in our own pipeline that obscured it before correction, as part of the
result.

---

## 1. Introduction

The bulk-boundary correspondence — that data measured only on the boundary
of a system can determine, or fail to determine, properties of its
interior — is a unifying theme across condensed matter topology (Kane &
Mele, 2005 [`cond-mat/0506581`]; Hasan & Kane, 2010 [`1002.3895`]) and
holographic duality (Maldacena, 1997 [`hep-th/9711200`]; Ryu & Takayanagi,
2006 [`hep-th/0603001`]). A tabletop, purely classical instance of the same
question is the inverse conductivity (Calderón) problem: given boundary
voltage-to-current data on a resistor network, can the interior
conductances be recovered, and how sensitive is that recovery to
measurement noise?

Two facts motivate this work. First, hyperbolic lattices — regular
tessellations of negatively-curved space — have been realised physically
in superconducting circuit QED (Kollár, Fitzpatrick & Houck, 2019
[`1802.09549`]) and on ordinary electrical circuit boards (Lenggenhager
*et al.*, 2022 [`2109.01148`]), and are an active platform for tabletop
studies of discrete holography (Asaduzzaman, Catterall, Hubisz & Nelson,
2020 [`2005.12726`]; Basteiro, Di Giulio, Erdmenger & Karl, 2022
[`2205.05693`]). Second, the resistor-network EIT literature independently
documents that reconstruction on flat lattices becomes unstable as network
size grows (Borcea, Druskin, Guevara Vasquez & Mamonov, 2011
[`1107.0343`]), consistent with logarithmic stability bounds for the
continuum and discrete Calderón problem (Ervedoza & de Gournay, 2011
[`1104.4858`], for $d\ge3$).

This work asks a specific, quantitative question these do not directly
answer: **how does the depth-dependent instability of the inverse
conductance problem interact with the *curvature* of the underlying
lattice** — specifically, does the logarithmic (rather than square-root)
growth of boundary depth with $N$ on a hyperbolic lattice translate into
qualitatively better-conditioned reconstruction at large $N$?

## 2. Setup

### 2.1 Lattices

We construct layer-truncated hyperbolic $\{7,3\}$ tilings (heptagons, 3 per
vertex) in the Poincaré disk by reflecting the central tile across its
geodesic edges, breadth-first by tile layer $L$, and compare against
Euclidean square and triangular lattice disks of matched node count $N$.
Every graph's faces are constructed explicitly (not inferred from vertex
degree alone), because a vertex of full degree can still lie on the
boundary — a "rim junction" on the hyperbolic tiling, or a notch vertex on
a disk cut from a Euclidean lattice both have full degree while touching
the outer face; classifying boundary by face incidence, verified against
the Euler characteristic $V-E+F=1$ for every instance tested, is required
to get this right.

### 2.2 The Dirichlet-to-Neumann map and its Jacobian

With unit edge conductances $g_e=1$, the graph Laplacian is
$L=\sum_e g_e L_e$, $L_e=(\delta_a-\delta_b)(\delta_a-\delta_b)^\top$ for
$e=(a,b)$. Partitioning nodes into boundary $\partial G$ and interior, the
Dirichlet-to-Neumann map is the Schur complement
$\Lambda = L_{bb} - L_{bi}L_{ii}^{-1}L_{ib}$. Writing $H$ for the harmonic
extension operator ($H|_{\partial G}=I$,
$H|_{\text{int}}=-L_{ii}^{-1}L_{ib}$), so that $\Lambda = H^\top L H$, an
envelope-theorem argument (the harmonic extension is the energy minimiser
for fixed boundary data, so its own variation with $g_e$ contributes
nothing to first order) gives the exact Jacobian
$$\partial\Lambda/\partial g_e = (P_a-P_b)^\top(P_a-P_b), \qquad P_v = H
\text{'s row for vertex } v,$$
computed with a single linear solve for the whole graph — not one solve
per edge, and not subject to a finite-difference step-size floor. This
identity was cross-checked against a central-difference Jacobian
(agreement to $1.15\times10^{-11}$) before being used for any reported
result.

## 3. Preregistration and results

An initial derivation predicting *exponential* per-edge sensitivity decay
on flat lattices, by direct analogy to continuum Calderón-problem
instability, did not survive scrutiny (the relevant Poisson-kernel
integral gives polynomial, not exponential, decay). Rather than lock a
prediction built on a flawed derivation, an unlocked exploratory pass was
run first (layers $L=1$–$3$) to determine the actual mechanism, then a
genuinely new data point ($L=4$, not previously computed) was
preregistered with a numeric prediction before being measured.

**Preregistered result.** At $L=4$: predicted depth $7$, measured $7$
(exact); predicted $N\in[800,900]$, measured $N=847$; predicted
$\log_{10}\kappa = 4.2\pm0.5$, measured $3.89$ (within band).

**Headline comparison, at matched $N$.** At $N\approx315$–$317$ (the
largest size at which condition numbers remain finite in double precision
on both families): $\log_{10}\kappa = 3.27$ (hyperbolic) vs. $9.72$
(square) — a $6.4$-decade gap. At $N\approx800$–$850$: the hyperbolic
lattice remains measurable ($\log_{10}\kappa=3.89$) while the flat
lattices' Jacobians are **numerically singular** in double precision
(smallest singular value at or below the machine-precision floor relative
to the largest) — an even larger effective separation, though not
expressible as a finite decade count.

**Mechanism.** In both geometries, $\log_{10}\kappa$ grows locally
linearly with maximal boundary depth ($\approx0.47$/layer for $\{7,3\}$,
$\approx1.14$/layer for the square lattice) — exponential decay of
information with depth is common to both. What differs is how depth
itself scales with $N$: $O(\log N)$ (hyperbolic, verified: boundary node
counts $28,77,203,532$ at $L=1$–$4$ satisfy the linear recurrence
$b_{n+2}=3b_{n+1}-b_n$ exactly, giving geometric per-layer growth) versus
$O(\sqrt N)$ (Euclidean, by elementary disk-area scaling).

## 4. What this is not: an exact-rank check

The condition-number results above are floating-point measurements. To
determine whether the growing ill-conditioning on Euclidean lattices
reflects a genuine loss of algebraic rank or is purely a precision
artefact, we separately certified the exact rank of the same Jacobian
construction using modular arithmetic: since edge conductances are
integers, the Laplacian and (for a prime $p$ with $\det(L_{ii})\not\equiv
0\pmod p$) the Jacobian are $p$-integral, and
$\mathrm{rank}_{\mathbb Q}(J) \ge \mathrm{rank}_{\mathbb F_p}(J\bmod p)$: a
full-rank result modulo $p$ is an exact certificate, and agreement across
two independent primes rules out an unlucky choice of $p$.

**Result:** every instance tested — hyperbolic $\{7,3\}$ at $L=1,2$; square
at $N=113$; triangular at $N=187$ and, decisively, at $N=475$ (comparable
in size to instances where the floating-point computation reported a
substantial rank deficiency) — is **exactly full rank**, certified across
both primes. **The conclusion of this paper is therefore about
conditioning, not identifiability**: both lattice families are, at these
sizes, algebraically full-rank; what differs is the numerical precision
required to exploit that rank, which is polynomial in $N$ for the
hyperbolic case and grows so fast for the Euclidean case that it exceeds
what double-precision arithmetic can represent well before $N=10^3$.

## 5. Errors found and corrected during this work, reported as part of the record

Per the working discipline this project follows (errors are corrected in
place, not silently), two measurement bugs materially affected earlier
statements of this result and are documented here rather than only in the
supplementary code history:

1. **A condition-number reporting bug.** An early implementation computed
   $\kappa$ as the ratio of the largest singular value to the smallest one
   *above a numerical rank-tolerance threshold*; since that threshold is
   itself proportional to $1/(\max(\text{shape})\cdot\varepsilon_{\text{machine}})$,
   this silently capped every reported $\kappa$ at that value, which was
   mistaken for the flat lattice's true condition number approaching
   double precision's representable range. The reported "plateau" values
   matched the cap formula to four significant figures — not a
   coincidence. Corrected to report the untruncated ratio, and to flag a
   case as numerically singular rather than printing a number when the
   smallest singular value cannot be distinguished from machine noise. The
   corrected result is *stronger*, not weaker (§3).
2. **A rank-deficiency claim, retracted by §4's exact computation.** The
   same tolerance-based reasoning had produced an apparent structural rank
   deficiency on large flat lattices, initially reported as edges being
   "structurally unrecoverable." The exact modular-arithmetic computation
   shows this was also a precision artefact.

## 6. Formal verification (partial)

The combinatorial half of the argument in §3 — that the hyperbolic
lattice's boundary node count, given the measured recurrence
$b_{n+2}=3b_{n+1}-b_n$, grows at least geometrically, hence depth is
$O(\log N)$ — has been formalised as a Lean 4 proof (`HyperbolicLogDepth.lean`,
supplementary material). **This proof has not been checked by the Lean
kernel**: the computing environment used for this draft could not execute
the Lean toolchain, so the proof is offered as written, not as verified,
pending an independent compilation and the standard build/`sorry`-check/
axiom-audit gate. It formalises only the combinatorial growth fact, not
the conditioning result itself (which remains a numerical/exact-rank
claim, §3–4) or a re-derivation of the Schur-complement identity in §2.2
(already present in Mathlib's `LinearAlgebra.Matrix.SchurComplement`).

## 7. Limitations, stated plainly

- **Curve-fitting caution.** With only three unsaturated flat-lattice data
  points, this work does not distinguish $\kappa\sim\exp(c\sqrt N)$ from a
  steep power law $\kappa\sim N^p$ for large $p$ — the qualitative claim
  (polynomial vs. eventually-unrepresentable growth) is well supported;
  the specific functional form of the flat-lattice divergence is not.
- **A negative result, included rather than omitted.** A simulated
  reconstruction of perturbed interior conductances from noisy boundary
  data (0.1% additive noise) succeeds at $L=1$ and *fails* at $L=2$
  ($\kappa(L{=}2)\approx290$, expected error $\approx0.29 > $ the $0.15$
  success threshold set before running it). This means a physical build
  at $L=2$ is not yet justified by the present analysis without either a
  tighter hardware precision budget ($\lesssim5\times10^{-4}$ total
  relative error) or reformulating the reconstruction task as difference
  imaging (localising a *change* in conductance, a better-conditioned
  problem than absolute recovery).
- **Hardware measures a different map than is simulated.** A physical
  network with current injection and voltage readout measures the
  Neumann-to-Dirichlet map $\Lambda^{+}$, not $\Lambda$; converting
  between them amplifies noise by $\kappa(\Lambda)$, which is exactly the
  quantity this paper shows becomes large. This must be accounted for in
  any physical realisation, and is not yet resolved here.
- **Bounded novelty search.** Two targeted searches did not find prior
  work stating the log-depth/polynomial-conditioning mechanism for
  hyperbolic resistor networks specifically, but this is not a systematic
  literature review. Gromov-hyperbolic graphs are quasi-trees, and
  effective resistance on trees is additive; a connection to tree-metric
  reconstruction from leaf distances is plausible and unexamined.
- **Extended precision needed for large $N$.** The double-precision
  "numerically singular" results at $N\gtrsim400$ (flat) establish that
  double precision cannot resolve the condition number there; they do not
  by themselves establish its true magnitude, which would need
  arbitrary-precision arithmetic.

## Data and code availability

All code, preregistrations, self-tests, raw data, and the Elenchus ledger
entries (tiers X and B) for every claim in this draft are in
`experiments/track_h_hyperbolic_network/` of the accompanying repository,
including the full correction history described in §5.
