from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.reclamacao_repository_port import (
    ReclamacaoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusReclamacaoTelecom,
    TipoReclamacaoTelecom,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.reclamacao import (
    Reclamacao,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.reclamacao_model import (
    ReclamacaoTelecomModel,
)


class SQLAlchemyReclamacaoRepository(ReclamacaoRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, reclamacao: Reclamacao) -> Reclamacao:
        model = await self.session.get(ReclamacaoTelecomModel, reclamacao.id)
        if not model:
            model = ReclamacaoTelecomModel(id=reclamacao.id)
            self.session.add(model)
        model.protocolo = reclamacao.protocolo
        model.assinante_id = reclamacao.assinante_id
        model.tipo = reclamacao.tipo.value
        model.descricao = reclamacao.descricao
        model.prioridade = reclamacao.prioridade
        model.status = reclamacao.status.value
        model.data_abertura = reclamacao.data_abertura
        model.data_fechamento = reclamacao.data_fechamento
        model.resposta = reclamacao.resposta
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, reclamacao_id: UUID) -> Reclamacao | None:
        model = await self.session.get(ReclamacaoTelecomModel, reclamacao_id)
        return self._to_domain(model) if model else None

    async def get_by_protocolo(self, protocolo: str) -> Reclamacao | None:
        stmt = select(ReclamacaoTelecomModel).where(
            ReclamacaoTelecomModel.protocolo == protocolo.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_assinante(self, assinante_id: UUID) -> list[Reclamacao]:
        stmt = (
            select(ReclamacaoTelecomModel)
            .where(ReclamacaoTelecomModel.assinante_id == assinante_id)
            .order_by(ReclamacaoTelecomModel.data_abertura.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[Reclamacao]:
        stmt = select(ReclamacaoTelecomModel).order_by(ReclamacaoTelecomModel.data_abertura.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_protocolo(self) -> str:
        year = date.today().year
        stmt = (
            select(func.count())
            .select_from(ReclamacaoTelecomModel)
            .where(ReclamacaoTelecomModel.protocolo.like(f"RCT/{year}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"RCT/{year}/{count + 1:06d}"

    @staticmethod
    def _to_domain(model: ReclamacaoTelecomModel) -> Reclamacao:
        return Reclamacao(
            id=model.id,
            protocolo=model.protocolo,
            assinante_id=model.assinante_id,
            tipo=TipoReclamacaoTelecom(model.tipo),
            descricao=model.descricao,
            prioridade=model.prioridade,
            status=StatusReclamacaoTelecom(model.status),
            data_abertura=model.data_abertura,
            data_fechamento=model.data_fechamento,
            resposta=model.resposta,
        )
