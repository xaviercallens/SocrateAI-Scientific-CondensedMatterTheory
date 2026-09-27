#!/usr/bin/env bash
# Run a release step with tokens from a token file, logging to release/publish.log.
# Token VALUES are never printed; only whether each variable is set.
#
#   bash release/publish.sh hf        # Hugging Face upload
#   bash release/publish.sh zenodo    # Zenodo DRAFT (never publishes)
#   bash release/publish.sh check     # only check the token file
#
# TOKEN_FILE defaults to ~/.token_workflow_token.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACK="$(dirname "$HERE")"
LOG="$HERE/publish.log"
TOKEN_FILE="${TOKEN_FILE:-$HOME/.token_workflow_token}"
STEP="${1:-check}"

exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -u +%FT%TZ) step=$STEP"

if [ ! -r "$TOKEN_FILE" ]; then echo "token file not readable: $TOKEN_FILE"; exit 1; fi
if ! bash -n "$TOKEN_FILE" 2>/tmp/.tokchk.$$; then
  echo "token file has a SHELL SYNTAX ERROR (values not shown):"
  sed -E 's/(=).*/\1<hidden>/' /tmp/.tokchk.$$
  rm -f /tmp/.tokchk.$$
  echo "hint: each line should look like   export NAME=\"value\"   with both quotes closed"
  exit 1
fi
rm -f /tmp/.tokchk.$$

set -a
# shellcheck disable=SC1090
. "$TOKEN_FILE"
set +a
for v in HUGGINGFACE_TOKEN HF_TOKEN ZENODO_TOKEN; do
  val="${!v:-}"
  if [ -n "$val" ]; then echo "$v: set (value length ${#val})"; else echo "$v: not set"; fi
done
unset val

cd "$TRACK"
case "$STEP" in
  hf)     python3 release/hf_upload.py ;;
  zenodo) python3 release/zenodo_draft.py ;;
  check)  echo "check only" ;;
  *)      echo "unknown step $STEP"; exit 2 ;;
esac
rc=$?
echo "=== exit=$rc"
exit $rc
