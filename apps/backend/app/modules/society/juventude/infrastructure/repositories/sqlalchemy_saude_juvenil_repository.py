from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.juventude.application.ports.saude_juvenil_repository_port import SaudeJuvenilRepositoryPort
from app.modules.society.juventude.domain.enums import StatusAcompanhamento, TipoSaudeJuvenil
from app.modules.society.juventude.domain.models.saude_juvenil import SaudeJuvenil
from app.modules.society.juventude.infrastructure.models.saude_juvenil_model import SaudeJuvenilModel

class SQLAlchemySaudeJuvenilRepository(SaudeJuvenilRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, registo: SaudeJuvenil) -> SaudeJuvenil:
        model = await self.session.get(SaudeJuvenilModel, registo.id)
        if not model:
            model = SaudeJuvenilModel(id=registo.id)
            self.session.add(model)
        model.codigo_registo = registo.codigo_registo
        model.jovem_id = registo.jovem_id
        model.tipo_registo = registo.tipo_registo.value
        model.descricao = registo.descricao
        model.data_registo = registo.data_registo
        model.status_acompanhamento = registo.status_acompanhamento.value
        model.encaminhamento_necessario = registo.encaminhamento_necessario
        model.data_cadastro = registo.data_cadastro
        model.observacoes = registo.observacoes
        model.ativo = registo.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, registo_id: UUID) -> SaudeJuvenil | None:
        model = await self.session.get(SaudeJuvenilModel, registo_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_registo: str) -> SaudeJuvenil | None:
        stmt = select(SaudeJuvenilModel).where(SaudeJuvenilModel.codigo_registo == codigo_registo.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[SaudeJuvenil]:
        stmt = select(SaudeJuvenilModel).order_by(SaudeJuvenilModel.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[SaudeJuvenil]:
        stmt = select(SaudeJuvenilModel).where(SaudeJuvenilModel.jovem_id == jovem_id).order_by(SaudeJuvenilModel.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusAcompanhamento) -> list[SaudeJuvenil]:
        stmt = select(SaudeJuvenilModel).where(SaudeJuvenilModel.status_acompanhamento == status.value).order_by(SaudeJuvenilModel.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, registo_id: UUID) -> bool:
        model = await self.session.get(SaudeJuvenilModel, registo_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(SaudeJuvenilModel).where(SaudeJuvenilModel.codigo_registo.like(f'SAU/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'SAU/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: SaudeJuvenilModel) -> SaudeJuvenil:
        return SaudeJuvenil(id=model.id, codigo_registo=model.codigo_registo, jovem_id=model.jovem_id, tipo_registo=TipoSaudeJuvenil(model.tipo_registo), descricao=model.descricao, data_registo=model.data_registo, status_acompanhamento=StatusAcompanhamento(model.status_acompanhamento), encaminhamento_necessario=model.encaminhamento_necessario, data_cadastro=model.data_cadastro or date.today(), observacoes=model.observacoes, ativo=model.ativo)