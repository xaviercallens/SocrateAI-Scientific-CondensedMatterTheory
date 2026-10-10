#!/usr/bin/env python3
"""POST-HOC diagnostic for PREREGISTRATION_26 (written after its data existed; not a preregistered test).
Hypothesis: on the diagonal strip the node values z_n = lam(k_n) lam(q - k_n) are real after removing the common phase
e^{-iq/2}, but of both signs (the sign flips when q - k wraps around 2 pi). The preregistered prediction used moduli only.
With signed nodes the node set is one interval [z_min, z_max] through zero, and the Green exponent is evaluated on it.
Compares with the six measured block rates (W = 384). Writes data/diagonal_signed_nodes_diagnostic.json."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "data" / "diagonal_boundary_orientation_and_the_gr.json").read_text())


def lam(k):
    A = 1 + np.exp(1j * k); C = 1 + np.exp(-1j * k)
    disc = np.sqrt(16 - 4 * A * C + 0j)
    disc = np.where(disc.real < 0, -disc, disc)
    return 2 * C / (4 + disc)


def green_rate(zmin, zmax):
    th = np.linspace(0.0005, np.pi, 6001); zeta = np.exp(1j * th)
    w = (2 * zeta - (zmax + zmin)) / (zmax - zmin); s = np.sqrt(w * w - 1 + 0j)
    big = np.where(np.abs(w + s) >= np.abs(w - s), w + s, w - s)
    return float(np.log(np.abs(big)).max() / np.log(10))


W = 384
out = {"post_hoc": True, "W": W, "rows": {}}
for label in ("8", "16", "24", "32", "40", "48"):
    i = data["W384"][label]["i"]; q = 2 * np.pi * i / W
    k = 2 * np.pi * np.arange(W) / W
    z = lam(k) * lam(q - k) * np.exp(1j * q / 2)
    imag_max = float(np.abs(z.imag).max())
    zr = z.real
    moduli_rate = green_rate(np.abs(zr).min(), np.abs(zr).max())     # what the preregistration used
    signed_rate = green_rate(zr.min(), zr.max())                      # one interval through zero
    meas = data["W384"][label]["rate"]
    out["rows"][label] = {"i": i, "max_abs_imag_after_phase": imag_max, "zmin_signed": float(zr.min()), "zmax_signed": float(zr.max()),
                          "moduli_only_rate": moduli_rate, "signed_rate": signed_rate, "measured_rate": meas,
                          "relative_error_signed": abs(signed_rate - meas) / meas}
    print("label %2s q=%.3f: imag part after the common phase %.1e ; signed interval [%.4f, %.4f] ; moduli-only %.4f ; signed %.4f ; measured %.4f ; rel. error %.4f" % (
        label, q, imag_max, zr.min(), zr.max(), moduli_rate, signed_rate, meas, abs(signed_rate - meas) / meas))
(HERE / "data" / "diagonal_signed_nodes_diagnostic.json").write_text(json.dumps(out, indent=1))
print("wrote data/diagonal_signed_nodes_diagnostic.json")
