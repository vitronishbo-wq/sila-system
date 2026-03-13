from __future__ import annotations
import asyncio
from decimal import Decimal
from uuid import uuid4
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from apps.backend.app.modules.society.assistencia_social.application.services.beneficio_service import BeneficioService
from apps.backend.app.modules.society.assistencia_social.application.services.pcd_service import PCDService
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, StatusBeneficio
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeEmpregoService, FakeRequestService, FakeSaudeService, InMemoryBeneficiarioRepo, InMemoryBeneficioRepo, InMemoryCadastroUnicoRepo, InMemoryPCDRepo, InMemoryProgramaRepo

def test_fluxo_bpc_pcd_aprova_e_ativa_pcd() -> None:

    async def scenario() -> None:
        beneficiario_repo = InMemoryBeneficiarioRepo()
        pcd_repo = InMemoryPCDRepo()
        request_service = FakeRequestService()
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request_service)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.EXTREMA)
        pcd_service = PCDService(pcd_repo=pcd_repo, beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(), request_service=request_service)
        pcd = await pcd_service.registrar_pcd(beneficiario_id=beneficiario.id, citizen_id_pcd=beneficiario.citizen_id, tipo_deficiencia='fisica', cid='G82.5', grau_deficiencia='grave', laudo_id=uuid4())
        beneficio_service = BeneficioService(beneficio_repo=InMemoryBeneficioRepo(), beneficiario_repo=beneficiario_repo, programa_repo=InMemoryProgramaRepo(), pcd_repo=pcd_repo, saude_service=FakeSaudeService(), emprego_service=FakeEmpregoService(previdenciarios=set()), request_service=request_service)
        beneficio = await beneficio_service.conceder_bpc_pcd(beneficiario_id=beneficiario.id, pcd_id=pcd.id, valor=Decimal('706.00'))
        pcd_atualizado = await pcd_repo.get_by_id(pcd.id)
        assert beneficio.status == StatusBeneficio.APROVADO
        assert pcd_atualizado is not None and pcd_atualizado.bpc_ativo is True
    asyncio.run(scenario())