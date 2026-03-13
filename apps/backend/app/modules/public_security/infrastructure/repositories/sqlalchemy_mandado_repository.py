from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.public_security.application.ports.mandado_repository_port import MandadoRepositoryPort
from app.modules.public_security.domain.enums import StatusMandado, TipoMandado
from app.modules.public_security.domain.models.mandado import Mandado
from app.modules.public_security.infrastructure.models.mandado_model import MandadoModel

class SQLAlchemyMandadoRepository(MandadoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, mandado: Mandado) -> Mandado:
        model = await self.session.get(MandadoModel, mandado.id)
        if not model:
            model = MandadoModel(id=mandado.id)
            self.session.add(model)
        model.numero_mandado = mandado.numero_mandado
        model.ocorrencia_id = mandado.ocorrencia_id
        model.tipo = mandado.tipo.value
        model.autoridade_judicial = mandado.autoridade_judicial
        model.data_expedicao = mandado.data_expedicao
        model.data_validade = mandado.data_validade
        model.status = mandado.status.value
        model.unidade_id = mandado.unidade_id
        model.policial_responsavel_id = mandado.policial_responsavel_id
        model.observacoes = mandado.observacoes
        model.ativo = mandado.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, mandado_id: UUID) -> Mandado | None:
        model = await self.session.get(MandadoModel, mandado_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_mandado: str) -> Mandado | None:
        stmt = select(MandadoModel).where(MandadoModel.numero_mandado == numero_mandado.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Mandado]:
        stmt = select(MandadoModel).order_by(MandadoModel.data_expedicao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Mandado]:
        stmt = select(MandadoModel).where(MandadoModel.ocorrencia_id == ocorrencia_id).order_by(MandadoModel.data_expedicao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoMandado) -> list[Mandado]:
        stmt = select(MandadoModel).where(MandadoModel.tipo == tipo.value).order_by(MandadoModel.data_expedicao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusMandado) -> list[Mandado]:
        stmt = select(MandadoModel).where(MandadoModel.status == status.value).order_by(MandadoModel.data_expedicao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, mandado_id: UUID) -> bool:
        model = await self.session.get(MandadoModel, mandado_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_numero(self) -> str:
        year = date.today().year
        prefix = f'MD/{year}/'
        stmt = select(func.count()).select_from(MandadoModel).where(MandadoModel.numero_mandado.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: MandadoModel) -> Mandado:
        return Mandado(id=model.id, numero_mandado=model.numero_mandado, ocorrencia_id=model.ocorrencia_id, tipo=TipoMandado(model.tipo), autoridade_judicial=model.autoridade_judicial, data_expedicao=model.data_expedicao, data_validade=model.data_validade, status=StatusMandado(model.status), unidade_id=model.unidade_id, policial_responsavel_id=model.policial_responsavel_id, observacoes=model.observacoes, ativo=model.ativo)