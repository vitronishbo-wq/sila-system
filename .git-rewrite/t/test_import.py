#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/truman/dev/sila-system/apps/backend')

try:
    from modules.auth.endpoints.router import router
    print("✅ Router import OK")
    print(f"Routes: {len(router.routes)}")
    for route in router.routes:
        print(f"  - {route.path} ({route.methods})")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
