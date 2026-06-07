from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    CadastroUnicoRepositoryPort,
    CitizenServicePort,
    RequestServicePort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade
from apps.backend.app.modules.society.assistencia_social.domain.models import Beneficiario


class BeneficiarioService:
    def __init__(
        self,
        *,
        beneficiario_repo: BeneficiarioRepositoryPort,
        citizen_service: CitizenServicePort,
        cadastro_unico_repo: CadastroUnicoRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.beneficiario_repo = beneficiario_repo
        self.citizen_service = citizen_service
        self.cadastro_unico_repo = cadastro_unico_repo
        self.request_service = request_service

    async def cadastrar_beneficiario(
        self,
        *,
        citizen_id: UUID,
        faixa_vulnerabilidade: FaixaVulnerabilidade,
        cadastro_unico_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Beneficiario:
        if not await self.citizen_service.is_citizen_active(citizen_id):
            raise ValueError("Cidadao inexistente ou inativo")
        existente = await self.beneficiario_repo.get_by_citizen(citizen_id)
        if existente is not None and existente.ativo:
            raise ValueError("Cidadao ja possui beneficiario ativo")
        if cadastro_unico_id is not None:
            cadastro = await self.cadastro_unico_repo.get_by_id(cadastro_unico_id)
            if cadastro is None:
                raise ValueError("Cadastro unico informado nao encontrado")
        codigo = next_codigo("BEN", len(await self.beneficiario_repo.list_all()))
        entity = Beneficiario.cadastrar(
            numero_registro=codigo,
            citizen_id=citizen_id,
            cadastro_unico_id=cadastro_unico_id,
            faixa_vulnerabilidade=faixa_vulnerabilidade,
            observacoes=observacoes,
        )
        saved = await self.beneficiario_repo.save(entity)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ASSISTENCIA_CADASTRO_BENEFICIARIO",
                entity_id=saved.id,
                citizen_id=saved.citizen_id,
                numero_processo=saved.numero_registro,
                metadata={"faixa_vulnerabilidade": saved.faixa_vulnerabilidade.value},
            )
        return saved

    async def buscar_beneficiario(self, beneficiario_id: UUID) -> Beneficiario:
        item = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if item is None:
            raise ValueError("Beneficiario nao encontrado")
        return item

    async def listar_beneficiarios(self) -> list[Beneficiario]:
        return await self.beneficiario_repo.list_all()

    async def suspender_beneficiario(
        self, beneficiario_id: UUID, motivo: str | None = None
    ) -> Beneficiario:
        item = await self.buscar_beneficiario(beneficiario_id)
        item.suspender(motivo)
        return await self.beneficiario_repo.save(item)

    async def inativar_beneficiario(
        self, beneficiario_id: UUID, motivo: str | None = None
    ) -> Beneficiario:
        item = await self.buscar_beneficiario(beneficiario_id)
        item.inativar(motivo)
        return await self.beneficiario_repo.save(item)

    async def remover_beneficiario(self, beneficiario_id: UUID) -> None:
        if not await self.beneficiario_repo.delete(beneficiario_id):
            raise ValueError("Beneficiario nao encontrado")
