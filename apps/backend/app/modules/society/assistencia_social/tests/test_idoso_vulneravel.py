from __future__ import annotations
import asyncio
from uuid import uuid4
from app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from app.modules.society.assistencia_social.application.services.idoso_vulneravel_service import IdosoVulneravelService
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade
from app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeRequestService, FakeSaudeService, InMemoryBeneficiarioRepo, InMemoryCadastroUnicoRepo, InMemoryIdosoRepo

def test_idoso_vulneravel_valida_idade_e_cobertura_saude() -> None:

    async def scenario() -> None:
        beneficiario_repo = InMemoryBeneficiarioRepo()
        request = FakeRequestService()
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA)
        service = IdosoVulneravelService(idoso_repo=InMemoryIdosoRepo(), beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(cobertura=False), request_service=request)
        erro = None
        try:
            await service.registrar_idoso(beneficiario_id=beneficiario.id, citizen_id_idoso=uuid4(), idade=59, dependencia=True, precisa_cuidados=True)
        except ValueError as exc:
            erro = str(exc)
        assert erro is not None
        assert '60' in erro
        registro = await service.registrar_idoso(beneficiario_id=beneficiario.id, citizen_id_idoso=uuid4(), idade=70, dependencia=True, precisa_cuidados=True)
        assert registro.codigo.startswith('IDO/')
        assert any((call['request_type'] == 'ASSISTENCIA_IDOSO_SEM_COBERTURA_SAUDE' for call in request.calls))
    asyncio.run(scenario())