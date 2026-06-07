#!/bin/bash

# ============================================================================
# SILA DevContainer - Post-Setup Validation
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        SILA DevContainer - Validation Check               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

passed=0
failed=0

# Test function
test_item() {
    local name=$1
    local command=$2
    
    echo -n "Testing: $name ... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((passed=passed+1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((failed=failed+1))
    fi
}

echo -e "${BLUE}[1/6] Checking Docker${NC}"
test_item "Docker available" "docker --version"

echo ""
echo -e "${BLUE}[2/6] Checking DevContainer Files${NC}"
test_item ".devcontainer/devcontainer.json" "test -f .devcontainer/devcontainer.json"
test_item ".devcontainer/docker-compose.yml" "test -f .devcontainer/docker-compose.yml"
test_item ".devcontainer/Dockerfile" "test -f .devcontainer/Dockerfile"
test_item ".devcontainer/init.sh" "test -f .devcontainer/init.sh && test -x .devcontainer/init.sh"

echo ""
echo -e "${BLUE}[3/6] Checking Configuration Files${NC}"
test_item ".env exists" "test -f .env"
test_item ".env.devcontainer exists" "test -f .env.devcontainer"
test_item ".codex-instructions.md" "test -f .codex-instructions.md"

echo ""
echo -e "${BLUE}[4/6] Checking Documentation${NC}"
test_item "README-DEVCONTAINER.md" "test -f README-DEVCONTAINER.md"
test_item "DEVCONTAINER-SETUP-SUMMARY.md" "test -f DEVCONTAINER-SETUP-SUMMARY.md"
test_item "quick-start.sh" "test -f quick-start.sh && test -x quick-start.sh"

echo ""
echo -e "${BLUE}[5/6] Checking Makefile${NC}"
test_item "Makefile extended" "grep -q 'make devcontainer-up' Makefile"
test_item "Pipeline target" "grep -q '^pipeline:' Makefile"
test_item "DB migration target" "grep -q 'db-migrate:' Makefile"
test_item "Test target" "grep -q '^test:' Makefile"
test_item "Codex agent target" "grep -q 'codex-agent:' Makefile"

echo ""
echo -e "${BLUE}[6/6] Checking Docker Compose Syntax${NC}"
test_item "docker-compose.yml valid" "docker compose -f .devcontainer/docker-compose.yml config > /dev/null"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}║          ✅ ALL CHECKS PASSED!                          ║${NC}"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}Summary: $passed passed, $failed failed${NC}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo ""
    echo "1️⃣  (Recommended) Run quick-start script:"
    echo "    bash quick-start.sh"
    echo ""
    echo "2️⃣  Or manually start:"
    echo "    make dev-setup"
    echo ""
    echo "3️⃣  Then open in VS Code:"
    echo "    F1 → Dev Containers: Reopen in Container"
    echo ""
    echo "4️⃣  Start the Codex agent:"
    echo "    make codex-agent"
    echo ""
    exit 0
else
    echo -e "${RED}║          ❌ SOME CHECKS FAILED                          ║${NC}"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${RED}Summary: $passed passed, $failed failed${NC}"
    echo ""
    echo -e "${YELLOW}Troubleshooting:${NC}"
    echo "- Check that all files were created: ls -la .devcontainer/"
    echo "- Verify Makefile changes: grep 'devcontainer-up' Makefile"
    echo "- Re-run setup: bash quick-start.sh"
    echo ""
    exit 1
fi
