#!/usr/bin/env python3
"""PUBLISH an existing Zenodo draft, after verifying it against the local build.

Publishing is irreversible: the DOI becomes permanent and the files are frozen.
Checks, all required before the publish call:
  - the deposition is still an unpublished draft
  - its files are exactly paper.pdf, dataset.zip, code.zip and each MD5 matches
    release/build/zenodo/<file>
  - title, license and related identifiers match zenodo_metadata.json

  ZENODO_TOKEN=... python3 release/zenodo_publish.py <deposition_id>
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build" / "zenodo"
BASE = "https://zenodo.org"


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: zenodo_publish.py <deposition_id>")
    dep_id = sys.argv[1]
    token = os.environ.get("ZENODO_TOKEN") or sys.exit("set ZENODO_TOKEN")
    h = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/api/deposit/depositions/{dep_id}", headers=h)
    r.raise_for_status()
    dep = r.json()
    want = json.loads((HERE / "zenodo_metadata.json").read_text())
    problems = []

    if dep.get("submitted"):
        problems.append("deposition is already published")
    remote = {f["filename"]: f["checksum"].split(":")[-1] for f in dep.get("files", [])}
    local = {p.name: md5(p) for p in BUILD.iterdir() if p.is_file()}
    if set(remote) != set(local):
        problems.append(f"file set differs: remote={sorted(remote)} local={sorted(local)}")
    for name in sorted(set(remote) & set(local)):
        ok = remote[name] == local[name]
        print(f"  {name}: md5 {'matches' if ok else 'DIFFERS'}")
        if not ok:
            problems.append(f"{name} checksum differs from release/build/zenodo")
    m = dep.get("metadata", {})
    if m.get("title") != want["title"]:
        problems.append("title differs from zenodo_metadata.json")
    lic = m.get("license")
    lic = lic.get("id") if isinstance(lic, dict) else lic
    if str(lic).lower() != want["license"]:
        problems.append(f"license is {lic}, expected {want['license']}")
    rel_r = {x["identifier"] for x in m.get("related_identifiers", [])}
    rel_w = {x["identifier"] for x in want["related_identifiers"]}
    if rel_w - rel_r:
        problems.append(f"missing related identifiers: {sorted(rel_w - rel_r)}")
    print(f"  title: {m.get('title')}")
    print(f"  creators: {[c.get('name') for c in m.get('creators', [])]}")
    print(f"  license: {lic}; version: {m.get('version')}; related identifiers: {len(rel_r)}")

    if problems:
        print("NOT PUBLISHED:")
        for p in problems:
            print("  -", p)
        return 1

    r = requests.post(f"{BASE}/api/deposit/depositions/{dep_id}/actions/publish", headers=h)
    r.raise_for_status()
    out = r.json()
    print("\nPUBLISHED.")
    print("DOI        :", out.get("doi"))
    print("record     :", out.get("links", {}).get("record_html") or out.get("links", {}).get("html"))
    print("concept DOI:", out.get("conceptdoi"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
