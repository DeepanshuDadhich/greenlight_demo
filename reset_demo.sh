#!/usr/bin/env bash
# Resets this repo to the vulnerable snapshot between Greenlight rehearsals.
# Destructive: force pushes main, deletes greenlight/* branches, closes open PRs.
set -euo pipefail

cd "$(dirname "$0")"

TAG="vulnerable_snapshot"
BRANCH_PREFIX="greenlight/"

for cmd in git gh npm node; do
  command -v "$cmd" >/dev/null || { echo "error: $cmd is required" >&2; exit 1; }
done

if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: working tree has uncommitted changes, commit or stash them first" >&2
  exit 1
fi

if [[ "${1:-}" != "--yes" ]]; then
  read -r -p "This force pushes main and closes all open PRs. Continue? [y/N] " answer
  [[ "$answer" == "y" || "$answer" == "Y" ]] || { echo "aborted"; exit 1; }
fi

echo "==> Fetching origin"
git fetch origin --prune --tags --force

git rev-parse -q --verify "refs/tags/$TAG" >/dev/null || { echo "error: tag $TAG not found" >&2; exit 1; }

echo "==> a. Restoring code from $TAG"
git checkout -q -B main "$TAG"

PKG_NAME="$(node -p "require('./package.json').name")"

echo "==> b. Looking up latest published version of $PKG_NAME"
if npm_out="$(npm view "$PKG_NAME" version 2>&1)"; then
  VERSION="$npm_out"
elif grep -q "E404" <<<"$npm_out"; then
  VERSION="0.1.0"
  echo "    not published yet, keeping $VERSION"
else
  echo "error: npm view failed:" >&2
  echo "$npm_out" >&2
  exit 1
fi
npm version "$VERSION" --no-git-tag-version --allow-same-version >/dev/null
echo "    version set to $VERSION"

echo "==> c. Committing"
git add package.json package-lock.json
# --allow-empty so the pushed head always carries [skip ci], even when the version is unchanged.
git commit -q --allow-empty -m "chore: reset demo to vulnerable snapshot (v$VERSION) [skip ci]"

echo "==> d. Force pushing main"
git push --force origin main

echo "==> e. Deleting remote branches starting with $BRANCH_PREFIX"
remote_branches="$(git ls-remote --heads origin "${BRANCH_PREFIX}*" | awk '{print $2}' | sed 's#^refs/heads/##')"
if [[ -n "$remote_branches" ]]; then
  while IFS= read -r branch; do
    echo "    deleting $branch"
    git push -q origin --delete "$branch"
  done <<<"$remote_branches"
else
  echo "    none"
fi

echo "==> f. Closing open PRs"
open_prs="$(gh pr list --state open --json number --jq '.[].number')"
if [[ -n "$open_prs" ]]; then
  while IFS= read -r pr; do
    echo "    closing #$pr"
    gh pr close "$pr" --comment "Closed by reset_demo.sh between rehearsals."
  done <<<"$open_prs"
else
  echo "    none"
fi

git fetch -q origin --prune
echo "==> Done. main is back at $TAG with version $VERSION."
