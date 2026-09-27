#!/usr/bin/env python3
"""Read-only inventory of reusable research assets across this machine's projects.

For each project root it records: stack markers (Lean/Lake, Cargo, CUDA, Python,
Docker/HPC), file-type counts, MCP servers, the first lines of its README, and
hits for a fixed list of domain keywords relevant to AdS/CMT and topological
matter. Nothing is written outside the output directory; no project is modified.

Output:
    docs/assets/inventory.json   machine-readable
    (stdout)                     a compact per-project summary

Usage:
    python3 tools/inventory_assets.py [--roots DIR ...] [--max-files N]
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path

HOME = Path.home()
DEFAULT_ROOTS = [
    HOME / name
    for name in (
        "AutoevolveAI",
        "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal",
        "SocrateAI-Scientific-Agora-Home",
        "SocrateAI-Scientific-Agora-K3-DarkMatter",
        "SocrateAI-Scientific-Agora-LeanMaster",
        "SocrateAI-Scientific-DualScaleSimulator",
        "SocrateAI-Scientific-Mensura",
        "SocrateAI-Wolfram-Hypergraph",
        "runux-ai-runtime",
        "rusty-SUNDIALS",
        "rust-linux-mini-kernel",
        "SocrateAI-Lean-Lib",
    )
] + [Path("/mnt/disks/disk-socrateai-local-1/callensxavier_home_data")]

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "target", ".lake",
    ".mypy_cache", ".ruff_cache", ".pytest_cache", ".hypothesis", "build",
    "dist", ".tmp_trace_tests", ".scratchpad", "worktrees", "lake-packages",
}
TEXT_EXT = {".py", ".rs", ".lean", ".md", ".toml", ".cu", ".cuh", ".jl", ".yaml",
            ".yml", ".json", ".sh", ".tex", ".cpp", ".c", ".h"}

# Domain keywords -> label. Case-insensitive, word-ish boundaries.
KEYWORDS = {
    "topology": r"topolog",
    "chern": r"\bchern",
    "winding": r"winding",
    "berry": r"\bberry",
    # Bare "bott" matches "bottleneck"/"bottom"; bare "ssh" matches the SSH
    # protocol. Both produced false positives in the first run.
    "k_theory": r"k-theory|ktheory|k_theory|bott periodicity",
    "clifford": r"clifford",
    "ssh_model": r"su-schrieffer|ssh model|ssh chain|ssh hamiltonian",
    "tight_binding": r"tight[- ]binding|hamiltonian",
    "entanglement": r"entangle",
    "tensor_network": r"tensor.network|\bmera\b|\bdmrg\b|\bmps\b",
    "holography": r"holograph|ads/cft|ads_cft|anti-de sitter",
    "syk": r"\bsyk\b|sachdev-ye",
    "anomaly": r"anomal",
    "lattice": r"lattice",
    "persistent_homology": r"persisten|gudhi|ripser|betti",
    "gpu_cuda": r"\bcuda\b|cupy|\btriton\b|\bwgpu\b|cublas",
    "ode_dae_solver": r"sundials|\bcvode\b|runge.kutta|solve_ivp|odeint",
    "eigensolver": r"eigen|lanczos|arpack|diagonaliz",
    "hpc": r"\bslurm\b|\bmpi\b|kubernetes|cloud ?run|\bray\b",
    "mcp": r"mcpservers|fastmcp|\bmcp\b",
}
COMPILED = {k: re.compile(v, re.IGNORECASE) for k, v in KEYWORDS.items()}


def readme_head(root: Path, lines: int = 6) -> list[str]:
    for name in ("README.md", "readme.md", "README.rst", "README"):
        path = root / name
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                return []
            return [t.strip() for t in text if t.strip()][:lines]
    return []


SCI_PACKAGES = {"gudhi", "ripser", "persim", "giotto_tda", "torch", "jax", "cupy",
                "numba", "chromadb", "sympy", "scipy", "quimb", "tenpy", "qiskit"}


def python_envs(root: Path) -> dict[str, list[str]]:
    """Scientific packages installed in each virtualenv directly under root.

    Virtualenvs are hidden directories and are skipped by the tree walk, so a
    project's TDA or GPU environment would otherwise go unreported.
    """
    found: dict[str, list[str]] = {}
    try:
        candidates = [e for e in os.scandir(root) if e.is_dir() and "venv" in e.name.lower()]
    except OSError:
        return found
    for env in candidates:
        lib = Path(env.path) / "lib"
        try:
            pythons = [p for p in lib.iterdir() if p.name.startswith("python")]
        except OSError:
            continue
        for py in pythons:
            site = py / "site-packages"
            try:
                names = {n.split("-")[0].lower() for n in os.listdir(site)}
            except OSError:
                continue
            hits = sorted(names & SCI_PACKAGES)
            if hits:
                found[f"{env.name}/{py.name}"] = hits
    return found


def scan(root: Path, max_files: int) -> dict:
    ext_counts: Counter[str] = Counter()
    keyword_files: dict[str, list[str]] = {k: [] for k in KEYWORDS}
    markers: set[str] = set()
    mcp_servers: list[str] = []
    scanned = 0

    # Two budgets: text files read, and directory entries visited. The second
    # matters because binary-heavy trees (datasets, model weights, toolchains)
    # never consume the first, so without it traversal is unbounded.
    visited = 0
    max_entries = max_files * 20
    stack = [root]
    while stack and scanned < max_files and visited < max_entries:
        current = stack.pop()
        try:
            entries = list(os.scandir(current))
        except OSError:
            continue
        visited += len(entries)
        for entry in entries:
            name = entry.name
            if entry.is_dir(follow_symlinks=False):
                if name not in SKIP_DIRS and not name.startswith("."):
                    stack.append(Path(entry.path))
                elif name == ".claude":
                    stack.append(Path(entry.path))
                continue
            if not entry.is_file(follow_symlinks=False):
                continue
            ext = Path(name).suffix.lower()
            ext_counts[ext or name] += 1

            if name in ("lakefile.lean", "lakefile.toml", "lean-toolchain"):
                markers.add("lean")
            elif name == "Cargo.toml":
                markers.add("rust")
            elif ext in (".cu", ".cuh"):
                markers.add("cuda")
            elif name in ("pyproject.toml", "requirements.txt", "setup.py"):
                markers.add("python")
            elif name.startswith("Dockerfile") or name in ("docker-compose.yml", "cloudbuild.yaml"):
                markers.add("container")
            elif name == ".mcp.json":
                try:
                    data = json.loads(Path(entry.path).read_text(encoding="utf-8"))
                    mcp_servers += list(data.get("mcpServers", {}).keys())
                except (OSError, ValueError):
                    pass

            if ext not in TEXT_EXT:
                continue
            try:
                if entry.stat().st_size > 2_000_000:
                    continue
                text = Path(entry.path).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned += 1
            rel = os.path.relpath(entry.path, root)
            for key, pattern in COMPILED.items():
                if pattern.search(text) and len(keyword_files[key]) < 12:
                    keyword_files[key].append(rel)

    return {
        "root": str(root),
        "readme": readme_head(root),
        "markers": sorted(markers),
        "mcp_servers": sorted(set(mcp_servers)),
        "python_envs": python_envs(root),
        "files_scanned": scanned,
        "top_extensions": ext_counts.most_common(8),
        "keywords": {k: v for k, v in keyword_files.items() if v},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="*", type=Path)
    parser.add_argument("--max-files", type=int, default=6000)
    parser.add_argument("--out", type=Path, default=Path("docs/assets/inventory.json"))
    args = parser.parse_args()

    roots: list[Path] = args.roots or DEFAULT_ROOTS
    expanded: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        # The data disk holds project checkouts next to datasets, caches and
        # toolchains. Only git checkouts are projects; skip the rest.
        if root.name == "callensxavier_home_data":
            expanded += [
                p for p in sorted(root.iterdir())
                if p.is_dir() and (p / ".git").exists()
            ]
        else:
            expanded.append(root)

    # A checkout reachable both from ~ and from the data disk (symlink) is
    # scanned once.
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in expanded:
        real = path.resolve()
        if real not in seen:
            seen.add(real)
            unique.append(path)
    expanded = unique

    results = []
    for root in expanded:
        info = scan(root, args.max_files)
        results.append(info)
        kw = ", ".join(f"{k}:{len(v)}" for k, v in sorted(info["keywords"].items()))
        print(f"\n## {root}")
        print(f"   markers={info['markers']} mcp={info['mcp_servers']} scanned={info['files_scanned']}")
        if info["python_envs"]:
            print(f"   envs={info['python_envs']}")
        print(f"   ext={info['top_extensions'][:6]}")
        if info["readme"]:
            print(f"   readme: {' | '.join(info['readme'][:3])[:220]}")
        print(f"   keywords: {kw}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {args.out} ({len(results)} projects)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
