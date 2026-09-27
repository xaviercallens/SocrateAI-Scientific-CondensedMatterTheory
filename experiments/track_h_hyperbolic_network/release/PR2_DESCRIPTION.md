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

### v1.1 (revised after peer review, 2026-09-27)
- The review is recorded verbatim with a point-by-point response in `paper/reviews/`; all requested computations were preregistered first (`PREREGISTRATION_3.md`).
- **Correction of v1.0:** a dimension-matched probe control refuted our prediction; at matched probe count and matched dimension the advantage is ≤ 0.5 decades (reversed at N≈112). Ledger H0-X-0005 + correction note on H0-X-0003.
- **Disorder:** all predictions held; the gap widens to 8.3 decades under two-decade log-uniform disorder (H0-X-0006).
- **Flat scaling beyond float64:** 512-bit Arb gives log₁₀κ = 15.99 (triangular N=421) and 16.54 (square N=797), within 0.4 decades of the preregistered exp(c√N) extrapolation and ≥ 2.7 decades from a power law; the largest case, triangular N=1069, gives 26.95 (depth form: 25.94; power law: 15.98). Local exponent keeps increasing (H0-X-0007).
- Proposition 1's degree-three premise argued for general L; the seven "typos" in the review were PDF-extraction artefacts.
- New Zenodo version under the concept DOI (v1.0 stays frozen); three new dataset tables.

### Published
- **Zenodo:** DOI [10.5281/zenodo.23000391](https://doi.org/10.5281/zenodo.23000391) (paper, dataset, code).
- **Hugging Face:** the [dataset](https://huggingface.co/datasets/callensxavier/hyperbolic-resistor-networks) and the [simulator](https://huggingface.co/callensxavier/hyperbolic-resistor-network-simulator).
- See `release/PUBLISHED.md`.

## Test plan
- [x] `python3 paper/build.py`: 0 undefined references, 0 overfull boxes
- [x] `python3 release/check_bundle.py`: all checks pass
- [x] Ledger gate: no findings without `--evidence-dir`; with it, every paper-cited claim verifies (5 older, unrelated digests flagged)
- [x] rusty-SUNDIALS wheel built and installed; `rc_network.py` re-run with both integrators, all controls pass
- [x] Hugging Face repositories published and checked without a token (all files present)
- [x] Zenodo draft checked against the build (MD5 checksums and metadata), then published

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01ScQDrMoCqVGrcxJWtEuG2N
