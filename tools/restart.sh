#!/usr/bin/env bash
# Quick restart: re-establish the project's state after a break or a new session.
# Read-only by default; `--rebuild` also reruns the analyses, the paper and the bundles.
#
#   bash tools/restart.sh            # status report (~1 min)
#   bash tools/restart.sh --rebuild  # + rerun Track H scripts, paper, release bundles (~10 min)
#
# Prints a STATUS table and ends with the next steps from docs/roadmap.md.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRACK="$ROOT/experiments/track_h_hyperbolic_network"
ELENCHUS_GATE="${ELENCHUS_GATE:-$HOME/SocrateAI-Scientific-Elenchus/tools/ledger.py}"
cd "$ROOT"
ok()   { printf '  \033[32mOK  \033[0m %s\n' "$*"; }
warn() { printf '  \033[33mWARN\033[0m %s\n' "$*"; }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$*"; }

echo "== repository"
echo "  branch $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD); $(git status --porcelain | wc -l) uncommitted paths"
git fetch -q origin 2>/dev/null && echo "  ahead/behind origin: $(git rev-list --left-right --count HEAD...@{u} 2>/dev/null || echo 'no upstream')"
gh pr list --state open --limit 5 2>/dev/null | sed 's/^/  PR /' || warn "gh not available"

echo "== python environment"
python3 - <<'PY'
import importlib
for m in ("numpy", "scipy", "matplotlib", "chromadb", "huggingface_hub", "pypdf", "rusty_sundials"):
    try:
        importlib.import_module(m); print(f"  OK   {m}")
    except Exception as e:
        print(f"  WARN {m}: {type(e).__name__}")
PY
command -v pdflatex >/dev/null && ok "pdflatex" || warn "pdflatex missing (paper build)"

echo "== self-tests"
python3 "$TRACK/hyperbolic_network.py" --self-test >/dev/null 2>&1 && ok "hyperbolic_network self-test" || bad "hyperbolic_network self-test"
python3 "$TRACK/hyperbolic_exact.py" --self-test >/dev/null 2>&1 && ok "hyperbolic_exact self-test" || bad "hyperbolic_exact self-test"
python3 tools/test_export_session_traces.py >/dev/null 2>&1 && ok "trace exporter self-test" || bad "trace exporter self-test"
if python3 -c "import rusty_sundials" 2>/dev/null; then
  python3 "$TRACK/release/rusty_sundials_contrib/examples/python/rc_network/rc_network_benchmark.py" >/dev/null 2>&1 \
    && ok "rusty-SUNDIALS RC benchmark (K1/K2)" || bad "rusty-SUNDIALS RC benchmark"
else
  warn "rusty_sundials not importable: bash $TRACK/release/rusty_sundials_contrib/apply.sh (or maturin build + pip install --user)"
fi

echo "== claim ledger"
if [ ! -f "$ELENCHUS_GATE" ] && [ -z "${ELENCHUS_NO_CLONE:-}" ]; then
  echo "  cloning Elenchus (gate) to $HOME/SocrateAI-Scientific-Elenchus"
  gh repo clone xaviercallens/SocrateAI-Scientific-Elenchus "$HOME/SocrateAI-Scientific-Elenchus" -- -q 2>/dev/null \
    || git clone -q https://github.com/xaviercallens/SocrateAI-Scientific-Elenchus "$HOME/SocrateAI-Scientific-Elenchus" 2>/dev/null
fi
if [ -f "$ELENCHUS_GATE" ]; then
  python3 "$ELENCHUS_GATE" docs/elenchus/ledger.json | sed 's/^/  /'
  python3 "$ELENCHUS_GATE" --evidence-dir docs/elenchus/evidence docs/elenchus/ledger.json >/dev/null 2>&1 \
    && ok "strict gate (evidence verified)" || warn "strict gate reports blocks (5 known legacy digests, roadmap H-8)"
else
  warn "Elenchus gate not found; set ELENCHUS_GATE=/path/to/SocrateAI-Scientific-Elenchus/tools/ledger.py"
fi

echo "== vector store (AutoevolveAI / ANSE Chroma)"
python3 - <<'PY'
import os
try:
    import chromadb
    c = chromadb.PersistentClient(path=os.environ.get("CHROMA_PATH", os.path.expanduser("~/AutoevolveAI/data/chroma")))
    names = [getattr(x, "name", x) for x in c.list_collections()]
    for n in ("adscmt_literature", "adscmt_generated", "phase1_traces"):
        print(f"  {'OK  ' if n in names else 'WARN'} {n}: {c.get_collection(n).count() if n in names else 'MISSING'}")
except Exception as e:
    print(f"  WARN chroma: {e}")
PY
curl -s -m 3 http://localhost:11434/api/tags >/dev/null && ok "Ollama up (embeddings)" || warn "Ollama down: ingestion will refuse to run (fail-closed)"

echo "== publications"
python3 - <<'PY'
import requests
for label, url in (("Zenodo record", "https://zenodo.org/api/records/23000391"),
                   ("DOI resolver", "https://doi.org/10.5281/zenodo.23000391"),
                   ("HF dataset", "https://huggingface.co/api/datasets/callensxavier/hyperbolic-resistor-networks"),
                   ("HF simulator", "https://huggingface.co/api/models/callensxavier/hyperbolic-resistor-network-simulator")):
    try:
        r = requests.head(url, allow_redirects=True, timeout=15)
        print(f"  {'OK  ' if r.status_code < 400 else 'WARN'} {label}: HTTP {r.status_code}")
    except Exception as e:
        print(f"  WARN {label}: {type(e).__name__}")
PY

if [ "${1:-}" = "--rebuild" ]; then
  echo "== rebuild"
  for s in probe_matched identifiability rc_network h2_explore interior_degree; do
    python3 "$TRACK/$s.py" >/dev/null 2>&1 && ok "$s.py" || bad "$s.py"
  done
  python3 "$TRACK/paper/build.py" | tail -2 | sed 's/^/  /'
  python3 "$TRACK/release/export.py" >/dev/null && python3 "$TRACK/release/check_bundle.py" | sed 's/^/  /'
  python3 tools/build_physics_verdicts.py | tail -1 | sed 's/^/  /'
  echo "  (git diff shows whether any number changed; data/*.json are evidence, re-point ledger digests if they did)"
fi

echo "== next steps (docs/roadmap.md, section 'État au 2026-09-27')"
grep -E '^\| \*\*H-[0-9]\*\*' docs/roadmap.md | cut -d'|' -f2,3 | sed 's/^/  /'
echo "  lessons: LL.md   |   memory: ~/.claude/projects/*CondensedMatterTheory*/memory/"
