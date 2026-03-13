from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.assistencia_social.application.ports.pcd_repository_port import PCDRepositoryPort
from app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento
from app.modules.society.assistencia_social.domain.models import PessoaComDeficiencia
from app.modules.society.assistencia_social.infrastructure.models.pcd_model import PCDModel

class SQLAlchemyPCDRepository(PCDRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: PessoaComDeficiencia) -> PessoaComDeficiencia:
        model = await self.session.get(PCDModel, entity.id)
        if model is None:
            model = PCDModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.citizen_id_pcd = entity.citizen_id_pcd
        model.tipo_deficiencia = entity.tipo_deficiencia
        model.cid = entity.cid
        model.grau_deficiencia = entity.grau_deficiencia
        model.laudo_id = entity.laudo_id
        model.bpc_ativo = entity.bpc_ativo
        model.data_registro = entity.data_registro
        model.status = entity.status.value
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> PessoaComDeficiencia | None:
        model = await self.session.get(PCDModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[PessoaComDeficiencia]:
        stmt = select(PCDModel).where(PCDModel.beneficiario_id == beneficiario_id).order_by(PCDModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[PessoaComDeficiencia]:
        stmt = select(PCDModel).order_by(PCDModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(PCDModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: PCDModel) -> PessoaComDeficiencia:
        return PessoaComDeficiencia(id=model.id, codigo=model.codigo, beneficiario_id=model.beneficiario_id, citizen_id_pcd=model.citizen_id_pcd, tipo_deficiencia=model.tipo_deficiencia, cid=model.cid, grau_deficiencia=model.grau_deficiencia, laudo_id=model.laudo_id, bpc_ativo=model.bpc_ativo, data_registro=model.data_registro, status=StatusAcompanhamento(model.status))