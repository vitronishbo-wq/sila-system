from __future__ import annotations
import asyncio
from uuid import uuid4
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, SituacaoBeneficiario
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeRequestService, InMemoryBeneficiarioRepo, InMemoryCadastroUnicoRepo

def test_beneficiario_rejeita_duplicidade_ativa_e_permite_inativar() -> None:

    async def scenario() -> None:
        citizen_id = uuid4()
        repo = InMemoryBeneficiarioRepo()
        request = FakeRequestService()
        service = BeneficiarioService(beneficiario_repo=repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request)
        primeiro = await service.cadastrar_beneficiario(citizen_id=citizen_id, faixa_vulnerabilidade=FaixaVulnerabilidade.MEDIA)
        assert primeiro.numero_registro.startswith('BEN/')
        assert len(request.calls) == 1
        erro = None
        try:
            await service.cadastrar_beneficiario(citizen_id=citizen_id, faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA)
        except ValueError as exc:
            erro = str(exc)
        assert erro is not None
        assert 'ativo' in erro.lower()
        inativo = await service.inativar_beneficiario(primeiro.id, 'encerrado')
        assert inativo.ativo is False
        assert inativo.situacao == SituacaoBeneficiario.INATIVO
    asyncio.run(scenario())