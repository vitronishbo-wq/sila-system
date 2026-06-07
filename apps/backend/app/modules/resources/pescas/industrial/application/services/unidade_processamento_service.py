from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.resources.pescas.industrial.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.resources.pescas.industrial.application.ports.industria_service_port import (
    IndustriaServicePort,
)
from apps.backend.app.modules.resources.pescas.industrial.application.ports.pescas_service_port import (
    PescasServicePort,
)
from apps.backend.app.modules.resources.pescas.industrial.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.resources.pescas.industrial.application.ports.unidade_processamento_repository_port import (
    UnidadeProcessamentoRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    ClassificacaoIndustrial,
    TipoProcessamento,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.models.unidade_processamento import (
    UnidadeProcessamento,
)


class UnidadeProcessamentoService:
    def __init__(
        self,
        *,
        unidade_repo: UnidadeProcessamentoRepositoryPort,
        pescas_service: PescasServicePort,
        industria_service: IndustriaServicePort,
        citizen_service: CitizenServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.unidade_repo = unidade_repo
        self.pescas_service = pescas_service
        self.industria_service = industria_service
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_unidade(
        self,
        *,
        cnpj: str,
        razao_social: str,
        tipo_processamento: list[TipoProcessamento],
        classificacao: ClassificacaoIndustrial,
        capacidade_kg_dia: Decimal,
        area_total_m2: Decimal,
        area_producao_m2: Decimal,
        area_armazenagem_m2: Decimal,
        numero_funcionarios: int,
        endereco: str,
        municipio: str,
        provincia: str,
        armador_id: UUID | None = None,
        responsavel_tecnico_id: UUID | None = None,
    ) -> UnidadeProcessamento:
        if await self.unidade_repo.get_by_cnpj(cnpj):
            raise ValueError("Unidade ja cadastrada com este CNPJ")
        if not await self.industria_service.cnpj_ativo(cnpj):
            raise ValueError("CNPJ sem conformidade no modulo industria")
        if armador_id and (not await self.pescas_service.armador_exists(armador_id)):
            raise ValueError("Armador nao encontrado no modulo pescas")
        if responsavel_tecnico_id and self.citizen_service is not None:
            ativo = await self.citizen_service.is_citizen_active(responsavel_tecnico_id)
            if not ativo:
                raise ValueError("Responsavel tecnico nao encontrado ou inativo")
        unidade = UnidadeProcessamento.cadastrar(
            cnpj=cnpj,
            razao_social=razao_social,
            tipo_processamento=tipo_processamento,
            classificacao=classificacao,
            capacidade_kg_dia=capacidade_kg_dia,
            area_total_m2=area_total_m2,
            area_producao_m2=area_producao_m2,
            area_armazenagem_m2=area_armazenagem_m2,
            numero_funcionarios=numero_funcionarios,
            endereco=endereco,
            municipio=municipio,
            provincia=provincia,
        )
        unidade.armador_id = armador_id
        unidade.responsavel_tecnico_id = responsavel_tecnico_id
        saved = await self.unidade_repo.save(unidade)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_UNIDADE_PROCESSAMENTO",
                entity_id=saved.id,
                metadata={
                    "cnpj": saved.cnpj,
                    "razao_social": saved.razao_social,
                    "municipio": saved.municipio,
                    "capacidade_kg_dia": str(saved.capacidade_kg_dia),
                },
                citizen_id=responsavel_tecnico_id,
                numero_processo=saved.cnpj,
            )
        return saved

    async def buscar_unidade(self, unidade_id: UUID) -> UnidadeProcessamento:
        item = await self.unidade_repo.get_by_id(unidade_id)
        if not item:
            raise ValueError("Unidade de processamento nao encontrada")
        return item

    async def listar_unidades(self, municipio: str | None = None) -> list[UnidadeProcessamento]:
        if municipio:
            return await self.unidade_repo.list_by_municipio(municipio)
        return await self.unidade_repo.list_all()

    async def listar_unidades_por_tipo(self, tipo: TipoProcessamento) -> list[UnidadeProcessamento]:
        return await self.unidade_repo.list_by_tipo(tipo)

    async def atualizar_capacidade(
        self, unidade_id: UUID, capacidade_kg_dia: Decimal
    ) -> UnidadeProcessamento:
        item = await self.buscar_unidade(unidade_id)
        item.atualizar_capacidade(capacidade_kg_dia)
        return await self.unidade_repo.save(item)

    async def remover_unidade(self, unidade_id: UUID) -> None:
        deleted = await self.unidade_repo.delete(unidade_id)
        if not deleted:
            raise ValueError("Unidade de processamento nao encontrada")
