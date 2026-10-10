#!/usr/bin/env python3
"""Fetch the AdS/CMT seed corpus from the arXiv API.

Writes, under ``papers/``:
  meta/<slug>.json   full arXiv record (title, authors, abstract, dates, DOI)
  pdf/<slug>.pdf     the PDF, when the download succeeds
  index.json         one row per paper, consumed by ingest_chroma.py

Fails closed on identity: every record's real title must contain the expected
fragment declared in ``seed_papers.py``. A mismatch is reported and the paper is
dropped rather than ingested, because a vector store that silently contains the
wrong paper is worse than one that is missing it.

Usage:
    python3 corpus/fetch_papers.py [--no-pdf]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seed_papers import SEED_PAPERS  # noqa: E402

ARXIV_API = "http://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"
USER_AGENT = "SocrateAI-CondensedMatterTheory/1.0 (literature review; mailto:noreply@example.org)"

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"


def slugify(arxiv_id: str) -> str:
    """`hep-th/9711200` -> `hep-th_9711200`; safe as a filename and a Chroma id."""
    return arxiv_id.replace("/", "_")


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch_batch(arxiv_ids: list[str]) -> dict[str, dict]:
    """One API call for a batch of ids. Returns {requested_id: record}."""
    query = urllib.parse.urlencode(
        {"id_list": ",".join(arxiv_ids), "max_results": len(arxiv_ids)}
    )
    request = urllib.request.Request(
        f"{ARXIV_API}?{query}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        root = ET.fromstring(response.read())

    records: dict[str, dict] = {}
    for entry in root.findall(f"{ATOM}entry"):
        raw_id = entry.findtext(f"{ATOM}id", "")
        # http://arxiv.org/abs/hep-th/9711200v3 -> hep-th/9711200, v3
        tail = raw_id.split("/abs/", 1)[-1]
        version_match = re.search(r"v(\d+)$", tail)
        version = version_match.group(0) if version_match else ""
        canonical = tail[: -len(version)] if version else tail

        published = entry.findtext(f"{ATOM}published", "")
        records[canonical] = {
            "arxiv_id": canonical,
            "version": version,
            "title": normalise(entry.findtext(f"{ATOM}title", "")),
            "abstract": normalise(entry.findtext(f"{ATOM}summary", "")),
            "authors": [
                normalise(a.findtext(f"{ATOM}name", ""))
                for a in entry.findall(f"{ATOM}author")
            ],
            "published": published,
            "updated": entry.findtext(f"{ATOM}updated", ""),
            "year": published[:4],
            "primary_category": (
                entry.find(f"{ARX}primary_category").get("term")
                if entry.find(f"{ARX}primary_category") is not None
                else ""
            ),
            "categories": [c.get("term") for c in entry.findall(f"{ATOM}category")],
            "doi": entry.findtext(f"{ARX}doi", "") or "",
            "journal_ref": entry.findtext(f"{ARX}journal_ref", "") or "",
            "abs_url": f"https://arxiv.org/abs/{canonical}",
            "pdf_url": f"https://arxiv.org/pdf/{canonical}",
        }
    return records


def download_pdf(record: dict, destination: Path) -> bool:
    if destination.exists() and destination.stat().st_size > 10_000:
        return True
    request = urllib.request.Request(
        record["pdf_url"], headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
    except Exception as exc:  # noqa: BLE001 - report and continue; PDFs are optional
        print(f"    ! pdf failed {record['arxiv_id']}: {exc}")
        return False
    # A captcha or error page is HTML, not a PDF. Do not store it as one.
    if not payload.startswith(b"%PDF"):
        print(f"    ! pdf not a PDF for {record['arxiv_id']} ({len(payload)} bytes)")
        return False
    destination.write_bytes(payload)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-pdf", action="store_true", help="metadata only")
    parser.add_argument("--ids", default="", help="comma-separated arXiv ids: fetch only these and MERGE them into papers/index.json")
    args = parser.parse_args()

    (PAPERS / "meta").mkdir(parents=True, exist_ok=True)
    (PAPERS / "pdf").mkdir(parents=True, exist_ok=True)

    selected = {x.strip() for x in args.ids.split(",") if x.strip()}
    seeds = [t for t in SEED_PAPERS if not selected or t[0] in selected]
    if selected and len(seeds) != len(selected):
        raise SystemExit("unknown ids: " + ", ".join(sorted(selected - {t[0] for t in seeds})))
    expected = {pid: (pillar, fragment) for pid, pillar, fragment in seeds}
    ids = [pid for pid, _, _ in seeds]

    fetched: dict[str, dict] = {}
    for start in range(0, len(ids), 10):
        batch = ids[start : start + 10]
        print(f"  fetching {start + 1}-{start + len(batch)} of {len(ids)} ...")
        fetched.update(fetch_batch(batch))
        time.sleep(3.1)  # arXiv asks for >=3s between API calls

    index: list[dict] = []
    missing: list[str] = []
    mismatched: list[str] = []

    for arxiv_id in ids:
        record = fetched.get(arxiv_id)
        if record is None:
            missing.append(arxiv_id)
            continue

        pillar, fragment = expected[arxiv_id]
        if fragment.lower() not in record["title"].lower():
            mismatched.append(f"{arxiv_id}: expected ~{fragment!r}, got {record['title']!r}")
            continue

        record["pillar"] = pillar
        slug = slugify(arxiv_id)
        record["slug"] = slug

        if not args.no_pdf:
            record["pdf_local"] = (
                f"papers/pdf/{slug}.pdf"
                if download_pdf(record, PAPERS / "pdf" / f"{slug}.pdf")
                else ""
            )
            time.sleep(1.0)
        else:
            record["pdf_local"] = ""

        (PAPERS / "meta" / f"{slug}.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        index.append(record)
        print(f"  ok  [{pillar:10}] {arxiv_id:20} {record['title'][:62]}")

    if selected and (PAPERS / "index.json").is_file():
        # partial run: merge into the existing index instead of overwriting it
        old = json.loads((PAPERS / "index.json").read_text(encoding="utf-8"))
        keep = [r for r in old if r["arxiv_id"] not in {x["arxiv_id"] for x in index}]
        index = keep + index
    (PAPERS / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n  indexed : {len(index)} / {len(ids)}")
    print(f"  pdfs    : {sum(1 for r in index if r['pdf_local'])}")
    if missing:
        print(f"  MISSING ({len(missing)}): {', '.join(missing)}")
    for line in mismatched:
        print(f"  MISMATCH {line}")
    return 0 if not (missing or mismatched) else 1


if __name__ == "__main__":
    raise SystemExit(main())
