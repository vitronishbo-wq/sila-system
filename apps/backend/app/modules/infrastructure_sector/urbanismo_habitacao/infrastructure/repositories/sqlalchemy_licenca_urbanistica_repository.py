from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.licenca_urbanistica_repository_port import LicencaUrbanisticaRepositoryPort
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLicencaUrbanistica, TipoAlvara
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.licenca_urbanistica import LicencaUrbanistica
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.models.licenca_urbanistica_model import LicencaUrbanisticaModel

class SQLAlchemyLicencaUrbanisticaRepository(LicencaUrbanisticaRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, LicencaUrbanistica] = {}
        self._seq = 0

    async def save(self, item: LicencaUrbanistica) -> LicencaUrbanistica:
        if self._session:
            existing = await self._session.execute(select(LicencaUrbanisticaModel).where(LicencaUrbanisticaModel.codigo_licenca == item.codigo_licenca))
            model = existing.scalars().first()
            if model is None:
                model = LicencaUrbanisticaModel(id=item.id, codigo_licenca=item.codigo_licenca, numero_processo=item.numero_processo, tipo_alvara=item.tipo_alvara.value, status=item.status.value, requerente_id=item.requerente_id, zoneamento_id=item.zoneamento_id, provincia=item.provincia, municipio=item.municipio, endereco_obra=item.endereco_obra, area_construida_prevista=item.area_construida_prevista, data_requerimento=item.data_requerimento, data_emissao=item.data_emissao, data_validade=item.data_validade, tecnico_responsavel_id=item.tecnico_responsavel_id, observacoes=item.observacoes, data_atualizacao=item.data_atualizacao)
                self._session.add(model)
            else:
                model.numero_processo = item.numero_processo
                model.tipo_alvara = item.tipo_alvara.value
                model.status = item.status.value
                model.requerente_id = item.requerente_id
                model.zoneamento_id = item.zoneamento_id
                model.provincia = item.provincia
                model.municipio = item.municipio
                model.endereco_obra = item.endereco_obra
                model.area_construida_prevista = item.area_construida_prevista
                model.data_requerimento = item.data_requerimento
                model.data_emissao = item.data_emissao
                model.data_validade = item.data_validade
                model.tecnico_responsavel_id = item.tecnico_responsavel_id
                model.observacoes = item.observacoes
                model.data_atualizacao = item.data_atualizacao
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_licenca] = item
        return item

    async def get_by_codigo(self, codigo_licenca: str) -> LicencaUrbanistica | None:
        if self._session:
            result = await self._session.execute(select(LicencaUrbanisticaModel).where(LicencaUrbanisticaModel.codigo_licenca == codigo_licenca))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_licenca)

    async def list(self, *, status: StatusLicencaUrbanistica | None=None, tipo_alvara: TipoAlvara | None=None, provincia: str | None=None) -> list[LicencaUrbanistica]:
        if self._session:
            statement = select(LicencaUrbanisticaModel)
            if status:
                statement = statement.where(LicencaUrbanisticaModel.status == status.value)
            if tipo_alvara:
                statement = statement.where(LicencaUrbanisticaModel.tipo_alvara == tipo_alvara.value)
            if provincia:
                statement = statement.where(func.lower(LicencaUrbanisticaModel.provincia) == provincia.strip().lower())
            result = await self._session.execute(statement.order_by(LicencaUrbanisticaModel.codigo_licenca.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo_alvara:
            values = [item for item in values if item.tipo_alvara == tipo_alvara]
        if provincia:
            values = [item for item in values if item.provincia.lower() == provincia.lower()]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'LIC/{year}/'
            result = await self._session.execute(select(func.count()).select_from(LicencaUrbanisticaModel).where(LicencaUrbanisticaModel.codigo_licenca.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'LIC/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: LicencaUrbanisticaModel) -> LicencaUrbanistica:
        return LicencaUrbanistica(id=model.id, codigo_licenca=model.codigo_licenca, numero_processo=model.numero_processo, tipo_alvara=TipoAlvara(model.tipo_alvara), status=StatusLicencaUrbanistica(model.status), requerente_id=model.requerente_id, zoneamento_id=model.zoneamento_id, provincia=model.provincia, municipio=model.municipio, endereco_obra=model.endereco_obra, area_construida_prevista=Decimal(model.area_construida_prevista) if model.area_construida_prevista is not None else None, data_requerimento=model.data_requerimento, data_emissao=model.data_emissao, data_validade=model.data_validade, tecnico_responsavel_id=model.tecnico_responsavel_id, observacoes=model.observacoes, data_atualizacao=model.data_atualizacao)