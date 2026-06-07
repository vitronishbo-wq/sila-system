from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.juventude.application.ports.empreendedorismo_juvenil_repository_port import (
    EmpreendedorismoJuvenilRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusEmpreendimento,
)
from apps.backend.app.modules.society.juventude.domain.models.empreendedorismo_juvenil import (
    EmpreendedorismoJuvenil,
)
from apps.backend.app.modules.society.juventude.infrastructure.models.empreendedorismo_juvenil_model import (
    EmpreendedorismoJuvenilModel,
)


class SQLAlchemyEmpreendedorismoJuvenilRepository(EmpreendedorismoJuvenilRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, empreendimento: EmpreendedorismoJuvenil) -> EmpreendedorismoJuvenil:
        model = await self.session.get(EmpreendedorismoJuvenilModel, empreendimento.id)
        if not model:
            model = EmpreendedorismoJuvenilModel(id=empreendimento.id)
            self.session.add(model)
        model.codigo_empreendimento = empreendimento.codigo_empreendimento
        model.jovem_id = empreendimento.jovem_id
        model.nome_negocio = empreendimento.nome_negocio
        model.area_interesse = empreendimento.area_interesse.value
        model.status = empreendimento.status.value
        model.receita_mensal = empreendimento.receita_mensal
        model.valor_credito = empreendimento.valor_credito
        model.data_cadastro = empreendimento.data_cadastro
        model.observacoes = empreendimento.observacoes
        model.ativo = empreendimento.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, empreendimento_id: UUID) -> EmpreendedorismoJuvenil | None:
        model = await self.session.get(EmpreendedorismoJuvenilModel, empreendimento_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_empreendimento: str) -> EmpreendedorismoJuvenil | None:
        stmt = select(EmpreendedorismoJuvenilModel).where(
            EmpreendedorismoJuvenilModel.codigo_empreendimento == codigo_empreendimento.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[EmpreendedorismoJuvenil]:
        stmt = select(EmpreendedorismoJuvenilModel).order_by(
            EmpreendedorismoJuvenilModel.data_cadastro.desc()
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[EmpreendedorismoJuvenil]:
        stmt = (
            select(EmpreendedorismoJuvenilModel)
            .where(EmpreendedorismoJuvenilModel.jovem_id == jovem_id)
            .order_by(EmpreendedorismoJuvenilModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusEmpreendimento) -> list[EmpreendedorismoJuvenil]:
        stmt = (
            select(EmpreendedorismoJuvenilModel)
            .where(EmpreendedorismoJuvenilModel.status == status.value)
            .order_by(EmpreendedorismoJuvenilModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, empreendimento_id: UUID) -> bool:
        model = await self.session.get(EmpreendedorismoJuvenilModel, empreendimento_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(EmpreendedorismoJuvenilModel)
            .where(EmpreendedorismoJuvenilModel.codigo_empreendimento.like(f"EMPJ/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"EMPJ/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: EmpreendedorismoJuvenilModel) -> EmpreendedorismoJuvenil:
        return EmpreendedorismoJuvenil(
            id=model.id,
            codigo_empreendimento=model.codigo_empreendimento,
            jovem_id=model.jovem_id,
            nome_negocio=model.nome_negocio,
            area_interesse=AreaInteresse(model.area_interesse),
            status=StatusEmpreendimento(model.status),
            receita_mensal=model.receita_mensal,
            valor_credito=model.valor_credito,
            data_cadastro=model.data_cadastro or date.today(),
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
