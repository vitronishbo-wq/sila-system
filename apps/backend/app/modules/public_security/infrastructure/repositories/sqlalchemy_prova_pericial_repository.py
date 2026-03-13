from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.public_security.application.ports.prova_pericial_repository_port import ProvaPericialRepositoryPort
from apps.backend.app.modules.public_security.domain.enums import StatusProva, TipoProva
from apps.backend.app.modules.public_security.domain.models.prova_pericial import ProvaPericial
from apps.backend.app.modules.public_security.infrastructure.models.prova_pericial_model import ProvaPericialModel

class SQLAlchemyProvaPericialRepository(ProvaPericialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, prova: ProvaPericial) -> ProvaPericial:
        model = await self.session.get(ProvaPericialModel, prova.id)
        if not model:
            model = ProvaPericialModel(id=prova.id)
            self.session.add(model)
        model.codigo_prova = prova.codigo_prova
        model.ocorrencia_id = prova.ocorrencia_id
        model.tipo = prova.tipo.value
        model.descricao = prova.descricao
        model.data_coleta = prova.data_coleta
        model.local_coleta = prova.local_coleta
        model.status = prova.status.value
        model.coletado_por_id = prova.coletado_por_id
        model.cadeia_custodia_id = prova.cadeia_custodia_id
        model.observacoes = prova.observacoes
        model.ativo = prova.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, prova_id: UUID) -> ProvaPericial | None:
        model = await self.session.get(ProvaPericialModel, prova_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_prova: str) -> ProvaPericial | None:
        stmt = select(ProvaPericialModel).where(ProvaPericialModel.codigo_prova == codigo_prova.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[ProvaPericial]:
        stmt = select(ProvaPericialModel).order_by(ProvaPericialModel.data_coleta.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[ProvaPericial]:
        stmt = select(ProvaPericialModel).where(ProvaPericialModel.ocorrencia_id == ocorrencia_id).order_by(ProvaPericialModel.data_coleta.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoProva) -> list[ProvaPericial]:
        stmt = select(ProvaPericialModel).where(ProvaPericialModel.tipo == tipo.value).order_by(ProvaPericialModel.data_coleta.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusProva) -> list[ProvaPericial]:
        stmt = select(ProvaPericialModel).where(ProvaPericialModel.status == status.value).order_by(ProvaPericialModel.data_coleta.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, prova_id: UUID) -> bool:
        model = await self.session.get(ProvaPericialModel, prova_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'PRV/{year}/'
        stmt = select(func.count()).select_from(ProvaPericialModel).where(ProvaPericialModel.codigo_prova.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: ProvaPericialModel) -> ProvaPericial:
        return ProvaPericial(id=model.id, codigo_prova=model.codigo_prova, ocorrencia_id=model.ocorrencia_id, tipo=TipoProva(model.tipo), descricao=model.descricao, data_coleta=model.data_coleta, local_coleta=model.local_coleta, status=StatusProva(model.status), coletado_por_id=model.coletado_por_id, cadeia_custodia_id=model.cadeia_custodia_id, observacoes=model.observacoes, ativo=model.ativo)