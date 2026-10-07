#!/usr/bin/env python3
"""PREREGISTRATION_2.md part C: the RC network and H2, with a two-code
cross-validation that uses rusty-SUNDIALS' CVODE when it is importable.

Model. A capacitance C=1 from every node to ground; boundary voltages
imposed. Interior dynamics:  C dV_i/dt = -(L_ii V_i + L_ib V_b).
Relaxation time tau = C / lambda_min(L_ii); stiffness ratio
lambda_max(L_ii) / lambda_min(L_ii). This is the time-resolved measurement
a physical circuit (and an ESP32 sampling it) actually produces.

Controls, in order; a later step is not reported unless the earlier one
passed:
  K1 known answer: the exact solution V(t) = expm(-L_ii t)(V0 - Vinf) + Vinf
     must be reproduced by each integrator at every output time to within
     K1_TOL = 1e-5 relative (max norm). rtol = 1e-8 is a LOCAL per-step
     tolerance; accumulated global error is legitimately larger, so the
     acceptance threshold is fixed here explicitly rather than implied.
  K2 two-code cross-validation: steady-state boundary currents under
     V_b = e_j (integrated to t >> tau) must equal column j of the
     Schur-complement Lambda to within 1e-6 relative.
Backends: 'rusty' (rusty_sundials.CvodeSolver, BDF) if importable; 'scipy'
(solve_ivp BDF) always, as the reference integrator. A backend that is not
importable is reported as NOT RUN, never as passed.

H2 itself (lambda_min(L_ii) vs N) needs no integrator -- it is an
eigenvalue -- and is computed with numpy for every size.

Outputs: data/rc_network.json
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hyperbolic_network import (  # noqa: E402
    build_hyperbolic, build_square_disk, build_triangular_disk, boundary_nodes, dtn, laplacian,
)

OUT = Path(__file__).resolve().parent / "data" / "rc_network.json"
RTOL, ATOL = 1e-8, 1e-10
K1_TOL = 1e-5

try:
    from rusty_sundials import CvodeSolver  # built from ~/rusty-SUNDIALS/crates/rusty-sundials-py
    HAVE_RUSTY = True
except Exception:
    HAVE_RUSTY = False


def blocks(g, bnd):
    n = len(g["nodes"])
    L = laplacian(n, g["edges"], np.ones(len(g["edges"])))
    interior = np.setdiff1d(np.arange(n), bnd)
    return L, interior, L[np.ix_(interior, interior)], L[np.ix_(interior, bnd)]


def integrate(backend, Lii, Lib, Vb, V0, t_out):
    """Return V_i at each time in t_out (t0 = 0)."""
    forcing = -(Lib @ Vb)

    def rhs(t, y):
        return (-(Lii @ np.asarray(y)) + forcing).tolist() if backend == "rusty" else -(Lii @ y) + forcing

    if backend == "scipy":
        sol = solve_ivp(rhs, (0.0, t_out[-1]), V0, method="BDF", t_eval=t_out, rtol=RTOL, atol=ATOL,
                        jac=-Lii)
        return sol.y.T
    if backend == "rusty":
        # The binding returns only the final state and takes no Jacobian;
        # step from output time to output time, restarting from the last state.
        out, y, t = [], list(V0), 0.0
        solver = CvodeSolver(method="bdf", rtol=RTOL, atol=ATOL, max_steps=200000)
        for tk in t_out:
            if tk > t:
                t, y = solver.solve(rhs, t, y, tk)
            out.append(np.array(y))
        return np.array(out)
    raise ValueError(backend)


def known_answer(Lii, Lib, Vb, V0, t_out):
    Vinf = np.linalg.solve(Lii, -(Lib @ Vb))
    return np.array([expm(-Lii * t) @ (V0 - Vinf) + Vinf for t in t_out])


def main() -> int:
    report = {"rusty_sundials_importable": HAVE_RUSTY, "controls": [], "H2": []}

    # ---- H2: spectrum, every size ----------------------------------------
    print("H2: Dirichlet spectral gap lambda_min(L_ii) and stiffness vs N")
    families = [("{7,3}", [build_hyperbolic(7, 3, L) for L in (1, 2, 3, 4)]),
                ("square", [build_square_disk(R) for R in (3, 6, 10, 16)]),
                ("triangular", [build_triangular_disk(R) for R in (3.2, 6.5, 11.5, 18.5)])]
    for fam, graphs in families:
        for g in graphs:
            _, _, Lii, _ = blocks(g, boundary_nodes(g))
            ev = np.linalg.eigvalsh(Lii)
            row = {"family": fam, "N": len(g["nodes"]), "lambda_min": float(ev[0]),
                   "lambda_max": float(ev[-1]), "stiffness": float(ev[-1] / ev[0]),
                   "tau": float(1.0 / ev[0])}
            report["H2"].append(row)
            print(f"  {fam:10} N={row['N']:5d}  lambda_min={row['lambda_min']:.4f}  "
                  f"tau={row['tau']:8.2f}  stiffness={row['stiffness']:9.1f}")

    # ---- Controls K1, K2 on small instances --------------------------------
    backends = ["scipy"] + (["rusty"] if HAVE_RUSTY else [])
    print(f"\ncontrols (backends run: {backends}; rusty-SUNDIALS "
          f"{'importable' if HAVE_RUSTY else 'NOT importable -> CVODE path NOT RUN'})")
    rng = np.random.default_rng(3)
    for name, g in (("{7,3} L=2", build_hyperbolic(7, 3, 2)), ("square R=6", build_square_disk(6))):
        bnd = boundary_nodes(g)
        L, interior, Lii, Lib = blocks(g, bnd)
        tau = 1.0 / np.linalg.eigvalsh(Lii)[0]
        t_out = np.array([0.25, 1.0, 4.0, 16.0]) * tau
        Vb = rng.uniform(-1, 1, len(bnd))
        V0 = np.zeros(len(interior))
        exact = known_answer(Lii, Lib, Vb, V0, t_out)
        lam = dtn(len(g["nodes"]), g["edges"], np.ones(len(g["edges"])), bnd)
        for be in backends:
            t0 = time.time()
            got = integrate(be, Lii, Lib, Vb, V0, t_out)
            err_k1 = float(np.max(np.abs(got - exact)) / np.max(np.abs(exact)))
            # K2: steady state under V_b = e_j for three probes j
            k2_errs = []
            for j in (0, len(bnd) // 3, 2 * len(bnd) // 3):
                e = np.zeros(len(bnd)); e[j] = 1.0
                Vi = integrate(be, Lii, Lib, e, np.zeros(len(interior)), np.array([40.0 * tau]))[-1]
                currents = L[np.ix_(bnd, bnd)] @ e + L[np.ix_(bnd, interior)] @ Vi
                k2_errs.append(float(np.max(np.abs(currents - lam[:, j])) / np.max(np.abs(lam[:, j]))))
            row = {"graph": name, "backend": be, "K1_rel_err": err_k1, "K1_pass": err_k1 < K1_TOL,
                   "K2_rel_err": max(k2_errs), "K2_pass": max(k2_errs) < 1e-6,
                   "seconds": round(time.time() - t0, 2)}
            report["controls"].append(row)
            print(f"  {name:11} {be:6}  K1 err={err_k1:.1e} ({'pass' if row['K1_pass'] else 'FAIL'})  "
                  f"K2 err={row['K2_rel_err']:.1e} ({'pass' if row['K2_pass'] else 'FAIL'})  "
                  f"{row['seconds']}s")
    if not HAVE_RUSTY:
        report["controls"].append({"backend": "rusty", "status": "NOT RUN (extension not importable)"})

    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
