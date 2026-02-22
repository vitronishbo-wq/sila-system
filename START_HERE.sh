#!/bin/bash
# Quick Start Guide - Sync/Async Migration Runbook
# Run this from project root: bash START_HERE.sh

set -e

echo "══════════════════════════════════════════════════════════════════════"
echo "  SYNC/ASYNC ARCHITECTURE - QUICK START RUNBOOK"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Validate Architecture
echo -e "${BLUE}[STEP 1] Validating Mapper Architecture...${NC}"
echo "Running: python validate_mapper_architecture.py"
echo ""

cd /home/dev12cls/sila-system
if python validate_mapper_architecture.py 2>&1 | grep -q "VALIDATION SUCCESSFUL"; then
    echo -e "${GREEN}✓ Architecture validation PASSED${NC}"
else
    echo -e "${YELLOW}⚠ Architecture validation - check output above${NC}"
fi

echo ""
echo "──────────────────────────────────────────────────────────────────────"

# Step 2: Show documentation files
echo -e "${BLUE}[STEP 2] Documentation Files Created:${NC}"
echo ""
echo "  📄 IMPLEMENTATION_COMPLETE.md"
echo "     └─ Overview of changes and status"
echo ""
echo "  📄 ASYNC_SYNC_MIGRATION_GUIDE.md"
echo "     └─ Complete migration strategy (3 phases)"
echo ""
echo "  📄 PRACTICAL_TEST_EXAMPLES.md"
echo "     └─ Code examples and refactoring patterns"
echo ""
echo "  🔧 validate_mapper_architecture.py"
echo "     └─ Validation script (can run anytime)"
echo ""

echo "──────────────────────────────────────────────────────────────────────"

# Step 3: Quick Migration Path
echo -e "${BLUE}[STEP 3] Migration Path:${NC}"
echo ""
echo "  Phase 1: Stabilization (Week 1-2)"
echo "    ✓ Mark existing sync tests with @pytest.mark.sync_legacy"
echo "    ✓ Update .query() calls to select() pattern where needed"
echo "    ✓ Verify all tests still pass"
echo ""
echo "  Phase 2: Convert Critical Tests (Week 3-4)"
echo "    ✓ Convert test_citizen_model.py to async"
echo "    ✓ Convert test_citizen_entity.py to async"
echo "    ✓ Convert test_citizen_repository.py to async"
echo "    ✓ Mark with @pytest.mark.async_ready"
echo ""
echo "  Phase 3: Full Migration (Month 2+)"
echo "    ✓ Convert remaining tests"
echo "    ✓ Remove sync fixtures"
echo "    ✓ Full async architecture"
echo ""

echo "──────────────────────────────────────────────────────────────────────"

# Step 4: First Conversion Example
echo -e "${BLUE}[STEP 4] First Conversion (Example):${NC}"
echo ""
echo "  Run this command to see how a test would be converted:"
echo "    cat PRACTICAL_TEST_EXAMPLES.md | grep -A 30 'Migrando Teste'"
echo ""

echo "──────────────────────────────────────────────────────────────────────"

# Step 5: Running Tests
echo -e "${BLUE}[STEP 5] Running Tests:${NC}"
echo ""
echo "  Run ALL tests:"
echo "    cd /home/dev12cls/sila-system/apps/backend"
echo "    /home/dev12cls/sila-system/.venv/bin/python -m pytest tests/ -xvs"
echo ""
echo "  Run only LEGACY tests:"
echo "    /home/dev12cls/sila-system/.venv/bin/python -m pytest tests/ -m sync_legacy -xvs"
echo ""
echo "  Run only ASYNC tests:"
echo "    /home/dev12cls/sila-system/.venv/bin/python -m pytest tests/ -m async_ready -xvs"
echo ""
echo "  Run a specific test file:"
echo "    /home/dev12cls/sila-system/.venv/bin/python -m pytest tests/test_citizen_model.py -xvs"
echo ""

echo "──────────────────────────────────────────────────────────────────────"

# Step 6: Key Files
echo -e "${BLUE}[STEP 6] Key Implementation Files:${NC}"
echo ""
echo "  Core Fixture:"
echo "    apps/backend/tests/conftest.py"
echo "    └─ Contains db (sync) and db_session (async) fixtures"
echo ""
echo "  Model Definition:"
echo "    apps/backend/app/citizen/core/models.py"
echo "    └─ CitizenFUC model (fixed duplicate definition)"
echo ""
echo "  Model Registration:"
echo "    apps/backend/app/db/base.py"
echo "    └─ All models imported here to register in Base.registry"
echo ""

echo "──────────────────────────────────────────────────────────────────────"

# Step 7: Helpful Commands
echo -e "${BLUE}[STEP 7] Helpful Commands:${NC}"
echo ""
echo "  Validate anytime:"
echo "    python validate_mapper_architecture.py"
echo ""
echo "  Check Python environment:"
echo "    /home/dev12cls/sila-system/.venv/bin/python --version"
echo ""
echo "  Install dependencies:"
echo "    cd /home/dev12cls/sila-system/apps/backend"
echo "    pip install -r requirements.txt"
echo ""

echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ QUICK START COMPLETE!${NC}"
echo ""
echo "Next steps:"
echo "  1. Read IMPLEMENTATION_COMPLETE.md for overview"
echo "  2. Read ASYNC_SYNC_MIGRATION_GUIDE.md for strategy"
echo "  3. Read PRACTICAL_TEST_EXAMPLES.md for code patterns"
echo "  4. Start converting first test to async"
echo ""
echo "══════════════════════════════════════════════════════════════════════"
echo ""
