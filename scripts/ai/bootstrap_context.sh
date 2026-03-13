#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

print_file() {
  local path="$1"
  echo "===== ${path} ====="
  if [[ -f "$path" ]]; then
    cat "$path"
  else
    echo "Missing: ${path}"
  fi
  echo ""
}

print_file "docs/AI_BOOTSTRAP_PROMPT.md"
print_file "docs/AI_CONTEXT.md"
print_file "docs/tree.md"
print_file "docs/architecture/domain_dependency_policy.yaml"
print_file "docs/architecture/entrypoints/SYSTEM_OVERVIEW.md"
print_file "docs/architecture/REPOSITORY_MAP.yaml"
print_file "docs/architecture/entrypoints/DOMAIN_MAP.md"
print_file "docs/architecture/entrypoints/API_ENTRYPOINTS.md"
print_file "docs/AI_DOMAIN_KERNEL.md"
print_file "docs/AI_ARCHITECTURE_GRAPH.yaml"
