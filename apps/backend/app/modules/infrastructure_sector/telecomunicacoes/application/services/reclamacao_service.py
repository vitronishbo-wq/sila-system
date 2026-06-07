from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import (
    ReclamacaoTelecomAbertaEvent,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.assinante_repository_port import (
    AssinanteRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.outbox_repository_port import (
    OutboxRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.reclamacao_repository_port import (
    ReclamacaoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    TipoReclamacaoTelecom,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.reclamacao import (
    Reclamacao,
)


class ReclamacaoService:
    def __init__(
        self,
        *,
        assinante_repo: AssinanteRepositoryPort,
        reclamacao_repo: ReclamacaoRepositoryPort,
        request_service: RequestServicePort | None = None,
        outbox_repo: OutboxRepositoryPort | None = None,
    ) -> None:
        self._assinante_repo = assinante_repo
        self._reclamacao_repo = reclamacao_repo
        self._request_service = request_service
        self._outbox_repo = outbox_repo

    async def criar_reclamacao(
        self, *, assinante_id: UUID, tipo: TipoReclamacaoTelecom, descricao: str, prioridade: str
    ) -> Reclamacao:
        assinante = await self._assinante_repo.get_by_id(assinante_id)
        if assinante is None:
            raise ValueError("Assinante nao encontrado")
        reclamacao = Reclamacao.abrir(
            assinante_id=assinante_id, tipo=tipo, descricao=descricao, prioridade=prioridade
        )
        reclamacao.protocolo = await self._reclamacao_repo.next_protocolo()
        saved = await self._reclamacao_repo.save(reclamacao)
        if self._request_service is not None:
            await self._request_service.create_request(
                request_type="RECLAMACAO_TELECOM",
                entity_id=saved.id,
                citizen_id=assinante.citizen_id,
                numero_processo=saved.protocolo,
                metadata={
                    "tipo": saved.tipo.value,
                    "prioridade": saved.prioridade,
                    "assinante_id": str(saved.assinante_id),
                },
            )
        if self._outbox_repo is not None:
            await self._outbox_repo.enqueue(ReclamacaoTelecomAbertaEvent.from_reclamacao(saved))
        return saved

    async def listar_reclamacoes_assinante(self, assinante_id: UUID) -> list[Reclamacao]:
        return await self._reclamacao_repo.list_by_assinante(assinante_id)
