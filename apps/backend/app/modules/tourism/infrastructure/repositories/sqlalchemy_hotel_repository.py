from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.tourism.application.ports.hotel_repository_port import (
    HotelRepositoryPort,
)
from apps.backend.app.modules.tourism.domain.enums import ClassificacaoHoteleira
from apps.backend.app.modules.tourism.domain.models.hotel import Hotel
from apps.backend.app.modules.tourism.infrastructure.models.hotel_model import HotelModel


class SQLAlchemyHotelRepository(HotelRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self.session = session
        self._items: dict[UUID, HotelModel] = {}

    async def save(self, hotel: Hotel) -> Hotel:
        model = HotelModel(
            id=hotel.id,
            cadastur=hotel.cadastur,
            nome=hotel.nome,
            tipo=hotel.tipo,
            classificacao=hotel.classificacao,
            cnpj=hotel.cnpj,
            endereco=hotel.endereco,
            numero=hotel.numero,
            bairro=hotel.bairro,
            municipio=hotel.municipio,
            provincia=hotel.provincia,
            cep=hotel.cep,
            telefone=hotel.telefone,
            email=hotel.email,
            quartos=hotel.quartos,
            capacidade_maxima=hotel.capacidade_maxima,
            categoria_estrelas=hotel.categoria_estrelas,
            proprietario_id=hotel.proprietario_id,
            data_abertura=hotel.data_abertura,
            inscricao_estadual=hotel.inscricao_estadual,
            inscricao_municipal=hotel.inscricao_municipal,
            complemento=hotel.complemento,
            coordenadas_lat=hotel.coordenadas_lat,
            coordenadas_long=hotel.coordenadas_long,
            site=hotel.site,
            area_comum=list(hotel.area_comum) if hotel.area_comum else None,
            servicos=list(hotel.servicos) if hotel.servicos else None,
            acessibilidade=hotel.acessibilidade,
            pet_friendly=hotel.pet_friendly,
            wifi=hotel.wifi,
            estacionamento=hotel.estacionamento,
            piscina=hotel.piscina,
            academia=hotel.academia,
            restaurante=hotel.restaurante,
            bar=hotel.bar,
            sala_reunioes=hotel.sala_reunioes,
            centro_convencoes=hotel.centro_convencoes,
            responsavel_id=hotel.responsavel_id,
            licenca_funcionamento=hotel.licenca_funcionamento,
            data_renovacao=hotel.data_renovacao,
            observacoes=hotel.observacoes,
        )
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, hotel_id: UUID) -> Hotel | None:
        model = self._items.get(hotel_id)
        return self._to_domain(model) if model else None

    async def get_by_cadastur(self, cadastur: str) -> Hotel | None:
        key = cadastur.strip().upper()
        for model in self._items.values():
            if model.cadastur.upper() == key:
                return self._to_domain(model)
        return None

    async def get_by_cnpj(self, cnpj: str) -> Hotel | None:
        key = cnpj.strip()
        for model in self._items.values():
            if model.cnpj == key:
                return self._to_domain(model)
        return None

    async def list_all(self) -> list[Hotel]:
        values = sorted(self._items.values(), key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def list_by_proprietario(self, proprietario_id: UUID) -> list[Hotel]:
        values = [item for item in self._items.values() if item.proprietario_id == proprietario_id]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def list_by_municipio(self, municipio: str) -> list[Hotel]:
        target = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == target]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def list_by_classificacao(self, classificacao: ClassificacaoHoteleira) -> list[Hotel]:
        values = [item for item in self._items.values() if item.classificacao == classificacao]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def next_cadastur(self, provincia: str) -> str:
        sigla = provincia.strip().upper()
        ano = date.today().year
        prefixo = f"{sigla}/{ano}/"
        sequencia = sum(1 for item in self._items.values() if item.cadastur.startswith(prefixo)) + 1
        return f"{sigla}/{ano}/{sequencia:04d}"

    @staticmethod
    def _to_domain(model: HotelModel) -> Hotel:
        return Hotel(
            id=model.id,
            cadastur=model.cadastur,
            nome=model.nome,
            tipo=model.tipo,
            classificacao=model.classificacao,
            cnpj=model.cnpj,
            endereco=model.endereco,
            numero=model.numero,
            bairro=model.bairro,
            municipio=model.municipio,
            provincia=model.provincia,
            cep=model.cep,
            telefone=model.telefone,
            email=model.email,
            quartos=model.quartos,
            capacidade_maxima=model.capacidade_maxima,
            categoria_estrelas=model.categoria_estrelas,
            proprietario_id=model.proprietario_id,
            data_abertura=model.data_abertura,
            inscricao_estadual=model.inscricao_estadual,
            inscricao_municipal=model.inscricao_municipal,
            complemento=model.complemento,
            coordenadas_lat=model.coordenadas_lat,
            coordenadas_long=model.coordenadas_long,
            site=model.site,
            area_comum=list(model.area_comum) if model.area_comum else None,
            servicos=list(model.servicos) if model.servicos else None,
            acessibilidade=model.acessibilidade,
            pet_friendly=model.pet_friendly,
            wifi=model.wifi,
            estacionamento=model.estacionamento,
            piscina=model.piscina,
            academia=model.academia,
            restaurante=model.restaurante,
            bar=model.bar,
            sala_reunioes=model.sala_reunioes,
            centro_convencoes=model.centro_convencoes,
            responsavel_id=model.responsavel_id,
            licenca_funcionamento=model.licenca_funcionamento,
            data_renovacao=model.data_renovacao,
            observacoes=model.observacoes,
        )
