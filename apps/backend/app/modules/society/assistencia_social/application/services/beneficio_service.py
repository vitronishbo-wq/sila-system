from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    BeneficioRepositoryPort,
    EmpregoServicePort,
    PCDRepositoryPort,
    ProgramaSocialRepositoryPort,
    RequestServicePort,
    SaudeServicePort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import TipoBeneficio
from apps.backend.app.modules.society.assistencia_social.domain.models import Beneficio


class BeneficioService:
    def __init__(
        self,
        *,
        beneficio_repo: BeneficioRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        programa_repo: ProgramaSocialRepositoryPort,
        pcd_repo: PCDRepositoryPort,
        saude_service: SaudeServicePort,
        emprego_service: EmpregoServicePort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.beneficio_repo = beneficio_repo
        self.beneficiario_repo = beneficiario_repo
        self.programa_repo = programa_repo
        self.pcd_repo = pcd_repo
        self.saude_service = saude_service
        self.emprego_service = emprego_service
        self.request_service = request_service

    async def solicitar_beneficio(
        self,
        *,
        beneficiario_id: UUID,
        tipo: TipoBeneficio,
        valor: Decimal,
        programa_social_id: UUID | None = None,
    ) -> Beneficio:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado")
        if programa_social_id is not None:
            programa = await self.programa_repo.get_by_id(programa_social_id)
            if programa is None:
                raise ValueError("Programa social nao encontrado")
        codigo = next_codigo("BNF", len(await self.beneficio_repo.list_all()))
        entity = Beneficio.solicitar(
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            programa_social_id=programa_social_id,
            tipo=tipo,
            valor=valor,
        )
        saved = await self.beneficio_repo.save(entity)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ASSISTENCIA_SOLICITACAO_BENEFICIO",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
                metadata={"tipo": saved.tipo.value, "valor": str(saved.valor)},
            )
        return saved

    async def conceder_bpc_pcd(
        self, *, beneficiario_id: UUID, pcd_id: UUID, valor: Decimal
    ) -> Beneficio:
        pcd = await self.pcd_repo.get_by_id(pcd_id)
        if pcd is None:
            raise ValueError("Registro PcD nao encontrado")
        if not await self.saude_service.validar_laudo_pcd(
            citizen_id=pcd.citizen_id_pcd, laudo_id=pcd.laudo_id, cid=pcd.cid
        ):
            raise ValueError("Laudo medico invalido para concessao de BPC")
        if await self.emprego_service.has_beneficio_previdenciario(pcd.citizen_id_pcd):
            raise ValueError("Cidadao ja possui beneficio previdenciario ativo")
        beneficio = await self.solicitar_beneficio(
            beneficiario_id=beneficiario_id, tipo=TipoBeneficio.BPC_PCD, valor=valor
        )
        beneficio.aprovar()
        saved = await self.beneficio_repo.save(beneficio)
        pcd.ativar_bpc()
        await self.pcd_repo.save(pcd)
        return saved

    async def buscar_beneficio(self, beneficio_id: UUID) -> Beneficio:
        item = await self.beneficio_repo.get_by_id(beneficio_id)
        if item is None:
            raise ValueError("Beneficio nao encontrado")
        return item

    async def listar_beneficios(self, beneficiario_id: UUID | None = None) -> list[Beneficio]:
        if beneficiario_id is not None:
            return await self.beneficio_repo.list_by_beneficiario(beneficiario_id)
        return await self.beneficio_repo.list_all()

    async def aprovar_beneficio(self, beneficio_id: UUID) -> Beneficio:
        item = await self.buscar_beneficio(beneficio_id)
        item.aprovar()
        return await self.beneficio_repo.save(item)

    async def negar_beneficio(self, beneficio_id: UUID, motivo: str) -> Beneficio:
        item = await self.buscar_beneficio(beneficio_id)
        item.negar(motivo)
        return await self.beneficio_repo.save(item)

    async def suspender_beneficio(self, beneficio_id: UUID, motivo: str) -> Beneficio:
        item = await self.buscar_beneficio(beneficio_id)
        item.suspender(motivo)
        return await self.beneficio_repo.save(item)

    async def encerrar_beneficio(self, beneficio_id: UUID, motivo: str) -> Beneficio:
        item = await self.buscar_beneficio(beneficio_id)
        item.encerrar(motivo)
        return await self.beneficio_repo.save(item)

    async def remover_beneficio(self, beneficio_id: UUID) -> None:
        if not await self.beneficio_repo.delete(beneficio_id):
            raise ValueError("Beneficio nao encontrado")
