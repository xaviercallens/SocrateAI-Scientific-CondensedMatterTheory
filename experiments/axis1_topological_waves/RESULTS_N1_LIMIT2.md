# Results: node N1-L2, the repeat of N1-L with corrected gates (preregistration N1-L2)

Recorded 2026-10-10 by the orchestrator directly (Tier X, not in the Elenchus ledger). Data: `evidence/n1_limit2.json`. Fresh seeds (base 2000); same chain, grid, draws and predictions as N1-L.

| Item | Threshold | Measured | Verdict |
|---|---|---|---|
| G0 statistic self-test | known case 0.2 to 1e-12; unperturbed topological chain ≤ 1e-12 | 0.2; 8.9e-16 | PASS |
| G1 unperturbed chains, from the theorem | exact harness exit 0; topological: E₀ ≤ 1e-12, W_L ≥ 0.99, Π = 1; trivial: E₀ ≤ 1e-12, W_R ≥ 0.99, W_L ≤ 0.01 | exit 0; 0.0, 0.999, 1.0; 0.0, 0.999, 0.0 | PASS |
| G2 perturbations act as meant | chiral asymmetry ≤ 1e-12 on every draw (ε < 1); on-site asymmetry > 1e-3 on every draw at ε = 0.5 | 4.2e-15; 0.130 | PASS |
| P1 protection inside the class | chiral: median E₀ ≤ 1e-6 up to ε = 0.5; end fraction ≥ 0.9 up to 0.3 | 0 at all ε; 1.0 up to ε = 0.5 | HELD |
| P2 the mode leaves the end only near gap closing | first ε with fraction < 0.5 is ≥ 0.5 or none | none (0.96 at ε = 0.7, 0.82 at 1) | HELD |
| P3 on-site breaking: linear energy, mode stays | slope in [0.2, 0.8]; fractions ≥ 0.9 up to 0.3 | 0.377; 1.0 up to 0.3 (0.92 at 0.5, 0.36 at 1) | HELD |
| P4 same-sublattice hopping is harsher | nnn E₀ at 0.1 > on-site's; fraction < 0.5 at some ε ≤ 0.5 | 0.100 > 0.039; drops from 1.0 to 0.0 between ε = 0.1 and 0.2 | HELD |
| P5 trivial control | no draw with E₀ < 0.1 and W_L ≥ 0.9 at ε ≤ 0.3 | none | HELD |

Deviations: none. Disclosure: the outcome of the first run was known when this card was written (stated in the card); the fresh draw agrees with it on every cell to the resolution of 50 draws (first-run slope 0.364, now 0.377; end fractions identical except at ε = 0.7 and 1, where they differ by 0.02 to 0.12).

**Reading (node N1, now readable).** Inside the chiral class the end mode is exact at every coupling disorder up to 50 % and stays at the left end until the disorder is strong enough to close the gap in places. Outside the class the two breakings differ in kind: on-site disorder shifts the mode's energy linearly (slope 0.38 per unit of ε) and leaves it at the end up to a third of the gap; same-sublattice hopping moves the energy as ε itself and delocalises the mode between a tenth and a fifth of the gap. So the winding fixes the side of the mode, the gap fixes the margin, and the chiral class fixes the energy by construction of that class. This is the first node of the programme with a readable record; it is a diagonalisation of a model, not a measurement of a physical system.
Limits: 41 sites, one gap, three perturbation classes, 50 draws per cell, double precision; the first run's gate failures stand in its own record (N1-L) as design errors of mine, with LL-A23.
