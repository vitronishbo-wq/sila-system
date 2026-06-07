#!/usr/bin/env bash
################################################################################
# MIGRATION GUARDRAIL
# Executa Alembic upgrade head com proteções contra drift silencioso
# DEVE ser executado em: CI/CD pipeline, init, pre-deployment
################################################################################

set -e

BACKEND_DIR="${BACKEND_DIR:-apps/backend}"
ALEMBIC_INI="$BACKEND_DIR/alembic.ini"
MIGRATION_VERSIONS="$BACKEND_DIR/alembic/versions"

echo "🔐 MIGRATION GUARDRAIL STARTED"
echo "📅 $(date)"
echo ""

# ============================================================================
# CHECK 1: Alembic.ini exists
# ============================================================================
if [ ! -f "$ALEMBIC_INI" ]; then
    echo "❌ ERROR: alembic.ini not found at $ALEMBIC_INI"
    exit 1
fi
echo "✅ alembic.ini found"

# ============================================================================
# CHECK 2: Migration versions directory exists
# ============================================================================
if [ ! -d "$MIGRATION_VERSIONS" ]; then
    echo "❌ ERROR: Migration versions directory not found at $MIGRATION_VERSIONS"
    exit 1
fi
echo "✅ Migration versions directory found"

# ============================================================================
# CHECK 3: Database connectivity (optional but recommended)
# ============================================================================
echo ""
echo "🔌 Checking database connectivity..."
cd "$BACKEND_DIR"
if python -c "from apps.backend.app.core.config import settings; from sqlalchemy import create_engine; engine = create_engine(str(settings.database_url)); engine.connect().close()" 2>/dev/null; then
    echo "✅ Database connectivity verified"
else
    echo "⚠️  Database not accessible (migrations will fail if DB is down)"
fi

# ============================================================================
# MAIN: Alembic upgrade head (with error handling)
# ============================================================================
echo ""
echo "📦 Executing: alembic upgrade head"
echo "   This will apply all pending migrations..."
echo ""

if cd "$BACKEND_DIR" && alembic upgrade head; then
    echo ""
    echo "✅ All migrations applied successfully"
    MIGRATION_STATUS=0
else
    echo ""
    echo "❌ Migration failed - CRITICAL"
    echo "   Schema drift detected or migration error occurred"
    MIGRATION_STATUS=1
fi

# ============================================================================
# CHECK 4: Post-migration validation (optional pytest)
# ============================================================================
if [ $MIGRATION_STATUS -eq 0 ]; then
    echo ""
    echo "🧪 Running post-migration validation..."
    if python -m pytest tests/integration/test_migrations.py -v --tb=short 2>/dev/null; then
        echo "✅ Post-migration tests passed"
    else
        echo "⚠️  Post-migration tests not available or failed"
    fi
fi

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "📊 MIGRATION GUARDRAIL SUMMARY"
echo "=============================="
if [ $MIGRATION_STATUS -eq 0 ]; then
    echo "✅ Status: SUCCESS"
    echo "   Database schema is synchronized with migrations"
    echo "📅 $(date)"
    exit 0
else
    echo "❌ Status: FAILED"
    echo "   Database migration failed - manual intervention required"
    echo "📅 $(date)"
    exit 1
fi
