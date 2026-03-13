#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "${ROOT_DIR}"

mkdir -p reports

echo "=== replace_core_imports.sh ==="
echo "Scanning app.core imports under apps/backend/app/modules..."

mapfile -t files < <(rg -l 'app\.core' apps/backend/app/modules || true)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No app.core imports found."
  exit 0
fi

printf "%s\n" "${files[@]}" > reports/replace_core_imports_targets.txt

printf "%s\n" "${files[@]}" \
  | xargs -r -P 8 -I{} sed -i 's/\bapp\.core\b/app.platform.shared/g' "{}"

echo "Updated files: ${#files[@]}"
echo "Targets log: reports/replace_core_imports_targets.txt"
