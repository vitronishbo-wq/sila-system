from __future__ import annotations
import asyncio
from uuid import uuid4
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from apps.backend.app.modules.society.assistencia_social.application.services.pcd_service import PCDService
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, StatusAcompanhamento
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeRequestService, FakeSaudeService, InMemoryBeneficiarioRepo, InMemoryCadastroUnicoRepo, InMemoryPCDRepo

def test_pcd_exige_laudo_valido_e_permite_fluxo_bpc() -> None:

    async def scenario() -> None:
        beneficiario_repo = InMemoryBeneficiarioRepo()
        pcd_repo = InMemoryPCDRepo()
        request = FakeRequestService()
        laudo_id = uuid4()
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.MEDIA)
        service_invalido = PCDService(pcd_repo=pcd_repo, beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(laudos_invalidos={laudo_id}), request_service=request)
        erro = None
        try:
            await service_invalido.registrar_pcd(beneficiario_id=beneficiario.id, citizen_id_pcd=beneficiario.citizen_id, tipo_deficiencia='fisica', cid='G82.5', grau_deficiencia='grave', laudo_id=laudo_id)
        except ValueError as exc:
            erro = str(exc)
        assert erro is not None
        assert 'laudo' in erro.lower()
        service = PCDService(pcd_repo=pcd_repo, beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(), request_service=request)
        pcd = await service.registrar_pcd(beneficiario_id=beneficiario.id, citizen_id_pcd=beneficiario.citizen_id, tipo_deficiencia='fisica', cid='G82.5', grau_deficiencia='grave', laudo_id=uuid4())
        assert pcd.bpc_ativo is False
        ativado = await service.ativar_bpc(pcd.id)
        assert ativado.bpc_ativo is True
        encerrado = await service.encerrar_pcd(pcd.id)
        assert encerrado.status == StatusAcompanhamento.ENCERRADO
    asyncio.run(scenario())