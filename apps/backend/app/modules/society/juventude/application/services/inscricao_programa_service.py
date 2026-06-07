from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.juventude.application.ports.inscricao_programa_repository_port import (
    InscricaoProgramaRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import (
    JovemRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.ports.programa_repository_port import (
    ProgramaRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusInscricao, StatusPrograma
from apps.backend.app.modules.society.juventude.domain.models.inscricao_programa import (
    InscricaoPrograma,
)


class InscricaoProgramaService:
    def __init__(
        self,
        *,
        inscricao_repo: InscricaoProgramaRepositoryPort,
        jovem_repo: JovemRepositoryPort,
        programa_repo: ProgramaRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.inscricao_repo = inscricao_repo
        self.jovem_repo = jovem_repo
        self.programa_repo = programa_repo
        self.request_service = request_service

    async def inscrever_jovem(
        self,
        *,
        programa_id: UUID,
        jovem_id: UUID,
        prioridade: int = 0,
        observacoes: str | None = None,
    ) -> InscricaoPrograma:
        jovem = await self.jovem_repo.get_by_id(jovem_id)
        if jovem is None:
            raise ValueError("Jovem nao encontrado para inscricao em programa")
        programa = await self.programa_repo.get_by_id(programa_id)
        if programa is None:
            raise ValueError("Programa nao encontrado para inscricao")
        if programa.status not in {StatusPrograma.INSCRICOES_ABERTAS, StatusPrograma.ATIVO}:
            raise ValueError("Programa nao esta em periodo valido para inscricoes")
        if await self.inscricao_repo.exists_active_by_jovem_programa(jovem_id, programa_id):
            raise ValueError("Jovem ja possui inscricao ativa para este programa")
        if programa.vagas is not None:
            confirmadas = await self.inscricao_repo.count_confirmadas_by_programa(programa_id)
            if confirmadas >= programa.vagas:
                raise ValueError("Programa sem vagas disponiveis para novas inscricoes")
        codigo = await self.inscricao_repo.next_codigo()
        inscricao = InscricaoPrograma.inscrever(
            codigo_inscricao=codigo,
            programa_id=programa_id,
            jovem_id=jovem_id,
            prioridade=prioridade,
            observacoes=observacoes,
        )
        saved = await self.inscricao_repo.save(inscricao)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="INSCRICAO_PROGRAMA_JUVENTUDE",
                entity_id=saved.id,
                citizen_id=jovem.citizen_id,
                numero_processo=saved.codigo_inscricao,
                metadata={
                    "programa_id": str(saved.programa_id),
                    "prioridade": saved.prioridade,
                    "status": saved.status.value,
                },
            )
        return saved

    async def buscar_inscricao(self, inscricao_id: UUID) -> InscricaoPrograma:
        item = await self.inscricao_repo.get_by_id(inscricao_id)
        if item is None:
            raise ValueError("Inscricao nao encontrada")
        return item

    async def listar_inscricoes(
        self,
        *,
        jovem_id: UUID | None = None,
        programa_id: UUID | None = None,
        status: StatusInscricao | None = None,
    ) -> list[InscricaoPrograma]:
        if jovem_id is not None:
            return await self.inscricao_repo.list_by_jovem(jovem_id)
        if programa_id is not None:
            return await self.inscricao_repo.list_by_programa(programa_id)
        if status is not None:
            return await self.inscricao_repo.list_by_status(status)
        return await self.inscricao_repo.list_all()

    async def confirmar_inscricao(self, inscricao_id: UUID) -> InscricaoPrograma:
        item = await self.buscar_inscricao(inscricao_id)
        item.confirmar()
        return await self.inscricao_repo.save(item)

    async def concluir_inscricao(self, inscricao_id: UUID) -> InscricaoPrograma:
        item = await self.buscar_inscricao(inscricao_id)
        item.concluir()
        return await self.inscricao_repo.save(item)

    async def cancelar_inscricao(
        self, inscricao_id: UUID, motivo: str | None = None
    ) -> InscricaoPrograma:
        item = await self.buscar_inscricao(inscricao_id)
        item.cancelar(motivo)
        return await self.inscricao_repo.save(item)

    async def remover_inscricao(self, inscricao_id: UUID) -> None:
        deleted = await self.inscricao_repo.delete(inscricao_id)
        if not deleted:
            raise ValueError("Inscricao nao encontrada")
