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

### Follow-up experiments after v1.1 (in the repository, **not** in the paper or the Zenodo v1.1 record)
Each was preregistered and committed before it ran; refutations and corrections are kept.
- **Boundary persistent homology (Gudhi), prereg 5:** a deep bulk defect leaves no topological signature (H3-X-0001).
- **Detection vs measurement noise, prereg 6; vs component tolerance, prereg 7:** a ×100 defect is detected at the 3×10⁻⁴ budget on all four lattices; against tolerance it survives 5 % on both hyperbolic lattices and 1 % on the flat R=10 (H3-X-0002/3).
- **Correction:** a ×2 defect is *not* ~100× weaker than ×100 (the response saturates, 27–37 %); my earlier note was wrong and is corrected (H3-X-0004, LL-A9).
- **Localisation, prereg 8–10:** single-node localisation is perfect at 3×10⁻⁴ on flat *and* hyperbolic lattices (two of my predictions refuted, LL-A10); the noise sweep shows the hyperbolic advantage is a noise margin (flat fails at 10⁻³–3×10⁻³, hyperbolic holds to ≥ 10⁻¹, ≥ 100× at N≈316); component tolerance up to 5 % does not degrade localisation (H3-X-0005..0007, LL-A11).
- **Other tilings, prereg 11 (H0-X-0008):** at equal maximal depth the hyperbolic tilings ({7,3}, {8,3}, {5,4}, {6,4}, {4,5}) agree within 0.56 decades while N varies ~15×; flat lattices are ≥ 1.8 decades worse at equal depth. The paper's "mechanism is depth" sentence holds within the hyperbolic class only (to qualify in a v1.2). One exponent prediction refuted; a control tolerance was amended in the open before any tiling result (LL-A12).
- **v1.2 draft** (`paper/main_v1_2.pdf`, generated from the v1.1 source by `paper/make_v12.py`, not published): folds in the tilings result, the defect detection/localisation simulations, an extended verification table and a v1.1 typesetting erratum. The published v1.1 source and PDF are untouched.
- Ledger: 30 claims, gate clean; training labels: 36 predictions; lessons learned in `LL.md`; roadmap updated (`docs/roadmap.md`, rows H-3a/H-3b).
- Limits: single-node defects, oracle decoder (known contrast set), i.i.d. noise, 20 trials per cell, tolerance ≤ 5 %.

### Published
- **Zenodo v1.1:** DOI [10.5281/zenodo.23002378](https://doi.org/10.5281/zenodo.23002378); v1.0: [10.5281/zenodo.23000391](https://doi.org/10.5281/zenodo.23000391); concept DOI 10.5281/zenodo.23000390.
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
