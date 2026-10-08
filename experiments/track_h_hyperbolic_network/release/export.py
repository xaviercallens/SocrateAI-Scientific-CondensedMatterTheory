#!/usr/bin/env python3
"""Build the release bundles (Hugging Face dataset, Hugging Face "model"
repository for the numerical simulator, Zenodo archive) from the code and
data in this directory. Everything is regenerated; nothing is hand-edited.

  python3 release/export.py            -> release/build/{hf_dataset,hf_model,zenodo}

Contents
  hf_dataset/  graphs (edge lists, coordinates, boundary), per-instance
               conditioning, exact ranks, spectral gaps, integrator controls,
               RC time series, DtN matrices (npz), the paper PDF.
  hf_model/    the simulator code (no weights) with a model card.
  zenodo/      paper.pdf, dataset.zip, code.zip -- the files the Zenodo draft
               script uploads.
"""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np

TRACK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TRACK))
from hyperbolic_network import (  # noqa: E402
    boundary_nodes, build_hyperbolic, build_square_disk, build_triangular_disk, dtn, laplacian,
)

BUILD = TRACK / "release" / "build"
DS, MD, ZD = BUILD / "hf_dataset", BUILD / "hf_model", BUILD / "zenodo"
CODE_FILES = ["hyperbolic_network.py", "hyperbolic_exact.py", "probe_matched.py", "identifiability.py",
              "rc_network.py", "h2_explore.py", "interior_degree.py", "flat_scaling_mp.py", "disorder.py",
              "subspace_control.py", "prereg3_predictions.py", "paper/make_assets.py", "paper/build.py",
              "paper/main.tex", "paper/refs.bib", "paper/reviews/REVIEW_2026-09-27_v1.0.md",
              "paper/reviews/RESPONSE_2026-09-27_v1.0.md", "PREREGISTRATION_3.md",
              "release/export.py", "release/hf_upload.py", "release/zenodo_new_version.py", "release/zenodo_publish.py",
              "release/zenodo_draft.py", "release/zenodo_metadata.json", "release/check_bundle.py",
              "release/rusty_sundials_contrib/examples/python/rc_network/rc_network_benchmark.py",
              "release/rusty_sundials_contrib/examples/python/rc_network/test_rc_network.py",
              "release/rusty_sundials_contrib/examples/python/rc_network/README.md",
              "release/rusty_sundials_contrib/examples/python/rc_network/fixtures/hyperbolic_7_3_L2.json",
              "release/rusty_sundials_contrib/examples/python/rc_network/fixtures/square_R6.json",
              "release/rusty_sundials_contrib/apply.sh",
              "PREREGISTRATION.md", "PREREGISTRATION_2.md"]
HERE_TEX = TRACK / "release"

GRAPHS = ([("{7,3}", f"L={L}", lambda L=L: build_hyperbolic(7, 3, L)) for L in range(1, 7)]
          + [("square", f"R={R}", lambda R=R: build_square_disk(R)) for R in (3, 6, 10, 16)]
          + [("triangular", f"R={R}", lambda R=R: build_triangular_disk(R))
             for R in (3.225, 6.45, 7.0, 10.75, 11.5, 17.2, 18.5)])
DTN_MAX_N = 900  # dense DtN matrices stored up to this size


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=TRACK, capture_output=True, text=True).stdout.strip()
    except Exception:
        return "unknown"


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def export_graphs():
    (DS / "graphs").mkdir(parents=True)
    (DS / "dtn").mkdir()
    index = []
    for fam, par, build in GRAPHS:
        g = build()
        n = len(g["nodes"])
        bnd = boundary_nodes(g)
        tag = f"{fam.strip('{}').replace(',', '_')}_{par.replace('=', '')}".replace(".", "p")
        z = np.asarray(g["nodes"])
        rec = {"family": fam, "param": par, "N": n, "E": len(g["edges"]), "boundary_size": int(len(bnd)),
               "x": z.real.round(12).tolist(), "y": z.imag.round(12).tolist(),
               "edges": [list(map(int, e)) for e in g["edges"]], "boundary": [int(b) for b in bnd]}
        (DS / "graphs" / f"{tag}.json").write_text(json.dumps(rec))
        stored = n <= DTN_MAX_N
        if stored:
            lam = dtn(n, g["edges"], np.ones(len(g["edges"])), bnd)
            np.savez_compressed(DS / "dtn" / f"{tag}.npz", Lambda=lam, boundary=bnd)
        index.append({"graph_id": tag, "family": fam, "param": par, "N": n, "E": len(g["edges"]),
                      "boundary_size": int(len(bnd)), "graph_file": f"graphs/{tag}.json",
                      "dtn_file": f"dtn/{tag}.npz" if stored else ""})
        print(f"  graph {tag}: N={n}")
    write_csv(DS / "graphs_index.csv", index)


def export_tables():
    D = TRACK / "data"
    h0 = json.loads((D / "h0.json").read_text())
    write_csv(DS / "conditioning.csv", [
        {"lattice": r["name"], "N": r["N"], "E": r["E"], "boundary_size": r["boundary"], "max_depth": r["max_depth"],
         "log10_kappa": "" if r["log10_kappa"] is None else r["log10_kappa"],
         "numerically_singular_float64": r["numerically_singular"]} for r in h0])
    pm = json.loads((D / "probe_matched.json").read_text())
    write_csv(DS / "probe_matched.csv", [
        {"case": r["name"], "N": r["N"], "E": r["E"], "probes": r["probes"],
         "log10_kappa_DtN": "" if r["log10_kappa_DtN"] is None else r["log10_kappa_DtN"],
         "log10_kappa_NtD": "" if r["log10_kappa_NtD"] is None else r["log10_kappa_NtD"]} for r in pm])
    ident = json.loads((D / "identifiability.json").read_text())
    write_csv(DS / "exact_rank.csv", [
        {"case": r["name"], "N": r["N"], "E": r["E"], "probes": r["probes"],
         "rank_mod_2147483647": r["exact_ranks"]["2147483647"], "rank_mod_998244353": r["exact_ranks"]["998244353"],
         "deficiency": r["deficiency"], "unmeasured_degree2_nodes": r["unmeasured_degree2_nodes"],
         "float_gap_at_rank": "" if r.get("float_gap_at_rank") is None else r["float_gap_at_rank"],
         "log10_kappa_identifiable_subspace": r["log10_kappa_identifiable"]} for r in ident])
    full = json.loads((D / "exact_rank_full.json").read_text())
    write_csv(DS / "exact_rank_full_boundary.csv", [
        {"case": r["case"], "N": r["N"], "E": r["E"], "rank_mod_2147483647": r["ranks"]["2147483647"],
         "rank_mod_998244353": r["ranks"]["998244353"], "primes_agree": r["primes_agree"],
         "full_rank_certified": r["full_rank_certified"]} for r in full])
    # v1.1 additions (peer-review revisions); each file is optional so export works at any stage
    for name, csvname, conv in (
        ("flat_scaling_mp.json", "conditioning_arb.csv", lambda rows: [
            {"case": r["case"], "N": r["N"], "E": r["E"], "boundary_size": r["boundary"], "prec_bits": r["prec_bits"],
             "log10_kappa_arb": r["log10_kappa_arb"], "max_rel_radius_Ginv": r["max_rel_radius_Ginv"],
             "float64_log10_kappa": "" if r["float64_log10_kappa"] is None else r["float64_log10_kappa"],
             "control_pass": "" if r["control_pass"] is None else r["control_pass"]} for r in rows]),
        ("disorder.json", "disorder.csv", lambda d: [
            {"graph": r["graph"], "N": r["N"], "regime": r["regime"], "seed": "" if r["seed"] is None else r["seed"],
             "defect_node": r.get("defect_node", ""), "defect_depth": r.get("defect_depth", ""),
             "log10_kappa_logparam": "" if r["log10_kappa_log"] is None else r["log10_kappa_log"],
             "log10_kappa_raw": "" if r["log10_kappa_raw"] is None else r["log10_kappa_raw"]} for r in d["rows"]]),
        ("subspace_control.json", "subspace_control.csv", lambda rows: rows),
        ("tilings_kappa.json", "tilings_kappa.csv", lambda d: [
            {"tiling": "{%d,%d}" % (r["p"], r["q"]), "L": r["L"], "N": r["N"], "E": r["E"], "boundary": r["boundary"],
             "d_max": r["d_max"], "interior_degree_q": r["interior_degree_q"], "log10_kappa": r["log10_kappa"],
             "log10_kappa_error_bound": r["log10_kappa_error_bound"]} for r in d["rows"]]),
        ("localize_tolerance.json", "localize_tolerance.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "tolerance": c["tau"], "noise_eps": c["eps"], "contrast": c["f"],
             "nodes_in_class": r["nodes_in_class"], "top1": c["top1"]}
            for r in d["results"] for c in r["cells"].values()]),
        ("localize_noise.json", "localize_noise.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "contrast": cell, "nodes_in_class": r["nodes_in_class"],
             "eps": e, "top1": t, "eps_loc": c["eps_loc"]}
            for r in d["results"] for cell, c in r["cells"].items() for e, t in zip(c["eps"], c["top1"])]),
        ("localize_defect.json", "localize_defect.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "interior_nodes": r["interior_nodes"], "cell": cell,
             "depth": c["depth"], "nodes_in_class": c["nodes_in_class"], "top1": c["top1"],
             "mean_hops": c["mean_hops"], "contrast_acc": c["contrast_acc"], "noise_eps": d["eps"]}
            for r in d["results"] for cell, c in r["cells"].items()]),
        ("tolerance_null.json", "tolerance_null.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "tolerance": tau, "defect_node": r["defect_node"],
             "defect_depth": r["defect_depth"], "B_null_max": t["B_null_max"], "B_defect_min": t["B_defect_min"],
             "B_detected": t["B_detected"], "A_null_max": t["A_null_max"], "A_defect_min": t["A_defect_min"],
             "A_detected": t["A_detected"]}
            for r in d["results"] for tau, t in r["tau"].items()]),
        ("tda_noise.json", "tda_noise.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "config": cfg, "node": c["node"], "depth": c["depth"],
             "eps_max_metric": c["eps_max"]["metric"], "eps_max_H1": c["eps_max"]["H1"],
             "detected_metric_by_eps": "".join("Y" if x else "." for x in c["detected"]["metric"]),
             "detected_H1_by_eps": "".join("Y" if x else "." for x in c["detected"]["H1"]),
             "eps_grid": " ".join(str(e) for e in d["eps"])}
            for r in d["results"] for cfg, c in r["configs"].items()]),
        ("tda_defect.json", "tda_defect.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "boundary_size": r["boundary"], "config": cfg,
             "node": s.get("node", ""), "depth": s.get("depth", ""), "bottleneck_H0": s["bottleneck_H0"],
             "bottleneck_H1": s["bottleneck_H1"], "rel_metric_change": s["rel_metric_change"],
             "null_p95_H0": r["null_p95"]["bottleneck_H0"], "null_p95_H1": r["null_p95"]["bottleneck_H1"],
             "null_p95_metric": r["null_p95"]["rel_metric_change"],
             "detected_H1": s["detected"]["bottleneck_H1"], "detected_metric": s["detected"]["rel_metric_change"]}
            for r in d["results"] for cfg, s in r["configs"].items()]),
        # post-v1.1, low-tier workflow rounds (preregistrations 12, 14-19)
        ("exact_rank_certificates_for_other_tiling.json", "exact_rank_tilings.csv", lambda d: [
            {"tiling": r["tiling"], "L": r["L"], "N": r["N"], "E": r["E"], "boundary": r["boundary"], "prime": p,
             "rank": v["rank"], "rows_used": v["rows_used"], "certified_full": v["certified_full"],
             "certified_full_both_primes": r["certified_full_both"]}
            for r in d["rows"] for p, v in r["primes"].items()]),
        ("rc_benchmark_on_other_tilings.json", "rc_benchmark_tilings.csv", lambda d: [
            {"tiling": r["tiling"], "L": r["L"], "N": r["N"], "d_max": r["d_max"], "lambda_min": r["lambda_min"],
             "lambda_max": r["lambda_max"], "tau": r["tau"], "stiffness": r["stiffness"], "backend": b,
             "K1_rel_err": c["K1_rel_err"], "K1_pass": c["K1_pass"], "K2_rel_err": c["K2_rel_err"], "K2_pass": c["K2_pass"]}
            for r in d["rows"] for b, c in r["controls"].items()]),
        ("minimum_detectable_contrast.json", "minimum_contrast.csv", lambda d: [
            {"lattice": r["lattice"], "N": r["N"], "nodes_in_class": r["nodes_in_class"], "contrast": c["f"],
             "noise_eps": c["eps"], "top1": c["top1"], "trials": d["trials"]}
            for r in d["results"] for c in r["cells"].values()]),
        ("localisation_under_correlated_hardware_n.json", "hardware_noise.csv", lambda d: [
            {"board": b, "contrast": d["f"], "iid_eps": d["eps_iid"], "trials": d["trials"], "cell": cell, "top1": t}
            for b, v in d["boards"].items() for cell, t in v["cells"].items()]),
        ("coherence_versus_depth_across_tilings.json", "coherence_depth.csv", lambda d: [
            {"family": r["family"], "param": r["param"], "N": r["N"], "E": r["E"], "edge_depth": k, "n_edges": v["n_edges"],
             "n_pairs": v["n_pairs"], "median_abs_cos": v["median_abs_cos"], "mean_abs_cos": v["mean_abs_cos"],
             "p90_abs_cos": v["p90_abs_cos"], "participation_ratio": v["participation_ratio"], "eff_dim_fraction": v["eff_dim_fraction"]}
            for r in d["rows"] for k, v in r["by_depth"].items()]),
        ("coherence_mechanism_prediction_test.json", "coherence_mechanism_test.csv", lambda d: [
            {"instance": r["name"], "N": r["N"], "E": r["E"], "d_max": r["d_max"], "kappa_method": r["kappa_method"], "d_star": r["d_star"],
             "delta_bar": r["delta_bar"], "edge_depth": k, "n_edges": v["n_edges"], "eff_dim_fraction": v["eff_dim_fraction"],
             "log10_kappa_depth_le_d": r["log10_kappa_by_depth"][int(k)]}
            for r in d["rows"] for k, v in r["by_depth"].items()]),
        ("flat_growth_rate_over_matched_relative_w.json", "flat_rate_windows.csv", lambda d: [
            {"instance": r["name"], "family": r["family"], "R": r["R"], "N": r["N"], "d_max": r["d_max"], "d_star": r["d_star"],
             "window_used": " ".join(str(x) for x in r["window_used"]), "window_extended": r["window_extended"],
             "window_truncated": r["window_truncated"], "rate_decades_per_depth": r["rate"], "edge_depth": k,
             "log10_kappa_depth_le_d": r["log10_kappa_by_depth"][int(k)], "n_edges": v["n_edges"],
             "eff_dim_fraction": v["eff_dim_fraction"], "lambda_min_normalised_gram": v["lambda_min_normalised_gram"]}
            for r in d["rows"] for k, v in r["by_depth"].items() if int(k) <= r["d_star"]]),
        ("coherence_mechanism_at_matched_size.json", "coherence_matched.csv", lambda d: [
            {"instance": r["name"], "N": r["N"], "E": r["E"], "d_max": r["d_max"], "kappa_method": r["kappa_method"],
             "delta_bar": r["delta_bar"], "edge_depth": k, "n_edges": v["n_edges"],
             "log10_kappa_depth_le_d": r["log10_kappa_by_depth"][int(k)], "eff_dim_fraction_full": v["eff_dim_fraction_full"],
             "matched_pr_fraction_median": v.get("matched_pr_fraction_median", ""), "n_match": d["n_match"], "n_draws": d["n_draws"]}
            for r in d["rows"] for k, v in r["by_depth"].items()]),
    ):
        p = D / name
        if p.exists():
            write_csv(DS / csvname, conv(json.loads(p.read_text())))
    rc = json.loads((D / "rc_network.json").read_text())
    ex =json.loads((D / "h2_explore.json").read_text())
    gap = [{"family": r["family"], "N": r["N"], "lambda_min": r["lambda_min"], "lambda_max": r["lambda_max"],
            "tau": r["tau"], "stiffness": r["stiffness"], "exploratory": False} for r in rc["H2"]]
    gap += [{"family": "{7,3}", "N": r["N"], "lambda_min": r["lambda_min"], "lambda_max": "",
             "tau": 1 / r["lambda_min"], "stiffness": "", "exploratory": True} for r in ex["rows"] if r["L"] >= 5]
    write_csv(DS / "spectral_gap.csv", gap)
    ctrl = [{"graph": r.get("graph", "all"), "backend": r["backend"], "K1_rel_err": r.get("K1_rel_err", ""),
             "K1_pass": r.get("K1_pass", ""), "K2_rel_err": r.get("K2_rel_err", ""), "K2_pass": r.get("K2_pass", ""),
             "status": r.get("status", "run")} for r in rc["controls"]]
    write_csv(DS / "integrator_controls.csv", ctrl)
    shutil.copy(D / "interior_degree.json", DS / "interior_degree.json")


def export_timeseries():
    """RC step response V_i(t) on the two control networks, reference (expm) solution."""
    from scipy.linalg import expm
    rows = []
    rng = np.random.default_rng(3)
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6))):
        n = len(g["nodes"])
        bnd = boundary_nodes(g)
        L = laplacian(n, g["edges"], np.ones(len(g["edges"])))
        interior = np.setdiff1d(np.arange(n), bnd)
        Lii, Lib = L[np.ix_(interior, interior)], L[np.ix_(interior, bnd)]
        Vb = rng.uniform(-1, 1, len(bnd))
        Vinf = np.linalg.solve(Lii, -(Lib @ Vb))
        tau = 1.0 / np.linalg.eigvalsh(Lii)[0]
        for t in np.linspace(0, 5 * tau, 41):
            V = expm(-Lii * t) @ (0 - Vinf) + Vinf
            rows += [{"network": name, "t": round(float(t), 10), "node": int(interior[k]), "V": float(V[k])}
                     for k in range(len(interior))]
    write_csv(DS / "rc_step_response.csv", rows)


def dataset_card(commit):
    return f"""---
license: cc-by-4.0
pretty_name: Hyperbolic vs flat resistor networks - inverse conductance conditioning
tags:
- physics
- inverse-problems
- electrical-impedance-tomography
- hyperbolic-lattices
- resistor-networks
- numerical-linear-algebra
size_categories:
- n<1K
configs:
- config_name: graphs_index
  data_files: graphs_index.csv
- config_name: conditioning
  data_files: conditioning.csv
- config_name: probe_matched
  data_files: probe_matched.csv
- config_name: exact_rank
  data_files: exact_rank.csv
- config_name: exact_rank_full_boundary
  data_files: exact_rank_full_boundary.csv
- config_name: conditioning_arb
  data_files: conditioning_arb.csv
- config_name: disorder
  data_files: disorder.csv
- config_name: subspace_control
  data_files: subspace_control.csv
- config_name: tda_defect
  data_files: tda_defect.csv
- config_name: tda_noise
  data_files: tda_noise.csv
- config_name: tolerance_null
  data_files: tolerance_null.csv
- config_name: localize_defect
  data_files: localize_defect.csv
- config_name: localize_noise
  data_files: localize_noise.csv
- config_name: localize_tolerance
  data_files: localize_tolerance.csv
- config_name: tilings_kappa
  data_files: tilings_kappa.csv
- config_name: exact_rank_tilings
  data_files: exact_rank_tilings.csv
- config_name: rc_benchmark_tilings
  data_files: rc_benchmark_tilings.csv
- config_name: minimum_contrast
  data_files: minimum_contrast.csv
- config_name: hardware_noise
  data_files: hardware_noise.csv
- config_name: coherence_depth
  data_files: coherence_depth.csv
- config_name: coherence_matched
  data_files: coherence_matched.csv
- config_name: coherence_mechanism_test
  data_files: coherence_mechanism_test.csv
- config_name: flat_rate_windows
  data_files: flat_rate_windows.csv
- config_name: spectral_gap
  data_files: spectral_gap.csv
- config_name: integrator_controls
  data_files: integrator_controls.csv
- config_name: rc_step_response
  data_files: rc_step_response.csv
---

# Hyperbolic vs flat resistor networks: conditioning of the inverse conductance problem

Data accompanying the preprint *Logarithmic boundary depth and the conditioning of the discrete
inverse conductance problem on hyperbolic lattices* (X. Callens, 2026), included as `paper.pdf`.

## Contents

| File | What it contains |
|---|---|
| `graphs/*.json` | Layer-truncated {{7,3}} tilings (L=1..6) and square/triangular lattice disks: node coordinates (Poincare disk / plane), edge list, boundary nodes (face incidence) |
| `dtn/*.npz` | Dirichlet-to-Neumann map `Lambda` (unit conductances) for graphs with N <= {DTN_MAX_N} |
| `conditioning.csv` | log10 condition number of the DtN sensitivity Jacobian; empty and `numerically_singular_float64=True` where float64 cannot resolve it |
| `probe_matched.csv` | DtN and Neumann-to-Dirichlet conditioning, full vs subsampled boundary |
| `exact_rank.csv` | Exact Jacobian ranks over GF(p) for two primes; deficiency vs number of unmeasured degree-2 nodes; condition number on the identifiable subspace |
| `exact_rank_full_boundary.csv` | Exact full-boundary Jacobian ranks over GF(p), two primes: full-rank certificates |
| `conditioning_arb.csv` | (v1.1) log10 condition number in 512-bit ball arithmetic for the float64-singular flat lattices, with certified radii and the two unsaturated controls |
| `disorder.csv` | (v1.1) log10 kappa (log-parametrised and raw Jacobian) under U[0.5,1.5] and log-uniform [0.1,10] conductances (5 seeds) and x100 / x0.01 defects |
| `subspace_control.csv` | (v1.1) probe-matched dimensionality control: square lattice sigma_1/sigma_r vs hyperbolic identifiable-subspace kappa |
| `tda_defect.csv` | (post-v1.1, not in the paper) persistent homology (Gudhi) of the boundary resistance metric with and without a bulk defect, vs a global-disorder null. The null was mis-sized; see `TDA_RESULTS.md` |
| `tda_noise.csv` | (post-v1.1, not in the paper) defect detection vs measurement-noise level (eps_max), metric and H1 detectors |
| `localize_defect.csv` | (post-v1.1, not in the paper) single-node defect localisation from two noisy NtD maps (oracle-dictionary matched filter); 60/60 cells perfect at noise 3e-4, so it is a ceiling, not a measurement of the failure boundary |
| `tilings_kappa.csv` | (post-v1.1, not in the paper) log10 condition number for {7,3}, {8,3}, {5,4}, {6,4}, {4,5} at L=1..6, with d_max and float64 error bounds (Gram-matrix method, controls in the repository) |
| `localize_tolerance.csv` | (post-v1.1, not in the paper) localisation top-1 on random boards with component tolerance 0.1 %, 1 %, 5 % and an ideal-model decoder; tolerance has no effect in this differential setting |
| `localize_noise.csv` | (post-v1.1, not in the paper) localisation top-1 vs noise level and eps_loc (largest noise with top-1 >= 0.9) at the deepest node, contrasts x1.25 and x2 |
| `tolerance_null.csv` | (post-v1.1, not in the paper) defect detection vs component tolerance (0.1 %, 1 %, 5 %), model-based and differential regimes; only the extreme x100 contrast is tested |
| `exact_rank_tilings.csv` | (v1.2) exact full-column-rank certificates (random row-combination method, two primes) for 11 instances of {{7,3}}, {{8,3}}, {{5,4}}, {{6,4}}, {{4,5}} up to E = 1604 |
| `rc_benchmark_tilings.csv` | (v1.2) RC relaxation time, stiffness and the K1/K2 integrator controls (SciPy BDF and rusty-SUNDIALS CVODE) on {{7,3}} L=2, {{8,3}} L=2, {{5,4}} L=3, {{6,4}} L=2, {{4,5}} L=4 |
| `minimum_contrast.csv` | (v1.2) localisation top-1 vs true contrast (x0.5 to x2) and noise (1e-4 to 3e-3) at the deepest node of four lattices; both geometries localise +-10 % at the 3e-4 budget |
| `hardware_noise.csv` | (v1.2) localisation top-1 under common-mode offset, gain drift and ADC quantisation at N~112, contrast x2; a floor (49/50 cells at 1.00), not a failure boundary |
| `coherence_depth.csv` | (v1.2) per edge depth and instance: exhaustive abs-cosine statistics between Jacobian columns of equal-depth edges and the effective dimension fraction (participation ratio / count) of their normalised Gram matrix |
| `coherence_matched.csv` | (v1.2) per depth on the largest instance of each family: log10 kappa of the Jacobian restricted to columns of depth <= d, the full-class effective dimension fraction and the six-column matched-size median of 50 draws |
| `coherence_mechanism_test.csv` | (v1.2) test of the band-counting argument on unseen instances ({{7,3}} L=5, {{4,5}} L=7, square R=16, triangular R=10.75): effective dimension fraction and depth-restricted log10 kappa per depth |
| `flat_rate_windows.csv` | (v1.2, exploratory) growth rate of the depth-restricted log10 kappa over windows fixed in relative depth on square R=6..22 and triangular R=3.2..17.2, with per-class effective dimension fraction and smallest normalised-Gram eigenvalue |
| `spectral_gap.csv` | Dirichlet spectral gap, RC relaxation time and stiffness; `exploratory=True` rows were not preregistered |
| `interior_degree.json` | Integer check that interior nodes of the {{7,3}} truncations have degree 3, and that the interior of G_L is G_(L-1) (coordinates and edge sets) |
| `integrator_controls.csv` | K1 (matrix-exponential known answer) and K2 (steady state = DtN column) controls per integrator; rows with `status` other than `run` were not executed |
| `rc_step_response.csv` | Reference (matrix-exponential) RC step response V_i(t), C=1, on {{7,3}} L=2 and square R=6 |

## Provenance and reproduction

Generated from commit `{commit}` of
https://github.com/xaviercallens/SocrateAI-Scientific-CondensedMatterTheory, directory
`experiments/track_h_hyperbolic_network`:

```
python3 hyperbolic_network.py --self-test && python3 hyperbolic_exact.py --self-test
python3 hyperbolic_exact.py && python3 probe_matched.py && python3 identifiability.py && python3 rc_network.py
python3 h2_explore.py && python3 interior_degree.py
python3 release/export.py
```

Each claim built on these data carries an evidence tier in `docs/elenchus/ledger.json` of that repository.

## Known limitations

- Condition numbers are float64 SVD values; "numerically singular" means unresolved, not infinite.
- The two-integrator (SciPy BDF, rusty-SUNDIALS CVODE) cross-validation covers two networks of ~110 nodes.
- The probe-matched identifiable-subspace metric was chosen post hoc (deviation from preregistration).

## License

Data and paper: CC BY 4.0. Code (see the companion model repository and the Zenodo archive): MIT.

## Citation

Callens, X. (2026). Logarithmic boundary depth and the conditioning of the discrete inverse
conductance problem on hyperbolic lattices. Preprint.
"""


def model_card(commit):
    return f"""---
license: mit
tags:
- physics
- numerical-simulation
- inverse-problems
- resistor-networks
- hyperbolic-lattices
library_name: numpy
---

# Hyperbolic resistor-network simulator (numerical model, no trained weights)

This repository holds a **numerical simulator**, not a machine-learning model: there are no weights and
no training. It builds layer-truncated hyperbolic {{p,q}} tilings and flat lattice disks, and computes

- the Dirichlet-to-Neumann map (Schur complement) and its exact sensitivity Jacobian,
- exact Jacobian ranks over GF(p),
- the Neumann-to-Dirichlet map and its conditioning,
- the RC network dynamics `C dV/dt = -(L_ii V + L_ib V_b)` with SciPy BDF or, when installed, the
  rusty-SUNDIALS CVODE integrator (https://github.com/xaviercallens/rusty-SUNDIALS), gated by
  analytic controls K1 (matrix exponential) and K2 (steady state = DtN).

## Use

```
pip install numpy scipy
python3 hyperbolic_network.py --self-test
python3 -c "from hyperbolic_network import build_hyperbolic, boundary_nodes, dtn; import numpy as np; \\
g = build_hyperbolic(7, 3, 2); b = boundary_nodes(g); print(dtn(len(g['nodes']), g['edges'], np.ones(len(g['edges'])), b).shape)"
```

To run the CVODE leg, build the rusty-SUNDIALS Python extension (`maturin develop` in
`crates/rusty-sundials-py`) and re-run `rc_network.py`.

## Intended use and limits

Research on conditioning of discrete inverse problems and design of tabletop resistor/RC network experiments.
Results are linearised sensitivities at unit conductances; see the paper's limitations section.

Source commit: `{commit}`. Dataset: companion Hugging Face dataset. Paper: `paper.pdf`.
"""


def zip_dir(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(src))


def main():
    if BUILD.exists():  # generated output only
        shutil.rmtree(BUILD)
    DS.mkdir(parents=True)
    commit = git_commit()
    # default: the published v1.1 PDF (keeps the v1.1 bundles reproducible); --v12 bundles the v1.2 draft instead
    pdf = TRACK / "paper" / ("main_v1_2.pdf" if "--v12" in sys.argv else "main.pdf")
    print("bundling", pdf.name)
    export_graphs()
    export_tables()
    export_timeseries()
    shutil.copy(pdf, DS / "paper.pdf")
    (DS / "README.md").write_text(dataset_card(commit))

    MD.mkdir()
    for f in CODE_FILES:
        dst = MD / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(TRACK / f, dst)
    shutil.copy(pdf, MD / "paper.pdf")
    (MD / "README.md").write_text(model_card(commit))
    (MD / "LICENSE").write_text((HERE_TEX / "LICENSE-MIT").read_text())

    ZD.mkdir()
    shutil.copy(pdf, ZD / "paper.pdf")
    zip_dir(DS, ZD / "dataset.zip")
    zip_dir(MD, ZD / "code.zip")
    (BUILD / "MANIFEST.json").write_text(json.dumps({
        "commit": commit,
        "files": {str(p.relative_to(BUILD)): p.stat().st_size for p in sorted(BUILD.rglob("*")) if p.is_file()}},
        indent=1))
    print(f"built {BUILD} from commit {commit[:12]}")


if __name__ == "__main__":
    main()
