## v1.1: revised after peer review

Revision of the Track H preprint *Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices* in response to a peer review of v1.0. The review is recorded verbatim
and answered point by point in `experiments/track_h_hyperbolic_network/paper/reviews/`. Every computation the
review asked for was **preregistered before it was run** (`PREREGISTRATION_3.md`).

### What changed
- **Correction of v1.0 (§3.3).** A dimension-matched probe control refuted our own preregistered prediction: against
  the square lattice's best-conditioned subspace of the same dimension, the hyperbolic advantage at matched probe
  count is at most 0.5 decades (N≈316) and reversed at N≈112. v1.0's sentence "the conditioning advantage survives
  probe matching" is withdrawn. The full-boundary result is unchanged, and the paper explains why the two are
  consistent.
- **Inhomogeneous conductances (§3.5, new).** Uniform disorder, two-decade log-uniform disorder, and ×100 / ×0.01
  defects. All preregistered predictions held; under strong disorder the gap widens to 8.3 decades.
- **Flat-lattice scaling beyond double precision (§2.4, §3.1).** Condition numbers of the double-precision-singular
  flat instances computed in 512-bit ball arithmetic (Arb) with certified radii; rival forms fixed in advance.
  Result: log₁₀κ = 15.99 (triangular N=421), 16.54 (square N=797), 26.95 (triangular N=1069), each within one
  decade of the preregistered e^{c√N} extrapolation and 2.7–11 decades from a power law. The flat growth is
  exponential in boundary depth; limitation (i) of v1.0 is resolved.
- **Proposition 1 (§3.6).** The degree-three premise is now argued for general L (disk property via the Euler
  characteristic; three heptagons per vertex).
- Seven "typographical" points in the review were artefacts of PDF text extraction; the source was correct.

### Also in this release: follow-up experiments after the Zenodo v1.1 record (not in the paper)
Preregistered and committed before each run (`PREREGISTRATION_5.md` to `PREREGISTRATION_10.md`); results in
`experiments/track_h_hyperbolic_network/TDA_RESULTS.md` and `LOCALIZATION_RESULTS.md`; ledger H3-X-0001 to H3-X-0007.
- A deep bulk defect has no persistent-homology signature on the boundary resistance metric.
- Defects are detected against measurement noise at the 3×10⁻⁴ budget on all four lattices, and against component
  tolerance up to 5 % on the hyperbolic lattices (1 % on the flat R=10); comparing a board with its own earlier
  measurement always works.
- Single-node localisation is perfect at 3×10⁻⁴ on flat and hyperbolic lattices alike; the hyperbolic lattice's
  advantage is a noise margin (≥ 100× at N≈316), and component tolerance up to 5 % does not degrade localisation.
- **Corrections recorded in the open:** an earlier "×2 defects are ~100× weaker" note was wrong (the response
  saturates); two localisation predictions and one tolerance prediction were refuted (`LL.md`: LL-A8 to LL-A11).
- Limits: single-node defects, known-contrast oracle decoder, i.i.d. noise, 20 trials per cell, tolerance ≤ 5 %.
- Also new: `LL.md`, `tools/restart.sh`, the project skill, `corpus/ingest_generated.py`,
  `tools/build_physics_verdicts.py` (`training/`), `tools/export_session_traces.py`.

### Records
- Zenodo: **DOI 10.5281/zenodo.23002378** (v1.1), under concept DOI 10.5281/zenodo.23000390; v1.0 stays at 10.5281/zenodo.23000391.
- Hugging Face dataset: three new tables (`conditioning_arb.csv`, `disorder.csv`, `subspace_control.csv`).
- Ledger: H0-X-0005 (dimension control, refuted prediction), H0-X-0006 (disorder), H0-X-0007 (Arb scaling);
  correction note appended to H0-X-0003.
- Lessons learned: `LL.md` LL-A7, LL-D9, LL-D10.
