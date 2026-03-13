from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.juventude.application.ports.inscricao_programa_repository_port import InscricaoProgramaRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import StatusInscricao
from apps.backend.app.modules.society.juventude.domain.models.inscricao_programa import InscricaoPrograma
from apps.backend.app.modules.society.juventude.infrastructure.models.inscricao_programa_model import InscricaoProgramaModel

class SQLAlchemyInscricaoProgramaRepository(InscricaoProgramaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, inscricao: InscricaoPrograma) -> InscricaoPrograma:
        model = await self.session.get(InscricaoProgramaModel, inscricao.id)
        if not model:
            model = InscricaoProgramaModel(id=inscricao.id)
            self.session.add(model)
        model.codigo_inscricao = inscricao.codigo_inscricao
        model.programa_id = inscricao.programa_id
        model.jovem_id = inscricao.jovem_id
        model.data_inscricao = inscricao.data_inscricao
        model.status = inscricao.status.value
        model.prioridade = inscricao.prioridade
        model.data_cadastro = inscricao.data_cadastro
        model.observacoes = inscricao.observacoes
        model.ativo = inscricao.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, inscricao_id: UUID) -> InscricaoPrograma | None:
        model = await self.session.get(InscricaoProgramaModel, inscricao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_inscricao: str) -> InscricaoPrograma | None:
        stmt = select(InscricaoProgramaModel).where(InscricaoProgramaModel.codigo_inscricao == codigo_inscricao.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[InscricaoPrograma]:
        stmt = select(InscricaoProgramaModel).order_by(InscricaoProgramaModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[InscricaoPrograma]:
        stmt = select(InscricaoProgramaModel).where(InscricaoProgramaModel.jovem_id == jovem_id).order_by(InscricaoProgramaModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_programa(self, programa_id: UUID) -> list[InscricaoPrograma]:
        stmt = select(InscricaoProgramaModel).where(InscricaoProgramaModel.programa_id == programa_id).order_by(InscricaoProgramaModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusInscricao) -> list[InscricaoPrograma]:
        stmt = select(InscricaoProgramaModel).where(InscricaoProgramaModel.status == status.value).order_by(InscricaoProgramaModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def exists_active_by_jovem_programa(self, jovem_id: UUID, programa_id: UUID) -> bool:
        stmt = select(InscricaoProgramaModel.id).where(and_(InscricaoProgramaModel.jovem_id == jovem_id, InscricaoProgramaModel.programa_id == programa_id, InscricaoProgramaModel.status.in_([StatusInscricao.PENDENTE.value, StatusInscricao.CONFIRMADA.value])))
        return (await self.session.execute(stmt)).first() is not None

    async def count_confirmadas_by_programa(self, programa_id: UUID) -> int:
        stmt = select(func.count()).select_from(InscricaoProgramaModel).where(InscricaoProgramaModel.programa_id == programa_id, InscricaoProgramaModel.status == StatusInscricao.CONFIRMADA.value)
        return int((await self.session.execute(stmt)).scalar() or 0)

    async def delete(self, inscricao_id: UUID) -> bool:
        model = await self.session.get(InscricaoProgramaModel, inscricao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(InscricaoProgramaModel).where(InscricaoProgramaModel.codigo_inscricao.like(f'INS/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'INS/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: InscricaoProgramaModel) -> InscricaoPrograma:
        return InscricaoPrograma(id=model.id, codigo_inscricao=model.codigo_inscricao, programa_id=model.programa_id, jovem_id=model.jovem_id, data_inscricao=model.data_inscricao, status=StatusInscricao(model.status), prioridade=model.prioridade, data_cadastro=model.data_cadastro, observacoes=model.observacoes, ativo=model.ativo)