#!/bin/bash
cd /home/truman/dev/sila-system/apps/backend
source .venv/bin/activate

# Test import
echo "Testing imports..."
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from main import app
    print("✅ Main app imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
EOF

echo "Starting server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
