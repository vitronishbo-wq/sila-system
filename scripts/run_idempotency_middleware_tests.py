#!/usr/bin/env python3
import asyncio
import importlib.util
import sys
from pathlib import Path

TEST_PATH = Path(__file__).resolve().parent.parent / "apps" / "backend" / "app" / "core" / "tests" / "test_idempotency_middleware.py"

spec = importlib.util.spec_from_file_location("idm_test", str(TEST_PATH))
mod = importlib.util.module_from_spec(spec)
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
BACKEND_APPS = REPO_ROOT / "apps" / "backend"
if str(BACKEND_APPS) not in sys.path:
    sys.path.insert(0, str(BACKEND_APPS))

spec.loader.exec_module(mod)

async def run_all():
    results = []
    for name in dir(mod):
        if name.startswith("test_"):
            func = getattr(mod, name)
            try:
                if asyncio.iscoroutinefunction(func):
                    await func()
                else:
                    func()
                print(f"PASS: {name}")
                results.append((name, True, None))
            except Exception as e:
                print(f"FAIL: {name} -> {e}")
                results.append((name, False, e))
    failed = [r for r in results if not r[1]]
    if failed:
        print(f"{len(failed)} test(s) failed")
        sys.exit(1)
    print("All tests passed")

if __name__ == '__main__':
    asyncio.run(run_all())
