#!/usr/bin/env python3
"""Smoke test: Verify SILA 3.0 imports and structure."""

import sys
import os

# Add apps/backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'apps/backend'))

try:
    from app.main import app
    print("✓ SILA 3.0 Online - Trust Engine Active")
    print(f"✓ App title: {app.title}")
    print(f"✓ Version: {app.version}")
    print(f"✓ Middleware registered: {len(app.user_middleware)}")
    print(f"✓ Routes registered: {len([r for r in app.routes])}")
    
    # List registered routes
    routes = [r.path for r in app.routes if hasattr(r, 'path')]
    print(f"\n✓ Registered endpoints: {len(routes)}")
    for route in sorted(set(routes))[:10]:
        print(f"  - {route}")
    
    print("\n✓ Clean State validation PASSED")
    
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
