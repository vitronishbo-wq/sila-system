from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.alvara_repository_port import AlvaraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusAlvara, TipoAlvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.alvara import Alvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.alvara_model import AlvaraModel

class SQLAlchemyAlvaraRepository(AlvaraRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Alvara] = {}
        self._seq = 0

    async def save(self, item: Alvara) -> Alvara:
        if self._session:
            existing = await self._session.execute(select(AlvaraModel).where(AlvaraModel.codigo_alvara == item.codigo_alvara))
            model = existing.scalars().first()
            if model is None:
                model = AlvaraModel(id=item.id, codigo_alvara=item.codigo_alvara, numero_processo=item.numero_processo, tipo=item.tipo.value, status=item.status.value, licenca_urbanistica_id=item.licenca_urbanistica_id, requerente_id=item.requerente_id, provincia=item.provincia, municipio=item.municipio, endereco_obra=item.endereco_obra, area_autorizada=item.area_autorizada, data_requerimento=item.data_requerimento, data_emissao=item.data_emissao, data_validade=item.data_validade, analista_id=item.analista_id, observacoes=item.observacoes, data_atualizacao=item.data_atualizacao)
                self._session.add(model)
            else:
                model.numero_processo = item.numero_processo
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.licenca_urbanistica_id = item.licenca_urbanistica_id
                model.requerente_id = item.requerente_id
                model.provincia = item.provincia
                model.municipio = item.municipio
                model.endereco_obra = item.endereco_obra
                model.area_autorizada = item.area_autorizada
                model.data_requerimento = item.data_requerimento
                model.data_emissao = item.data_emissao
                model.data_validade = item.data_validade
                model.analista_id = item.analista_id
                model.observacoes = item.observacoes
                model.data_atualizacao = item.data_atualizacao
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_alvara] = item
        return item

    async def get_by_codigo(self, codigo_alvara: str) -> Alvara | None:
        if self._session:
            result = await self._session.execute(select(AlvaraModel).where(AlvaraModel.codigo_alvara == codigo_alvara))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_alvara)

    async def list(self, *, status: StatusAlvara | None=None, tipo: TipoAlvara | None=None, provincia: str | None=None) -> list[Alvara]:
        if self._session:
            statement = select(AlvaraModel)
            if status:
                statement = statement.where(AlvaraModel.status == status.value)
            if tipo:
                statement = statement.where(AlvaraModel.tipo == tipo.value)
            if provincia:
                statement = statement.where(func.lower(AlvaraModel.provincia) == provincia.strip().lower())
            result = await self._session.execute(statement.order_by(AlvaraModel.codigo_alvara.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if provincia:
            values = [item for item in values if item.provincia.lower() == provincia.lower()]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'ALV/{year}/'
            result = await self._session.execute(select(func.count()).select_from(AlvaraModel).where(AlvaraModel.codigo_alvara.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'ALV/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: AlvaraModel) -> Alvara:
        return Alvara(id=model.id, codigo_alvara=model.codigo_alvara, numero_processo=model.numero_processo, tipo=TipoAlvara(model.tipo), status=StatusAlvara(model.status), licenca_urbanistica_id=model.licenca_urbanistica_id, requerente_id=model.requerente_id, provincia=model.provincia, municipio=model.municipio, endereco_obra=model.endereco_obra, area_autorizada=Decimal(model.area_autorizada) if model.area_autorizada is not None else None, data_requerimento=model.data_requerimento, data_emissao=model.data_emissao, data_validade=model.data_validade, analista_id=model.analista_id, observacoes=model.observacoes, data_atualizacao=model.data_atualizacao)