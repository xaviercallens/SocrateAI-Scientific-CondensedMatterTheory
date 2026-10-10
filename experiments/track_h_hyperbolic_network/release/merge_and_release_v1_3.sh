#!/usr/bin/env bash
# Merge PR #3 (merge commit, keeps every commit) and create the GitHub release v1.3 with the four new record PDFs attached.
# RUN THIS IN YOUR OWN TERMINAL with your own gh login (gh auth login) or GH_TOKEN. The assisting model does not merge.
# It refuses to continue if anything looks off, never uses --admin, and is safe to re-run: steps already done are skipped.
# Log: release/merge_release.log
#
#   bash experiments/track_h_hyperbolic_network/release/merge_and_release_v1_3.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"
REL=experiments/track_h_hyperbolic_network/release
PAPER=experiments/track_h_hyperbolic_network/paper
exec > >(tee -a "$ROOT/$REL/merge_release.log") 2>&1
PR=3
TAG=v1.3
TITLE="v1.3: four new Zenodo records (strip rate, topological proxy, column-residual certificate, programme manifesto), topology programme, Lean 4, protocols"

step() { echo; echo "== $*"; }
fail() { echo "STOP: $*"; exit 1; }

echo "=== $(date -u +%FT%TZ) merge_and_release_v1_3"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated (run: gh auth login, or export GH_TOKEN=...)"
state="$(gh pr view "$PR" --json state -q .state)" || fail "cannot read PR #$PR"

if [ "$state" = "OPEN" ]; then
  step "PR #$PR is open: compare its head with this checkout"
  remote_head="$(gh pr view "$PR" --json headRefOid -q .headRefOid)"
  local_head="$(git rev-parse HEAD)"
  echo "PR head ${remote_head:0:7}, local HEAD ${local_head:0:7}"
  [ "$remote_head" = "$local_head" ] || fail "they differ: push or pull first, so the merge contains what you expect"
  step "merge (merge commit)"
  gh pr merge "$PR" --merge || fail "merge refused; read the message above (this script does not use --admin)"
  for _ in 1 2 3 4 5 6; do
    [ "$(gh pr view "$PR" --json state -q .state)" = "MERGED" ] && break
    sleep 5
  done
fi
[ "$(gh pr view "$PR" --json state -q .state)" = "MERGED" ] || fail "PR #$PR is not merged, so no release is created"

if gh release view "$TAG" >/dev/null 2>&1; then
  echo "release $TAG already exists; not recreating it"
else
  step "create release $TAG on main"
  gh release create "$TAG" --target main --title "$TITLE" --notes-file "$REL/RELEASE_NOTES_v1.3.md" \
    "$PAPER/manifesto.pdf#Programme manifesto (PDF, DOI 10.5281/zenodo.23283365)" \
    "$PAPER/paper3.pdf#Column-residual certificate (PDF, DOI 10.5281/zenodo.23248393)" \
    "$PAPER/paper2.pdf#Topological proxy and integrator check (PDF, DOI 10.5281/zenodo.23244556)" \
    "$PAPER/note_cylinder.pdf#Strip rates and transient data (PDF, DOI 10.5281/zenodo.23241463)" \
    "experiments/track_h_hyperbolic_network/protocols/protocol_garage.pdf#Garage protocol H4 (PDF)" \
    "experiments/track_h_hyperbolic_network/protocols/protocol_computational.pdf#Computational, formal and publication protocol (PDF)" || fail "release creation failed"
fi

step "verify"
gh pr view "$PR" --json state,mergedAt,mergeCommit -q '"PR #'"$PR"': \(.state) at \(.mergedAt), merge commit \(.mergeCommit.oid[0:7])"'
gh release view "$TAG" --json tagName,targetCommitish,url,assets \
  -q '"release \(.tagName) -> \(.targetCommitish); assets: \([.assets[].name] | join(", ")); \(.url)"'
echo "done"
