# Results: node N1-L, the limit of bulk–boundary protection in the finite SSH chain (preregistration N1-L)

Recorded 2026-10-10 by the orchestrator directly (Tier X, not in the Elenchus ledger). Data: `evidence/n1_limit.json`, diagnostic `evidence/n1_limit_gate_diag.json`.
Chain of 41 sites, topological phase v = 1/2, w = 1 (gap 1), 50 draws per cell, strengths ε from 0.01 to 1.

| Item | Threshold | Measured | Verdict |
|---|---|---|---|
| G1 | exact harness exit 0; topological chain E₀ ≤ 1e-12, left weight ≥ 0.99, polarisation 1; trivial chain E₀ ≥ 0.4 | exit 0; 7e-17, 0.999, 1.000; trivial E₀ 5e-16 (zero mode at the right end) | **FAILED as written** (my wrong clause, Deviation 1) |
| G2 | chiral spectrum symmetric to 1e-12, on-site not | statistic miscoded (3.9 for a symmetric spectrum); correct values 6e-15 and 0.81 | **FAILED as written**, holds post hoc |
| P1 protection inside the class | chiral: median E₀ ≤ 1e-6 up to ε = 0.5, left-weight fraction ≥ 0.9 up to 0.3 | median E₀ = 0 at all ε; fractions 1.0 up to ε = 0.5 | HELD |
| P2 the mode leaves the end only near gap closing | first ε with fraction < 0.5 is ≥ 0.5 | never below 0.5 on the grid (0.98 at ε = 0.7, 0.70 at ε = 1) | HELD |
| P3 on-site breaking: linear energy, mode stays | slope in [0.2, 0.8]; fractions ≥ 0.9 up to 0.3 | slope 0.364; fractions 1.0 up to 0.3, 0.88 at 0.5, 0.30 at 1 | HELD |
| P4 same-sublattice hopping is harsher | nnn E₀ at 0.1 > on-site E₀ at 0.1; fraction < 0.5 at some ε ≤ 0.5 | 0.100 > 0.037; the fraction drops from 1.0 to 0.0 between ε = 0.1 and 0.2 | HELD |
| P5 trivial control | no draw with E₀ < 0.1 and left weight ≥ 0.9 at ε ≤ 0.3 | none | HELD |

Deviation 1: both gates failed through my errors (a wrong physics clause for the trivial control; a miscoded statistic); the diagnostic is post hoc.

**Reading.** This is the limit L of node N1, measured. Inside the chiral class the end mode is exact at every coupling disorder up to 50 % and stays at the left end until the disorder is strong enough to close the gap in places (a localisation length comparable to the chain), which agrees with the theorem's hypothesis: no coupling vanishes, no symmetry-breaking term.
Outside the class the two breakings differ in kind: on-site disorder shifts the mode's energy linearly (slope 0.36 per unit of ε, a fraction of the local on-site energy) but leaves it at the end up to a third of the gap; next-nearest-neighbour hopping, which couples the sublattices' partners, moves the energy exactly as ε (median E₀ = ε up to 0.1) and delocalises the mode abruptly between ε = 0.1 and 0.2, a fifth of the gap. So the "protection" of the SSH end mode is protection of its *energy* by chiral symmetry and of its *position* by the gap; the integer ν fixes the side, the gap and the symmetry fix how far the perturbation may go. This is the form the thesis must take at every node: the invariant decides the discrete fact, the spectrum decides the margin.
Not claimed: anything about the physical channel of axis 1a, the infinite chain, interacting systems, or holography. The gate failures are design errors of mine, kept.

## Correction (2026-10-10, after an adversarial read of the programme paper)

The reading above was written as if P1 to P5 counted. By the programme's own rule (a failed gate means nothing below it is read; applied to preregistration 33 the same day), **P1 to P5 are unread** while G1 and G2 stand as failed as written, whatever the post hoc diagnostic says about why. The table's "HELD" entries are kept as the record of what the data showed, with this correction beside them. The run is to be repeated under a corrected card (trivial control stated through the side of the mode, as the theorem says; a symmetry statistic tested on a known symmetric spectrum before the card is committed) before node N1 counts. The reading, if the repeat confirms it, is as written above, with one change the referee required: "chiral symmetry fixes the energy" holds by construction of the chiral perturbation class, not as a finding.
