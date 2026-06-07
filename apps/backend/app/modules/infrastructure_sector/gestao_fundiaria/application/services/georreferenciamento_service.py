from __future__ import annotations

from datetime import date
from decimal import Decimal

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.georreferenciamento_repository_port import (
    GeorreferenciamentoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.imovel_repository_port import (
    ImovelRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.georreferenciamento import (
    Georreferenciamento,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import (
    GeorreferenciamentoAlreadyExistsError,
    GeorreferenciamentoNotFoundError,
    ImovelNotFoundError,
)


class GeorreferenciamentoService:
    def __init__(
        self,
        *,
        georreferenciamento_repo: GeorreferenciamentoRepositoryPort,
        imovel_repo: ImovelRepositoryPort,
        geosampa_adapter: GeosampaServicePort | None = None,
    ) -> None:
        self._georreferenciamento_repo = georreferenciamento_repo
        self._imovel_repo = imovel_repo
        self._geosampa_adapter = geosampa_adapter

    def has_geosampa_adapter(self) -> bool:
        return self._geosampa_adapter is not None

    async def registrar(
        self,
        *,
        imovel_inscricao: str,
        latitude: Decimal,
        longitude: Decimal,
        sistema_referencia: str = "WGS84",
        precisao_metros: Decimal | None = None,
        area_calculada: Decimal | None = None,
        codigo_geo: str | None = None,
    ) -> Georreferenciamento:
        imovel = await self._imovel_repo.get_by_inscricao(imovel_inscricao)
        if not imovel:
            raise ImovelNotFoundError("Imovel nao encontrado para georreferenciamento")
        codigo = codigo_geo or await self._georreferenciamento_repo.next_codigo()
        existente = await self._georreferenciamento_repo.get_by_codigo(codigo)
        if existente:
            raise GeorreferenciamentoAlreadyExistsError(
                "Ja existe georreferenciamento com este codigo"
            )
        if self._geosampa_adapter:
            valido = await self._geosampa_adapter.validar_coordenadas(latitude, longitude)
            if not valido:
                raise ValueError("Coordenadas invalidas segundo o modulo Geosampa")
        item = Georreferenciamento.registrar(
            codigo_geo=codigo,
            imovel_inscricao=imovel_inscricao,
            latitude=latitude,
            longitude=longitude,
            sistema_referencia=sistema_referencia,
            precisao_metros=precisao_metros,
            area_calculada=area_calculada,
        )
        salvo = await self._georreferenciamento_repo.save(item)
        imovel.coordenadas_lat = salvo.latitude
        imovel.coordenadas_long = salvo.longitude
        imovel.data_atualizacao = date.today()
        await self._imovel_repo.save(imovel)
        return salvo

    async def atualizar_ponto(
        self, codigo_geo: str, *, latitude: Decimal, longitude: Decimal
    ) -> Georreferenciamento:
        item = await self._obter_ou_erro(codigo_geo)
        if self._geosampa_adapter:
            valido = await self._geosampa_adapter.validar_coordenadas(latitude, longitude)
            if not valido:
                raise ValueError("Coordenadas invalidas segundo o modulo Geosampa")
        item.atualizar_ponto(latitude=latitude, longitude=longitude)
        salvo = await self._georreferenciamento_repo.save(item)
        imovel = await self._imovel_repo.get_by_inscricao(salvo.imovel_inscricao)
        if imovel:
            imovel.coordenadas_lat = salvo.latitude
            imovel.coordenadas_long = salvo.longitude
            imovel.data_atualizacao = date.today()
            await self._imovel_repo.save(imovel)
        return salvo

    async def invalidar(self, codigo_geo: str, *, motivo: str) -> Georreferenciamento:
        item = await self._obter_ou_erro(codigo_geo)
        item.invalidar(motivo)
        return await self._georreferenciamento_repo.save(item)

    async def obter_por_codigo(self, codigo_geo: str) -> Georreferenciamento:
        return await self._obter_ou_erro(codigo_geo)

    async def listar(
        self,
        *,
        imovel_inscricao: str | None = None,
        validado: bool | None = None,
        ativo: bool | None = None,
    ) -> list[Georreferenciamento]:
        return await self._georreferenciamento_repo.list(
            imovel_inscricao=imovel_inscricao, validado=validado, ativo=ativo
        )

    async def _obter_ou_erro(self, codigo_geo: str) -> Georreferenciamento:
        item = await self._georreferenciamento_repo.get_by_codigo(codigo_geo)
        if not item:
            raise GeorreferenciamentoNotFoundError("Georreferenciamento nao encontrado")
        return item
