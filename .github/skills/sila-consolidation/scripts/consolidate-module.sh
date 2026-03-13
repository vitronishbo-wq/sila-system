#!/bin/bash
#
# consolidate-module.sh
# Main consolidation script - extracts scattered logic into hexagonal core
# Usage: ./consolidate-module.sh <MODULE_NAME>
# Example: ./consolidate-module.sh justice
#

set -e

MODULE="${1:-justice}"
PROJECT_ROOT="${PROJECT_ROOT:-.}"
MODULE_PATH="$PROJECT_ROOT/app/modules/$MODULE"

if [ ! -d "$MODULE_PATH" ]; then
    echo "❌ Module not found: $MODULE_PATH"
    exit 1
fi

echo "=========================================="
echo "SILA Consolidation: $MODULE"
echo "=========================================="
echo ""

# ============ PHASE 1: INDEX DISCOVERY ============
echo "📋 PHASE 1: Index-Based Discovery"
echo "---"

echo "Locating scattered logic..."
SCATTERED_COUNT=$(find "$MODULE_PATH" -name "*.py" | grep -E "(service|entity|model)" | wc -l)
echo "Found $SCATTERED_COUNT candidate files"
echo ""

# ============ PHASE 2: CREATE TARGET STRUCTURE ============
echo "🏗️ PHASE 2: Creating Hexagonal Core Structure"
echo "---"

CORE_DIR="$MODULE_PATH/core"
mkdir -p "$CORE_DIR"/{domain,application,infrastructure}
mkdir -p "$CORE_DIR/domain"/{entities,events,value_objects}
mkdir -p "$CORE_DIR/application"/{ports,services,dto}
mkdir -p "$CORE_DIR/infrastructure"/{models,repositories,adapters,ports}

echo "✅ Target structure created at $CORE_DIR/"
echo ""

# ============ PHASE 3: PARALLEL BATCH EXTRACTION ============
echo "⚙️ PHASE 3: Parallel Batch Extraction"
echo "---"

BATCH_LOG="/tmp/consolidation_${MODULE}_$(date +%s).log"
: > "$BATCH_LOG"  # Clear log

# Batch 1: Extract domain entities
echo "Batch 1: Extracting domain entities (parallel)..."
{
    # Find all entity files across fragmented contexts
    find "$MODULE_PATH" -path "*/core/domain/entities" -prune -o \
         -path "*/domain/entities/*.py" -type f -print 2>/dev/null | while read entity_file; do
        if [ -f "$entity_file" ]; then
            filename=$(basename "$entity_file")
            dest="$CORE_DIR/domain/entities/$filename"
            if [ ! -f "$dest" ]; then
                mv "$entity_file" "$dest"
                echo "  ✓ Moved $entity_file" >> "$BATCH_LOG"
            fi
        fi
    done
} &

# Batch 2: Extract application services
echo "Batch 2: Extracting application services (parallel)..."
{
    find "$MODULE_PATH" -path "*/core/application/services" -prune -o \
         -path "*/application/services/*.py" -type f -print 2>/dev/null | while read service_file; do
        if [ -f "$service_file" ] && ! grep -q "^from.*core\.application" "$service_file" 2>/dev/null; then
            filename=$(basename "$service_file")
            dest="$CORE_DIR/application/services/$filename"
            # Avoid overwriting existing core services
            if [ ! -f "$dest" ]; then
                mv "$service_file" "$dest"
                echo "  ✓ Moved $service_file" >> "$BATCH_LOG"
            else
                echo "  ⚠ Skipped (already exists): $filename" >> "$BATCH_LOG"
            fi
        fi
    done
} &

# Batch 3: Extract value objects
echo "Batch 3: Extracting value objects (parallel)..."
{
    find "$MODULE_PATH" -path "*/core/domain/value_objects" -prune -o \
         -path "*/value_objects/*.py" -type f -print 2>/dev/null | while read vo_file; do
        if [ -f "$vo_file" ]; then
            filename=$(basename "$vo_file")
            dest="$CORE_DIR/domain/value_objects/$filename"
            if [ ! -f "$dest" ]; then
                mv "$vo_file" "$dest"
                echo "  ✓ Moved $vo_file" >> "$BATCH_LOG"
            fi
        fi
    done
} &

# Batch 4: Extract models (SQLAlchemy, Pydantic)
echo "Batch 4: Extracting data models (parallel)..."
{
    find "$MODULE_PATH" -path "*/core/infrastructure/models" -prune -o \
         -path "*/models/*.py" -type f -print 2>/dev/null | while read model_file; do
        if [ -f "$model_file" ]; then
            filename=$(basename "$model_file")
            dest="$CORE_DIR/infrastructure/models/$filename"
            if [ ! -f "$dest" ]; then
                mv "$model_file" "$dest"
                echo "  ✓ Moved $model_file" >> "$BATCH_LOG"
            fi
        fi
    done
} &

wait
echo "✅ Batch extractions complete"
echo ""

# ============ PHASE 4: CREATE MIGRATION REPORT ============
echo "📊 PHASE 4: Migration Report"
echo "---"

MIGRATION_REPORT="/tmp/migration_${MODULE}_$(date +%s).txt"
{
    echo "Consolidation Migration Report: $MODULE"
    echo "========================================"
    echo "Timestamp: $(date)"
    echo ""
    echo "Actions Applied (Parallel Batches):"
    cat "$BATCH_LOG" | sed 's/^/  /'
    echo ""
    echo "Core Structure Verification:"
    echo "Domain entities: $(find "$CORE_DIR/domain/entities" -name "*.py" | wc -l) files"
    echo "Application services: $(find "$CORE_DIR/application/services" -name "*.py" | wc -l) files"
    echo "Data models: $(find "$CORE_DIR/infrastructure/models" -name "*.py" | wc -l) files"
} > "$MIGRATION_REPORT"

cat "$MIGRATION_REPORT"
echo ""

# ============ PHASE 5: UPDATE IMPORTS ============
echo "🔗 PHASE 5: Update Internal Imports (Core Only)"
echo "---"

# Replace old paths with core paths in extracted files
find "$CORE_DIR" -name "*.py" -type f | while read file; do
    # Update imports to use new core structure
    sed -i "s|from app\.modules\.$MODULE\.bounded_contexts\.|from app.modules.$MODULE.core.|g" "$file"
    sed -i "s|from app\.modules\.$MODULE\.$MODULE\..*\.domain\.|from app.modules.$MODULE.core.domain.|g" "$file"
    sed -i "s|from app\.modules\.$MODULE\..*\.application\.|from app.modules.$MODULE.core.application.|g" "$file"
    sed -i "s|from app\.modules\.$MODULE\..*\.infrastructure\.|from app.modules.$MODULE.core.infrastructure.|g" "$file"
done

echo "✅ Updated imports in $CORE_DIR"
echo ""

# ============ PHASE 6: GENERATE CONFORMANCE CHECKLIST ============
echo "📋 PHASE 6: Generate Conformance Checklist"
echo "---"

CHECKLIST="/tmp/conformance_${MODULE}_$(date +%Y%m%d_%H%M%S).md"
cp "references/conformance-checklist.md" "$CHECKLIST"

echo "✅ Checklist created at $CHECKLIST"
echo ""

# ============ CLEANUP ============
echo "🧹 PHASE 7: Cleanup"
echo "---"

# Remove empty directories (but preserve core)
find "$MODULE_PATH" -type d -empty ! -path "$CORE_DIR/*" -delete 2>/dev/null || true

echo "✅ Cleaned up empty directories"
echo ""

# ============ FINAL REPORT ============
echo "=========================================="
echo "✅ CONSOLIDATION COMPLETE: $MODULE"
echo "=========================================="
echo ""
echo "Summary:"
echo "  Core location: $CORE_DIR/"
echo "  Layers created: domain, application, infrastructure"
echo "  Migration log: $MIGRATION_REPORT"
echo "  Conformance checklist: $CHECKLIST"
echo ""
echo "Next steps:"
echo "  1. Review $CHECKLIST"
echo "  2. Run: pytest app/modules/$MODULE/tests/"
echo "  3. Run: ./scripts/audit-consolidation.sh $MODULE"
echo ""
