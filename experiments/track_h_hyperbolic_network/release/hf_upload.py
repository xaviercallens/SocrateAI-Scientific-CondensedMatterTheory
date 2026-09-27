#!/usr/bin/env python3
"""Upload release/build/hf_dataset and release/build/hf_model to Hugging Face.

Run after `hf auth login` and `python3 release/export.py`:

  python3 release/hf_upload.py --namespace <your-hf-username> [--private]

Creates (if absent) <namespace>/hyperbolic-resistor-networks (dataset) and
<namespace>/hyperbolic-resistor-network-simulator (model repo, code only).
Prints the URLs. Re-running uploads a new commit; nothing is deleted.
"""
import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi

BUILD = Path(__file__).resolve().parent / "build"
DATASET_NAME = "hyperbolic-resistor-networks"
MODEL_NAME = "hyperbolic-resistor-network-simulator"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--namespace", help="Hugging Face user or organisation (default: the authenticated user)")
    ap.add_argument("--private", action="store_true", help="create the repositories as private")
    a = ap.parse_args()
    manifest = (BUILD / "MANIFEST.json")
    if not manifest.exists():
        raise SystemExit("run release/export.py first")
    # token: HUGGINGFACE_TOKEN or HF_TOKEN from the environment, else the `hf auth login` cache
    token = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN") or None
    api = HfApi(token=token)
    user = api.whoami()["name"]
    print("authenticated as:", user)
    ns = a.namespace or user
    for kind, name, folder in (("dataset", DATASET_NAME, BUILD / "hf_dataset"),
                               ("model", MODEL_NAME, BUILD / "hf_model")):
        repo_id = f"{ns}/{name}"
        api.create_repo(repo_id, repo_type=kind, private=a.private, exist_ok=True)
        api.upload_folder(repo_id=repo_id, repo_type=kind, folder_path=str(folder),
                          commit_message="Release v1.0: data/code for the hyperbolic conditioning preprint")
        prefix = "datasets/" if kind == "dataset" else ""
        print(f"{kind}: https://huggingface.co/{prefix}{repo_id}")


if __name__ == "__main__":
    main()
