#!/usr/bin/env python
import sys

sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")

try:
    from apps.backend.app.api.routers.events import router

    print("✓ Router imported successfully")
    print(f"✓ Router has {len(router.routes)} routes")
    for route in router.routes:
        print(f"  - {route.path} ({route.methods})")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
