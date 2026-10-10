#!/usr/bin/env bash
# Merge PR #2 (merge commit, keeps every commit) and create the GitHub release v1.2 (v1.1 PDF attached as well).
# RUN THIS IN YOUR OWN TERMINAL with your own gh login (gh auth login) or GH_TOKEN.
# It refuses to continue if anything looks off, never uses --admin, and is safe to re-run:
# steps that are already done are skipped. Log: release/merge_release.log
#
#   bash experiments/track_h_hyperbolic_network/release/merge_and_release.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"
REL=experiments/track_h_hyperbolic_network/release
exec > >(tee -a "$ROOT/$REL/merge_release.log") 2>&1
PR=2
TAG=v1.2
TITLE="v1.2: Track H preprint (mechanism of the depth dependence, defects, other tilings), data, simulator, lab protocol"

step() { echo; echo "== $*"; }
fail() { echo "STOP: $*"; exit 1; }

echo "=== $(date -u +%FT%TZ) merge_and_release"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated (run: gh auth login, or export GH_TOKEN=...)"
state="$(gh pr view "$PR" --json state -q .state)" || fail "cannot read PR #$PR"

if [ "$state" = "OPEN" ]; then
  step "PR #$PR is open: compare its head with this checkout"
  remote_head="$(gh pr view "$PR" --json headRefOid -q .headRefOid)"
  local_head="$(git rev-parse HEAD)"
  echo "PR head ${remote_head:0:7}, local HEAD ${local_head:0:7}"
  [ "$remote_head" = "$local_head" ] || fail "they differ: push or pull first, so the merge contains what you expect"
  step "refresh the PR description"
  gh pr edit "$PR" --body-file "$REL/PR2_DESCRIPTION.md" || fail "could not edit the PR description"
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
  gh release create "$TAG" --target main --title "$TITLE" --notes-file "$REL/RELEASE_NOTES_v1.2.md" \
    "experiments/track_h_hyperbolic_network/paper/main_v1_2.pdf#Preprint v1.2 (PDF, DOI 10.5281/zenodo.23228685)" \
    "experiments/track_h_hyperbolic_network/paper/main.pdf#Preprint v1.1 (PDF, DOI 10.5281/zenodo.23002378)" || fail "release creation failed"
fi

step "verify"
gh pr view "$PR" --json state,mergedAt,mergeCommit -q '"PR #'"$PR"': \(.state) at \(.mergedAt), merge commit \(.mergeCommit.oid[0:7])"'
gh release view "$TAG" --json tagName,targetCommitish,url,assets \
  -q '"release \(.tagName) -> \(.targetCommitish); assets: \([.assets[].name] | join(", ")); \(.url)"'
echo "done"
