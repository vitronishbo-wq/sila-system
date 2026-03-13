from __future__ import annotations
import asyncio
from uuid import uuid4
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from apps.backend.app.modules.society.assistencia_social.application.services.situacao_rua_service import SituacaoRuaService
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, StatusAcompanhamento
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeRequestService, InMemoryBeneficiarioRepo, InMemoryCadastroUnicoRepo, InMemorySituacaoRuaRepo

def test_situacao_rua_registra_e_encerra() -> None:

    async def scenario() -> None:
        beneficiario_repo = InMemoryBeneficiarioRepo()
        request = FakeRequestService()
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.EXTREMA)
        service = SituacaoRuaService(situacao_repo=InMemorySituacaoRuaRepo(), beneficiario_repo=beneficiario_repo, request_service=request)
        situacao = await service.registrar_situacao(beneficiario_id=beneficiario.id, localizacao='Mercado Municipal', motivo='perda de moradia')
        assert situacao.codigo.startswith('SRU/')
        assert len(request.calls) == 2
        encerrada = await service.encerrar_situacao(situacao.id)
        assert encerrada.status == StatusAcompanhamento.ENCERRADO
    asyncio.run(scenario())