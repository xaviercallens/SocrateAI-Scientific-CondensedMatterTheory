#!/usr/bin/env python3
"""Build main.pdf: make_assets -> pdflatex -> bibtex -> pdflatex x2.

Exits non-zero if any step fails or the final log has undefined references
or citations. Usage: python3 paper/build.py
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(cmd):
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    print(f"$ {' '.join(cmd)} -> exit {r.returncode}")
    return r


def main() -> int:
    if run([sys.executable, "make_assets.py"]).returncode:
        return 1
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    b = run(["bibtex", "main"])
    if b.returncode:
        print(b.stdout[-2000:])
        return 1
    for _ in range(2):
        r = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    if r.returncode:
        print(r.stdout[-3000:])
        return 1
    log = (HERE / "main.log").read_text(errors="replace")
    bad = re.findall(r".*(?:undefined|Undefined).*", log)
    warn = [l for l in log.splitlines() if "Overfull" in l]
    print(f"undefined refs/cites: {len(bad)}; overfull boxes: {len(warn)}")
    for l in bad[:20] + warn[:20]:
        print("  ", l)
    pages = re.search(r"Output written on main.pdf \((\d+) pages", log)
    print("pages:", pages.group(1) if pages else "?")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
