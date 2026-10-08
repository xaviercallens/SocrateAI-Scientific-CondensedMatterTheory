# Publication plan for paper 3 (prepared 2026-10-08, not executed)

Title: Ill-conditioning of the discrete inverse conductance problem as exponential dependence on the earlier span: a column-residual certificate, partly machine-checked, and its measurement (5 pages).

Status: manuscript built (`paper/paper3.tex`, `.pdf`), bundle built by `python3 release/paper3/export_paper3.py` into `release/build/zenodo_paper3/` (paper.pdf, dataset.zip, code.zip), metadata in `release/paper3/zenodo_metadata_paper3.json`.
No Zenodo draft exists yet. The bundle was built from commit 4d2f9fd plus this plan; rebuild it right before the draft if anything changes.

## When the user says go (from the track directory)
1. `python3 release/paper3/export_paper3.py` (rebuilds the bundle; the zip checksums change with timestamps, so draft and publish from the same build).
2. `python3 release/paper3/zenodo_paper3.py draft` prints the draft id.
3. `python3 release/paper3/zenodo_paper3.py publish <id>` verifies the three MD5 sums and the metadata against the local build, refuses on any difference, then publishes (irreversible).
4. `python3 release/paper3/zenodo_paper3.py verify <id>` checks the public record without a token; append the record to `release/PUBLISHED.md`.

## Before publishing, worth deciding
- Specialist feedback has still not been obtained on any of the three records; the novelty of the exact strip statement is not established (docs/LITERATURE_REVIEW_INVERSE.md).
- Paper 3's Lean part cites a project that points to a local LeanMaster checkout; a reader needs LeanMaster to rebuild it. The README in the bundle says so.
- The runs of preregistrations 29 to 32 are recorded by the orchestrator, not entered in the evidence ledger.
