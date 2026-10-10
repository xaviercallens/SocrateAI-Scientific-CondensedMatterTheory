#!/usr/bin/env python3
"""Build the Zenodo bundle for paper 3: release/build/zenodo_paper3/{paper.pdf, dataset.zip, code.zip}.
Run from anywhere: python3 release/paper3/export_paper3.py"""
import hashlib
import shutil
import zipfile
from pathlib import Path

TRACK = Path(__file__).resolve().parents[2]
REPO = TRACK.parents[1]
OUT = TRACK / "release" / "build" / "zenodo_paper3"
OUT.mkdir(parents=True, exist_ok=True)

DATA = ["depth_ordered_residuals_of_jacobian_columns", "jacobian_column_cloud_homology", "jacobian_column_cloud_homology_firstrun", "jacobian_column_cloud_homology_posthoc"]
PREREGS = [f"PREREGISTRATION_{n}.md" for n in (30, 32)]
SCRIPTS = ["exp29_laplace_resolved_jacobian_conditioning.py", "exp30_jacobian_column_cloud_homology.py", "exp32_depth_ordered_residuals.py",
           "exp32_pilot_residuals.py", "exp32_pilot_residual_cloud.py", "hyperbolic_network.py"]
LEAN = ["DtNOffsets.lean", "GramSchmidtBound.lean", "lakefile.lean", "lean-toolchain", "lake-manifest.json", "STATUS.md", "docs/statement_lock.json"]

README = """Paper 3: bundle contents

paper.pdf      the paper (5 pages)
dataset.zip    data/*.json behind every table and figure, preregistrations 30 and 32, results blocks (TILINGS_RESULTS.md)
code.zip       experiment scripts (exp29 imported by exp30 and exp32, exp30, exp32 and its two disclosed pilots), the network builder, the figure/table generator, the LaTeX source,
               and the Lean 4 project dtn_offsets (two modules, status file, statement lock)

Reproduce tables and figure from the stored data: python3 paper/make_paper3.py, then pdflatex paper3.tex twice. The Lean project builds against Mathlib v4.34.0-rc2 (see lakefile.lean; it points to a local LeanMaster checkout).
Companions: doi:10.5281/zenodo.23228685, doi:10.5281/zenodo.23241463, doi:10.5281/zenodo.23244556. Code MIT, data and paper CC BY 4.0.
Nothing here concerns holography.
"""


def zipit(name, items):
    with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in items:
            z.write(path, arc)
        z.writestr("README.txt", README)


def main():
    shutil.copyfile(TRACK / "paper" / "paper3.pdf", OUT / "paper.pdf")
    ds = [(f"data/{n}.json", TRACK / "data" / f"{n}.json") for n in DATA]
    ds += [(n, TRACK / n) for n in PREREGS]
    ds += [(n, TRACK / n) for n in ("TILINGS_RESULTS.md",)]
    zipit("dataset.zip", ds)
    cs = [(f"scripts/{n}", TRACK / n) for n in SCRIPTS]
    cs += [("paper/" + n, TRACK / "paper" / n) for n in ("make_paper3.py", "paper3.tex", "tables_p3.tex")]
    cs += [("LICENSE-MIT", TRACK / "release" / "LICENSE-MIT")]
    cs += [("lean/dtn_offsets/" + n, REPO / "lean" / "dtn_offsets" / n) for n in LEAN]
    zipit("code.zip", cs)
    for f in sorted(OUT.iterdir()):
        print(f.name, f.stat().st_size, hashlib.md5(f.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
