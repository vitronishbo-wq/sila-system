from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.assistencia_social.application.ports.beneficiario_repository_port import BeneficiarioRepositoryPort
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, SituacaoBeneficiario
from app.modules.society.assistencia_social.domain.models import Beneficiario
from app.modules.society.assistencia_social.infrastructure.models.beneficiario_model import BeneficiarioModel

class SQLAlchemyBeneficiarioRepository(BeneficiarioRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: Beneficiario) -> Beneficiario:
        model = await self.session.get(BeneficiarioModel, entity.id)
        if model is None:
            model = BeneficiarioModel(id=entity.id)
            self.session.add(model)
        model.numero_registro = entity.numero_registro
        model.citizen_id = entity.citizen_id
        model.cadastro_unico_id = entity.cadastro_unico_id
        model.faixa_vulnerabilidade = entity.faixa_vulnerabilidade.value
        model.situacao = entity.situacao.value
        model.data_cadastro = entity.data_cadastro
        model.observacoes = entity.observacoes
        model.ativo = entity.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> Beneficiario | None:
        model = await self.session.get(BeneficiarioModel, entity_id)
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID) -> Beneficiario | None:
        stmt = select(BeneficiarioModel).where(BeneficiarioModel.citizen_id == citizen_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Beneficiario]:
        stmt = select(BeneficiarioModel).order_by(BeneficiarioModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(BeneficiarioModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: BeneficiarioModel) -> Beneficiario:
        return Beneficiario(id=model.id, numero_registro=model.numero_registro, citizen_id=model.citizen_id, cadastro_unico_id=model.cadastro_unico_id, faixa_vulnerabilidade=FaixaVulnerabilidade(model.faixa_vulnerabilidade), situacao=SituacaoBeneficiario(model.situacao), data_cadastro=model.data_cadastro, observacoes=model.observacoes, ativo=model.ativo)