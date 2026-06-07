from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.cultura.application.ports.espaco_cultural_repository_port import (
    EspacoCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.cultura.domain.enums import TipoEspacoCultural
from apps.backend.app.modules.society.cultura.domain.models.espaco_cultural import EspacoCultural


class EspacoCulturalService:
    def __init__(
        self,
        *,
        espaco_repo: EspacoCulturalRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.espaco_repo = espaco_repo
        self.request_service = request_service

    async def cadastrar_espaco(
        self,
        *,
        nome: str,
        tipo: TipoEspacoCultural,
        municipio: str,
        provincia: str,
        endereco: str,
        capacidade: int,
        area_m2: float,
        administracao: str,
        responsavel_cpf: str,
        orgao_gestor: str | None = None,
        ano_inauguracao: int | None = None,
        acessibilidade: bool = False,
        observacoes: str | None = None,
    ) -> EspacoCultural:
        codigo = await self.espaco_repo.next_codigo()
        espaco = EspacoCultural.cadastrar(
            codigo_espaco=codigo,
            nome=nome,
            tipo=tipo,
            municipio=municipio,
            provincia=provincia,
            endereco=endereco,
            capacidade=capacidade,
            area_m2=area_m2,
            administracao=administracao,
            responsavel_cpf=responsavel_cpf,
            orgao_gestor=orgao_gestor,
            ano_inauguracao=ano_inauguracao,
            acessibilidade=acessibilidade,
            observacoes=observacoes,
        )
        saved = await self.espaco_repo.save(espaco)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_ESPACO_CULTURAL",
                entity_id=saved.id,
                numero_processo=saved.codigo_espaco,
                metadata={
                    "codigo_espaco": saved.codigo_espaco,
                    "tipo": saved.tipo.value,
                    "municipio": saved.municipio,
                },
            )
        return saved

    async def buscar_espaco(self, espaco_id: UUID) -> EspacoCultural:
        item = await self.espaco_repo.get_by_id(espaco_id)
        if item is None:
            raise ValueError("Espaco cultural nao encontrado")
        return item

    async def listar_espacos(
        self,
        *,
        tipo: TipoEspacoCultural | None = None,
        municipio: str | None = None,
        somente_ativos: bool = True,
    ) -> list[EspacoCultural]:
        if tipo is not None:
            items = await self.espaco_repo.list_by_tipo(tipo)
        elif municipio is not None:
            items = await self.espaco_repo.list_by_municipio(municipio)
        else:
            items = await self.espaco_repo.list_all()
        if somente_ativos:
            return [item for item in items if item.ativo]
        return items

    async def atualizar_espaco(
        self,
        *,
        espaco_id: UUID,
        nome: str | None = None,
        tipo: TipoEspacoCultural | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        endereco: str | None = None,
        capacidade: int | None = None,
        area_m2: float | None = None,
        administracao: str | None = None,
        responsavel_cpf: str | None = None,
        orgao_gestor: str | None = None,
        ano_inauguracao: int | None = None,
        acessibilidade: bool | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> EspacoCultural:
        item = await self.buscar_espaco(espaco_id)
        item.atualizar(
            nome=nome,
            tipo=tipo,
            municipio=municipio,
            provincia=provincia,
            endereco=endereco,
            capacidade=capacidade,
            area_m2=area_m2,
            administracao=administracao,
            responsavel_cpf=responsavel_cpf,
            orgao_gestor=orgao_gestor,
            ano_inauguracao=ano_inauguracao,
            acessibilidade=acessibilidade,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.espaco_repo.save(item)

    async def remover_espaco(self, espaco_id: UUID) -> None:
        deleted = await self.espaco_repo.delete(espaco_id)
        if not deleted:
            raise ValueError("Espaco cultural nao encontrado")
