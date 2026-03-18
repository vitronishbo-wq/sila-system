#!/bin/bash
# 🧹 SILA-System Root Directory Cleanup Script
# ============================================
#
# Purpose: Remove phantom artifacts created by VS Code extensions
# Usage:   ./scripts/cleanup.sh [--dry-run] [--auto] [--help]
#
# This script wraps cleanup_artifacts.py with shell convenience

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$SCRIPT_DIR/cleanup_artifacts.py"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
AUTO_REMOVE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --auto)
      AUTO_REMOVE=true
      shift
      ;;
    -h|--help)
      python3 "$PYTHON_SCRIPT" --help
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Change to project root
cd "$PROJECT_ROOT"

# Build command
CMD="python3 $PYTHON_SCRIPT"
[ "$DRY_RUN" = true ] && CMD="$CMD --dry-run"
[ "$AUTO_REMOVE" = true ] && CMD="$CMD --auto"

# Execute
echo -e "${BLUE}🧹 SILA-System Artifact Cleanup${NC}\n"
$CMD

exit 0
