#!/usr/bin/env python3
"""Generate every number-bearing table and figure of the paper from data/*.json.

No number in the paper's tables is typed by hand: re-running the analysis
scripts and then this one updates the manuscript (in particular the CVODE
row of Table 4, once rusty-SUNDIALS is importable and rc_network.py re-run).

Outputs (next to this file): tables.tex, fig_kappa.pdf, fig_h2.pdf
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"


def load(name):
    return json.loads((DATA / name).read_text())


def fam(name):
    return "{7,3}" if name.startswith("{7,3}") else name.split()[0]


def tex_name(s):
    """'{7,3} L=2' -> '$\\{7,3\\}$, $L=2$'; 'triangular R=3.2249...' -> 'triangular, $R=3.2$'."""
    head, _, par = s.partition(" ")
    head = head.replace("{7,3}", r"$\{7,3\}$")
    if "=" not in par:
        return head
    k, v = par.split("=", 1)
    v = f"{float(v):g}" if "." not in v else f"{float(v):.1f}".rstrip("0").rstrip(".")
    return rf"{head}, ${k}={v}$"


def sci(x, digits=1):
    m, e = f"{x:.{digits}e}".split("e")
    return rf"${m}\times10^{{{int(e)}}}$"


def table_kappa(h0):
    rows = []
    for r in h0:
        k = r"\textsc{sing.}" if r["log10_kappa"] is None else f"{r['log10_kappa']:.2f}"
        rows.append(f"{tex_name(r['name'])} & {r['N']} & {r['E']} & {r['boundary']} & {r['max_depth']} & {k} \\\\")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Conditioning of the DtN sensitivity Jacobian, unit conductances, full boundary. "
        r"$d_{\max}$: maximal graph distance to the boundary. \textsc{sing.}: smallest singular value at or "
        r"below $\varepsilon_{\mathrm{mach}}\,\sigma_{\max}$ in IEEE double precision (the true $\kappa$ is not "
        r"resolved there). The $\{7,3\}$, $L=4$ row is the preregistered confirmatory point.}",
        r"\label{tab:kappa}",
        r"\begin{tabular}{lrrrrr}\toprule",
        r"Lattice & $N$ & $|E|$ & $|\partial G|$ & $d_{\max}$ & $\log_{10}\kappa$ \\ \midrule",
        *rows,
        r"\bottomrule\end{tabular}\end{table}",
    ])


def table_probe(pm, ident):
    by = {r["name"]: r for r in ident}
    full = {r["name"]: r for r in pm}
    lines = []
    for L, R in ((2, 6), (3, 10)):
        h = by[f"{{7,3}} L={L}, {'44' if L == 2 else '76'} probes"]
        s = by[f"square R={R}, all {'44' if L == 2 else '76'} probes"]
        fh = full[f"{{7,3}} L={L} full boundary"]
        fs = full[f"square R={R}"]
        rank = next(iter(h["exact_ranks"].values()))
        lines.append(
            rf"$\{{7,3\}}$, $L={L}$ & {h['N']} & {h['probes']} & {h['E']} & {rank} & {h['unmeasured_degree2_nodes']} & "
            rf"{sci(h['float_gap_at_rank'])} & {h['log10_kappa_identifiable']:.2f} & {fh['log10_kappa_NtD']:.2f} \\")
        lines.append(
            rf"square, $R={R}$ & {s['N']} & {s['probes']} & {s['E']} & {next(iter(s['exact_ranks'].values()))} & 0 & "
            rf"--- & {s['log10_kappa_identifiable']:.2f} & {fs['log10_kappa_NtD']:.2f} \\")
        if L == 2:
            lines.append(r"\addlinespace")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Probe-matched control and Neumann-to-Dirichlet (NtD) map. The $\{7,3\}$ boundary is subsampled "
        r"to the square disk's probe count; unused boundary nodes carry zero current. Rank: exact, over "
        r"$\mathbb{F}_p$ for two primes (agreeing). $n_2$: unmeasured interior nodes of degree~2. "
        r"$\sigma_r/\sigma_{r+1}$: float64 gap at the certified rank. $\kappa_{\mathrm{id}}$: condition number on the "
        r"identifiable subspace (a post hoc metric; see text). $\kappa_{\mathrm{NtD}}$: full boundary.}",
        r"\label{tab:probe}",
        r"\begin{tabular}{lrrrrrrrr}\toprule",
        r"Lattice & $N$ & probes & $|E|$ & rank & $n_2$ & $\sigma_r/\sigma_{r+1}$ & $\log_{10}\kappa_{\mathrm{id}}$ & "
        r"$\log_{10}\kappa_{\mathrm{NtD}}$ \\ \midrule",
        *lines,
        r"\bottomrule\end{tabular}\end{table}",
    ])


def table_h2(rc, explore):
    rows = []
    for r in rc["H2"]:
        rows.append(f"{r['family']} & {r['N']} & {r['lambda_min']:.4f} & {r['tau']:.2f} & {r['stiffness']:.1f} \\\\"
                    .replace("{7,3}", r"$\{7,3\}$"))
    for r in explore["rows"]:
        if r["L"] >= 5:
            rows.append(rf"$\{{7,3\}}$\textsuperscript{{e}} & {r['N']} & {r['lambda_min']:.4f} & "
                        rf"{1 / r['lambda_min']:.2f} & --- \\")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Dirichlet spectral gap $\lambda_{\min}(L_{ii})$ of the RC network ($C=1$), relaxation time "
        r"$\tau=C/\lambda_{\min}$ and stiffness ratio $\lambda_{\max}/\lambda_{\min}$. "
        r"\textsuperscript{e}: exploratory, not preregistered (sparse shift-invert eigensolver).}",
        r"\label{tab:h2}",
        r"\begin{tabular}{lrrrr}\toprule",
        r"Lattice & $N$ & $\lambda_{\min}$ & $\tau$ & $\lambda_{\max}/\lambda_{\min}$ \\ \midrule",
        *rows,
        r"\bottomrule\end{tabular}\end{table}",
    ])


def table_controls(rc):
    rows = []
    for r in rc["controls"]:
        if "status" in r:
            rows.append(rf"all & rusty-SUNDIALS CVODE (BDF) & \multicolumn{{4}}{{c}}{{not run: Python extension not built}} \\")
            continue
        be = "SciPy BDF" if r["backend"] == "scipy" else "rusty-SUNDIALS CVODE (BDF)"
        rows.append(rf"{tex_name(r['graph'])} & {be} & {sci(r['K1_rel_err'])} & {'pass' if r['K1_pass'] else 'FAIL'} & "
                    rf"{sci(r['K2_rel_err'])} & {'pass' if r['K2_pass'] else 'FAIL'} \\")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Integrator controls for the RC network ($\mathrm{rtol}=10^{-8}$, $\mathrm{atol}=10^{-10}$). "
        r"K1: max-norm relative error against the matrix-exponential solution at $t\in\{0.25,1,4,16\}\tau$, "
        r"threshold $10^{-5}$. K2: relative error of the integrated steady-state boundary currents against the "
        r"Schur-complement column $\Lambda e_j$, threshold $10^{-6}$.}",
        r"\label{tab:controls}",
        r"\begin{tabular}{llrlrl}\toprule",
        r"Network & Integrator & K1 error & & K2 error & \\ \midrule",
        *rows,
        r"\bottomrule\end{tabular}\end{table}",
    ])


def fig_kappa(h0):
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    style = {"{7,3}": ("o-", "C0"), "square": ("s--", "C1"), "triangular": ("^:", "C2")}
    for f, (m, c) in style.items():
        pts = [(r["N"], r["log10_kappa"]) for r in h0 if fam(r["name"]) == f]
        fin = [(n, k) for n, k in pts if k is not None]
        ax.plot(*zip(*fin), m, color=c, label=f"{{{f[1:-1]}}}" if f == "{7,3}" else f)
        sing = [n for n, k in pts if k is None]
        if sing:
            ax.scatter(sing, [15.7] * len(sing), marker="x", color=c)
    ax.axhline(math.log10(1 / 2.220446049250313e-16), color="grey", lw=0.6)
    ax.text(40, 15.95, "float64 floor", fontsize=7, color="grey")
    ax.set_xscale("log")
    ax.set_xlabel("$N$ (nodes)")
    ax.set_ylabel(r"$\log_{10}\kappa$")
    ax.set_ylim(0, 17)
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "fig_kappa.pdf")


def fig_h2(rc, explore):
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    hyp = [(r["N"], r["lambda_min"]) for r in explore["rows"]]
    ax.plot(*zip(*hyp), "o-", color="C0", label="{7,3}")
    for f, m, c in (("square", "s--", "C1"), ("triangular", "^:", "C2")):
        pts = [(r["N"], r["lambda_min"]) for r in rc["H2"] if r["family"] == f]
        ax.plot(*zip(*pts), m, color=c, label=f)
    ax.axhline(3 - 2 * math.sqrt(2), color="grey", lw=0.6)
    ax.text(25, 0.135, r"$3-2\sqrt{2}\geq\lambda_0$", fontsize=7, color="grey")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$N$ (nodes)")
    ax.set_ylabel(r"$\lambda_{\min}(L_{ii})$")
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "fig_h2.pdf")


def main():
    h0, pm, ident = load("h0.json"), load("probe_matched.json"), load("identifiability.json")
    rc, explore = load("rc_network.json"), load("h2_explore.json")
    (HERE / "tables.tex").write_text("% GENERATED by make_assets.py from data/*.json -- do not edit\n" + "\n\n".join(
        [table_kappa(h0), table_probe(pm, ident), table_h2(rc, explore), table_controls(rc)]) + "\n")
    fig_kappa(h0)
    fig_h2(rc, explore)
    print("wrote tables.tex, fig_kappa.pdf, fig_h2.pdf")


if __name__ == "__main__":
    main()
