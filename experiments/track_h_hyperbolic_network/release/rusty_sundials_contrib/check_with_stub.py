#!/usr/bin/env python3
"""Validate the benchmark script's own logic with a SciPy-backed stand-in for
rusty_sundials.CvodeSolver (same call signature). This checks the harness, not
rusty-SUNDIALS; the real check is running the benchmark against the built wheel."""
import sys
import types
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


class CvodeSolver:
    def __init__(self, method="bdf", rtol=1e-8, atol=1e-10, max_steps=500):
        self.rtol, self.atol = rtol, atol

    def solve(self, rhs, t0, y0, t_out):
        s = solve_ivp(lambda t, y: np.asarray(rhs(t, list(y))), (t0, t_out), y0, method="BDF",
                      rtol=self.rtol, atol=self.atol)
        return float(s.t[-1]), s.y[:, -1].tolist()


sys.modules["rusty_sundials"] = types.SimpleNamespace(CvodeSolver=CvodeSolver)
sys.path.insert(0, str(Path(__file__).resolve().parent / "examples" / "python" / "rc_network"))
import rc_network_benchmark  # noqa: E402

sys.exit(rc_network_benchmark.main())
