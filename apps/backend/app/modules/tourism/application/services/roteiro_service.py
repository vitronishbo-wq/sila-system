from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.tourism.application.ports.comercio_servicos_service_port import (
    ComercioServicosServicePort,
)
from apps.backend.app.modules.tourism.application.ports.roteiro_repository_port import (
    RoteiroRepositoryPort,
)
from apps.backend.app.modules.tourism.application.ports.transportes_logistica_service_port import (
    TransportesLogisticaServicePort,
)
from apps.backend.app.modules.tourism.domain.models.roteiro import Roteiro


class RoteiroService:
    def __init__(
        self,
        *,
        repository: RoteiroRepositoryPort,
        transportes_service: TransportesLogisticaServicePort | None = None,
        comercio_service: ComercioServicosServicePort | None = None,
    ):
        self.repository = repository
        self.transportes_service = transportes_service
        self.comercio_service = comercio_service

    async def cadastrar(
        self,
        *,
        titulo: str,
        descricao: str,
        municipio_origem: str,
        provincia_origem: str,
        duracao_horas: int,
        pontos_parada: list[str] | None = None,
        acessivel: bool = True,
        valor_estimado: Decimal | None = None,
        observacoes: str | None = None,
    ) -> Roteiro:
        roteiro = Roteiro.criar(
            titulo=titulo,
            descricao=descricao,
            municipio_origem=municipio_origem,
            provincia_origem=provincia_origem,
            duracao_horas=duracao_horas,
            pontos_parada=pontos_parada,
            acessivel=acessivel,
            valor_estimado=valor_estimado,
            observacoes=observacoes,
        )
        roteiro.codigo = await self.repository.next_codigo(provincia_origem)
        await self._atualizar_integracao(roteiro)
        return await self.repository.save(roteiro)

    async def obter(self, roteiro_id: UUID) -> Roteiro:
        roteiro = await self.repository.get_by_id(roteiro_id)
        if not roteiro:
            raise ValueError("Roteiro nao encontrado")
        return roteiro

    async def listar(
        self, *, municipio_origem: str | None = None, ativo: bool | None = None
    ) -> list[Roteiro]:
        return await self.repository.list(municipio_origem=municipio_origem, ativo=ativo)

    async def atualizar(
        self,
        roteiro_id: UUID,
        *,
        titulo: str | None = None,
        descricao: str | None = None,
        municipio_origem: str | None = None,
        provincia_origem: str | None = None,
        duracao_horas: int | None = None,
        pontos_parada: list[str] | None = None,
        acessivel: bool | None = None,
        valor_estimado: Decimal | None = None,
        observacoes: str | None = None,
        ativo: bool | None = None,
        refresh_integracoes: bool = True,
    ) -> Roteiro:
        roteiro = await self.obter(roteiro_id)
        roteiro.atualizar(
            titulo=titulo,
            descricao=descricao,
            municipio_origem=municipio_origem,
            provincia_origem=provincia_origem,
            duracao_horas=duracao_horas,
            pontos_parada=pontos_parada,
            acessivel=acessivel,
            valor_estimado=valor_estimado,
            observacoes=observacoes,
        )
        if ativo is True:
            roteiro.ativar()
        if ativo is False:
            roteiro.desativar()
        if refresh_integracoes:
            await self._atualizar_integracao(roteiro)
        return await self.repository.save(roteiro)

    async def remover(self, roteiro_id: UUID) -> None:
        deleted = await self.repository.delete(roteiro_id)
        if not deleted:
            raise ValueError("Roteiro nao encontrado")

    async def _atualizar_integracao(self, roteiro: Roteiro) -> None:
        meios_transporte: list[str] = []
        parceiros: list[str] = []
        if self.transportes_service is not None:
            meios_transporte = await self.transportes_service.list_opcoes_transporte(
                origem=roteiro.municipio_origem,
                destino=roteiro.pontos_parada[-1]
                if roteiro.pontos_parada
                else roteiro.municipio_origem,
            )
        if self.comercio_service is not None:
            parceiros = await self.comercio_service.list_parceiros_turisticos(
                municipio=roteiro.municipio_origem
            )
        roteiro.atualizar_integracoes(
            meios_transporte_sugeridos=meios_transporte, parceiros_comerciais=parceiros
        )
