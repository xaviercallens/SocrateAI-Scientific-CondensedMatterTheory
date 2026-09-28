#!/usr/bin/env python3
"""Build the content-addressed evidence store docs/elenchus/evidence/<hex>.json
that `ledger.py --evidence-dir` verifies against.

1. H2-L-0001 and H2-C-0001 previously hashed literal strings. They get real JSON
   blobs (the citations with DOIs; the argument text) and their digests are
   replaced, with the change recorded in their notes.
2. Every other claim's digest is looked up among the repository's tracked files
   and data/*.json; a matching file is copied into the store under its digest.
3. A digest that matches no file is NOT papered over: the claim's notes get an
   'EVIDENCE BLOB NOT RECOVERED' remark, and the gate will report it.
Idempotent.
"""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
STORE = ROOT / "docs" / "elenchus" / "evidence"
NOT_RECOVERED = (" [EVIDENCE BLOB NOT RECOVERED: no tracked file hashes to this digest; the gate with "
                 "--evidence-dir reports it. Statement unchanged.]")

BLOBS = {
    "H2-L-0001": {
        "kind": "citation",
        "claim": "lambda_0 > 0 for the {7,3} tiling graph; lambda_0 <= 3 - 2 sqrt 2",
        "sources": [
            {"ref": "J. Dodziuk, Difference equations, isoperimetric inequality and transience of certain random walks, "
                    "Trans. Amer. Math. Soc. 284 (1984) 787-794",
             "used_for": "Cheeger-type bound: positive isoperimetric constant => positive bottom of spectrum"},
            {"ref": "B. Mohar, Isoperimetric inequalities, growth, and the spectrum of graphs, Linear Algebra Appl. 103 "
                    "(1988) 119-131", "doi": "10.1016/0024-3795(88)90224-8",
             "used_for": "same, combinatorial Laplacian of bounded-degree infinite graphs"},
            {"ref": "O. Haggstrom, J. Jonasson, R. Lyons, Explicit isoperimetric constants and phase transitions in the "
                    "random-cluster model, Ann. Probab. 30 (2002) 443-473", "arxiv": "math/0008191",
             "used_for": "explicit positive edge-isoperimetric constants of planar regular tilings with regular duals"},
        ],
        "upper_bound": "the 3-regular tree covers the {7,3} graph; spectral radius of simple random walk is at least "
                       "the tree's 2 sqrt 2 / 3, so lambda_0 = 3 (1 - rho) <= 3 - 2 sqrt 2",
    },
    "H2-C-0001": {
        "kind": "argument",
        "premises": ["H2-B-0001 (interior degree 3; interior of G_L equals G_{L-1}, L<=6)", "H2-L-0001"],
        "argument": [
            "If every interior node has full degree 3, f^T L_ii f = sum over edges of the infinite graph of "
            "(f_a - f_b)^2 for f supported on the interior; so L_ii is the compression of the infinite Laplacian.",
            "Rayleigh quotient: lambda_min(L_ii) = inf over interior-supported f >= inf over finitely supported f = lambda_0.",
            "Nested interiors => lambda_min non-increasing in L; exhaustion (every finitely supported f is eventually "
            "interior-supported) => convergence to lambda_0.",
            "lambda_0 > 0 by H2-L-0001; hence tau = C / lambda_min <= C / lambda_0 uniformly in N.",
        ],
        "scope": "premise certified for L<=6 only; general L argued from the face-incidence boundary definition",
        "written_in": "experiments/track_h_hyperbolic_network/paper/main.tex, Proposition 1",
    },
}


def sha(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def main():
    STORE.mkdir(parents=True, exist_ok=True)
    d = json.loads(LEDGER.read_text())
    by_id = {c["id"]: c for c in d["claims"]}

    for cid, body in BLOBS.items():
        raw = (json.dumps(body, indent=1, sort_keys=True) + "\n").encode()
        dig = sha(raw)
        c = by_id[cid]
        if c["evidence"] != dig:
            c["notes"] = (c.get("notes") or "") + (f" [evidence replaced: previous digest {c['evidence'][:19]}... hashed "
                                                   "a literal string, not a file; now a JSON blob in docs/elenchus/evidence]")
            c["evidence"] = dig
        (STORE / (dig.split(":")[1] + ".json")).write_bytes(raw)

    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    files += [str(p.relative_to(ROOT)) for p in (ROOT / "experiments").rglob("data/*.json")]
    index = {}
    for f in set(files):
        p = ROOT / f
        if p.is_file() and not str(f).startswith("docs/elenchus/evidence/"):
            index.setdefault(sha(p.read_bytes()), f)

    missing = []
    for c in d["claims"]:
        if c["id"] in BLOBS:
            continue
        stored = STORE / (c["evidence"].split(":")[1] + ".json")
        if stored.exists() and sha(stored.read_bytes()) == c["evidence"]:
            # already archived (the live data file may have been regenerated since)
            c["notes"] = (c.get("notes") or "").replace(NOT_RECOVERED, "")
            continue
        src = index.get(c["evidence"])
        if src:
            shutil.copy(ROOT / src, STORE / (c["evidence"].split(":")[1] + ".json"))
            print(f"  {c['id']}: {src}")
        else:
            missing.append(c["id"])
            if "EVIDENCE BLOB NOT RECOVERED" not in (c.get("notes") or ""):
                c["notes"] = (c.get("notes") or "") + NOT_RECOVERED
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    print("not recovered:", missing or "none")


if __name__ == "__main__":
    main()
