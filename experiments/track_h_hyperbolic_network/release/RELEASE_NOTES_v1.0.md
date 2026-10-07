## v1.0: Track H preprint, data and simulator

First scientific release. It contains a preprint, with its data and numerical model, on the conditioning of the
discrete inverse conductance (Calderón) problem on hyperbolic lattices.

### Preprint
*Logarithmic boundary depth and the conditioning of the discrete inverse conductance problem on hyperbolic
lattices*, X. Callens (2026).
- **Zenodo** (paper, dataset, code): DOI [10.5281/zenodo.23000391](https://doi.org/10.5281/zenodo.23000391), record https://zenodo.org/record/23000391
- **PDF:** attached to this release, and at `experiments/track_h_hyperbolic_network/paper/main.pdf`

### Results
- **Conditioning.** The condition number κ grows polynomially on the {7,3} lattice: log₁₀κ = 3.89 at N=847, inside the preregistered band. Flat lattices reach 10^9.7 at N=317 and cannot be resolved in float64 from N≈400. The mechanism is boundary depth, O(log N) versus O(√N).
- **Identifiability.** Exact GF(p) ranks show every tested network is algebraically identifiable. The difference between geometries is conditioning, not identifiability.
- **Robustness.** The advantage survives probe matching (a post hoc metric on the identifiable subspace) and holds for the Neumann-to-Dirichlet map.
- **RC network.** A preregistered finite-size prediction was refuted. Separately, a domain-monotonicity argument shows the Dirichlet spectral gap decreases to λ₀ > 0, so the RC relaxation time is bounded uniformly in N.
- **Solver cross-check.** SciPy BDF and the rusty-SUNDIALS CVODE solver both match the exact solution (errors below 3e-8).

### Data and model
- **Dataset:** https://huggingface.co/datasets/callensxavier/hyperbolic-resistor-networks
- **Simulator** (code only, no weights): https://huggingface.co/callensxavier/hyperbolic-resistor-network-simulator
- **rusty-SUNDIALS benchmark:** merged upstream in xaviercallens/rusty-SUNDIALS#62

### Rigour
- **Preregistration:** predictions were fixed before running (`PREREGISTRATION.md`, `PREREGISTRATION_2.md`). Deviations and refutations are reported as results.
- **Claim ledger:** `docs/elenchus/ledger.json` holds 19 claims, with a content-addressed evidence store in `docs/elenchus/evidence/`. Every claim the paper cites verifies against the stored evidence.
- **Generated outputs:** every table and figure is generated from `data/*.json` by `paper/make_assets.py`.

### Also in this release (since v0.1)
- Erratum on finite-size smearing (PoC)
- Scientific roadmap v1 and laboratory plan

### Licences
- Paper and data: CC BY 4.0
- Code: MIT
