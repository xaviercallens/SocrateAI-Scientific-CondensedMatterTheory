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

**LL-A8: match the null to the effect size.**
- **What happened:** PREREGISTRATION_5 used a global 50 % conductance disorder as the null against a single-node defect. The defect's boundary signal was 6–9× larger on the hyperbolic lattice than on the square, exactly as predicted, but both sat below a null that perturbs 400+ edges at once; P2 was "refuted" by the design, not by the physics.
- **Rule:** a null distribution must have the same perturbation budget as the effect it is compared with (same number of edges, or same Σ|Δln g|). Otherwise the test measures the null's size, not the effect's.
- **Evidence:** H3-X-0001, `TDA_RESULTS.md`.

**LL-A9: never extrapolate a saturating response linearly in a ledger note.**
- **What happened:** in H3-X-0003's notes and `TDA_RESULTS.md` I wrote that a ×2 defect would be "~100× weaker" than the tested ×100 one because "the signal is roughly linear in the conductance change". I had not computed it. A 30-second calculation showed the response saturates: ×2 gives 27–37 % of the ×100 signal. The error would have steered the next preregistration and the hardware plan toward a wrong worry.
- **Rule:** a quantitative limitation that will steer decisions is computed before it is written; if it can't be, it is labelled a guess. Corrections are appended to the note and the results file (statement unchanged), and the correcting data goes in the ledger (H3-X-0004).

**LL-A10: don't predict a decoder from a different statistic's SNR.**
- **What happened:** for localisation I predicted the flat lattice would fail at deep nodes and low contrast, reasoning from the SNR of the *detection* statistic (a single norm, ~3× the noise floor). The matched-filter decoder localised perfectly in all 60 cells: it uses all m² correlated matrix entries, not one norm. Two of three predictions were refuted, and the result weakens the localisation motivation for a hyperbolic build.
- **Rule:** predict a decoder's performance from a model of the decoder, or from a noise sweep that finds its failure boundary; a perfect score (60/60) is a ceiling, not a measurement, and always calls for the sweep (PREREGISTRATION_9).
- **Evidence:** H3-X-0005, `LOCALIZATION_RESULTS.md`.

**LL-A11: don't carry a conclusion across measurement regimes.**
- **What happened:** tolerance broke *model-based* detection of a defect at 5 % (compare with the ideal simulation), so I predicted it would also break *differential* localisation (compare a board with its own earlier measurement). It did not: localisation was unchanged up to 5 % tolerance. The tolerance is common to both maps of one board and cancels to first order in their difference; the model-based regime has no such cancellation.
- **Rule:** before predicting how a perturbation affects a new task, ask whether the task measures a difference within the perturbed system or a comparison with an idealised model; the two regimes can give opposite answers. (Second time in a day I applied one experiment's result to a different statistic; see LL-A10.)
- **Evidence:** H3-X-0007, `LOCALIZATION_RESULTS.md`.

**LL-A12: a control's tolerance must include the method's numerical floor.**
- **What happened:** for the multi-tiling run I computed κ from the Gram matrix G = JᵀJ (cheap, no giant Jacobian) and preregistered a control tolerance of 1e-6 against the direct SVD. It passed on {7,3} (3e-12) and failed on square R=6 (1.1e-6), because forming G squares the condition number: float64 loses ≈ ε·κ(G) (here 3e-6 at κ(G) = 10¹⁰). The method was fine; the tolerance ignored the known floor.
- **Rule:** derive a control's tolerance from the method's error model (here max(1e-6, 10·ε·κ(G))), and store an error bound with every value. When a control fails, diagnose before changing anything, then amend the preregistration in the open *before* looking at any result the control was guarding (Deviation 1 in `PREREGISTRATION_11.md`, committed as cc537c5).
- **Also learned in the same run:** a threshold I set from intuition (local exponent ≤ 1.0 for the q = 4, 5 tilings) was too low and was refuted (1.19 and 1.06); state such thresholds with the argument they come from.
- **Evidence:** `gram_control_diag.py`, H0-X-0008.

**LL-A13: a median says nothing about the tail that sets the conditioning.**
- **What happened:** preregistration 18 fixed three of its four predictions on the *median* |cos| between Jacobian columns of equal-depth edges. Most pairs are nearly orthogonal on every lattice (medians of 10⁻⁶ to 10⁻³ at depth ≤ 3), so the median is dominated by irrelevant far-apart pairs, ratios of medians are noise (the square/{7,3} ratio jumps 450 → 59 → 207 → 43 → 15 with depth), and a "spread across families" of such medians is a spread of near-zeros (2×10⁵). P1, P2 and P4 were refuted for that reason alone. The one prediction set on an aggregate quantity sensitive to the collinear tail, the participation-ratio fraction PR/n of the normalised Gram matrix, held with margin (hyperbolic ≥ 0.80 at depth 3 vs flat ≤ 0.39) and tells the story cleanly on every depth and every family.
- **Rule:** when the hypothesis is about a tail (collinearity, worst case, smallest singular value), preregister a tail or spectrum statistic (participation ratio, p90, smallest eigenvalue of the normalised Gram), never a central one. Check the statistic against a small instance before fixing thresholds on it; the median on {7,3} L=2 was already 10⁻³ at depth 1.
- **Evidence:** H0-X-0010, `TILINGS_RESULTS.md`, `data/coherence_versus_depth_across_tilings.json`.

**LL-A14: a collective deficiency is invisible to small random subsets; match size at the deepest class, not at a fixed depth.**
- **What happened:** preregistration 19 matched class sizes by subsampling six columns per depth. On square R=10 at depth 3 the full class of 76 columns has an effective dimension fraction of 0.39, but six random columns from it give 0.94, so prediction P1 ("flat ≤ 0.80 at depth 3") was refuted while the same statistic at the deepest classes (P3) and the κ increments (P2a, P2b) held. The dry-run instance (square R=6, 0.71 at depth 3) has a smaller d_max, so its "depth 3" is relatively deeper than square R=10's.
- **Rule:** when the hypothesis is that a set of columns is collectively rank-deficient, a random small subset underestimates the deficit; match sizes at the largest n the smaller class allows, compare at the deepest class or at depth relative to d_max, and never transfer a threshold between disks of different d_max at a fixed absolute depth. Record the full-class statistic alongside the matched one.
- **Evidence:** H0-X-0011, `data/coherence_mechanism_at_matched_size.json`.

**LL-A15: compare growth rates over matched relative windows, and separate a form prediction from a rate prediction.**
- **What happened:** preregistration 20 predicted that the per-depth growth of the depth-restricted κ on flat disks is independent of R (|Δ̄(R=16) − Δ̄(R=10)| ≤ 0.2). It was refuted (1.26 vs 0.98; triangular 1.71): double precision limits R=16 to d ≤ 8 of 14 while R=10 was averaged over its full range, where the last increments shrink (1.02 → 0.55 near d_max); and the argument's "rate set by the lattice cutoff" step was unsupported anyway. The band-counting prediction in the same card (d·f_d constant) held on both instances.
- **Rule:** when a quantity is averaged over depth, fix the window in relative depth d/d_max and in the usable precision range before predicting a number; and preregister the structural prediction (a scaling form) and the rate prediction as separate items, so a wrong constant does not take the form down with it (it did not here only because they were separate predictions).
- **Evidence:** H0-X-0012, `MECHANISM_NOTE.md` (test outcome), `data/coherence_mechanism_prediction_test.json`.

**LL-A16: derive the symmetries of the measured object before predicting a perturbation; compute the prediction instead of guessing; check the derivation against a brute-force scan before preregistering it.**
- **What happened:** in H3-X-0009 I predicted that a 1 % common-mode offset would break the flat board and all three predictions were refuted. Preregistration 22 shows why in one line: current conservation makes every dictionary signature have zero row and column sums, so any offset of the form u1ᵀ + 1wᵀ is exactly orthogonal to all candidates and the decoded node is identical trial by trial (0 differences in every offset cell, up to 100× the rms entry). I could have derived that before the first card. For scalar gain drift I derived the expected top-1 curve by integrating the noiseless decode over the drift law, and it matched the simulated curves in all 28 cells (largest deviation 0.128). My first analytic attempt was wrong twice (a tail function returning the wrong tail, and counting same-node contrast candidates as errors although the decoder returns the node), and was caught only because I compared it with a direct noiseless scan before preregistering.
- **Rule:** (1) list the exact symmetries and conservation laws of the measured object; perturbations along them are invisible, and the rest can be computed; (2) when the decoder is deterministic, evaluate the perturbed decision directly (a scan) and integrate over the perturbation law, instead of reasoning from the size of the perturbation relative to the signal; (3) cross-check an analytic derivation against a brute-force evaluation of one case before the numbers are fixed in a preregistration; (4) state which already-known measurements agree with a prediction, since they are not independent tests.
- **Also learned:** a surprising result gets a mechanism check before it is recorded. "Top-1 = 1.00 at 1 bit of quantisation" was real but narrow: the quantised difference is a sparse deterministic fingerprint of the defect node (814 entries flipping by one step on {7,3}, norm four times the true signature), which an ideal undithered quantiser with aligned grids preserves; noiselessly the decode is right at every tested bit count on both boards, so the square board's failures at 3 bits or fewer are noise flipping the roundings.
- **Evidence:** H3-X-0010, `data/hardware_noise_failure_boundaries.json`, `data/quantisation_diagnostic.json`.

**LL-A17: an explanation fitted to one number is a hypothesis, and the rival form from standard theory should be written down next to it before the decisive computation.**
- **What happened:** preregistration 23 predicted a rate of 0.784 decades per row for the square cylinder, from a Chebyshev growth estimate for a Vandermonde-type system; the run gave 1.78. I then "found what the number had left out" (κ is a ratio across momentum blocks) and produced a corrected closed form, 1.833, which agreed with 1.78 to 3 % and with a block rate of 1.85 to 1 %. It was wrong: I had placed the Chebyshev evaluation point at t = −1 after rescaling the interval, whereas the coefficient norm lives on the unit circle of the original variable. The potential-theory (Green function) value is 1.653 for the zigzag block, and the exact 140-digit computation of preregistration 25 gave 1.653 at width 768 and agreed with that form for all six momenta to 0.06–1.6 %. The apparent agreement with 1.833 came from double-precision data at a finite height whose increments were still rising (1.74, 1.84, 1.97), so a window average happened to land near it.
- **Rule:** (1) when a correction is found after seeing the data, write it up as a hypothesis, derive it again from the standard theory of the problem (here the asymptotics of polynomial coefficients on an interval), and preregister both forms as rivals for a computation that can separate them; (2) never read a rate off increments that are still changing: check that they have converged or compute the asymptote exactly; (3) a closed form that matches one number to 1–3 % has not been tested, whatever its tidiness.
- **Evidence:** H0-X-0014, H0-X-0015, H0-X-0016; `MECHANISM_NOTE.md`.

**LL-A18: count the degrees of freedom before choosing a window; and keep the geometry the same when comparing two computations.**
- **What happened:** two design errors in one afternoon. Preregistration 25 asked for depths 20 to 30 at width 96, but a block at total momentum π has only 25 distinct nodes there (k → −k and k → π − k collapse the 96 mode indices), so the restricted Jacobian is rank-deficient from depth 24: a boundary of W sites carries finitely many data per momentum. And preregistration 24 compared its block machinery (cylinder height 14) with the explicit rates of preregistration 23 (height 18) as a consistency gate, without matching the height; gate G2 failed legitimately. The explicit SVD at height 14 reproduces the block values exactly, and at height 18 gives up to 0.34 decades less at depth 6.
- **Rule:** before fixing a depth window, count the distinct nodes (or data components) per block; before comparing two computations, list every parameter they share (height, width, depth convention) and make them equal, or state the difference in the gate.
- **Evidence:** `PREREGISTRATION_24.md`, `PREREGISTRATION_25.md` (Deviation 1), `data/momentum_height_diagnostic.json`.

**LL-A19: a symmetric background can make a Jacobian exactly singular; check rank before conditioning on a new geometry.**
- **What happened:** the straight, periodic triangular cylinder of preregistration 23 has an exact null vector among the depth-0 diagonal edges (the sum over boundary nodes of the difference of their two diagonal columns vanishes, by translation invariance plus mirror symmetry about each interior node), so no depth could be kept and the series was empty. The triangular disk, which lacks the symmetry, is full rank.
- **Rule:** on any new geometry compute the rank of the Jacobian at the smallest depth first; a periodic and mirror-symmetric background is a suspect.
- **Evidence:** H0-X-0014, post-hoc diagnostics of `PREREGISTRATION_23.md` Deviation 1.

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

**LL-D11: score counts, not float differences.**
- **What happened:** PREREGISTRATION_12's P3 allowed a top-1 difference ≤ 0.2; the scorer compared 0.9 − 0.7 as floats (0.20000000000000007) and returned false for a difference of exactly 4 of 20 trials.
- **Rule:** in `score()`, compare integer trial counts (or round to the trial resolution) against thresholds; add a tolerance of half a trial otherwise. Corrections of a scorer are appended to the claim's notes; the data file and statement stay as written.

**LL-D12: what the low-tier workflow can and cannot do here (observed 2026-09-28).**
- Subagents (Haiku) can run `python3` scripts, write files, run `tools/ledger_add.py` and `tools/experiment_gate.py`, and copy tables faithfully; they **cannot run git** in this environment, and a background run redirected into the worktree was refused. They stopped correctly at every failure instead of improvising.
- Errors they made: one technical paraphrase ("eigenvalues of the DtN matrix" for L_ii). Errors *I* made that they surfaced: the gate archived evidence after checking it; the runbook told them to log inside the worktree; a scorer used float comparison.
- **Rule:** low tier records, gates and reports; the orchestrator audits (`tools/audit_low_tier.py`), corrects wording, commits, and writes readings. Tell low-tier agents to copy technical sentences verbatim rather than summarise them.

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
