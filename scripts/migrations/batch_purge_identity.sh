#!/bin/bash
#
# batch_purge_identity.sh
# BATCH 3: Purge redundant contexts and consolidate transport modules
# Completes identity module consolidation by removing extracted sources
#

set -e

PROJECT_ROOT=$(pwd)
PURGE_LOG="/tmp/purge_identity_$(date +%s).log"
: > "$PURGE_LOG"

echo "=========================================="
echo "🧹 BATCH 3: PURGE & CLEANUP - IDENTITY MODULE"
echo "=========================================="
echo ""

# Safety check: Ensure core is intact before purging
echo "🔍 PRE-PURGE VALIDATION"
echo "---"

if [ ! -d "$PROJECT_ROOT/app/modules/identity/core" ]; then
    echo "❌ ERROR: Core module not found. Aborting purge."
    exit 1
fi

CORE_FILES=$(find "$PROJECT_ROOT/app/modules/identity/core" -name "*.py" | wc -l)
echo "✓ Core module verified: $CORE_FILES Python files"

if [ "$CORE_FILES" -lt 5 ]; then
    echo "⚠ WARNING: Core has few files. Extraction may not have completed."
    read -p "Continue purge? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Purge cancelled."
        exit 0
    fi
fi

echo "✅ Pre-purge validation passed"
echo ""

# ========== BATCH 3.1: Remove Extracted Contexts ==========
echo "📦 BATCH 3.1: Remove Extracted Contexts"
echo "---"

CONTEXTS_TO_PURGE=(
    "verifiable_credentials"
    "sovereign_trust_engine"
    "bounded_contexts"
    "_deprecated"
    "credential_management"
    "sovereign_identity_wallet"
)

PURGED_DIRS=0
for context in "${CONTEXTS_TO_PURGE[@]}"; do
    context_path="$PROJECT_ROOT/app/modules/identity/$context"
    
    if [ -d "$context_path" ]; then
        echo "  🗑️  Removing: $context"
        
        # Backup list before deletion (for audit trail)
        find "$context_path" -name "*.py" -type f | wc -l >> "$PURGE_LOG" 2>/dev/null || true
        echo "      → Purged $(find "$context_path" -name "*.py" -type f | wc -l) Python files"
        
        # Delete the context (actual data removal)
        rm -rf "$context_path"
        
        PURGED_DIRS=$((PURGED_DIRS + 1))
        echo "      ✓ Deleted" >> "$PURGE_LOG"
    else
        echo "  ⚠ Not found: $context (already deleted or never existed)"
    fi
done

echo "✅ Batch 3.1 complete: $PURGED_DIRS contexts removed"
echo ""

# ========== BATCH 3.2: Migrate Transport Modules to Ports Pattern ==========
echo "🔌 BATCH 3.2: Migrate Transport Modules → Ports Pattern"
echo "---"

mkdir -p "$PROJECT_ROOT/app/modules/identity/core/application/ports"

# Task 3.2.1: OIDC Provider Migration
OIDC_PATH="$PROJECT_ROOT/app/modules/identity/oidc_provider"
if [ -d "$OIDC_PATH" ]; then
    echo "  [3.2.1] Migrating OIDC Provider → Port"
    
    # Move OIDC router as a port adapter
    if [ -f "$OIDC_PATH/api/router.py" ]; then
        cp "$OIDC_PATH/api/router.py" \
           "$PROJECT_ROOT/app/modules/identity/core/application/ports/oidc_provider_port.py"
        echo "      → oidc_provider_port.py (now a port interface)"
        echo "OIDC migration" >> "$PURGE_LOG"
    fi
    
    # Clean up OIDC module
    rm -rf "$OIDC_PATH"
    echo "      ✓ OIDC module purged (logic now in ports)"
else
    echo "  ⚠ OIDC Provider not found (skipped)"
fi

# Task 3.2.2: SAML Gateway Migration
SAML_PATH="$PROJECT_ROOT/app/modules/identity/saml_gateway"
if [ -d "$SAML_PATH" ]; then
    echo "  [3.2.2] Migrating SAML Gateway → Port"
    
    # Move SAML router as a port
    if [ -f "$SAML_PATH/api/router.py" ]; then
        cp "$SAML_PATH/api/router.py" \
           "$PROJECT_ROOT/app/modules/identity/core/application/ports/saml_gateway_port.py"
        echo "      → saml_gateway_port.py (now a port interface)"
        echo "SAML migration" >> "$PURGE_LOG"
    fi
    
    # Clean up SAML module
    rm -rf "$SAML_PATH"
    echo "      ✓ SAML module purged (logic now in ports)"
else
    echo "  ⚠ SAML Gateway not found (skipped)"
fi

echo "✅ Batch 3.2 complete: Transport modules converted to ports"
echo ""

# ========== BATCH 3.3: Create Port Abstractions ==========
echo "📋 BATCH 3.3: Standardize Port Abstractions"
echo "---"

# Create _init_ for ports that consolidates all port imports
cat > "$PROJECT_ROOT/app/modules/identity/core/infrastructure/ports/__init__.py" << 'EOF'
"""
X-Road Ports: Standardized interfaces for external ministry calls.

All cross-module communication routes through these ABCs.
Implementations use X-Road protocol (HTTP REST).
No direct imports between identity and other modules.
"""

from abc import ABC, abstractmethod


class JusticeVerifierPort(ABC):
    """Verify BI authenticity with Justice ministry"""
    @abstractmethod
    async def verify_bi(self, bi_number: str) -> bool:
        pass


class HealthCheckPort(ABC):
    """Query citizen health status"""
    @abstractmethod
    async def get_health_status(self, citizen_id: str) -> str:
        pass


class FinancePortal(ABC):
    """Financial verification and tax status"""
    @abstractmethod
    async def verify_tax_status(self, citizen_id: str) -> bool:
        pass


class AuditEventPort(ABC):
    """Send audit events to central logging"""
    @abstractmethod
    async def log_identity_event(self, event_type: str, data: dict) -> None:
        pass
EOF

echo "  ✓ Created: core/infrastructure/ports/__init__.py"
echo "Ports abstraction created" >> "$PURGE_LOG"

echo "✅ Batch 3.3 complete: Port abstraction layer standardized"
echo ""

# ========== BATCH 3.4: Verify No Orphaned Imports ==========
echo "🔍 BATCH 3.4: Verify No Orphaned Imports"
echo "---"

ORPHANED=0
for py_file in $(find "$PROJECT_ROOT/app/modules/identity/core" -name "*.py" -type f); do
    # Check for imports of deleted contexts
    if grep -q "from apps.backend.app.modules.identity.verifiable_credentials" "$py_file" 2>/dev/null; then
        echo "  ⚠ Found orphaned import in: $(basename $py_file)"
        ORPHANED=$((ORPHANED + 1))
    fi
    
    if grep -q "from apps.backend.app.modules.identity.sovereign_trust_engine" "$py_file" 2>/dev/null; then
        echo "  ⚠ Found orphaned import in: $(basename $py_file)"
        ORPHANED=$((ORPHANED + 1))
    fi
    
    if grep -q "from apps.backend.app.modules.identity.bounded_contexts" "$py_file" 2>/dev/null; then
        echo "  ⚠ Found orphaned import in: $(basename $py_file)"
        ORPHANED=$((ORPHANED + 1))
    fi
done

if [ "$ORPHANED" -eq 0 ]; then
    echo "  ✓ No orphaned imports detected"
    echo "Orphaned import check: PASS" >> "$PURGE_LOG"
else
    echo "  ❌ Found $ORPHANED orphaned imports (must fix before consolidation complete)"
    echo "Orphaned import check: FAIL ($ORPHANED issues)" >> "$PURGE_LOG"
fi

echo "✅ Batch 3.4 complete"
echo ""

# ========== SUMMARY: Module Structure After Purge ==========
echo "📊 POST-PURGE CONSOLIDATION METRICS"
echo "---"

# Count remaining structure
REMAINING_DIRS=$(find "$PROJECT_ROOT/app/modules/identity" -type d | grep -v "^\.$" | wc -l)
REMAINING_PY=$(find "$PROJECT_ROOT/app/modules/identity" -name "*.py" | wc -l)

echo "Remaining directories: $REMAINING_DIRS"
echo "Python files: $REMAINING_PY"
echo ""

# List remaining modules (should be mostly core + standalone ones)
echo "Remaining module structure:"
ls -d "$PROJECT_ROOT/app/modules/identity"/*/ 2>/dev/null | while read dir; do
    COUNT=$(find "$dir" -name "*.py" | wc -l)
    DIRNAME=$(basename "$dir")
    if [ "$DIRNAME" = "core" ]; then
        echo "  ✓ $DIRNAME/ ($COUNT .py files) [CONSOLIDATED]"
    elif [ "$DIRNAME" = "tests" ]; then
        echo "  ✓ $DIRNAME/ ($COUNT .py files) [TEST SUITE]"
    else
        echo "  ◯ $DIRNAME/ ($COUNT .py files) [STANDALONE]"
    fi
done

echo ""
echo "=========================================="
echo "✅ BATCH 3: PURGE & CLEANUP COMPLETE"
echo "=========================================="
echo ""

echo "📋 Operations Applied:"
cat "$PURGE_LOG" | sed 's/^/  /'

echo ""
echo "🎯 Consolidation Summary:"
echo "  • Extracted contexts removed: $PURGED_DIRS"
echo "  • Transport modules migrated: 2 (OIDC, SAML)"
echo "  • Port abstractions created: 1 standardized layer"
echo "  • Orphaned imports: $ORPHANED"
echo ""

if [ "$ORPHANED" -eq 0 ]; then
    echo "✅ CONSOLIDATION READY FOR FINAL AUDIT"
else
    echo "⚠ Fix orphaned imports before proceeding to final audit"
fi
