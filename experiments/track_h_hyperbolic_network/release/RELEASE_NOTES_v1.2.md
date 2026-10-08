## v1.2 (draft, prepared 2026-10-07; not yet published)

Second revision of the Track H preprint *Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices*. The v1.1 source and PDF are untouched; `paper/main_v1_2.tex` is
generated from them by `paper/make_v12.py` (every replacement asserted to match once), and every number inserted
is read from a recorded, preregistered result. All computations were **preregistered and committed before each run**
(`PREREGISTRATION_5.md` to `PREREGISTRATION_19.md`); refuted predictions are kept and listed.

### What is new in the paper (17 pages)
- **Other tilings (§3.2).** {7,3}, {8,3}, {5,4}, {6,4}, {4,5} up to N = 2888: at equal maximal depth the hyperbolic
  tilings agree within 0.56 decades while N varies ~15×; flat lattices are ≥ 1.8 decades worse at equal depth. The
  v1.1 sentence "the mechanism is the scaling of depth with size" is qualified: it holds within the hyperbolic class.
- **Where the difference comes from (§3.2, new paragraph, Table 3, Fig. 3).** The per-edge boundary signal decays
  alike on all lattices (−2.0 to −2.4 decades at depth 3). What differs is the *coherence* of equal-depth Jacobian
  columns: effective dimension fraction ≥ 0.79 at every depth on the hyperbolic tilings, falling to 0.14–0.39 on the
  flat disks; the condition number of the Jacobian restricted to depth ≤ d grows by 0.98–1.19 decades per depth on
  flat lattices against 0.28–0.44 on hyperbolic ones, and the deficit survives size matching. Four of eight predictions
  were refuted, all statistic choices on our side (LL-A13, LL-A14 in `LL.md`); the result rests on the ones that held.
  A harmonic-measure band-counting argument (`MECHANISM_NOTE.md`, Tier C) predicts the flat collapse: on instances it
  had not seen, depth × effective dimension fraction is constant within 1.26× (square R=16) and 1.42× (triangular);
  its growth-rate prediction was refuted, and a follow-up over windows fixed in relative depth shows the rate is a
  lattice constant (≈ 1.1–1.2 decades per depth square, 1.7–1.8 triangular), still underived (H0-X-0012, H0-X-0013).
- **Defect detection and localisation in simulation (§3.7).** Persistent homology sees nothing; the resistance metric
  detects a deep defect at the 3×10⁻⁴ budget; single-node localisation is perfect at the budget on flat and hyperbolic
  lattices alike, the hyperbolic advantage being a ≥ 100× noise margin at N ≈ 316; tolerance ≤ 5 % is harmless; a ±10 %
  change is localised at the budget on both, only the hyperbolic board keeps that at 10× the noise; offset ≤ 10 %,
  drift ≤ 1 % and a 10-bit ADC leave localisation intact at N ≈ 112 (a floor, not a boundary).
- **Exact rank certificates** for eleven instances of the five tilings up to E = 1604 (Tier B, random row-combination
  certificate) and **integrator controls** on four more tilings with SciPy and rusty-SUNDIALS CVODE.
- Verification table extended to 29 ledger rows; erratum for the "27.1" spacing slip of v1.1.
- Part of the later runs were recorded by a small model and audited by a larger one under `docs/RUNBOOK.md`; the
  paper says so.

### Records to create when publishing
- Zenodo: new version under concept DOI 10.5281/zenodo.23000390 (`release/publish.sh newversion`, then verify the
  draft's MD5 checksums and metadata, then `release/publish.sh publish` on explicit go-ahead).
- Hugging Face dataset: new tables `coherence_depth.csv`, `coherence_matched.csv`, `exact_rank_tilings.csv`,
  `rc_benchmark_tilings.csv`, `minimum_contrast.csv`, `hardware_noise.csv` (`release/export.py`).
- Ledger: H0-X-0009, H0-X-0010, H0-X-0011, H0-B-0003, H2-X-0005, H3-X-0008, H3-X-0009 added since v1.1.

### Not in this version
The garage measurement (prereg 13, not yet run), a derivation of the coherence mechanism (card Q5d), two-node defects (Q4).
