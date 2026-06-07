#!/usr/bin/env bash
################################################################################
# POST-MUTATION PIPELINE (Self-Healing Code Agent)
# Executa após qualquer alteração no código:
# 1. ruff check . --fix
# 2. black .
# 3. pytest
################################################################################

set -e  # Exit on error

BACKEND_DIR="${BACKEND_DIR:-apps/backend}"
LOG_FILE="post-mutation-pipeline.log"

echo "🔧 POST-MUTATION PIPELINE STARTED" | tee -a "$LOG_FILE"
echo "📅 $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ============================================================================
# STEP 1: RUFF FIX (Auto-remediate linter issues)
# ============================================================================
echo "📝 [STEP 1/3] Running ruff fix..." | tee -a "$LOG_FILE"
if cd "$BACKEND_DIR" && python -m ruff check . --fix 2>&1 | tee -a "$LOG_FILE"; then
    echo "✅ ruff fix completed" | tee -a "$LOG_FILE"
else
    echo "⚠️  ruff fix had issues (non-fatal, continuing)" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# ============================================================================
# STEP 2: BLACK FORMAT (Code formatting)
# ============================================================================
echo "🎨 [STEP 2/3] Running black..." | tee -a "$LOG_FILE"
if python -m black . --quiet 2>&1 | tee -a "$LOG_FILE"; then
    echo "✅ black formatter completed" | tee -a "$LOG_FILE"
else
    echo "⚠️  black had issues (non-fatal, continuing)" | tee -a "$LOG_FILE"
fi
echo "" | tee -a "$LOG_FILE"

# ============================================================================
# STEP 3: PYTEST (Unit & Integration Tests)
# ============================================================================
echo "🧪 [STEP 3/3] Running pytest..." | tee -a "$LOG_FILE"
if python -m pytest -v --tb=short 2>&1 | tee -a "$LOG_FILE"; then
    echo "✅ pytest passed" | tee -a "$LOG_FILE"
    EXIT_CODE=0
else
    echo "❌ pytest failed (test suite validation required)" | tee -a "$LOG_FILE"
    EXIT_CODE=1
fi
echo "" | tee -a "$LOG_FILE"

# ============================================================================
# SUMMARY
# ============================================================================
echo "📊 PIPELINE SUMMARY" | tee -a "$LOG_FILE"
echo "==================" | tee -a "$LOG_FILE"
echo "✅ ruff fix:     Completed" | tee -a "$LOG_FILE"
echo "✅ black:        Completed" | tee -a "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ pytest:       Passed" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    echo "🎉 POST-MUTATION PIPELINE: SUCCESS" | tee -a "$LOG_FILE"
else
    echo "❌ pytest:       Failed" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    echo "⚠️  POST-MUTATION PIPELINE: NEEDS REVIEW" | tee -a "$LOG_FILE"
fi

echo "📅 $(date)" >> "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

exit $EXIT_CODE
