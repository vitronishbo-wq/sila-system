from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    IdosoVulneravelRepositoryPort,
    RequestServicePort,
    SaudeServicePort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.models import IdosoVulneravel


class IdosoVulneravelService:
    def __init__(
        self,
        *,
        idoso_repo: IdosoVulneravelRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        saude_service: SaudeServicePort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.idoso_repo = idoso_repo
        self.beneficiario_repo = beneficiario_repo
        self.saude_service = saude_service
        self.request_service = request_service

    async def registrar_idoso(
        self,
        *,
        beneficiario_id: UUID,
        citizen_id_idoso: UUID,
        idade: int,
        dependencia: bool,
        precisa_cuidados: bool,
    ) -> IdosoVulneravel:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado")
        if idade < 60:
            raise ValueError("Idoso vulneravel deve ter 60 anos ou mais")
        codigo = next_codigo("IDO", len(await self.idoso_repo.list_all()))
        item = IdosoVulneravel.registrar(
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            citizen_id_idoso=citizen_id_idoso,
            idade=idade,
            dependencia=dependencia,
            precisa_cuidados=precisa_cuidados,
        )
        saved = await self.idoso_repo.save(item)
        cobertura_ok = await self.saude_service.verificar_cobertura_idoso(
            citizen_id=citizen_id_idoso
        )
        if self.request_service is not None and (not cobertura_ok):
            await self.request_service.create_request(
                request_type="ASSISTENCIA_IDOSO_SEM_COBERTURA_SAUDE",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
            )
        return saved

    async def buscar_idoso(self, item_id: UUID) -> IdosoVulneravel:
        item = await self.idoso_repo.get_by_id(item_id)
        if item is None:
            raise ValueError("Registro de idoso vulneravel nao encontrado")
        return item

    async def listar_idosos(self, beneficiario_id: UUID | None = None) -> list[IdosoVulneravel]:
        if beneficiario_id is not None:
            return await self.idoso_repo.list_by_beneficiario(beneficiario_id)
        return await self.idoso_repo.list_all()

    async def encerrar_idoso(self, item_id: UUID) -> IdosoVulneravel:
        item = await self.buscar_idoso(item_id)
        item.encerrar_acompanhamento()
        return await self.idoso_repo.save(item)

    async def remover_idoso(self, item_id: UUID) -> None:
        if not await self.idoso_repo.delete(item_id):
            raise ValueError("Registro de idoso vulneravel nao encontrado")
