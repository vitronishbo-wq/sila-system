from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.assistencia_social.application.ports.crianca_risco_repository_port import CriancaRiscoRepositoryPort
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento
from apps.backend.app.modules.society.assistencia_social.domain.models import CriancaRisco
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.crianca_risco_model import CriancaRiscoModel

class SQLAlchemyCriancaRiscoRepository(CriancaRiscoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: CriancaRisco) -> CriancaRisco:
        model = await self.session.get(CriancaRiscoModel, entity.id)
        if model is None:
            model = CriancaRiscoModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.citizen_id_crianca = entity.citizen_id_crianca
        model.idade = entity.idade
        model.motivo = entity.motivo
        model.escolarizada = entity.escolarizada
        model.data_registro = entity.data_registro
        model.status = entity.status.value
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> CriancaRisco | None:
        model = await self.session.get(CriancaRiscoModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[CriancaRisco]:
        stmt = select(CriancaRiscoModel).where(CriancaRiscoModel.beneficiario_id == beneficiario_id).order_by(CriancaRiscoModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[CriancaRisco]:
        stmt = select(CriancaRiscoModel).order_by(CriancaRiscoModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(CriancaRiscoModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: CriancaRiscoModel) -> CriancaRisco:
        return CriancaRisco(id=model.id, codigo=model.codigo, beneficiario_id=model.beneficiario_id, citizen_id_crianca=model.citizen_id_crianca, idade=model.idade, motivo=model.motivo, escolarizada=model.escolarizada, data_registro=model.data_registro, status=StatusAcompanhamento(model.status))