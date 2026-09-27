## Summary

Earlier commits on this branch: the finite-size smearing erratum, the scientific roadmap v1, and the lab plan.

This update adds **Track H**: the conditioning of the discrete inverse conductance problem on hyperbolic lattices.

### Preprint
- **Paper:** `experiments/track_h_hyperbolic_network/paper/main.pdf` (10 pages), with LaTeX source in `main.tex`.
  - Every table and figure is generated from `data/*.json` by `make_assets.py`.
  - `build.py` fails the build if any reference or citation is undefined.

### Results
- **Conditioning.** κ grows polynomially on {7,3}: log₁₀κ = 3.89 at N=847, inside the preregistered band. Flat lattices reach 10^9.7 at N=317 and are float64-singular from N≈400.
- **Exact identifiability.** GF(p) ranks with two primes show every tested full-boundary network is exactly full rank. The certificates are in `data/exact_rank_full.json`.
- **Probe-matched control.**
  - The preregistered version was singular by design. The exact deficiency equals the number of unmeasured degree-2 nodes (series reduction).
  - On the identifiable subspace (a post hoc metric), log₁₀κ is 2.97 vs 9.72.
- **Neumann-to-Dirichlet map.** The ordering is preserved, as preregistered.
- **H2 (RC network).**
  - The finite-size prediction is **refuted** as preregistered.
  - A domain-monotonicity argument shows λ_min decreases to λ₀({7,3}) > 0, so τ ≤ C/λ₀ for all N.
  - Its premises are certified for L ≤ 6: interior degree 3, and interior(G_L) = G_{L−1} by coordinates and edge sets.
- **Integrator controls.** K1 and K2 pass with **both** SciPy BDF and the rusty-SUNDIALS CVODE solver (binding 6.0.0 from af4886f). Both agree with the exact solution to about 3e-8 (H2-X-0004).
- **rusty-SUNDIALS contribution.** `release/rusty_sundials_contrib/` holds the RC-network benchmark (two fixture networks, pytest) and `apply.sh`. Merged upstream as [rusty-SUNDIALS#62](https://github.com/xaviercallens/rusty-SUNDIALS/pull/62) (4ce8abb).

### Ledger
- The Elenchus ledger has 19 claims and a content-addressed evidence store in `docs/elenchus/evidence/`.
- `ledger.py --evidence-dir` verifies every claim the paper cites.
- It blocks on 5 older digests that match no tracked file: SSH-L-0001, SSH-C-0001, POC-X-0001, POC-X-0002, and the superseded H0-X-0001. Each is flagged in its notes, and no statement was changed.

### Release tooling (`release/`)
- `export.py` builds the HF dataset, HF model repository (simulator code, no weights) and Zenodo bundles.
- `check_bundle.py` checks the bundles.
- `hf_upload.py` uploads to Hugging Face.
- `zenodo_draft.py` creates a Zenodo draft only and never publishes.

## Test plan
- [x] `python3 paper/build.py`: 0 undefined references, 0 overfull boxes
- [x] `python3 release/check_bundle.py`: all checks pass
- [x] Ledger gate: no findings without `--evidence-dir`; with it, every paper-cited claim verifies (5 older, unrelated digests flagged)
- [x] rusty-SUNDIALS wheel built and installed; `rc_network.py` re-run with both integrators, all controls pass
- [ ] `hf auth login`, then `release/hf_upload.py --namespace <user>`
- [ ] `ZENODO_TOKEN=... release/zenodo_draft.py`, review the draft, then publish manually

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01ScQDrMoCqVGrcxJWtEuG2N
