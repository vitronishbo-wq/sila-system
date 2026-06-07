from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure.application.ports.edital_repository_port import (
    EditalRepositoryPort,
)
from apps.backend.app.modules.infrastructure.domain.enums import StatusEdital
from apps.backend.app.modules.infrastructure.domain.models.edital import Edital
from apps.backend.app.modules.infrastructure.infrastructure.models.edital_model import EditalModel


class SQLAlchemyEditalRepository(EditalRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session
        self._items: dict[str, Edital] = {}
        self._seq = 0

    async def save(self, item: Edital) -> Edital:
        if self._session:
            existing = await self._session.execute(
                select(EditalModel).where(EditalModel.numero_edital == item.numero_edital)
            )
            model = existing.scalars().first()
            if model is None:
                model = EditalModel(
                    id=item.id,
                    numero_edital=item.numero_edital,
                    titulo=item.titulo,
                    objeto=item.objeto,
                    licitacao_id=item.licitacao_id,
                    status=item.status.value,
                    data_publicacao=item.data_publicacao,
                    data_abertura=item.data_abertura,
                    data_encerramento=item.data_encerramento,
                    data_cadastro=item.data_cadastro,
                    versao=item.versao,
                    data_atualizacao=item.data_atualizacao,
                    observacoes=item.observacoes,
                )
                self._session.add(model)
            else:
                model.titulo = item.titulo
                model.objeto = item.objeto
                model.licitacao_id = item.licitacao_id
                model.status = item.status.value
                model.data_publicacao = item.data_publicacao
                model.data_abertura = item.data_abertura
                model.data_encerramento = item.data_encerramento
                model.data_cadastro = item.data_cadastro
                model.versao = item.versao
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.numero_edital] = item
        return item

    async def get_by_numero(self, numero_edital: str) -> Edital | None:
        if self._session:
            result = await self._session.execute(
                select(EditalModel).where(EditalModel.numero_edital == numero_edital)
            )
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(numero_edital)

    async def list(
        self, *, status: StatusEdital | None = None, licitacao_id: UUID | None = None
    ) -> list[Edital]:
        if self._session:
            statement = select(EditalModel)
            if status:
                statement = statement.where(EditalModel.status == status.value)
            if licitacao_id:
                statement = statement.where(EditalModel.licitacao_id == licitacao_id)
            result = await self._session.execute(
                statement.order_by(EditalModel.numero_edital.asc())
            )
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if licitacao_id:
            values = [item for item in values if item.licitacao_id == licitacao_id]
        return values

    async def next_numero(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f"EDT/{year}/"
            result = await self._session.execute(
                select(func.count())
                .select_from(EditalModel)
                .where(EditalModel.numero_edital.like(f"{prefix}%"))
            )
            seq = int(result.scalar() or 0) + 1
            return f"{prefix}{seq:06d}"
        self._seq += 1
        return f"EDT/{date.today().year}/{self._seq:06d}"

    @staticmethod
    def _to_domain(model: EditalModel) -> Edital:
        return Edital(
            id=model.id,
            numero_edital=model.numero_edital,
            titulo=model.titulo,
            objeto=model.objeto,
            licitacao_id=model.licitacao_id,
            status=StatusEdital(model.status),
            data_publicacao=model.data_publicacao,
            data_abertura=model.data_abertura,
            data_encerramento=model.data_encerramento,
            data_cadastro=model.data_cadastro,
            versao=model.versao,
            data_atualizacao=model.data_atualizacao,
            observacoes=model.observacoes,
        )
