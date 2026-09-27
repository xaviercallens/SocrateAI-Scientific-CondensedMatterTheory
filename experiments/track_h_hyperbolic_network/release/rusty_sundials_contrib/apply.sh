#!/usr/bin/env bash
# Install the rusty-SUNDIALS Python binding and open a PR adding the RC-network
# benchmark. Uses a separate git worktree, so your current rusty-SUNDIALS
# checkout and its uncommitted changes are not touched. Does NOT merge.
#
#   bash apply.sh            (from anywhere)
set -euo pipefail

RS="${RS:-$HOME/rusty-SUNDIALS}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANCH="feat/python-rc-network-benchmark"
WT="$RS/../rusty-SUNDIALS-rc-benchmark"

echo "== 1/4 build and install the Python binding from the base branch"
cd "$RS"
git fetch -q origin
BASE="$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)"
if [ ! -d "$WT" ]; then
  git worktree add -q -b "$BRANCH" "$WT" "origin/$BASE"
fi
cd "$WT/crates/rusty-sundials-py"
maturin build --release
# maturin names the wheel after the package: rusty_sundials_py-<ver>-...whl.
# (find, not ls: with pipefail a missing candidate directory must not abort the script)
WHL="$(find "$WT/target/wheels" "$WT/crates/rusty-sundials-py/target/wheels" -maxdepth 1 \
        -name 'rusty_sundials_py-*.whl' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2- || true)"
if [ -z "$WHL" ]; then echo "no wheel found under $WT/target/wheels" >&2; exit 1; fi
echo "installing $WHL"
python3 -m pip install --user --force-reinstall "$WHL"
python3 -c "import rusty_sundials; print('rusty_sundials importable:', rusty_sundials.__file__)"

echo "== 2/4 add the benchmark"
cd "$WT"
mkdir -p examples/python
cp -r "$SRC/examples/python/rc_network" examples/python/

echo "== 3/4 run it against the installed binding (the PR is opened only if it passes)"
PYTHONDONTWRITEBYTECODE=1 python3 examples/python/rc_network/rc_network_benchmark.py

echo "== 4/4 commit, push, open PR (not merged)"
git add examples/python/rc_network
git commit -q -m "examples(python): RC-network benchmark with analytic K1/K2 controls

Stiff linear ODE dV/dt = -(L_ii V + L_ib V_b) on resistor networks
(hyperbolic {7,3} and square-lattice fixtures), checked against the
matrix-exponential solution (K1, 1e-5) and the Dirichlet-to-Neumann
Schur complement (K2, 1e-6). Source: SocrateAI-Scientific-CondensedMatterTheory,
experiments/track_h_hyperbolic_network."
git push -q -u origin "$BRANCH"
gh pr create --base "$BASE" --head "$BRANCH" \
  --title "examples(python): RC-network benchmark with analytic controls" \
  --body "Adds \`examples/python/rc_network/\`: a stiff linear RC-network benchmark for \`CvodeSolver\` (BDF) with two analytic controls, K1 (matrix exponential, 1e-5) and K2 (steady state = Dirichlet-to-Neumann Schur complement, 1e-6), on a hyperbolic {7,3} network (N=112, stiffness ~15) and a square-lattice disk (N=113, stiffness ~35). Includes a pytest wrapper. Motivation and results: Track H study in SocrateAI-Scientific-CondensedMatterTheory (\`experiments/track_h_hyperbolic_network\`). Follow-up worth considering: an analytic Jacobian argument in the binding.

Test plan: \`python3 examples/python/rc_network/rc_network_benchmark.py\` passes against a wheel built from this branch's base."
echo "PR opened. Merge when ready:  gh pr merge --squash $BRANCH  (run inside $RS)"
