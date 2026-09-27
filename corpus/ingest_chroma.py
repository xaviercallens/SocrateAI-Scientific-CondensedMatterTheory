#!/usr/bin/env python3
"""Ingest the AdS/CMT corpus into AutoevolveAI (ANSE)'s Chroma store.

Design decisions, and why:

* **Embedding function.** ANSE ships two. `chroma_rag.FastDeterministicEmbeddingFunction`
  builds 384-d vectors from md5 over character n-grams; ANSE's own
  `anse/memory/ollama_embeddings.py` documents that nearest neighbours in that
  space are hash collisions, not related meanings, and that it must never back
  anything presented as semantic search. So this script uses
  `OllamaEmbeddingFunction` (`qwen3-embedding:0.6b`, 1024-d, verified live on
  this host) and imports it from ANSE rather than copying it, so the two stay
  on one definition.

* **Fail closed.** If Ollama is unreachable the script aborts. It never falls
  back to the hash embedder, because a collection that mixes the two is
  unrecoverable: the vectors are the same object shape and carry no marker.

* **Its own collection.** The papers go into `adscmt_literature`, not into an
  existing collection. Chroma pins a dimension per collection, and the live
  store's `phase1_traces` is 4096-d; writing 1024-d vectors there would fail,
  and mixing corpora would pollute ANSE's existing retrieval.

* **Deterministic ids.** `<slug>::<kind>::<n>` with `upsert`, so re-running
  re-indexes in place instead of duplicating.

Usage:
    python3 corpus/ingest_chroma.py                    # default ANSE store
    python3 corpus/ingest_chroma.py --dry-run          # chunk only, no writes
    CHROMA_PATH=/some/where python3 corpus/ingest_chroma.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"

DEFAULT_CHROMA_PATH = os.environ.get(
    "CHROMA_PATH", str(Path.home() / "AutoevolveAI" / "data" / "chroma")
)
DEFAULT_ANSE_ROOT = os.environ.get("ANSE_ROOT", str(Path.home() / "AutoevolveAI"))
COLLECTION = os.environ.get("ADSCMT_COLLECTION", "adscmt_literature")

CHUNK_CHARS = 1800
CHUNK_OVERLAP = 250
MAX_BODY_CHUNKS = 40  # per paper; reviews run to hundreds of pages


def load_anse_embedding_function():
    """Import ANSE's OllamaEmbeddingFunction from the sibling checkout.

    Loaded by file path rather than by package import: `anse/__init__.py` pulls
    in the wider harness (redis, chromadb-in-venv, torch), none of which this
    script needs. The module itself depends only on httpx.
    """
    module_path = Path(DEFAULT_ANSE_ROOT) / "anse" / "memory" / "ollama_embeddings.py"
    if not module_path.is_file():
        raise SystemExit(
            f"ANSE embedding module not found at {module_path}.\n"
            f"Set ANSE_ROOT to the AutoevolveAI checkout."
        )
    spec = importlib.util.spec_from_file_location("anse_ollama_embeddings", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.OllamaEmbeddingFunction


def clean(text: str) -> str:
    """Collapse the whitespace damage that PDF text extraction leaves behind."""
    text = text.replace("\x00", " ")
    text = re.sub(r"-\n(?=[a-z])", "", text)  # de-hyphenate line-broken words
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(pdf_path: Path, max_pages: int = 60) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        reader = PdfReader(str(pdf_path))
        pages = [(p.extract_text() or "") for p in reader.pages[:max_pages]]
        return clean("\n\n".join(pages))
    except Exception as exc:  # noqa: BLE001 - a broken PDF must not stop the run
        print(f"    ! pdf text extraction failed for {pdf_path.name}: {exc}")
        return ""


def chunk(text: str, size: int = CHUNK_CHARS, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Sliding window on paragraph-ish boundaries, never emitting empty chunks.

    Empty chunks matter: ANSE's embedding function rejects a whitespace-only
    string for the whole batch, so they are filtered here rather than at the
    network boundary.
    """
    chunks: list[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + size, length)
        if end < length:
            window = text.rfind("\n\n", start + size // 2, end)
            if window == -1:
                window = text.rfind(". ", start + size // 2, end)
            if window != -1:
                end = window + 1
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= length:
            break
        start = max(end - overlap, start + 1)
    return chunks


def build_records(papers: list[dict], use_fulltext: bool) -> tuple[list, list, list]:
    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict] = []

    for paper in papers:
        base_meta = {
            "arxiv_id": paper["arxiv_id"],
            "slug": paper["slug"],
            "title": paper["title"],
            "authors": ", ".join(paper["authors"][:8]),
            "year": paper["year"],
            "pillar": paper["pillar"],
            "primary_category": paper.get("primary_category", ""),
            "abs_url": paper["abs_url"],
            "journal_ref": paper.get("journal_ref", ""),
            "doi": paper.get("doi", ""),
            "corpus": "adscmt",
        }

        # The abstract chunk carries full bibliographic context so that a hit on
        # it is self-describing when it lands in an agent's prompt.
        header = (
            f"Title: {paper['title']}\n"
            f"Authors: {', '.join(paper['authors'])} ({paper['year']})\n"
            f"arXiv: {paper['arxiv_id']}  [{paper.get('primary_category', '')}]\n"
            f"Pillar: {paper['pillar']}\n\n"
            f"Abstract:\n{paper['abstract']}"
        )
        ids.append(f"{paper['slug']}::abstract")
        documents.append(header)
        metadatas.append({**base_meta, "kind": "abstract", "chunk": 0})

        if not use_fulltext:
            continue
        pdf_rel = paper.get("pdf_local") or ""
        if not pdf_rel:
            continue
        text = extract_pdf_text(ROOT / pdf_rel)
        if not text:
            continue
        pieces = chunk(text)[:MAX_BODY_CHUNKS]
        for n, piece in enumerate(pieces):
            ids.append(f"{paper['slug']}::body::{n}")
            # Prefixing the title keeps a body chunk attributable after retrieval.
            documents.append(f"[{paper['title']} | arXiv:{paper['arxiv_id']}]\n\n{piece}")
            metadatas.append({**base_meta, "kind": "body", "chunk": n})
        print(f"    {paper['arxiv_id']:20} {len(pieces):3d} body chunks")

    return ids, documents, metadatas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chroma-path", default=DEFAULT_CHROMA_PATH)
    parser.add_argument("--collection", default=COLLECTION)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--abstracts-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("ANSE_EMBED_TIMEOUT", "900")),
        help="per-request embedding timeout in seconds",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="skip chunk ids already present in the collection",
    )
    args = parser.parse_args()

    index_path = PAPERS / "index.json"
    if not index_path.is_file():
        raise SystemExit("papers/index.json missing - run corpus/fetch_papers.py first")
    papers = json.loads(index_path.read_text(encoding="utf-8"))
    print(f"corpus: {len(papers)} papers")

    print("chunking ...")
    ids, documents, metadatas = build_records(papers, use_fulltext=not args.abstracts_only)
    print(f"  {len(ids)} chunks total")

    if args.dry_run:
        print("dry run - nothing written")
        return 0

    embedding_cls = load_anse_embedding_function()
    # The host's Ollama serves embeddings slowly and serially (measured: ~33 s
    # cold load, and requests queue behind each other), so ANSE's 120 s default
    # times out mid-run. Raise it rather than lower the work.
    embedder = embedding_cls(timeout_s=args.timeout, max_retries=2)
    probe = embedder.probe()  # raises EmbeddingUnavailableError if Ollama is down
    print(f"embeddings: {probe['model']} @ {probe['host']} -> {probe['dimension']}-d", flush=True)

    import chromadb

    client = chromadb.PersistentClient(path=args.chroma_path)
    collection = client.get_or_create_collection(
        name=args.collection,
        embedding_function=embedder,
        metadata={"hnsw:space": "cosine"},
    )

    if args.resume:
        present = set(collection.get(ids=ids, include=[]).get("ids") or [])
        if present:
            keep = [i for i, cid in enumerate(ids) if cid not in present]
            print(f"resume: {len(present)} chunks already stored, {len(keep)} to go", flush=True)
            ids = [ids[i] for i in keep]
            documents = [documents[i] for i in keep]
            metadatas = [metadatas[i] for i in keep]

    done = 0
    for start in range(0, len(ids), args.batch_size):
        stop = start + args.batch_size
        collection.upsert(
            ids=ids[start:stop],
            documents=documents[start:stop],
            metadatas=metadatas[start:stop],
        )
        done = min(stop, len(ids))
        print(f"  upserted {done}/{len(ids)} (collection={collection.count()})", flush=True)

    print(f"\ncollection '{args.collection}' now holds {collection.count()} chunks")
    print(f"store: {args.chroma_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
