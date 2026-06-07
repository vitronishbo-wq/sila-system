from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.public_security.application.ports.investigacao_repository_port import (
    InvestigacaoRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.ocorrencia_repository_port import (
    OcorrenciaRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.policial_repository_port import (
    PolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.public_security.domain.enums import StatusInvestigacao
from apps.backend.app.modules.public_security.domain.models.investigacao import Investigacao


class InvestigacaoService:
    def __init__(
        self,
        *,
        investigacao_repo: InvestigacaoRepositoryPort,
        ocorrencia_repo: OcorrenciaRepositoryPort,
        policial_repo: PolicialRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.investigacao_repo = investigacao_repo
        self.ocorrencia_repo = ocorrencia_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def abrir_investigacao(
        self,
        *,
        ocorrencia_id: UUID,
        delegado_responsavel_id: UUID | None = None,
        resumo: str | None = None,
        observacoes: str | None = None,
        citizen_id: UUID | None = None,
    ) -> Investigacao:
        ocorrencia = await self.ocorrencia_repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise ValueError("Ocorrencia nao encontrada para abertura de investigacao")
        if delegado_responsavel_id is not None:
            delegado = await self.policial_repo.get_by_id(delegado_responsavel_id)
            if delegado is None:
                raise ValueError("Delegado responsavel nao encontrado")
            if delegado.unidade_id != ocorrencia.unidade_id:
                raise ValueError("Delegado responsavel nao pertence a unidade da ocorrencia")
        codigo = await self.investigacao_repo.next_codigo()
        investigacao = Investigacao.abrir(
            codigo_investigacao=codigo,
            ocorrencia_id=ocorrencia_id,
            unidade_id=ocorrencia.unidade_id,
            delegado_responsavel_id=delegado_responsavel_id,
            resumo=resumo,
            observacoes=observacoes,
        )
        saved = await self.investigacao_repo.save(investigacao)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ABERTURA_INVESTIGACAO",
                entity_id=saved.id,
                numero_processo=saved.codigo_investigacao,
                citizen_id=citizen_id,
                metadata={
                    "codigo_investigacao": saved.codigo_investigacao,
                    "ocorrencia_id": str(saved.ocorrencia_id),
                    "unidade_id": str(saved.unidade_id),
                },
            )
        return saved

    async def buscar_investigacao(self, investigacao_id: UUID) -> Investigacao:
        investigacao = await self.investigacao_repo.get_by_id(investigacao_id)
        if investigacao is None:
            raise ValueError("Investigacao nao encontrada")
        return investigacao

    async def listar_investigacoes(
        self, *, ocorrencia_id: UUID | None = None, status: StatusInvestigacao | None = None
    ) -> list[Investigacao]:
        if ocorrencia_id is not None:
            return await self.investigacao_repo.list_by_ocorrencia(ocorrencia_id)
        if status is not None:
            return await self.investigacao_repo.list_by_status(status)
        return await self.investigacao_repo.list_all()

    async def atualizar_status(
        self, *, investigacao_id: UUID, status: StatusInvestigacao, observacoes: str | None = None
    ) -> Investigacao:
        investigacao = await self.buscar_investigacao(investigacao_id)
        investigacao.atualizar_status(status, observacoes)
        return await self.investigacao_repo.save(investigacao)

    async def remover_investigacao(self, investigacao_id: UUID) -> None:
        deleted = await self.investigacao_repo.delete(investigacao_id)
        if not deleted:
            raise ValueError("Investigacao nao encontrada")
