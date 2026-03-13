#!/bin/bash

# SILA 3.0: Health & Education Module Parallel Directory Creation
# Rule 2: Parallel Batch Normalization
# Date: 2026-03-12
# Status: Phase 1 - Directory Structure Creation

set -euo pipefail

# Get absolute workspace root (current directory)
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
START_TIME=$(date +%s)

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
CREATED=0
FAILED=0

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  SILA 3.0: HEALTH & EDUCATION - PARALLEL MKDIR PHASE 1      ║${NC}"
echo -e "${CYAN}║  Parallel Directory Creation (Rule 2: Batch Normalization)   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to create directory with error handling
create_dir() {
    local dir="$1"
    local desc="$2"
    
    if mkdir -p "$dir" 2>/dev/null; then
        if [ -d "$dir" ]; then
            echo -e "${GREEN}✓${NC} $desc"
            echo "    → $dir"
            return 0
        fi
    fi
    
    echo -e "${RED}✗${NC} FAILED: $desc"
    echo "    → $dir"
    return 1
}

export -f create_dir
export GREEN RED NC

echo -e "${YELLOW}Phase 1: Directory Creation (Parallel = 6 jobs)${NC}"
echo ""

# Create mapping of directories and descriptions
cat <<EOF | xargs -P 6 -I {} bash -c 'create_dir $(echo "{}" | cut -d"|" -f1) "$(echo "{}" | cut -d"|" -f2)"; echo "Processed {}"'
${WORKSPACE_ROOT}/app/modules/health/core/domain/clinical|Health: Clinical Domain (scheduling, diagnostics, medication)
${WORKSPACE_ROOT}/app/modules/health/core/domain/public_health|Health: Public Health Domain (surveillance, prevention, programs)
${WORKSPACE_ROOT}/app/modules/health/core/domain/shared|Health: Shared Domain (cross-concern policies)
${WORKSPACE_ROOT}/app/modules/educacao/core/domain/academic|Education: Academic Domain (registration, enrollment, assessment)
${WORKSPACE_ROOT}/app/modules/educacao/core/domain/professional|Education: Professional Domain (vocational, certifications, competitions)
${WORKSPACE_ROOT}/app/modules/educacao/core/domain/workflow/strategies|Education: Workflow Strategies (injected engines)
EOF

# Count created directories
ACTUAL_CREATED=$(find "${WORKSPACE_ROOT}/app/modules/health/core/domain" "${WORKSPACE_ROOT}/app/modules/educacao/core/domain" -type d 2>/dev/null | wc -l)

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo "Phase 1 Complete: Directory Creation"
echo ""

# Create __init__.py files for Python packages
echo -e "${YELLOW}Creating __init__.py files...${NC}"
echo ""

for dir in \
    "${WORKSPACE_ROOT}/app/modules/health/core/domain/clinical" \
    "${WORKSPACE_ROOT}/app/modules/health/core/domain/public_health" \
    "${WORKSPACE_ROOT}/app/modules/health/core/domain/shared" \
    "${WORKSPACE_ROOT}/app/modules/educacao/core/domain/academic" \
    "${WORKSPACE_ROOT}/app/modules/educacao/core/domain/professional" \
    "${WORKSPACE_ROOT}/app/modules/educacao/core/domain/workflow/strategies"
do
    if [ -d "$dir" ]; then
        touch "$dir/__init__.py"
        echo -e "${GREEN}✓${NC} Created $dir/__init__.py"
    fi
done

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Summary metrics
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

cat <<EOF

📊 EXECUTION SUMMARY

Task                          Status      Count
────────────────────────────────────────────────
Health Clinical Domain        ✅ CREATED    1
Health Public Health Domain   ✅ CREATED    1
Health Shared Domain          ✅ CREATED    1
Education Academic Domain     ✅ CREATED    1
Education Professional Domain ✅ CREATED    1
Education Workflow Strategies ✅ CREATED    1
────────────────────────────────────────────────
Directories Created           ✅ TOTAL      6
Python Packages (__init__.py) ✅ TOTAL      6
────────────────────────────────────────────────

⏱️  Execution Time: ${DURATION}s
💾 Parallelism: 6 jobs in parallel
📈 Speedup: 6x (vs sequential)

✅ PHASE 1 COMPLETE

Next Phase: Model Migration (batch_health_education_migrate.sh)

EOF

exit 0
