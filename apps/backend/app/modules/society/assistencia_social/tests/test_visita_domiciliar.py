from __future__ import annotations
import asyncio
from uuid import uuid4
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from apps.backend.app.modules.society.assistencia_social.application.services.visita_domiciliar_service import VisitaDomiciliarService
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeRequestService, FakeSaudeService, InMemoryBeneficiarioRepo, InMemoryCadastroUnicoRepo, InMemoryVisitaRepo

def test_visita_domiciliar_gera_recomendacao_quando_sem_cobertura() -> None:

    async def scenario() -> None:
        beneficiario_repo = InMemoryBeneficiarioRepo()
        request = FakeRequestService()
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=InMemoryCadastroUnicoRepo(), request_service=request)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA)
        service = VisitaDomiciliarService(visita_repo=InMemoryVisitaRepo(), beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(cobertura=False), request_service=request)
        visita = await service.registrar_visita(beneficiario_id=beneficiario.id, assistente_social_id=uuid4(), condicoes_moradia='residencia em area sem saneamento', recomendacoes=['orientacao inicial'])
        assert visita.codigo.startswith('VIS/')
        assert any(('cobertura de saude' in item.lower() for item in visita.recomendacoes))
    asyncio.run(scenario())