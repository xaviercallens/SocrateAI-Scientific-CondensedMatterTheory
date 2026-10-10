# Programme: where topology drives physics, and where it does not

Date: 2026-10-10. Status: a research structure, not a result. It organises what the repository already contains (five experimental axes, the Lean ladder, Track H,
the entanglement-TDA proof of concept) into one testable thesis with a counter-programme, and fixes the discipline each node follows (docs/rigor_protocol.md,
`experiments/track_h_hyperbolic_network/protocols/protocol_computational.pdf`). Nothing in it is claimed until its node's gates pass.

## 1. The thesis, stated so that it can lose

"Physics is driven by topology" is not a claim that can be tested as written. The testable form is a family of statements of one shape:

> **In domain D, an integer invariant ν of the bulk (a winding number, a Chern number, a circulation, a catastrophe type, a Betti number) determines an observable O of the
> boundary or of the response, with O robust to a class P of perturbations and failing outside P.**

Each node of the programme is one such statement, with three parts that must all be present before the node counts:
- **T (theorem):** the exact statement proved, in Lean 4 where the ladder reaches it, kernel-checked; what is *not* proved is written beside it.
- **E (experiment):** a preregistered measurement, numerical or physical, with gates, bands and a refutation criterion fixed before data exist.
- **L (limit):** the perturbation class outside which ν no longer determines O, measured, not assumed. A node without a measured limit is incomplete.

The thesis is refuted at a node when ν is well-defined and O is not determined by it inside P. The thesis is *bounded* at a node when the limit L is found. The
programme's output is the map of nodes with their limits, not a slogan.

## 2. The counter-programme (already partly done)

Track H is the counter-programme and is further advanced than the thesis. On the discrete inverse conductance problem the controlling quantity is geometric and spectral,
not topological: the condition number of the DtN Jacobian grows exponentially in depth on flat lattices and polynomially on hyperbolic ones (doi 10.5281/zenodo.23228685);
the rate on solvable strips is a Green-function exponent (doi 10.5281/zenodo.23241463); nearest-neighbour persistent homology of the Jacobian columns sees only a power law
and learned persistence features fail a leak gate, while the Gram–Schmidt residual carries the rate (doi 10.5281/zenodo.23244556, 10.5281/zenodo.23248393, preregistration 33).
Reading: on this problem, geometry (curvature, non-amenability, the spectral gap) decides, and topology of the data cloud does not. Every thesis node below must say what
distinguishes it from this case: a *gap* protected by a symmetry class, which the conductance problem does not have.

## 3. The nodes

| Node | Domain | ν (bulk) | O (boundary / response) | T status | E status | L (limit to measure) |
|---|---|---|---|---|---|---|
| N1 | SSH chain, classical waves (axis 1) | winding of v + w z | one zero mode at the left end of the odd open chain | bulk half: the two residue integrals in `lean/dtn_offsets/SSHWinding.lean` (gates G1–G4 pass, wording audited; `h' = w`, non-vanishing on the circle, the transfer under the integral and the `(2πi)⁻¹` normalisation remain to formalise); boundary half: exact arithmetic on instances (`ssh_exact.py`, Tier B), Lean T2 not yet; T3 (Toeplitz index) not started | preregistered (axis 1a), not run; PoC on the ring (entanglement spectrum, POC-X-0001) | chiral-symmetry breaking (on-site terms), coupling disorder beyond the gap, lateral leakage in the channel |
| N2 | Vortex / orbital angular momentum (axis 3, acoustic route) | integer phase winding ℓ | phase singularity, OAM, quantised by homotopy | T0–T1 reachable (homotopy invariance, Stokes quantisation), not started | preregistered, not run | nonlinearity, finite aperture (singularity splitting), reconnection |
| N3 | Caustics (axis 5) | Arnold type A₂, A₃, A₄, D₄ | stable singularity list of a generic front | normal form of the cusp (T2 in the ladder), not started | preregistered, not run; the most robust node: disorder is the subject | non-generic (symmetric) surfaces; caustics of non-stable type that persist by symmetry |
| N4 | Analogue horizon (axis 2) | none topological; ergoregion is geometric | superradiant amplification | reformulated: not a topology node, kept as a geometry control | preregistered (stimulated scattering), not run | — (control) |
| N5 | Wave chaos (axis 4) | none topological; spectral statistics | Weyl law, level repulsion | T2 rectangle Weyl asymptotics, not started | pivot to microwave billiard, not run | — (control) |
| N6 | Phase transitions by persistent homology | Betti numbers of configuration clouds | order parameter, critical exponent of persistence | no theorem; literature (Donato et al., Cole–Loges–Shiu, Loftus 2026: H₀ is density, H₁ is topology) | not started; the TDA toolchain and 24 papers are in the vector store | density-driven H₀ signal (Loftus) must be separated by a stratified null (LL-A21) |
| N7 | Hyperbolic lattices (Track H boards) | none; spectral gap from non-amenability | relaxation time, conditioning | Kesten, Dodziuk, Higuchi–Shirai (literature, not Lean) | garage protocol H4 (not run); conditioning done | counter-programme node |

Nodes N4, N5, N7 are *controls*: domains where an integer invariant is absent and geometry or spectrum controls the physics. The thesis needs them as much as N1–N3; a programme that only
collects successes of topology is not a test.

## 4. Order of execution and what each step costs

1. **N1, T:** finish the bulk half in Lean (this commit), then the boundary half as a Lean statement about the finite matrix (nullity of the odd chain's chiral block, exactness of the kernel vector),
   then lock T2 under `statement_lock.py` with an independent wording audit. Cost: days. The ladder's T3 (Toeplitz index, dim ker = |ν| on the half-line) stays an ambition.
2. **N1, E and L (numerical):** a preregistered card on the finite SSH chain with on-site disorder and chiral-symmetry-breaking terms: measure the zero-mode energy and localisation against the
   perturbation strength, and find the class P where the left-end mode survives and the strength where it does not (the limit L). Exact arithmetic where possible (the chain is small), double precision otherwise, with the gates of the computational protocol. Cost: a day.
3. **N6:** persistent homology of Ising or XY configurations with the density-versus-topology decomposition of Loftus as the preregistered control, so that the H₀ signal is not mistaken for topology (the lesson of preregistration 33). Cost: days; a reuse of the GUDHI pipeline.
4. **N1, E (physical) and N3:** the garage axes 1a and 5, in the order the experimental programme recommends; their protocols exist, their numbers are provisional until the band calculation is committed.
5. **N2:** acoustic vortex (route B), after N1's chain of metrology is proven.

## 5. What a sceptical reviewer will say, and the answer the programme must give

- *"Bulk–boundary correspondence is a theorem; measuring it again adds nothing."* The answer is in L: the programme measures where the correspondence fails for a given platform, with the failure strength preregistered.
- *"Classical analogues are not the quantum systems where topology matters."* Agreed and stated: the nodes are classical-wave realisations of the same spectral theorems; nothing about quantum matter is claimed.
- *"Persistent homology is blind to spectral content."* Known (docs/LITERATURE_REVIEW_TDA.md §4); N6 uses the density-versus-topology decomposition and N7 is the recorded counter-example.
- *"The thesis is unfalsifiable."* Each node has a refutation criterion; N7 already refutes it in one domain, and the programme's output includes that refutation.

## 6. Rules carried over
Commit before run; refutations kept; numbers from stored data; never edit a published artefact; say what is not claimed; nothing concerns holography (docs/rigor_protocol.md; LL.md LL-A13 to LL-A22).

## 7. The thesis after the first survey and the first node (2026-10-10)

A verified survey (sources in the vector store, pillar `topoprog`; the four already present are under `topology` and `hyperbolic`) gives, for each domain, the theorem, the measurement and the limit:
- **Condensed matter.** Theorems: Kitaev's periodic table (arXiv:0901.2686), the ten-fold way (0912.2157), Graf–Porta bulk-edge correspondence under a spectral gap (1207.5989), Prodan–Schulz-Baldes bulk index under a *mobility* gap but bulk-boundary equality only under a *spectral* gap (1510.08744), Bellissard–van Elst–Schulz-Baldes: Hall conductance is a Fredholm index, quantised while the Fermi level sits in localised spectrum (cond-mat/9411052). Measurements: von Klitzing 1980; the Zak phase difference 0.97(2)π between SSH dimerisations (Atala et al., 1212.0572). Limits: interactions reduce Z to Z₈ (Fidkowski–Kitaev, 0904.2197); non-Hermitian point-gap topology produces skin modes and no protected boundary states (Okuma et al., 1910.02878); disorder can create a quantised phase from a trivial metal (topological Anderson insulator, 0811.3045).
- **Classical waves.** Kane–Lubensky index theorem for isostatic lattices (1308.0554); Delplace–Marston–Venaille equatorial waves (1702.07583); limits: the edge-mode count of a continuum depends on the boundary condition (Tauber–Delplace–Venaille, 1902.10050), and the best photonic measurement finds no protection against real roughness (Rosiek et al., 2206.11741).
- **Fluids.** Helicity is conserved through reconnection because the reconnecting strands are anti-parallel; the *topology* (linking) is exactly what is not conserved (Scheeler et al., 1404.6513).
- **Field theory.** Anomaly inflow (Callan–Harvey 1985); Witten's η-invariant cancellation and the Z₁₆ reduction (1508.04715).
- **Statistical mechanics.** The strongest "topological origin of phase transitions" theorem is false: Kastner–Mehta's 2D φ⁴ transition with constant Euler characteristic (1108.2345). Persistence signals are necessary, not sufficient.
- **Hyperbolic lattices.** Chern numbers exist (Urwyler et al., 2203.07292) but a macroscopic fraction of states is boundary, and the known gaps are geometric (Kollar et al.: "the origin of the spectral gap remains unknown").

**The reviewer's verdict, adopted.** Every theorem carries a gap hypothesis, spectral or mobility; the invariant decides a discrete fact and the gap decides the margin. The defensible thesis is therefore:

> **Topology constrains, under a gap, what geometry and spectrum then determine.**

Node N1's readable run says exactly this (`experiments/axis1_topological_waves/RESULTS_N1_LIMIT2.md`; the first run, N1-L, had both gates fail through my errors and is kept unread): the winding fixes the side of the end mode; chiral symmetry fixes its energy at zero for any coupling disorder short of gap closing; the gap fixes how far a symmetry-breaking term may go (a third of the gap for on-site terms, a fifth for same-sublattice hopping) before the mode leaves the end.
The programme's title is weakened accordingly, and each remaining node must report its margin, not only its invariant.
