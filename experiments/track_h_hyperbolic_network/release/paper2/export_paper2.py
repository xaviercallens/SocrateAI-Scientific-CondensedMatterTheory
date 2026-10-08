#!/usr/bin/env python3
"""Build the Zenodo bundle for paper 2: release/build/zenodo_paper2/{paper.pdf, dataset.zip, code.zip}.
Run from anywhere: python3 release/paper2/export_paper2.py"""
import hashlib
import shutil
import zipfile
from pathlib import Path

TRACK = Path(__file__).resolve().parents[2]
REPO = TRACK.parents[1]
OUT = TRACK / "release" / "build" / "zenodo_paper2"
OUT.mkdir(parents=True, exist_ok=True)

DATA = ["jacobian_column_cloud_homology", "jacobian_column_cloud_homology_firstrun", "jacobian_column_cloud_homology_posthoc",
        "cvode_check_of_the_garage_virtual_bench", "laplace_resolved_jacobian_conditioning", "laplace_link_tail_corrected", "laplace_wide_window_posthoc"]
PREREGS = [f"PREREGISTRATION_{n}.md" for n in (29, 30, 31)]
SCRIPTS = ["exp29_laplace_resolved_jacobian_conditioning.py", "exp30_jacobian_column_cloud_homology.py", "exp30_diag_g2.py", "exp30_diag_powerlaw.py",
           "exp31_cvode_virtual_bench_check.py", "hyperbolic_network.py"]

README = """Paper 2: bundle contents

paper.pdf      the paper (5 pages)
dataset.zip    data/*.json behind every table and figure, preregistrations 29-31, results blocks (TILINGS_RESULTS.md)
code.zip       experiment scripts exp29-exp31, the network builder, the lab virtual bench, the figure/table generator and the LaTeX source

Reproduce tables and figure from the stored data: python3 paper/make_paper2.py, then pdflatex paper2.tex twice.
Companions: doi:10.5281/zenodo.23228685 and doi:10.5281/zenodo.23241463. Code MIT, data and paper CC BY 4.0.
Nothing here concerns holography.
"""


def zipit(name, items):
    with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in items:
            z.write(path, arc)
        z.writestr("README.txt", README)


def main():
    shutil.copyfile(TRACK / "paper" / "paper2.pdf", OUT / "paper.pdf")
    ds = [(f"data/{n}.json", TRACK / "data" / f"{n}.json") for n in DATA]
    ds += [(n, TRACK / n) for n in PREREGS]
    ds += [(n, TRACK / n) for n in ("TILINGS_RESULTS.md",)]
    zipit("dataset.zip", ds)
    cs = [(f"scripts/{n}", TRACK / n) for n in SCRIPTS]
    cs += [("paper/" + n, TRACK / "paper" / n) for n in ("make_paper2.py", "paper2.tex", "tables_p2.tex")]
    cs += [("lab/virtual_bench.py", TRACK / "lab" / "virtual_bench.py"), ("LICENSE-MIT", TRACK / "release" / "LICENSE-MIT")]
    zipit("code.zip", cs)
    for f in sorted(OUT.iterdir()):
        print(f.name, f.stat().st_size, hashlib.md5(f.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
