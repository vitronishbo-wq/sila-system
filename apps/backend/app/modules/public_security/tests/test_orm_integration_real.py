from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.public_security.application.services.cadeia_custodia_service import CadeiaCustodiaService
from apps.backend.app.modules.public_security.application.services.evidencia_service import EvidenciaService
from apps.backend.app.modules.public_security.application.services.investigacao_service import InvestigacaoService
from apps.backend.app.modules.public_security.application.services.laudo_pericial_service import LaudoPericialService
from apps.backend.app.modules.public_security.application.services.mandado_service import MandadoService
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import ProvaPericialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.application.services.vestigio_service import VestigioService
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusCadeiaCustodia, TipoAgente, TipoEvidencia, TipoLaudo, TipoMandado, TipoOcorrencia, TipoProva, TipoUnidadePolicial, TipoVestigio, TipoVinculo

def _tables():
    from apps.backend.app.modules.public_security.infrastructure.models.cadeia_custodia_model import CadeiaCustodiaModel
    from apps.backend.app.modules.public_security.infrastructure.models.evidencia_model import EvidenciaModel
    from apps.backend.app.modules.public_security.infrastructure.models.investigacao_model import InvestigacaoModel
    from apps.backend.app.modules.public_security.infrastructure.models.laudo_pericial_model import LaudoPericialModel
    from apps.backend.app.modules.public_security.infrastructure.models.mandado_model import MandadoModel
    from apps.backend.app.modules.public_security.infrastructure.models.ocorrencia_model import OcorrenciaModel
    from apps.backend.app.modules.public_security.infrastructure.models.policial_model import PolicialModel
    from apps.backend.app.modules.public_security.infrastructure.models.prova_pericial_model import ProvaPericialModel
    from apps.backend.app.modules.public_security.infrastructure.models.unidade_policial_model import UnidadePolicialModel
    from apps.backend.app.modules.public_security.infrastructure.models.vestigio_model import VestigioModel
    if not hasattr(UnidadePolicialModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [UnidadePolicialModel.__table__, PolicialModel.__table__, OcorrenciaModel.__table__, MandadoModel.__table__, InvestigacaoModel.__table__, ProvaPericialModel.__table__, CadeiaCustodiaModel.__table__, LaudoPericialModel.__table__, VestigioModel.__table__, EvidenciaModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM seguranca_evidencias'))
    await session.execute(text('DELETE FROM seguranca_vestigios'))
    await session.execute(text('DELETE FROM seguranca_laudos_periciais'))
    await session.execute(text('DELETE FROM seguranca_cadeias_custodia'))
    await session.execute(text('DELETE FROM seguranca_provas_periciais'))
    await session.execute(text('DELETE FROM seguranca_investigacoes'))
    await session.execute(text('DELETE FROM seguranca_mandados'))
    await session.execute(text('DELETE FROM seguranca_ocorrencias'))
    await session.execute(text('DELETE FROM seguranca_policiais'))
    await session.execute(text('DELETE FROM seguranca_unidades_policiais'))
    await session.commit()

@asynccontextmanager
async def _session_scope():
    await _ensure_schema()
    async with AsyncSessionLocal() as session:
        await _clear_data(session)
        try:
            yield session
        finally:
            await _clear_data(session)

@pytest.mark.integration
def test_fluxo_real_orm_seguranca_publica_slices_foundation_investigativo_forense() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_cadeia_custodia_repository import SQLAlchemyCadeiaCustodiaRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_evidencia_repository import SQLAlchemyEvidenciaRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_investigacao_repository import SQLAlchemyInvestigacaoRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_laudo_pericial_repository import SQLAlchemyLaudoPericialRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_mandado_repository import SQLAlchemyMandadoRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_ocorrencia_repository import SQLAlchemyOcorrenciaRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_policial_repository import SQLAlchemyPolicialRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_prova_pericial_repository import SQLAlchemyProvaPericialRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_unidade_policial_repository import SQLAlchemyUnidadePolicialRepository
            from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_vestigio_repository import SQLAlchemyVestigioRepository
            unidade_repo = SQLAlchemyUnidadePolicialRepository(session)
            policial_repo = SQLAlchemyPolicialRepository(session)
            ocorrencia_repo = SQLAlchemyOcorrenciaRepository(session)
            mandado_repo = SQLAlchemyMandadoRepository(session)
            investigacao_repo = SQLAlchemyInvestigacaoRepository(session)
            prova_repo = SQLAlchemyProvaPericialRepository(session)
            cadeia_repo = SQLAlchemyCadeiaCustodiaRepository(session)
            laudo_repo = SQLAlchemyLaudoPericialRepository(session)
            vestigio_repo = SQLAlchemyVestigioRepository(session)
            evidencia_repo = SQLAlchemyEvidenciaRepository(session)
            unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
            policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
            ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
            mandado_service = MandadoService(mandado_repo=mandado_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
            investigacao_service = InvestigacaoService(investigacao_repo=investigacao_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
            prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
            cadeia_service = CadeiaCustodiaService(cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo)
            laudo_service = LaudoPericialService(laudo_repo=laudo_repo, prova_repo=prova_repo, policial_repo=policial_repo)
            vestigio_service = VestigioService(vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo)
            evidencia_service = EvidenciaService(evidencia_repo=evidencia_repo, vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo)
            unidade = await unidade_service.cadastrar_unidade(nome='Delegacia ORM Seguranca', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Luanda', provincia='Luanda', endereco='Rua ORM 100', comandante='Delegado ORM')
            policial = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Inspector ORM', data_nascimento=date.today() - timedelta(days=365 * 35), cpf='999.888.777-66', rg='RG999888', tipo=TipoAgente.POLICIAL, vinculo=TipoVinculo.EFETIVO)
            ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=policial.id, tipo=TipoOcorrencia.ROUBO, prioridade=PrioridadeOcorrencia.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=4), descricao='Teste integracao ORM seguranca publica', municipio='Luanda', provincia='Luanda', vitimas=2, suspeitos=1)
            mandado = await mandado_service.expedir_mandado(ocorrencia_id=ocorrencia.id, tipo=TipoMandado.BUSCA_APREENSAO, autoridade_judicial='Juizo Criminal ORM', data_expedicao=date.today(), data_validade=date.today() + timedelta(days=15), unidade_id=unidade.id, policial_responsavel_id=policial.id)
            investigacao = await investigacao_service.abrir_investigacao(ocorrencia_id=ocorrencia.id, delegado_responsavel_id=policial.id, resumo='Fluxo ORM de investigacao')
            prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DIGITAL, descricao='Midia digital apreendida para pericia', local_coleta='Laboratorio forense', coletado_por_id=policial.id)
            cadeia = await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Cofre forense', responsavel_id=policial.id)
            await cadeia_service.registrar_movimentacao(cadeia_id=cadeia.id, status=StatusCadeiaCustodia.EM_TRANSITO, local_atual='Laboratorio de analise', responsavel_id=policial.id, observacao='Transferida para analise')
            laudo = await laudo_service.emitir_laudo(prova_id=prova.id, tipo_laudo=TipoLaudo.INFORMATICA, perito_id=policial.id, conclusao='Evidencias digitais compativeis com a narrativa da ocorrencia.')
            vestigio = await vestigio_service.registrar_vestigio(cadeia_custodia_id=cadeia.id, tipo=TipoVestigio.MIDIA_DIGITAL, descricao='Vestigio digital associado ao material periciado', localizacao='Laboratorio de analise', coletado_por_id=policial.id)
            evidencia = await evidencia_service.registrar_evidencia(vestigio_id=vestigio.id, tipo=TipoEvidencia.DIGITAL, descricao='Evidencia digital consolidada para instruir a investigacao', fonte='Analise forense', confiabilidade=5, analisado_por_id=policial.id)
            fetched_unidade = await unidade_service.buscar_unidade(unidade.id)
            fetched_policial = await policial_service.buscar_policial(policial.id)
            fetched_ocorrencia = await ocorrencia_service.buscar_ocorrencia(ocorrencia.id)
            fetched_mandado = await mandado_service.buscar_mandado(mandado.id)
            fetched_investigacao = await investigacao_service.buscar_investigacao(investigacao.id)
            fetched_prova = await prova_service.buscar_prova(prova.id)
            fetched_cadeia = await cadeia_service.buscar_cadeia(cadeia.id)
            fetched_laudo = await laudo_service.buscar_laudo(laudo.id)
            fetched_vestigio = await vestigio_service.buscar_vestigio(vestigio.id)
            fetched_evidencia = await evidencia_service.buscar_evidencia(evidencia.id)
            assert fetched_unidade.codigo_unidade.startswith('UND/')
            assert fetched_policial.matricula.startswith('POL/')
            assert fetched_ocorrencia.codigo_ocorrencia.startswith('OCO/')
            assert fetched_ocorrencia.policial_responsavel_id == fetched_policial.id
            assert fetched_mandado.numero_mandado.startswith('MD/')
            assert fetched_investigacao.codigo_investigacao.startswith('INV/')
            assert fetched_prova.codigo_prova.startswith('PRV/')
            assert fetched_cadeia.codigo_cadeia.startswith('CCD/')
            assert fetched_laudo.numero_laudo.startswith('LDP/')
            assert fetched_vestigio.codigo_vestigio.startswith('VST/')
            assert fetched_evidencia.codigo_evidencia.startswith('EVD/')
    asyncio.run(scenario())