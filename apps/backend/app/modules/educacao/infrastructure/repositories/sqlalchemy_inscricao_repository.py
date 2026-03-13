from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.educacao.application.ports.inscricao_repository_port import InscricaoEntity, InscricaoRepositoryPort
from app.modules.educacao.domain.enums import StatusFluxo, TipoInscricao
from app.modules.educacao.domain.models.inscricao_basica import InscricaoBasica
from app.modules.educacao.domain.models.inscricao_secundaria import InscricaoSecundaria
from app.modules.educacao.domain.models.inscricao_superior import InscricaoSuperior
from app.modules.educacao.domain.models.inscricao_tecnico import InscricaoTecnico
from app.modules.educacao.infrastructure.models.inscricao_model import InscricaoModel

class SQLAlchemyInscricaoRepository(InscricaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, inscricao: InscricaoEntity) -> InscricaoEntity:
        model = await self.session.get(InscricaoModel, inscricao.id)
        if not model:
            model = InscricaoModel(id=inscricao.id)
            self.session.add(model)
        model.numero_processo = inscricao.numero_processo
        model.tipo = inscricao.tipo.value
        model.citizen_id = inscricao.citizen_id
        model.escola_id = inscricao.escola_id
        model.data_inscricao = inscricao.data_inscricao
        model.status = inscricao.status.value
        model.observacoes = inscricao.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID):
        model = await self.session.get(InscricaoModel, id)
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID, tipo: TipoInscricao | None=None):
        stmt = select(InscricaoModel).where(InscricaoModel.citizen_id == citizen_id)
        if tipo:
            stmt = stmt.where(InscricaoModel.tipo == tipo.value)
        stmt = stmt.order_by(InscricaoModel.data_inscricao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def exists_active_for_citizen(self, citizen_id: UUID, tipo: TipoInscricao) -> bool:
        stmt = select(InscricaoModel.id).where(and_(InscricaoModel.citizen_id == citizen_id, InscricaoModel.tipo == tipo.value, InscricaoModel.status.in_([StatusFluxo.PENDENTE.value, StatusFluxo.CONFIRMADA.value])))
        return (await self.session.execute(stmt)).first() is not None

    async def next_numero_processo(self, ano: int, tipo: TipoInscricao) -> str:
        prefix = f'INS/{tipo.value.upper()}/{ano}/'
        count_stmt = select(func.count()).select_from(InscricaoModel).where(InscricaoModel.numero_processo.like(f'{prefix}%'))
        count = (await self.session.execute(count_stmt)).scalar() or 0
        return f'{prefix}{count + 1:04d}'

    @staticmethod
    def _to_domain(model: InscricaoModel) -> InscricaoEntity:
        tipo = TipoInscricao(model.tipo)
        kwargs = {'id': model.id, 'numero_processo': model.numero_processo, 'citizen_id': model.citizen_id, 'escola_id': model.escola_id, 'data_inscricao': model.data_inscricao or date.today(), 'status': StatusFluxo(model.status), 'observacoes': model.observacoes}
        if tipo == TipoInscricao.BASICA:
            return InscricaoBasica(**kwargs)
        if tipo == TipoInscricao.SECUNDARIA:
            return InscricaoSecundaria(**kwargs)
        if tipo == TipoInscricao.SUPERIOR:
            return InscricaoSuperior(**kwargs)
        return InscricaoTecnico(**kwargs)