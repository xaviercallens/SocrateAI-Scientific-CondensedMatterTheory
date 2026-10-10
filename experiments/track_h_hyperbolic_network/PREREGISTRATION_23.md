# Preregistration 23: an exponential-sum picture of the flat growth rate, tested on cylinders (task Q5f)

**Date:** 2026-10-08, committed before the run. **Roadmap item:** H-2. **Why:** H0-X-0013 showed that on flat disks the
depth-restricted condition number grows by a lattice constant per unit depth (square 1.1–1.2 decades, triangular
1.7–1.8), and `MECHANISM_NOTE.md` explains the form of the collapse but not the constant. This card tests a picture in
which the constant has an exact origin, on a geometry where the problem separates: a lattice **cylinder**, periodic in
one direction (W columns), rows 0…H, with the measurement on row 0 and a closed far end.

## The picture (derived now, before any cylinder was computed)
Fourier-transform along the periodic direction. The harmonic extension of a boundary mode of wave number k decays by a
factor z₁(k) = e^(−κ(k)) per row, with the lattice dispersion relation cosh κ(k) = 2 − cos k on the square lattice. The
signature of a vertical edge at depth r (between rows r and r+1) is, per mode, proportional to z₁(k)^r, and the Jacobian
column is the outer product of two signatures, so at total momentum q the data components (k, q−k) carry the factor
z(k)^r with z(k) = e^(−(κ(k)+κ(q−k))). For each q the vertical-edge columns of depth 0…d therefore form a
Vandermonde-type matrix [a_k z_k^r] whose nodes z_k fill an interval [a, 1]; on the square lattice
a = e^(−2κ_max) with κ_max = acosh(3) (the zigzag mode k = π), so a = 0.0294. The condition number of such a matrix grows
geometrically with the number of columns, with ratio ρ = x + √(x² − 1), x = (3 + a)/(1 − a) (the Chebyshev growth on
[a, 1]). For the square lattice this gives
**log₁₀ ρ = 0.784 decades per unit depth for the vertical-edge columns alone.** Adding the horizontal edges can only
increase the condition number (more columns), so the full rate is at least this, and probably more (two column types
per depth). The picture says nothing yet about the disk's 1.1–1.2; whether a cylinder reproduces the disk rate is the
exploratory part. It also implies that, for nodes filling [0, 1] (a → 0, the triangular zigzag mode decouples), the
single-type rate is 0.766, so the single-type rate is nearly lattice-independent; any large difference between the
lattices must come from the number of column types per depth.

## Design
Square and triangular cylinders, unit conductances: W ∈ {64, 96} with H = 18 (square) and H = 12 (triangular) rows
below the boundary; boundary = row 0 (W nodes); unknowns = every edge (including the boundary row's own horizontal
edges); edge depth = min of the endpoints' graph distance to row 0 (= row index). The triangular lattice has odd rows
shifted by half a column (six neighbours per node). The explicit Jacobian of `hyperbolic_network.jacobian` is used
(strictly upper-triangular data entries, W(W−1)/2 rows). For d = 0, 1, …: log₁₀ κ_d of the Jacobian restricted to
columns of depth ≤ d (square: also restricted to vertical edges only), kept while log₁₀ κ_d ≤ 12.5 and the number of
columns does not exceed the number of rows (d* = last kept depth). **Rate** = least-squares slope of log₁₀ κ_d against d
over 3 ≤ d ≤ d*. Data file: `data/cylinder_exponential_sum_picture.json`.

**Deviation 1 (2026-10-08, after the first run, which crashed in `score()` before writing the data file; no threshold or
prediction below is changed).** The first run printed the square series and then failed on the triangular series, for
which no depth was kept: the triangular cylinder's Jacobian restricted to depth 0 is exactly singular (smallest singular
value at round-off level, next smallest 2×10⁻³), so log₁₀ κ₀ exceeds the floor and the series is empty. A post-hoc
diagnostic (not part of the tests; scripts in the job directory) found one exact null vector: the sum over boundary nodes
of the difference of the two diagonal edges' Jacobian columns vanishes, a consequence of translation invariance plus the
mirror symmetry of the lattice about each interior node. A straight periodic triangular boundary row is therefore a
non-generic geometry with an exact first-order degeneracy (the triangular disk has no such symmetry and is full rank).
Consequences, fixed before the rerun: gate G3 fails for the triangular series, so **P4 is void** (not evaluable; recorded
as neither held nor refuted); the scorer is made safe against empty series; the computation is deterministic, so the
rerun reproduces the first run's printed square numbers, which were seen before this deviation was written
(square rates 1.78 and 1.77–1.79, against the preregistered 0.784; P1 and P3 are therefore refuted and P2 holds,
whatever the rerun is). Nothing else changes.

## Validity gates
- G1: on a tiny cylinder (W = 8, H = 3) of each lattice, the explicit Jacobian agrees with `jacobian_finite_diff`
  to 10⁻⁵ of its largest entry (the library functions are valid on these graphs).
- G2: on the square cylinders, log₁₀ κ_d(full) ≥ log₁₀ κ_d(vertical only) − 10⁻⁶ at every kept depth (a necessity).
- G3: d* ≥ 6 for every one of the six series (enough points for a rate).

## Predictions (fixed now)
- **P1 (the closed-form rate, derived).** Square cylinders, vertical-edge columns only: the rate is in [0.63, 0.94]
  (0.784 ± 20 %) for both W = 64 and W = 96. **Refuted if** either is outside.
- **P2 (convergence in W).** The vertical-only rate at W = 96 differs from the one at W = 64 by at most 0.10.
  **Refuted if** it differs by more.
- **P3 (cylinder vs disk, square, exploratory).** The full square cylinder rate is in [0.9, 1.5] for both W (the disk
  values 1.08–1.23 ± 25 %). **Refuted if** either is outside.
- **P4 (cylinder vs disk, triangular, exploratory).** The full triangular cylinder rate is in [1.3, 2.3] for both W (disk
  1.69–1.84 ± 25 %) **and** the triangular/square full-rate ratio is at least 1.2 for both W. **Refuted if** any fails.

## What a refutation would mean (written now)
P1 refuted: the exponential-sum picture (Vandermonde conditioning from the spread of mode decay factors) is not the origin
of the flat growth rate, or the unknown-type structure changes the rate already for vertical edges. P2 refuted: the
continuum picture needs W ≫ 96 or the rate depends on the discretisation of the modes. P3/P4 refuted: the flat disk's
rate is a property of the disk geometry (curvature, diagonals, graph-distance depth) and not of the lattice with a
boundary on one side; that would be informative in its own right (the next card would isolate which).

## Not claimed
A proof of the Vandermonde asymptotics for the discrete problem; anything about the disk beyond P3/P4; hyperbolic
geometry; the effect of the closed far end (H is finite but the kept depths are far from it); anything about holography.
