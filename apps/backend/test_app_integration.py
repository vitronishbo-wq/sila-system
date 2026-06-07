#!/usr/bin/env python
"""Test FastAPI app integration with event routes."""

import asyncio
import sys

sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")


async def test_integration():
    try:
        from main import app

        print("✓ FastAPI app loaded successfully")

        # Check that routes are registered
        route_paths = [route.path for route in app.routes]
        event_routes = [p for p in route_paths if "events" in p]

        print(f"✓ Found {len(event_routes)} event routes:")
        for route in event_routes:
            print(f"  - {route}")

        if len(event_routes) < 5:
            print("✗ Not all event routes are registered!")
            return False

        print("✓ All event routes registered successfully")
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_integration())
    sys.exit(0 if result else 1)
