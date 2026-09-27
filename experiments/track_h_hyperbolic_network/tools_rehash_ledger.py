#!/usr/bin/env python3
"""Refresh ledger evidence digests for claims whose evidence is a data file here.

Usage: tools_rehash_ledger.py CLAIM_ID=data_file.json [...]
Records the old digest in the claim's notes so the change stays visible.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def main():
    want = dict(a.split("=", 1) for a in sys.argv[1:])
    d = json.loads(LEDGER.read_text())
    for c in d["claims"]:
        if c["id"] in want:
            new = "sha256:" + hashlib.sha256((DATA / want[c["id"]]).read_bytes()).hexdigest()
            if new != c["evidence"]:
                c["notes"] = (c.get("notes") or "") + f" [evidence re-hashed: {want[c['id']]} regenerated with an added field; previous digest {c['evidence'][:19]}...]"
                c["evidence"] = new
                print("rehashed", c["id"])
    LEDGER.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
