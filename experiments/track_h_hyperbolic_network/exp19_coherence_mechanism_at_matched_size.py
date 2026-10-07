#!/usr/bin/env python3
"""PREREGISTRATION_19.md: matched-size coherence (PR/n at n_match = 6, 50 draws) and the condition number of the
Jacobian restricted to columns of depth <= d, on the largest instance of each family. Writes
data/coherence_mechanism_at_matched_size.json and data/fig_coherence_matched.pdf; score() reads the file alone."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, build_triangular_disk, depths, harmonic_extension, jacobian,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "coherence_mechanism_at_matched_size.json"
FIG = HERE / "data" / "fig_coherence_matched.pdf"
TK = HERE / "data" / "tilings_kappa.json"
H0 = HERE / "data" / "h0.json"
N_MATCH, N_DRAWS, SEED, MAX_J_ENTRIES = 6, 50, 0, int(2e8)
SCORED = [("{7,3} L=4", lambda: build_hyperbolic(7, 3, 4)), ("{8,3} L=4", lambda: build_hyperbolic(8, 3, 4)),
          ("{5,4} L=5", lambda: build_hyperbolic(5, 4, 5)), ("{6,4} L=4", lambda: build_hyperbolic(6, 4, 4)),
          ("{4,5} L=6", lambda: build_hyperbolic(4, 5, 6)), ("square R=10", lambda: build_square_disk(10)),
          ("triangular R=6.45", lambda: build_triangular_disk(6.45))]
HYP = [n for n, _ in SCORED if n.startswith("{")]
FLAT = ["square R=10", "triangular R=6.45"]


def signatures(g):
    n, edges = len(g["nodes"]), g["edges"]
    bnd = boundary_nodes(g); d = depths(g, bnd)
    H, _ = harmonic_extension(n, edges, np.ones(len(edges)), bnd)
    ea = np.array([a for a, _ in edges]); eb = np.array([b for _, b in edges])
    return (H[ea] - H[eb]).T, np.minimum(d[ea], d[eb]), bnd


def gram(D):
    """Closed-form Gram matrix of the upper-triangular Jacobian columns: G_ef = 1/2[(d_e.d_f)^2 - sum_i d_e,i^2 d_f,i^2]."""
    M1 = D.T @ D; M2 = (D ** 2).T @ (D ** 2)
    return 0.5 * (M1 ** 2 - M2)


def pr_fraction(Gsub):
    nrm = np.sqrt(np.diag(Gsub)); C = Gsub / np.outer(nrm, nrm)
    ev = np.linalg.eigvalsh((C + C.T) / 2)
    return float(ev.sum() ** 2 / np.sum(ev ** 2) / len(ev)), float(max(ev.min(), 0.0))


def one_instance(name, g, rng):
    D, ed, bnd = signatures(g)
    m, E = D.shape
    G = gram(D)
    use_J = m * (m + 1) // 2 * E <= MAX_J_ENTRIES
    J = jacobian(len(g["nodes"]), g["edges"], np.ones(E), bnd) if use_J else None
    dmax = int(ed.max())
    log_kappa = []
    for k in range(dmax + 1):
        sub = np.where(ed <= k)[0]
        if use_J:
            s = np.linalg.svd(J[:, sub], compute_uv=False); lk = float(np.log10(s[0] / s[-1]))
        else:
            ev = np.linalg.eigvalsh(G[np.ix_(sub, sub)]); lk = float(0.5 * np.log10(ev[-1] / ev[0]))
        log_kappa.append(lk)
    by_depth = {}
    for k in range(dmax + 1):
        idx = np.where(ed == k)[0]; n = len(idx)
        if n < 2:
            continue
        f_full, lmin = pr_fraction(G[np.ix_(idx, idx)])
        rec = {"n_edges": int(n), "eff_dim_fraction_full": f_full, "lambda_min_normalised_gram": lmin}
        if n >= N_MATCH:
            fs = [pr_fraction(G[np.ix_(s, s)])[0] for s in (rng.choice(idx, N_MATCH, replace=False) for _ in range(N_DRAWS))]
            rec.update({"n_draws": N_DRAWS, "matched_pr_fraction_median": float(np.median(fs)),
                        "matched_pr_fraction_q10": float(np.percentile(fs, 10)), "matched_pr_fraction_q90": float(np.percentile(fs, 90))})
        by_depth[str(k)] = rec
    delta_bar = (log_kappa[dmax] - log_kappa[1]) / (dmax - 1) if dmax >= 2 else None
    r = {"name": name, "N": len(g["nodes"]), "E": int(E), "boundary": int(m), "d_max": dmax, "kappa_method": "explicit_J" if use_J else "gram",
         "log10_kappa_by_depth": log_kappa, "delta_bar": delta_bar, "by_depth": by_depth}
    print("  %-18s N=%5d d_max=%d method=%-10s log10 kappa_d: %s  delta_bar=%s" % (
        name, r["N"], dmax, r["kappa_method"], " ".join("%.2f" % x for x in log_kappa),
        "%.3f" % delta_bar if delta_bar is not None else "n/a"), flush=True)
    for k, v in by_depth.items():
        if "matched_pr_fraction_median" in v:
            print("      d=%s n=%4d PR/n=%.3f matched(6)=%.3f" % (k, v["n_edges"], v["eff_dim_fraction_full"], v["matched_pr_fraction_median"]))
    return r


def run() -> dict:
    rng = np.random.default_rng(SEED)
    rows = [one_instance(name, build(), rng) for name, build in SCORED]
    # G1: match by (N, E) to tilings_kappa.json (hyperbolic, with error bound) or h0.json (flat, v1.0; tolerance 1e-5)
    ref = {}
    for r in json.load(open(TK))["rows"]:
        ref[(r["N"], r["E"])] = ("tilings_kappa", r["log10_kappa"], max(1e-6, 100 * float(r["log10_kappa_error_bound"])))
    for r in json.load(open(H0)):
        if r.get("log10_kappa") is not None:
            ref.setdefault((r["N"], r["E"]), ("h0", r["log10_kappa"], 1e-5))
    g1 = []
    for r in rows:
        t = ref.get((r["N"], r["E"]))
        if t is None:
            g1.append({"name": r["name"], "ok": False, "reason": "no reference row"}); continue
        g1.append({"name": r["name"], "source": t[0], "ours": r["log10_kappa_by_depth"][-1], "reference": t[1], "tol": t[2],
                   "ok": bool(abs(r["log10_kappa_by_depth"][-1] - t[1]) <= t[2])})
    print("  G1 matches:", [(x["name"], x.get("source"), x["ok"]) for x in g1])
    return {"n_match": N_MATCH, "n_draws": N_DRAWS, "seed": SEED, "rows": rows, "g1": g1}


def score(d: dict) -> dict:
    R = {r["name"]: r for r in d["rows"]}
    G1 = len(d["g1"]) == 7 and all(x["ok"] for x in d["g1"])

    def matched(name, k):
        v = R[name]["by_depth"].get(str(k))
        return v.get("matched_pr_fraction_median") if v else None

    def deepest(name):
        ks = [int(k) for k, v in R[name]["by_depth"].items() if "matched_pr_fraction_median" in v]
        return max(ks)

    used = [(n, 3) for n in R] + [(n, deepest(n)) for n in R]
    G2 = all(R[n]["by_depth"][str(k)]["n_edges"] >= d["n_match"] and R[n]["by_depth"][str(k)].get("n_draws") == d["n_draws"] for n, k in used)
    P1 = all(matched(h, 3) >= 0.85 for h in HYP) and all(matched(f, 3) <= 0.80 for f in FLAT)
    db = {n: R[n]["delta_bar"] for n in R}
    P2a = db["square R=10"] >= 0.8 and db["triangular R=6.45"] >= 0.8 and db["{7,3} L=4"] <= 0.5 and db["{8,3} L=4"] <= 0.5
    P2b = all(db[h] < min(db["square R=10"], db["triangular R=6.45"]) for h in HYP)
    P3 = all(matched(f, deepest(f)) < 0.6 for f in FLAT) and all(matched(h, deepest(h)) >= 0.8 for h in HYP)
    return {"G1": bool(G1), "G2": bool(G2), "P1": bool(P1), "P2a": bool(P2a), "P2b": bool(P2b), "P3": bool(P3),
            "matched_pr_fraction_depth3": {n: round(matched(n, 3), 4) for n in R},
            "matched_pr_fraction_deepest": {n: [deepest(n), round(matched(n, deepest(n)), 4)] for n in R},
            "delta_bar": {n: round(v, 4) for n, v in db.items()}}


def figure(d):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for r in d["rows"]:
        hyp = r["name"].startswith("{")
        st = dict(ls="-" if hyp else "--", marker="o" if hyp else "s", ms=4, lw=0.9, label=r["name"])
        ks = [int(k) for k, v in r["by_depth"].items() if "matched_pr_fraction_median" in v]
        axes[0].plot(ks, [r["by_depth"][str(k)]["matched_pr_fraction_median"] for k in ks], **st)
        axes[1].plot(range(len(r["log10_kappa_by_depth"])), r["log10_kappa_by_depth"], **st)
    axes[0].set_xlabel("edge depth"); axes[0].set_ylabel("matched PR/n (n = 6, median of 50 draws)")
    axes[1].set_xlabel("d"); axes[1].set_ylabel("log10 kappa of J restricted to depth <= d")
    axes[0].legend(fontsize=7, frameon=False); fig.tight_layout(); fig.savefig(FIG)


def main() -> int:
    d = run(); d["verdicts"] = score(d); figure(d)
    OUT.write_text(json.dumps(d, indent=1))
    print("verdicts:", d["verdicts"]); print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
