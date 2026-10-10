## v1.3 (2026-10-10): four new Zenodo records, the topology programme, Lean 4, protocols, corpus

Everything since v1.2 (156 commits on the branch `worktree-adscmt-litreview`, merged by PR #3). The v1.0, v1.1 and v1.2 artefacts are untouched. Every computation
was preregistered and committed before its run (preregistrations 23 to 33 of Track H, N1-L and N1-L2 of axis 1); every failed gate and refuted prediction is kept in its record.

### Published records (all CC BY 4.0, code MIT; each verified against the public record by checksum)
| Record | DOI | Pages |
|---|---|---|
| Exact exponential rates for the discrete Calderón problem on lattice strips, and what transient data do not change | [10.5281/zenodo.23241463](https://doi.org/10.5281/zenodo.23241463) | 8 |
| A topological proxy for the ill-conditioning of the discrete inverse conductance problem, and an independent integrator check of a resistor–capacitor bench | [10.5281/zenodo.23244556](https://doi.org/10.5281/zenodo.23244556) | 5 |
| Ill-conditioning of the discrete inverse conductance problem as exponential dependence on the earlier span: a column-residual certificate, partly machine-checked, and its measurement | [10.5281/zenodo.23248393](https://doi.org/10.5281/zenodo.23248393) | 5 |
| Topology constrains, under a gap, what geometry and spectrum then determine: a programme for testing where topology drives physics (the programme manifesto) | [10.5281/zenodo.23283365](https://doi.org/10.5281/zenodo.23283365) | 9 |

### Research results (Track H, preregistrations 23 to 33)
- Exact asymptotic rate of the DtN-Jacobian conditioning on solvable strips: the Green-function exponent of the node set (1.653 decades per row aligned, 1.067 diagonal, 1.762 and 2.498 at conductance ratios 0.05 and 16); curvature raises the rate; transient data lower the condition number by one decade and leave the rate unchanged.
- Nearest-neighbour persistent homology of the Jacobian columns sees depth only as a power law; the depth-ordered Gram–Schmidt residual carries the exponential rate (1.243 against 1.272 decades per layer) and transfers to hyperbolic tilings; learned persistence features fail a depth-stratified leak gate and are unread.
- CVODE (rusty-SUNDIALS) reproduces the garage bench's time constants to 3e-5 and the predicted ratio 0.604 within 1 %.

### Topology programme
- `docs/TOPOLOGY_PROGRAMME.md`: the thesis as nodes N1 to N7 with theorem, experiment and limit; Track H as the counter-programme; the thesis weakened after a verified survey.
- Node N1 (finite SSH chain): first run unread (both gates failed through design errors, kept); repeat N1-L2 read: end mode exact under chiral disorder to 50 %, on-site breaking tolerated to a third of the gap, same-sublattice hopping to a fifth.

### Lean 4 (`lean/dtn_offsets`, Mathlib v4.34.0-rc2 through LeanMaster)
Three modules, 12 locked declarations, 10 theorems depending only on propext, Classical.choice and Quot.sound: zero row and column sums and symmetry of the Schur-complement DtN matrix, offset orthogonality, decision invariance, a column-residual bound on any lower bound of a matrix's action, and the two residue integrals of the SSH symbol's pole. Build, `sorry` search, axiom audit, statement lock and an independent wording audit for each module. What is not formalised is listed in `STATUS.md`.

### Protocols and corpus
- `protocols/protocol_garage.pdf` (H4, six sessions with gates) and `protocols/protocol_computational.pdf` (preregistration, numerics, Lean, publication, with the register of failures), 5 pages each.
- Corpus: 152 identity-checked papers in 13 pillars (new: `inverse`, `conditioning`, `tda`, `topoprog`), 5333 chunks in the Chroma store behind `mcp_adscmt_rag.py`; reviews in `docs/LITERATURE_REVIEW_INVERSE.md` and `docs/LITERATURE_REVIEW_TDA.md`.

### Lessons added
LL-A17 to LL-A23 in `LL.md` (reference height, depth windows, signed nodes, permutation gates, reviewing the method before using it, control clauses derived from the theorem).

### Not claimed
Novelty of the exact strip statement (Szegő 1936 and Widom–Wilf 1966 unread); any physical measurement (node N1 is a diagonalisation); anything about holography.
