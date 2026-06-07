"""Test EMIS endpoints after governance fix."""
import sys
sys.path.insert(0, ".")

from apps.backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test EMIS health
r = client.get("/emis/health")
print(f"GET /emis/health: {r.status_code} {r.json()['status']}")

# Test EMIS stats
r = client.get("/emis/stats")
print(f"GET /emis/stats: {r.status_code}")
if r.status_code == 200:
    print(f"  {r.json()}")
else:
    print(f"  ERROR: {r.text[:200]}")

# Test EMIS logs
r = client.get("/emis/logs")
print(f"GET /emis/logs: {r.status_code}")
if r.status_code == 200:
    print(f"  count={len(r.json())}")
else:
    print(f"  ERROR: {r.text[:200]}")

# OpenAPI count
r = client.get("/openapi.json")
paths = r.json().get("paths", {})
emis_count = len([p for p in paths if "/emis/" in p or p.endswith("/emis")])
print(f"\nOpenAPI: {len(paths)} total, {emis_count} EMIS")
