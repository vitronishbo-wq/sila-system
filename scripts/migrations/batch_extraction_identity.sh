#!/bin/bash
#
# batch_extraction_identity.sh
# Parallel extraction of identity module components into core
#

set -e
PROJECT_ROOT=$(pwd)
BATCH_LOG="/tmp/batch_extraction_$(date +%s).log"
: > "$BATCH_LOG"

echo "=========================================="
echo "⚙️  BATCH 2: PARALLEL EXTRACTION - IDENTITY MODULE"
echo "=========================================="
echo ""

# ========== BATCH 1: Extract Sovereign Entities [TASK_2.1] ==========
echo "📦 BATCH 1: Extract Sovereign Entities"
echo "---"

mkdir -p "$PROJECT_ROOT/app/modules/identity/core/domain/entities"

# Task 1.1: Verifiable Credentials Entities
if [ -d "$PROJECT_ROOT/app/modules/identity/verifiable_credentials/domain/entities" ]; then
    echo "  [TASK_1.1] ✓ Verifiable Credentials Entities"
    find "$PROJECT_ROOT/app/modules/identity/verifiable_credentials/domain/entities" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        cp "$file" "$PROJECT_ROOT/app/modules/identity/core/domain/entities/$filename" 2>/dev/null || true
        echo "    → $filename" >> "$BATCH_LOG"
    done
else
    echo "  [TASK_1.1] ⚠ Verifiable Credentials not found (skipped)"
fi

# Task 1.2: Access Control Entities
if [ -d "$PROJECT_ROOT/app/modules/identity/bounded_contexts/access_control/domain/entities" ]; then
    echo "  [TASK_1.2] ✓ Access Control Entities"
    find "$PROJECT_ROOT/app/modules/identity/bounded_contexts/access_control/domain/entities" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        cp "$file" "$PROJECT_ROOT/app/modules/identity/core/domain/entities/$filename" 2>/dev/null || true
        echo "    → $filename" >> "$BATCH_LOG"
    done
else
    echo "  [TASK_1.2] ⚠ Access Control not found (skipped)"
fi

echo "✅ Batch 1 complete"
echo ""

# ========== BATCH 2: Consolidate Identity Services [TASK_2.2] ==========
echo "🔧 BATCH 2: Consolidate Identity Services (High-Trust Layer)"
echo "---"

mkdir -p "$PROJECT_ROOT/app/modules/identity/core/application/services"

# Task 2.1: Verifiable Credentials Services
if [ -d "$PROJECT_ROOT/app/modules/identity/verifiable_credentials/application/services" ]; then
    echo "  [TASK_2.1] ✓ Verifiable Credentials Services"
    find "$PROJECT_ROOT/app/modules/identity/verifiable_credentials/application/services" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        cp "$file" "$PROJECT_ROOT/app/modules/identity/core/application/services/$filename" 2>/dev/null || true
        echo "    → $filename" >> "$BATCH_LOG"
    done
else
    echo "  [TASK_2.1] ⚠ Verifiable Credentials Services not found"
fi

# Task 2.2: Sovereign Trust Engine Services
if [ -d "$PROJECT_ROOT/app/modules/identity/sovereign_trust_engine/application" ]; then
    echo "  [TASK_2.2] ✓ Sovereign Trust Engine"
    find "$PROJECT_ROOT/app/modules/identity/sovereign_trust_engine/application" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        if [ "$filename" != "__init__.py" ]; then
            cp "$file" "$PROJECT_ROOT/app/modules/identity/core/application/services/${filename%.py}_trust_engine.py" 2>/dev/null || true
            echo "    → ${filename%.py}_trust_engine.py" >> "$BATCH_LOG"
        fi
    done
else
    echo "  [TASK_2.2] ⚠ Sovereign Trust Engine not found"
fi

# Task 2.3: IAM Services
if [ -d "$PROJECT_ROOT/app/modules/identity/bounded_contexts/iam/application/services" ]; then
    echo "  [TASK_2.3] ✓ IAM Services"
    find "$PROJECT_ROOT/app/modules/identity/bounded_contexts/iam/application/services" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        if [ "$filename" != "__init__.py" ]; then
            cp "$file" "$PROJECT_ROOT/app/modules/identity/core/application/services/$filename" 2>/dev/null || true
            echo "    → $filename" >> "$BATCH_LOG"
        fi
    done
else
    echo "  [TASK_2.3] ⚠ IAM Services not found"
fi

echo "✅ Batch 2 complete"
echo ""

# ========== BATCH 3: Migrate Repositories & Security [TASK_2.3] ==========
echo "🔐 BATCH 3: Migrate Repositories & Security Layer"
echo "---"

mkdir -p "$PROJECT_ROOT/app/modules/identity/core/infrastructure/repositories"
mkdir -p "$PROJECT_ROOT/app/modules/identity/core/infrastructure/security"
mkdir -p "$PROJECT_ROOT/app/modules/identity/core/infrastructure/models"

# Task 3.1: Verifiable Credentials Repositories
if [ -d "$PROJECT_ROOT/app/modules/identity/verifiable_credentials/infrastructure/repositories" ]; then
    echo "  [TASK_3.1] ✓ VC Repositories"
    find "$PROJECT_ROOT/app/modules/identity/verifiable_credentials/infrastructure/repositories" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        cp "$file" "$PROJECT_ROOT/app/modules/identity/core/infrastructure/repositories/$filename" 2>/dev/null || true
        echo "    → $filename" >> "$BATCH_LOG"
    done
else
    echo "  [TASK_3.1] ⚠ VC Repositories not found"
fi

# Task 3.2: Access Control Repositories
if [ -d "$PROJECT_ROOT/app/modules/identity/bounded_contexts/access_control/infrastructure/repositories" ]; then
    echo "  [TASK_3.2] ✓ Access Control Repositories"
    find "$PROJECT_ROOT/app/modules/identity/bounded_contexts/access_control/infrastructure/repositories" -name "*.py" -type f 2>/dev/null | while read file; do
        filename=$(basename "$file")
        cp "$file" "$PROJECT_ROOT/app/modules/identity/core/infrastructure/repositories/$filename" 2>/dev/null || true
        echo "    → $filename" >> "$BATCH_LOG"
    done
else
    echo "  [TASK_3.2] ⚠ Access Control Repositories not found"
fi

# Task 3.3: Legacy Security Layer (JWT Engine)
if [ -f "$PROJECT_ROOT/app/modules/identity/infrastructure/security/jwt_engine.py" ]; then
    echo "  [TASK_3.3] ✓ JWT Engine (Security)"
    cp "$PROJECT_ROOT/app/modules/identity/infrastructure/security/jwt_engine.py" \
       "$PROJECT_ROOT/app/modules/identity/core/infrastructure/security/jwt_engine.py" 2>/dev/null || true
    echo "    → jwt_engine.py" >> "$BATCH_LOG"
else
    echo "  [TASK_3.3] ⚠ JWT Engine not found"
fi

# Task 3.4: User Model
if [ -f "$PROJECT_ROOT/app/modules/identity/infrastructure/models/user_model.py" ]; then
    echo "  [TASK_3.4] ✓ User Model"
    cp "$PROJECT_ROOT/app/modules/identity/infrastructure/models/user_model.py" \
       "$PROJECT_ROOT/app/modules/identity/core/infrastructure/models/user_model.py" 2>/dev/null || true
    echo "    → user_model.py" >> "$BATCH_LOG"
else
    echo "  [TASK_3.4] ⚠ User Model not found"
fi

# Task 3.5: Citizen Repository (if exists in top-level infrastructure)
if [ -f "$PROJECT_ROOT/app/modules/identity/infrastructure/repositories/citizen_repository.py" ]; then
    echo "  [TASK_3.5] ✓ Citizen Repository"
    cp "$PROJECT_ROOT/app/modules/identity/infrastructure/repositories/citizen_repository.py" \
       "$PROJECT_ROOT/app/modules/identity/core/infrastructure/repositories/citizen_repository.py" 2>/dev/null || true
    echo "    → citizen_repository.py" >> "$BATCH_LOG"
else
    echo "  [TASK_3.5] ⚠ Citizen Repository not found"
fi

echo "✅ Batch 3 complete"
echo ""

# ========== AUDIT: Count consolidated files ==========
echo "📊 CONSOLIDATION SUMMARY"
echo "---"

ENTITY_COUNT=$(find "$PROJECT_ROOT/app/modules/identity/core/domain/entities" -name "*.py" -type f 2>/dev/null | wc -l)
SERVICE_COUNT=$(find "$PROJECT_ROOT/app/modules/identity/core/application/services" -name "*.py" -type f 2>/dev/null | wc -l)
REPO_COUNT=$(find "$PROJECT_ROOT/app/modules/identity/core/infrastructure/repositories" -name "*.py" -type f 2>/dev/null | wc -l)
SEC_COUNT=$(find "$PROJECT_ROOT/app/modules/identity/core/infrastructure/security" -name "*.py" -type f 2>/dev/null | wc -l)
MODEL_COUNT=$(find "$PROJECT_ROOT/app/modules/identity/core/infrastructure/models" -name "*.py" -type f 2>/dev/null | wc -l)

echo "✅ Domain Entities: $ENTITY_COUNT files"
echo "✅ Application Services: $SERVICE_COUNT files"
echo "✅ Infrastructure Repositories: $REPO_COUNT files"
echo "✅ Security Components: $SEC_COUNT files"
echo "✅ Data Models: $MODEL_COUNT files"
echo ""

TOTAL_OPERATIONS=$(grep -c "→" "$BATCH_LOG" || echo "0")
echo "📋 Total Operations Applied (Parallel): $TOTAL_OPERATIONS"
echo ""

echo "=========================================="
echo "✅ BATCH 2 EXTRACTION COMPLETE"
echo "=========================================="

cat "$BATCH_LOG"
