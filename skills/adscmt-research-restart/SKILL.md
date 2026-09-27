---
name: adscmt-research-restart
description: Resume the SocrateAI AdS/CMT + Track H (hyperbolic resistor networks) research project - status check, rigor rules, where every artefact lives, and how to publish/ingest/export without breaking the evidence chain. Use when starting a new session on SocrateAI-Scientific-CondensedMatterTheory, the rusty-SUNDIALS RC benchmark, or the adscmt Chroma collections.
---

# AdS/CMT + Track H: restart and working rules

Install (once): `mkdir -p ~/.claude/skills && cp -r skills/adscmt-research-restart ~/.claude/skills/`

## 1. Restart (always first)
```
bash tools/restart.sh            # status: git, env, self-tests, ledger gate, Chroma counts, publications, next steps
bash tools/restart.sh --rebuild  # + rerun analyses, paper, release bundles, physics dataset
```
Before any new work, read `LL.md` (lessons learned) and the "État au …" section at the top of `docs/roadmap.md`.

## 2. Where things are
| Artefact | Location |
|---|---|
| Track H code, data and paper | `experiments/track_h_hyperbolic_network/` (`paper/build.py`, `data/*.json`) |
| Published preprint v1.0 | Zenodo DOI 10.5281/zenodo.23000391. Hugging Face: dataset `callensxavier/hyperbolic-resistor-networks`, simulator `callensxavier/hyperbolic-resistor-network-simulator` |
| Claim ledger and evidence | `docs/elenchus/ledger.json`, `docs/elenchus/evidence/<sha256>.json`. Gate: `~/SocrateAI-Scientific-Elenchus/tools/ledger.py`, which `restart.sh` clones if it is missing |
| Literature RAG | Chroma store `~/AutoevolveAI/data/chroma`, collection `adscmt_literature` (`corpus/ingest_chroma.py --resume`) |
| Generated-documents RAG | collection `adscmt_generated` (`corpus/ingest_generated.py`). Never mix it with the literature |
| Physics training labels | `training/physics_predictions.jsonl`, `training/ledger_claims.jsonl` (`tools/build_physics_verdicts.py`) |
| Session input/output export | `tools/export_session_traces.py` → `~/AutoevolveAI/data/training/adscmt_sessions/`. Drops thinking blocks and scrubs secrets |
| rusty-SUNDIALS benchmark | upstream `examples/python/rc_network/` (PR #62). Local wheel: `maturin build`, then `pip install --user` |
| Release and publish wrapper | `experiments/track_h_hyperbolic_network/release/publish.sh {check,hf,zenodo,publish <id>}` |

## 3. Non-negotiable rules
- **Preregistration.** Commit predictions, with rival forms and refutation criteria, **before** computing. Report deviations and refutations as results.
- **Ledger.** Every claim goes in the ledger with a tier (X < C < L < B < A) and the digest of a real file. Run the gate with `--evidence-dir`.
- **Conditioning.** When κ is large, certify rank exactly over GF(p) with two primes. Report the raw σ_max/σ_min, and label the result SINGULAR when σ_min ≤ ε·σ_max.
- **Citations.** Cite only through the arXiv identity gate (`corpus/fetch_papers.py`) or a pinned search. Author lists that can't be verified become "et al.".
- **Generated numbers.** Tables and figures come from `data/*.json` via `make_assets.py`. Never type numbers by hand.
- **Irreversible or outward actions** (Zenodo publish, merges, uploads):
  - prepare a script, have the human run it, then verify the result anonymously;
  - for Zenodo, create a draft first, verify its MD5 checksums and metadata, then publish.
- **Training data.**
  - Never train on the model's thinking, and never export transcripts that haven't been scrubbed.
  - ANSE's `phase1_traces` contain reward-hacked "perfect" traces (see LL-E1). Filter them before training.
- **Scope.** Track H does not test AdS/CMT. Never present it that way.

## 4. Next steps
From the roadmap (`docs/roadmap.md`), H-1 to H-8:
- **H-1:** merge PR #2 and create the v1.0 release.
- **H-2:** scaling law across several tilings.
- **H-3:** difference-imaging reconstruction.
- **H-4:** the physical RC build, {7,3} L=2 against square R=6. Predictions: τ = 2.75 vs 4.55 RC, stiffness 14.9 vs 35.4.
- **H-5:** specialist feedback, then arXiv or a journal.
- **H-6:** Lean proof of the spectral-gap proposition.
- **H-7:** rusty-SUNDIALS CI fixes and an analytic Jacobian.
- **H-8:** the legacy ledger digests.
