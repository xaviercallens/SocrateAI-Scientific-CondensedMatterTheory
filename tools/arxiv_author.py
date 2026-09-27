#!/usr/bin/env python3
"""List an author's arXiv papers, with categories, as JSON and a table.

Used to ground author-focused reviews (e.g. Shinsei Ryu) in the real record
instead of memory. Author names on arXiv are ambiguous; pass --require-coauthor
or inspect the output before treating a row as the author's.

Usage:
    python3 tools/arxiv_author.py "Ryu_Shinsei" --max 400 --out docs/assets/ryu_arxiv.json
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "http://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"
UA = "SocrateAI-CondensedMatterTheory/1.0 (author survey)"


def fetch(author: str, start: int, size: int) -> list[dict]:
    query = urllib.parse.urlencode({
        "search_query": f"au:{author}",
        "start": start,
        "max_results": size,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=90) as response:
        root = ET.fromstring(response.read())
    rows = []
    for entry in root.findall(f"{ATOM}entry"):
        raw = entry.findtext(f"{ATOM}id", "").split("/abs/", 1)[-1]
        arxiv_id = re.sub(r"v\d+$", "", raw)
        primary = entry.find(f"{ARX}primary_category")
        rows.append({
            "arxiv_id": arxiv_id,
            "title": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}title", "")).strip(),
            "year": entry.findtext(f"{ATOM}published", "")[:4],
            "authors": [a.findtext(f"{ATOM}name", "") for a in entry.findall(f"{ATOM}author")],
            "primary": primary.get("term") if primary is not None else "",
            "abstract": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}summary", "")).strip(),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("author")
    parser.add_argument("--max", type=int, default=400)
    parser.add_argument("--full-name", default="Shinsei Ryu",
                        help="exact author string required in the author list")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    rows: list[dict] = []
    for start in range(0, args.max, 100):
        batch = fetch(args.author, start, 100)
        rows += batch
        if len(batch) < 100:
            break
        time.sleep(3.1)

    # Disambiguation: keep rows whose author list contains the full name.
    kept = [r for r in rows if any(args.full_name.lower() == a.lower() for a in r["authors"])]
    print(f"fetched {len(rows)}, kept {len(kept)} with exact author '{args.full_name}'")

    by_year: dict[str, int] = {}
    by_cat: dict[str, int] = {}
    for r in kept:
        by_year[r["year"]] = by_year.get(r["year"], 0) + 1
        by_cat[r["primary"]] = by_cat.get(r["primary"], 0) + 1
    print("per year :", dict(sorted(by_year.items())))
    print("per cat  :", dict(sorted(by_cat.items(), key=lambda kv: -kv[1])))
    for r in kept:
        print(f"{r['year']}  {r['arxiv_id']:18} [{r['primary']:18}] {r['title'][:95]}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(kept, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
