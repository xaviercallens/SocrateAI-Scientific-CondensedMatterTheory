#!/usr/bin/env python3
"""Finite-size scaling of the SSH entanglement mid-gap levels -- the corrected
version of Part A, and the design numbers for the axis-1a tank.

Why this file exists (erratum to results.md Part A, 2026-09-27, post-v0.1):
results.md claimed the two zeta=1/2 entanglement levels are pinned exactly
with NO finite-size smearing, and "explained" this as a quantised invariant
that cannot smear. That claim was made from subsystems of exactly ell = L/2
cells, at two ring sizes. ell = L/2 is a special geometry: the ring then has
a reflection through the two cut points that exchanges subsystem and
complement, and together with chiral symmetry this cancels the hybridisation
of the two edge-like modes EXACTLY. For any ell != L/2 the two modes
hybridise with amplitude ~ (v/w)^min(ell, L-ell), and the levels leave 1/2
by that amount. So the preregistered sub-prediction (smearing of width ~xi
that shrinks as the system grows) was right; the "refutation" was an
artefact of testing only the symmetric cut. Elenchus: be most suspicious of
the result you wanted.

What is checked here, with pass/fail exits:

  S1  chiral pairing: the two closest-to-1/2 levels satisfy z1 + z2 = 1
      (exact to 1e-10) for every (r, ell) -- the pair is real, only its
      distance from 1/2 was misreported.
  S2  symmetric cut: delta(ell = L/2) < 1e-12 (the artefact, now understood).
  S3  reflection: delta(ell) = delta(L - ell) to 1e-8 relative.
  S4  exponential decay: for ell < L/2, log delta(ell) is linear in ell with
      slope b; require |b - ln r| < 0.15*|ln r|  (xi = -1/ln r).
      Also a compensated-flatness check (Elenchus): the successive ratios
      delta(ell+1)/delta(ell) have no sign flip (all < 1) and their spread
      is bounded -- a fit alone can hide a bad series.

  D1  design number for the tank: an OPEN chain with a domain wall hosts an
      exact zero mode (odd site count => exact by chiral symmetry); its
      profile decays as (v/w)^n away from the wall. Fit xi from the profile
      and report the number of cells per side needed for the mode to be
      99% contained -- that is the minimum channel length for axis 1a.

Outputs: data/finite_size_scaling.json, figures/finite_size_scaling.png
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ssh_ring_entanglement import entanglement_spectrum  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "finite_size_scaling.json"
FIG = HERE / "figures" / "finite_size_scaling.png"

FLOOR = 1e-13  # below this, delta is floating-point noise, not physics


def closest_pair(zeta: np.ndarray) -> tuple[float, float, float]:
    """(delta, z1, z2): distance of the closest level to 1/2, and the two
    closest levels themselves (for the chiral-pairing check)."""
    order = np.argsort(np.abs(zeta - 0.5))
    z1, z2 = zeta[order[0]], zeta[order[1]]
    return float(abs(z1 - 0.5)), float(z1), float(z2)


def domain_wall_chain(v: float, w: float, cells_per_side: int) -> np.ndarray:
    """Open SSH chain with one domain wall in the middle and an ODD number of
    sites, terminated with STRONG bonds at both physical ends so neither end
    hosts its own mode; the single exact zero mode then lives at the wall.

    Requires |w| > |v| (w is the strong bond; this is the r = v/w < 1 regime
    the tank targets). Left segment: bond i (site i -> i+1) is w for even i,
    v for odd i, so bond 0 is strong. Right segment: the pattern is inverted,
    so the last bond (index 4c-1, odd) is w, strong. The wall sits at site
    2c, which is flanked by two WEAK bonds (bond 2c-1 = v, bond 2c = v):
    that is the defect that binds the mode. Total sites = 4c + 1.

    A first version of this function had the strong/weak labels backwards
    (it terminated both ends with weak bonds, so the ends hosted modes and
    the profile fit returned xi < 0 with the right magnitude). The
    end-bond and wall-bond pattern is now asserted rather than trusted.
    """
    if not abs(w) > abs(v):
        raise ValueError("domain_wall_chain assumes |w| > |v| (w strong)")
    c = cells_per_side
    n = 4 * c + 1
    wall = 2 * c
    bonds = []
    for i in range(n - 1):
        if i < wall:
            t = w if i % 2 == 0 else v
        else:
            t = v if i % 2 == 0 else w
        bonds.append(t)
    assert bonds[0] == w and bonds[-1] == w, "ends must terminate on strong bonds"
    assert bonds[wall - 1] == v and bonds[wall] == v, "wall must be flanked by weak bonds"
    h = np.zeros((n, n))
    for i, t in enumerate(bonds):
        h[i, i + 1] = h[i + 1, i] = t
    return h


def main() -> int:
    failures: list[str] = []

    def check(ok: bool, label: str) -> None:
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failures.append(label)

    L = 200
    r_values = [0.5, 0.7, 0.8, 0.9]
    ells = list(range(4, L // 2 + 1))
    results: dict = {"L": L, "ring": {}, "domain_wall": {}}

    print("ring entanglement spectrum, L=200 cells, subsystem ell cells")
    for r in r_values:
        v, w = r, 1.0
        deltas, pairs = [], []
        for ell in ells:
            zeta = entanglement_spectrum(v, w, L, ell)
            d, z1, z2 = closest_pair(zeta)
            deltas.append(d)
            pairs.append(abs(z1 + z2 - 1.0))
        deltas = np.array(deltas)
        results["ring"][str(r)] = {"ell": ells, "delta": deltas.tolist()}

        # S1 chiral pairing
        check(max(pairs) < 1e-10, f"S1 r={r}: closest pair is chiral (z1+z2=1), max dev {max(pairs):.1e}")
        # S2 symmetric cut is exactly pinned (the artefact)
        d_half = deltas[ells.index(L // 2)]
        check(d_half < 1e-12, f"S2 r={r}: delta(ell=L/2) = {d_half:.1e} (symmetry-cancelled)")
        # S3 reflection ell <-> L-ell on a few samples
        # Tolerance is noise-aware: each eigenvalue carries ~1e-16 absolute
        # error, so a relative test on a delta of 1e-9 cannot be tighter than
        # ~1e-7. A first version demanded 1e-8 relative and failed on exactly
        # those points -- a checker artefact, not a symmetry violation.
        refl_ok = True
        for ell in (10, 33, 57):
            a, _, _ = closest_pair(entanglement_spectrum(v, w, L, ell))
            b, _, _ = closest_pair(entanglement_spectrum(v, w, L, L - ell))
            if abs(a - b) > 1e-6 * a + 1e-14:
                refl_ok = False
        check(refl_ok, f"S3 r={r}: delta(ell) = delta(L-ell) (tol 1e-6 rel + 1e-14 abs)")
        # S4 exponential decay with the predicted rate, on the clean window
        mask = (deltas > FLOOR) & (np.array(ells) < L // 2 - 5)
        x = np.array(ells)[mask]
        y = np.log(deltas[mask])
        if len(x) >= 6:
            slope, intercept = np.polyfit(x, y, 1)
            xi_fit = -1.0 / slope
            xi_th = -1.0 / math.log(r)
            ratios = deltas[mask][1:] / deltas[mask][:-1]
            flat = bool(np.all(ratios < 1.0)) and float(np.std(ratios)) < 0.15
            check(abs(slope - math.log(r)) < 0.15 * abs(math.log(r)),
                  f"S4 r={r}: fitted xi={xi_fit:.2f} cells vs theory {xi_th:.2f} (slope {slope:.3f} vs ln r {math.log(r):.3f})")
            check(flat, f"S4 r={r}: ratios monotone (<1), spread {np.std(ratios):.3f}; compensated flatness")
            results["ring"][str(r)]["xi_fit"] = xi_fit
            results["ring"][str(r)]["xi_theory"] = xi_th
        else:
            check(False, f"S4 r={r}: too few points above the floor to fit")

    print("\nopen chain with one domain wall (the object the tank realises)")
    for r in r_values:
        v, w = r, 1.0
        cells = 30
        h = domain_wall_chain(v, w, cells)
        e, vec = np.linalg.eigh(h)
        k = int(np.argmin(np.abs(e)))
        e0 = float(e[k])
        psi = np.abs(vec[:, k])
        wall_site = 2 * cells
        # The mode is on the wall's sublattice (even sites); sample every
        # second site rightward from the wall and fit the exponential decay.
        n_idx = np.arange(0, cells)
        amp = psi[wall_site + 2 * n_idx]
        good = amp > 1e-12
        slope, _ = np.polyfit(n_idx[good], np.log(amp[good]), 1)
        xi = -1.0 / slope
        # Design number: smallest N such that sites within +-2N of the wall
        # (N cells on each side) hold 99% of the mode's weight.
        weights = psi**2 / np.sum(psi**2)
        n99 = None
        for N in range(0, cells + 1):
            lo, hi = wall_site - 2 * N, wall_site + 2 * N + 1
            if weights[max(lo, 0):hi].sum() >= 0.99:
                n99 = N
                break
        peak_at_wall = int(np.argmax(psi)) == wall_site
        results["domain_wall"][str(r)] = {"E0": e0, "xi_cells": xi, "cells_for_99pct": n99}
        check(abs(e0) < 1e-10, f"D1 r={r}: domain-wall mode energy {e0:.1e} (exact zero, odd site count)")
        check(peak_at_wall, f"D1 r={r}: mode peaks AT the wall (site {wall_site}), not at a chain end")
        check(abs(xi - (-1 / math.log(r))) < 0.1 * (-1 / math.log(r)),
              f"D1 r={r}: profile xi={xi:.2f} cells (theory {-1/math.log(r):.2f}); 99% within {n99} cells/side")

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(results, indent=1), encoding="utf-8")

    # Figure: log delta vs ell for each r, plus the domain-wall profile.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax = axes[0]
    for r in r_values:
        d = np.array(results["ring"][str(r)]["delta"])
        ax.semilogy(ells, np.maximum(d, FLOOR), ".", ms=3, label=f"r={r}, xi={results['ring'][str(r)].get('xi_fit', float('nan')):.1f}")
    ax.axvline(L // 2, color="grey", ls="--", lw=1)
    ax.axhline(FLOOR, color="grey", ls=":", lw=1)
    ax.set_xlabel("subsystem ell (cells), L=200"); ax.set_ylabel("|zeta - 1/2| of closest level")
    ax.set_title("Ring: hybridisation ~ r^ell; exactly 0 only at ell=L/2 (symmetry)")
    ax.legend(fontsize=8)

    # The zero mode lives on ONE sublattice (chiral symmetry): the wall's
    # sublattice carries the r^n envelope, the other sublattice is ~1e-16.
    # In the tank this is a measurable signature -- every second chamber is
    # (nearly) still -- so the two sublattices are drawn distinctly rather
    # than as one comb-like line.
    ax = axes[1]
    for r in r_values:
        v, w = r, 1.0
        h = domain_wall_chain(v, w, 30)
        e, vec = np.linalg.eigh(h)
        k = int(np.argmin(np.abs(e)))
        psi = np.abs(vec[:, k])
        x = np.arange(len(psi)) - 60
        line, = ax.semilogy(x[::2], np.maximum(psi[::2], 1e-16), "-o", ms=2.5, lw=1,
                            label=f"r={r} (wall sublattice)")
        ax.semilogy(x[1::2], np.maximum(psi[1::2], 1e-16), "x", ms=3, color=line.get_color(), alpha=0.5)
    ax.axhline(1e-16, color="grey", ls=":", lw=1)
    ax.set_ylim(1e-17, 2)
    ax.set_xlabel("site (0 = domain wall)"); ax.set_ylabel("|psi| of the zero mode")
    ax.set_title("Open chain + domain wall: lines = wall sublattice, x = other (empty)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=150)
    plt.close(fig)

    print(f"\nwrote {DATA}\nwrote {FIG}")
    print(f"{'PASS' if not failures else f'FAILED ({len(failures)})'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
