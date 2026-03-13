#!/usr/bin/env bash
# Unified cleanup script for sila-system repository
# Removes obsolete files, caches, logs, backups, and node_modules

set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════════╗"
echo "║     SILA-SYSTEM CLEANUP (Cache, Logs, Backups)    ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

PHASE=${1:-all}  # all, cache, code, deps

case "$PHASE" in
  cache)
    echo "Phase: Cache cleanup only"
    ;;
  code)
    echo "Phase: Code cleanup only"
    ;;
  deps)
    echo "Phase: Dependencies cleanup only"
    ;;
  all)
    echo "Phase: Full cleanup"
    ;;
  *)
    echo "Usage: $0 [all|cache|code|deps]"
    exit 1
    ;;
esac

echo ""

# ============================================
# PHASE 1: CACHE CLEANUP
# ============================================
if [[ "$PHASE" == "all" || "$PHASE" == "cache" ]]; then
  echo "[1/3] Cleaning Python cache..."
  find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
  find . -type f -name '*.pyc' -delete 2>/dev/null || true
  find . -type f -name '*.pyo' -delete 2>/dev/null || true
  find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
  rm -f apps/backend/.coverage 2>/dev/null || true
  rm -f apps/backend/celerybeat-schedule 2>/dev/null || true
  echo "  ✓ Python cache cleaned"
fi

echo ""

# ============================================
# PHASE 2: CODE CLEANUP
# ============================================
if [[ "$PHASE" == "all" || "$PHASE" == "code" ]]; then
  echo "[2/3] Cleaning old code artifacts..."
  rm -f apps/backend/app/core/events_old.py 2>/dev/null || true
  find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name 'dist' -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name 'build' -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
  find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
  echo "  ✓ Code artifacts cleaned"
fi

echo ""

# ============================================
# PHASE 3: DEPENDENCIES CLEANUP
# ============================================
if [[ "$PHASE" == "all" || "$PHASE" == "deps" ]]; then
  echo "[3/3] Cleaning dependencies (can be restored with npm/poetry)..."
  rm -rf apps/frontend/node_modules 2>/dev/null || true
  rm -rf apps/backend/node_modules 2>/dev/null || true
  rm -f apps/backend/*.db 2>/dev/null || true
  rm -f apps/backend/*.db-wal 2>/dev/null || true
  rm -f apps/backend/*.db-shm 2>/dev/null || true
  echo "  ✓ Dependencies cleaned"
fi

echo ""
echo "✅ Cleanup complete"
echo ""
echo "Final size: $(du -sh . 2>/dev/null | cut -f1)"
