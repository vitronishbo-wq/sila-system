#!/usr/bin/env python3
"""Validate that base.py can be imported after fixes"""

import sys
import os

# Set up paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'backend', 'app'))
os.chdir(os.path.join(os.path.dirname(__file__), 'apps', 'backend'))

try:
    from app.db.base import Base
    print('✅ app.db.base imports successfully')
    print(f'✅ Base Registry has {len(Base.metadata.tables)} tables')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
