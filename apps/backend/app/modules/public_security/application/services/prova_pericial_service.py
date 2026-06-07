from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.public_security.application.ports.ocorrencia_repository_port import (
    OcorrenciaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.policial_repository_port import (
    PolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.prova_pericial_repository_port import (
    ProvaPericialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.public_security.domain.enums import StatusProva, TipoProva
from apps.backend.app.modules.public_security.domain.models.prova_pericial import ProvaPericial


class ProvaPericialService:
    def __init__(
        self,
        *,
        prova_repo: ProvaPericialRepositoryPort,
        ocorrencia_repo: OcorrenciaRepositoryPort,
        policial_repo: PolicialRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.prova_repo = prova_repo
        self.ocorrencia_repo = ocorrencia_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def coletar_prova(
        self,
        *,
        ocorrencia_id: UUID,
        tipo: TipoProva,
        descricao: str,
        local_coleta: str,
        data_coleta: date | None = None,
        coletado_por_id: UUID | None = None,
        observacoes: str | None = None,
        citizen_id: UUID | None = None,
    ) -> ProvaPericial:
        ocorrencia = await self.ocorrencia_repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise ValueError("Ocorrencia nao encontrada para coleta de prova")
        if coletado_por_id is not None:
            coletor = await self.policial_repo.get_by_id(coletado_por_id)
            if coletor is None:
                raise ValueError("Responsavel pela coleta da prova nao encontrado")
        codigo = await self.prova_repo.next_codigo()
        prova = ProvaPericial.coletar(
            codigo_prova=codigo,
            ocorrencia_id=ocorrencia_id,
            tipo=tipo,
            descricao=descricao,
            local_coleta=local_coleta,
            data_coleta=data_coleta,
            coletado_por_id=coletado_por_id,
            observacoes=observacoes,
        )
        saved = await self.prova_repo.save(prova)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="COLETA_PROVA_PERICIAL",
                entity_id=saved.id,
                numero_processo=saved.codigo_prova,
                citizen_id=citizen_id,
                metadata={
                    "codigo_prova": saved.codigo_prova,
                    "ocorrencia_id": str(saved.ocorrencia_id),
                    "tipo": saved.tipo.value,
                },
            )
        return saved

    async def buscar_prova(self, prova_id: UUID) -> ProvaPericial:
        prova = await self.prova_repo.get_by_id(prova_id)
        if prova is None:
            raise ValueError("Prova pericial nao encontrada")
        return prova

    async def listar_provas(
        self,
        *,
        ocorrencia_id: UUID | None = None,
        tipo: TipoProva | None = None,
        status: StatusProva | None = None,
    ) -> list[ProvaPericial]:
        if ocorrencia_id is not None:
            return await self.prova_repo.list_by_ocorrencia(ocorrencia_id)
        if tipo is not None:
            return await self.prova_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.prova_repo.list_by_status(status)
        return await self.prova_repo.list_all()

    async def atualizar_status(
        self, *, prova_id: UUID, status: StatusProva, observacoes: str | None = None
    ) -> ProvaPericial:
        prova = await self.buscar_prova(prova_id)
        prova.atualizar_status(status, observacoes)
        return await self.prova_repo.save(prova)

    async def vincular_cadeia_custodia(
        self, *, prova_id: UUID, cadeia_custodia_id: UUID
    ) -> ProvaPericial:
        prova = await self.buscar_prova(prova_id)
        prova.vincular_cadeia_custodia(cadeia_custodia_id)
        return await self.prova_repo.save(prova)

    async def remover_prova(self, prova_id: UUID) -> None:
        deleted = await self.prova_repo.delete(prova_id)
        if not deleted:
            raise ValueError("Prova pericial nao encontrada")
