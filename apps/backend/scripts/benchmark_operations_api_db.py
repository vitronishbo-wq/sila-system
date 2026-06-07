#!/usr/bin/env python3
"""Run API+DB benchmark for operational flow and persist latency/error report."""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import httpx
from fastapi import FastAPI, Request

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from apps.backend.app.api.deps import get_identity_context  # noqa: E402

from apps.backend.app.core.identity import IdentityContext  # noqa: E402
from apps.backend.app.modules.intelligence.operations.api.router import (  # noqa: E402
    router as operations_router,
)


@dataclass
class EndpointStats:
    latencies_ms: list[float] = field(default_factory=list)
    count: int = 0
    errors: int = 0

    def add(self, latency_ms: float, ok: bool) -> None:
        self.count += 1
        self.latencies_ms.append(latency_ms)
        if not ok:
            self.errors += 1


class BenchmarkMetrics:
    def __init__(self) -> None:
        self.endpoints: dict[str, EndpointStats] = defaultdict(EndpointStats)

    def record(self, endpoint: str, latency_ms: float, ok: bool) -> None:
        self.endpoints[endpoint].add(latency_ms, ok)

    @staticmethod
    def _percentile(values: list[float], q: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        if len(ordered) == 1:
            return ordered[0]
        idx = (len(ordered) - 1) * q
        lo = math.floor(idx)
        hi = math.ceil(idx)
        if lo == hi:
            return ordered[lo]
        return ordered[lo] + (ordered[hi] - ordered[lo]) * (idx - lo)

    def serialize(self) -> dict:
        payload: dict[str, dict] = {}
        for endpoint, stats in sorted(self.endpoints.items()):
            lat = stats.latencies_ms
            payload[endpoint] = {
                "count": stats.count,
                "errors": stats.errors,
                "error_rate": (stats.errors / stats.count) if stats.count else 0.0,
                "latency_ms": {
                    "min": min(lat) if lat else 0.0,
                    "avg": (sum(lat) / len(lat)) if lat else 0.0,
                    "p50": self._percentile(lat, 0.50),
                    "p95": self._percentile(lat, 0.95),
                    "p99": self._percentile(lat, 0.99),
                    "max": max(lat) if lat else 0.0,
                },
            }
        return payload

    def total_errors(self) -> int:
        return sum(item.errors for item in self.endpoints.values())


async def _benchmark_identity_context(request: Request) -> IdentityContext:
    raw = request.headers.get("x-citizen-id")
    citizen_id = str(raw) if raw else str(uuid4())
    return IdentityContext(
        {
            "citizen_id": citizen_id,
            "user_id": citizen_id,
            "email": f"{citizen_id}@benchmark.local",
            "roles": ["CITIZEN"],
        }
    )


async def _request(
    client: httpx.AsyncClient,
    metrics: BenchmarkMetrics,
    endpoint: str,
    method: str,
    path: str,
    headers: dict[str, str] | None = None,
    payload: dict | None = None,
) -> httpx.Response:
    start = time.perf_counter()
    try:
        response = await client.request(method, path, headers=headers, json=payload)
        ok = 200 <= response.status_code < 300
        metrics.record(endpoint, (time.perf_counter() - start) * 1000.0, ok)
        return response
    except Exception:
        metrics.record(endpoint, (time.perf_counter() - start) * 1000.0, False)
        raise


async def _load_order_flow(
    client: httpx.AsyncClient,
    metrics: BenchmarkMetrics,
    service_id: str,
    citizen_id: UUID,
) -> tuple[bool, str | None]:
    headers = {"x-citizen-id": str(citizen_id)}

    order_response = await _request(
        client=client,
        metrics=metrics,
        endpoint="POST /api/v1/orders",
        method="POST",
        path="/api/v1/orders",
        headers=headers,
        payload={"service_id": service_id},
    )
    if order_response.status_code >= 300:
        return False, None
    order_id = order_response.json()["id"]

    docs_response = await _request(
        client=client,
        metrics=metrics,
        endpoint="POST /api/v1/orders/{order_id}/documents",
        method="POST",
        path=f"/api/v1/orders/{order_id}/documents",
        headers=headers,
        payload={
            "documents": [
                {
                    "filename": "bi.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 2048,
                    "uri": f"s3://bench/{order_id}/bi.pdf",
                }
            ]
        },
    )
    if docs_response.status_code >= 300:
        return False, None

    submit_response = await _request(
        client=client,
        metrics=metrics,
        endpoint="POST /api/v1/orders/{order_id}/submit",
        method="POST",
        path=f"/api/v1/orders/{order_id}/submit",
        headers=headers,
    )
    if submit_response.status_code >= 300:
        return False, None

    payment_response = await _request(
        client=client,
        metrics=metrics,
        endpoint="POST /api/v1/payments/{order_id}/generate",
        method="POST",
        path=f"/api/v1/payments/{order_id}/generate",
        headers=headers,
    )
    if payment_response.status_code >= 300:
        return False, None

    reference = payment_response.json()["reference"]
    return True, reference


async def run_benchmark(
    orders: int,
    concurrency: int,
    workers: int,
    confirms_per_worker: int,
    output: Path,
    strict: bool,
) -> int:
    benchmark_app = FastAPI(title="Operational Benchmark API")
    benchmark_app.include_router(operations_router, prefix="/api/v1")
    benchmark_app.dependency_overrides[get_identity_context] = _benchmark_identity_context
    metrics = BenchmarkMetrics()
    started = datetime.now(UTC)
    successful_orders = 0
    reference_for_contention: str | None = None

    try:
        transport = httpx.ASGITransport(app=benchmark_app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://benchmark.local"
        ) as client:
            services_response = await _request(
                client=client,
                metrics=metrics,
                endpoint="GET /api/v1/services",
                method="GET",
                path="/api/v1/services",
            )
            if services_response.status_code >= 300:
                raise RuntimeError(
                    f"Unable to load service catalog: {services_response.status_code}"
                )

            services = services_response.json()
            if not services:
                raise RuntimeError("No services available in catalog.")
            service_id = services[0]["id"]

            semaphore = asyncio.Semaphore(concurrency)

            async def _run_order(index: int) -> tuple[bool, str | None]:
                async with semaphore:
                    citizen_id = uuid4()
                    try:
                        return await _load_order_flow(
                            client=client,
                            metrics=metrics,
                            service_id=service_id,
                            citizen_id=citizen_id,
                        )
                    except Exception:
                        return False, None

            order_results = await asyncio.gather(*(_run_order(i) for i in range(orders)))
            for ok, ref in order_results:
                if ok:
                    successful_orders += 1
                    if reference_for_contention is None and ref:
                        reference_for_contention = ref

            if reference_for_contention:

                async def _worker() -> int:
                    worker_errors = 0
                    async with httpx.AsyncClient(
                        transport=httpx.ASGITransport(app=benchmark_app),
                        base_url="http://benchmark.local",
                    ) as worker_client:
                        for _ in range(confirms_per_worker):
                            response = await _request(
                                client=worker_client,
                                metrics=metrics,
                                endpoint="POST /api/v1/payments/{reference}/confirm [contention]",
                                method="POST",
                                path=f"/api/v1/payments/{reference_for_contention}/confirm",
                                headers={"x-citizen-id": str(uuid4())},
                            )
                            if response.status_code >= 300:
                                worker_errors += 1
                    return worker_errors

                contention_errors = await asyncio.gather(*(_worker() for _ in range(workers)))
                if sum(contention_errors) > 0:
                    print(f"[WARN] contention confirmation errors={sum(contention_errors)}")

    finally:
        benchmark_app.dependency_overrides.pop(get_identity_context, None)

    completed = datetime.now(UTC)
    report = {
        "started_at": started.isoformat(),
        "completed_at": completed.isoformat(),
        "duration_seconds": (completed - started).total_seconds(),
        "config": {
            "orders": orders,
            "concurrency": concurrency,
            "confirm_workers": workers,
            "confirm_requests_per_worker": confirms_per_worker,
        },
        "summary": {
            "successful_orders": successful_orders,
            "failed_orders": max(orders - successful_orders, 0),
            "total_errors": metrics.total_errors(),
        },
        "endpoints": metrics.serialize(),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Benchmark report written: {output}")
    print(
        "summary "
        f"orders_ok={report['summary']['successful_orders']} "
        f"orders_failed={report['summary']['failed_orders']} "
        f"errors={report['summary']['total_errors']}"
    )
    if strict and (report["summary"]["failed_orders"] > 0 or report["summary"]["total_errors"] > 0):
        return 1
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark operational flow API+DB.")
    parser.add_argument("--orders", type=int, default=int(os.getenv("LOAD_ORDERS", "1000")))
    parser.add_argument(
        "--concurrency", type=int, default=int(os.getenv("LOAD_CONCURRENCY", "120"))
    )
    parser.add_argument(
        "--confirm-workers", type=int, default=int(os.getenv("LOAD_CONFIRM_WORKERS", "16"))
    )
    parser.add_argument(
        "--confirm-requests-per-worker",
        type=int,
        default=int(os.getenv("LOAD_CONFIRM_REQUESTS_PER_WORKER", "25")),
    )
    parser.add_argument(
        "--strict", action="store_true", help="Exit with code 1 on failed requests."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT
        / "apps"
        / "backend"
        / "report"
        / f"operations_api_db_benchmark_{datetime.now(UTC):%Y%m%d_%H%M%S}.json",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    return asyncio.run(
        run_benchmark(
            orders=args.orders,
            concurrency=args.concurrency,
            workers=args.confirm_workers,
            confirms_per_worker=args.confirm_requests_per_worker,
            output=args.output,
            strict=args.strict,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
