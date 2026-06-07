from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.logistics.domain.enums import StatusFrota, TipoTarifa
from apps.backend.app.modules.logistics.domain.models import Frota
from apps.backend.app.modules.logistics.domain.ports import (
    FinancasServicePort,
    FrotaRepositoryPort,
    SegurancaPublicaServicePort,
    ServiceRequestsServicePort,
    WorkflowServicePort,
)
from apps.backend.app.modules.logistics.domain.services import FrotaDomainService


class FrotaService:
    def __init__(
        self,
        *,
        frota_repo: FrotaRepositoryPort,
        workflow_adapter: WorkflowServicePort | None = None,
        service_requests_adapter: ServiceRequestsServicePort | None = None,
        financas_adapter: FinancasServicePort | None = None,
        seguranca_publica_adapter: SegurancaPublicaServicePort | None = None,
    ) -> None:
        self._domain = FrotaDomainService(
            frota_repo=frota_repo,
            workflow_adapter=workflow_adapter,
            service_requests_adapter=service_requests_adapter,
            financas_adapter=financas_adapter,
            seguranca_publica_adapter=seguranca_publica_adapter,
        )

    def has_workflow_adapter(self) -> bool:
        return self._domain.has_workflow_adapter()

    def has_service_requests_adapter(self) -> bool:
        return self._domain.has_service_requests_adapter()

    async def criar_frota(
        self,
        *,
        nome: str,
        operadora_id: UUID,
        municipio: str,
        provincia: str,
        codigo_frota: str | None = None,
        observacoes: str | None = None,
    ) -> Frota:
        return await self._domain.criar_frota(
            nome=nome,
            operadora_id=operadora_id,
            municipio=municipio,
            provincia=provincia,
            codigo_frota=codigo_frota,
            observacoes=observacoes,
        )

    async def adicionar_veiculo(
        self,
        codigo_frota: str,
        *,
        veiculo_id: UUID,
        placa: str,
        tipo: str,
        capacidade: int | None = None,
    ) -> Frota:
        return await self._domain.adicionar_veiculo(
            codigo_frota, veiculo_id=veiculo_id, placa=placa, tipo=tipo, capacidade=capacidade
        )

    async def registrar_manutencao(
        self,
        codigo_frota: str,
        *,
        veiculo_id: UUID,
        tipo: str,
        oficina: str,
        custo: Decimal,
        data_manutencao: date | None = None,
        observacoes: str | None = None,
    ) -> Frota:
        return await self._domain.registrar_manutencao(
            codigo_frota,
            veiculo_id=veiculo_id,
            tipo=tipo,
            oficina=oficina,
            custo=custo,
            data_manutencao=data_manutencao,
            observacoes=observacoes,
        )

    async def atualizar_tarifa(
        self,
        codigo_frota: str,
        *,
        tipo_tarifa: TipoTarifa,
        valor: Decimal,
        motivo: str,
        data_inicio_vigencia: date | None = None,
        data_fim_vigencia: date | None = None,
    ) -> Frota:
        return await self._domain.atualizar_tarifa(
            codigo_frota,
            tipo_tarifa=tipo_tarifa,
            valor=valor,
            motivo=motivo,
            data_inicio_vigencia=data_inicio_vigencia,
            data_fim_vigencia=data_fim_vigencia,
        )

    async def registrar_fiscalizacao(
        self,
        codigo_frota: str,
        *,
        fiscal_id: UUID,
        conformidade: bool,
        apontamentos: str,
        data_fiscalizacao: date | None = None,
        auto_infracao: str | None = None,
        observacoes: str | None = None,
    ) -> Frota:
        return await self._domain.registrar_fiscalizacao(
            codigo_frota,
            fiscal_id=fiscal_id,
            conformidade=conformidade,
            apontamentos=apontamentos,
            data_fiscalizacao=data_fiscalizacao,
            auto_infracao=auto_infracao,
            observacoes=observacoes,
        )

    async def obter_por_codigo(self, codigo_frota: str) -> Frota:
        return await self._domain.obter_por_codigo(codigo_frota)

    async def listar(
        self,
        *,
        status: StatusFrota | None = None,
        operadora_id: UUID | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
    ) -> list[Frota]:
        return await self._domain.listar(
            status=status, operadora_id=operadora_id, municipio=municipio, provincia=provincia
        )
