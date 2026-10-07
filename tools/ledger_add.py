#!/usr/bin/env python3
"""Add a claim to the Elenchus ledger from a JSON file, or append a correction note to an existing claim.
Replaces the per-experiment tools_add_ledger_N.py scripts: no Python needs to be written per claim.

  python3 tools/ledger_add.py claim.json           # add (idempotent: an existing id is left untouched)
  python3 tools/ledger_add.py --correct H3-X-0003 "CORRECTION (date): ..."   # append to notes, statement unchanged
  python3 tools/ledger_add.py --self-test

claim.json:
  {"id": "H3-X-0008", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0007"],
   "evidence_file": "experiments/track_h_hyperbolic_network/data/foo.json",
   "statement": "PREREGISTRATION_12 ... P1 HELD ...", "notes": "script; LIMITS: ..."}
Rules enforced here (the gate enforces the rest): id matches ^[A-Z0-9]+-[XCLBA]-\\d{4}$ and its letter equals tier;
kind in {numeric, exact_harness, citation, argument, solver_reading}; evidence_file exists and is tracked or under
data/; statement non-empty and mentions HELD/REFUTED/DEVIATION/EXPLORATORY/CORRECTS/RETRACTS/CONFIRMED or an
explicit 'verdict:'; depends_on ids exist. After adding, run tools/experiment_gate.py.
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
KINDS = {"numeric", "exact_harness", "citation", "argument", "solver_reading"}
VERDICT_WORDS = ("HELD", "REFUTED", "DEVIATION", "EXPLORATORY", "CORRECTS", "RETRACTS", "CONFIRMED", "verdict:")


def load(path=LEDGER):
    return json.loads(Path(path).read_text())


def save(d, path=LEDGER):
    Path(path).write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


def validate(c, ledger, root=ROOT):
    errs = []
    m = re.fullmatch(r"[A-Z0-9]+-([XCLBA])-\d{4}", c.get("id", ""))
    if not m:
        errs.append("id must look like H3-X-0008")
    elif m.group(1) != c.get("tier"):
        errs.append("tier letter in id differs from tier")
    if c.get("kind") not in KINDS:
        errs.append("kind must be one of " + ", ".join(sorted(KINDS)))
    ids = {x["id"] for x in ledger["claims"]}
    for dep in c.get("depends_on", []):
        if dep not in ids:
            errs.append("depends_on names an unknown claim: " + dep)
    ev = c.get("evidence_file")
    if not ev or not (root / ev).is_file():
        errs.append("evidence_file missing or not found: " + str(ev))
    st = c.get("statement", "")
    if len(st) < 40:
        errs.append("statement too short")
    elif not any(w in st for w in VERDICT_WORDS):
        errs.append("statement must state a verdict (HELD / REFUTED / DEVIATION / EXPLORATORY / CORRECTS / 'verdict:')")
    return errs


def add(claim_path, ledger_path=LEDGER, root=ROOT):
    c = json.loads(Path(claim_path).read_text())
    d = load(ledger_path)
    errs = validate(c, d, root)
    if errs:
        for e in errs:
            print("  refused:", e)
        return 1
    if c["id"] in {x["id"] for x in d["claims"]}:
        print("  exists, untouched:", c["id"])
        return 0
    raw = (root / c["evidence_file"]).read_bytes()
    rec = {"id": c["id"], "tier": c["tier"], "kind": c["kind"], "depends_on": c.get("depends_on", []),
           "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None,
           "statement": c["statement"], "notes": c.get("notes", "") + " [evidence file: " + c["evidence_file"] + "]"}
    d["claims"].append(rec)
    save(d, ledger_path)
    print("  added", c["id"])
    return 0


def correct(cid, text, ledger_path=LEDGER):
    d = load(ledger_path)
    for x in d["claims"]:
        if x["id"] == cid:
            if text in (x.get("notes") or ""):
                print("  note already present on", cid); return 0
            x["notes"] = (x.get("notes") or "") + " " + text
            save(d, ledger_path); print("  appended note to", cid, "(statement unchanged)"); return 0
    print("  no such claim:", cid); return 1


def fix_uncommitted_deps(cid, deps, ledger_path=LEDGER):
    """Correct depends_on of a claim that has NEVER been committed (absent from the ledger at HEAD). Refuses for any
    committed claim, so the committed ledger stays append-only. Records the correction in the claim's notes."""
    import subprocess
    head = subprocess.run(["git", "show", "HEAD:docs/elenchus/ledger.json"], cwd=ROOT, capture_output=True, text=True)
    if head.returncode == 0 and cid in {x["id"] for x in json.loads(head.stdout)["claims"]}:
        print("  refused: %s is committed; append a correction instead" % cid); return 1
    d = load(ledger_path)
    ids = {x["id"] for x in d["claims"]}
    for dep in deps:
        if dep not in ids:
            print("  refused: unknown dependency " + dep); return 1
    for x in d["claims"]:
        if x["id"] == cid:
            old = x["depends_on"]; x["depends_on"] = deps
            x["notes"] = (x.get("notes") or "") + " [depends_on corrected before commit: %s -> %s]" % (old, deps)
            save(d, ledger_path); print("  fixed depends_on of uncommitted", cid, old, "->", deps); return 0
    print("  no such claim:", cid); return 1


def self_test():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        lp = td / "ledger.json"
        save({"schema_version": 1, "claims": [{"id": "T0-X-0001", "tier": "X", "kind": "numeric", "depends_on": [],
                                               "evidence": "sha256:" + "0" * 64, "audit": None, "statement": "x", "notes": ""}]}, lp)
        ev = td / "ev.json"; ev.write_text("{}")
        good = {"id": "T0-X-0002", "tier": "X", "kind": "numeric", "depends_on": ["T0-X-0001"], "evidence_file": "ev.json",
                "statement": "PREREGISTRATION_99 part A: prediction P1 HELD because the measured value matched.", "notes": "n"}
        bad = dict(good, id="T0-B-0003", tier="X")
        ok = []
        ok.append(("good claim validates", validate(good, load(lp), td) == []))
        errs = validate(dict(good, statement="too short"), load(lp), td); ok.append(("short statement refused", any("short" in e for e in errs)))
        errs = validate(bad, load(lp), td); ok.append(("tier mismatch refused", any("tier letter" in e for e in errs)))
        errs = validate(dict(good, depends_on=["NOPE-X-0001"]), load(lp), td); ok.append(("unknown dependency refused", any("unknown" in e for e in errs)))
        errs = validate(dict(good, evidence_file="missing.json"), load(lp), td); ok.append(("missing evidence refused", any("evidence_file" in e for e in errs)))
        cp = td / "claim.json"; cp.write_text(json.dumps(good))
        r1 = add(cp, lp, td); r2 = add(cp, lp, td)
        ok.append(("add then idempotent", r1 == 0 and r2 == 0 and len(load(lp)["claims"]) == 2))
        ok.append(("digest is of the file", load(lp)["claims"][1]["evidence"] == "sha256:" + hashlib.sha256(b"{}").hexdigest()))
        correct("T0-X-0001", "CORRECTION (test): appended.", lp)
        ok.append(("correction appended, statement unchanged", load(lp)["claims"][0]["statement"] == "x" and "CORRECTION" in load(lp)["claims"][0]["notes"]))
    for name, passed in ok:
        print(("  ok   " if passed else "  FAIL ") + name)
    return 0 if all(p for _, p in ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--self-test":
        sys.exit(self_test())
    if a[0] == "--correct":
        sys.exit(correct(a[1], a[2]))
    if a[0] == "--fix-uncommitted-deps":
        sys.exit(fix_uncommitted_deps(a[1], [x for x in a[2].split(",") if x]))
    sys.exit(add(a[0]))
