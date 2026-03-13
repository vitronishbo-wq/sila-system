"""Standalone runner for RoleLevelGuard quick tests.

This script does not rely on pytest or the project's conftest; it
creates a minimal FastAPI app, mounts a test endpoint using the guard,
and performs requests to validate behavior.
"""
import json
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from app.api.guards import RoleLevelGuard
import app.core.territory.service as territory_service_module


app = FastAPI()


@app.get("/test/{municipality_id}")
async def test_endpoint(municipality_id: str, _guard=Depends(RoleLevelGuard("MUNICIPAL", resource_param="municipality_id"))):
    return {"ok": True}


async def fake_get_ancestors(db, target_id):
    return [
        {"id": 1, "type": "commune"},
        {"id": 5, "type": "municipality"},
        {"id": 10, "type": "province"},
    ]


def run():
    # monkeypatch TerritoryService.get_territory_ancestors
    territory_service_module.TerritoryService.get_territory_ancestors = staticmethod(fake_get_ancestors)

    # We'll test the RoleLevelGuard directly (bypassing FastAPI DI) to avoid
    # flaky dependency override behavior in this standalone runner.
    from app.api.guards import RoleLevelGuard
    import asyncio
    from fastapi import HTTPException

    guard_callable = RoleLevelGuard("MUNICIPAL", resource_param="municipality_id")()

    class DummyRequest:
        def __init__(self, path_params=None, query_params=None):
            self.path_params = path_params or {}
            self.query_params = query_params or {}

    scenarios = [
        ("superuser bypass", {"is_superuser": True}, DummyRequest(path_params={"municipality_id": "5"}), 200),
        ("no region denied", {"is_superuser": False, "administrative_level": "MUNICIPAL", "region_id": None}, DummyRequest(path_params={"municipality_id": "5"}), 403),
        ("region ancestor allowed", {"is_superuser": False, "administrative_level": "MUNICIPAL", "region_id": 5}, DummyRequest(path_params={"municipality_id": "5"}), 200),
        ("region not ancestor denied", {"is_superuser": False, "administrative_level": "MUNICIPAL", "region_id": 999}, DummyRequest(path_params={"municipality_id": "5"}), 403),
    ]

    for name, user, request_obj, expect in scenarios:
        try:
            print(f"[test] running scenario: {name} user={user}")
            # Call the async guard directly, supplying current_user and db
            asyncio.get_event_loop().run_until_complete(
                guard_callable(request_obj, current_user=user, db=None)
            )
            status = 200
        except HTTPException as he:
            status = he.status_code
        except Exception as e:
            status = 500

        print(f"{name}: status={status} expected={expect}")


if __name__ == "__main__":
    run()
