from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.assistencia_social.application.ports.cadastro_unico_repository_port import CadastroUnicoRepositoryPort
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusCadastroUnico
from apps.backend.app.modules.society.assistencia_social.domain.models import CadastroUnico
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.cadastro_unico_model import CadastroUnicoModel

class SQLAlchemyCadastroUnicoRepository(CadastroUnicoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: CadastroUnico) -> CadastroUnico:
        model = await self.session.get(CadastroUnicoModel, entity.id)
        if model is None:
            model = CadastroUnicoModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.citizen_id_responsavel = entity.citizen_id_responsavel
        model.renda_per_capita = entity.renda_per_capita
        model.composicao_familiar = entity.composicao_familiar
        model.condicoes_moradia = entity.condicoes_moradia
        model.acesso_agua = entity.acesso_agua
        model.acesso_energia = entity.acesso_energia
        model.status = entity.status.value
        model.data_cadastro = entity.data_cadastro
        model.observacoes = entity.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> CadastroUnico | None:
        model = await self.session.get(CadastroUnicoModel, entity_id)
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID) -> CadastroUnico | None:
        stmt = select(CadastroUnicoModel).where(CadastroUnicoModel.citizen_id_responsavel == citizen_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[CadastroUnico]:
        stmt = select(CadastroUnicoModel).order_by(CadastroUnicoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(CadastroUnicoModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: CadastroUnicoModel) -> CadastroUnico:
        return CadastroUnico(id=model.id, codigo=model.codigo, citizen_id_responsavel=model.citizen_id_responsavel, renda_per_capita=model.renda_per_capita, composicao_familiar=model.composicao_familiar or [], condicoes_moradia=model.condicoes_moradia, acesso_agua=model.acesso_agua, acesso_energia=model.acesso_energia, status=StatusCadastroUnico(model.status), data_cadastro=model.data_cadastro, observacoes=model.observacoes)