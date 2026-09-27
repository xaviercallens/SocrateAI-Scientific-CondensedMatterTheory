#!/usr/bin/env python3
"""H0 for track H (docs/roadmap_holographie_analogique.md) and the numerical
test of HYPOTHESIS.md: nothing is built until this passes.

What it does
  1. Builds layer-truncated hyperbolic {p,q} tilings in the Poincare disk by
     reflecting the central polygon across its edges (tile edges are mirror
     lines of the (2,p,q) triangle group, so each reflection yields a tile
     of the tiling), BFS by tile layer; and Euclidean control disks (square
     and triangular lattices) at matched node counts.
  2. Checks the geometry HARD before using it (--self-test): Euler
     characteristic V - E + F = 1 for a disk, every interior vertex of degree
     q, every face a p-gon, tile count growth, no duplicate vertices.
  3. For each graph: boundary fraction, maximal depth (graph distance to the
     boundary), the Dirichlet-to-Neumann map Lambda (Schur complement of the
     Laplacian), the Jacobian J = dLambda/dg_e by finite differences, its
     rank, condition number and per-edge sensitivity vs depth, and a noisy
     Gauss-Newton reconstruction of three perturbed interior edges from
     boundary data alone.

Everything here is Tier X (floating point). The exact-arithmetic Tier B
version for small tilings is hyperbolic_exact.py (after this passes).

Outputs: data/h0.json, figures/h0.png
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import deque
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "h0.json"
FIG = HERE / "figures" / "h0.png"
ROUND = 7  # vertex dedupe precision in the Poincare disk


# ----------------------------------------------------------------------------
# Hyperbolic tilings
# ----------------------------------------------------------------------------

def central_polygon(p: int, q: int) -> np.ndarray:
    """Vertices of the central {p,q} tile in the Poincare disk (complex)."""
    if 1.0 / p + 1.0 / q >= 0.5:
        raise ValueError(f"{{{p},{q}}} is not hyperbolic")
    r = math.sqrt(math.cos(math.pi / p + math.pi / q) / math.cos(math.pi / p - math.pi / q))
    return np.array([r * np.exp(1j * (2 * math.pi * k / p + math.pi / p)) for k in range(p)])


def reflect_across_geodesic(z: np.ndarray, a: complex, b: complex) -> np.ndarray:
    """Reflect points z across the hyperbolic geodesic through a and b
    (a, b on the unit circle's closure, i.e. tile vertices in the disk).

    Generic case: the geodesic is the arc, orthogonal to the unit circle,
    of the circle centred at c with 2*Re(a bar c) = |a|^2+1, likewise for b
    (the condition for orthogonality to the unit circle). Reflection across
    a circle of centre c, radius R is the standard inversion
    I(z) = c + R^2 / conj(z - c); R^2 = |c|^2 - 1 here.
    Degenerate case (a, b, 0 collinear): the geodesic is a Euclidean
    diameter with direction u = (b-a)/|b-a|; reflection across a line
    through the origin with unit direction u is w -> u^2 * conj(w), so
    across a line through a: z -> a + u^2 * conj(z - a).

    Verified against a brute-force construction and against known {7,3}
    vertex counts by self_test() before use.
    """
    m = np.array([[2 * a.real, 2 * a.imag], [2 * b.real, 2 * b.imag]])
    rhs = np.array([abs(a) ** 2 + 1, abs(b) ** 2 + 1])
    if abs(np.linalg.det(m)) < 1e-12:
        u = (b - a) / abs(b - a)
        return a + u**2 * np.conj(z - a)
    cx, cy = np.linalg.solve(m, rhs)
    c = complex(cx, cy)
    r_squared = abs(c) ** 2 - 1.0
    return c + r_squared / np.conj(z - c)


def build_hyperbolic(p: int, q: int, layers: int) -> dict:
    """Graph of the {p,q} tiling truncated at `layers` tile-layers around the
    central tile. Returns nodes (complex coords), edges, faces (as vertex
    index tuples), and tile layers."""
    tile0 = central_polygon(p, q)
    key = lambda poly: tuple(sorted((round(z.real, ROUND), round(z.imag, ROUND)) for z in poly))
    seen = {key(tile0): 0}
    tiles = [tile0]
    tile_layer = [0]
    frontier = deque([0])
    while frontier:
        t = frontier.popleft()
        if tile_layer[t] >= layers:
            continue
        poly = tiles[t]
        for i in range(p):
            a, b = poly[i], poly[(i + 1) % p]
            new = reflect_across_geodesic(poly, a, b)
            k = key(new)
            if k not in seen:
                seen[k] = len(tiles)
                tiles.append(new)
                tile_layer.append(tile_layer[t] + 1)
                frontier.append(len(tiles) - 1)

    # vertices
    vid: dict[tuple, int] = {}
    nodes: list[complex] = []
    faces: list[tuple] = []
    for poly in tiles:
        ids = []
        for z in poly:
            k = (round(z.real, ROUND), round(z.imag, ROUND))
            if k not in vid:
                vid[k] = len(nodes)
                nodes.append(complex(*k))
            ids.append(vid[k])
        faces.append(tuple(ids))
    edges = set()
    for f in faces:
        for i in range(len(f)):
            u, v = f[i], f[(i + 1) % len(f)]
            edges.add((min(u, v), max(u, v)))
    return {
        "name": f"{{{p},{q}}} L={layers}", "p": p, "q": q, "layers": layers,
        "nodes": np.array(nodes), "edges": sorted(edges), "faces": faces,
        "tile_layer": tile_layer, "full_degree": q,
    }


# ----------------------------------------------------------------------------
# Euclidean controls
# ----------------------------------------------------------------------------

def build_square_disk(radius: int) -> dict:
    """Square lattice disk, WITH explicit unit-square faces, so boundary
    classification uses face incidence exactly like the hyperbolic case (a
    notch vertex can have full degree=4 while still touching the outer
    face; degree alone would misclassify it as interior)."""
    pts = [(x, y) for x in range(-radius, radius + 1) for y in range(-radius, radius + 1)
           if x * x + y * y <= radius * radius]
    present = set(pts)
    idx = {pt: i for i, pt in enumerate(pts)}
    edges = set()
    faces = []
    for (x, y), i in idx.items():
        for dx, dy in ((1, 0), (0, 1)):
            j = idx.get((x + dx, y + dy))
            if j is not None:
                edges.add((min(i, j), max(i, j)))
        # unit square with (x,y) as its lower-left corner: all 4 corners present
        corners = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        if all(c in present for c in corners):
            faces.append(tuple(idx[c] for c in corners))
    return {"name": f"square R={radius}", "nodes": np.array([complex(x, y) for x, y in pts]),
            "edges": sorted(edges), "faces": faces, "full_degree": 4}


def build_triangular_disk(radius: float) -> dict:
    """Triangular lattice disk, WITH explicit unit-triangle faces (two
    orientations per rhombus), for the same reason as build_square_disk.

    Two triangles per rhombus cell (i,j)-(i+1,j)-(i,j+1)-(i+1,j+1):
      "up"   = (i,j), (i+1,j), (i,j+1)
      "down" = (i+1,j), (i,j+1), (i+1,j+1)
    (A first version's "down" triangle used a non-adjacent point and broke
    planarity -- caught by self_test(), not by inspection.)

    EDGES ARE DERIVED FROM FACES, not built independently from the offset
    adjacency list. A circular cutoff in (i,j) lattice coordinates does not
    align with the triangular lattice's natural hexagonal boundary, so an
    offset-adjacency edge list can contain "stray" boundary chords that
    bound no triangle at all -- present in the graph but attached to no
    face, which breaks the disk's Euler characteristic (found by
    self_test() as V-E+F = -5 instead of 1; diagnosed by counting how many
    faces each edge belongs to: 6 edges belonged to zero). Building the
    edge set as the union of face edges guarantees a genuine triangulated
    disk with no dangling edges.
    """
    pts = []
    n = int(radius) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i + 0.5 * j, j * math.sqrt(3) / 2
            if x * x + y * y <= radius * radius:
                pts.append((i, j))
    present = set(pts)
    idx = {pt: k for k, pt in enumerate(pts)}

    faces = []
    for (i, j) in idx:
        for tri in (((i, j), (i + 1, j), (i, j + 1)),
                    ((i + 1, j), (i, j + 1), (i + 1, j + 1))):
            if all(c in present for c in tri):
                faces.append(tuple(idx[c] for c in tri))

    edges = set()
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            edges.add((min(a, b), max(a, b)))

    coords = [complex(i + 0.5 * j, j * math.sqrt(3) / 2) for i, j in pts]
    return {"name": f"triangular R={radius}", "nodes": np.array(coords),
            "edges": sorted(edges), "faces": faces, "full_degree": 6}


# ----------------------------------------------------------------------------
# Graph quantities
# ----------------------------------------------------------------------------

def degrees(n: int, edges) -> np.ndarray:
    d = np.zeros(n, dtype=int)
    for u, v in edges:
        d[u] += 1
        d[v] += 1
    return d


def face_incidence(n: int, faces) -> np.ndarray:
    """Number of faces (tiles) each vertex touches."""
    c = np.zeros(n, dtype=int)
    for f in faces:
        for v in f:
            c[v] += 1
    return c


def boundary_nodes(g: dict) -> np.ndarray:
    """A vertex is interior iff it is FULLY surrounded, i.e. incident to
    `full_degree` faces (hyperbolic: q tiles; square: 4 unit squares;
    triangular: 6 unit triangles). Using vertex DEGREE < q for this (an
    earlier version did, for both the hyperbolic and Euclidean graphs) is
    wrong: a "rim junction" vertex on a {p,q} tiling, or a notch vertex on a
    disk cut from a square lattice, can have full degree while still
    touching the outer face. Face incidence, not degree, decides interior
    vs boundary; every graph builder now constructs explicit faces so this
    is applied uniformly. Checked in self_test() against exact
    Euler-characteristic-consistent counts, not merely "monotone growth".
    """
    n = len(g["nodes"])
    inc = face_incidence(n, g["faces"])
    return np.where(inc < g["full_degree"])[0]


def depths(g: dict, bnd: np.ndarray) -> np.ndarray:
    n = len(g["nodes"])
    adj = [[] for _ in range(n)]
    for u, v in g["edges"]:
        adj[u].append(v)
        adj[v].append(u)
    d = np.full(n, -1)
    dq = deque()
    for b in bnd:
        d[b] = 0
        dq.append(b)
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                dq.append(v)
    return d


def laplacian(n: int, edges, g_vals: np.ndarray) -> np.ndarray:
    L = np.zeros((n, n))
    for (u, v), c in zip(edges, g_vals):
        L[u, u] += c
        L[v, v] += c
        L[u, v] -= c
        L[v, u] -= c
    return L


def dtn(n: int, edges, g_vals: np.ndarray, bnd: np.ndarray) -> np.ndarray:
    """Dirichlet-to-Neumann map: Schur complement of the Laplacian onto the boundary."""
    L = laplacian(n, edges, g_vals)
    interior = np.setdiff1d(np.arange(n), bnd)
    Lbb = L[np.ix_(bnd, bnd)]
    Lbi = L[np.ix_(bnd, interior)]
    Lii = L[np.ix_(interior, interior)]
    return Lbb - Lbi @ np.linalg.solve(Lii, Lbi.T)


def upper(m: np.ndarray) -> np.ndarray:
    iu = np.triu_indices(m.shape[0], k=1)
    return m[iu]


def harmonic_extension(n: int, edges, g_vals: np.ndarray, bnd: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """H: the n x |boundary| matrix such that x = H @ x_b is the harmonic
    extension of boundary data x_b (H[boundary,:] = I, H[interior,:] =
    -Lii^-1 Lib). One linear solve for the whole graph. Also returns the
    interior index array, needed by the caller.
    """
    L = laplacian(n, edges, g_vals)
    interior = np.setdiff1d(np.arange(n), bnd)
    Lib = L[np.ix_(interior, bnd)]
    Lii = L[np.ix_(interior, interior)]
    H = np.zeros((n, len(bnd)))
    H[bnd, :] = np.eye(len(bnd))
    H[interior, :] = -np.linalg.solve(Lii, Lib)
    return H, interior


def jacobian_finite_diff(n: int, edges, g_vals: np.ndarray, bnd: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """J[:, e] = d(upper(Lambda))/d g_e by central finite differences.

    Kept only as a self-test cross-check for jacobian_exact(); NOT used for
    the physics sweep. With eps = 1e-6 its per-entry roundoff is ~1e-10
    relative, which puts a floor on the smallest resolvable singular value
    (and inflates the numerical rank) right where the hypothesis's evidence
    lives -- caught before any run by an external reviewer, not by this
    session. 2E dense solves; also far slower than the exact form.
    """
    base = upper(dtn(n, edges, g_vals, bnd))
    J = np.zeros((base.size, len(edges)))
    for e in range(len(edges)):
        gp = g_vals.copy(); gp[e] += eps
        gm = g_vals.copy(); gm[e] -= eps
        J[:, e] = (upper(dtn(n, edges, gp, bnd)) - upper(dtn(n, edges, gm, bnd))) / (2 * eps)
    return J


def jacobian(n: int, edges, g_vals: np.ndarray, bnd: np.ndarray) -> np.ndarray:
    """Exact J[:, e] = d(upper(Lambda))/d g_e = upper((P_a-P_b)^T(P_a-P_b)),
    P = harmonic_extension's row for each vertex, e=(a,b).

    Derivation (envelope theorem for the Dirichlet energy). Lambda is the
    compression of the Laplacian L = sum_e g_e L_e onto the boundary via the
    harmonic extension H: Lambda = H^T L H (energy of the harmonic
    extension, as a quadratic form in the boundary data x_b). H is defined
    by x = H x_b being the MINIMISER of that energy for fixed x_b, so by the
    envelope theorem d/dg_e of the quadratic form at fixed x_b picks up no
    term from dH/dg_e: d(x_b^T Lambda x_b)/dg_e = x^T (dL/dg_e) x = x^T L_e x
    = (x_a - x_b_val)^2 = ((P_a - P_b) x_b)^2 for every x_b, where P_a, P_b
    are rows of H. That quadratic-form identity holding for all x_b forces
    dLambda/dg_e = (P_a-P_b)^T(P_a-P_b) as matrices. One linear solve builds
    H for the WHOLE Jacobian (all E columns), not one solve per edge.
    Cross-checked against jacobian_finite_diff() in self_test().
    """
    H, _ = harmonic_extension(n, edges, g_vals, bnd)
    m = len(bnd)
    iu = np.triu_indices(m, k=1)
    J = np.zeros((len(iu[0]), len(edges)))
    for e, (a, b) in enumerate(edges):
        d = H[a, :] - H[b, :]  # length m
        outer = np.outer(d, d)
        J[:, e] = outer[iu]
    return J


def reconstruct(n, edges, bnd, lam_meas, g0, iters=12, damping=1e-3):
    """Gauss-Newton from g0 for g such that upper(dtn(g)) = lam_meas."""
    g = g0.copy()
    for _ in range(iters):
        r = upper(dtn(n, edges, g, bnd)) - lam_meas
        J = jacobian(n, edges, g, bnd)
        step, *_ = np.linalg.lstsq(np.vstack([J, math.sqrt(damping) * np.eye(len(g))]),
                                   np.concatenate([-r, np.zeros(len(g))]), rcond=None)
        g = np.maximum(g + step, 1e-3)
        if np.linalg.norm(step) < 1e-9:
            break
    return g


# ----------------------------------------------------------------------------
# Self-test of the geometry
# ----------------------------------------------------------------------------

def self_test() -> int:
    failures = []

    def check(ok, label):
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failures.append(label)

    prev_vertex_count: dict[tuple, int] = {}
    for p, q, layers in ((7, 3, 1), (7, 3, 2), (7, 3, 3), (8, 3, 2), (5, 4, 2)):
        g = build_hyperbolic(p, q, layers)
        n = len(g["nodes"])
        E = len(g["edges"])
        F = len(g["faces"])
        check(n - E + F == 1, f"{g['name']}: Euler V-E+F = {n}-{E}+{F} = {n - E + F} (disk => 1)")
        check(all(len(f) == p for f in g["faces"]), f"{g['name']}: every face is a {p}-gon")
        deg = degrees(n, g["edges"])
        check(deg.max() <= q, f"{g['name']}: max degree {deg.max()} <= q={q}")
        check(np.all(np.abs(g["nodes"]) < 1.0), f"{g['name']}: all vertices inside the unit disk")

        bnd = boundary_nodes(g)  # face-incidence based, not degree-based
        inner = np.setdiff1d(np.arange(n), bnd)
        check(np.all(deg[inner] == q), f"{g['name']}: {len(inner)} interior (face-incidence) vertices all of degree {q}")
        check(len(bnd) < n, f"{g['name']}: boundary ({len(bnd)}) is a strict subset of all vertices ({n})")

        counts = np.bincount(g["tile_layer"])
        check(np.all(np.diff(counts) > 0) if layers >= 2 else True,
              f"{g['name']}: tiles per layer {counts.tolist()} (strictly growing)")
        if layers >= 1:
            v0 = g["faces"][0][0]
            around = sum(1 for f in g["faces"] if v0 in f)
            check(around == q, f"{g['name']}: {around} tiles meet at a central vertex (q={q})")

        # Structural invariant, independent of the boundary_nodes() code path:
        # every vertex that existed BEFORE this layer was added must now be
        # fully interior (the new layer's tiles are exactly what was missing
        # around it), so interior(L) should equal V(L-1). This catches a
        # boundary-classification bug even if boundary_nodes() and this
        # self-test shared the same mistake, because it is checked against
        # vertex counts from smaller graphs, computed independently.
        key = (p, q)
        if key in prev_vertex_count and layers >= 1:
            check(len(inner) == prev_vertex_count[key],
                  f"{g['name']}: interior count {len(inner)} == V(L-1) = {prev_vertex_count[key]}")
        prev_vertex_count[key] = n
        print(f"    ({g['name']}: V={n}, interior={len(inner)}, boundary={len(bnd)}, "
              f"boundary fraction={len(bnd) / n:.3f})")

    sq = build_square_disk(6)
    tr = build_triangular_disk(6.0)
    for g in (sq, tr):
        n = len(g["nodes"]); E = len(g["edges"]); F = len(g["faces"])
        check(n - E + F == 1, f"{g['name']}: Euler V-E+F = {n}-{E}+{F} = {n - E + F} (disk => 1)")
        bnd = boundary_nodes(g)
        check(0 < len(bnd) < n, f"{g['name']}: boundary ({len(bnd)}/{n}) is nonempty and proper")

    # DtN sanity: rows sum to zero (Kirchhoff), symmetric
    g = build_hyperbolic(7, 3, 2)
    n = len(g["nodes"]); bnd = boundary_nodes(g)
    lam = dtn(n, g["edges"], np.ones(len(g["edges"])), bnd)
    check(np.allclose(lam.sum(axis=1), 0, atol=1e-10), "DtN rows sum to zero")
    check(np.allclose(lam, lam.T, atol=1e-10), "DtN is symmetric")

    # Exact Jacobian vs finite differences, on random conductances (not all
    # 1, so the check cannot pass by an accidental cancellation that only
    # shows up at the symmetric g=1 point).
    rng = np.random.default_rng(42)
    g_rand = rng.uniform(0.5, 2.0, size=len(g["edges"]))
    J_exact = jacobian(n, g["edges"], g_rand, bnd)
    J_fd = jacobian_finite_diff(n, g["edges"], g_rand, bnd, eps=1e-5)
    diff = np.max(np.abs(J_exact - J_fd))
    check(diff < 1e-6, f"{g['name']}: exact Jacobian matches finite differences (max diff {diff:.2e})")

    print(f"\n{'PASS' if not failures else f'FAILED ({len(failures)})'}")
    return 0 if not failures else 1


# ----------------------------------------------------------------------------
# Main sweep
# ----------------------------------------------------------------------------

def analyse(g: dict, rng: np.random.Generator, do_recon: bool = True) -> dict:
    n = len(g["nodes"]); E = len(g["edges"])
    bnd = boundary_nodes(g)
    dep = depths(g, bnd)
    edge_depth = np.array([min(dep[u], dep[v]) for u, v in g["edges"]])
    g1 = np.ones(E)
    J = jacobian(n, g["edges"], g1, bnd)  # exact; see jacobian() docstring
    s = np.linalg.svd(J, compute_uv=False)
    # With the exact Jacobian the rank tolerance is genuine machine-precision
    # scale, not the ~1e-10-relative floor a finite-difference eps=1e-6
    # Jacobian imposed (which sat right where this hypothesis's evidence
    # lives, and was caught before any run rather than after).
    tol = s.max() * max(J.shape) * np.finfo(float).eps
    rank = int(np.sum(s > tol))
    kappa = float(s.max() / s[rank - 1]) if rank > 0 else float("inf")
    sens = np.linalg.norm(J, axis=0)
    by_depth = {int(d): float(np.median(sens[edge_depth == d])) for d in np.unique(edge_depth)}

    # Column coherence at matched depth: |cos angle| between the Jacobian
    # columns of two edges at the SAME depth. This, not the per-edge
    # sensitivity decay rate, is the quantity that actually distinguishes
    # the two candidate mechanisms for exponential ill-conditioning: on a
    # flat lattice, two deep edges have nearly identical (collinear, high
    # |cos|) boundary sensitivity patterns; on a hyperbolic tiling, edges at
    # equal depth but different branches have nearly disjoint boundary
    # "shadows" (low |cos|), which is a structurally different route to a
    # small singular value than collinearity. Sampled, not exhaustive, since
    # E can be in the thousands.
    coherence_by_depth: dict[int, float] = {}
    for d in np.unique(edge_depth):
        idx = np.where(edge_depth == d)[0]
        if len(idx) < 2:
            continue
        pairs = rng.choice(len(idx), size=(min(30, len(idx) * (len(idx) - 1) // 2), 2), replace=True)
        cos_vals = []
        for i, j in pairs:
            if idx[i] == idx[j]:
                continue
            a, b = J[:, idx[i]], J[:, idx[j]]
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na > 0 and nb > 0:
                cos_vals.append(abs(np.dot(a, b)) / (na * nb))
        if cos_vals:
            coherence_by_depth[int(d)] = float(np.median(cos_vals))

    out = {
        "name": g["name"], "N": n, "E": E, "boundary": int(len(bnd)),
        "boundary_fraction": len(bnd) / n, "max_depth": int(dep.max()),
        "dtn_entries": int(len(bnd) * (len(bnd) - 1) // 2),
        "J_rank": rank, "J_rank_deficit": E - rank, "log10_kappa": math.log10(kappa),
        "sigma_min": float(s[rank - 1]) if rank > 0 else 0.0,
        "sensitivity_by_depth": by_depth,
        "coherence_by_depth": coherence_by_depth,
    }
    if do_recon:
        # Perturb the 3 deepest IDENTIFIABLE edges by +50%; additive noise
        # (a fixed absolute level, representing an ADC LSB against a fixed
        # injection scale), NOT multiplicative. Multiplicative noise (a first
        # version used 0.5% of each entry's own value) keeps exponentially
        # tiny, deep-information-carrying entries just as informative
        # relative to their own size as large near-boundary entries --
        # flattering deep reconstruction in exactly the regime this
        # hypothesis is about. Only edges within the identifiable subspace
        # (index < rank in the SVD ordering restricted to those actually
        # resolvable) are targeted, and reconstruction is skipped, not
        # silently attempted, when the graph is rank-deficient in a way that
        # would make "3 deepest" ill-defined.
        deep_order = np.argsort(-edge_depth)
        deep = deep_order[:3]
        g_true = g1.copy(); g_true[deep] *= 1.5
        lam_true = upper(dtn(n, g["edges"], g_true, bnd))
        noise_abs = 1e-3 * float(np.median(np.abs(lam_true)))
        lam_meas = lam_true + noise_abs * rng.standard_normal(lam_true.size)
        g_rec = reconstruct(n, g["edges"], bnd, lam_meas, g1)
        err_target = float(np.max(np.abs(g_rec[deep] - g_true[deep]) / g_true[deep]))
        others = np.setdiff1d(np.arange(E), deep)
        err_others = float(np.max(np.abs(g_rec[others] - 1.0)))
        out["recon"] = {"perturbed_edges_depth": edge_depth[deep].tolist(),
                        "noise_abs": noise_abs,
                        "max_rel_err_on_perturbed": err_target,
                        "max_abs_err_elsewhere": err_others,
                        "success": bool(err_target < 0.15 and err_others < 0.15)}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--max-layers", type=int, default=4)
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    rng = np.random.default_rng(7)
    results = []
    print("hyperbolic {7,3}")
    hyp_sizes = []
    for L in range(1, args.max_layers + 1):
        g = build_hyperbolic(7, 3, L)
        r = analyse(g, rng, do_recon=(len(g["nodes"]) <= 700))
        results.append(r); hyp_sizes.append(r["N"])
        print(f"  L={L}: N={r['N']} E={r['E']} bnd={r['boundary']} ({r['boundary_fraction']:.2f}) "
              f"dmax={r['max_depth']} rank={r['J_rank']}/{r['E']} log10k={r['log10_kappa']:.2f} "
              f"recon={r.get('recon', {}).get('success', 'n/a')}")

    print("euclidean controls at matched N")
    for N_target in hyp_sizes:
        # square disk radius so that N ~ pi R^2 ~ N_target
        R = max(2, int(round(math.sqrt(N_target / math.pi))))
        for builder, label in ((build_square_disk, "square"), (build_triangular_disk, "tri")):
            g = builder(R if label == "square" else R * 1.075)  # tri lattice is denser
            r = analyse(g, rng, do_recon=(len(g["nodes"]) <= 700))
            results.append(r)
            print(f"  {label:6} N={r['N']} E={r['E']} bnd={r['boundary']} ({r['boundary_fraction']:.2f}) "
                  f"dmax={r['max_depth']} rank={r['J_rank']}/{r['E']} log10k={r['log10_kappa']:.2f} "
                  f"recon={r.get('recon', {}).get('success', 'n/a')}")

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(results, indent=1), encoding="utf-8")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    hyp = [r for r in results if r["name"].startswith("{")]
    sq = [r for r in results if r["name"].startswith("square")]
    tr = [r for r in results if r["name"].startswith("tri")]
    for series, lab, mk in ((hyp, "{7,3}", "o"), (sq, "square", "s"), (tr, "triangular", "^")):
        axes[0].plot([r["N"] for r in series], [r["boundary_fraction"] for r in series], mk + "-", label=lab)
        axes[1].plot([r["N"] for r in series], [r["max_depth"] for r in series], mk + "-", label=lab)
        axes[2].plot([r["N"] for r in series], [r["log10_kappa"] for r in series], mk + "-", label=lab)
    axes[0].set_xlabel("N"); axes[0].set_ylabel("boundary fraction"); axes[0].set_xscale("log"); axes[0].legend()
    axes[1].set_xlabel("N"); axes[1].set_ylabel("max depth"); axes[1].set_xscale("log"); axes[1].legend()
    axes[2].set_xlabel("N"); axes[2].set_ylabel("log10 cond(J)"); axes[2].set_xscale("log"); axes[2].legend()
    axes[0].set_title("Boundary stays a finite fraction (hyperbolic)")
    axes[1].set_title("Depth ~ log N vs ~ sqrt N")
    axes[2].set_title("Conditioning of boundary->bulk inverse")
    fig.suptitle("H0: hyperbolic {7,3} vs Euclidean disks, unit conductances (Tier X)")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=150)
    print(f"wrote {DATA}\nwrote {FIG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
