#!/bin/bash

# 🚀 SILA System - WSL2 Deployment Script
# This script initializes and starts the SILA System for WSL2 deployment

set -e

PROJECT_ROOT="/home/dev03wsl/sila-system"
BACKEND_DIR="$PROJECT_ROOT/apps/backend"
VENV="$PROJECT_ROOT/.venv"

echo "================================================================"
echo "🚀 SILA SYSTEM - WSL2 DEPLOYMENT INITIALIZATION"
echo "================================================================"

# 1. Verify Python environment
echo ""
echo "📦 Verifying Python environment..."
if [ ! -d "$VENV" ]; then
    echo "❌ Virtual environment not found at $VENV"
    exit 1
fi

PYTHON="$VENV/bin/python"
$PYTHON --version

# 2. Test app import
echo ""
echo "🔍 Testing app import..."
$PYTHON -c "import sys; sys.path.insert(0, '$BACKEND_DIR'); from app.main import app; print('✅ App imports successfully')" || {
    echo "❌ App import failed"
    exit 1
}

# 3. Optionally run sanity checks via pytest
echo ""
echo "🧪 Running basic sanity tests..."
cd "$PROJECT_ROOT"
# use pytest to run selected readiness tests instead of deprecated script
$PYTHON -m pytest tests/test_database_integrity.py -q || {
    echo "❌ Readiness tests failed"
    exit 1
}

echo ""
echo "================================================================"
echo "✅ DEPLOYMENT INITIALIZATION COMPLETE!"
echo "================================================================"
echo ""
echo "To start the SILA System, run:"
echo ""
echo "  cd $BACKEND_DIR"
echo "  $PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "Then access:"
echo "  - API: http://localhost:8000"
echo "  - Swagger Docs: http://localhost:8000/docs"
echo ""
echo "📝 For more information, see: $PROJECT_ROOT/DEPLOYMENT_READY.md"
echo ""
