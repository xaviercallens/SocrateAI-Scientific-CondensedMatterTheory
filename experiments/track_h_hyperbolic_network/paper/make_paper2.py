#!/usr/bin/env python3
"""Generate the figure and tables of paper 2 (topology of the Jacobian column cloud; integrator check of the garage bench) from the stored data.
Writes paper/fig_p2_cloud.pdf and paper/tables_p2.tex."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
D = HERE.parent / "data"


def load(n):
    return json.loads((D / (n + ".json")).read_text())


c30 = load("jacobian_column_cloud_homology")
f30 = load("jacobian_column_cloud_homology_firstrun")
p30 = load("jacobian_column_cloud_homology_posthoc")
c31 = load("cvode_check_of_the_garage_virtual_bench")
c29 = load("laplace_resolved_jacobian_conditioning")


def f3(x):
    return "%.3f" % x


def fe(x):
    return "%.1e" % x


def verdict(v, gate=False):
    return ("pass" if v else "fail") if gate else ("held" if v else "refuted")


def figure():
    sq = c30["square"]["layers"]
    ks = [int(k) for k in sq]
    m = [sq[str(k)]["median_death"] for k in ks]
    hy = c30["hyperbolic_73_L5"]["layers"]
    kh = [int(k) for k in hy]
    mh = [hy[str(k)]["median_death"] for k in kh]
    ct = c30["control"]["layers"]
    kc = [int(k) for k in ct]
    mc = [ct[str(k)]["median_death"] for k in kc]
    sg = c30["square"]["sigma"]
    fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.3))
    ax[0].plot(ks, m, "o-", label="square disk")
    ax[0].plot(kh, mh, "s-", label=r"$\{7,3\}$")
    ax[0].plot(kc, mc, "^--", color="gray", label="random control")
    ax[0].plot(ks[1:], [p30["k_times_m"][2] / k for k in ks[1:]], ":", color="k", label=r"$\propto 1/k$ (post hoc)")
    ax[0].set_yscale("log"); ax[0].set_xlabel("depth layer $k$"); ax[0].set_ylabel("median $H_0$ death time"); ax[0].legend(fontsize=7)
    ax[1].plot(ks, [np.log10(sg[str(k)]["sigma_min"]) for k in ks], "o-")
    ax[1].set_xlabel("depth $d$"); ax[1].set_ylabel(r"$\log_{10}\sigma_{\min}(J_{\leq d})$ (square disk)")
    fig.tight_layout(); fig.savefig(HERE / "fig_p2_cloud.pdf"); plt.close(fig)


def table_cloud():
    sq = c30["square"]["layers"]
    sg = c30["square"]["sigma"]
    rows = []
    for k in sq:
        rows.append(f"{k} & {sq[k]['n']} & {f3(sq[k]['median_death'])} & {f3(int(k) * sq[k]['median_death'])} & {f3(np.log10(sg[k]['sigma_min']))} \\\\")
    hy = c30["hyperbolic_73_L5"]["layers"]
    hrow = ", ".join(f"{k}: {f3(hy[k]['median_death'])}" for k in hy)
    return "\n".join([
        "\\begin{table}[t]\\centering\\small",
        "\\caption{Square disk of radius 16: edges per layer, median $H_0$ death time $m_k$ of the sine-distance cloud of Jacobian columns, $k\\,m_k$, and $\\log_{10}\\sigma_{\\min}$ of the Jacobian restricted to depth $\\le k$. "
        "On the $\\{7,3\\}$ tiling (5 layers) the median death times are " + hrow + ".}",
        "\\label{tab:cloud}",
        "\\begin{tabular}{ccccc}\\toprule",
        "$k$ & edges & $m_k$ & $k\\,m_k$ & $\\log_{10}\\sigma_{\\min}$ \\\\ \\midrule", *rows, "\\bottomrule\\end{tabular}\\end{table}"])


def table_cvode():
    rows = []
    for r in c31["waveform_draws"]:
        rows.append(f"{r['board']} & ({r['tolerances_used'][0]:.0e}, {r['tolerances_used'][1]:.0e}) & {fe(r['max_rel_waveform_diff'])} & {fe(r['tau_rel_diff'])} \\\\")
    p3 = c31["P3"]
    return "\n".join([
        "\\begin{table}[t]\\centering\\small",
        "\\caption{Integrator check: for each of six draws per board (5\\,\\% resistors, 10\\,\\% capacitors), the CVODE tolerances used, the maximum difference to the bench's modal solution in units of $V_0$, and the relative difference of the fitted time constant. "
        f"Ratio of fitted time constants $\\{{7,3\\}}$/square over 12 draws at 1\\,\\%: mean {f3(p3['mean'])}, range {f3(p3['min'])}--{f3(p3['max'])}, spread {f3(p3['spread'])}.}}",
        "\\label{tab:cvode}",
        "\\begin{tabular}{llcc}\\toprule",
        "Board & (rtol, atol) & max $|\\Delta V|/V_0$ & $|\\Delta\\tau|/\\tau$ \\\\ \\midrule", *rows, "\\bottomrule\\end{tabular}\\end{table}"])


def table_register():
    rows = [
        ("30", "G1 control", verdict(c30["G1"]["pass"], True)),
        ("30", "G2 duplicated columns", verdict(c30["G2"]["pass"], True) + " (limit unattainable, Sec.~\\ref{sec:fail})"),
        ("30", "G3 clipping", verdict(c30["G3_clipped_below_1pct"], True)),
        ("30", "P1 collapse (square)", verdict(c30["P1"]["pass"])),
        ("30", "P2 flat vs hyperbolic", verdict(c30["P2"]["pass"])),
        ("30", "P3 tracks $\\sigma_{\\min}$", verdict(c30["P3"]["pass"])),
        ("30", "P4 exponential size", verdict(c30["P4"]["pass"])),
        ("31", "G1 integrator vs bench", verdict(c31["G1"]["pass"], True)),
        ("31", "P1 waveforms", verdict(c31["P1"]["pass"])),
        ("31", "P2 fitted $\\tau$", verdict(c31["P2"]["pass"])),
        ("31", "P3 ratio band", verdict(c31["P3"]["pass"])),
    ]
    body = [f"{a} & {b} & {c} \\\\" for a, b, c in rows]
    return "\n".join([
        "\\begin{table}[t]\\centering\\small",
        "\\caption{Register of the preregistered gates and predictions, from the stored verdicts. Every refutation and failed gate is kept.}",
        "\\label{tab:register2}",
        "\\begin{tabular}{llp{6cm}}\\toprule", "Prereg. & Item & Verdict \\\\ \\midrule", *body, "\\bottomrule\\end{tabular}\\end{table}"])


def main():
    figure()
    (HERE / "tables_p2.tex").write_text("% GENERATED by make_paper2.py from data/*.json -- do not edit\n" + table_cloud() + "\n\n" + table_cvode() + "\n\n" + table_register() + "\n")
    print("wrote fig_p2_cloud.pdf, tables_p2.tex; first-run G2:", f30["G2"]["max_median_death"], "P4 slope", f30["P4"]["slope"], "ref c29 slopes", c29["slopes"])


if __name__ == "__main__":
    main()
