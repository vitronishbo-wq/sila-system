from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    RequestServicePort,
    SituacaoRuaRepositoryPort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.models import SituacaoRua


class SituacaoRuaService:
    def __init__(
        self,
        *,
        situacao_repo: SituacaoRuaRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.situacao_repo = situacao_repo
        self.beneficiario_repo = beneficiario_repo
        self.request_service = request_service

    async def registrar_situacao(
        self, *, beneficiario_id: UUID, localizacao: str, motivo: str
    ) -> SituacaoRua:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado")
        codigo = next_codigo("SRU", len(await self.situacao_repo.list_all()))
        item = SituacaoRua.registrar(
            codigo=codigo, beneficiario_id=beneficiario_id, localizacao=localizacao, motivo=motivo
        )
        saved = await self.situacao_repo.save(item)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ASSISTENCIA_SITUACAO_RUA",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
            )
        return saved

    async def buscar_situacao(self, situacao_id: UUID) -> SituacaoRua:
        item = await self.situacao_repo.get_by_id(situacao_id)
        if item is None:
            raise ValueError("Registro de situacao de rua nao encontrado")
        return item

    async def listar_situacoes(self, beneficiario_id: UUID | None = None) -> list[SituacaoRua]:
        if beneficiario_id is not None:
            return await self.situacao_repo.list_by_beneficiario(beneficiario_id)
        return await self.situacao_repo.list_all()

    async def encerrar_situacao(self, situacao_id: UUID) -> SituacaoRua:
        item = await self.buscar_situacao(situacao_id)
        item.encerrar()
        return await self.situacao_repo.save(item)

    async def remover_situacao(self, situacao_id: UUID) -> None:
        if not await self.situacao_repo.delete(situacao_id):
            raise ValueError("Registro de situacao de rua nao encontrado")
