from __future__ import annotations
import asyncio
from uuid import uuid4
from app.modules.society.assistencia_social.application.services.atendimento_service import AtendimentoService
from app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, TipoAtendimento
from app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeRequestService, InMemoryAtendimentoRepo, InMemoryBeneficiarioRepo, InMemoryCadastroUnicoRepo

def test_atendimento_exige_beneficiario_e_persiste_fluxo() -> None:

    async def scenario() -> None:
        atendimento_service = AtendimentoService(atendimento_repo=InMemoryAtendimentoRepo(), beneficiario_repo=InMemoryBeneficiarioRepo(), request_service=FakeRequestService())
        erro = None
        try:
            await atendimento_service.registrar_atendimento(beneficiario_id=uuid4(), tipo=TipoAtendimento.SOCIAL, descricao='nao deve cadastrar', responsavel_id=uuid4())
        except ValueError as exc:
            erro = str(exc)
        assert erro is not None
        beneficiario_repo = InMemoryBeneficiarioRepo()
        request = FakeRequestService()
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.BAIXA)
        service = AtendimentoService(atendimento_repo=InMemoryAtendimentoRepo(), beneficiario_repo=beneficiario_repo, request_service=request)
        atendimento = await service.registrar_atendimento(beneficiario_id=beneficiario.id, tipo=TipoAtendimento.SOCIAL, descricao='visita no CRAS', responsavel_id=uuid4(), encaminhamentos=[{'tipo': 'retorno'}])
        assert atendimento.codigo.startswith('ATD/')
        assert atendimento.encaminhamentos and atendimento.encaminhamentos[0]['tipo'] == 'retorno'
    asyncio.run(scenario())