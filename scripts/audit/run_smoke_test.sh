#!/bin/bash
# Smoke test runner for SILA 3.0 Clean State

cd /home/dev03wsl/sila-system
export PYTHONPATH="/home/dev03wsl/sila-system/apps/backend:$PYTHONPATH"

echo "---"
echo "SMOKE TEST: SILA 3.0 Trust Engine Validation"
echo "---"

python3 smoke_test.py
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✓✓✓ CLEAN STATE Operation Successful ✓✓✓"
    exit 0
else
    echo ""
    echo "✗✗✗ CLEAN STATE Operation Failed ✗✗✗"
    exit 1
fi
