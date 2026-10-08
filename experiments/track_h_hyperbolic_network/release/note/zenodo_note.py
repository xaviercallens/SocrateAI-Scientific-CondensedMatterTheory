#!/usr/bin/env python3
"""Zenodo steps for the strip-rate paper (a NEW record, not a version of the v1.x record).

  python3 release/note/zenodo_note.py draft            # create a DRAFT with the three files and the metadata; never publishes
  python3 release/note/zenodo_note.py publish <id>     # verify MD5 and metadata against the local build, then PUBLISH (irreversible)
  python3 release/note/zenodo_note.py verify <id>      # anonymous check of the public record

The token is read from the environment (ZENODO_TOKEN) or from ~/.token_workflow_token (lines NAME=value or export NAME="value");
its value is never printed.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / "build" / "zenodo_note"
BASE = "https://zenodo.org"
FILES = ["paper.pdf", "dataset.zip", "code.zip"]


def token():
    t = os.environ.get("ZENODO_TOKEN")
    if t:
        return t
    f = Path.home() / ".token_workflow_token"
    for line in f.read_text().splitlines():
        m = re.match(r'\s*(?:export\s+)?ZENODO_TOKEN\s*=\s*"?([^"\s]+)"?', line)
        if m:
            return m.group(1)
    raise SystemExit("ZENODO_TOKEN not found")


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def draft():
    h = {"Authorization": f"Bearer {token()}"}
    meta = json.loads((HERE / "zenodo_metadata_note.json").read_text())
    r = requests.post(f"{BASE}/api/deposit/depositions", headers=h, json={})
    r.raise_for_status()
    dep = r.json()
    for name in FILES:
        with open(BUILD / name, "rb") as fp:
            requests.put(f"{dep['links']['bucket']}/{name}", data=fp, headers=h).raise_for_status()
        print("uploaded", name)
    r = requests.put(f"{BASE}/api/deposit/depositions/{dep['id']}", headers=h, json={"metadata": meta})
    r.raise_for_status()
    dep = r.json()
    print("DRAFT created (not published). id:", dep["id"])
    print("reserved DOI:", dep["metadata"].get("prereserve_doi", {}).get("doi"))
    print("review:", dep["links"]["html"])


def publish(dep_id):
    h = {"Authorization": f"Bearer {token()}"}
    dep = requests.get(f"{BASE}/api/deposition/depositions/{dep_id}".replace("/api/deposition/", "/api/deposit/"), headers=h)
    dep.raise_for_status()
    dep = dep.json()
    want = json.loads((HERE / "zenodo_metadata_note.json").read_text())
    problems = []
    if dep.get("submitted"):
        problems.append("already published")
    remote = {f["filename"]: f["checksum"].split(":")[-1] for f in dep.get("files", [])}
    local = {n: md5(BUILD / n) for n in FILES}
    if set(remote) != set(local):
        problems.append(f"file set differs: remote={sorted(remote)}")
    for n in sorted(set(remote) & set(local)):
        ok = remote[n] == local[n]
        print(f"  {n}: md5 {'matches' if ok else 'DIFFERS'}")
        if not ok:
            problems.append(f"{n} checksum differs")
    m = dep.get("metadata", {})
    if m.get("title") != want["title"]:
        problems.append("title differs")
    lic = m.get("license")
    lic = lic.get("id") if isinstance(lic, dict) else lic
    if str(lic).lower() != want["license"]:
        problems.append(f"license {lic}")
    rel_r = {x["identifier"] for x in m.get("related_identifiers", [])}
    rel_w = {x["identifier"] for x in want["related_identifiers"]}
    if rel_w - rel_r:
        problems.append(f"missing related identifiers {sorted(rel_w - rel_r)}")
    if problems:
        print("NOT PUBLISHED:", *problems, sep="\n  - ")
        return 1
    r = requests.post(f"{BASE}/api/deposit/depositions/{dep_id}/actions/publish", headers=h)
    r.raise_for_status()
    out = r.json()
    print("PUBLISHED. DOI:", out.get("doi"), "record:", out.get("links", {}).get("record_html"), "concept:", out.get("conceptdoi"))
    return 0


def verify(dep_id):
    r = requests.get(f"{BASE}/api/records/{dep_id}")
    r.raise_for_status()
    j = r.json()
    print("title:", j["metadata"]["title"])
    print("doi:", j.get("doi"), "| access:", j["metadata"].get("access_right"), "| version:", j["metadata"].get("version"))
    for f in j.get("files", []):
        print(" ", f["key"], f.get("checksum"))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "draft":
        draft()
    elif cmd == "publish" and len(sys.argv) == 3:
        sys.exit(publish(sys.argv[2]))
    elif cmd == "verify" and len(sys.argv) == 3:
        sys.exit(verify(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
