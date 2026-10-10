#!/usr/bin/env python3
"""PREREGISTRATION_N1_LIMIT.md: the limit of bulk-boundary protection in the finite SSH chain under three perturbation classes.
Writes evidence/n1_limit.json."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "evidence" / "n1_limit.json"
N = 20
SITES = 2 * N + 1
EPS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
DRAWS = 50
PHASES = {"topological": (0.5, 1.0), "trivial": (1.0, 0.5)}


def chain(v, w, eps, kind, rng):
    H = np.zeros((SITES, SITES))
    hop = []
    for i in range(SITES - 1):
        t = v if i % 2 == 0 else w
        if kind == "chiral":
            t = t * (1 + eps * rng.uniform(-1, 1))
        hop.append(t)
        H[i, i + 1] = H[i + 1, i] = t
    if kind == "onsite":
        d = eps * rng.uniform(-1, 1, SITES)
        H[np.diag_indices(SITES)] = d
    if kind == "nnn":
        for i in range(SITES - 2):
            H[i, i + 2] = H[i + 2, i] = eps
    return H


def observe(H):
    ev, U = np.linalg.eigh(H)
    j = int(np.argmin(np.abs(ev)))
    psi = U[:, j]
    left = int(SITES // 4)
    WL = float(np.sum(psi[:left] ** 2))
    A = psi[0::2]
    B = psi[1::2]
    pol = float(np.sum(A ** 2) - np.sum(B ** 2))
    asym = float(np.max(np.abs(np.sort(ev) + np.sort(-ev))))
    return {"E0": float(abs(ev[j])), "WL": WL, "pol": pol, "asym": asym}


def main():
    res = {"N": N, "sites": SITES, "eps": EPS, "draws": DRAWS}
    # G1: exact harness and unperturbed checks
    r = subprocess.run([sys.executable, str(HERE / "ssh_exact.py")], capture_output=True, text=True)
    g1 = {"ssh_exact_exit": r.returncode}
    for ph, (v, w) in PHASES.items():
        o = observe(chain(v, w, 0.0, "none", np.random.default_rng(0)))
        g1[ph] = o
    g1["pass"] = bool(r.returncode == 0 and g1["topological"]["E0"] <= 1e-12 and g1["topological"]["WL"] >= 0.99 and abs(g1["topological"]["pol"] - 1) <= 1e-12
                      and g1["trivial"]["E0"] >= 0.4 and g1["trivial"]["WL"] < 0.5)
    res["G1"] = g1
    print("G1", g1, flush=True)

    table = {}
    for ph, (v, w) in PHASES.items():
        for kind in ("chiral", "onsite", "nnn"):
            for eps in EPS:
                rng = np.random.default_rng(1000 + int(eps * 1000) + {"chiral": 1, "onsite": 2, "nnn": 3}[kind] * 7)
                obs = [observe(chain(v, w, eps, kind, rng)) for _ in range(DRAWS)]
                table[f"{ph}|{kind}|{eps}"] = {"median_E0": float(np.median([o["E0"] for o in obs])), "frac_WL_ge_0_9": float(np.mean([o["WL"] >= 0.9 for o in obs])),
                                               "median_WL": float(np.median([o["WL"] for o in obs])), "median_pol": float(np.median([o["pol"] for o in obs])),
                                               "max_asym": float(np.max([o["asym"] for o in obs])),
                                               "any_E0_lt_0_1_and_WL_ge_0_9": bool(any(o["E0"] < 0.1 and o["WL"] >= 0.9 for o in obs))}
    res["table"] = table
    T = lambda kind, eps, key: table[f"topological|{kind}|{eps}"][key]  # noqa: E731
    # G2
    res["G2"] = {"chiral_max_asym_eps_0_5": T("chiral", 0.5, "max_asym"), "onsite_max_asym_eps_0_5": T("onsite", 0.5, "max_asym")}
    res["G2"]["pass"] = bool(all(T("chiral", e, "max_asym") <= 1e-12 for e in EPS if e < 1) and T("onsite", 0.5, "max_asym") > 1e-3)
    # P1
    res["P1"] = {"median_E0_chiral": {str(e): T("chiral", e, "median_E0") for e in EPS if e <= 0.5}, "frac_WL": {str(e): T("chiral", e, "frac_WL_ge_0_9") for e in EPS if e <= 0.3}}
    res["P1"]["pass"] = bool(all(T("chiral", e, "median_E0") <= 1e-6 for e in EPS if e <= 0.5) and all(T("chiral", e, "frac_WL_ge_0_9") >= 0.9 for e in EPS if e <= 0.3))
    # P2
    first = next((e for e in EPS if T("chiral", e, "frac_WL_ge_0_9") < 0.5), None)
    res["P2"] = {"first_eps_frac_below_0_5": first, "pass": bool(first is None or first >= 0.5)}
    # P3
    es = [e for e in EPS if e <= 0.5]
    ys = [T("onsite", e, "median_E0") for e in es]
    slope = float(np.polyfit(es, ys, 1)[0])
    res["P3"] = {"slope": slope, "frac_WL": {str(e): T("onsite", e, "frac_WL_ge_0_9") for e in EPS if e <= 0.3},
                 "pass": bool(0.2 <= slope <= 0.8 and all(T("onsite", e, "frac_WL_ge_0_9") >= 0.9 for e in EPS if e <= 0.3))}
    # P4
    first_nnn = next((e for e in EPS if T("nnn", e, "frac_WL_ge_0_9") < 0.5), None)
    res["P4"] = {"nnn_E0_0_1": T("nnn", 0.1, "median_E0"), "onsite_E0_0_1": T("onsite", 0.1, "median_E0"), "first_eps_nnn_frac_below_0_5": first_nnn,
                 "pass": bool(T("nnn", 0.1, "median_E0") > T("onsite", 0.1, "median_E0") and first_nnn is not None and first_nnn <= 0.5)}
    # P5
    res["P5"] = {"pass": bool(not any(table[f"trivial|{k}|{e}"]["any_E0_lt_0_1_and_WL_ge_0_9"] for k in ("chiral", "onsite", "nnn") for e in EPS if e <= 0.3))}
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    for k in ("G1", "G2", "P1", "P2", "P3", "P4", "P5"):
        print(k, {a: b for a, b in res[k].items() if a in ("pass", "slope", "first_eps_frac_below_0_5", "first_eps_nnn_frac_below_0_5", "nnn_E0_0_1", "onsite_E0_0_1")})
    for kind in ("chiral", "onsite", "nnn"):
        print(kind, "median E0:", [round(T(kind, e, "median_E0"), 4) for e in EPS])
        print(kind, "frac WL>=0.9:", [T(kind, e, "frac_WL_ge_0_9") for e in EPS])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
