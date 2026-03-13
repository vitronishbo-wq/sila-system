from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.assistencia_social.application.ports.programa_social_repository_port import ProgramaSocialRepositoryPort
from app.modules.society.assistencia_social.domain.enums import PublicoAlvo, StatusProgramaSocial
from app.modules.society.assistencia_social.domain.models import ProgramaSocial
from app.modules.society.assistencia_social.infrastructure.models.programa_social_model import ProgramaSocialModel

class SQLAlchemyProgramaSocialRepository(ProgramaSocialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: ProgramaSocial) -> ProgramaSocial:
        model = await self.session.get(ProgramaSocialModel, entity.id)
        if model is None:
            model = ProgramaSocialModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.nome = entity.nome
        model.publico_alvo = entity.publico_alvo.value
        model.criterio_renda_max = entity.criterio_renda_max
        model.valor_base = entity.valor_base
        model.vagas = entity.vagas
        model.status = entity.status.value
        model.data_inicio = entity.data_inicio
        model.data_fim = entity.data_fim
        model.observacoes = entity.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> ProgramaSocial | None:
        model = await self.session.get(ProgramaSocialModel, entity_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo: str) -> ProgramaSocial | None:
        stmt = select(ProgramaSocialModel).where(ProgramaSocialModel.codigo == codigo.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[ProgramaSocial]:
        stmt = select(ProgramaSocialModel).order_by(ProgramaSocialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(ProgramaSocialModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: ProgramaSocialModel) -> ProgramaSocial:
        return ProgramaSocial(id=model.id, codigo=model.codigo, nome=model.nome, publico_alvo=PublicoAlvo(model.publico_alvo), criterio_renda_max=model.criterio_renda_max, valor_base=model.valor_base, vagas=model.vagas, status=StatusProgramaSocial(model.status), data_inicio=model.data_inicio, data_fim=model.data_fim, observacoes=model.observacoes)