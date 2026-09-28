#!/usr/bin/env python3
"""Ledger entry for PREREGISTRATION_11 (conditioning across tilings). Idempotent.
Text is built by concatenation (no .format / f-strings) because it contains literal braces."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "elenchus" / "ledger.json"
DATA = Path(__file__).resolve().parent / "data"


def score():
    d = json.loads((DATA / "tilings_kappa.json").read_text())
    assert all(c["control_pass"] for c in d["controls"])
    rows = [r for r in d["rows"] if r["log10_kappa"] is not None]
    assert all(r["interior_degree_q"] for r in d["rows"])
    fam = {}
    for r in rows:
        fam.setdefault((r["p"], r["q"]), []).append(r)
    for v in fam.values():
        v.sort(key=lambda r: r["L"])
    k = lambda p, q, L: next(r["log10_kappa"] for r in fam[(p, q)] if r["L"] == L)
    inc = lambda p, q: [k(p, q, L + 1) - k(p, q, L) for L in (1, 2, 3)]
    P1 = all(all(x > y for x, y in zip(inc(p, q), inc(p, q)[1:])) for p, q in ((7, 3), (8, 3)))
    P2 = all(k(8, 3, L) < k(7, 3, L) for L in (2, 3, 4))
    spreads = {}
    for dm in (1, 2, 3, 5):
        vals = [r["log10_kappa"] for r in rows if r["d_max"] == dm]
        tilings = {(r["p"], r["q"]) for r in rows if r["d_max"] == dm}
        if len(tilings) >= 2:
            spreads[dm] = max(vals) - min(vals)
    P3a = all(s <= 1.0 for s in spreads.values())
    h0 = {r["name"]: r for r in json.loads((DATA / "h0.json").read_text())}
    flat5 = {n: h0[n]["log10_kappa"] for n in ("square R=6", "triangular R=6.449999999999999")}
    hyp5 = max(r["log10_kappa"] for r in rows if r["d_max"] == 5)
    P3b = all(v - hyp5 >= 1.0 for v in flat5.values())
    expo = {}
    for (p, q), v in fam.items():
        a, b = v[-2], v[-1]
        expo[(p, q)] = (b["log10_kappa"] - a["log10_kappa"]) / (math.log10(b["N"]) - math.log10(a["N"]))
    P4 = expo[(8, 3)] <= 1.5 and all(expo[t] <= 1.0 for t in ((5, 4), (6, 4), (4, 5)))
    return d, dict(P1=P1, P2=P2, P3a=P3a, P3b=P3b, P4=P4), spreads, expo, inc, hyp5, flat5


def main():
    d, P, spreads, expo, inc, hyp5, flat5 = score()
    raw = (DATA / "tilings_kappa.json").read_bytes()
    e = lambda t: "%.2f" % expo[t]
    statement = (
        "PREREGISTRATION_11 (log10 kappa of the DtN sensitivity Jacobian across (p,q) tilings via the closed-form Gram "
        "matrix in float64; gates passed: interior degree q in every tiling; controls v1.0 direct SVD {7,3} L=3 (diff 3e-12) and "
        "square R=6 (diff 1.1e-6, tolerance 3.1e-5 after Deviation 1). P1 HELD (" + str(P["P1"]) + "): log kappa is concave in L for "
        "{7,3} (increments " + ", ".join("%.2f" % x for x in inc(7, 3)) + ") and {8,3} (" + ", ".join("%.2f" % x for x in inc(8, 3)) + "). "
        "P2 HELD (" + str(P["P2"]) + "): {8,3} is better conditioned than {7,3} at L = 2, 3, 4 (2.31 < 2.46, 3.06 < 3.27, 3.69 < 3.89). "
        "P3a HELD (" + str(P["P3a"]) + "): at equal d_max the hyperbolic tilings agree within " + ", ".join(
            "%.2f (d_max=%d)" % (v, k) for k, v in spreads.items()) + " decades, while N varies by up to ~15x at fixed d_max. "
        "P3b HELD (" + str(P["P3b"]) + "): at d_max = 5 square R=6 (%.2f) and triangular R=6.45 (%.2f) exceed the hyperbolic maximum "
        "(%.2f) by >= 1.8 decades. P4 REFUTED (" % (flat5["square R=6"], flat5["triangular R=6.449999999999999"], hyp5) + str(P["P4"]) + "): local exponents "
        "d log kappa / d log N between the two largest sizes are {8,3} " + e((8, 3)) + " (<= 1.5 ok), {6,4} " + e((6, 4)) + " (<= 1.0 ok), "
        "{5,4} " + e((5, 4)) + " (> 1.0) and {4,5} " + e((4, 5)) + " (> 1.0); they decrease with size but stay above 1 in the tested range. "
        "Reading: within the hyperbolic class log kappa is nearly a function of d_max alone and concave in it; across classes it is not "
        "(the flat lattice is linear in d_max and much worse at equal depth), so 'the mechanism is the scaling of depth with size' "
        "(paper v1.1, sec. 3.1) holds only within the hyperbolic class.")
    c = {"id": "H0-X-0008", "tier": "X", "kind": "numeric", "depends_on": ["H0-X-0002"],
         "evidence": "sha256:" + hashlib.sha256(raw).hexdigest(), "audit": None, "statement": statement,
         "notes": ("experiments/track_h_hyperbolic_network/tilings_kappa.py. Unit conductances, full boundary only. Values carry a "
                   "float64 error bound eps*kappa(G) (<= 4e-9 in log10 kappa for every hyperbolic tiling). Five tilings, <= 6 layers, "
                   "N <= 2888; the (5,4), (6,4), (4,5) tilings reach d_max <= 4, so equal-d_max comparisons are limited to d_max <= 3 "
                   "outside {7,3}/{8,3}. The published paper (v1.1) is unchanged; its mechanism sentence needs the qualification above "
                   "in a v1.2. Deviation 1 (control tolerance) recorded in PREREGISTRATION_11.md before any tiling result was seen.")}
    led = json.loads(LEDGER.read_text())
    if c["id"] not in {x["id"] for x in led["claims"]}:
        led["claims"].append(c)
        print("added", c["id"], P, {k: round(v, 2) for k, v in spreads.items()}, {t: round(v, 2) for t, v in expo.items()})
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
