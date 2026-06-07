from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.zoneamento_repository_port import (
    ZoneamentoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusZoneamento,
    TipoZona,
    UsoPermitido,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.zoneamento import (
    Zoneamento,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    ZoneamentoAlreadyExistsError,
    ZoneamentoNotFoundError,
)


class ZoneamentoService:
    def __init__(self, *, zoneamento_repo: ZoneamentoRepositoryPort) -> None:
        self._zoneamento_repo = zoneamento_repo

    async def criar(
        self,
        *,
        nome: str,
        tipo_zona: TipoZona,
        plano_diretor_id: UUID,
        provincia: str,
        usos_permitidos: list[UsoPermitido],
        municipio: str | None = None,
        codigo_zoneamento: str | None = None,
    ) -> Zoneamento:
        codigo = codigo_zoneamento or await self._zoneamento_repo.next_codigo()
        existente = await self._zoneamento_repo.get_by_codigo(codigo)
        if existente:
            raise ZoneamentoAlreadyExistsError("Ja existe zoneamento com este codigo")
        item = Zoneamento.criar(
            codigo_zoneamento=codigo,
            nome=nome,
            tipo_zona=tipo_zona,
            plano_diretor_id=plano_diretor_id,
            provincia=provincia,
            usos_permitidos=usos_permitidos,
            municipio=municipio,
        )
        return await self._zoneamento_repo.save(item)

    async def iniciar_consulta_publica(self, codigo_zoneamento: str) -> Zoneamento:
        item = await self._obter_ou_erro(codigo_zoneamento)
        item.iniciar_consulta_publica()
        return await self._zoneamento_repo.save(item)

    async def aprovar(self, codigo_zoneamento: str) -> Zoneamento:
        item = await self._obter_ou_erro(codigo_zoneamento)
        item.aprovar()
        return await self._zoneamento_repo.save(item)

    async def vigorar(self, codigo_zoneamento: str, *, data_inicio_vigencia: date) -> Zoneamento:
        item = await self._obter_ou_erro(codigo_zoneamento)
        item.vigorar(data_inicio_vigencia=data_inicio_vigencia)
        return await self._zoneamento_repo.save(item)

    async def suspender(self, codigo_zoneamento: str, *, motivo: str) -> Zoneamento:
        item = await self._obter_ou_erro(codigo_zoneamento)
        item.suspender(motivo=motivo)
        return await self._zoneamento_repo.save(item)

    async def revogar(self, codigo_zoneamento: str, *, motivo: str) -> Zoneamento:
        item = await self._obter_ou_erro(codigo_zoneamento)
        item.revogar(motivo=motivo)
        return await self._zoneamento_repo.save(item)

    async def atualizar_parametros(
        self,
        codigo_zoneamento: str,
        *,
        usos_permitidos: list[UsoPermitido] | None = None,
        coeficiente_aproveitamento_max: Decimal | None = None,
        taxa_ocupacao_max: Decimal | None = None,
        gabarito_maximo: int | None = None,
        recuo_frontal_minimo: Decimal | None = None,
        permeabilidade_minima: Decimal | None = None,
        area_lote_minima: Decimal | None = None,
    ) -> Zoneamento:
        item = await self._obter_ou_erro(codigo_zoneamento)
        item.atualizar_parametros(
            usos_permitidos=usos_permitidos,
            coeficiente_aproveitamento_max=coeficiente_aproveitamento_max,
            taxa_ocupacao_max=taxa_ocupacao_max,
            gabarito_maximo=gabarito_maximo,
            recuo_frontal_minimo=recuo_frontal_minimo,
            permeabilidade_minima=permeabilidade_minima,
            area_lote_minima=area_lote_minima,
        )
        return await self._zoneamento_repo.save(item)

    async def obter_por_codigo(self, codigo_zoneamento: str) -> Zoneamento:
        return await self._obter_ou_erro(codigo_zoneamento)

    async def listar(
        self,
        *,
        status: StatusZoneamento | None = None,
        tipo_zona: TipoZona | None = None,
        provincia: str | None = None,
    ) -> list[Zoneamento]:
        return await self._zoneamento_repo.list(
            status=status, tipo_zona=tipo_zona, provincia=provincia
        )

    async def _obter_ou_erro(self, codigo_zoneamento: str) -> Zoneamento:
        item = await self._zoneamento_repo.get_by_codigo(codigo_zoneamento)
        if not item:
            raise ZoneamentoNotFoundError("Zoneamento nao encontrado")
        return item
