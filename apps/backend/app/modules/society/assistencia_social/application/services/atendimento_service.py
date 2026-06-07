from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    AtendimentoRepositoryPort,
    BeneficiarioRepositoryPort,
    RequestServicePort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import TipoAtendimento
from apps.backend.app.modules.society.assistencia_social.domain.models import Atendimento


class AtendimentoService:
    def __init__(
        self,
        *,
        atendimento_repo: AtendimentoRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.atendimento_repo = atendimento_repo
        self.beneficiario_repo = beneficiario_repo
        self.request_service = request_service

    async def registrar_atendimento(
        self,
        *,
        beneficiario_id: UUID,
        tipo: TipoAtendimento,
        descricao: str,
        responsavel_id: UUID,
        encaminhamentos: list[dict] | None = None,
    ) -> Atendimento:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado para atendimento")
        codigo = next_codigo("ATD", len(await self.atendimento_repo.list_all()))
        entity = Atendimento.registrar(
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            tipo=tipo,
            descricao=descricao,
            responsavel_id=responsavel_id,
            encaminhamentos=encaminhamentos,
        )
        saved = await self.atendimento_repo.save(entity)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ASSISTENCIA_ATENDIMENTO",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
                metadata={"tipo": saved.tipo.value},
            )
        return saved

    async def buscar_atendimento(self, atendimento_id: UUID) -> Atendimento:
        item = await self.atendimento_repo.get_by_id(atendimento_id)
        if item is None:
            raise ValueError("Atendimento nao encontrado")
        return item

    async def listar_atendimentos(self, beneficiario_id: UUID | None = None) -> list[Atendimento]:
        if beneficiario_id is not None:
            return await self.atendimento_repo.list_by_beneficiario(beneficiario_id)
        return await self.atendimento_repo.list_all()

    async def encerrar_atendimento(self, atendimento_id: UUID) -> Atendimento:
        item = await self.buscar_atendimento(atendimento_id)
        item.encerrar()
        return await self.atendimento_repo.save(item)

    async def remover_atendimento(self, atendimento_id: UUID) -> None:
        if not await self.atendimento_repo.delete(atendimento_id):
            raise ValueError("Atendimento nao encontrado")
