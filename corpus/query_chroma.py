#!/usr/bin/env python3
"""Query and verify the adscmt_literature collection from the command line.

`--verify` is the acceptance check for the ingestion: it confirms the
collection is reachable, reports its true dimension, and runs a set of probe
queries whose top hit is asserted to be a specific paper. It exits non-zero on
failure, so it can gate a pipeline rather than merely print reassurance.

Usage:
    python3 corpus/query_chroma.py --verify
    python3 corpus/query_chroma.py "why do topological insulators have edge states"
    python3 corpus/query_chroma.py "strange metal transport" --pillar adscmt -n 3
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path

CHROMA_PATH = os.environ.get(
    "CHROMA_PATH", str(Path.home() / "AutoevolveAI" / "data" / "chroma")
)
ANSE_ROOT = os.environ.get("ANSE_ROOT", str(Path.home() / "AutoevolveAI"))
COLLECTION = os.environ.get("ADSCMT_COLLECTION", "adscmt_literature")

# (query, arxiv_id that must appear in the top-k). Chosen so that each probe
# targets a different pillar and a different paper, and so that a collection
# embedded with the wrong model would fail them.
PROBES: list[tuple[str, str, int]] = [
    ("holographic derivation of entanglement entropy from a minimal surface", "hep-th/0603001", 3),
    ("Z2 invariant protecting helical edge states under time reversal", "cond-mat/0506581", 5),
    ("ten-fold way classification of topological insulators and superconductors", "0803.2786", 5),
    ("scalar condensate outside a charged black hole horizon breaking U(1)", "0801.2977", 5),
    ("Sachdev-Ye-Kitaev model, Schwarzian mode and maximal chaos", "1604.07818", 5),
    ("anomaly inflow and theta term response of topological insulators", "1010.0936", 5),
]


def load_embedding_function():
    module_path = Path(ANSE_ROOT) / "anse" / "memory" / "ollama_embeddings.py"
    spec = importlib.util.spec_from_file_location("anse_ollama_embeddings", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.OllamaEmbeddingFunction()


def open_collection():
    import chromadb

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(
        name=COLLECTION, embedding_function=load_embedding_function()
    )


def run_verify(collection) -> int:
    print(f"store      : {CHROMA_PATH}")
    print(f"collection : {COLLECTION}")
    count = collection.count()
    print(f"chunks     : {count}")

    peek = collection.peek(limit=1)
    embeddings = peek.get("embeddings")
    dimension = len(embeddings[0]) if embeddings is not None and len(embeddings) else 0
    print(f"dimension  : {dimension}")

    failures = 0
    if count == 0:
        print("FAIL: collection is empty")
        failures += 1
    if dimension != 1024:
        print(f"FAIL: expected 1024-d (qwen3-embedding:0.6b), got {dimension}")
        failures += 1

    print("\nprobe queries (top hit must be the expected paper):")
    for query, expected_id, k in PROBES:
        results = collection.query(query_texts=[query], n_results=k)
        metadatas = (results.get("metadatas") or [[]])[0]
        hit_ids = [m.get("arxiv_id") for m in metadatas]
        ok = expected_id in hit_ids
        status = "ok  " if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"  {status} {query[:58]:58} -> {hit_ids[0] if hit_ids else '-'} (want {expected_id})")

    print(f"\n{'PASS' if failures == 0 else f'FAILED ({failures})'}")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default=None)
    parser.add_argument("-n", "--n-results", type=int, default=5)
    parser.add_argument("--pillar", default="")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    collection = open_collection()

    if args.verify or not args.query:
        return run_verify(collection)

    where = {"pillar": args.pillar} if args.pillar else None
    results = collection.query(
        query_texts=[args.query], n_results=args.n_results, where=where
    )
    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]
    for i, document in enumerate(documents):
        meta = metadatas[i]
        print(f"\n--- {i + 1}. {meta['title']} ({meta['year']})")
        print(f"    arXiv:{meta['arxiv_id']}  pillar={meta['pillar']}  d={distances[i]:.4f}")
        print("    " + document.strip()[:600].replace("\n", "\n    "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
