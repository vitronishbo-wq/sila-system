from __future__ import annotations

import asyncio
import os
import sys
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

import asyncpg
from apps.backend.app.core.db import Base
from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSON, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

sys.modules.setdefault("apps.backend.app.core.bridges.compat", sys.modules[__name__])
# NOTE: keep legacy alias above to avoid import-time cycles.
from apps.backend.app.modules.justice.infrastructure.legacy_adapters.attestation_service_adapter import (  # noqa: E402
    AttestationServiceAdapter,
)
from apps.backend.app.modules.justice.infrastructure.legacy_adapters.certificate_service_adapter import (  # noqa: E402
    CertificateServiceAdapter,
)
from apps.backend.app.modules.justice.infrastructure.legacy_adapters.finances_service_adapter import (  # noqa: E402
    FinancesServiceAdapter,
)
from apps.backend.app.modules.justice.infrastructure.legacy_adapters.notification_service_adapter import (  # noqa: E402
    NotificationServiceAdapter,
)
from apps.backend.app.modules.justice.infrastructure.legacy_adapters.request_tracking_service_adapter import (  # noqa: E402
    RequestTrackingServiceAdapter,
)


class ProfileQueries:
    """Read-model helpers for profile dashboards."""

    @staticmethod
    def get_commune_dashboard(_db_session: Any, _commune_id: Any) -> dict[str, Any]:
        return {
            "perfil": "comuna",
            "pendentes": [],
            "metricas": {"total_ativos": 0, "media_tempo_resposta": 0, "taxa_resolucao": 0},
        }

    @staticmethod
    def get_escalated_to_municipality(_db_session: Any, _municipality_id: Any) -> list[Any]:
        return []

    @staticmethod
    def get_municipality_dashboard(_db_session: Any, _municipality_id: Any) -> dict[str, Any]:
        return {
            "perfil": "municipio",
            "performance_comunas": [],
            "metricas_consolidadas": {"total_pedidos_regiao": 0},
        }

    @staticmethod
    def get_critical_cases(_db_session: Any, _province_id: Any) -> list[Any]:
        return []


class RequestState(StrEnum):
    EM_ANALISE_COMUNAL = "EM_ANALISE_COMUNAL"
    EM_ANALISE_MUNICIPAL = "EM_ANALISE_MUNICIPAL"
    EM_ANALISE_PROVINCIAL = "EM_ANALISE_PROVINCIAL"
    EM_ANALISE_NACIONAL = "EM_ANALISE_NACIONAL"
    AGUARDANDO_DOCUMENTOS = "AGUARDANDO_DOCUMENTOS"
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    AGUARDANDO_REVISAO = "AGUARDANDO_REVISAO"
    RESOLVIDO = "RESOLVIDO"
    INDEFERIDO = "INDEFERIDO"
    CANCELADO = "CANCELADO"

    @staticmethod
    def initial_states() -> list[RequestState]:
        return [
            RequestState.EM_ANALISE_COMUNAL,
            RequestState.EM_ANALISE_MUNICIPAL,
            RequestState.EM_ANALISE_PROVINCIAL,
            RequestState.EM_ANALISE_NACIONAL,
        ]

    @staticmethod
    def terminal_states() -> list[RequestState]:
        return [RequestState.RESOLVIDO, RequestState.INDEFERIDO, RequestState.CANCELADO]

    @staticmethod
    def waiting_states() -> list[RequestState]:
        return [
            RequestState.AGUARDANDO_DOCUMENTOS,
            RequestState.AGUARDANDO_PAGAMENTO,
            RequestState.AGUARDANDO_REVISAO,
        ]


class RoutingRule(StrEnum):
    COMUNA_ONLY = "COMUNA_ONLY"
    MUNICIPIO_ONLY = "MUNICIPIO_ONLY"
    PROVINCIA_ONLY = "PROVINCIA_ONLY"
    COMUNA_ESCALABLE = "COMUNA_ESCALABLE"
    MUNICIPIO_ESCALABLE = "MUNICIPIO_ESCALABLE"


from apps.backend.app.modules.justice._deprecated.bounded_contexts.civil_registry_core.infrastructure.repositories.citizen_repository import (  # noqa: E402
    CitizenRepository,
)

_DEFAULT_OWNER_ID: int | None = None


def _resolve_default_owner_id() -> int:
    db_url = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db"
    )
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)

    async def _fetch() -> int | None:
        try:
            conn = await asyncpg.connect(db_url)
        except Exception:
            return None
        try:
            row = await conn.fetchrow("SELECT id FROM users ORDER BY id LIMIT 1")
            return row["id"] if row else None
        finally:
            await conn.close()

    try:
        owner_id = asyncio.run(_fetch())
    except RuntimeError:
        owner_id = None
    return owner_id or 1


def _get_default_owner_id() -> int:
    global _DEFAULT_OWNER_ID
    if _DEFAULT_OWNER_ID is None:
        _DEFAULT_OWNER_ID = _resolve_default_owner_id()
    return _DEFAULT_OWNER_ID


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"extend_existing": True}
    id: Mapped[Any] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, default=_get_default_owner_id)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, **kwargs):
        citizen_id = kwargs.pop("citizen_id", None)
        document_type = kwargs.pop("document_type", None)
        document_number = kwargs.pop("document_number", None)
        status = kwargs.pop("status", None)
        if "title" not in kwargs:
            kwargs["title"] = f"Document {document_number or ''}".strip()
        if "filename" not in kwargs:
            kwargs["filename"] = document_number or f"document-{uuid4().hex}"
        if "file_path" not in kwargs:
            kwargs["file_path"] = document_number or f"/tmp/{uuid4().hex}"
        if "file_type" not in kwargs:
            kwargs["file_type"] = document_type or "ID_CARD"
        if "file_size" not in kwargs:
            kwargs["file_size"] = 0
        if "owner_id" not in kwargs:
            kwargs["owner_id"] = _get_default_owner_id()
        if status is not None and "status" not in kwargs:
            kwargs["status"] = status
        super().__init__(**kwargs)
        if citizen_id is not None:
            self.citizen_id = citizen_id


from apps.backend.app.modules.economy.domain.models.enums import (  # noqa: E402
    InvoiceStatus,
    PaymentStatus,
)


class Invoice(Base):
    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reference: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    metadata_info: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(self, **kwargs):
        kwargs.pop("citizen_id", None)
        kwargs.pop("service_code", None)
        kwargs.pop("service_name", None)
        kwargs.pop("revenue_code", None)
        kwargs.pop("cost_center", None)
        kwargs.pop("due_date", None)
        kwargs.pop("request_id", None)
        if "id" in kwargs and (not isinstance(kwargs["id"], int)):
            kwargs.pop("id")
        if "reference" not in kwargs:
            kwargs["reference"] = f"INV-{uuid4().hex[:10].upper()}"
        if "amount" not in kwargs:
            kwargs["amount"] = 0
        if "currency" not in kwargs:
            kwargs["currency"] = "AOA"
        status = kwargs.get("status")
        if isinstance(status, InvoiceStatus):
            kwargs["status"] = status.value
        elif status is None:
            kwargs["status"] = InvoiceStatus.PENDING.value
        kwargs.setdefault("method", "INVOICE")
        now = datetime.utcnow()
        kwargs.setdefault("created_at", now)
        kwargs.setdefault("updated_at", now)
        super().__init__(**kwargs)


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reference: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    metadata_info: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(self, **kwargs):
        kwargs.pop("invoice_id", None)
        kwargs.pop("citizen_id", None)
        gateway_reference = kwargs.pop("gateway_reference", None)
        if gateway_reference and "reference" not in kwargs:
            kwargs["reference"] = gateway_reference
        payment_method = kwargs.pop("payment_method", None)
        if payment_method and "method" not in kwargs:
            kwargs["method"] = payment_method
        if "id" in kwargs and (not isinstance(kwargs["id"], int)):
            kwargs.pop("id")
        if "reference" not in kwargs:
            kwargs["reference"] = f"PAY-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        if "currency" not in kwargs:
            kwargs["currency"] = "AOA"
        status = kwargs.get("status")
        if isinstance(status, PaymentStatus):
            kwargs["status"] = status.value
        elif status is None:
            kwargs["status"] = PaymentStatus.PENDING.value
        now = datetime.utcnow()
        kwargs.setdefault("created_at", now)
        kwargs.setdefault("updated_at", now)
        super().__init__(**kwargs)


__all__ = [
    "AttestationServiceAdapter",
    "CertificateServiceAdapter",
    "FinancesServiceAdapter",
    "NotificationServiceAdapter",
    "RequestTrackingServiceAdapter",
    "ProfileQueries",
    "RequestState",
    "RoutingRule",
    "CitizenRepository",
    "Document",
    "Invoice",
    "Payment",
    "InvoiceStatus",
    "PaymentStatus",
]
