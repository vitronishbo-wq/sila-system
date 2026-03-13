#!/bin/bash
#
# audit-consolidation.sh
# Verifies consolidation success: no circular deps, compliance checks, test results
# Usage: ./audit-consolidation.sh <MODULE_NAME>
#

set -e

MODULE="${1:-justice}"
PROJECT_ROOT="${PROJECT_ROOT:-.}"
MODULE_PATH="$PROJECT_ROOT/app/modules/$MODULE"
CORE_PATH="$MODULE_PATH/core"

if [ ! -d "$CORE_PATH" ]; then
    echo "❌ Core module not found at $CORE_PATH"
    exit 1
fi

echo "=========================================="
echo "Consolidation Audit: $MODULE"
echo "=========================================="
echo ""

AUDIT_REPORT="/tmp/audit_${MODULE}_$(date +%Y%m%d_%H%M%S).md"
: > "$AUDIT_REPORT"

# ============ COMPLIANCE CHECK 1: DIRECTORY STRUCTURE ============
echo "🏗️ Check 1: Directory Structure"
echo "---"
{
    echo "## Directory Structure"
    echo ""
    
    checks=0
    pass=0
    
    for dir in domain application infrastructure; do
        checks=$((checks + 1))
        if [ -d "$CORE_PATH/$dir" ]; then
            echo "✅ \`$dir/\` exists"
            pass=$((pass + 1))
        else
            echo "❌ \`$dir/\` missing"
        fi
    done
    
    for dir in domain/entities application/services infrastructure/models; do
        checks=$((checks + 1))
        if [ -d "$CORE_PATH/$dir" ]; then
            echo "✅ \`$dir/\` exists"
            pass=$((pass + 1))
        else
            echo "❌ \`$dir/\` missing"
        fi
    done
    
    echo ""
    echo "Structure Score: $pass/$checks"
} | tee -a "$AUDIT_REPORT"
echo ""

# ============ COMPLIANCE CHECK 2: NO CIRCULAR IMPORTS ============
echo "🔄 Check 2: Circular Dependency Detection"
echo "---"
{
    echo "## Circular Dependencies" >> "$AUDIT_REPORT"
    echo "" >> "$AUDIT_REPORT"
    
    # Check for imports back to non-core contexts
    CIRCULAR_COUNT=$(
        find "$CORE_PATH" -name "*.py" -type f -exec grep -l \
            -e "from app\.modules\..*\.bounded_contexts\b" \
            -e "from app\.modules\..*\.civil_registry\b" \
            -e "from app\.modules\..*\.vital_events\b" \
            {} \; 2>/dev/null | wc -l
    )
    
    if [ "$CIRCULAR_COUNT" -eq 0 ]; then
        echo "✅ No imports to obsolete contexts"
        echo "✅ No imports to obsolete contexts" >> "$AUDIT_REPORT"
    else
        echo "❌ Found $CIRCULAR_COUNT files with problematic imports"
        echo "❌ Found $CIRCULAR_COUNT files with problematic imports" >> "$AUDIT_REPORT"
        find "$CORE_PATH" -name "*.py" -type f -exec grep -l \
            -e "from app\.modules\..*\.bounded_contexts\b" \
            -e "from app\.modules\..*\.civil_registry\b" \
            {} \; 2>/dev/null | sed 's/^/  File: /'
    fi
} | tee -a "$AUDIT_REPORT"
echo ""

# ============ COMPLIANCE CHECK 3: TEST EXECUTION ============
echo "🧪 Check 3: Unit Tests"
echo "---"
{
    echo "## Test Results" >> "$AUDIT_REPORT"
    echo "" >> "$AUDIT_REPORT"
    
    if command -v pytest &> /dev/null; then
        TEST_PATH="$CORE_PATH/tests"
        if [ -d "$TEST_PATH" ]; then
            echo "Running pytest on $TEST_PATH..."
            if pytest "$TEST_PATH" -v --tb=short -q > /tmp/pytest_output.txt 2>&1; then
                PASS_COUNT=$(grep -c "PASSED\|passed" /tmp/pytest_output.txt || echo "0")
                echo "✅ All tests passed"
                echo "✅ All tests passed ($PASS_COUNT)" >> "$AUDIT_REPORT"
                tail -10 /tmp/pytest_output.txt | sed 's/^/  /' >> "$AUDIT_REPORT"
            else
                FAIL_COUNT=$(grep -c "FAILED\|failed" /tmp/pytest_output.txt || echo "0")
                echo "❌ Tests failed ($FAIL_COUNT failures)"
                echo "❌ Tests failed ($FAIL_COUNT failures)" >> "$AUDIT_REPORT"
                tail -20 /tmp/pytest_output.txt | sed 's/^/  /' >> "$AUDIT_REPORT"
            fi
        else
            echo "⚠️ No tests directory found at $TEST_PATH"
            echo "⚠️ No tests directory found" >> "$AUDIT_REPORT"
        fi
    else
        echo "⚠️ pytest not installed; skipping test execution"
        echo "⚠️ pytest not installed" >> "$AUDIT_REPORT"
    fi
} | tee -a "$AUDIT_REPORT"
echo ""

# ============ COMPLIANCE CHECK 4: PORT DEFINITIONS ============
echo "🔌 Check 4: Port Definitions (X-Road Boundaries)"
echo "---"
{
    echo "## Port Definitions" >> "$AUDIT_REPORT"
    echo "" >> "$AUDIT_REPORT"
    
    PORTS_DIR="$CORE_PATH/infrastructure/ports"
    if [ -d "$PORTS_DIR" ]; then
        PORT_FILES=$(find "$PORTS_DIR" -name "*.py" -type f | wc -l)
        echo "✅ Ports directory exists with $PORT_FILES files"
        echo "✅ Ports directory exists with $PORT_FILES files" >> "$AUDIT_REPORT"
        
        # Check that ports are ABCs
        ABC_COUNT=$(grep -l "ABC\|@abstractmethod" "$PORTS_DIR"/*.py 2>/dev/null | wc -l)
        if [ "$ABC_COUNT" -gt 0 ]; then
            echo "✅ Found $ABC_COUNT port files with ABC/abstractmethod"
            echo "✅ Found $ABC_COUNT port files with ABC/abstractmethod" >> "$AUDIT_REPORT"
        else
            echo "⚠️ Some ports may not use ABC properly"
        fi
    else
        echo "❌ No ports directory found"
        echo "❌ No ports directory found" >> "$AUDIT_REPORT"
    fi
} | tee -a "$AUDIT_REPORT"
echo ""

# ============ COMPLIANCE CHECK 5: ENTITY COUNT ============
echo "📊 Check 5: Entity & Service Consolidation"
echo "---"
{
    echo "## Consolidation Metrics" >> "$AUDIT_REPORT"
    echo "" >> "$AUDIT_REPORT"
    
    ENTITY_FILES=$(find "$CORE_PATH/domain/entities" -name "*.py" | wc -l)
    SERVICE_FILES=$(find "$CORE_PATH/application/services" -name "*.py" | wc -l)
    MODEL_FILES=$(find "$CORE_PATH/infrastructure/models" -name "*.py" | wc -l)
    
    echo "Domain entities: $ENTITY_FILES files"
    echo "Application services: $SERVICE_FILES files"
    echo "Data models: $MODEL_FILES files"
    echo ""
    echo "| Layer | File Count |" >> "$AUDIT_REPORT"
    echo "|-------|------------|" >> "$AUDIT_REPORT"
    echo "| Domain Entities | $ENTITY_FILES |" >> "$AUDIT_REPORT"
    echo "| Application Services | $SERVICE_FILES |" >> "$AUDIT_REPORT"
    echo "| Infrastructure Models | $MODEL_FILES |" >> "$AUDIT_REPORT"
    echo "" >> "$AUDIT_REPORT"
} | tee -a "$AUDIT_REPORT"
echo ""

# ============ COMPLIANCE CHECK 6: CODE QUALITY ============
echo "📈 Check 6: Basic Code Quality"
echo "---"
{
    echo "## Code Quality" >> "$AUDIT_REPORT"
    echo "" >> "$AUDIT_REPORT"
    
    # Check for syntax errors
    if command -v python3 &> /dev/null; then
        SYNTAX_ERRORS=0
        find "$CORE_PATH" -name "*.py" -type f | while read file; do
            python3 -m py_compile "$file" 2>/dev/null || SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
        done
        
        if [ "$SYNTAX_ERRORS" -eq 0 ]; then
            echo "✅ No syntax errors in Python files"
            echo "✅ No syntax errors in Python files" >> "$AUDIT_REPORT"
        else
            echo "❌ Found $SYNTAX_ERRORS files with syntax errors"
        fi
    fi
} | tee -a "$AUDIT_REPORT"
echo ""

# ============ SUMMARY ============
echo "=========================================="
echo "Audit Report Generated"
echo "=========================================="
echo ""
echo "Full report: $AUDIT_REPORT"
echo ""

# Print summary to stdout
cat "$AUDIT_REPORT"

echo ""
echo "📊 Visual Conformance Summary"
echo "---"
echo "If all checks ✅ above,"
echo "Module is READY for deployment"
echo ""
