from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.domain.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.civil_protection.application.services.bombeiro_service import BombeiroService
from apps.backend.app.modules.civil_protection.application.services.corporacao_service import CorporacaoService
from apps.backend.app.modules.civil_protection.application.services.despacho_service import DespachoService
from apps.backend.app.modules.civil_protection.application.services.ocorrencia_emergencial_service import OcorrenciaEmergencialService
from apps.backend.app.modules.civil_protection.application.services.atendimento_service import AtendimentoService
from apps.backend.app.modules.civil_protection.domain.enums import PrioridadeAtendimento, StatusAtendimento, StatusDespacho, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial

def _tables():
    from apps.backend.app.modules.civil_protection.infrastructure.models.bombeiro_model import BombeiroModel
    from apps.backend.app.modules.civil_protection.infrastructure.models.despacho_model import DespachoModel
    from apps.backend.app.modules.civil_protection.infrastructure.models.atendimento_model import AtendimentoModel
    from apps.backend.app.modules.civil_protection.infrastructure.models.corporacao_model import CorporacaoModel
    from apps.backend.app.modules.civil_protection.infrastructure.models.ocorrencia_emergencial_model import OcorrenciaEmergencialModel
    if not hasattr(CorporacaoModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [CorporacaoModel.__table__, BombeiroModel.__table__, OcorrenciaEmergencialModel.__table__, DespachoModel.__table__, AtendimentoModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM protecao_civil_atendimentos'))
    await session.execute(text('DELETE FROM protecao_civil_despachos'))
    await session.execute(text('DELETE FROM protecao_civil_ocorrencias_emergenciais'))
    await session.execute(text('DELETE FROM protecao_civil_bombeiros'))
    await session.execute(text('DELETE FROM protecao_civil_corporacoes'))
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
def test_fluxo_real_orm_protecao_civil_foundation() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model import AttachmentModel
            from apps.backend.app.modules.governance.service_requests.infrastructure.models.request_event_model import RequestEventModel
            from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_bombeiro_repository import SQLAlchemyBombeiroRepository
            from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_despacho_repository import SQLAlchemyDespachoRepository
            from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_atendimento_repository import SQLAlchemyAtendimentoRepository
            from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_corporacao_repository import SQLAlchemyCorporacaoRepository
            from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_ocorrencia_emergencial_repository import SQLAlchemyOcorrenciaEmergencialRepository
            corporacao_repo = SQLAlchemyCorporacaoRepository(session)
            bombeiro_repo = SQLAlchemyBombeiroRepository(session)
            ocorrencia_repo = SQLAlchemyOcorrenciaEmergencialRepository(session)
            despacho_repo = SQLAlchemyDespachoRepository(session)
            atendimento_repo = SQLAlchemyAtendimentoRepository(session)
            corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
            bombeiro_service = BombeiroService(bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo)
            ocorrencia_service = OcorrenciaEmergencialService(ocorrencia_repo=ocorrencia_repo, corporacao_repo=corporacao_repo, bombeiro_repo=bombeiro_repo)
            despacho_service = DespachoService(despacho_repo=despacho_repo, ocorrencia_repo=ocorrencia_repo, bombeiro_repo=bombeiro_repo)
            atendimento_service = AtendimentoService(atendimento_repo=atendimento_repo, despacho_repo=despacho_repo, ocorrencia_repo=ocorrencia_repo, bombeiro_repo=bombeiro_repo)
            corporacao = await corporacao_service.cadastrar_corporacao(nome='Corpo de Bombeiros ORM', municipio='Luanda', provincia='Luanda', endereco='Rua ORM 100', comandante='Comandante ORM')
            bombeiro = await bombeiro_service.cadastrar_bombeiro(corporacao_id=corporacao.id, nome='Bombeiro ORM', data_nascimento=date.today() - timedelta(days=365 * 35), cpf='999.888.777-66', rg='RG999888')
            ocorrencia = await ocorrencia_service.registrar_ocorrencia(corporacao_id=corporacao.id, bombeiro_responsavel_id=bombeiro.id, tipo=TipoOcorrenciaEmergencial.INUNDACAO, prioridade=PrioridadeAtendimento.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=3), descricao='Teste integracao ORM protecao civil', municipio='Luanda', provincia='Luanda', vitimas=2, desalojados=3)
            despacho = await despacho_service.registrar_despacho(ocorrencia_id=ocorrencia.id, bombeiro_responsavel_id=bombeiro.id, meio_deslocamento='auto_bomba')
            atendimento = await atendimento_service.registrar_atendimento(despacho_id=despacho.id, local_atendimento='Bairro ORM', vitimas_atendidas=2, desalojados_atendidos=3, equipe_responsavel_id=bombeiro.id)
            atendimento_finalizado = await atendimento_service.finalizar_atendimento(atendimento_id=atendimento.id, resumo='Fluxo completo encerrado')
            fetched_corporacao = await corporacao_service.buscar_corporacao(corporacao.id)
            fetched_bombeiro = await bombeiro_service.buscar_bombeiro(bombeiro.id)
            fetched_ocorrencia = await ocorrencia_service.buscar_ocorrencia(ocorrencia.id)
            fetched_despacho = await despacho_service.buscar_despacho(despacho.id)
            fetched_atendimento = await atendimento_service.buscar_atendimento(atendimento.id)
            assert fetched_corporacao.codigo_corporacao.startswith('COR/')
            assert fetched_bombeiro.matricula.startswith('BOM/')
            assert fetched_ocorrencia.codigo_ocorrencia.startswith('OCE/')
            assert fetched_ocorrencia.bombeiro_responsavel_id == fetched_bombeiro.id
            assert fetched_despacho.codigo_despacho.startswith('DSP/')
            assert fetched_atendimento.codigo_atendimento.startswith('ATE/')
            assert fetched_despacho.status == StatusDespacho.CONCLUIDO
            assert fetched_atendimento.status == StatusAtendimento.FINALIZADO
            assert atendimento_finalizado.fim_atendimento is not None
            assert fetched_ocorrencia.status == StatusOcorrenciaEmergencial.CONCLUIDA
    asyncio.run(scenario())