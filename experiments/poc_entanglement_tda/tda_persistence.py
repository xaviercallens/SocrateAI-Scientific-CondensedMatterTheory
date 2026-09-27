#!/usr/bin/env python3
"""Gudhi persistence on the SSH-ring and SYK data, with the baseline metric
that PREREGISTRATION.md requires next to every barcode.

Honesty note, stated once here rather than only in prose: H0 persistence of a
1D point cloud is exactly the sorted list of gaps between consecutive points
-- Vietoris-Rips in one dimension does not discover anything a sort() call
would not. It is used here because it is the correct minimal tool for "is
there an isolated cluster", not because it is doing something a human could
not check by eye; every figure below is paired with that same check computed
directly (the baseline), so the reader can see the two agree.

Reads:  experiments/poc_entanglement_tda/data/ssh_ring.json
        experiments/poc_entanglement_tda/data/syk.json
Writes: experiments/poc_entanglement_tda/figures/*.png
"""

from __future__ import annotations

import json
from pathlib import Path

import gudhi
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FIG = HERE / "figures"


def rips_h0_barcode(points_1d: np.ndarray) -> list[tuple[float, float]]:
    """H0 persistence of a 1D point cloud. Returns [(birth, death), ...],
    death=inf for the one bar that never dies (dropped by convention here).
    """
    pts = points_1d.reshape(-1, 1).astype(float)
    rips = gudhi.RipsComplex(points=pts, max_edge_length=float(np.ptp(pts)) + 1.0 if len(pts) > 1 else 1.0)
    st = rips.create_simplex_tree(max_dimension=1)
    st.compute_persistence()
    bars = st.persistence_intervals_in_dimension(0)
    return [(b, d) for b, d in bars if np.isfinite(d)]


def fig_ssh_baseline_and_barcodes():
    rows = json.loads((DATA / "ssh_ring.json").read_text())
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    # Panel (0,0): baseline curve, near-half count vs r, both sizes.
    ax = axes[0, 0]
    for L, marker in ((100, "o"), (300, "^")):
        sub = sorted([r for r in rows if r["L"] == L], key=lambda r: r["r"])
        rs = [r["r"] for r in sub]
        counts = [r["near_half_count"] for r in sub]
        ax.plot(rs, counts, marker, ms=4, label=f"L={L}", alpha=0.8)
    ax.axvline(1.0, color="grey", ls="--", lw=1)
    ax.set_xlabel("r = v/w"); ax.set_ylabel(r"# of $\zeta_n$ within 0.05 of 1/2")
    ax.set_title("Baseline (not TDA): mid-gap count vs r")
    ax.legend()

    # Panel (0,1): baseline curve, min distance to 1/2.
    ax = axes[0, 1]
    for L, marker in ((100, "o"), (300, "^")):
        sub = sorted([r for r in rows if r["L"] == L], key=lambda r: r["r"])
        rs = [r["r"] for r in sub]
        dists = [r["min_dist_to_half"] for r in sub]
        ax.plot(rs, dists, marker, ms=4, label=f"L={L}", alpha=0.8)
    ax.axvline(1.0, color="grey", ls="--", lw=1)
    ax.set_xlabel("r = v/w"); ax.set_ylabel(r"min$_n |\zeta_n - 1/2|$")
    ax.set_title("Baseline: distance of the closest level to 1/2")
    ax.legend()

    # Panel (1,0): H0 barcode for a representative topological r (L=300).
    ax = axes[1, 0]
    topo_row = next(r for r in rows if r["L"] == 300 and abs(r["r"] - 0.9) < 1e-6)
    zeta = np.array(topo_row["zeta"])
    bars = rips_h0_barcode(np.abs(zeta - 0.5))
    bars = sorted(bars, key=lambda b: b[0] - b[1])[:15]  # 15 longest
    for i, (b, d) in enumerate(bars):
        ax.plot([b, d], [i, i], lw=3)
    ax.set_title(f"H0 barcode, |ζ-1/2| point cloud, r=0.9 (topological), L=300")
    ax.set_xlabel("filtration scale"); ax.set_yticks([])

    # Panel (1,1): same, trivial phase.
    ax = axes[1, 1]
    triv_row = next(r for r in rows if r["L"] == 300 and abs(r["r"] - 1.1) < 1e-6)
    zeta = np.array(triv_row["zeta"])
    bars = rips_h0_barcode(np.abs(zeta - 0.5))
    bars = sorted(bars, key=lambda b: b[0] - b[1])[:15]
    for i, (b, d) in enumerate(bars):
        ax.plot([b, d], [i, i], lw=3, color="tab:orange")
    ax.set_title(f"H0 barcode, |ζ-1/2| point cloud, r=1.1 (trivial), L=300")
    ax.set_xlabel("filtration scale"); ax.set_yticks([])

    fig.suptitle("Part A: SSH ring entanglement spectrum -- baseline vs. persistence barcode")
    fig.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / "ssh_ring_baseline_and_barcodes.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"wrote {path}")


def fig_syk_degeneracy():
    rows = json.loads((DATA / "syk.json").read_text())
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # Panel 0: baseline bar chart, degenerate fraction vs N mod 8.
    ax = axes[0]
    Ns = [r["N"] for r in rows]
    fracs = [r["degenerate_fraction"] for r in rows]
    colors = ["tab:red" if r["N_mod_8"] == 4 else "tab:blue" for r in rows]
    ax.bar([str(n) for n in Ns], fracs, color=colors)
    ax.set_xlabel("N"); ax.set_ylabel("fraction with exact ground degeneracy")
    ax.set_title("Baseline 1: degeneracy fraction\n(red: N mod 8=4, blue: N mod 8=0)")
    ax.set_ylim(0, 1.05)

    # Panel 1: baseline 2, the RAW values on a shared axis. This is the honest
    # baseline for what the barcode in panel 2 claims to show: every point at
    # its own log10(gap/scale), jittered in x by N only for readability. A
    # first version of this figure ran Rips-H0 separately per class and
    # plotted the within-class gaps -- which discards exactly the fact that
    # matters (the two classes sit ~14 orders of magnitude apart), because
    # Rips H0 bars are always (0, inter-point distance): they carry no
    # information about a class's absolute position on the axis, only its
    # internal spread. Caught before shipping by looking at this panel.
    ax = axes[1]
    by_n = {}
    for r in rows:
        vals = [rr["gap_over_scale"] for rr in r["realizations"] if rr["gap_over_scale"] is not None]
        by_n[r["N"]] = np.log10(np.clip(vals, 1e-16, None))
    for n, vals in sorted(by_n.items()):
        color = "tab:red" if n % 8 == 4 else "tab:blue"
        jitter = np.random.default_rng(n).uniform(-0.15, 0.15, size=len(vals))
        ax.scatter(np.full(len(vals), n) + jitter, vals, s=10, color=color, alpha=0.5)
    ax.set_xlabel("N"); ax.set_ylabel("log10(same-sector gap / energy scale)")
    ax.set_title("Baseline 2: every realization, raw value\n(the actual finding is in this panel)")
    ax.set_xticks(sorted(by_n))

    # Panel 2: H0 barcode of the POOLED data (all N together). This is the
    # correct use of persistence here: it should surface ONE very long bar
    # (the gap between the ~1e-15 cluster and the ~1e-1 cluster) standing far
    # above many short bars (spacing within each cluster) -- i.e. persistent
    # homology detecting that there are two clusters, not one, from the point
    # cloud alone, without being told the class labels.
    ax = axes[2]
    pooled = np.concatenate(list(by_n.values()))
    bars = sorted(rips_h0_barcode(pooled), key=lambda b: b[0] - b[1])[:25]
    for i, (b, d) in enumerate(bars):
        length = d - b
        color = "black" if i == 0 else "tab:gray"  # i==0 is the longest bar (sorted above)
        ax.plot([b, d], [i, i], lw=3 if i == 0 else 1.5, color=color)
    ax.set_title("H0 barcode, ALL realizations pooled\n(unsupervised: no class label used)")
    ax.set_xlabel("filtration scale (log10 gap/scale)"); ax.set_yticks([])
    if bars:
        longest = bars[0]
        ax.text(0.02, 0.95, f"longest bar: {longest[1]-longest[0]:.1f} decades",
                transform=ax.transAxes, fontsize=9, va="top")

    fig.suptitle("Part B: SYK ground-state degeneracy vs N mod 8 (Tier X, exploratory)")
    fig.tight_layout()
    path = FIG / "syk_degeneracy.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"wrote {path}")


def main() -> int:
    fig_ssh_baseline_and_barcodes()
    fig_syk_degeneracy()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
