from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.assistencia_social.application.ports.beneficio_repository_port import BeneficioRepositoryPort
from app.modules.society.assistencia_social.domain.enums import StatusBeneficio, TipoBeneficio
from app.modules.society.assistencia_social.domain.models import Beneficio
from app.modules.society.assistencia_social.infrastructure.models.beneficio_model import BeneficioModel

class SQLAlchemyBeneficioRepository(BeneficioRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: Beneficio) -> Beneficio:
        model = await self.session.get(BeneficioModel, entity.id)
        if model is None:
            model = BeneficioModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.programa_social_id = entity.programa_social_id
        model.tipo = entity.tipo.value
        model.valor = entity.valor
        model.status = entity.status.value
        model.data_solicitacao = entity.data_solicitacao
        model.data_concessao = entity.data_concessao
        model.data_fim = entity.data_fim
        model.motivo_status = entity.motivo_status
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> Beneficio | None:
        model = await self.session.get(BeneficioModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[Beneficio]:
        stmt = select(BeneficioModel).where(BeneficioModel.beneficiario_id == beneficiario_id).order_by(BeneficioModel.data_solicitacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[Beneficio]:
        stmt = select(BeneficioModel).order_by(BeneficioModel.data_solicitacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(BeneficioModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: BeneficioModel) -> Beneficio:
        return Beneficio(id=model.id, codigo=model.codigo, beneficiario_id=model.beneficiario_id, programa_social_id=model.programa_social_id, tipo=TipoBeneficio(model.tipo), valor=model.valor, status=StatusBeneficio(model.status), data_solicitacao=model.data_solicitacao, data_concessao=model.data_concessao, data_fim=model.data_fim, motivo_status=model.motivo_status)