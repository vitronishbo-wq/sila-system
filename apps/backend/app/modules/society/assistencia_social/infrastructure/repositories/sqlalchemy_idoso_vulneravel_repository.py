from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.assistencia_social.application.ports.idoso_vulneravel_repository_port import IdosoVulneravelRepositoryPort
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento
from apps.backend.app.modules.society.assistencia_social.domain.models import IdosoVulneravel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.idoso_vulneravel_model import IdosoVulneravelModel

class SQLAlchemyIdosoVulneravelRepository(IdosoVulneravelRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: IdosoVulneravel) -> IdosoVulneravel:
        model = await self.session.get(IdosoVulneravelModel, entity.id)
        if model is None:
            model = IdosoVulneravelModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.citizen_id_idoso = entity.citizen_id_idoso
        model.idade = entity.idade
        model.dependencia = entity.dependencia
        model.precisa_cuidados = entity.precisa_cuidados
        model.data_registro = entity.data_registro
        model.status = entity.status.value
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> IdosoVulneravel | None:
        model = await self.session.get(IdosoVulneravelModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[IdosoVulneravel]:
        stmt = select(IdosoVulneravelModel).where(IdosoVulneravelModel.beneficiario_id == beneficiario_id).order_by(IdosoVulneravelModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[IdosoVulneravel]:
        stmt = select(IdosoVulneravelModel).order_by(IdosoVulneravelModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(IdosoVulneravelModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: IdosoVulneravelModel) -> IdosoVulneravel:
        return IdosoVulneravel(id=model.id, codigo=model.codigo, beneficiario_id=model.beneficiario_id, citizen_id_idoso=model.citizen_id_idoso, idade=model.idade, dependencia=model.dependencia, precisa_cuidados=model.precisa_cuidados, data_registro=model.data_registro, status=StatusAcompanhamento(model.status))