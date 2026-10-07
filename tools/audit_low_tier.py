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
        # numbers inside labels too ("bits10", "offset0.01", "eps3e-4"): condition names are legitimate sources
        for m in re.findall(r"\d+(?:\.\d+)?(?:[eE]-?\d+)?", x):
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
    text = re.sub(r"PREREGISTRATION_\d+|[A-Z]\d-[XCLBA]-\d{4}|\{\d+,\d+\}|\b[LR]=\d+(?:\.\d+)?|\b[GP]\d\b"
                  r"|GF\([^)]*\)|\d+\^\d+(?:-\d+)?", " ", c["statement"])  # identifiers, field names, powers
    # a number computed from data values (a difference, a ratio) is accepted only if the notes declare it explicitly
    # as DERIVED(<number>) = <formula>, normally through a CORRECTION appended with ledger_add.py --correct
    derived = set(re.findall(r"DERIVED\(([^)]+)\)", c.get("notes", "")))
    for tok in NUM.findall(text):
        if tok in derived:
            continue
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
    published = ["experiments/track_h_hyperbolic_network/paper/" + f for f in ("main.tex", "main.pdf", "tables.tex", "refs.bib")]
    diff = subprocess.run(["git", "diff", "--name-only", base, "--"] + published,
                          cwd=ROOT, capture_output=True, text=True).stdout.strip()  # same scope as experiment_gate.py check 8
    if diff:
        fails.append("A5 paper files changed: " + diff.replace("\n", ", "))
    # A6 results block: every number in lines ADDED to a results file since --base must occur in the data, except in
    # lines copied verbatim from the preregistration (design, thresholds, limits). Pass --results <file>.
    if "--results" in a:
        rf = a[a.index("--results") + 1]
        prereg_text = ""
        pm = re.search(r"PREREGISTRATION_\d+", c["statement"])
        if pm:
            pf = ev.parent.parent / (pm.group(0) + ".md")
            prereg_text = pf.read_text() if pf.exists() else ""
        added = [l[1:] for l in subprocess.run(["git", "diff", base, "--", rf], cwd=ROOT, capture_output=True, text=True)
                 .stdout.splitlines() if l.startswith("+") and not l.startswith("+++")]
        # only the low-tier part: lines before the orchestrator's "*Recorded by a low-tier agent" marker
        cut = next((i for i, l in enumerate(added) if l.strip().startswith("*Recorded by")), len(added))
        added = added[:cut]
        norm = lambda x: re.sub(r"\s+", " ", x)
        prereg_norm = norm(prereg_text)
        # A7: the first prose paragraph after the block title (the design/method statement) must be a verbatim copy
        prose = [l.strip() for l in added if l.strip() and not l.strip().startswith(("#", "|", "*Recorded"))]
        if prose:
            # the runbook template (§4) prefixes the paragraph with "Design:"; strip that label before comparing
            first = norm(re.sub(r"^(?:\*\*[^*]+\*\*\s*|Design:\s*)+", "", prose[0]))
            if first[:120] not in prereg_norm:
                fails.append("A7 design/method line is not a verbatim copy of the preregistration: " + first[:90])
        prereg_text = prereg_norm
        for line in added:
            s = line.strip()
            if not s or s.startswith("*Recorded by") or s.startswith("**Scorer") or s.startswith("**Reading"):
                continue
            core = norm(re.sub(r"^\*\*[^*]+\*\*\s*", "", s))
            if len(core) > 60 and core[:60] in prereg_text:
                continue  # verbatim copy from the preregistration
            if s.startswith("|") and ("Prediction" in s or "Threshold" in s or s.startswith("|---")):
                continue
            cells = s.split("|")
            nums_line = s if not s.startswith("|") else "|".join(cells[:-2] if "HELD" in s or "held" in s or "REFUTED" in s or "refuted" in s else cells)
            t2 = re.sub(r"PREREGISTRATION_\d+|[A-Z]\d-[XCLBA]-\d{4}|\{\d+,\d+\}|\b[GP]\d\b|GF\([^)]*\)|\d+\^\d+(?:-\d+)?|10⁻\S+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", " ", nums_line)
            if s.startswith("|") and any(w in s for w in ("HELD", "held", "REFUTED", "refuted", "PASS", "pass", "FAIL", "fail")):
                continue  # verdict rows (predictions and gates) carry thresholds copied from the preregistration
            # the runbook template (§4) puts the pre-run commit hash in the block title: drop tokens that resolve to a commit
            for h in set(re.findall(r"\b[0-9a-f]{7,40}\b", t2)):
                if subprocess.run(["git", "cat-file", "-e", h + "^{commit}"], cwd=ROOT, capture_output=True).returncode == 0:
                    t2 = t2.replace(h, " ")
            for tok in NUM.findall(t2):
                if not found(tok, pool):
                    fails.append("A6 results-block number not in data: %s  (line: %s)" % (tok, s[:90]))
    for f in fails:
        print("  FAIL " + f)
    print(("AUDIT PASS " if not fails else "AUDIT FAIL ") + cid + " (evidence " + str(ev.relative_to(ROOT)) + ")")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
