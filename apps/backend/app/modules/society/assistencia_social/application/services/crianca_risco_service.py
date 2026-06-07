from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    CriancaRiscoRepositoryPort,
    EducacaoServicePort,
    RequestServicePort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.models import CriancaRisco


class CriancaRiscoService:
    def __init__(
        self,
        *,
        crianca_repo: CriancaRiscoRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        educacao_service: EducacaoServicePort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.crianca_repo = crianca_repo
        self.beneficiario_repo = beneficiario_repo
        self.educacao_service = educacao_service
        self.request_service = request_service

    async def registrar_crianca_risco(
        self,
        *,
        beneficiario_id: UUID,
        citizen_id_crianca: UUID,
        idade: int,
        motivo: str,
        escolarizada: bool,
    ) -> CriancaRisco:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado")
        if idade < 0 or idade > 17:
            raise ValueError("Idade da crianca em risco deve estar entre 0 e 17")
        estudante_ativo = await self.educacao_service.is_estudante_ativo(citizen_id_crianca)
        status_escolar = escolarizada and estudante_ativo
        codigo = next_codigo("CRI", len(await self.crianca_repo.list_all()))
        item = CriancaRisco.registrar(
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            citizen_id_crianca=citizen_id_crianca,
            idade=idade,
            motivo=motivo,
            escolarizada=status_escolar,
        )
        saved = await self.crianca_repo.save(item)
        if self.request_service is not None and (not status_escolar):
            await self.request_service.create_request(
                request_type="ASSISTENCIA_CRIANCA_FORA_ESCOLA",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
                metadata={"citizen_id_crianca": str(citizen_id_crianca)},
            )
        return saved

    async def buscar_crianca_risco(self, item_id: UUID) -> CriancaRisco:
        item = await self.crianca_repo.get_by_id(item_id)
        if item is None:
            raise ValueError("Registro de crianca em risco nao encontrado")
        return item

    async def listar_criancas_risco(
        self, beneficiario_id: UUID | None = None
    ) -> list[CriancaRisco]:
        if beneficiario_id is not None:
            return await self.crianca_repo.list_by_beneficiario(beneficiario_id)
        return await self.crianca_repo.list_all()

    async def encerrar_crianca_risco(self, item_id: UUID) -> CriancaRisco:
        item = await self.buscar_crianca_risco(item_id)
        item.encerrar_acompanhamento()
        return await self.crianca_repo.save(item)

    async def remover_crianca_risco(self, item_id: UUID) -> None:
        if not await self.crianca_repo.delete(item_id):
            raise ValueError("Registro de crianca em risco nao encontrado")
