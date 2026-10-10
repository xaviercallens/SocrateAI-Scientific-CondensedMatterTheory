#!/usr/bin/env python3
"""PREREGISTRATION_N1_LIMIT2.md: repeat of N1-L with corrected gates. Writes evidence/n1_limit2.json."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp_n1_limit import EPS, SITES, chain  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "evidence" / "n1_limit2.json"
DRAWS = 50
SEED_BASE = 2000
PHASES = {"topological": (0.5, 1.0), "trivial": (1.0, 0.5)}


def asym(ev):
    s = np.sort(ev)
    return float(np.max(np.abs(s + s[::-1])))


def observe(H):
    ev, U = np.linalg.eigh(H)
    j = int(np.argmin(np.abs(ev)))
    psi = U[:, j]
    q = SITES // 4
    return {"E0": float(abs(ev[j])), "WL": float(np.sum(psi[:q] ** 2)), "WR": float(np.sum(psi[-q:] ** 2)),
            "pol": float(np.sum(psi[0::2] ** 2) - np.sum(psi[1::2] ** 2)), "asym": asym(ev)}


def main():
    res = {"sites": SITES, "eps": EPS, "draws": DRAWS, "seed_base": SEED_BASE}
    # G0
    a_known = asym(np.array([0.3, 0.1, -0.2]))
    a_top = observe(chain(0.5, 1.0, 0.0, "none", np.random.default_rng(0)))["asym"]
    res["G0"] = {"asym_known_case": a_known, "asym_unperturbed_topological": a_top, "pass": bool(abs(a_known - 0.2) <= 1e-12 and a_top <= 1e-12)}
    print("G0", res["G0"], flush=True)
    if not res["G0"]["pass"]:
        OUT.write_text(json.dumps(res, indent=2))
        print("G0 FAILED: card withdrawn, nothing run")
        return 1
    # G1
    r = subprocess.run([sys.executable, str(HERE / "ssh_exact.py")], capture_output=True, text=True)
    g1 = {"ssh_exact_exit": r.returncode}
    for ph, (v, w) in PHASES.items():
        g1[ph] = observe(chain(v, w, 0.0, "none", np.random.default_rng(0)))
    t, tr = g1["topological"], g1["trivial"]
    g1["pass"] = bool(r.returncode == 0 and t["E0"] <= 1e-12 and t["WL"] >= 0.99 and abs(t["pol"] - 1) <= 1e-12
                      and tr["E0"] <= 1e-12 and tr["WR"] >= 0.99 and tr["WL"] <= 0.01)
    res["G1"] = g1
    print("G1", {k: (v if k in ("pass", "ssh_exact_exit") else {a: round(b, 6) for a, b in v.items()}) for k, v in g1.items()}, flush=True)

    table = {}
    for ph, (v, w) in PHASES.items():
        for kind in ("chiral", "onsite", "nnn"):
            for eps in EPS:
                rng = np.random.default_rng(SEED_BASE + int(eps * 1000) + {"chiral": 1, "onsite": 2, "nnn": 3}[kind] * 7 + (0 if ph == "topological" else 50000))
                obs = [observe(chain(v, w, eps, kind, rng)) for _ in range(DRAWS)]
                table[f"{ph}|{kind}|{eps}"] = {"median_E0": float(np.median([o["E0"] for o in obs])), "frac_WL_ge_0_9": float(np.mean([o["WL"] >= 0.9 for o in obs])),
                                               "median_WL": float(np.median([o["WL"] for o in obs])), "max_asym": float(np.max([o["asym"] for o in obs])),
                                               "min_asym": float(np.min([o["asym"] for o in obs])),
                                               "any_E0_lt_0_1_and_WL_ge_0_9": bool(any(o["E0"] < 0.1 and o["WL"] >= 0.9 for o in obs))}
    res["table"] = table
    T = lambda kind, eps, key: table[f"topological|{kind}|{eps}"][key]  # noqa: E731
    res["G2"] = {"chiral_max_asym_all_eps_lt_1": max(T("chiral", e, "max_asym") for e in EPS if e < 1), "onsite_min_asym_eps_0_5": T("onsite", 0.5, "min_asym")}
    res["G2"]["pass"] = bool(res["G2"]["chiral_max_asym_all_eps_lt_1"] <= 1e-12 and res["G2"]["onsite_min_asym_eps_0_5"] > 1e-3)
    res["P1"] = {"pass": bool(all(T("chiral", e, "median_E0") <= 1e-6 for e in EPS if e <= 0.5) and all(T("chiral", e, "frac_WL_ge_0_9") >= 0.9 for e in EPS if e <= 0.3))}
    first = next((e for e in EPS if T("chiral", e, "frac_WL_ge_0_9") < 0.5), None)
    res["P2"] = {"first_eps_frac_below_0_5": first, "pass": bool(first is None or first >= 0.5)}
    es = [e for e in EPS if e <= 0.5]
    slope = float(np.polyfit(es, [T("onsite", e, "median_E0") for e in es], 1)[0])
    res["P3"] = {"slope": slope, "pass": bool(0.2 <= slope <= 0.8 and all(T("onsite", e, "frac_WL_ge_0_9") >= 0.9 for e in EPS if e <= 0.3))}
    first_nnn = next((e for e in EPS if T("nnn", e, "frac_WL_ge_0_9") < 0.5), None)
    res["P4"] = {"nnn_E0_0_1": T("nnn", 0.1, "median_E0"), "onsite_E0_0_1": T("onsite", 0.1, "median_E0"), "first_eps_nnn_frac_below_0_5": first_nnn,
                 "pass": bool(T("nnn", 0.1, "median_E0") > T("onsite", 0.1, "median_E0") and first_nnn is not None and first_nnn <= 0.5)}
    res["P5"] = {"pass": bool(not any(table[f"trivial|{k}|{e}"]["any_E0_lt_0_1_and_WL_ge_0_9"] for k in ("chiral", "onsite", "nnn") for e in EPS if e <= 0.3))}
    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")
    for k in ("G2", "P1", "P2", "P3", "P4", "P5"):
        print(k, res[k])
    for kind in ("chiral", "onsite", "nnn"):
        print(kind, "median E0:", [round(T(kind, e, "median_E0"), 4) for e in EPS], "frac:", [T(kind, e, "frac_WL_ge_0_9") for e in EPS])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
