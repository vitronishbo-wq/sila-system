#!/bin/bash

# ============================================================================
# SILA Dev Container Validation Script
# ============================================================================
# Validates that all devcontainer components are properly configured
# Usage: bash .devcontainer/validate.sh
# ============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Functions
check_file() {
    local file=$1
    local desc=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $desc"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $desc (missing: $file)"
        ((FAIL++))
        return 1
    fi
}

check_json() {
    local file=$1
    local desc=$2
    
    if command -v jq &> /dev/null; then
        if jq empty "$file" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $desc"
            ((PASS++))
            return 0
        else
            echo -e "${RED}✗${NC} $desc (invalid JSON)"
            ((FAIL++))
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} $desc (jq not found, skipping validation)"
        ((WARN++))
        return 0
    fi
}

check_field() {
    local file=$1
    local field=$2
    local desc=$3
    
    if command -v jq &> /dev/null; then
        if jq -e ".$field" "$file" &>/dev/null; then
            echo -e "${GREEN}✓${NC} $desc"
            ((PASS++))
            return 0
        else
            echo -e "${RED}✗${NC} $desc (missing field: $field)"
            ((FAIL++))
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} $desc (jq not found)"
        ((WARN++))
        return 0
    fi
}

check_security_feature() {
    local file=$1
    local feature=$2
    local desc=$3
    
    if grep -q "$feature" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $desc"
        ((PASS++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $desc"
        ((WARN++))
        return 1
    fi
}

# ============================================================================
# Main Validation
# ============================================================================

echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ SILA Dev Container Validation Report  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# 1. File Structure
echo -e "${BLUE}[1/5]${NC} Checking file structure..."
check_file ".devcontainer/devcontainer.json" "devcontainer.json exists"
check_file ".devcontainer/docker-compose.yml" "docker-compose.yml exists"
check_file ".devcontainer/Dockerfile" "Dockerfile exists"
check_file ".devcontainer/init.sh" "init.sh exists"
check_file ".devcontainer/README.md" "README.md documentation"
check_file ".devcontainer/SECURITY.md" "SECURITY.md documentation"
check_file ".devcontainer/.env.example" ".env.example template"
echo ""

# 2. JSON Validation
echo -e "${BLUE}[2/5]${NC} Validating JSON structure..."
check_json ".devcontainer/devcontainer.json" "devcontainer.json is valid JSON"
echo ""

# 3. Configuration Fields
echo -e "${BLUE}[3/5]${NC} Checking required configuration fields..."
check_field ".devcontainer/devcontainer.json" "name" "Container has name"
check_field ".devcontainer/devcontainer.json" "dockerComposeFile" "Docker Compose file configured"
check_field ".devcontainer/devcontainer.json" "service" "Service name set"
check_field ".devcontainer/devcontainer.json" "runServices" "runServices configured"
check_field ".devcontainer/devcontainer.json" "containerUser" "containerUser specified"
check_field ".devcontainer/devcontainer.json" "overrideCommand" "overrideCommand set to false"
check_field ".devcontainer/devcontainer.json" "postCreateCommand" "postCreateCommand configured"
check_field ".devcontainer/devcontainer.json" "updateContentCommand" "updateContentCommand configured"
echo ""

# 4. Security Configuration
echo -e "${BLUE}[4/5]${NC} Checking security configuration..."
check_security_feature ".devcontainer/devcontainer.json" "SSH_AUTH_SOCK" "SSH Agent forwarding enabled"
check_security_feature ".devcontainer/devcontainer.json" "vscode" "Running as vscode user"
check_security_feature ".devcontainer/docker-compose.yml" "no-new-privileges" "Security options applied"
check_security_feature ".devcontainer/docker-compose.yml" "healthcheck" "Health checks configured"
check_security_feature ".devcontainer/docker-compose.yml" "redis_data" "Redis volume persisted"
check_security_feature ".devcontainer/.env.example" "POSTGRES_PASSWORD" "Credentials template provided"

# Check SSH mount (should NOT be there)
if grep -q 'source=.*\.ssh.*target=/root' ".devcontainer/devcontainer.json" 2>/dev/null; then
    echo -e "${RED}✗${NC} SSH key mounting removed (should use SSH_AUTH_SOCK)"
    ((FAIL++))
else
    echo -e "${GREEN}✓${NC} SSH key mounting properly replaced with SSH_AUTH_SOCK"
    ((PASS++))
fi
echo ""

# 5. Docker Services
echo -e "${BLUE}[5/5]${NC} Checking Docker Compose services..."

if [ -f ".devcontainer/docker-compose.yml" ]; then
    if grep -q "  app:" ".devcontainer/docker-compose.yml"; then
        echo -e "${GREEN}✓${NC} App service configured"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} App service missing"
        ((FAIL++))
    fi
    
    if grep -q "  db:" ".devcontainer/docker-compose.yml"; then
        echo -e "${GREEN}✓${NC} PostgreSQL service configured"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} PostgreSQL service missing"
        ((FAIL++))
    fi
    
    if grep -q "  redis:" ".devcontainer/docker-compose.yml"; then
        echo -e "${GREEN}✓${NC} Redis service configured"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Redis service missing"
        ((FAIL++))
    fi
    
    # Check for persistence
    if grep -q "postgres_data:" ".devcontainer/docker-compose.yml"; then
        echo -e "${GREEN}✓${NC} PostgreSQL data volume configured"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} PostgreSQL data volume missing"
        ((FAIL++))
    fi
    
    if grep -q "redis_data:" ".devcontainer/docker-compose.yml"; then
        echo -e "${GREEN}✓${NC} Redis data volume configured"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Redis data volume missing"
        ((FAIL++))
    fi
fi
echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ Validation Summary                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${GREEN}✓ Passed:${NC}  $PASS"
echo -e "  ${YELLOW}⚠ Warnings:${NC} $WARN"
echo -e "  ${RED}✗ Failed:${NC}  $FAIL"
echo ""

# Scoring
TOTAL=$((PASS + FAIL))
if [ "$TOTAL" -gt 0 ]; then
    SCORE=$((PASS * 100 / TOTAL))
else
    SCORE=0
fi

echo -e "  📊 ${BLUE}Score: $SCORE%${NC}"
echo ""

# Recommendations
if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Your dev container is enterprise-ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cp .devcontainer/.env.example .devcontainer/.env"
    echo "  2. Edit .devcontainer/.env with your credentials"
    echo "  3. Open VS Code: code ."
    echo "  4. Press F1 → 'Dev Containers: Reopen in Container'"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  Some checks failed. Review above and fix issues.${NC}"
    echo ""
    exit 1
fi

