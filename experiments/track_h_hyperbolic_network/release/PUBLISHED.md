# Published records

## Version 1.2 (2026-10-08, mechanism of the depth dependence; defects; other tilings)

| Where | Identifier |
|---|---|
| Zenodo (paper, dataset.zip, code.zip) | DOI [10.5281/zenodo.23228685](https://doi.org/10.5281/zenodo.23228685), record https://zenodo.org/record/23228685 |
| Concept DOI (latest version) | [10.5281/zenodo.23000390](https://doi.org/10.5281/zenodo.23000390) |
| Hugging Face dataset (updated in place, 8 new tables) | https://huggingface.co/datasets/callensxavier/hyperbolic-resistor-networks |
| Hugging Face simulator (updated in place) | https://huggingface.co/callensxavier/hyperbolic-resistor-network-simulator |

Built from commit ccfc30d (`python3 release/export.py --v12`; `paper/build.py main_v1_2 --final`, 18 pages). MD5 of
paper.pdf 0662bfe4e948f9853edffe6791db373d, dataset.zip 10de7fb459a2d200fc01e5b623bebf81, code.zip
b32781f3a56f93081c1c1f138918eabc, verified against the draft by `zenodo_publish.py` before publishing; the public
record was then checked without a token (version 1.2, three files, open access). Changes from v1.1: see
`RELEASE_NOTES_v1.2.md` and the paper's "Changes from version 1.1". The v1.1 source and PDF are untouched.

Cite v1.2 as: Callens, X. (2026). *Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices* (v1.2). Zenodo. https://doi.org/10.5281/zenodo.23228685

## Version 1.1 (2026-09-27, revised after peer review)

| Where | Identifier |
|---|---|
| Zenodo (paper, dataset.zip, code.zip) | DOI [10.5281/zenodo.23002378](https://doi.org/10.5281/zenodo.23002378), record https://zenodo.org/record/23002378 |
| Concept DOI (latest version) | [10.5281/zenodo.23000390](https://doi.org/10.5281/zenodo.23000390) |
| Hugging Face dataset (updated in place, 3 new tables) | https://huggingface.co/datasets/callensxavier/hyperbolic-resistor-networks |
| Hugging Face simulator (updated in place) | https://huggingface.co/callensxavier/hyperbolic-resistor-network-simulator |

Built from commit 13b8e69; MD5 checksums of the three files verified against `release/build/zenodo/` before
publishing. Changes from v1.0: see `RELEASE_NOTES_v1.1.md` and the paper's "Changes from version 1.0".

Cite v1.1 as: Callens, X. (2026). *Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices* (v1.1). Zenodo. https://doi.org/10.5281/zenodo.23002378

## Version 1.0 (2026-09-27)

**Preprint:** Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices. Author: Xavier Callens.

| Where | Identifier |
|---|---|
| Zenodo (paper, dataset.zip, code.zip) | DOI [10.5281/zenodo.23000391](https://doi.org/10.5281/zenodo.23000391), record https://zenodo.org/record/23000391 |
| Zenodo concept DOI (always the latest version) | [10.5281/zenodo.23000390](https://doi.org/10.5281/zenodo.23000390) |
| Hugging Face dataset | https://huggingface.co/datasets/callensxavier/hyperbolic-resistor-networks |
| Hugging Face simulator (code only, no weights) | https://huggingface.co/callensxavier/hyperbolic-resistor-network-simulator |
| rusty-SUNDIALS benchmark | https://github.com/xaviercallens/rusty-SUNDIALS/pull/62 (merge commit 4ce8abb) |

The published files are the ones built from commit a8a5687. Before publishing, `zenodo_publish.py`
verified their MD5 checksums against `release/build/zenodo/`.

Licences: paper and data are CC BY 4.0; code is MIT.

## Cite

Callens, X. (2026). *Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices* (v1.0). Zenodo. https://doi.org/10.5281/zenodo.23000391

## Corrections

The record is frozen. Any correction is published as a new Zenodo version under the concept DOI,
never by editing v1.0.

## Strip-rate paper (2026-10-08, a separate record, not a version of the v1.x record)

| Where | Identifier |
|---|---|
| Zenodo (paper.pdf, dataset.zip, code.zip) | DOI [10.5281/zenodo.23241463](https://doi.org/10.5281/zenodo.23241463), record https://zenodo.org/record/23241463, concept DOI 10.5281/zenodo.23241462 |

Title: Exact exponential rates for the discrete Calderon problem on lattice strips, and what transient data do not change (8 pages). Built by
`python3 release/note/export_note.py`; MD5 of paper.pdf 641ed2245ecf7bd8429b401937a73ef9, dataset.zip 6b95e408c16aa5c5bca59d1b83215fe7, code.zip
e7ba2931e92cf259f268e41f5af59cee, verified against the draft by `release/note/zenodo_note.py publish` before publishing, and against the public record
without a token. Published on the author's explicit instruction. Related identifiers: isSupplementTo 10.5281/zenodo.23228685, references concept DOI 10.5281/zenodo.23000390.
Two empty drafts created by failed attempts of mine were deleted. The novelty of the exact statement is not established (see `docs/LITERATURE_REVIEW_INVERSE.md`); no specialist
feedback was obtained before publishing, contrary to the earlier plan, because the author asked for publication.

## Paper 2 (2026-10-08, a separate record)

| Where | Identifier |
|---|---|
| Zenodo (paper.pdf, dataset.zip, code.zip) | DOI [10.5281/zenodo.23244556](https://doi.org/10.5281/zenodo.23244556), record https://zenodo.org/record/23244556, concept DOI 10.5281/zenodo.23244555 |

Title: A topological proxy for the ill-conditioning of the discrete inverse conductance problem, and an independent integrator check of a resistor-capacitor bench (5 pages). Built by
`python3 release/paper2/export_paper2.py`; MD5 of paper.pdf 47f248657928e621def124cbbddf729b, dataset.zip 3f470a233102cfa352b5b7e6b750c501, code.zip fe2cc70f3f31ca508cc1978450257e72, verified against the draft by
`release/paper2/zenodo_paper2.py publish` before publishing and against the public record without a token. Published on the author's instruction ("Publish the 2 papers"): read as the strip-rate paper (already published, 10.5281/zenodo.23241463, not republished) and this one.
Related identifiers: isSupplementTo 10.5281/zenodo.23241463 and 10.5281/zenodo.23228685.

## Paper 3 (2026-10-08, a separate record)

| Where | Identifier |
|---|---|
| Zenodo (paper.pdf, dataset.zip, code.zip) | DOI [10.5281/zenodo.23248393](https://doi.org/10.5281/zenodo.23248393), record https://zenodo.org/record/23248393, concept DOI 10.5281/zenodo.23248392 |

Title: Ill-conditioning of the discrete inverse conductance problem as exponential dependence on the earlier span: a column-residual certificate, partly machine-checked, and its measurement (5 pages). Built by
`python3 release/paper3/export_paper3.py`; MD5 of paper.pdf 0dc928d7bfcd7a619f03de59eefe209f, dataset.zip 4654c20d9f2c729f75fd09041649ca9e, code.zip 67db9a1111d801cea8b0c0b1d4466945, verified against the draft by
`release/paper3/zenodo_paper3.py publish` before publishing and against the public record without a token. Published on the author's instruction ("publish, merge and prepare ..."). Related identifiers: isSupplementTo 10.5281/zenodo.23244556, 23241463 and 23228685.

## Programme manifesto (2026-10-10, a separate record)

| Where | Identifier |
|---|---|
| Zenodo (paper.pdf, dataset.zip, code.zip) | DOI [10.5281/zenodo.23283365](https://doi.org/10.5281/zenodo.23283365), record https://zenodo.org/record/23283365, concept DOI 10.5281/zenodo.23283364 |

Title: Topology constrains, under a gap, what geometry and spectrum then determine: a programme for testing where topology drives physics, with a verified history, a measured first node, and the tools to continue (9 pages). Built by
`python3 release/manifesto/export_manifesto.py`; MD5 of paper.pdf 31a11fb5569fa97ac57f53d6652ab605, dataset.zip a8e44f1ec37064d893489740c760a502, code.zip 748d7ebacda1d9c0137dca4d973d2897, verified against the draft before publishing and against the public record without a token.
Published on the author's instruction after node N1-L2 was run and read. The bundle holds both N1 runs (the first, unread, with its failed gates; the repeat, read), the Lean project (three modules, 12 locked declarations, 10 theorems), the two protocols, the programme document and the two literature reviews. Related identifiers: isSupplementTo the four earlier records.
The paper was revised after an adversarial read by a separate model instance (failure count corrected to 8 gates by design error and 12 refuted predictions; Lean claim narrowed; slogans removed). The title's phrase "a measured first node" refers to a diagonalisation of a model, which the paper says in its first sentence on the node.
