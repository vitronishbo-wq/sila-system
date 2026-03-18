"""Real API+DB load tests for operational flow.

Opt-in execution:
  RUN_LOAD_TESTS=1 RUN_DB_LOAD_TESTS=1 pytest -q --noconftest apps/backend/tests/load/test_operations_load.py
"""

from __future__ import annotations

import asyncio
import os
from uuid import UUID, uuid4

import httpx
import pytest
from fastapi import FastAPI
from fastapi import Request

from app.api.deps import get_identity_context
from apps.backend.app.core.identity import IdentityContext
from apps.backend.app.modules.intelligence.operations.api.router import router as operations_router


pytestmark = pytest.mark.load


def _load_enabled() -> bool:
    return os.getenv("RUN_LOAD_TESTS", "0") == "1" and os.getenv("RUN_DB_LOAD_TESTS", "0") == "1"


def _build_benchmark_app() -> FastAPI:
    benchmark_app = FastAPI(title="Operational Load Test API")
    benchmark_app.include_router(operations_router, prefix="/api/v1")
    return benchmark_app


async def _identity_override(request: Request) -> IdentityContext:
    raw = request.headers.get("x-citizen-id")
    citizen_id = str(raw) if raw else str(uuid4())
    return IdentityContext(
        {
            "citizen_id": citizen_id,
            "user_id": citizen_id,
            "email": f"{citizen_id}@load.local",
            "roles": ["CITIZEN"],
        }
    )


async def _get_first_service_id(client: httpx.AsyncClient) -> str:
    response = await client.get("/api/v1/services")
    assert response.status_code == 200, response.text
    services = response.json()
    assert services, "Service catalog is empty"
    return services[0]["id"]


async def _create_order_flow(client: httpx.AsyncClient, service_id: str, citizen_id: UUID) -> tuple[str, str]:
    headers = {"x-citizen-id": str(citizen_id)}

    order_response = await client.post("/api/v1/orders", json={"service_id": service_id}, headers=headers)
    assert order_response.status_code == 201, order_response.text
    order_id = order_response.json()["id"]

    docs_response = await client.post(
        f"/api/v1/orders/{order_id}/documents",
        json={
            "documents": [
                {
                    "filename": "bench-bi.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 4096,
                    "uri": f"s3://load/{order_id}/bench-bi.pdf",
                }
            ]
        },
        headers=headers,
    )
    assert docs_response.status_code == 200, docs_response.text

    submit_response = await client.post(f"/api/v1/orders/{order_id}/submit", headers=headers)
    assert submit_response.status_code == 200, submit_response.text

    payment_response = await client.post(f"/api/v1/payments/{order_id}/generate", headers=headers)
    assert payment_response.status_code == 200, payment_response.text
    reference = payment_response.json()["reference"]
    return order_id, reference


@pytest.mark.asyncio
@pytest.mark.skipif(not _load_enabled(), reason="Set RUN_LOAD_TESTS=1 and RUN_DB_LOAD_TESTS=1")
async def test_create_10k_orders_via_real_api_db():
    orders = int(os.getenv("LOAD_ORDERS", "10000"))
    concurrency = int(os.getenv("LOAD_CONCURRENCY", "150"))

    app = _build_benchmark_app()
    app.dependency_overrides[get_identity_context] = _identity_override
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://load.local",
            timeout=60.0,
        ) as client:
            service_id = await _get_first_service_id(client)
            semaphore = asyncio.Semaphore(concurrency)

            async def _run_one(index: int) -> bool:
                async with semaphore:
                    citizen_id = uuid4()
                    order_id, reference = await _create_order_flow(client, service_id, citizen_id)
                    return bool(order_id and reference)

            results = await asyncio.gather(*(_run_one(i) for i in range(orders)))
            assert all(results)
            assert len(results) == orders
    finally:
        app.dependency_overrides.pop(get_identity_context, None)


@pytest.mark.asyncio
@pytest.mark.skipif(not _load_enabled(), reason="Set RUN_LOAD_TESTS=1 and RUN_DB_LOAD_TESTS=1")
async def test_confirm_payment_contention_multi_worker_real_db_lock():
    workers = int(os.getenv("LOAD_CONFIRM_WORKERS", "16"))
    requests_per_worker = int(os.getenv("LOAD_CONFIRM_REQUESTS_PER_WORKER", "25"))

    app = _build_benchmark_app()
    app.dependency_overrides[get_identity_context] = _identity_override
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://load.local",
            timeout=60.0,
        ) as client:
            service_id = await _get_first_service_id(client)
            citizen_id = uuid4()
            order_id, reference = await _create_order_flow(client, service_id, citizen_id)

        async def _worker() -> int:
            success = 0
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="http://load.local",
                timeout=60.0,
            ) as worker_client:
                for _ in range(requests_per_worker):
                    response = await worker_client.post(
                        f"/api/v1/payments/{reference}/confirm",
                        headers={"x-citizen-id": str(uuid4())},
                    )
                    if response.status_code == 200 and response.json().get("status") == "CONFIRMED":
                        success += 1
            return success

        worker_results = await asyncio.gather(*(_worker() for _ in range(workers)))
        assert sum(worker_results) == workers * requests_per_worker

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://load.local",
            timeout=60.0,
        ) as client:
            order_response = await client.get(
                f"/api/v1/orders/{order_id}",
                headers={"x-citizen-id": str(citizen_id)},
            )
            assert order_response.status_code == 200, order_response.text
            payload = order_response.json()
            paid_transitions = [h for h in payload.get("status_history", []) if h.get("to") == "PAID"]
            assert len(paid_transitions) == 1, payload.get("status_history")
    finally:
        app.dependency_overrides.pop(get_identity_context, None)
