#!/usr/bin/env python3
"""Figure and tables of paper 3 (depth-ordered residuals), from the stored data. Writes paper/fig_p3_residuals.pdf and paper/tables_p3.tex."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
D = HERE.parent / "data"
c32 = json.loads((D / "depth_ordered_residuals_of_jacobian_columns.json").read_text())
c30 = json.loads((D / "jacobian_column_cloud_homology.json").read_text())
W = c32["window"]
SQ = c32["square"]["table"]
HY = c32["hyperbolic_73_L5"]["table"]


def f3(x):
    return "%.3f" % x


def figure():
    fig, ax = plt.subplots(1, 2, figsize=(8.8, 3.4))
    for key, lab, st in (("sigma_min", r"$\sigma_{\min}(J_{\leq k})$", "o-"), ("loo_min", "leave-one-out minimum", "s--"),
                         ("rho", "depth-ordered minimum", "^-"), ("s_min", "distance to shallower span, minimum", "d:")):
        ax[0].plot(W, [np.log10(SQ[str(k)][key]) for k in W], st, label=lab)
    ax[0].set_xlabel("depth layer $k$"); ax[0].set_ylabel(r"$\log_{10}$"); ax[0].legend(fontsize=7)
    ax[0].set_title("square disk, radius 16", fontsize=9)
    ax[1].plot(W, [np.log10(SQ[str(k)]["median_rel_s"]) for k in W], "o-", label="square: median relative distance to shallower span")
    hk = c32["hyperbolic_73_L5"]["layers"]
    ax[1].plot(hk, [np.log10(HY[str(k)]["median_rel_s"]) for k in hk], "s-", label=r"$\{7,3\}$: same quantity")
    lay = c30["square"]["layers"]
    kk = [k for k in W if str(k) in lay]
    ax[1].plot(kk, [np.log10(lay[str(k)]["median_death"]) for k in kk], "^--", color="gray", label="square: nearest-neighbour $H_0$ median death")
    ax[1].set_xlabel("depth layer $k$"); ax[1].set_ylabel(r"$\log_{10}$"); ax[1].legend(fontsize=6.5)
    fig.tight_layout(); fig.savefig(HERE / "fig_p3_residuals.pdf"); plt.close(fig)


def table_layers():
    rows = []
    for k in W:
        t = SQ[str(k)]
        rows.append(f"{k} & {t['n_layer']} & " + " & ".join(f3(np.log10(t[x])) for x in ("sigma_min", "loo_min", "rho", "s_min")) + f" & {f3(t['median_rel_s'])} \\\\")
    hrows = []
    for k in c32["hyperbolic_73_L5"]["layers"]:
        t = HY[str(k)]
        hrows.append(f"{k} & {t['n_layer']} & " + " & ".join(f3(np.log10(t[x])) for x in ("sigma_min", "loo_min", "rho", "s_min")) + f" & {f3(t['median_rel_s'])} \\\\")
    head = "Layer & edges & $\\log_{10}\\sigma_{\\min}$ & $\\log_{10}$ LOO & $\\log_{10}\\rho$ & $\\log_{10}s$ & median $s/\\|J_e\\|$ \\\\ \\midrule"
    return "\n".join([
        "\\begin{table}[t]\\centering\\small",
        "\\caption{Square disk (radius 16), scored layers: $\\sigma_{\\min}$ of $J_{\\leq k}$, minimum leave-one-out residual (LOO), minimum depth-ordered residual $\\rho$, minimum distance $s$ to the span of strictly shallower layers, "
        "and the median of $s/\\|J_e\\|$ over the layer. Below the rule: the $\\{7,3\\}$ tiling with five layers (Gram route).}",
        "\\label{tab:layers}", "\\resizebox{\\linewidth}{!}{%", "\\begin{tabular}{ccccccc}\\toprule", head, *rows, "\\midrule", *hrows, "\\bottomrule\\end{tabular}}\\end{table}"])


def verdict(v, gate=False):
    return ("pass" if v else "fail") if gate else ("held" if v else "refuted")


def table_register():
    sl = c32["slopes"]
    rows = [("G1 exact chain", verdict(c32["G1"]["pass"], True), ""), ("G2 QR reconstruction", verdict(c32["G2"]["pass"], True), "%.1e" % c32["G2"]["recon_rel"]),
            ("G3 leave-one-out identity", verdict(c32["G3"]["pass"], True), "%.1e" % c32["G3"]["max_rel_err"]),
            ("G4 Gram route (added)", verdict(c32["G4"]["pass"], True), "%.1e" % c32["G4"]["max_rel_err"]),
            ("P1 rate captured", verdict(c32["P1"]["pass"]), "ratio " + f3(c32["P1"]["ratio"])),
            ("P2 looseness of $\\rho$", verdict(c32["P2"]["pass"]), "gaps %.2f to %.2f" % (min(c32["P2"]["gaps"]), max(c32["P2"]["gaps"]))),
            ("P3 same layer versus depth", verdict(c32["P3"]["pass"]), "gaps %.2f to %.2f, mean %.2f" % (min(c32["P3"]["gaps"]), max(c32["P3"]["gaps"]), c32["P3"]["mean"])),
            ("P4 median residual exponential", verdict(c32["P4"]["pass"]), "slope %s, Pearson %s" % (f3(c32["P4"]["slope"]), f3(c32["P4"]["pearson"]))),
            ("P5 hyperbolic", verdict(c32["P5"]["pass"]), "slope %s against %s" % (f3(c32["P5"]["slope_hyp"]), f3(c32["P5"]["slope_sq"]))),
            ("P6 contrast with nearest neighbours", verdict(c32["P6"]["pass"]), "ratio %.1f" % c32["P6"]["ratio"])]
    body = [f"{a} & {b} & {c} \\\\" for a, b, c in rows]
    slopes = ", ".join(f"{k.replace('_', ' ')} {f3(v)}" for k, v in sl.items())
    return "\n".join([
        "\\begin{table}[t]\\centering\\small",
        "\\caption{Gates and predictions of preregistration 32, from the stored verdicts. Slopes in decades per layer: " + slopes + ".}",
        "\\label{tab:register3}", "\\begin{tabular}{lll}\\toprule", "Item & Verdict & Value \\\\ \\midrule", *body, "\\bottomrule\\end{tabular}\\end{table}"])


def main():
    figure()
    (HERE / "tables_p3.tex").write_text("% GENERATED by make_paper3.py from data/*.json -- do not edit\n" + table_layers() + "\n\n" + table_register() + "\n")
    print("wrote fig_p3_residuals.pdf, tables_p3.tex")


if __name__ == "__main__":
    main()
