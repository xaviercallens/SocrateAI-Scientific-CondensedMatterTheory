# Task queue (2026-09-28), ordered; each card is executable with `docs/RUNBOOK.md`

Format: **id · tier · roadmap item** — goal; inputs; acceptance; escalation notes. Tiers as in RUNBOOK §6.
A card marked `low` has its design fixed here; the agent only fills sizes/seeds into the scaffold.

## Now (blocked on the human)
- **Q0 · human · release** — merge PR #2 and create GitHub release v1.1: `bash experiments/track_h_hyperbolic_network/release/merge_and_release.sh` from your own terminal. Acceptance: the script prints the merge commit and the `v1.1` release with `main.pdf` attached.
- **Q1 · human · v1.2** — read `paper/main_v1_2.pdf`; decide: (a) publish as Zenodo v1.2 now, (b) wait for specialist feedback (H-5), (c) request changes. Nothing is published without this answer.
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
- **Q11 · human · H-4, phase 1 (this week)** — Build and measure per `experiments/track_h_hyperbolic_network/lab/LAB_GUIDE_H4.md` and `PREREGISTRATION_13.md` (committed before any soldering). Day 1 is simulation only: `lab/bom_and_netlist.py`, `lab/virtual_bench.py`, `lab/analyze_measurements.py --demo` must all run. Parts: 342 × 100 kΩ 1 %, 106 × 1 µF film, quad rail-to-rail op-amp, ADS1115, ESP32 (`lab/out/BOM.md`). Acceptance: gates G1–G4 of the preregistration pass in order and `analyze_measurements.py` writes `lab/data/h4_step_response.json`; then RUNBOOK steps 6–8 with claim id `H4-X-0001` (any verdict). Predictions: τ ratio 0.604 ± 0.03; τ/τ_cal = 2.750 ± 0.08 and 4.551 ± 0.14.
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

## Next for the low-tier loop (preregistration to be written by the orchestrator first)
- Q8 (correlated hardware noise), Q4 (two-node defects, greedy decoder), Q5 (sensitivity vs depth, exploratory).

## Retired (done since the roadmap of 2026-09-27)
H-1 (v1.0 + v1.1 published), H-2 first pass (tilings, H0-X-0008), H-3a/H-3b (persistent homology, detection, localisation, noise margin, tolerance: H3-X-0001..0007), v1.2 draft.
