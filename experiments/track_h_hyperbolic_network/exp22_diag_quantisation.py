#!/usr/bin/env python3
"""POST-HOC diagnostic for PREREGISTRATION_22 (written after its data existed; not part of the preregistered tests).
Why does the {7,3} L=2 board localise a defect at 1 bit of quantisation? Records, noiselessly and per bit count, how
many entries of the quantised difference are non-zero, its norm against the true signature's norm, whether the decode
is right, and how an ADC that spans +-max|P0| maps onto the step relative to the rms entry used in the preregistration.
Writes data/quantisation_diagnostic.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exp22_hardware_noise_failure_boundaries as e22  # noqa: E402
import exp17_localisation_under_correlated_hardware_n as e17  # noqa: E402

OUT = Path(__file__).resolve().parent / "data" / "quantisation_diagnostic.json"


def main() -> int:
    out = {"post_hoc": True, "boards": {}}
    for name, build in e22.BOARDS:
        b = e17.Board(build()); s = b.s; P0 = b.P0
        rec = {"s_rms": float(s), "max_abs_P0": float(np.abs(P0).max()), "fraction_entries_below_s_over_2": float((np.abs(P0) < s / 2).mean()),
               "full_scale_bits_minus_rms_bits": float(np.log2(2 * np.abs(P0).max() / s)), "bits": {}}
        for bits in (1, 2, 3, 4, 6):
            q = 2.0 ** (-bits) * s; per_node = []
            for v in b.nodes:
                i_true = int(np.where(b.interior == v)[0][0])
                d = b.flat[e22.truth_index(b, v, 2.0)]
                x = np.round((P0 + d.reshape(P0.shape)) / q) * q - np.round(P0 / q) * q
                k = int(np.argmin(np.linalg.norm(b.flat - x.ravel(), axis=1))) // e22.ND
                per_node.append({"nonzero_entries": int((x != 0).sum()), "norm_x": float(np.linalg.norm(x)), "norm_true_signature": float(np.linalg.norm(d)),
                                 "decode_correct": bool(k == i_true)})
            rec["bits"][str(bits)] = {"step": float(q), "per_node": per_node}
        out["boards"][name] = rec
        print(name, "full-scale bits minus rms bits = %.2f" % rec["full_scale_bits_minus_rms_bits"],
              {k: (v["per_node"][0]["nonzero_entries"], round(v["per_node"][0]["norm_x"], 2), v["per_node"][0]["decode_correct"]) for k, v in rec["bits"].items()})
    OUT.write_text(json.dumps(out, indent=1))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
