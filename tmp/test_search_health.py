"""Test creating the search router and calling health directly."""
import sys, os
sys.path.insert(0, '/home/dev03wsl/sila-system')
sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.environ['ENV_MODE'] = 'host'

from fastapi.testclient import TestClient

# Build the app with only the search router
from apps.backend.app.modules.educacao.marketplace.search.api.router import router as search_router
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class PassThroughMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        import time
        print(f"MW: {request.method} {request.url.path}")
        try:
            response = await call_next(request)
            print(f"MW result: {response.status_code}")
            return response
        except Exception as e:
            import traceback
            print(f"MW ERROR: {e}")
            traceback.print_exc()
            raise

app.add_middleware(PassThroughMiddleware)
app.include_router(search_router)

client = TestClient(app)

# Try health
r = client.get("/search/health")
print(f"GET /search/health: STATUS={r.status_code}, BODY={r.text[:200]}")
print(f"  HEADERS={dict(r.headers)}")

# Try root
r = client.get("/search/")
print(f"GET /search/: STATUS={r.status_code}, BODY={r.text[:200]}")
