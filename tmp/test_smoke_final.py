"""Run initial smoke test after fixes"""
import sys, os
sys.path.insert(0, '/home/dev03wsl/sila-system')
sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.environ['ENV_MODE'] = 'host'
os.environ['GMX_ENV_LOADED'] = '1'

from fastapi.testclient import TestClient
from apps.backend.app.main import create_app

app = create_app()
client = TestClient(app)

tests = [
    ("GET", "/"),
    ("GET", "/api/health/live"),
    ("GET", "/api/health/ready"),
    ("GET", "/api/providers/health"),
    ("GET", "/api/providers/metrics"),
    ("GET", "/society/assistencia_social/assistencia-social/beneficiarios/"),
    ("GET", "/society/assistencia_social/assistencia-social/beneficios/"),
    ("GET", "/educacao/marketplace/search/search/health"),
]

passed = 0
failed = 0
for method, path in tests:
    try:
        r = client.request(method, path)
        if r.status_code < 500:
            print(f"  OK  {r.status_code} {path}")
            passed += 1
        else:
            print(f"  FAIL {r.status_code} {path}")
            failed += 1
    except Exception as e:
        print(f"  ERROR {path}: {e}")
        failed += 1

print(f"\nResultado: {passed}/{len(tests)} OK, {failed} FAIL")
