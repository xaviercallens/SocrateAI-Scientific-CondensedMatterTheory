## AdS/CMT literature review, Shinsei Ryu review, experimental programme critique, Elenchus rigor discipline

### What this adds

- **Literature review** (`docs/literature_review.md`): AdS/CFT, holographic entanglement, AdS/CMT applications, the ten-fold topological classification, and the mechanisms that actually bridge them (anomaly inflow, entanglement, quantum error correction). Corrects the opening framing: topological insulators and AdS/CFT are not the same bulk-boundary statement (a one-way implication vs. an exact equivalence).
- **Shinsei Ryu review** (`docs/ryu_review.md`): built from his full arXiv record (202 papers, pulled live, not from memory). Confirms and sharpens the original intuition: Gu, Lee, Wen, Cho & Ryu (1605.00570) prove that the holographic dual of a 2+1-d quantum anomalous Hall state is a 3+1-d topological insulator — for free-fermion states, via tensor-network holography, not AdS/CFT with dynamical gravity.
- **Contribution map** (`docs/contribution_map.md`): ranks three concrete projects (Lean formalisation of Ryu–Hatsugai/SSH, GPU stabilizer-entropy engine, TDA transition detection) against Lean 4 / GPU / Rust / HPC / Gudhi expertise, grounded in what's actually installed on this machine.
- **Machine asset inventory** (`docs/assets/README.md`): every reusable asset opened and checked by hand, and — importantly — what looked relevant but wasn't (a "K-theory" Lean file that's really an integer triple with no Mathlib).
- **Experimental programme critique** (`docs/experimental_program.md` + `experiments/*/PREREGISTRATION.md`): a five-axis "garage deep tech" plan (topological water waves, analogue horizons, optical vortices, wave chaos, caustics), reviewed for real physics errors (a 3D-printed optical vortex plate needs 1.3 µm relief — 40-80x finer than any FDM/SLA printer; spontaneous Hawking radiation is ~1e-12 K, undetectable) and given a preregistration per axis.
- **Elenchus rigor discipline** (`docs/rigor_protocol.md`, `docs/elenchus/`): aligned to the real Elenchus tier scale (X<C<L<B<A) after the repo was cloned and read. First ledger filed: 4 claims on the SSH bulk-boundary statement, verified clean by Elenchus's own `tools/ledger.py` (2x Tier B via `experiments/axis1_topological_waves/ssh_exact.py`, exact-arithmetic with negative/positive controls; 1x Tier L citing a specific Mathlib lemma with its uncovered case named; 1x Tier C for the physical reading, capped as an interpretation).
- **Chroma RAG pipeline** (`corpus/`, `mcp_adscmt_rag.py`): 73 arXiv papers, every ID checked against its real arXiv title (the gate caught 6+ wrong IDs before ingestion), embedded with ANSE's `qwen3-embedding:0.6b` (1024-d) into `adscmt_literature`. `--verify` passes: 73/73 abstracts present, 8/8 semantic probes correct.
- **MCP integration**: ANSE's own servers copied into `config/mcp.json.example`; a new `mcp_rusty_sundials.py` for rusty-SUNDIALS, honestly scoped (no MCP server exists upstream, no local checkout yet — a real but limited status/list/run-raw server, not a fabricated physics API).

### Known limits (stated, not hidden)

- Only abstracts are ingested into Chroma (full text, ~1500 chunks, is pending — throttled by GPU contention with another session's Lean prover on the shared T4).
- `rusty-SUNDIALS` has no local checkout; its MCP server is a real but limited scaffold until cloned.
- Elenchus's ledger evidence digests are schema-valid but not yet blob-verified against its `--evidence-dir` convention (honestly reported by its own tool as `evidence_verified: false`).

### How to verify

```bash
python3 corpus/query_chroma.py --verify
python3 experiments/axis1_topological_waves/ssh_check.py      # Tier X numeric witness
python3 experiments/axis1_topological_waves/ssh_exact.py       # Tier B exact-arithmetic + controls
python3 <elenchus-checkout>/tools/ledger.py docs/elenchus/ledger.json --json
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)
