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
              "rc_network.py", "h2_explore.py", "interior_degree.py", "paper/make_assets.py", "paper/build.py",
              "paper/main.tex", "paper/refs.bib", "release/export.py", "release/hf_upload.py",
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
    pdf = TRACK / "paper" / "main.pdf"
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
