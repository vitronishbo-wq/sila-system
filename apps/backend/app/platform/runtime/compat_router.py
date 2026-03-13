from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Response, status
from pydantic import BaseModel, Field

from app.api.deps import get_current_user

router = APIRouter()

# In-memory stores for lightweight E2E flows
_SERVICES: list[dict[str, Any]] = [
    {
        "id": "svc-bi-001",
        "code": "BI_EMISSAO",
        "name": "Emissao de BI",
        "price": 1000.0,
    }
]
_ORDERS: dict[str, dict[str, Any]] = {}
_PAYMENTS: dict[str, dict[str, Any]] = {}
_PING_MODULES = {
    "urbanism",
    "justice",
    "commercial",
    "education",
    "address",
    "registry",
    "reports",
    "identity",
    "social",
    "common",
    "governance",
    "journeys",
    "services",
    "training",
    "internal",
}


class OrderCreatePayload(BaseModel):
    service_id: str = Field(..., min_length=1)


class DocumentPayload(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    uri: str


class DocumentsPayload(BaseModel):
    documents: list[DocumentPayload]


class BIEmitPayload(BaseModel):
    citizen_fuc_id: str


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "SILA Backend online"}


@router.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "service": "SILA-System",
        "version": "20.2",
        "environment": "development",
        "timestamp": time.time(),
        "database": "local",
    }


@router.options("/health")
def health_options() -> Response:
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "access-control-allow-origin": "*",
            "access-control-allow-methods": "GET,OPTIONS",
            "access-control-allow-headers": "*",
        },
    )


@router.get("/info")
def info() -> dict[str, Any]:
    return {
        "system": {
            "name": "SILA",
            "environment": "development",
            "debug": True,
            "version": "20.2",
        },
        "database": {
            "host": "localhost",
            "database": "sila_db",
        },
        "features": {
            "event_sourcing": True,
            "trust_engine": True,
            "catalog": True,
        },
    }


@router.get("/api/auth/me")
async def auth_me(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return current_user


@router.get("/api/v1/identidade/bi/tipos-evento")
def bi_event_types() -> list[dict[str, str]]:
    return [
        {"code": "EMISSAO", "label": "Emissao"},
        {"code": "RENOVACAO", "label": "Renovacao"},
        {"code": "SEGUNDA_VIA", "label": "Segunda Via"},
    ]


@router.post("/api/v1/identidade/bi/emit")
def bi_emit(
    payload: BIEmitPayload,
    authorization: str | None = Header(default=None),
    x_token: str | None = Header(default=None, alias="X-Token"),
) -> dict[str, Any]:
    if not authorization and not x_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    return {
        "status": "queued",
        "request_id": str(uuid.uuid4()),
        "citizen_fuc_id": payload.citizen_fuc_id,
    }


@router.get("/api/v1/services")
def list_services() -> list[dict[str, Any]]:
    return _SERVICES


@router.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreatePayload) -> dict[str, Any]:
    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "service_id": payload.service_id,
        "status": "created",
    }
    _ORDERS[order_id] = order
    return order


@router.post("/api/v1/orders/{order_id}/documents")
def attach_documents(order_id: str, payload: DocumentsPayload) -> dict[str, Any]:
    order = _ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    order["documents"] = [doc.model_dump() for doc in payload.documents]
    return {"status": "ok", "order_id": order_id}


@router.post("/api/v1/orders/{order_id}/submit")
def submit_order(order_id: str) -> dict[str, Any]:
    order = _ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    order["status"] = "submitted"
    return {"status": "submitted", "order_id": order_id}


@router.post("/api/v1/payments/{order_id}/generate")
def generate_payment(order_id: str) -> dict[str, Any]:
    order = _ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"
    payment = {"reference": reference, "order_id": order_id, "status": "PENDING"}
    _PAYMENTS[reference] = payment
    return payment


@router.post("/api/v1/payments/{reference}/confirm")
def confirm_payment(reference: str) -> dict[str, Any]:
    payment = _PAYMENTS.get(reference)
    if not payment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid reference")
    payment["status"] = "CONFIRMED"
    return {"reference": reference, "status": payment["status"]}


@router.post("/api/v1/orders/{order_id}/complete")
def complete_order(order_id: str) -> dict[str, Any]:
    order = _ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="order not found")
    order["status"] = "completed"
    return {"status": "completed", "order_id": order_id}


@router.get("/api/v1/orders/{order_id}/receipt")
def get_receipt(order_id: str) -> dict[str, Any]:
    order = _ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return {
        "order_id": order_id,
        "status": "issued",
        "items": order.get("documents", []),
    }


@router.get("/api/v1/{module}/ping")
def module_ping(module: str) -> dict[str, str]:
    if module not in _PING_MODULES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="module not found")
    return {
        "status": "success",
        "message": "pong",
        "module": module,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
