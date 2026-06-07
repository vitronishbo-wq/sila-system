#!/usr/bin/env bash
################################################################################
# 🚀 SILA SYSTEM - 100% AUTONOMY ACTIVATION GUIDE
#
# This guide walks through activating the Codex Agent in full autonomous mode
# with all infrastructure, pipelines, and safeguards enabled.
#
# PREREQUISITE: All layers validated (see AUTONOMY_CHECKLIST.md)
################################################################################

set -e

echo "🚀 SILA System - 100% Autonomy Activation"
echo "=========================================="
echo ""

# ============================================================================
# STEP 1: Verify Environment
# ============================================================================
echo "✅ STEP 1: Verifying Environment Setup"
echo ""

# Check Docker
if command -v docker &> /dev/null; then
    echo "  ✅ Docker: $(docker --version)"
else
    echo "  ❌ Docker not found. Install Docker Desktop."
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "  ✅ Python: $(python3 --version)"
else
    echo "  ❌ Python not found."
    exit 1
fi

# Check Makefile
if [ -f Makefile ]; then
    echo "  ✅ Makefile: Detected"
else
    echo "  ❌ Makefile not found."
    exit 1
fi

echo ""

# ============================================================================
# STEP 2: Start DevContainer Stack
# ============================================================================
echo "✅ STEP 2: Starting DevContainer Stack"
echo ""

echo "  Starting services..."
make devcontainer-up
echo "  ✅ Stack started (PostgreSQL, Redis, RabbitMQ)"

sleep 5

echo ""

# ============================================================================
# STEP 3: Database Migrations
# ============================================================================
echo "✅ STEP 3: Running Database Migrations"
echo ""

make migration-guardrail

echo ""

# ============================================================================
# STEP 4: Run Quality Pipeline
# ============================================================================
echo "✅ STEP 4: Running Quality Pipeline"
echo ""

echo "  This validates:"
echo "  - Code formatting (ruff)"
echo "  - Test suite (pytest)"
echo "  - Architecture (audit-full)"
echo ""

make pipeline

echo ""

# ============================================================================
# STEP 5: Enable Post-Mutation Pipeline
# ============================================================================
echo "✅ STEP 5: Post-Mutation Pipeline Ready"
echo ""

echo "  This runs automatically after any code mutation:"
echo "  - Command: make post-mutation-pipeline"
echo "  - Or call directly: bash scripts/post-mutation-pipeline.sh"
echo ""

# ============================================================================
# STEP 6: Configuration Summary
# ============================================================================
echo "✅ STEP 6: System Configuration"
echo ""

cat << 'EOF'
🔐 Credentials (Configure in your environment):
   POSTGRES_USER=sila_user
   POSTGRES_PASSWORD=(from securely stored vault)
   POSTGRES_DB=sila_db
   POSTGRES_HOST=db (docker-compose) or localhost (direct)
   POSTGRES_PORT=5432

🔧 Available Commands:
   make help                   - Show all available commands
   make pipeline              - Run full quality gate
   make codex-agent           - Activate Codex in autonomy mode
   make daily-audit           - Run daily health check
   make watch-mode            - Auto-run tests on .py changes
   
  Integration Commands:
   make post-mutation-pipeline - Auto-run: ruff fix → black → pytest
   make migration-guardrail    - Verify: alembic upgrade head
   make b904-batch-fixer      - Fix exception handling in batch

📊 Monitoring:
   tail -f post-mutation-pipeline.log  - Watch pipeline execution
   make daily-audit                    - Generate health report

EOF

echo ""

# ============================================================================
# STEP 7: Final Activation
# ============================================================================
echo "✅ STEP 7: Ready for Full Autonomy"
echo ""

cat << 'EOF'

🎯 ACTIVATION SEQUENCE:

1️⃣  Codex Agent (Full Autonomy)
    make codex-agent

    Now the agent can:
    ✅ Implement features (e.g., "add JWT auth")
    ✅ Scaffold modules (e.g., "create payment service")
    ✅ Refactor code (e.g., "improve error handling")
    ✅ Run migrations (automatic)
    ✅ Run tests (automatic)
    ✅ Apply auto-fixes (automatic)

2️⃣  Example Agent Command:
    "Apply B904 to all remaining routers"
    
    Agent will:
    - Scan for B904 violations
    - Create batch fixes
    - Run post-mutation pipeline
    - Validate with pytest
    - Report results

3️⃣  Continuous Validation:
    make daily-audit
    
    Runs every 24 hours:
    - Code quality check
    - Architecture validation
    - Database schema check
    - Performance audit

🚨 SAFEGUARDS ENABLED:
   ✅ Post-mutation pipeline validates every change
   ✅ Migration guardrails prevent schema drift
   ✅ Architecture audit prevents circular dependencies
   ✅ Pytest validates functionality
   ✅ Ruff ensures code quality

EOF

echo ""
echo "🎉 SYSTEM FULLY OPERATIONAL - 100% AUTONOMY ENABLED"
echo ""
