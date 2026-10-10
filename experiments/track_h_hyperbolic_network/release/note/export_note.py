#!/usr/bin/env python3
"""Build the Zenodo bundle for the strip-rate paper: release/build/zenodo_note/{paper.pdf, dataset.zip, code.zip}.
Run from anywhere: python3 release/note/export_note.py"""
import hashlib
import shutil
import zipfile
from pathlib import Path

TRACK = Path(__file__).resolve().parents[2]
REPO = TRACK.parents[1]
OUT = TRACK / "release" / "build" / "zenodo_note"
OUT.mkdir(parents=True, exist_ok=True)

DATA = ["cylinder_exponential_sum_picture", "momentum_resolved_rates_on_the_cylinder", "momentum_diagnostic", "momentum_height_diagnostic",
        "exact_semi_infinite_blocks_asymptotic_ra", "diagonal_boundary_orientation_and_the_gr", "diagonal_signed_nodes_diagnostic",
        "aligned_strip_with_unequal_conductances", "aligned_strip_height_diagnostic", "curvature_on_a_polar_grid_disk",
        "laplace_resolved_jacobian_conditioning", "laplace_link_tail_corrected", "laplace_wide_window_posthoc"]
PREREGS = [f"PREREGISTRATION_{n}.md" for n in (23, 24, 25, 26, 27, 28, 29)]
SCRIPTS = ["exp23_cylinder_exponential_sum_picture.py", "exp24_momentum_resolved_rates_on_the_cylinder.py", "exp24_diag_floor.py", "exp24_diag_height.py",
           "exp25_exact_semi_infinite_blocks_asymptotic_ra.py", "exp26_diagonal_boundary_orientation_and_the_gr.py", "exp26_diag_signed_nodes.py",
           "exp27_aligned_strip_with_unequal_conductances.py", "exp27_diag_height.py", "exp28_curvature_on_a_polar_grid_disk.py",
           "exp29_laplace_resolved_jacobian_conditioning.py", "exp29_diag_g1_tail.py", "exp29_diag_wide_window.py", "hyperbolic_network.py"]
LEAN = ["DtNOffsets.lean", "lakefile.lean", "lean-toolchain", "lake-manifest.json", "STATUS.md", "docs/statement_lock.json"]

README = """Strip-rate paper: bundle contents

paper.pdf      the paper (8 pages)
dataset.zip    data/*.json behind every table and figure, preregistrations 23-29, results blocks (TILINGS_RESULTS.md, MECHANISM_NOTE.md)
code.zip       experiment scripts exp23-exp29, the network builder, the figure/table generator, the LaTeX source, the Lean 4 project dtn_offsets,
               the literature review document

Reproduce tables and figures from the stored data: python3 paper/make_note_cylinder.py, then pdflatex note_cylinder.tex twice.
Companion preprint: doi:10.5281/zenodo.23228685 (concept doi:10.5281/zenodo.23000390). Code MIT, data and paper CC BY 4.0.
Nothing here concerns holography.
"""


def zipit(name, items):
    with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in items:
            z.write(path, arc)
        z.writestr("README.txt", README)


def main():
    shutil.copyfile(TRACK / "paper" / "note_cylinder.pdf", OUT / "paper.pdf")
    ds = [(f"data/{n}.json", TRACK / "data" / f"{n}.json") for n in DATA]
    ds += [(n, TRACK / n) for n in PREREGS]
    ds += [(n, TRACK / n) for n in ("TILINGS_RESULTS.md", "MECHANISM_NOTE.md")]
    zipit("dataset.zip", ds)
    cs = [(f"scripts/{n}", TRACK / n) for n in SCRIPTS]
    cs += [("paper/" + n, TRACK / "paper" / n) for n in ("make_note_cylinder.py", "note_cylinder.tex", "tables_note.tex")]
    cs += [("lean/dtn_offsets/" + n, REPO / "lean" / "dtn_offsets" / n) for n in LEAN]
    cs += [("docs/LITERATURE_REVIEW_INVERSE.md", REPO / "docs" / "LITERATURE_REVIEW_INVERSE.md"), ("LICENSE-MIT", TRACK / "release" / "LICENSE-MIT")]
    zipit("code.zip", cs)
    for f in sorted(OUT.iterdir()):
        print(f.name, f.stat().st_size, hashlib.md5(f.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
