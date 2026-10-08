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
