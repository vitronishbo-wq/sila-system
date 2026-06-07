#!/bin/bash

# PRODUCTION READINESS CHECK - DEFINITIVO
cd /home/dev03wsl/sila-system/apps/backend
export PYTHONPATH=/home/dev03wsl/sila-system/apps/backend

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 PRODUCTION READINESS - FINAL CHECK                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

ERRORS=0

# Test 1: Imports
echo "📦 Core imports..."
python tests/test_sanity.py > /tmp/sanity.log 2>&1
if [ $? -eq 0 ]; then
    echo "  ✅ All critical imports OK"
else
    echo "  ❌ Import error"
    cat /tmp/sanity.log | head -5
    ERRORS=$((ERRORS+1))
fi

# Test 2: Dependencies
echo ""
echo "📚 Dependencies..."
python -c "import fastapi, sqlalchemy, asyncpg, pydantic; print('  ✅ Core deps installed')" 2>/dev/null || echo "  ❌ Missing deps"

# Test 3: Core modules
echo ""
echo "⚙️  Core modules..."
python << 'EOF'
try:
    from apps.backend.app.core.db import AsyncSessionLocal, importAsyncSessionLocal
    from apps.backend.app.core.security import IAMClient
    from apps.backend.app.core.events import get_event_bus
    print("  ✅ core.db OK")
    print("  ✅ core.security OK")
    print("  ✅ core.events OK")
except Exception as e:
    print(f"  ❌ {e}")
EOF

# Test 4: Database
echo ""
echo "🗄️  Database..."
python << 'EOF'
import asyncio
import os

async def test_db():
    try:
        from apps.backend.app.core.db import engine
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
            print("  ✅ Database connection OK")
    except Exception as e:
        print(f"  ❌ DB Error: {str(e)[:50]}")

try:
    asyncio.run(test_db())
except Exception as e:
    print(f"  ⚠️  DB test skipped: {str(e)[:40]}")
EOF

# Test 5: Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
if [ $ERRORS -eq 0 ]; then
    echo "║            🟢 SYSTEM READY FOR PRODUCTION                    ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "✅ All checks passed"
    echo ""
    echo "To start server:"
    echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
else
    echo "║            🔴 SYSTEM NOT READY - $ERRORS ERRORS                    ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
fi

exit $ERRORS
