#!/usr/bin/env python3
"""One command that runs every mechanical check of the research workflow and prints PASS/FAIL per check.
A low-capability agent runs this after every experiment step and must not report success unless it prints
ALL PASS. It never modifies the ledger; it only reads and rebuilds derived artefacts.

  python3 tools/experiment_gate.py            # all checks
  python3 tools/experiment_gate.py --quick    # skip export/check_bundle (slow)

Checks
  1 prereg-before-data: for every entry of experiments/track_h_hyperbolic_network/experiments.json, the first
    commit of the preregistration precedes the first commit of each data file, and the prereg has no 'TODO'
  2 ledger gate (bookkeeping)                              -> 'no findings'
  3 ledger gate with --evidence-dir (strict)               -> only the 5 known legacy digests may be flagged
  4 evidence store rebuild                                 -> 'not recovered' list == the known legacy list
  5 training labels rebuild (build_physics_verdicts.py)    -> runs, count printed
  6 self-tests: hyperbolic_network, hyperbolic_exact, ledger_add, export_session_traces
  7 export + check_bundle (unless --quick)                 -> 'all checks pass'
  8 no uncommitted changes to the published v1.1 artefacts (paper/main.tex, main.pdf, tables.tex)
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "experiments" / "track_h_hyperbolic_network"
GATE = os.environ.get("ELENCHUS_GATE") or next((p for p in (
    Path.home() / "SocrateAI-Scientific-Elenchus" / "tools" / "ledger.py",
    Path.home() / ".claude" / "jobs" / "9fcde7bc" / "tmp" / "elenchus" / "tools" / "ledger.py") if p.is_file()), None)
LEGACY = {"SSH-L-0001", "SSH-C-0001", "POC-X-0001", "POC-X-0002", "H0-X-0001"}
results = []


def sh(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(("  PASS " if ok else "  FAIL ") + name + (("  " + detail) if detail else ""))


def first_commit_time(rel):
    rc, out = sh(["git", "log", "--diff-filter=A", "--format=%ct", "--", rel])
    ts = [int(x) for x in out.split() if x.strip()]
    return min(ts) if ts else None


def main():
    quick = "--quick" in sys.argv
    print("== 1 preregistration committed before data")
    man = json.loads((TRACK / "experiments.json").read_text())
    for prereg, e in man.items():
        p = TRACK / prereg
        todo = "TODO" in p.read_text() if p.exists() else True
        tp = first_commit_time(str(p.relative_to(ROOT)))
        for df in e["data"]:
            td = first_commit_time(str((TRACK / df).relative_to(ROOT)))
            ok = (tp is not None) and (td is None or tp <= td) and not todo
            check(prereg + " -> " + df, ok, "" if ok else ("prereg uncommitted" if tp is None else ("TODO left" if todo else "data committed first")))
    # evidence store FIRST: a newly added claim's blob must be archived before the strict gate can verify it
    print("== 4 evidence store")
    rc, out = sh([sys.executable, str(TRACK / "tools_evidence_store.py")])
    nr = out.strip().splitlines()[-1] if out.strip() else ""
    check("evidence store: not-recovered == legacy", rc == 0 and set(eval(nr.split(":", 1)[1].strip())) == LEGACY if "not recovered" in nr else False, nr)
    print("== 2/3 ledger gate")
    if GATE is None:
        check("ledger gate available", False, "set ELENCHUS_GATE")
    else:
        rc, out = sh([sys.executable, str(GATE), "docs/elenchus/ledger.json"])
        check("ledger gate (bookkeeping)", rc == 0 and "no findings" in out, out.strip().splitlines()[0] if out.strip() else "")
        rc, out = sh([sys.executable, str(GATE), "--evidence-dir", "docs/elenchus/evidence", "docs/elenchus/ledger.json"])
        flagged = {l.split()[2].rstrip(":") for l in out.splitlines() if "LEDGER_EVIDENCE" in l}
        check("strict gate: only legacy digests flagged", flagged <= LEGACY, "flagged: " + ", ".join(sorted(flagged - LEGACY)) if flagged - LEGACY else "")
    print("== 5 training labels")
    rc, out = sh([sys.executable, "tools/build_physics_verdicts.py"])
    check("build_physics_verdicts", rc == 0, out.strip().splitlines()[-1] if out.strip() else "")
    labels = (ROOT / "training" / "physics_predictions.jsonl").read_text()
    for prereg, e in man.items():
        for df in e["data"]:
            p = TRACK / df
            if p.exists() and isinstance(json.loads(p.read_text()).get("verdicts"), dict):
                check("training labels exist for " + prereg, ('"' + prereg + '"') in labels)
    print("== 6 self-tests")
    for cmd in ((sys.executable, str(TRACK / "hyperbolic_network.py"), "--self-test"),
                (sys.executable, str(TRACK / "hyperbolic_exact.py"), "--self-test"),
                (sys.executable, "tools/ledger_add.py", "--self-test"),
                (sys.executable, "tools/test_export_session_traces.py")):
        rc, out = sh(list(cmd))
        check(Path(cmd[1]).name, rc == 0)
    if not quick:
        print("== 7 export + bundle check")
        rc, out = sh([sys.executable, str(TRACK / "release" / "export.py")])
        rc2, out2 = sh([sys.executable, str(TRACK / "release" / "check_bundle.py")])
        check("export + check_bundle", rc == 0 and rc2 == 0 and "all checks pass" in out2)
    print("== 8 published v1.1 artefacts untouched")
    rc, out = sh(["git", "status", "--porcelain", "--", str(TRACK / "paper" / "main.tex"), str(TRACK / "paper" / "main.pdf"),
                  str(TRACK / "paper" / "tables.tex")])
    check("v1.1 artefacts unmodified in the working tree", out.strip() == "")
    n_ok = sum(1 for _, ok in results if ok)
    print("\n" + ("ALL PASS" if n_ok == len(results) else "FAIL") + " (%d/%d)" % (n_ok, len(results)))
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
