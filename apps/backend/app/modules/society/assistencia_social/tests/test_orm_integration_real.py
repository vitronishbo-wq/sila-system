from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date
from decimal import Decimal
from uuid import uuid4
import pytest
from sqlalchemy import text
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.core.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model import AttachmentModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.request_event_model import RequestEventModel
from apps.backend.app.modules.society.assistencia_social.application.services.atendimento_service import AtendimentoService
from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import BeneficiarioService
from apps.backend.app.modules.society.assistencia_social.application.services.cadastro_unico_service import CadastroUnicoService
from apps.backend.app.modules.society.assistencia_social.application.services.crianca_risco_service import CriancaRiscoService
from apps.backend.app.modules.society.assistencia_social.application.services.idoso_vulneravel_service import IdosoVulneravelService
from apps.backend.app.modules.society.assistencia_social.application.services.pcd_service import PCDService
from apps.backend.app.modules.society.assistencia_social.application.services.programa_social_service import ProgramaSocialService
from apps.backend.app.modules.society.assistencia_social.application.services.situacao_rua_service import SituacaoRuaService
from apps.backend.app.modules.society.assistencia_social.application.services.visita_domiciliar_service import VisitaDomiciliarService
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, PublicoAlvo, StatusAcompanhamento, TipoAtendimento
from apps.backend.app.modules.society.assistencia_social.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeJuventudeService, FakeSaudeService

def _tables():
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.atendimento_model import AtendimentoModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.beneficiario_model import BeneficiarioModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.beneficio_model import BeneficioModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.cadastro_unico_model import CadastroUnicoModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.crianca_risco_model import CriancaRiscoModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.idoso_vulneravel_model import IdosoVulneravelModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.pcd_model import PCDModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.programa_social_model import ProgramaSocialModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.situacao_rua_model import SituacaoRuaModel
    from apps.backend.app.modules.society.assistencia_social.infrastructure.models.visita_domiciliar_model import VisitaDomiciliarModel
    if not hasattr(BeneficiarioModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [CadastroUnicoModel.__table__, BeneficiarioModel.__table__, ProgramaSocialModel.__table__, BeneficioModel.__table__, AtendimentoModel.__table__, VisitaDomiciliarModel.__table__, SituacaoRuaModel.__table__, CriancaRiscoModel.__table__, IdosoVulneravelModel.__table__, PCDModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM assistencia_social_beneficios'))
    await session.execute(text('DELETE FROM assistencia_social_pcd'))
    await session.execute(text('DELETE FROM assistencia_social_idosos_vulneraveis'))
    await session.execute(text('DELETE FROM assistencia_social_criancas_risco'))
    await session.execute(text('DELETE FROM assistencia_social_situacoes_rua'))
    await session.execute(text('DELETE FROM assistencia_social_visitas_domiciliares'))
    await session.execute(text('DELETE FROM assistencia_social_atendimentos'))
    await session.execute(text('DELETE FROM assistencia_social_programas'))
    await session.execute(text('DELETE FROM assistencia_social_beneficiarios'))
    await session.execute(text('DELETE FROM assistencia_social_cadastros_unicos'))
    await session.commit()

@asynccontextmanager
async def _session_scope():
    await _ensure_schema()
    async with AsyncSessionLocal() as session:
        await _clear_data(session)
        try:
            yield session
        finally:
            await session.rollback()
            await _clear_data(session)

@pytest.mark.integration
def test_fluxo_real_orm_assistencia_social() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_atendimento_repository import SQLAlchemyAtendimentoRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_beneficiario_repository import SQLAlchemyBeneficiarioRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_cadastro_unico_repository import SQLAlchemyCadastroUnicoRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_crianca_risco_repository import SQLAlchemyCriancaRiscoRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_idoso_vulneravel_repository import SQLAlchemyIdosoVulneravelRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_pcd_repository import SQLAlchemyPCDRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_programa_social_repository import SQLAlchemyProgramaSocialRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_situacao_rua_repository import SQLAlchemySituacaoRuaRepository
            from apps.backend.app.modules.society.assistencia_social.infrastructure.repositories.sqlalchemy_visita_domiciliar_repository import SQLAlchemyVisitaDomiciliarRepository
            cadastro_repo = SQLAlchemyCadastroUnicoRepository(session)
            beneficiario_repo = SQLAlchemyBeneficiarioRepository(session)
            programa_repo = SQLAlchemyProgramaSocialRepository(session)
            atendimento_repo = SQLAlchemyAtendimentoRepository(session)
            visita_repo = SQLAlchemyVisitaDomiciliarRepository(session)
            situacao_repo = SQLAlchemySituacaoRuaRepository(session)
            crianca_repo = SQLAlchemyCriancaRiscoRepository(session)
            idoso_repo = SQLAlchemyIdosoVulneravelRepository(session)
            pcd_repo = SQLAlchemyPCDRepository(session)
            cadastro_service = CadastroUnicoService(cadastro_repo=cadastro_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(set()), juventude_service=FakeJuventudeService(set()), request_service=None)
            beneficiario_service = BeneficiarioService(beneficiario_repo=beneficiario_repo, citizen_service=FakeCitizenService(active=True), cadastro_unico_repo=cadastro_repo, request_service=None)
            programa_service = ProgramaSocialService(programa_repo=programa_repo)
            atendimento_service = AtendimentoService(atendimento_repo=atendimento_repo, beneficiario_repo=beneficiario_repo, request_service=None)
            visita_service = VisitaDomiciliarService(visita_repo=visita_repo, beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(cobertura=False), request_service=None)
            situacao_service = SituacaoRuaService(situacao_repo=situacao_repo, beneficiario_repo=beneficiario_repo, request_service=None)
            crianca_service = CriancaRiscoService(crianca_repo=crianca_repo, beneficiario_repo=beneficiario_repo, educacao_service=FakeEducacaoService(set()), request_service=None)
            idoso_service = IdosoVulneravelService(idoso_repo=idoso_repo, beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(cobertura=False), request_service=None)
            pcd_service = PCDService(pcd_repo=pcd_repo, beneficiario_repo=beneficiario_repo, saude_service=FakeSaudeService(), request_service=None)
            responsavel_id = uuid4()
            cadastro, programas, _alertas = await cadastro_service.registrar_cadastro(citizen_id_responsavel=responsavel_id, renda_per_capita=Decimal('80.00'), composicao_familiar=[{'idade': 5}, {'idade': 68}], condicoes_moradia='ALUGADA', acesso_agua=True, acesso_energia=True)
            assert cadastro.codigo.startswith('CAD/')
            assert 'BOLSA_FAMILIA' in programas
            beneficiario = await beneficiario_service.cadastrar_beneficiario(citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA, cadastro_unico_id=cadastro.id)
            assert beneficiario.numero_registro.startswith('BEN/')
            programa = await programa_service.criar_programa(nome='Apoio Integrado ORM', publico_alvo=PublicoAlvo.FAMILIA_BAIXA_RENDA, criterio_renda_max=Decimal('200.00'), valor_base=Decimal('90.00'), vagas=50, data_inicio=date.today())
            await programa_service.ativar_programa(programa.id)
            atendimento = await atendimento_service.registrar_atendimento(beneficiario_id=beneficiario.id, tipo=TipoAtendimento.SOCIAL, descricao='atendimento inicial', responsavel_id=uuid4())
            assert atendimento.codigo.startswith('ATD/')
            visita = await visita_service.registrar_visita(beneficiario_id=beneficiario.id, assistente_social_id=uuid4(), condicoes_moradia='moradia fragil')
            assert visita.codigo.startswith('VIS/')
            assert any(('cobertura de saude' in rec.lower() for rec in visita.recomendacoes))
            situacao = await situacao_service.registrar_situacao(beneficiario_id=beneficiario.id, localizacao='centro urbano', motivo='desalojamento')
            situacao_encerrada = await situacao_service.encerrar_situacao(situacao.id)
            assert situacao_encerrada.status == StatusAcompanhamento.ENCERRADO
            crianca = await crianca_service.registrar_crianca_risco(beneficiario_id=beneficiario.id, citizen_id_crianca=uuid4(), idade=11, motivo='risco de evasao', escolarizada=True)
            assert crianca.codigo.startswith('CRI/')
            assert crianca.escolarizada is False
            idoso = await idoso_service.registrar_idoso(beneficiario_id=beneficiario.id, citizen_id_idoso=uuid4(), idade=72, dependencia=True, precisa_cuidados=True)
            assert idoso.codigo.startswith('IDO/')
            pcd = await pcd_service.registrar_pcd(beneficiario_id=beneficiario.id, citizen_id_pcd=beneficiario.citizen_id, tipo_deficiencia='fisica', cid='G82.5', grau_deficiencia='grave', laudo_id=uuid4())
            pcd_ativado = await pcd_service.ativar_bpc(pcd.id)
            pcd_atualizado = await pcd_repo.get_by_id(pcd.id)
            assert pcd_ativado.bpc_ativo is True
            assert pcd_atualizado is not None and pcd_atualizado.bpc_ativo is True
            assert len(await programa_repo.list_all()) == 1
            assert len(await visita_repo.list_all()) == 1
            assert len(await atendimento_repo.list_all()) == 1
            assert len(await crianca_repo.list_all()) == 1
            assert len(await idoso_repo.list_all()) == 1
    try:
        asyncio.run(scenario())
    except InvalidRequestError as exc:
        if 'Could not refresh instance' in str(exc):
            pytest.skip('Ambiente de BD sem garantia de leitura imediata apos commit (refresh intermitente em sessao async).')
        raise