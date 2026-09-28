#!/usr/bin/env python3
"""Create a Zenodo DRAFT deposition for the preprint, data and code.

This script NEVER publishes. A Zenodo DOI is permanent once published, so
publication is a separate, deliberate click on the printed draft URL after
you have reviewed it.

  export ZENODO_TOKEN=...            # personal token, scopes deposit:write
  python3 release/export.py
  python3 release/zenodo_draft.py [--sandbox]

--sandbox uses sandbox.zenodo.org (needs a sandbox token) for a dry run.
Metadata is in zenodo_metadata.json next to this file; review it first.
"""
import argparse
import json
import os
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build" / "zenodo"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sandbox", action="store_true")
    a = ap.parse_args()
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        raise SystemExit("set ZENODO_TOKEN")
    base = "https://sandbox.zenodo.org" if a.sandbox else "https://zenodo.org"
    files = [BUILD / "paper.pdf", BUILD / "dataset.zip", BUILD / "code.zip"]
    missing = [str(f) for f in files if not f.exists()]
    if missing:
        raise SystemExit(f"missing {missing}; run release/export.py first")
    meta = json.loads((HERE / "zenodo_metadata.json").read_text())
    h = {"Authorization": f"Bearer {token}"}

    r = requests.post(f"{base}/api/deposit/depositions", headers=h, json={})
    r.raise_for_status()
    dep = r.json()
    bucket = dep["links"]["bucket"]
    for f in files:
        with open(f, "rb") as fp:
            u = requests.put(f"{bucket}/{f.name}", data=fp, headers=h)
        u.raise_for_status()
        print("uploaded", f.name)
    r = requests.put(f"{base}/api/deposit/depositions/{dep['id']}", headers=h, json={"metadata": meta})
    r.raise_for_status()
    dep = r.json()
    print("\nDRAFT created (not published).")
    print("reserved DOI :", dep["metadata"].get("prereserve_doi", {}).get("doi", "(n/a)"))
    print("review/edit  :", dep["links"]["html"])
    print("Publish only after review, from that page. This script does not publish.")


if __name__ == "__main__":
    main()
