#!/usr/bin/env python3
"""PREREGISTRATION_15.md: RC relaxation time, stiffness and two-integrator controls on other tilings.
Writes data/rc_benchmark_on_other_tilings.json; score() returns verdicts from the file alone."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import boundary_nodes, build_hyperbolic, depths, dtn  # noqa: E402
import rc_network as rc  # noqa: E402

D = Path(__file__).resolve().parent / "data"
OUT = D / "rc_benchmark_on_other_tilings.json"
NETS = [(7, 3, 2), (8, 3, 2), (5, 4, 3), (6, 4, 2), (4, 5, 4)]


def run() -> dict:
    backends = ["scipy"] + (["rusty"] if rc.HAVE_RUSTY else [])
    rows = []
    for (p, q, L) in NETS:
        g = build_hyperbolic(p, q, L)
        bnd = boundary_nodes(g)
        Lfull, interior, Lii, Lib = rc.blocks(g, bnd)
        ev = np.linalg.eigvalsh(Lii)
        tau = float(1.0 / ev[0])
        row = {"tiling": "{%d,%d}" % (p, q), "L": L, "N": len(g["nodes"]), "d_max": int(depths(g, bnd).max()),
               "lambda_min": float(ev[0]), "lambda_max": float(ev[-1]), "tau": tau, "stiffness": float(ev[-1] / ev[0]),
               "controls": {}}
        rng = np.random.default_rng(3)
        t_out = np.array([0.25, 1.0, 4.0, 16.0]) * tau
        Vb = rng.uniform(-1, 1, len(bnd)); V0 = np.zeros(len(interior))
        exact = rc.known_answer(Lii, Lib, Vb, V0, t_out)
        lam = dtn(len(g["nodes"]), g["edges"], np.ones(len(g["edges"])), bnd)
        for be in backends:
            got = rc.integrate(be, Lii, Lib, Vb, V0, t_out)
            k1 = float(np.max(np.abs(got - exact)) / np.max(np.abs(exact)))
            k2 = []
            for j in (0, len(bnd) // 3, 2 * len(bnd) // 3):
                e = np.zeros(len(bnd)); e[j] = 1.0
                Vi = rc.integrate(be, Lii, Lib, e, np.zeros(len(interior)), np.array([40.0 * tau]))[-1]
                cur = Lfull[np.ix_(bnd, bnd)] @ e + Lfull[np.ix_(bnd, interior)] @ Vi
                k2.append(float(np.max(np.abs(cur - lam[:, j])) / np.max(np.abs(lam[:, j]))))
            row["controls"][be] = {"K1_rel_err": k1, "K1_pass": bool(k1 < rc.K1_TOL), "K2_rel_err": max(k2), "K2_pass": bool(max(k2) < 1e-6)}
        if not rc.HAVE_RUSTY:
            row["controls"]["rusty"] = "NOT RUN (rusty_sundials not importable)"
        rows.append(row)
        print("  %s L=%d N=%d d_max=%d tau=%.4f stiffness=%.2f  %s" % (row["tiling"], L, row["N"], row["d_max"], tau, row["stiffness"],
              "; ".join("%s K1 %.1e K2 %.1e" % (b, c["K1_rel_err"], c["K2_rel_err"]) if isinstance(c, dict) else "%s %s" % (b, c)
                        for b, c in row["controls"].items())), flush=True)
    return {"backends_run": backends, "rows": rows}


def score(d: dict) -> dict:
    ref = json.loads((D / "rc_network.json").read_text())
    r73 = next(r for r in ref["H2"] if r["family"] == "{7,3}" and r["N"] == 112)
    sq6 = next(r for r in ref["H2"] if r["family"] == "square" and r["N"] == 113)
    rows = d["rows"]
    c = next(r for r in rows if r["tiling"] == "{7,3}")
    G1 = abs(c["tau"] / r73["tau"] - 1) < 1e-3 and abs(c["stiffness"] / r73["stiffness"] - 1) < 1e-3
    G2 = c["controls"]["scipy"]["K1_pass"] and c["controls"]["scipy"]["K2_pass"]
    P1 = all(v["K1_pass"] and v["K2_pass"] for r in rows for v in r["controls"].values() if isinstance(v, dict))
    q45 = [r for r in rows if r["tiling"] in ("{5,4}", "{6,4}", "{4,5}")]
    t83 = next(r for r in rows if r["tiling"] == "{8,3}")["tau"]
    P2 = all(r["tau"] < r73["tau"] for r in q45) and 0.75 * r73["tau"] <= t83 <= 1.25 * r73["tau"]
    P3 = all(r["stiffness"] < sq6["stiffness"] for r in rows)
    return {"G1": G1, "G2": G2, "P1": P1, "P2": P2, "P3": P3, "rusty_run": "rusty" in d["backends_run"]}


def main() -> int:
    d = run()
    d["verdicts"] = score(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"])
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
