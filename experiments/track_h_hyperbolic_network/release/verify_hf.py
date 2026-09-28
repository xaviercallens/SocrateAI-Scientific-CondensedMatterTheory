#!/usr/bin/env python3
"""Anonymous (no token) check that the published HF repos are public and match the local build."""
import sys
from pathlib import Path

from huggingface_hub import HfApi

BUILD = Path(__file__).resolve().parent / "build"
NS = sys.argv[1] if len(sys.argv) > 1 else "callensxavier"


def main():
    api = HfApi(token=False)
    bad = 0
    for kind, name, folder in (("dataset", "hyperbolic-resistor-networks", BUILD / "hf_dataset"),
                               ("model", "hyperbolic-resistor-network-simulator", BUILD / "hf_model")):
        remote = set(api.list_repo_files(f"{NS}/{name}", repo_type=kind))
        local = {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file()}
        missing = sorted(local - remote)
        print(f"{kind} {NS}/{name}: {len(remote)} remote files, {len(local)} local, missing={missing}")
        bad += bool(missing)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
