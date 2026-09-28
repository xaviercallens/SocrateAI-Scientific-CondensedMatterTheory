#!/usr/bin/env python3
"""Audit a claim recorded by a low-tier agent (run by a higher tier before accepting the result).

  python3 tools/audit_low_tier.py H3-X-0008 [--base <git rev>]

Checks
  A1 every number written in the claim statement occurs in the evidence data file (rounded to the precision written)
  A2 each 'Pn HELD/REFUTED' and 'Gn true/false' in the statement agrees with data["verdicts"] written by score()
  A3 the evidence digest in the ledger is the sha256 of the evidence file as it is now
  A4 the ledger change since --base (default HEAD~1) is append-only: no existing claim's statement changed or vanished
  A5 nothing under experiments/track_h_hyperbolic_network/paper/ changed since --base
Exit 0 only if all pass. Prints the offending item for each failure.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?:[eE]-?\d+)?")


def flat_numbers(x, out):
    if isinstance(x, bool) or x is None:
        return
    if isinstance(x, (int, float)):
        out.append(float(x)); return
    if isinstance(x, str):
        for m in NUM.findall(x):
            out.append(float(m))
        return
    if isinstance(x, dict):
        for k, v in x.items():
            flat_numbers(k, out); flat_numbers(v, out)
    elif isinstance(x, list):
        for v in x:
            flat_numbers(v, out)


def found(tok, pool):
    v = float(tok)
    dec = len(tok.split(".")[1].split("e")[0].split("E")[0]) if "." in tok else 0
    tol = 0.5 * 10 ** (-dec) if "e" not in tok.lower() else abs(v) * 0.05
    return any(abs(p - v) <= tol + 1e-12 for p in pool)


def main():
    a = sys.argv[1:]
    cid = a[0]
    base = a[a.index("--base") + 1] if "--base" in a else "HEAD~1"
    led = json.loads(LEDGER.read_text())
    c = next((x for x in led["claims"] if x["id"] == cid), None)
    if c is None:
        print("no such claim", cid); return 1
    m = re.search(r"\[evidence file: ([^\]]+)\]", c.get("notes", ""))
    if not m:
        print("A0 FAIL: claim has no '[evidence file: ...]' note (was it added with tools/ledger_add.py?)"); return 1
    ev = ROOT / m.group(1)
    data = json.loads(ev.read_text())
    pool = []
    flat_numbers(data, pool)
    fails = []
    # A1 numbers (skip identifiers: preregistration numbers, lattice labels like L=3 / R=10 / {7,3}, ledger ids)
    text = re.sub(r"PREREGISTRATION_\d+|[A-Z]\d-[XCLBA]-\d{4}|\{\d+,\d+\}|\b[LR]=\d+(?:\.\d+)?|\b[GP]\d\b", " ", c["statement"])
    for tok in NUM.findall(text):
        if not found(tok, pool):
            fails.append("A1 number not in data: " + tok)
    # A2 verdict words
    ver = data.get("verdicts", {})
    for key, word in re.findall(r"\b([GP]\d)\b[^A-Za-z]{0,3}(HELD|REFUTED|true|false|True|False)", c["statement"]):
        if key in ver and isinstance(ver[key], bool):
            said = word in ("HELD", "true", "True")
            if said != ver[key]:
                fails.append("A2 %s written %s but score() gave %s" % (key, word, ver[key]))
    # A3 digest
    if c["evidence"] != "sha256:" + hashlib.sha256(ev.read_bytes()).hexdigest():
        fails.append("A3 evidence digest does not match the current file")
    # A4 append-only
    try:
        old = json.loads(subprocess.run(["git", "show", base + ":docs/elenchus/ledger.json"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
        new = {x["id"]: x for x in led["claims"]}
        for x in old["claims"]:
            if x["id"] not in new:
                fails.append("A4 claim removed: " + x["id"])
            elif new[x["id"]]["statement"] != x["statement"]:
                fails.append("A4 statement changed: " + x["id"])
    except subprocess.CalledProcessError:
        fails.append("A4 cannot read ledger at " + base)
    # A5 paper untouched
    diff = subprocess.run(["git", "diff", "--name-only", base, "--", "experiments/track_h_hyperbolic_network/paper/"],
                          cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if diff:
        fails.append("A5 paper files changed: " + diff.replace("\n", ", "))
    for f in fails:
        print("  FAIL " + f)
    print(("AUDIT PASS " if not fails else "AUDIT FAIL ") + cid + " (evidence " + str(ev.relative_to(ROOT)) + ")")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
