#!/usr/bin/env python3
"""Generate everything the garage build needs from the SAME graph builders as the paper:
  lab/out/<board>_nodes.csv     node id, x, y (layout), depth, role (boundary/interior), degree, layer group
  lab/out/<board>_edges.csv     resistor id, node a, node b, depth class, nominal R
  lab/out/<board>_wiring.md     wiring tables grouped by layer (what to solder, in order)
  lab/out/<board>_mve.cir       SPICE netlist of the minimal viable experiment (all boundary nodes on one driven
                                rail, one capacitor per interior node to ground, step source, probe nodes)
  lab/out/<board>_schematic.pdf labelled schematic (node ids, resistor ids, boundary contacts marked)
  lab/out/BOM.md                bill of materials for both boards + calibration cells + measurement chain
  lab/out/predictions_static.json  effective resistances between chosen boundary pairs (ohms), tau factors
Component values (nominal): R = 100 kOhm 1 % metal film, C = 1 uF film (or C0G/NP0), V0 = 3.3 V.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hyperbolic_network import boundary_nodes, build_hyperbolic, build_square_disk, degrees, depths, dtn  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"
R_NOM, C_NOM, V0 = 100e3, 1e-6, 3.3
BOARDS = (("hyp73_L2", "{7,3} L=2", lambda: build_hyperbolic(7, 3, 2)),
          ("square_R6", "square R=6", lambda: build_square_disk(6)))
PROBE_DEPTHS = (1, 2, 3)  # one probe per depth class (first node by index)


def board_tables(tag, label, g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd); deg = degrees(n, edges)
    z = np.asarray(g["nodes"]); interior = np.setdiff1d(np.arange(n), bnd)
    isb = np.zeros(n, bool); isb[bnd] = True
    with open(OUT / (tag + "_nodes.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["node", "x", "y", "depth", "role", "degree", "capacitor"])
        for v in range(n):
            w.writerow([v, "%.4f" % z[v].real, "%.4f" % z[v].imag, int(d[v]), "boundary" if isb[v] else "interior",
                        int(deg[v]), ("C%03d" % v) if not isb[v] else ""])
    rows = []
    for e, (a, b) in enumerate(edges):
        rows.append({"resistor": "R%03d" % e, "a": int(a), "b": int(b), "depth_class": int(min(d[a], d[b])),
                     "R_nominal_ohm": R_NOM})
    with open(OUT / (tag + "_edges.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # wiring tables by depth class (solder the deepest first: fewer leads crossing later)
    md = ["# Wiring: " + label, "", "Order: deepest class first, then outward; boundary rail last. "
          "Tick each line when soldered and checked with the DMM (expected %.0f kOhm per resistor)." % (R_NOM / 1e3), ""]
    for dc in sorted({r["depth_class"] for r in rows}, reverse=True):
        sub = [r for r in rows if r["depth_class"] == dc]
        md.append("## Depth class %d (%d resistors)" % (dc, len(sub)))
        md.append("| done | resistor | node a | node b |"); md.append("|---|---|---|---|")
        md += ["| [ ] | %s | %d%s | %d%s |" % (r["resistor"], r["a"], "*" if isb[r["a"]] else "", r["b"], "*" if isb[r["b"]] else "") for r in sub]
        md.append("")
    md.append("`*` = boundary node (on the driven rail). Capacitors: one per interior node to ground: " +
              ", ".join("C%03d" % v for v in interior) + " (%d).\n" % len(interior))
    (OUT / (tag + "_wiring.md")).write_text("\n".join(md))
    # SPICE netlist of the MVE
    probes = [int(interior[np.argmax(d[interior] == pd)]) for pd in PROBE_DEPTHS if (d[interior] == pd).any()]
    cir = ["* %s minimal viable experiment: boundary rail driven by a step, C to ground at interior nodes" % label,
           "* nominal R=%.0f C=%.2e V0=%.1f; node names n<id>; boundary nodes tied to node RAIL" % (R_NOM, C_NOM, V0),
           "Vstep RAIL 0 PULSE(0 %.1f 10m 1u 1u 100 200)" % V0]
    name = lambda v: "RAIL" if isb[v] else "n%d" % v
    for r in rows:
        if isb[r["a"]] and isb[r["b"]]:
            continue  # both on the rail: shorted by the rail in the MVE
        cir.append("%s %s %s %.0f" % (r["resistor"], name(r["a"]), name(r["b"]), R_NOM))
    cir += ["C%03d n%d 0 %.3e" % (v, v, C_NOM) for v in interior]
    cir += [".tran 1m 8", ".print tran " + " ".join("v(n%d)" % p for p in probes), ".end"]
    (OUT / (tag + "_mve.cir")).write_text("\n".join(cir) + "\n")
    # schematic
    fig, ax = plt.subplots(figsize=(9, 9))
    for e, (a, b) in enumerate(edges):
        ax.plot([z[a].real, z[b].real], [z[a].imag, z[b].imag], color="0.6", lw=0.8, zorder=1)
        m = (z[a] + z[b]) / 2
        ax.text(m.real, m.imag, "R%d" % e, fontsize=3.5, color="0.35", ha="center", va="center", zorder=3)
    ax.scatter(z[interior].real, z[interior].imag, s=26, c=d[interior], cmap="viridis", zorder=2, edgecolors="k", linewidths=0.4)
    ax.scatter(z[bnd].real, z[bnd].imag, s=30, marker="s", color="tab:red", zorder=2, edgecolors="k", linewidths=0.4)
    for v in range(n):
        ax.text(z[v].real, z[v].imag + 0.012 * (1 if tag.startswith("hyp") else 8), str(v), fontsize=4.5, ha="center", va="bottom", zorder=4)
    for p in probes:
        ax.annotate("probe d=%d" % d[p], (z[p].real, z[p].imag), textcoords="offset points", xytext=(18, 12), fontsize=7,
                    arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("%s: N=%d, %d resistors, %d boundary contacts (red squares, driven rail), %d capacitors (interior, colour = depth)"
                 % (label, n, len(edges), len(bnd), len(interior)), fontsize=9)
    fig.savefig(OUT / (tag + "_schematic.pdf"), bbox_inches="tight")
    return {"tag": tag, "label": label, "N": n, "E": len(edges), "boundary": int(len(bnd)), "interior": int(len(interior)),
            "probes": probes, "rail_shorted_edges": int(sum(1 for r in rows if isb[r["a"]] and isb[r["b"]]))}


def static_predictions(g, k=6):
    """Effective resistance (ohms) between k boundary pairs, from the DtN pseudo-inverse."""
    n = len(g["nodes"]); bnd = boundary_nodes(g)
    P = np.linalg.pinv(dtn(n, g["edges"], np.ones(len(g["edges"])), bnd), rcond=1e-12)
    m = len(bnd); rng = np.random.default_rng(1)
    pairs = [(0, 1), (0, m // 2)] + [tuple(sorted(rng.choice(m, 2, replace=False))) for _ in range(k - 2)]
    return [{"boundary_i": int(bnd[i]), "boundary_j": int(bnd[j]),
             "R_eff_ohm": float(R_NOM * (P[i, i] + P[j, j] - 2 * P[i, j]))} for i, j in pairs]


def main():
    OUT.mkdir(exist_ok=True)
    rc = json.loads((Path(__file__).resolve().parents[1] / "data" / "rc_network.json").read_text())
    tau_factor = {"{7,3} L=2": next(r["tau"] for r in rc["H2"] if r["family"] == "{7,3}" and r["N"] == 112),
                  "square R=6": next(r["tau"] for r in rc["H2"] if r["family"] == "square" and r["N"] == 113)}
    info, pred = [], {"R_nominal_ohm": R_NOM, "C_nominal_F": C_NOM, "RC_s": R_NOM * C_NOM, "boards": {}}
    for tag, label, build in BOARDS:
        g = build()
        i = board_tables(tag, label, g); info.append(i)
        pred["boards"][label] = {"tau_factor": tau_factor[label], "tau_s_nominal": tau_factor[label] * R_NOM * C_NOM,
                                 "static_pairs": static_predictions(g), "probes": i["probes"]}
        print("%-11s N=%d E=%d boundary=%d interior=%d probes=%s tau=%.3f RC = %.3f s" %
              (label, i["N"], i["E"], i["boundary"], i["interior"], i["probes"], tau_factor[label], tau_factor[label] * R_NOM * C_NOM))
    pred["tau_ratio_hyp_over_square"] = tau_factor["{7,3} L=2"] / tau_factor["square R=6"]
    (OUT / "predictions_static.json").write_text(json.dumps(pred, indent=1))
    n_r = sum(i["E"] for i in info); n_c = sum(i["interior"] for i in info)
    bom = ["# Bill of materials (two boards + calibration cells + measurement chain)", "",
           "| Item | Qty | Spec | Note |", "|---|---|---|---|",
           "| Resistor 100 kOhm | %d + 10 spare | metal film, 1 %% (5 %% acceptable for the differential tests, 1 %% for tau) | %d for {7,3} L=2, %d for square R=6, 2 for calibration cells |" % (n_r + 2, info[0]["E"], info[1]["E"]),
           "| Capacitor 1 uF | %d + 6 spare | film (PET/PP) or C0G; NOT class-2 ceramic (DC bias), NOT electrolytic (leakage) | %d + %d interior nodes, 2 calibration cells |" % (n_c + 2, info[0]["interior"], info[1]["interior"]),
           "| Perfboard / stripboard | 2 | >= 15 x 15 cm | one per board; or a 3D-printed jig following the schematic layout |",
           "| Bus wire | 3 m | tinned copper | boundary rail and ground |",
           "| Op-amp | 1 x quad | rail-to-rail input, low bias (MCP6004 / TLV2374 class) | unity-gain buffers: 1 driver + 3 probes |",
           "| ADC | 1 | >= 12 bit with <= 1 LSB noise, >= 100 S/s per channel; 16-bit ADS1115 (860 SPS) recommended | the ESP32 internal ADC (10-bit effective) is EXCLUDED: the virtual bench gives +20 % to +80 % tau error with it |",
           "| Microcontroller | 1 | ESP32 / Arduino / Raspberry Pi Pico | step generation (GPIO -> driver buffer), ADC readout, timestamping |",
           "| DMM | 1 | 4.5 digits preferred | component sorting, static effective-resistance checks |",
           "| Bench supply / USB 5 V | 1 | 3.3 V rail for the step | |",
           "| Calibration cell | 2 | one R + one C from the same batches, on each board | measures RC directly: the tau predictions are multiples of it |",
           "", "Nominal RC = %.3f s; predicted tau: {7,3} L=2 = %.3f s, square R=6 = %.3f s; ratio %.3f." %
           (R_NOM * C_NOM, pred["boards"]["{7,3} L=2"]["tau_s_nominal"], pred["boards"]["square R=6"]["tau_s_nominal"], pred["tau_ratio_hyp_over_square"]),
           "", "Every row of a wiring table should be checked with the DMM before the next row is soldered."]
    (OUT / "BOM.md").write_text("\n".join(bom) + "\n")
    print("tau ratio hyperbolic/square = %.4f" % pred["tau_ratio_hyp_over_square"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
