# Task queue (2026-09-28), ordered; each card is executable with `docs/RUNBOOK.md`

Format: **id · tier · roadmap item** — goal; inputs; acceptance; escalation notes. Tiers as in RUNBOOK §6.
A card marked `low` has its design fixed here; the agent only fills sizes/seeds into the scaffold.

## Now (blocked on the human)
- **Q0 · human · release** — merge PR #2 and create GitHub release v1.1: `bash experiments/track_h_hyperbolic_network/release/merge_and_release.sh` from your own terminal. Acceptance: the script prints the merge commit and the `v1.1` release with `main.pdf` attached.
- **Q1 · done 2026-10-08** — v1.2 published on the user's instruction: DOI 10.5281/zenodo.23228685 (18 pages, built from ccfc30d, MD5-verified); Hugging Face dataset and simulator updated in place (`release/PUBLISHED.md`).
- **Q2 · human · H-6** — compile `lean/HyperbolicLogDepth.lean` on a machine with Lean 4 + Mathlib (command in `lean/README.md`); report the axiom footprint. Blocked here: no toolchain.

## Next experiments (design fixed; low/mid execution)
- **Q3 · low · H-3** — *Minimum detectable contrast.* **Ready to run:** `PREREGISTRATION_12.md` and `exp12_minimum_detectable_contrast.py` are written and committed (unrun). Do RUNBOOK steps 5–8: `python3 experiments/track_h_hyperbolic_network/exp12_minimum_detectable_contrast.py > <abs log path> 2>&1` (about 15 min; run in background), then a claim file with id `H3-X-0008`, `depends_on ["H3-X-0007"]`, evidence `data/minimum_detectable_contrast.json`, statement built from the printed `verdicts` (G1, G2 must be true; report P1–P4 as HELD/REFUTED with the top-1 numbers at ε = 3e-4 for f = 0.9, 1.1 on {7,3} L=3 and square R=10), then `experiment_gate.py`, then the results block in `LOCALIZATION_RESULTS.md`. If G1 or G2 is false, or any P is refuted, stop after recording and escalate (RUNBOOK §5).
- **Q4 · mid · H-3** — *Two-node defects.* Dictionary of node pairs is too large (C(interior,2)); design a greedy two-step matched filter (find node 1, subtract, find node 2) and preregister its top-2 accuracy vs noise on the four lattices, f = 2. Escalate the design to high tier if the greedy decoder fails on the ideal-noise control.
- **Q5 · mid · H-2** — *Why concave in depth?* Exploratory (label it): per-depth sensitivity profile ‖∂Λ/∂g_e‖ averaged over edges at depth d, for every tiling in `tilings_kappa.py`, plus the flat lattices; fit log-sensitivity vs d. No prediction; output a figure and a ledger entry marked EXPLORATORY. Feeds a high-tier derivation attempt.
- **Q6 · low · H-2** — *Exact rank certificates for the new tilings.* Run `hyperbolic_exact.certified_rank` for {8,3} L ≤ 3, {5,4} L ≤ 4, {6,4} L ≤ 3, {4,5} L ≤ 5 (skip any with E > 1500). Prediction: full rank everywhere (as for {7,3}); tier B claim if all agree across the two primes.
- **Q7 · low · H-4** — *RC benchmark on the new tilings.* Extend `rc_network.py` families with {8,3} L=2 and {5,4} L=3; K1/K2 controls with both integrators; prediction: both pass at the same tolerances. Also gives τ and stiffness for the build's alternatives.
- **Q8 · mid · H-4** — *Correlated hardware noise model.* Replace i.i.d. noise by (i) a common-mode offset per measurement, (ii) 1/f drift between the two maps, (iii) ADC quantisation at 12 and 16 bits; rerun `localize_noise.py`'s sweep for {7,3} L=2 and square R=6 only. Preregister that quantisation at 12 bits (≈2.4e-4) leaves both boards at top-1 = 1 for f = 2, and that drift ≥ 1e-3 breaks the flat board first.
- **Q9 · mid · H-7** — rusty-SUNDIALS: add an analytic-Jacobian argument to `CvodeSolver.solve` (Rust side), then a benchmark of solver cost vs geometry. Needs Rust; PR to rusty-SUNDIALS via `apply.sh`-style script; the human merges.
- **Q10 · low · H-8** — Ledger hygiene: for the five legacy digests (SSH-L-0001, SSH-C-0001, POC-X-0001, POC-X-0002, H0-X-0001) either regenerate the evidence file from the named script and re-point with `tools_rehash_ledger.py` (note appended), or, if the script no longer exists, append a note "evidence not reproducible; claim retained as historical". Acceptance: `experiment_gate.py` strict check passes with an empty legacy set (edit `LEGACY` in the gate only after this).

## Later (needs a human decision first)
- **Q11 · human · H-4, phase 1 (this week)** — Build and measure per `lab/PROTOCOL_H4.md` (session checklists, gates in order, generated forms under `lab/forms/` from `python3 lab/make_forms.py`), with `lab/LAB_GUIDE_H4.md` for the reasons and `PREREGISTRATION_13.md` (committed before any soldering). Day 1 is simulation only: `lab/bom_and_netlist.py`, `lab/virtual_bench.py`, `lab/analyze_measurements.py --demo` must all run. Parts: 342 × 100 kΩ 1 %, 106 × 1 µF film, quad rail-to-rail op-amp, ADS1115, ESP32 (`lab/out/BOM.md`). Acceptance: gates G1–G4 of the preregistration pass in order and `analyze_measurements.py` writes `lab/data/h4_step_response.json`; then RUNBOOK steps 6–8 with claim id `H4-X-0001` (any verdict). Predictions: τ ratio 0.604 ± 0.03; τ/τ_cal = 2.750 ± 0.08 and 4.551 ± 0.14.
- **Q12 · human · H-5** — Send v1.1 (or v1.2) to one inverse-problems specialist (e.g. the Borcea / Guevara Vasquez group) with a five-line message and the DOI; ask specifically about prior work on conditioning versus boundary depth.
- **Q13 · high · paper** — arXiv submission (math.NA / math-ph; endorsement needed) after Q12's answer.

## Done on 2026-09-28 with the low-tier workflow (orchestrator ran, Haiku recorded, orchestrator audited)
- **Q3** → H3-X-0008: at the 3×10⁻⁴ budget both geometries localise a ±10 % single-node change; at 3×10⁻³ the smallest
  localisable contrast is 0.9/1.1 on {7,3} but 0.5/1.5 on square R=10. P2 refuted; P3's "refuted" was a float-comparison
  scorer artefact (holds on trial counts; correction appended).
- **Q6** → H0-B-0003 (Tier B): full column rank certified over two finite fields for 11 new instances ({7,3} L=3,
  {8,3} L=2–3, {5,4} L=3–5, {6,4} L=2–3, {4,5} L=4–6, up to E = 1604) with a random row-combination certificate.
- **Q7** → H2-X-0005: RC τ and stiffness on four more tilings, K1/K2 pass with SciPy **and** rusty-SUNDIALS CVODE;
  {8,3} L=2: τ = 2.618 (board alternative with 5 % shorter relaxation than {7,3}); q = 4, 5 tilings: τ 0.50–0.91.

- **Q8** → H3-X-0009: at N≈112, f = 2, a common-mode offset up to 10 %, gain drift up to 1 % and a 10-bit ADC all leave
  localisation intact on both boards (49/50 cells at 1.00, lowest 0.95). All three predictions refuted in the safe
  direction: a ceiling; the failure boundary lies beyond the grid. Localisation needs less of the chain than τ does.
- **Q5** → H0-X-0009 (exploratory): the per-edge sensitivity profile versus depth is nearly the same on hyperbolic and
  flat lattices (all concave, −2.0 to −2.4 decades at depth 3), so amplitude decay does not explain concave-vs-linear
  κ; the candidate is the collinearity of equal-depth edges (v1.0's "coherence"). One control statistic was mis-specified
  and amended in the open (Deviation 1) before the rerun; no prediction was at stake.

## Done on 2026-10-07
- **Q5b** → H0-X-0010 (prereg 18): exhaustive coherence between Jacobian columns of equal-depth edges. The effective
  dimension fraction PR/n of the normalised Gram matrix separates the classes at every depth: hyperbolic 0.80–0.99 at
  depth 3 and never below 0.79 at any depth, flat 0.39 (square R=10) and 0.23 (triangular R=6.45) at depth 3 falling to
  0.14–0.20 at the deepest edges. P3 held (margin ≥ 2.07× against the 1.5× threshold). P1, P2, P4 were set on the
  median |cos| and refuted: the median of a zero-inflated distribution is not a coherence statistic (LL-A13).
- **Q5c** → H0-X-0011 (prereg 19): the mechanism survives size matching and is tied to κ. The condition number of
  the Jacobian restricted to depth-≤d columns grows 0.98 (square R=10) and 1.19 (triangular R=6.45) decades per depth
  beyond depth 1, against 0.28–0.44 on the five hyperbolic tilings (P2a, P2b held); at the deepest class with six
  matched columns the flat disks are at 0.35 and 0.46 while every hyperbolic tiling is ≥ 0.85 (P3 held). P1 (flat
  ≤ 0.80 at depth 3 with six columns) refuted: six random columns out of 76 do not see a collective deficit (LL-A14).
  Full κ reproduces H0-X-0008 and v1.0 (G1).

## Next for the low-tier loop (preregistration to be written by the orchestrator first)
- **Q5d** (high, H-2): *derivation attempt.* **Argument written** (`MECHANISM_NOTE.md`, Tier C: harmonic-measure
  bumps of width ≈ d on a flat boundary of length ≈ 2πR give the depth-d class an effective rank ≈ R/d, so d·f_d is
  constant and κ grows ≈ 1 decade per depth; on a hyperbolic disk the overlap number stays O(1)). **Test running:**
  `PREREGISTRATION_20.md` (committed 9ad012e before the run) on instances the argument never saw. **Tested (H0-X-0012):**
  P1 held (d·f_d constant within 1.26× on square R=16 over d = 2…12, 1.42× on triangular R=10.75), P2 held (hyperbolic
  f_d ≥ 0.76 at L=5 / 0.80 at L=7), P3b held (hyperbolic rate does not grow with L), **P3a refuted** (flat rate is
  R- and window-dependent: 1.26 at R=16 vs 0.98 at R=10; LL-A15). The overlap-number picture stands; the flat κ rate
  is underived.
- **Q5e** → H0-X-0013 (prereg 21, exploratory, Deviation 1 before the rerun): over windows fixed in relative depth the
  flat rate is a lattice constant for R ≥ 10 (square 1.08–1.23, triangular 1.69–1.84 decades per depth), so the
  R-dependence of H0-X-0012 was the window effect (LL-A15); both weak extrapolations refuted (the rate saturates;
  the two-layer triangular disk is below the square). Next **Q5f** (mid): Fourier coefficients of the lattice harmonic
  measure per depth on each disk; prediction to derive: the rate equals the decay constant of the highest resolvable
  boundary mode, and the triangular/square ratio ≈ 1.5 follows from the two lattices' boundary spacing.
- **Q5i** (high, H-2): *from the cylinder to the disk.* Steps done: orientation (diagonal strip, H0-X-0017), an out-of-sample test of the
  node picture (H0-X-0018) and curvature (polar-grid disk, H0-X-0019: curvature **raises** the rate by a few percent over the first quarter
  radius, so it does not explain the square disk's lower constant). **Remaining:** orientation mixtures and boundary roughness, the two
  candidates left for the square disk's 1.1–1.2 (between the diagonal 1.07 and aligned 1.65). **Q5k (high):** a strip along a general lattice
  direction, e.g. (2,1): the periodic unit has several nodes per row, so the blocks are banded and the harmonic extension needs a transfer
  matrix per momentum (mpmath); prediction to state before computing: the zigzag-block rate from the Green exponent of the signed node set of
  that geometry, tested with the same exact machinery and an explicit-Jacobian gate. Also open: potential theory for complex node sets
  (unequal-conductance diagonal strip) and the triangular lattice with a generic boundary.
- **Q14** (mid, paper): **draft built 2026-10-08, not published:** `paper/note_cylinder.tex`/`.pdf` (6 pages, generated tables and figures
  from the stored data by `paper/make_note_cylinder.py`): a self-contained computational note on the exact block structure and the
  Green-function rate on lattice strips, with the post-hoc signed-node step labelled and a register of every failure. Recommendation: a
  separate short record (Zenodo, later arXiv math.NA) rather than a v1.3 section, after specialist feedback (Q12) and ideally after the
  disk question (Q5i). v1.2 stays as published. Human decision: publish now, wait, or fold into v1.3.
- **Q4** (two-node defects, greedy two-step matched filter; escalate if the ideal-noise control fails).

## Done on 2026-10-08 (research, latest)
- **Q5i curvature** → H0-X-0019 (prereg 28): on a polar-grid disk (exact blocks, gate to four decimals) smooth curvature **raises** the per-row loss
  with depth (R = 48: 1.605 at level 3 to 1.801 at level 24; R = 96 to 1.675), growth 0.71–0.77 of the local-strip prediction (band set from pilots),
  scaling with l/R to 13 %, flat limit recovered (1.609 vs 1.611). Curvature therefore cannot explain the square disk's lower constant; orientation
  mixture and roughness remain (card Q5k). Ledger 46 claims, gate 57 checks. Decision recorded: the cylinder note waits for specialist feedback
  (`docs/SPECIALIST_OUTREACH.md`, `release/NOTE_PUBLICATION_PLAN.md`; nothing sent or published).

## Done on 2026-10-08 (research, later)
- **Q5i step 1, Q5j** → H0-X-0017 (prereg 26), H0-X-0018 (prereg 27): boundary orientation changes the exact rate (diagonal zigzag
  1.067 vs aligned 1.653; moduli-based Green and 1/√2 forms both wrong); a signed-node correction found post hoc matches all six
  diagonal block rates to 0.85 %; applied out of sample to the aligned strip with lateral conductance 0.05 and 16 the Green exponent
  predicts the converged zigzag rate to 0.15 % and 1.9 % (the λ-independent null refuted). Failures: moduli forms (card 26), two
  too-tight width tolerances and an undersized reference height (card 27). LL-A20; ledger 45 claims, gate 55 checks.

## Done on 2026-10-08 (research)
- **Q5f, Q5g, Q5h** → H0-X-0014 (prereg 23), H0-X-0015 (prereg 24), H0-X-0016 (prereg 25): the flat growth constant is exact where
  the problem separates. On the square cylinder the vertical-edge Jacobian is block-diagonal in total momentum; each block's
  smallest singular value decays at the Green-function exponent of the interval of its node values; verified in 140-digit
  arithmetic for six momenta (0.06–1.6 %), zigzag block dominant, global rate 1.65 decades per row. Four of the eleven
  evaluable predictions across the three cards were refuted (the preregistered 0.784 and the full-rate interval of card 23;
  the momentum table of card 24, which was my post-hoc closed form; a 1 % width-convergence threshold of card 25 missed at
  1.5 %), one was void, and design errors are recorded as LL-A17 to LL-A19. The triangular straight periodic boundary is
  exactly singular. Not explained: the disk (1.1–1.2 square), which is below the cylinder value.
- **Q8b** → H3-X-0010 (prereg 22): the ceiling of H3-X-0009 is resolved by derivation. Offsets of the form u1ᵀ + 1wᵀ are
  exactly invisible (every signature has zero row and column sums; 0 differences in every cell up to 100× rms);
  scalar gain drift between the two maps has a predicted curve (noiseless decode integrated over the drift law) that
  matched all 28 cells (largest deviation 0.128), plain decoder fails at 3–10 %, gain-fitted decoder is unaffected to
  30 %; quantisation is harmless on the {7,3} board down to 1 bit relative to rms and needs about 8 bits at full scale
  on the square board; per-channel gain mismatch between the two maps (exploratory) breaks localisation at ≈ 0.3 %
  (square) and ≈ 1 % ({7,3}). All five predictions held; lessons LL-A16; requirements in `lab/LAB_GUIDE_H4.md` §6b.

- **Q15** done (prereg 29): Laplace-resolved Jacobian; transient data lower kappa by about one decade, rate unchanged; recorded in the published strip-rate paper (Zenodo 10.5281/zenodo.23241463).
- **Q16** done (prereg 30): GUDHI H0 of the Jacobian column cloud per depth layer falls as a power law (~2.3/k) on the square disk, flat on {7,3}; tracks sigma_min monotonically but not its exponential rate; P4 and G2 failed as written. Next: H1 and a principal-angle filtration (angle to the span of shallower columns), which is where the linear dependence lives; more hyperbolic layers.
- **Q17** done (prereg 31): CVODE agrees with the garage virtual bench (tau to 3e-5, ratio 0.605); P1 narrowly refuted on the square board (integrator tolerance). Draft paper 2 (`paper/paper2.tex`, 5 pages) holds Q16 and Q17; not published, awaiting a go-ahead.
- **Q16b** done (prereg 32): depth-ordered Gram-Schmidt residual carries sigma_min's rate (-1.243 vs -1.272 decades/layer on the square disk), median shallower-span residual exponential (-0.656), 7x the nearest-neighbour topology; {7,3} worst column -0.40/layer over four layers; P3 bound refuted. Lean: `lean/dtn_offsets/GramSchmidtBound.lean` (7 theorems in the project, gates pass). Paper 3 drafted (5 pages), bundle built, publication plan in `release/paper3/PUBLICATION_PLAN.md`; not published. Next: more hyperbolic layers by the Gram route; formalise the leave-one-out identity and the nested-span inequality in Lean; the principal-angle filtration proper (persistent homology of the residual cloud, which the pilot found non-uniform).
- **Q18** done (prereg 33): learned persistence features (GUDHI persistence image, landscape, Atol; ridge and trees) of the Jacobian column cloud; gate G1 (leak) failed as written and again under a 200-permutation depth-stratified null (median R² 0.79 on shuffled targets), so P1 to P6 are unread; what survives: the certified residual transfers to hyperbolic tilings (R² 0.55) and no learned feature set does. TDA literature review in docs/LITERATURE_REVIEW_TDA.md (24 papers in the vector store, pillar tda). Lessons LL-A21, LL-A22. Next, only if wanted: depth-blind features (residual cloud after regressing out depth and size, stratified gate); the persistent Laplacian proper (Memoli-Wan-Wang) on the same filtration rather than the full-level Laplacian; cite Ghafuri-Jassim, Giusti et al., Carson-Chen in any revision of paper 2.
- **Topology programme** (docs/TOPOLOGY_PROGRAMME.md, 2026-10-10): the thesis as nodes N1–N7 with theorem/experiment/limit, Track H as the counter-programme, weakened after a verified survey to "topology constrains, under a gap, what geometry and spectrum then determine". Run once: node N1-L (finite SSH chain: data show the end mode exact under chiral disorder to 50 %, on-site breaking tolerated to a third of the gap, same-sublattice hopping to a fifth; both gates failed as written through my errors, so P1-P5 were unread; the repeat N1-L2 (gates G0-G2 pass on a fresh draw) holds all five, and node N1 is readable: `RESULTS_N1_LIMIT2.md`); Lean `SSHWinding.lean` (two residue integrals, gates pass, audited). Corpus: 10 papers under pillar `topoprog` (5333 chunks). Manifesto drafted (`paper/manifesto.tex`, 9 pages, adversarially reviewed, bundle built, not published). Next in order: (1) Lean: `h' = w`, non-vanishing on the circle, `circleIntegral.integral_congr` transfer, the `(2πi)⁻¹` normalisation as a named winding number; then the boundary half as a Lean statement on the finite matrix; (2) node N6 with Loftus's density-versus-topology decomposition as the preregistered control; (3) nodes N3 and N1a in the garage.
- **Q5k** still open: strip along a general lattice direction.

## Retired (done since the roadmap of 2026-09-27)
H-1 (v1.0 + v1.1 published), H-2 first pass (tilings, H0-X-0008), H-3a/H-3b (persistent homology, detection, localisation, noise margin, tolerance: H3-X-0001..0007), v1.2 draft.
