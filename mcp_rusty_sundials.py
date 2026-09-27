#!/usr/bin/env python3
"""MCP server for rusty-SUNDIALS (xaviercallens/rusty-SUNDIALS): a Rust port of
LLNL's SUNDIALS CVODE, useful here for stiff ODE integration (SYK/lindbladian
dynamics, disorder-averaged tight-binding time evolution -- see
docs/contribution_map.md, "Solveur Rust").

Honesty constraint, deliberate. rusty-SUNDIALS has NO MCP server of its own
(checked: its GitHub repo has no mcp_server.py or .mcp.json), and as of this
writing there is no local checkout on this machine, and this session's own
`git clone` calls are refused by its permission mode (only a `!`-prefixed
command run by the person at the keyboard succeeded, for the Elenchus repo,
earlier in this project). So this file does NOT invent a typed physics API for
a crate whose real CLI contract was never inspected -- that would be exactly
the "wind-egg" this project's own Elenchus rigor protocol exists to catch
(docs/rigor_protocol.md): a tool that looks like an integration and decides
nothing.

What this server actually does, honestly:
  - sundials_status()        : reports what preconditions are met, with no
                                side effects. Safe to call any time.
  - sundials_list_examples() : lists examples/*.rs by name, if the checkout
                                exists. Does not run anything.
  - sundials_run_example()   : runs `cargo run --release --example <name> --
                                <args>` and returns raw stdout/stderr/exit code
                                UNPARSED. It does not claim to know the output
                                format, because that was never verified here.

To make this a real integration rather than a stub:
    ! git clone --depth 1 https://github.com/xaviercallens/rusty-SUNDIALS ~/rusty-SUNDIALS
then re-open this session (RUSTY_SUNDIALS_ROOT defaults to that path).
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP  # mcp < 2
except ModuleNotFoundError:
    from mcp.server.mcpserver import MCPServer as FastMCP  # mcp >= 2: FastMCP renamed

ROOT = Path(os.environ.get("RUSTY_SUNDIALS_ROOT", str(Path.home() / "rusty-SUNDIALS")))
CLONE_CMD = (
    "! git clone --depth 1 https://github.com/xaviercallens/rusty-SUNDIALS "
    + str(ROOT)
)

mcp = FastMCP("rusty-sundials")


def _cargo_path() -> str | None:
    return shutil.which("cargo")


@mcp.tool()
def sundials_status() -> str:
    """Report whether rusty-SUNDIALS can actually be used from here: checkout
    present, Cargo.toml found, and a `cargo` toolchain on PATH. Never runs
    anything; safe to call first.
    """
    lines = [f"RUSTY_SUNDIALS_ROOT = {ROOT}"]
    checked_out = ROOT.is_dir()
    lines.append(f"checkout present   : {checked_out}")
    if not checked_out:
        lines.append(f"  -> to clone it, run in your own shell: {CLONE_CMD}")
        return "\n".join(lines)

    cargo_toml = ROOT / "Cargo.toml"
    lines.append(f"Cargo.toml found   : {cargo_toml.is_file()}")
    cargo = _cargo_path()
    lines.append(f"cargo on PATH      : {cargo or 'NOT FOUND'}")
    examples_dir = ROOT / "examples"
    lines.append(f"examples/ present  : {examples_dir.is_dir()}")
    if not cargo:
        lines.append("  -> install a Rust toolchain (e.g. via rustup) to run examples")
    return "\n".join(lines)


@mcp.tool()
def sundials_list_examples() -> str:
    """List examples/*.rs by name. Read-only; does not compile or run anything."""
    examples_dir = ROOT / "examples"
    if not ROOT.is_dir():
        return f"No checkout at {ROOT}. Run: {CLONE_CMD}"
    if not examples_dir.is_dir():
        return f"No examples/ directory found under {ROOT}."
    names = sorted(p.stem for p in examples_dir.glob("*.rs"))
    if not names:
        return "examples/ exists but contains no .rs files."
    return "\n".join(names)


@mcp.tool()
def sundials_run_example(name: str, args: str = "", timeout_s: float = 300.0) -> str:
    """Run `cargo run --release --example <name> -- <args>` and return the raw
    result, UNPARSED. This tool does not know the crate's output format or its
    examples' argument contract -- neither was inspected before writing this
    server (see module docstring) -- so it reports exactly what the process
    printed and exited with, rather than a structured, unverified guess.

    Args:
        name: an example name from sundials_list_examples(), e.g. "lorenz".
        args: extra arguments passed after `--`, as a single string.
        timeout_s: kill the process after this many seconds (default 300).
    """
    if not ROOT.is_dir():
        return f"No checkout at {ROOT}. Run: {CLONE_CMD}"
    cargo = _cargo_path()
    if not cargo:
        return "No `cargo` on PATH. Install a Rust toolchain (e.g. via rustup) first."
    if not (ROOT / "examples" / f"{name}.rs").is_file():
        return f"No such example '{name}'. Call sundials_list_examples() for the real list."

    command = [cargo, "run", "--release", "--example", name]
    if args.strip():
        command += ["--"] + args.split()

    try:
        result = subprocess.run(
            command, cwd=str(ROOT), capture_output=True, text=True, timeout=timeout_s
        )
    except subprocess.TimeoutExpired:
        return f"Timed out after {timeout_s}s running: {' '.join(command)}"
    except OSError as exc:
        return f"Failed to launch cargo: {exc}"

    return (
        f"$ {' '.join(command)}\n"
        f"exit code: {result.returncode}\n"
        f"--- stdout (raw, unparsed) ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )


if __name__ == "__main__":
    mcp.run()
