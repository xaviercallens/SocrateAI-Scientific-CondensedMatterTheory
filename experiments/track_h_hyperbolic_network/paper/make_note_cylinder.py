#!/usr/bin/env python3
"""Figures and tables for paper/note_cylinder.tex, generated from the stored data files of preregistrations 23-27 and
their post-hoc diagnostics. Writes paper/fig_note_rates.pdf, paper/fig_note_increments.pdf, paper/tables_note.tex.
No number of the note's tables is typed by hand."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
D = HERE.parent / "data"
LABELS = ["8", "16", "24", "32", "40", "48"]
QTEX = ["$\\pi/6$", "$\\pi/3$", "$\\pi/2$", "$2\\pi/3$", "$5\\pi/6$", "$\\pi$"]
QX = [int(l) / 48 for l in LABELS]   # q / pi


def load(name):
    return json.loads((D / (name + ".json")).read_text())


c25 = load("exact_semi_infinite_blocks_asymptotic_ra")
c26 = load("diagonal_boundary_orientation_and_the_gr")
c27 = load("aligned_strip_with_unequal_conductances")
d26 = load("diagonal_signed_nodes_diagnostic")
c23, c24 = load("cylinder_exponential_sum_picture"), load("momentum_resolved_rates_on_the_cylinder")

CONFIGS = [  # (name, measured W384 rates, Green prediction used as the comparison, W768 zigzag measured, predicted zigzag, colour, marker)
    ("aligned, $\\lambda=1$", [c25["W384"][l]["rate"] for l in LABELS], [c25["verdicts"]["predicted_green"][l] for l in LABELS],
     c25["W768_pi"]["rate"], c25["verdicts"]["predicted_green"]["48"], "C0", "o"),
    ("diagonal (signed nodes)", [c26["W384"][l]["rate"] for l in LABELS], [d26["rows"][l]["signed_rate"] for l in LABELS],
     c26["W768_pi"]["rate"], d26["rows"]["48"]["signed_rate"], "C3", "s"),
    ("aligned, $\\lambda=0.05$", [c27["lams"]["0.05"]["W384"][l]["rate"] for l in LABELS], [c27["verdicts"]["detail"]["0.05"]["predicted"][l] for l in LABELS],
     c27["lams"]["0.05"]["W768_pi"]["rate"], c27["verdicts"]["detail"]["0.05"]["predicted"]["48"], "C2", "^"),
    ("aligned, $\\lambda=16$", [c27["lams"]["16"]["W384"][l]["rate"] for l in LABELS], [c27["verdicts"]["detail"]["16"]["predicted"][l] for l in LABELS],
     c27["lams"]["16"]["W768_pi"]["rate"], c27["verdicts"]["detail"]["16"]["predicted"]["48"], "C1", "D"),
]


def figure_rates():
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    for name, meas, pred, _, _, col, mk in CONFIGS:
        ax.plot(QX, pred, "-", color=col, lw=0.9)
        ax.plot(QX, meas, mk, color=col, mfc="none", ms=6, label=name.replace("$", "").replace("\\", ""))
    ax.plot(QX, [d26["rows"][l]["moduli_only_rate"] for l in LABELS], ":", color="C3", lw=0.9, label="diagonal, moduli only (wrong)")
    ax.set_xlabel(r"total momentum $q/\pi$"); ax.set_ylabel("decades of $\\sigma_{\\min}$ lost per row")
    ax.legend(fontsize=7, frameon=False); fig.tight_layout(); fig.savefig(HERE / "fig_note_rates.pdf"); plt.close(fig)


def figure_increments():
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    sets = [("aligned $\\lambda=1$", c25["W384"]["48"]["log10_sigma_min"], c25["verdicts"]["predicted_green"]["48"], "C0"),
            ("diagonal", c26["W384"]["48"]["log10_sigma_min"], d26["rows"]["48"]["signed_rate"], "C3"),
            ("aligned $\\lambda=0.05$", c27["lams"]["0.05"]["W384"]["48"]["log10_sigma_min"], c27["verdicts"]["detail"]["0.05"]["predicted"]["48"], "C2"),
            ("aligned $\\lambda=16$", c27["lams"]["16"]["W384"]["48"]["log10_sigma_min"], c27["verdicts"]["detail"]["16"]["predicted"]["48"], "C1")]
    for name, ls, pred, col in sets:
        inc = [ls[d - 1] - ls[d] for d in range(1, len(ls))]
        ax.plot(range(1, len(ls)), inc, "-", color=col, lw=0.9, label=name.replace("$", "").replace("\\", ""))
        ax.axhline(pred, color=col, ls=":", lw=0.7)
    ax.set_xlabel("depth $d$"); ax.set_ylabel("per-row loss at the zigzag block ($W=384$)")
    ax.legend(fontsize=7, frameon=False, ncol=2); fig.tight_layout(); fig.savefig(HERE / "fig_note_increments.pdf"); plt.close(fig)


def f3(x):
    return "%.3f" % x


def table_rates():
    rows = []
    for name, meas, pred, m768, p768, _, _ in CONFIGS:
        cells = " & ".join(f3(m) + " / " + f3(p) for m, p in zip(meas, pred))
        rows.append(name + " & " + cells + " & " + f3(m768) + " / " + f3(p768) + " \\\\")
    rows.append("diagonal, moduli only (wrong) & " + " & ".join(f3(c26["W384"][l]["rate"]) + " / " + f3(d26["rows"][l]["moduli_only_rate"]) for l in LABELS) + " & " + f3(c26["W768_pi"]["rate"]) + " / " + f3(d26["rows"]["48"]["moduli_only_rate"]) + " \\\\")
    return "\n".join([
        "\\begin{table}[t]\\centering\\scriptsize",
        "\\caption{Measured / predicted decay rate of $\\sigma_{\\min}$ (decades per row) of the momentum blocks, exact semi-infinite computation at $W=384$ "
        "(last column: zigzag block at $W=768$). Predictions are the Green-function exponents of the node sets; for the diagonal boundary the "
        "signed-node form was found after the data (Section~\\ref{sec:orient}), the moduli-only form was the preregistered one.}",
        "\\label{tab:rates}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{l" + "c" * 7 + "}\\toprule",
        "Geometry & " + " & ".join(QTEX) + " & $\\pi$ ($W{=}768$) \\\\ \\midrule",
        *rows, "\\bottomrule\\end{tabular}}\\end{table}"])


def word(v, gate=False):
    if v is None:
        return "void"
    return ("pass" if v else "fail") if gate else ("held" if v else "refuted")


def table_register():
    cards = [("23", "H0-X-0014", c23["verdicts"]), ("24", "H0-X-0015", c24["verdicts"]), ("25", "H0-X-0016", c25["verdicts"]),
             ("26", "H0-X-0017", c26["verdicts"]), ("27", "H0-X-0018", c27["verdicts"])]
    rows = []
    for num, led, v in cards:
        gates = ", ".join(k + " " + word(v[k], True) for k in sorted(v) if k.startswith("G") and not k.startswith("G3_") and isinstance(v[k], (bool, type(None))))
        preds = ", ".join(k + " " + word(v[k]) for k in sorted(v) if k.startswith("P") and not k.endswith("_fits") and "rival" not in k and isinstance(v[k], (bool, type(None))))
        rows.append(num + " & " + led + " & " + gates + " & " + preds + " \\\\")
    return "\n".join([
        "\\begin{table}[t]\\centering\\scriptsize",
        "\\caption{Register of the preregistered gates and predictions behind this note, from the stored verdicts. Every refutation is kept; "
        "the failed gates are design errors of mine (Section~\\ref{sec:failures}).}",
        "\\label{tab:register}",
        "\\begin{tabular}{llp{3.2cm}p{5.6cm}}\\toprule",
        "Prereg. & Ledger & Gates & Predictions \\\\ \\midrule", *rows, "\\bottomrule\\end{tabular}\\end{table}"])


def table_laplace():
    c29 = load("laplace_resolved_jacobian_conditioning")
    ph = load("laplace_wide_window_posthoc")
    tab = c29["square"]["table"]
    ds = list(range(3, 10))
    rows = [str(d) + " & " + " & ".join(f3(tab[k][str(d)]["log10_kappa"]) for k in ("S1", "S2", "S5")) + " \\\\" for d in ds]
    rows.append("\\midrule slope, $d=3..9$ (post hoc) & " + " & ".join(f3(ph["slope"][k]) for k in ("S1", "S2", "S5")) + " \\\\")
    rows.append("slope, preregistered window $d=3,4$ & " + " & ".join(f3(c29["slopes"][k]) for k in ("S1", "S2", "S5")) + " \\\\")
    return "\n".join([
        "\\begin{table}[t]\\centering\\small",
        "\\caption{$\\log_{10}\\kappa(J_d)$ of the square disk (radius 16) for one, two and five real Laplace variables "
        "($S_1=\\{0\\}$, $S_2=\\{0,0.3\\}$, $S_5=\\{0,0.1,0.3,1,3\\}$), from the stored data. Values of $S_1$ above 9 are near the double-precision floor.}",
        "\\label{tab:laplace}",
        "\\begin{tabular}{cccc}\\toprule",
        "$d$ & $S_1$ & $S_2$ & $S_5$ \\\\ \\midrule", *rows, "\\bottomrule\\end{tabular}\\end{table}"])


def main():
    figure_rates(); figure_increments()
    (HERE / "tables_note.tex").write_text("% GENERATED by make_note_cylinder.py from data/*.json -- do not edit\n" + table_rates() + "\n\n" + table_register() + "\n\n" + table_laplace() + "\n")
    print("wrote fig_note_rates.pdf, fig_note_increments.pdf, tables_note.tex")


if __name__ == "__main__":
    main()
