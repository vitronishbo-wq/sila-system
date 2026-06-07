from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure.infrastructure.read_model.dashboard_model import (
    DashboardProjectionOffsetModel,
    ObraDashboardReadModel,
)


class DashboardProjectionRepository:
    async def project(
        self,
        session: AsyncSession,
        *,
        event_type: str,
        payload: dict,
        tenant_id: str,
        event_id: UUID | None = None,
    ) -> None:
        if event_id is not None:
            inserted = await self._mark_event_once(session, event_id=event_id)
            if not inserted:
                return
        if event_type == "ObraCriadaEvent":
            await self._project_obra_criada(session, payload=payload, tenant_id=tenant_id)
            return
        if event_type == "MedicaoAprovadaEvent":
            await self._project_medicao_aprovada(session, payload=payload, tenant_id=tenant_id)
            return
        if event_type == "ObraIniciadaEvent":
            await self._project_status(session, payload=payload, status="EM_EXECUCAO")
            return
        if event_type == "ObraConcluidaEvent":
            await self._project_status(session, payload=payload, status="CONCLUIDA")
            return

    async def _project_obra_criada(
        self, session: AsyncSession, *, payload: dict, tenant_id: str
    ) -> None:
        obra_id = str(payload["obra_id"])
        row = await session.get(ObraDashboardReadModel, obra_id)
        if row is None:
            row = ObraDashboardReadModel(
                obra_id=obra_id,
                tenant_id=tenant_id,
                codigo=str(payload.get("codigo_obra") or ""),
                status="PROJETO",
                valor_total=Decimal(str(payload.get("valor_orcado") or "0.00")),
                valor_executado=Decimal("0.00"),
                percentual_execucao=Decimal("0.00"),
            )
            session.add(row)
            await session.flush()
            return
        row.codigo = str(payload.get("codigo_obra") or row.codigo)
        row.tenant_id = tenant_id
        row.valor_total = Decimal(str(payload.get("valor_orcado") or row.valor_total))
        row.updated_at = datetime.now(UTC)
        await session.flush()

    async def _project_medicao_aprovada(
        self, session: AsyncSession, *, payload: dict, tenant_id: str
    ) -> None:
        obra_id = str(payload["obra_id"])
        row = await session.get(ObraDashboardReadModel, obra_id)
        if row is None:
            row = ObraDashboardReadModel(
                obra_id=obra_id,
                tenant_id=tenant_id,
                codigo=str(payload.get("codigo_obra") or ""),
                status="EM_EXECUCAO",
                valor_total=Decimal("0.00"),
                valor_executado=Decimal("0.00"),
                percentual_execucao=Decimal("0.00"),
            )
            session.add(row)
        row.valor_executado = Decimal(str(row.valor_executado)) + Decimal(
            str(payload.get("valor_medido") or "0.00")
        )
        if Decimal(str(row.valor_total)) > 0:
            row.percentual_execucao = row.valor_executado / row.valor_total * Decimal("100")
        else:
            row.percentual_execucao = Decimal(str(payload.get("percentual_executado") or "0.00"))
        row.status = "EM_EXECUCAO"
        row.updated_at = datetime.now(UTC)
        await session.flush()

    async def _project_status(self, session: AsyncSession, *, payload: dict, status: str) -> None:
        obra_id = str(payload["obra_id"])
        row = await session.get(ObraDashboardReadModel, obra_id)
        if row is None:
            return
        row.status = status
        row.updated_at = datetime.now(UTC)
        await session.flush()

    async def _mark_event_once(self, session: AsyncSession, *, event_id: UUID) -> bool:
        stmt = insert(DashboardProjectionOffsetModel).values(event_id=event_id)
        stmt = stmt.on_conflict_do_nothing(index_elements=["event_id"])
        result = await session.execute(stmt)
        return bool(result.rowcount)
