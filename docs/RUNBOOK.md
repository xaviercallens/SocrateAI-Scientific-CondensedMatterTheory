# Runbook: executing this research programme with a low-capability agent

Written 2026-09-28. Audience: an automated workflow or a small model (Haiku-class, or a local 7–8B model) that runs
experiments in `experiments/track_h_hyperbolic_network/`. The design goal is that **no step needs scientific judgment
inside the loop**: judgment is either fixed in advance (the preregistration) or escalated (Section 5). Everything
else is a command with a machine-checkable outcome.

Read first: `LL.md` (what went wrong before), then `docs/TASK_QUEUE.md` (what to do next, with tier per task).

## 1. The only loop

Every experiment is the same eight steps. Do not reorder, skip, or merge them.

| # | Step | Command / action | Done when |
|---|---|---|---|
| 0 | Restart | `bash tools/restart.sh` | it prints a status table; `python3 tools/experiment_gate.py --quick` prints `ALL PASS` |
| 1 | Scaffold | `python3 tools/new_experiment.py <n> "<title>"` | `PREREGISTRATION_<n>.md`, `exp<n>_<slug>.py` and a manifest entry exist |
| 2 | Fill the preregistration | edit `PREREGISTRATION_<n>.md`: design, gates, **numeric** thresholds for every prediction, "Not claimed" | no `TODO` remains; every prediction has a number and a "refuted if" |
| 3 | Fill the script | edit `exp<n>_<slug>.py`: `run()` writes `data/<slug>.json`; `score()` returns verdicts from the file alone | `python3 -c "import ast,sys;ast.parse(open('<script>').read())"` succeeds; no result computed yet |
| 4 | **Commit before running** | `git add <prereg> <script> experiments.json && git commit -m "prereg <n>: <title>; script unrun"` then `git push` | `git log -1` shows the commit; the data file does not exist |
| 5 | Run | `python3 <script>` (background if > 5 min; log to a file) | `data/<slug>.json` exists; the script printed `verdicts:` |
| 6 | Record | write `claim.json` (Section 3), then `python3 tools/ledger_add.py claim.json` | it prints `added <id>` |
| 7 | Gate | `python3 tools/experiment_gate.py` | `ALL PASS`. If `FAIL`: do **not** edit the ledger by hand; go to Section 5 |
| 8 | Report and commit | append the results block (Section 4) to the results file named in the task; `git add -A experiments/track_h_hyperbolic_network docs training && git commit && git push` | pushed; the report contains the verdict of **every** prediction, including refuted ones |

Between step 4 and step 5 nothing may change in the preregistration. If something must change (a control fails,
a tolerance was wrong), write a dated **"Deviation"** paragraph in the preregistration explaining what and why,
commit it, and only then run. The gate checks commit order (prereg before data) from git history.

## 2. Absolute rules (violating one ends the run; escalate instead)

1. Never edit the `statement` of an existing ledger claim. Corrections are appended to `notes` with
   `tools/ledger_add.py --correct <id> "CORRECTION (<date>): ..."`.
2. Never publish, merge, tag, upload, or call an API with a token. These are the human's (Section 5).
3. Never touch `paper/main.tex`, `paper/main.pdf`, `paper/tables.tex` (the published v1.1). The gate checks this.
4. Never write a number into a document that was not read from a data file or printed by a script this session.
5. Never present Track H as a test of holography or AdS/CFT, and never call a spectral gap a "topological phase".
6. Never compare condition numbers of subspaces of different dimension without a dimension-matched control (LL-A7).
7. A null distribution must have the same perturbation budget as the effect (LL-A8).
8. A result of 100 % or 0 % in every cell is a ceiling/floor, not a measurement: the next task is a sweep (LL-A10).
9. Do not extrapolate a quantity you have not computed (LL-A9); if a limitation needs a number, compute it or label it a guess.
10. In Python: no braces inside `.format` strings, no nested same-quote f-strings, no backslash inside f-string expressions
    (Python 3.10). Cast NumPy scalars with `float()/int()/bool()` before `json.dumps`.
11. Shell: one command per `!` input; never paste several lines; `bash script.sh` and `rm`/`cp` may be refused, so
    prefer `python3 script.py`; write logs to a fixed absolute path inside the worktree.

## 3. Claim file (input to `tools/ledger_add.py`)

```json
{"id": "H3-X-0008", "tier": "X", "kind": "numeric", "depends_on": ["H3-X-0007"],
 "evidence_file": "experiments/track_h_hyperbolic_network/data/<slug>.json",
 "statement": "PREREGISTRATION_<n> (<one-line design>). P1 HELD (<numbers>). P2 REFUTED (<numbers>). <one-sentence reading>.",
 "notes": "experiments/track_h_hyperbolic_network/exp<n>_<slug>.py. LIMITS: <what was not tested>."}
```
Id prefix: `H0` conditioning/identifiability, `H2` RC dynamics, `H3` detection/localisation, `H4` hardware, `H6`
formal proofs. Tier `X` for any numerical result; `B` only for exact/integer computations; `L` for citations; `C`
for arguments; never `A` (kernel-checked proofs are the human's call). The next free number: look at the ledger.

## 4. Results block (append to the results file; numbers copied from the data file only)

```
## <title> (`PREREGISTRATION_<n>.md`, <commit> before the run; ledger <id>)
Design: <two lines>. Data: `data/<slug>.json`.
| Prediction | Threshold | Measured | Verdict |
|---|---|---|---|
Deviations: <none | dated paragraph copied from the preregistration>.
Limits: <copied from "Not claimed", plus anything discovered>.
```
No interpretation beyond the verdict table unless the task says "interpret" (then Section 5 applies).

## 5. Escalation: stop and hand up when

| Situation | Hand to |
|---|---|
| A validity gate or control fails | mid-tier model: diagnose, write the Deviation paragraph; a human approves it if it changes a threshold |
| A prediction is **refuted** | mid-tier model writes the reading and the LL.md lesson; the low-tier agent only records the verdict |
| A result contradicts a published sentence (v1.0/v1.1) | human: decides whether a correction note or a new version is needed |
| `experiment_gate.py` prints FAIL and the cause is not obvious from its line | mid-tier model |
| Anything that would publish, merge, tag, upload, or spend a token | human (`release/publish.sh`, `release/merge_and_release.sh`) |
| A new tiling, lattice family, decoder, or physical model is needed | high-tier model designs it; the loop above runs it |
| Text for the paper (`make_v12.py` replacements) | high-tier model; a human reads the PDF before any release |

## 6. Tiers (what each level of capability is trusted to do)

- **Low (workflow / small model):** steps 0–8 for a task in `TASK_QUEUE.md` marked `tier: low`, where the
  preregistration is already written by a higher tier and only sizes/seeds change; recording claims; running the
  gate; regenerating exports; appending results blocks; nothing else.
- **Mid:** writing preregistrations from a task card, scoring functions, Deviation paragraphs, LL.md entries,
  results readings, `make_assets.py` tables.
- **High:** new experimental designs, decoder or model changes, paper text, responses to reviewers, the roadmap.
- **Human:** publication, merges, releases, tokens, thresholds that change after a control failure, physical builds.

## 7. Weekly hygiene (low tier)

`bash tools/restart.sh`; `python3 tools/experiment_gate.py`; `python3 corpus/ingest_generated.py` (re-index our
documents); `python3 tools/export_session_traces.py` (training data, thinking stripped, secrets scrubbed); report
the three summary lines. Do not fix anything the gate flags; report it.
