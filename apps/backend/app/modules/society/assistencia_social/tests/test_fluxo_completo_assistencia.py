from __future__ import annotations
import asyncio
from datetime import date
from decimal import Decimal
from uuid import uuid4
from app.modules.society.assistencia_social.application.services.atendimento_service import AtendimentoService
from app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from app.modules.society.assistencia_social.application.services.beneficio_service import BeneficioService
from app.modules.society.assistencia_social.application.services.cadastro_unico_service import CadastroUnicoService
from app.modules.society.assistencia_social.application.services.programa_social_service import ProgramaSocialService
from app.modules.society.assistencia_social.application.services.visita_domiciliar_service import VisitaDomiciliarService
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, PublicoAlvo, TipoAtendimento, TipoBeneficio
from app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService, FakeJuventudeService, FakeRequestService, FakeSaudeService, InMemoryAtendimentoRepo, InMemoryBeneficiarioRepo, InMemoryBeneficioRepo, InMemoryCadastroUnicoRepo, InMemoryPCDRepo, InMemoryProgramaRepo, InMemoryVisitaRepo

def test_fluxo_basico_assistencia_social() -> None:

    async def scenario() -> None:
        request = FakeRequestService()
        cadastro_repo = InMemoryCadastroUnicoRepo()
        beneficiario_repo = InMemoryBeneficiarioRepo()
        programa_repo = InMemoryProgramaRepo()
        cadastro_service = CadastroUnicoService(cadastro_repo=cadastro_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(set()), juventude_service=FakeJuventudeService(set()), request_service=request)
        cadastro, _, _ = await cadastro_service.registrar_cadastro(citizen_id_responsavel=uuid4(), renda_per_capita=Decimal('120.00'), composicao_familiar=[], condicoes_moradia='CEDIDA', acesso_agua=True, acesso_energia=False)
        beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=cadastro_repo, request_service=request)
        beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA, cadastro_unico_id=cadastro.id)
        programa_service = ProgramaSocialService(programa_repo=programa_repo)
        programa = await programa_service.criar_programa(nome='Auxilio Familiar', publico_alvo=PublicoAlvo.FAMILIA_BAIXA_RENDA, criterio_renda_max=Decimal('150.00'), valor_base=Decimal('80.00'), vagas=100, data_inicio=date.today())
        await programa_service.ativar_programa(programa.id)
        beneficio_service = BeneficioService(beneficio_repo=InMemoryBeneficioRepo(), beneficiario_repo=beneficiario_repo, programa_repo=programa_repo, pcd_repo=InMemoryPCDRepo(), saude_service=FakeSaudeService(), emprego_service=FakeEmpregoService(), request_service=request)
        beneficio = await beneficio_service.solicitar_beneficio(beneficiario_id=beneficiario.id, tipo=TipoBeneficio.AUXILIO_NUTRICIONAL, valor=Decimal('80.00'), programa_social_id=programa.id)
        atendimento_service = AtendimentoService(atendimento_repo=InMemoryAtendimentoRepo(), beneficiario_repo=beneficiario_repo, request_service=request)
        atendimento = await atendimento_service.registrar_atendimento(beneficiario_id=beneficiario.id, tipo=TipoAtendimento.SOCIAL, descricao='Acompanhamento inicial', responsavel_id=uuid4())
        visita_service = VisitaDomiciliarService(visita_repo=InMemoryVisitaRepo(), beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(cobertura=False), request_service=request)
        visita = await visita_service.registrar_visita(beneficiario_id=beneficiario.id, assistente_social_id=uuid4(), condicoes_moradia='RESIDENCIA SEM SANEAMENTO')
        assert beneficio.codigo.startswith('BNF/')
        assert atendimento.codigo.startswith('ATD/')
        assert visita.codigo.startswith('VIS/')
        assert len(request.calls) >= 4
    asyncio.run(scenario())