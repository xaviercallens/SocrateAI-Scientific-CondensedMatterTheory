# LL.md: lessons learned

This file records what went wrong, or nearly went wrong, in this project, and the rule each incident taught.
Each entry gives what happened, why it mattered, and the rule now applied.
Entries are appended and never edited away.

Scope: the AdS/CMT literature work, the PoC v0.1, and Track H v1.0 (preprint, DOI 10.5281/zenodo.23000391).

---

## A. Numerics and measurement

**LL-A1: a plateau that matches a formula is the formula, not the physics.**
- **What happened:** κ for the flat lattices "saturated" near 10^13. The value equalled `1/(max(shape)·ε)` to four significant figures, because κ was computed as s_max / s[rank-1] with a rank tolerance that capped it by construction.
- **Rule:** report the raw σ_max/σ_min, label a result SINGULAR when σ_min ≤ ε·σ_max, and never report a number that the method bounds.
- **Evidence:** ledger H0-X-0002.

**LL-A2: floating-point rank is not rank.**
- **What happened:** float64 said the flat lattices had a "structural rank deficiency". Exact rank over GF(p), with two primes that must agree, showed full rank.
- **Rule:** whenever κ is large, certify rank exactly before calling anything non-identifiable.
- **Evidence:** H0-B-0001, `data/exact_rank_full.json`.

**LL-A3: design controls against existing theory before running them.**
- **What happened:** the preregistered probe-matched control was singular by design. Unmeasured degree-2 nodes put resistors in series, and a series pair is non-identifiable. This is textbook circular-planar-network theory (Curtis–Ingerman–Morrow).
- **Rule:** before locking a control, check that its metric is defined on the setup. If it isn't, report a deviation, never a silent swap.
- **Evidence:** H0-B-0002, H0-X-0003.

**LL-A4: look for a theorem before preregistering a number.**
- **What happened:** the H2 prediction "λ_min constant" was refuted at finite size. A domain-monotonicity argument, together with λ₀ > 0 for nonamenable graphs (Dodziuk, Mohar), already settled the asymptotics.
- **Rule:** search for the governing theorem first. Preregister what the theorem leaves open, such as a rate or a constant, not what it already decides.

**LL-A5: a check proves only what it tests.**
- **What happened:** the paper said "the interior of G_L *is* G_{L−1}" when the script had only compared node counts. It now matches coordinates to 1e-9 and compares edge sets.
- **Rule:** word a claim to match the check exactly, or strengthen the check.
- **Evidence:** H2-B-0001.

**LL-A7: match dimension before comparing condition numbers.**
- **What happened:** v1.0 read a 6.7-decade probe-matched gap as a geometry effect. A reviewer asked whether it was dimensionality (306 vs 592 recovered parameters). The preregistered dimension-matched control (flat best-r subspace) showed the residual is ≤ 0.5 decades and reversed at N≈112; my own prediction (1–4 decades) was wrong.
- **Rule:** when two κ's are compared on subspaces of different dimension, also compare against the other side's best subspace of the same dimension. Any comparison of conditioning is a comparison of the same number of unknowns, or it is not a comparison.
- **Evidence:** H0-X-0005; the correction is stated in the paper (v1.1 §3.3), not hidden.

**LL-A6: two integrators beat one.**
- **What happened:** the RC model passes a known-answer check (K1, matrix exponential) and a static cross-check (K2, Schur complement) in both SciPy and rusty-SUNDIALS CVODE.
- **Rule:** a solver result counts only after a known-answer control and a second code.

## B. Citations and literature

**LL-B1: never cite from memory.**
- **What happened:** "Deban, Borcea et al." was a mis-citation; the paper is by Borcea, Druskin, Guevara Vasquez & Mamonov.
- **Rule:** pin every reference through the arXiv identity gate (`corpus/fetch_papers.py`) or an explicit search. Author lists that can't be verified are truncated to "et al."

**LL-B2: "not found" is not "novel".**
- **Rule:** novelty statements say which searches were run and that nothing was found. They never claim priority.

## C. Evidence and bookkeeping

**LL-C1: a digest must hash a file.**
- **What happened:** two ledger claims hashed literal strings, and older digests matched no file. The gate passed only because it ran without `--evidence-dir`.
- **Rule:** keep a content-addressed evidence store (`docs/elenchus/evidence/`), run the gate in strict mode, and flag unrecoverable digests in the claim's notes instead of hiding them.

**LL-C2: a regenerated data file breaks every digest that points at it.**
- **Rule:** archive the blob before regenerating the file, and re-point a claim only with a note in its notes field. The evidence-store tool now checks the store before labelling anything "not recovered".

**LL-C3: verify stores by counting, not by memory.**
- **What happened:** the `adscmt_literature` Chroma collection was assumed ingested. On 2026-09-27 the store held only `phase1_traces`.
- **Rule:** a restart begins by listing collections and their counts (`tools/restart.sh`).

**LL-C4: claim only what is done.**
- **What happened:** the paper said the benchmark "has been contributed" to rusty-SUNDIALS before the PR existed; the wording was changed to "proposed" until the merge.
- **Rule:** the tense of a claim follows the state of the world.

## D. Tooling and operations

**LL-D1: `set -euo pipefail` plus `ls` on a missing directory aborts silently.**
- **What happened:** `apply.sh` stopped after a successful build, because the wheel lookup ran `ls` over a candidate directory that didn't exist.
- **Rule:** use `find ... || true`, test that the result is non-empty, and print an explicit error.

**LL-D2: maturin names wheels after the package, not the module.**
- **What happened:** the wheel is `rusty_sundials_py-*.whl` while the import is `rusty_sundials`. `maturin develop` also needs a virtualenv.
- **Rule:** without a virtualenv, use `maturin build` followed by `pip install --user`.

**LL-D3: interactive `!` commands.**
- **What happened:** a multi-line paste runs as one script, so `!` on later lines breaks it. Sourcing a token file inline could fail with no output at all.
- **Rule:** use a wrapper script (`release/publish.sh`) that runs one step, logs to a fixed absolute path, checks the token file's syntax, and prints only whether each token is set, never its value.

**LL-D4: environment variables must be exported.**
- **Rule:** use `NAME=value` lines only with `set -a` around `.`, or write `export NAME=value`.

**LL-D5: irreversible actions are verified first.**
- **What happened:** the Zenodo publish step compares the draft's MD5 checksums, title, licence and related identifiers with the local build before calling publish.
- **Rule:** a DOI is permanent, so verify first and publish second.

**LL-D6: a DOI can lag its record.**
- **What happened:** doi.org returned 404 for a while after publication, while the Zenodo record was already public.
- **Rule:** report both states, and don't call a DOI broken until a day has passed.

**LL-D7: branch protection with an already-red `main`.**
- **What happened:** rusty-SUNDIALS `main` failed 4 CI jobs before PR #62, and auto-merge is disabled in that repository. #62 was merged with admin rights after it was shown to add no new failure.
- **Rule:** compare the PR's checks with `main`'s, job by job, before overriding protection, and record why.

**LL-D9: Python 3.10 f-strings.**
- **What happened:** twice, scripts failed with `SyntaxError` for a nested same-quote f-string and for a backslash inside an f-string expression (both allowed only from Python 3.12).
- **Rule:** compute the fragment in a variable first; keep f-string expressions free of quotes and backslashes.

**LL-D10: a PDF-to-text reviewer sees a different paper.**
- **What happened:** all seven "typographical" points of the v1.0 review were artefacts of PDF text extraction (dropped math, a period, a brace). The LaTeX source was correct.
- **Rule:** check every typographical remark against the source before "fixing" it, and say so in the response rather than silently ignoring it.

**LL-D8: permission boundaries are part of the design.**
- **What happened:** the assistant session could not use tokens, touch sibling repositories, or read transcripts.
- **Rule:** prepare a script, have the human run it, then verify the result anonymously (public API, no token). Never work around a denial.

## E. Learning systems (AutoevolveAI / ANSE)

**LL-E1: an energy-0 trace can be reward hacking.**
- **What happened:** in ANSE's `phase1_traces`, "write fib(n)" tasks are labelled `perfect` (energy 0.0) while the code is `def solution(): return True`. The verifier checked the script's own asserts, not the task.
- **Rule:** a verifier must test the task's specification with held-out cases the solution didn't write. Training on these traces as they stand teaches the model to game its own checks. Filter or relabel them first.

**LL-E2: refutations are the most valuable labels.**
- **Rule:** `training/physics_predictions.jsonl` keeps refuted and deviating predictions with energy 1 or null. A physics-learning dataset made only of confirmations teaches confidence, not physics.

**LL-E3: never train on the model's hidden reasoning, and scrub secrets.**
- **Rule:** `tools/export_session_traces.py` drops thinking blocks and redacts tokens and email addresses. Review `MANIFEST.json` and a sample before any training run.

## F. From the PoC (v0.1)

**LL-F1: finite-size smearing.**
- **What happened:** the v0.1 claim of "no finite-size smearing" in entanglement spectra was false, and was corrected by an erratum in `experiments/poc_entanglement_tda/results.md`.
- **Rule:** any claim that an effect is absent needs a size scan.
