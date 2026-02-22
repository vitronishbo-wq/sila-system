#!/usr/bin/env bash
set -euo pipefail

MODULES="apps/backend/modules"
BACKUP_DIR=".backup_modules_$(date +%Y%m%d_%H%M%S)"
BRANCH="safefix/$(date +%Y%m%d_%H%M%S)"

echo "Creating backup to $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp -r "$MODULES" "$BACKUP_DIR/"

echo "Creating git branch $BRANCH"
git checkout -b "$BRANCH"

echo "Running isort (black profile)"
.venv/bin/isort "$MODULES" --profile black || isort "$MODULES" --profile black

echo "Running black"
.venv/bin/black "$MODULES" || black "$MODULES" || true

# Autoflake: remove unused imports and variables (be careful!)
if command -v .venv/bin/autoflake >/dev/null 2>&1; then
  AF=.venv/bin/autoflake
elif command -v autoflake >/dev/null 2>&1; then
  AF=autoflake
else
  AF=""
fi

if [ -n "$AF" ]; then
  echo "Running autoflake to remove unused imports (safe mode: --remove-all-unused-imports --ignore-init-module-imports)"
  # we process file-by-file, create .orig backups for safety
  find "$MODULES" -name "*.py" | while read -r f; do
    cp "$f" "$f.orig_autoflake" || true
    "$AF" --remove-all-unused-imports --ignore-init-module-imports --in-place "$f" || true
  done
else
  echo "autoflake not found: skipping automatic removal of unused imports"
fi

echo "Fixing end-of-file newlines (POSIX)"
find "$MODULES" -name "*.py" -exec sed -i -e '$a\' {} \;

echo "Running pre-commit (if available)"
if command -v pre-commit >/dev/null 2>&1; then
  pre-commit run --all-files || true
else
  echo "pre-commit not installed; skipping"
fi

echo "Staging changes and creating commit"
git add -A "$MODULES"
git commit -m "safefix: formatting + autoflake cleanup (automated, reversible)" || echo "nothing to commit"

PATCH_FILE="patches/safefix_$(date +%Y%m%d_%H%M%S).patch"
mkdir -p patches
git format-patch -1 --stdout > "$PATCH_FILE" || echo "no patch created"
echo "Patch available at $PATCH_FILE"

echo "Safe fixes applied. Backup at $BACKUP_DIR. Branch: $BRANCH"
echo "Review changes, run tests and run migrations generation as necessary."
