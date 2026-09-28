#!/usr/bin/env python3
"""Create a NEW VERSION draft of a published Zenodo record (v1.0 is frozen; a
correction is always a new version under the same concept DOI).

  ZENODO_TOKEN=... python3 release/zenodo_new_version.py <published_deposition_id> <version>

Steps: newversion action -> latest draft -> delete the inherited files ->
upload release/build/zenodo/{paper.pdf,dataset.zip,code.zip} -> set metadata
from zenodo_metadata.json with the given version string -> print the draft
URL and reserved DOI. It never publishes; use zenodo_publish.py <draft_id>,
which verifies MD5s and metadata first.
"""
import json
import os
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build" / "zenodo"
BASE = "https://zenodo.org"


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: zenodo_new_version.py <published_deposition_id> <version>")
    dep_id, version = sys.argv[1], sys.argv[2]
    token = os.environ.get("ZENODO_TOKEN") or sys.exit("set ZENODO_TOKEN")
    h = {"Authorization": f"Bearer {token}"}
    files = [BUILD / "paper.pdf", BUILD / "dataset.zip", BUILD / "code.zip"]
    missing = [str(f) for f in files if not f.exists()]
    if missing:
        raise SystemExit(f"missing {missing}; run release/export.py first")

    r = requests.post(f"{BASE}/api/deposit/depositions/{dep_id}/actions/newversion", headers=h)
    r.raise_for_status()
    latest = r.json()["links"]["latest_draft"]
    draft = requests.get(latest, headers=h); draft.raise_for_status(); draft = draft.json()
    did = draft["id"]
    print("new-version draft id:", did)
    for f in draft.get("files", []):
        d = requests.delete(f"{BASE}/api/deposit/depositions/{did}/files/{f['id']}", headers=h)
        d.raise_for_status(); print("removed inherited", f["filename"])
    bucket = draft["links"]["bucket"]
    for f in files:
        with open(f, "rb") as fp:
            u = requests.put(f"{bucket}/{f.name}", data=fp, headers=h)
        u.raise_for_status(); print("uploaded", f.name)
    meta = json.loads((HERE / "zenodo_metadata.json").read_text())
    meta["version"] = version
    meta.pop("prereserve_doi", None)
    r = requests.put(f"{BASE}/api/deposit/depositions/{did}", headers=h, json={"metadata": meta})
    r.raise_for_status()
    dep = r.json()
    print("\nDRAFT (new version, not published)")
    print("version     :", version)
    print("reserved DOI:", dep["metadata"].get("prereserve_doi", {}).get("doi", "(n/a)"))
    print("review/edit :", dep["links"]["html"])
    print(f"publish with: bash release/publish.sh publish {did}")


if __name__ == "__main__":
    main()
