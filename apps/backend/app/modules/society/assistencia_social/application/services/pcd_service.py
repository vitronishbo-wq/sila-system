from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    BeneficiarioRepositoryPort,
    PCDRepositoryPort,
    RequestServicePort,
    SaudeServicePort,
)
from apps.backend.app.modules.society.assistencia_social.application.services._codegen import (
    next_codigo,
)
from apps.backend.app.modules.society.assistencia_social.domain.models import PessoaComDeficiencia


class PCDService:
    def __init__(
        self,
        *,
        pcd_repo: PCDRepositoryPort,
        beneficiario_repo: BeneficiarioRepositoryPort,
        saude_service: SaudeServicePort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.pcd_repo = pcd_repo
        self.beneficiario_repo = beneficiario_repo
        self.saude_service = saude_service
        self.request_service = request_service

    async def registrar_pcd(
        self,
        *,
        beneficiario_id: UUID,
        citizen_id_pcd: UUID,
        tipo_deficiencia: str,
        cid: str,
        grau_deficiencia: str,
        laudo_id: UUID,
    ) -> PessoaComDeficiencia:
        beneficiario = await self.beneficiario_repo.get_by_id(beneficiario_id)
        if beneficiario is None:
            raise ValueError("Beneficiario nao encontrado")
        laudo_valido = await self.saude_service.validar_laudo_pcd(
            citizen_id=citizen_id_pcd, laudo_id=laudo_id, cid=cid
        )
        if not laudo_valido:
            raise ValueError("Laudo medico invalido para registro PcD")
        codigo = next_codigo("PCD", len(await self.pcd_repo.list_all()))
        item = PessoaComDeficiencia.registrar(
            codigo=codigo,
            beneficiario_id=beneficiario_id,
            citizen_id_pcd=citizen_id_pcd,
            tipo_deficiencia=tipo_deficiencia,
            cid=cid,
            grau_deficiencia=grau_deficiencia,
            laudo_id=laudo_id,
        )
        saved = await self.pcd_repo.save(item)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="ASSISTENCIA_REGISTRO_PCD",
                entity_id=saved.id,
                citizen_id=beneficiario.citizen_id,
                numero_processo=saved.codigo,
                metadata={"cid": saved.cid, "grau_deficiencia": saved.grau_deficiencia},
            )
        return saved

    async def buscar_pcd(self, item_id: UUID) -> PessoaComDeficiencia:
        item = await self.pcd_repo.get_by_id(item_id)
        if item is None:
            raise ValueError("Registro PcD nao encontrado")
        return item

    async def listar_pcd(self, beneficiario_id: UUID | None = None) -> list[PessoaComDeficiencia]:
        if beneficiario_id is not None:
            return await self.pcd_repo.list_by_beneficiario(beneficiario_id)
        return await self.pcd_repo.list_all()

    async def ativar_bpc(self, item_id: UUID) -> PessoaComDeficiencia:
        item = await self.buscar_pcd(item_id)
        item.ativar_bpc()
        return await self.pcd_repo.save(item)

    async def encerrar_pcd(self, item_id: UUID) -> PessoaComDeficiencia:
        item = await self.buscar_pcd(item_id)
        item.encerrar_acompanhamento()
        return await self.pcd_repo.save(item)

    async def remover_pcd(self, item_id: UUID) -> None:
        if not await self.pcd_repo.delete(item_id):
            raise ValueError("Registro PcD nao encontrado")
