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


def load_opt(name):
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else None


def table_kappa(h0, mp):
    """mp: flat_scaling_mp.json rows (Arb), keyed by the h0 row name; None if absent."""
    arb = {}
    for r in (mp or []):
        for h in h0:
            if r["case"].split(" (")[0] == tex_key(h["name"]):
                arb[h["name"]] = r
    rows = []
    for r in h0:
        k = r"\textsc{sing.}" if r["log10_kappa"] is None else f"{r['log10_kappa']:.2f}"
        a = arb.get(r["name"])
        ka = "" if a is None else f"{a['log10_kappa_arb']:.2f}"
        rows.append(f"{tex_name(r['name'])} & {r['N']} & {r['E']} & {r['boundary']} & {r['max_depth']} & {k} & {ka} \\\\")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Conditioning of the DtN sensitivity Jacobian, unit conductances, full boundary. "
        r"$d_{\max}$: maximal graph distance to the boundary. \textsc{sing.}: smallest singular value at or "
        r"below $\varepsilon_{\mathrm{mach}}\,\sigma_{\max}$ in IEEE double precision. The last column is the "
        r"512-bit ball-arithmetic value (Sec.~\ref{sec:arb}), given for the two unsaturated controls and for the "
        r"double-precision-singular flat instances. The $\{7,3\}$, $L=4$ row is the preregistered confirmatory point.}",
        r"\label{tab:kappa}",
        r"\begin{tabular}{lrrrrrr}\toprule",
        r"Lattice & $N$ & $|E|$ & $|\partial G|$ & $d_{\max}$ & $\log_{10}\kappa$ (float64) & $\log_{10}\kappa$ (Arb) \\ \midrule",
        *rows,
        r"\bottomrule\end{tabular}\end{table}",
    ])


def tex_key(name):
    """'triangular R=10.75' -> 'triangular R=10.75'; float radii normalised like flat_scaling_mp CASES."""
    head, _, par = name.partition(" ")
    if "=" not in par:
        return head
    k, v = par.split("=", 1)
    v = f"{float(v):g}" if "." not in v else f"{float(v):.2f}".rstrip("0").rstrip(".")
    return f"{head} {k}={v}"


def table_disorder(dis):
    if dis is None:
        return ""
    s = dis["summary_median_logparam"]
    def f(x): return r"\textsc{sing.}" if x is None else f"{x:.2f}"
    rows = []
    for regime, label in (("unit", "unit ($g_e=1$)"), ("U[0.5,1.5]", r"$g_e\sim\mathcal U[0.5,1.5]$"),
                          ("logU[0.1,10]", r"$\log_{10} g_e\sim\mathcal U[-1,1]$"),
                          ("defect x100", r"defect $\times100$"), ("defect x0.01", r"defect $\times0.01$")):
        d = s[regime]
        rows.append(rf"{label} & {f(d['{7,3} L=2'])} & {f(d['square R=6'])} & {f(d['gap_N112'])} & "
                    rf"{f(d['{7,3} L=3'])} & {f(d['square R=10'])} & {f(d['gap_N316'])} \\")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Conditioning under inhomogeneous conductances: $\log_{10}\kappa$ of the log-parametrised "
        r"Jacobian $\partial\Lambda/\partial\ln g_e$, medians over five seeds for the random regimes. The defect "
        r"multiplies every edge of one interior node at maximal depth. Gap: square minus hyperbolic.}",
        r"\label{tab:disorder}",
        r"\begin{tabular}{lrrrrrr}\toprule",
        r" & \multicolumn{3}{c}{$N\approx112$} & \multicolumn{3}{c}{$N\approx316$} \\",
        r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}",
        r"Conductances & $\{7,3\}$ $L{=}2$ & square $R{=}6$ & gap & $\{7,3\}$ $L{=}3$ & square $R{=}10$ & gap \\ \midrule",
        *rows,
        r"\bottomrule\end{tabular}\end{table}",
    ])


def table_subspace(sub):
    if sub is None:
        return ""
    rows = []
    for r in sub:
        hyp = r["hyperbolic"].replace("{7,3}", "$\\{7,3\\}$")
        rows.append(f"{hyp} & {r['r']} & {r['hyp_log10_kappa_identifiable']:.2f} & "
                    f"square ${r['square']}$ & {r['square_E']} & {r['square_full_log10_kappa']:.2f} & "
                    f"{r['square_log10_sigma1_over_sigma_r']:.2f} \\\\")
    return "\n".join([
        r"\begin{table}[t]\centering\small",
        r"\caption{Dimensionality in the probe-matched control. $r$: hyperbolic identifiable dimension. "
        r"$\sigma_1/\sigma_r$: condition number of the square lattice's best-conditioned $r$-dimensional "
        r"parameter subspace (top-$r$ right singular vectors), the most favourable $r$-dimensional comparison "
        r"for the flat lattice.}",
        r"\label{tab:subspace}",
        r"\begin{tabular}{lrrlrrr}\toprule",
        r"Hyperbolic (subsampled) & $r$ & $\log_{10}\kappa_{\mathrm{id}}$ & Flat & $|E|$ & $\log_{10}\kappa$ (all $|E|$) & "
        r"$\log_{10}\sigma_1/\sigma_r$ \\ \midrule",
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


def fig_kappa(h0, mp):
    """Left: log10 kappa vs N (Arb values replace float64-singular points). Right: flat families vs sqrt N."""
    arb = {}
    for r in (mp or []):
        if r["control_pass"] is None:  # saturated cases only
            for h in h0:
                if r["case"] == tex_key(h["name"]):
                    arb[h["name"]] = r["log10_kappa_arb"]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.2))
    style = {"{7,3}": ("o-", "C0"), "square": ("s--", "C1"), "triangular": ("^:", "C2")}
    ymax = 17
    for f, (m, c) in style.items():
        pts = [(r["N"], r["log10_kappa"] if r["log10_kappa"] is not None else arb.get(r["name"]))
               for r in h0 if fam(r["name"]) == f]
        fin = [(n, k) for n, k in pts if k is not None]
        ax.plot(*zip(*fin), m, color=c, label=f"{{{f[1:-1]}}}" if f == "{7,3}" else f)
        ymax = max(ymax, max(k for _, k in fin) + 1)
        for r in h0:
            if fam(r["name"]) == f and r["log10_kappa"] is None:
                if r["name"] in arb:
                    ax.scatter([r["N"]], [arb[r["name"]]], marker="o", facecolors="none", edgecolors=c, s=60)
                else:
                    ax.scatter([r["N"]], [15.7], marker="x", color=c)
        if f != "{7,3}":
            ax2.plot([math.sqrt(n) for n, _ in fin], [k for _, k in fin], m, color=c, label=f)
    ax.axhline(math.log10(1 / 2.220446049250313e-16), color="grey", lw=0.6)
    ax.text(40, 15.95, "float64 floor", fontsize=7, color="grey")
    ax.set_xscale("log"); ax.set_xlabel("$N$ (nodes)"); ax.set_ylabel(r"$\log_{10}\kappa$"); ax.set_ylim(0, ymax)
    ax.legend(fontsize=8, frameon=False)
    ax2.set_xlabel(r"$\sqrt{N}$"); ax2.set_ylabel(r"$\log_{10}\kappa$")
    ax2.legend(fontsize=8, frameon=False)
    ax2.set_title("flat lattices (open markers: Arb)" if arb else "flat lattices", fontsize=8)
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
    mp, dis, sub = load_opt("flat_scaling_mp.json"), load_opt("disorder.json"), load_opt("subspace_control.json")
    (HERE / "tables.tex").write_text("% GENERATED by make_assets.py from data/*.json -- do not edit\n" + "\n\n".join(
        [table_kappa(h0, mp), table_probe(pm, ident), table_subspace(sub), table_disorder(dis),
         table_h2(rc, explore), table_controls(rc)]) + "\n")
    fig_kappa(h0, mp)
    fig_h2(rc, explore)
    print("wrote tables.tex, fig_kappa.pdf, fig_h2.pdf")


if __name__ == "__main__":
    main()
