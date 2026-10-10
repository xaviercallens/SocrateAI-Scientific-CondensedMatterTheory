#!/usr/bin/env python3
"""Build the Zenodo bundle for the programme manifesto: release/build/zenodo_manifesto/{paper.pdf, dataset.zip, code.zip}.
Run from anywhere: python3 release/manifesto/export_manifesto.py"""
import hashlib
import shutil
import zipfile
from pathlib import Path

TRACK = Path(__file__).resolve().parents[2]
REPO = TRACK.parents[1]
OUT = TRACK / "release" / "build" / "zenodo_manifesto"
OUT.mkdir(parents=True, exist_ok=True)

DATA = ["depth_ordered_residuals_of_jacobian_columns", "jacobian_column_cloud_homology", "learned_persistence_features_of_jacobian_columns", "learned_persistence_features_g1_stratified"]
PREREGS = [f"PREREGISTRATION_{n}.md" for n in (30, 32, 33)]
SCRIPTS = ["hyperbolic_network.py"]
LEAN = ["DtNOffsets.lean", "GramSchmidtBound.lean", "SSHWinding.lean", "lakefile.lean", "lean-toolchain", "lake-manifest.json", "STATUS.md", "docs/statement_lock.json"]
AX1 = ["PREREGISTRATION_N1_LIMIT.md", "RESULTS_N1_LIMIT.md", "PREREGISTRATION_N1_LIMIT2.md", "RESULTS_N1_LIMIT2.md", "exp_n1_limit.py", "exp_n1_limit2.py", "exp_n1_diag_gates.py", "ssh_exact.py", "ssh_check.py", "evidence/n1_limit.json", "evidence/n1_limit2.json", "evidence/n1_limit_gate_diag.json", "evidence/ssh_exact.json"]
DOCS = ["TOPOLOGY_PROGRAMME.md", "LITERATURE_REVIEW_TDA.md", "LITERATURE_REVIEW_INVERSE.md", "TASK_QUEUE.md"]

README = """Programme manifesto: bundle contents

paper.pdf      the paper (8 pages)
dataset.zip    the stored data behind every table and figure (Track H preregistrations 30, 32, 33 and node N1 of axis 1), results blocks, the programme document, the two literature reviews, the task queue
code.zip       the generator (paper/make_manifesto.py) and LaTeX source, the node N1 scripts and exact harness, the network builder, the Lean 4 project dtn_offsets (three modules, status file, statement lock), the two protocols (tex and pdf)

Reproduce tables and figure from the stored data: python3 paper/make_manifesto.py, then pdflatex manifesto.tex twice. The Lean project builds against Mathlib v4.34.0-rc2 (lakefile.lean points to a local LeanMaster checkout).
Base: doi:10.5281/zenodo.23228685, 10.5281/zenodo.23241463, 10.5281/zenodo.23244556, 10.5281/zenodo.23248393. Code MIT, data and paper CC BY 4.0.
Nothing here concerns holography.
"""


def zipit(name, items):
    with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in items:
            z.write(path, arc)
        z.writestr("README.txt", README)


def main():
    shutil.copyfile(TRACK / "paper" / "manifesto.pdf", OUT / "paper.pdf")
    ds = [(f"data/{n}.json", TRACK / "data" / f"{n}.json") for n in DATA]
    ds += [(n, TRACK / n) for n in PREREGS]
    ds += [(n, TRACK / n) for n in ("TILINGS_RESULTS.md",)]
    ds += [("axis1/" + n, REPO / "experiments" / "axis1_topological_waves" / n) for n in AX1 if n.startswith("evidence") or n.endswith(".md")]
    ds += [("docs/" + n, REPO / "docs" / n) for n in DOCS]
    zipit("dataset.zip", ds)
    cs = [(f"scripts/{n}", TRACK / n) for n in SCRIPTS]
    cs += [("paper/" + n, TRACK / "paper" / n) for n in ("make_manifesto.py", "manifesto.tex", "tables_manifesto.tex")]
    cs += [("LICENSE-MIT", TRACK / "release" / "LICENSE-MIT")]
    cs += [("lean/dtn_offsets/" + n, REPO / "lean" / "dtn_offsets" / n) for n in LEAN]
    cs += [("axis1/" + n, REPO / "experiments" / "axis1_topological_waves" / n) for n in AX1 if n.endswith(".py")]
    cs += [("protocols/" + n, TRACK / "protocols" / n) for n in ("protocol_garage.tex", "protocol_garage.pdf", "protocol_computational.tex", "protocol_computational.pdf")]
    zipit("code.zip", cs)
    for f in sorted(OUT.iterdir()):
        print(f.name, f.stat().st_size, hashlib.md5(f.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
