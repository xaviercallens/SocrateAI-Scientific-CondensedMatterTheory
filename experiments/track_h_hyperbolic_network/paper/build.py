#!/usr/bin/env python3
"""Build a PDF: assets -> pdflatex -> bibtex -> pdflatex x2.

  python3 paper/build.py              # main.tex      (version 1.1, the published record; do not rebuild casually)
  python3 paper/build.py main_v1_2    # main_v1_2.tex (version 1.2 draft, generated from main.tex by make_v12.py)

Exits non-zero if any step fails or the final log has undefined references or citations.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEM = sys.argv[1] if len(sys.argv) > 1 else "main"


def run(cmd):
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    print("$ " + " ".join(cmd) + " -> exit " + str(r.returncode))
    return r


def main() -> int:
    assets = [sys.executable, "make_assets.py"] + ([] if STEM == "main" else ["--v12"])
    if run(assets).returncode:
        return 1
    # `python3 paper/build.py main_v1_2 --final` drops the "draft" labels (for the published v1.2 record)
    if STEM == "main_v1_2" and run([sys.executable, "make_v12.py"] + (["--final"] if "--final" in sys.argv else [])).returncode:
        return 1
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", STEM + ".tex"])
    b = run(["bibtex", STEM])
    if b.returncode:
        print(b.stdout[-2000:])
        return 1
    for _ in range(2):
        r = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", STEM + ".tex"])
    if r.returncode:
        print(r.stdout[-3000:])
        return 1
    log = (HERE / (STEM + ".log")).read_text(errors="replace")
    bad = re.findall(r".*(?:undefined|Undefined).*", log)
    warn = [l for l in log.splitlines() if "Overfull" in l]
    print("undefined refs/cites: " + str(len(bad)) + "; overfull boxes: " + str(len(warn)))
    for l in bad[:20] + warn[:20]:
        print("  ", l)
    pages = re.search(r"Output written on " + re.escape(STEM) + r"\.pdf \((\d+) pages", log)
    print("pages:", pages.group(1) if pages else "?")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
