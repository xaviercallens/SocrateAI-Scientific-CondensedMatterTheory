#!/usr/bin/env python3
"""MCP server exposing the AdS/CMT literature collection as retrieval tools.

Why this exists instead of the off-the-shelf `chroma-mcp`
---------------------------------------------------------
`chroma-mcp` takes `--client-type persistent --data-dir ...` and would reach
this store fine, but it has no flag for an Ollama embedding function: its
choices are `default`, `cohere`, `openai`, `jina`, `voyageai`, `roboflow`.
The `adscmt_literature` collection is written with `qwen3-embedding:0.6b`
(1024-d), so `chroma-mcp` would embed queries with its 384-d default and
either raise a dimension error or, worse, search a different vector space than
the one the documents live in.

This server queries with the *same* embedding function used at ingestion --
imported from AutoevolveAI (ANSE) rather than reimplemented, so there is a
single definition. It follows the pattern already in ANSE's own `.mcp.json`,
which runs custom Python MCP servers.

Environment:
    CHROMA_PATH        default ~/AutoevolveAI/data/chroma
    ANSE_ROOT          default ~/AutoevolveAI
    ADSCMT_COLLECTION  default adscmt_literature
    OLLAMA_HOST        default http://localhost:11434
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

CHROMA_PATH = os.environ.get(
    "CHROMA_PATH", str(Path.home() / "AutoevolveAI" / "data" / "chroma")
)
ANSE_ROOT = os.environ.get("ANSE_ROOT", str(Path.home() / "AutoevolveAI"))
COLLECTION = os.environ.get("ADSCMT_COLLECTION", "adscmt_literature")

PILLARS = ("holography", "adscmt", "topology", "bridge", "experiment", "ryu")

# ANSE's default is 120 s. While the shared T4 is held by another session's
# prover, a single query embedding can wait longer than that, so the timeout is
# configurable. Expect cold-start latency of ~30 s even on an idle GPU.
EMBED_TIMEOUT_S = float(os.environ.get("ANSE_EMBED_TIMEOUT", "600"))

mcp = FastMCP("adscmt-rag")

_collection = None


def _load_embedding_function():
    module_path = Path(ANSE_ROOT) / "anse" / "memory" / "ollama_embeddings.py"
    if not module_path.is_file():
        raise RuntimeError(f"ANSE embedding module not found at {module_path}")
    spec = importlib.util.spec_from_file_location("anse_ollama_embeddings", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.OllamaEmbeddingFunction(timeout_s=EMBED_TIMEOUT_S, max_retries=2)


def get_collection():
    """Open the collection lazily, so an unreachable Ollama surfaces per-call.

    Deliberately uses `get_collection`, not `get_or_create_collection`: if the
    name is wrong or the store was never populated, that should be an error,
    not an empty collection that answers every query with silence.
    """
    global _collection
    if _collection is None:
        import chromadb

        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_collection(
            name=COLLECTION, embedding_function=_load_embedding_function()
        )
    return _collection


def _format(results: dict) -> str:
    documents = (results.get("documents") or [[]])[0]
    if not documents:
        return "No matching chunks."
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    lines: list[str] = []
    for i, document in enumerate(documents):
        meta = metadatas[i] if i < len(metadatas) else {}
        distance = distances[i] if i < len(distances) else float("nan")
        lines.append(
            f"### {i + 1}. {meta.get('title', '?')} ({meta.get('year', '?')})\n"
            f"arXiv:{meta.get('arxiv_id', '?')} | pillar={meta.get('pillar', '?')} | "
            f"{meta.get('kind', '?')} chunk {meta.get('chunk', '?')} | "
            f"cosine_distance={distance:.4f}\n"
            f"{meta.get('abs_url', '')}\n\n{document.strip()[:1600]}"
        )
    return "\n\n---\n\n".join(lines)


@mcp.tool()
def adscmt_search(query: str, n_results: int = 5, pillar: str = "") -> str:
    """Semantic search over the AdS/CMT literature corpus (52 arXiv papers).

    Covers holographic duality (AdS/CFT), its condensed-matter applications
    (holographic superconductors, non-Fermi liquids, SYK), topological
    insulators and superconductors (the ten-fold way), and the mechanisms
    bridging them (anomaly inflow, entanglement spectra, holographic
    topological semimetals).

    Args:
        query: natural-language question or topic.
        n_results: how many chunks to return (1-20).
        pillar: optional filter, one of holography, adscmt, topology, bridge,
            experiment.
    """
    n_results = max(1, min(int(n_results), 20))
    where = None
    if pillar:
        if pillar not in PILLARS:
            return f"Unknown pillar {pillar!r}; expected one of {', '.join(PILLARS)}."
        where = {"pillar": pillar}
    results = get_collection().query(
        query_texts=[query], n_results=n_results, where=where
    )
    return _format(results)


@mcp.tool()
def adscmt_paper(arxiv_id: str, max_chunks: int = 8) -> str:
    """Return the stored chunks of one paper, by arXiv id (e.g. hep-th/0603001)."""
    results = get_collection().get(
        where={"arxiv_id": arxiv_id}, include=["documents", "metadatas"]
    )
    documents = results.get("documents") or []
    if not documents:
        return f"No chunks stored for arXiv:{arxiv_id}."
    metadatas = results.get("metadatas") or []
    order = sorted(
        range(len(documents)),
        key=lambda i: (metadatas[i].get("kind") != "abstract", metadatas[i].get("chunk", 0)),
    )[: max(1, int(max_chunks))]
    head = metadatas[order[0]]
    body = "\n\n---\n\n".join(documents[i].strip() for i in order)
    return (
        f"# {head.get('title', '?')}\n"
        f"{head.get('authors', '')} ({head.get('year', '?')})\n"
        f"arXiv:{arxiv_id} | pillar={head.get('pillar', '?')} | "
        f"{len(documents)} chunks stored, showing {len(order)}\n"
        f"{head.get('abs_url', '')}\n\n{body}"
    )


@mcp.tool()
def adscmt_corpus_stats() -> str:
    """Report what is actually in the collection: counts per pillar and per paper."""
    collection = get_collection()
    results = collection.get(include=["metadatas"])
    metadatas = results.get("metadatas") or []
    per_pillar: dict[str, int] = {}
    papers: dict[str, str] = {}
    for meta in metadatas:
        per_pillar[meta.get("pillar", "?")] = per_pillar.get(meta.get("pillar", "?"), 0) + 1
        papers[meta.get("arxiv_id", "?")] = meta.get("title", "?")
    lines = [
        f"collection : {COLLECTION}",
        f"store      : {CHROMA_PATH}",
        f"chunks     : {collection.count()}",
        f"papers     : {len(papers)}",
        "",
        "chunks per pillar:",
    ]
    lines += [f"  {k:12} {v}" for k, v in sorted(per_pillar.items())]
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
