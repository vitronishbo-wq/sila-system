from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    RequestServicePort,
    SaudeServicePort,
    VisitaDomiciliarRepositoryPort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import ResultadoVisita
from apps.backend.app.modules.society.assistencia_social.domain.models import VisitaDomiciliar


class VisitaDomiciliarService:
    def __init__(
        self,
        *,
        visita_repo: VisitaDomiciliarRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        saude_service: SaudeServicePort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.visita_repo = visita_repo
        self.beneficiario_repo = beneficiario_repo
        self.saude_service = saude_service
        self.request_service = request_service

    async def registrar_visita(
        self,
        *,
        beneficiario_id: UUID,
        assistente_social_id: UUID,
        condicoes_moradia: str,
        observacoes: str | None = None,
        recomendacoes: list[str] | None = None,
        resultado: ResultadoVisita = ResultadoVisita.RETORNO_NECESSARIO,
    ) -> VisitaDomiciliar:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado para visita")
        recs = list(recomendacoes or [])
        possui_cobertura = await self.saude_service.verificar_cobertura_idoso(
            citizen_id=beneficiario.citizen_id
        )
        if not possui_cobertura:
            recs.append("Encaminhar familia para avaliacao de cobertura de saude")
        codigo = next_codigo("VIS", len(await self.visita_repo.list_all()))
        entity = VisitaDomiciliar.registrar(
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            assistente_social_id=assistente_social_id,
            condicoes_moradia=condicoes_moradia,
            observacoes=observacoes,
            recomendacoes=recs,
            resultado=resultado,
        )
        saved = await self.visita_repo.save(entity)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ASSISTENCIA_VISITA_DOMICILIAR",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
                metadata={"resultado": saved.resultado.value},
            )
        return saved

    async def buscar_visita(self, visita_id: UUID) -> VisitaDomiciliar:
        item = await self.visita_repo.get_by_id(visita_id)
        if item is None:
            raise ValueError("Visita domiciliar nao encontrada")
        return item

    async def listar_visitas(self, beneficiario_id: UUID | None = None) -> list[VisitaDomiciliar]:
        if beneficiario_id is not None:
            return await self.visita_repo.list_by_beneficiario(beneficiario_id)
        return await self.visita_repo.list_all()

    async def remover_visita(self, visita_id: UUID) -> None:
        if not await self.visita_repo.delete(visita_id):
            raise ValueError("Visita domiciliar nao encontrada")
