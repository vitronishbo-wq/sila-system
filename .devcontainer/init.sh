#!/bin/bash

# ============================================================================
# SILA DevContainer Initialization Script (Enterprise-Ready)
# ============================================================================

set -e

echo "🚀 Initializing SILA Enterprise Development Environment..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Trap errors
trap 'echo -e "${RED}❌ Initialization failed!${NC}" >&2' ERR

# Set umask early (ensures created files have readable permissions globally)
umask 0022

# 0. Permission validation (CRITICAL - fail fast)
echo -e "${BLUE}[0/7]${NC} Validating filesystem permissions..."
if ! touch /workspace/.perm_test 2>/dev/null; then
    echo -e "${RED}❌ CRITICAL: No write permission on /workspace${NC}"
    echo "Host permissions: $(ls -ld /workspace)"
    echo "Container user: $(id)"
    exit 1
fi
rm /workspace/.perm_test
echo "  ✓ /workspace is writable (permissions OK)"

# SSH agent diagnostics (non-blocking)
if [ -z "$SSH_AUTH_SOCK" ]; then
    echo -e "${YELLOW}  ⚠️  SSH agent not available (git operations may fail)${NC}"
else
    echo "  ✓ SSH_AUTH_SOCK: $SSH_AUTH_SOCK"
fi

# 1. Environment validation
echo -e "${BLUE}[1/7]${NC} Validating environment..."
if [ -z "$POSTGRES_HOST" ]; then
    export POSTGRES_HOST=db
fi
if [ -z "$REDIS_HOST" ]; then
    export REDIS_HOST=redis
fi
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=sila_user
fi
if [ -z "$POSTGRES_DB" ]; then
    export POSTGRES_DB=sila_db
fi
echo "  ✓ POSTGRES_HOST: $POSTGRES_HOST"
echo "  ✓ REDIS_HOST: $REDIS_HOST"

# 2. Wait for PostgreSQL
echo -e "${BLUE}[2/7]${NC} Waiting for PostgreSQL..."
max_retries=30
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" 2>/dev/null; then
        echo "  ✓ PostgreSQL healthy"
        break
    fi
    retry_count=$((retry_count + 1))
    echo "  ⏳ Attempt $retry_count/$max_retries..."
    sleep 2
done

if [ $retry_count -eq $max_retries ]; then
    echo "  ⚠️ PostgreSQL not ready (will retry on first migration)"
fi

# 3. Wait for Redis
echo -e "${BLUE}[3/7]${NC} Waiting for Redis..."
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if redis-cli -h "$REDIS_HOST" ping 2>/dev/null | grep -q PONG; then
        echo "  ✓ Redis healthy"
        break
    fi
    retry_count=$((retry_count + 1))
    echo "  ⏳ Attempt $retry_count/$max_retries..."
    sleep 1
done

if [ $retry_count -eq $max_retries ]; then
    echo "  ⚠️ Redis not ready (will retry on startup)"
fi

# 4. Install dev dependencies
echo -e "${BLUE}[4/7]${NC} Installing development dependencies..."
cd /workspace

if [ -f "requirements/dev.txt" ]; then
    pip install -q -r requirements/dev.txt 2>/dev/null && echo "  ✓ Dev requirements installed" || echo "  ⚠️ Some dev dependencies skipped"
elif [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt 2>/dev/null && echo "  ✓ Base requirements installed" || echo "  ⚠️ Some requirements skipped"
else
    echo "  ℹ️ No requirements found"
fi

# 5. Set up pre-commit hooks (if available)
echo -e "${BLUE}[5/7]${NC} Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    if [ -f ".pre-commit-config.yaml" ]; then
        pre-commit install 2>/dev/null && echo "  ✓ Pre-commit configured" || echo "  ℹ️ Pre-commit skipped"
    else
        echo "  ℹ️ No .pre-commit-config.yaml found"
    fi
else
    echo "  ℹ️ pre-commit not installed"
fi

# 6. Database migration (if alembic exists)
echo -e "${BLUE}[6/7]${NC} Running database migrations..."
if [ -d "apps/backend/alembic" ]; then
    cd apps/backend
    
    # Wait one more time before migration
    echo "  ⏳ Final PostgreSQL check..."
    retry_count=0
    while [ $retry_count -lt 10 ]; do
        if pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" 2>/dev/null; then
            echo "  ✓ PostgreSQL ready, running migrations..."
            alembic upgrade heads 2>&1 | tail -10 || true
            break
        fi
        retry_count=$((retry_count + 1))
        echo "  ⏳ Retry $retry_count/10..."
        sleep 2
    done
    
    if [ $retry_count -eq 10 ]; then
        echo "  ⚠️ Skipping migrations (database not ready)"
    fi
    
    cd /workspace
else
    echo "  ℹ️ No alembic directory found"
fi

# 7. Final validation
echo -e "${BLUE}[7/7]${NC} Final environment validation..."
echo "  ✓ UID/GID: $(id)"
echo "  ✓ Workspace: $(pwd)"
echo "  ✓ Umask: $(umask)"
echo ""
echo -e "${GREEN}✅ Environment ready!${NC}"
echo ""
echo -e "${YELLOW}Quick commands:${NC}"
echo "  📦 make setup          - Install all dependencies"
echo "  🧪 make test           - Run test suite"
echo "  🔍 make audit-full     - Full architecture audit"
echo "  🚀 make pipeline       - Build + migrate + test"
echo "  🔗 make dev            - Start dev server"
echo ""
echo -e "${YELLOW}Services:${NC}"
echo "  PostgreSQL: postgres://$POSTGRES_USER@$POSTGRES_HOST:5432/$POSTGRES_DB"
echo "  Redis: redis://$REDIS_HOST:6379"
echo ""
echo -e "${GREEN}Ready for Codex full autonomy mode! 🤖${NC}"
echo ""
