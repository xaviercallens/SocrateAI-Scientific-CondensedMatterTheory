# v0.1

First release: AdS/CMT ↔ topological matter research foundation — literature review, a Shinsei Ryu review built from his full arXiv record, a critically-reviewed 5-axis experimental programme, an Elenchus rigor discipline, a Chroma RAG pipeline, and a first computational PoC (SSH ring entanglement spectrum + SYK N mod 8, via Gudhi persistence).

## Theory

- **`docs/literature_review.md`** — AdS/CFT, holographic entanglement, AdS/CMT, the ten-fold topological classification, and what actually bridges them (anomaly inflow, entanglement, quantum error correction). Corrects the opening framing: topological insulators and AdS/CFT are not the same bulk-boundary statement.
- **`docs/ryu_review.md`** — Shinsei Ryu's programme, from his full arXiv record (202 papers, pulled live via `tools/arxiv_author.py`, not from memory).
- **`docs/contribution_map.md`** — three ranked projects mapping Lean 4 / GPU / Rust / HPC / Gudhi expertise onto open problems.
- **`docs/assets/README.md`** — every reusable asset on the host machine, opened and checked by hand (and what looked relevant but wasn't).

## Experimental programme

- **`docs/experimental_program.md`** + one `PREREGISTRATION.md` per axis — a 5-axis "garage deep tech" plan (topological water waves, analogue horizons, optical vortices, wave chaos, caustics), reviewed for real physics errors and given falsifiable predictions.
- **`docs/safety.md`**, **`lean/README.md`** (T0→T3 target ladder).

## Rigor discipline

- **`docs/rigor_protocol.md`**, **`docs/elenchus/ledger.json`** — aligned to the real Elenchus tier scale (X<C<L<B<A) after the repo was cloned and read. 6 claims filed, verified clean by Elenchus's own `tools/ledger.py`.
- **`experiments/axis1_topological_waves/ssh_exact.py`** — Tier B: the finite half of the SSH bulk-boundary statement, exact rational arithmetic, with negative and positive controls.

## Corpus + RAG

- **73→78 arXiv papers**, every ID checked against its real arXiv title before ingestion (the identity gate caught 6+ wrong IDs, one mistitled journal-vs-arXiv name, and a title cited from memory).
- **Chroma collection `adscmt_literature`** in AutoevolveAI's store, `qwen3-embedding:0.6b` (1024-d). `--verify` passes on all 73 abstracts, 8/8 semantic probes.
- **MCP servers**: `adscmt-rag`, `chroma-admin`, ANSE's own servers, and a scoped `rusty-sundials` server (no upstream MCP server exists for it; this one is honest about what it can and can't do yet).

## First computational PoC

- **`experiments/poc_entanglement_tda/`** — entanglement spectrum of an SSH ring + a Majorana SYK model, analyzed with Gudhi persistent homology.
  - **SSH ring**: both preregistered controls confirmed exactly — 2 mid-gap entanglement levels in the topological phase, 0 in the trivial phase, at two ring sizes. One sub-prediction (finite-size smearing) was refuted and reported as such: the invariant is quantized, so it jumps rather than crosses over.
  - **SYK, N mod 8**: a clean all-or-nothing split at every tested N≤24 — ground-state degeneracy present at N≡4 (mod 8), absent at N≡0 (mod 8), ~14 orders of magnitude apart in the same-sector gap. Gudhi recovers this split **unsupervised**, on the pooled, unlabelled data.

## Known limits, stated plainly

- Only paper **abstracts** are in Chroma; full text (~1500 chunks) is pending, throttled by GPU contention with another session's Lean prover on the shared T4.
- `rusty-SUNDIALS` has no local checkout on this host; its MCP server is a real but limited scaffold until cloned.
- The SYK N mod 8 pattern is empirical (Tier X): the symmetry operator behind it was not constructed here.
