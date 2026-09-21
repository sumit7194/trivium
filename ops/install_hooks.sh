#!/usr/bin/env bash
# Activate this repo's tracked hooks, and PROVE they can refuse before trusting them.
#
# WHY THIS FILE EXISTS.  .githooks/pre-commit is tracked and survives a clone.
# core.hooksPath -- the setting that makes git RUN it -- lives in .git/config,
# which is local and is NOT cloned.  So a fresh clone gets the hook as a file
# and not as a gate, and nothing announces the difference: the hook is in git,
# in the diff, and reviewable.  Found 2026-09-22 after ../SpaceTime reported the
# mirror-image fault on their side (a blocking-capable gate that nothing invoked).
#
#   ./ops/install_hooks.sh          activate, then run the known-fail control
#   ./ops/install_hooks.sh --check  report status only, change nothing (exit 1 if inactive)

set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

HP=$(git config core.hooksPath || true)
if [[ "${1:-}" == "--check" ]]; then
  if [[ "$HP" == ".githooks" ]]; then echo "hooks ACTIVE (core.hooksPath=$HP)"; exit 0; fi
  echo "hooks INACTIVE -- .githooks/pre-commit exists but git will not run it."
  echo "  fix: ./ops/install_hooks.sh"
  exit 1
fi

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
echo "core.hooksPath = $(git config core.hooksPath)"

# KNOWN-FAIL CONTROL.  A hook that has only ever been seen to pass has not been
# tested.  Stage a file whose mtime is now and confirm the live-checkpoint guard
# REFUSES; then confirm a clean commit is allowed.
echo
echo "-- control: does the gate refuse? --"
T=".hookctl_$$_state.npz"; : > "$T"; git add -f "$T" 2>/dev/null
if git commit -m "control: expect refusal" >/dev/null 2>&1; then
  echo "  FAIL -- commit was ALLOWED. The gate cannot refuse; do not trust it."
  git reset --soft HEAD~1 >/dev/null 2>&1
  RC=1
else
  echo "  PASS -- commit REFUSED, as it must be."
  RC=0
fi
git reset -q HEAD "$T" 2>/dev/null; rm -f "$T"
echo
echo "bypass, when you genuinely mean it:  git commit --no-verify"
exit $RC
