from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.imovel_repository_port import ImovelRepositoryPort
from app.modules.infrastructure_sector.gestao_fundiaria.domain.models.imovel import Imovel
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import NaturezaImovel, RegimePropriedade, SituacaoDominial, TipoImovel
from app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.models.imovel_model import ImovelModel

class SQLAlchemyImovelRepository(ImovelRepositoryPort):
    """Repository com suporte a ORM real (AsyncSession) e fallback in-memory."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, Imovel] = {}
        self._seq = 0

    async def save(self, item: Imovel) -> Imovel:
        if self._session:
            existing = await self._session.execute(select(ImovelModel).where(ImovelModel.inscricao_imobiliaria == item.inscricao_imobiliaria))
            model = existing.scalars().first()
            if model is None:
                model = ImovelModel(id=item.id, inscricao_imobiliaria=item.inscricao_imobiliaria, tipo=item.tipo.value, natureza=item.natureza.value, regime=item.regime.value, situacao=item.situacao.value, area_total=item.area_total, endereco=item.endereco, bairro=item.bairro, municipio=item.municipio, provincia=item.provincia, data_cadastro=item.data_cadastro, area_privativa=item.area_privativa, area_construida=item.area_construida, area_terreno=item.area_terreno, cep=item.cep, coordenadas_lat=item.coordenadas_lat, coordenadas_long=item.coordenadas_long, matricula_id=item.matricula_id, proprietario_atual_id=item.proprietario_atual_id, data_atualizacao=item.data_atualizacao, ativo=item.ativo, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.tipo = item.tipo.value
                model.natureza = item.natureza.value
                model.regime = item.regime.value
                model.situacao = item.situacao.value
                model.area_total = item.area_total
                model.endereco = item.endereco
                model.bairro = item.bairro
                model.municipio = item.municipio
                model.provincia = item.provincia
                model.area_privativa = item.area_privativa
                model.area_construida = item.area_construida
                model.area_terreno = item.area_terreno
                model.cep = item.cep
                model.coordenadas_lat = item.coordenadas_lat
                model.coordenadas_long = item.coordenadas_long
                model.matricula_id = item.matricula_id
                model.proprietario_atual_id = item.proprietario_atual_id
                model.data_atualizacao = item.data_atualizacao
                model.ativo = item.ativo
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.inscricao_imobiliaria] = item
        return item

    async def get_by_inscricao(self, inscricao_imobiliaria: str) -> Imovel | None:
        if self._session:
            result = await self._session.execute(select(ImovelModel).where(ImovelModel.inscricao_imobiliaria == inscricao_imobiliaria))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(inscricao_imobiliaria)

    async def list(self, *, proprietario_atual_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None, ativo: bool | None=None) -> list[Imovel]:
        if self._session:
            statement = select(ImovelModel)
            if proprietario_atual_id:
                statement = statement.where(ImovelModel.proprietario_atual_id == proprietario_atual_id)
            if municipio:
                statement = statement.where(func.lower(ImovelModel.municipio) == municipio.strip().lower())
            if provincia:
                statement = statement.where(func.lower(ImovelModel.provincia) == provincia.strip().lower())
            if ativo is not None:
                statement = statement.where(ImovelModel.ativo == ativo)
            result = await self._session.execute(statement.order_by(ImovelModel.inscricao_imobiliaria.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if proprietario_atual_id:
            values = [item for item in values if item.proprietario_atual_id == proprietario_atual_id]
        if municipio:
            mun = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == mun]
        if provincia:
            prov = provincia.strip().lower()
            values = [item for item in values if item.provincia.lower() == prov]
        if ativo is not None:
            values = [item for item in values if item.ativo == ativo]
        return values

    async def next_inscricao(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'IMV/{year}/'
            result = await self._session.execute(select(func.count()).select_from(ImovelModel).where(ImovelModel.inscricao_imobiliaria.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'IMV/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: ImovelModel) -> Imovel:
        return Imovel(id=model.id, inscricao_imobiliaria=model.inscricao_imobiliaria, tipo=TipoImovel(model.tipo), natureza=NaturezaImovel(model.natureza), regime=RegimePropriedade(model.regime), situacao=SituacaoDominial(model.situacao), area_total=Decimal(model.area_total), endereco=model.endereco, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, data_cadastro=model.data_cadastro, area_privativa=Decimal(model.area_privativa) if model.area_privativa is not None else None, area_construida=Decimal(model.area_construida) if model.area_construida is not None else None, area_terreno=Decimal(model.area_terreno) if model.area_terreno is not None else None, cep=model.cep, coordenadas_lat=Decimal(model.coordenadas_lat) if model.coordenadas_lat is not None else None, coordenadas_long=Decimal(model.coordenadas_long) if model.coordenadas_long is not None else None, matricula_id=model.matricula_id, proprietario_atual_id=model.proprietario_atual_id, data_atualizacao=model.data_atualizacao, ativo=model.ativo, observacoes=model.observacoes)