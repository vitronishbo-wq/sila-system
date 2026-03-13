from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date, timedelta
from uuid import uuid4
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.society.desporto.application.services.atleta_service import AtletaService
from apps.backend.app.modules.society.desporto.application.services.clube_service import ClubeService
from apps.backend.app.modules.society.desporto.application.services.competicao_service import CompeticaoService
from apps.backend.app.modules.society.desporto.application.services.jogo_service import JogoService
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusCompeticao, StatusJogo, TipoAtleta, TipoClube, TipoCompeticao
from apps.backend.app.modules.society.desporto.tests._fakes import FakeEducacaoService, FakeObrasPublicasService, FakeTurismoService

def _tables():
    from apps.backend.app.modules.society.desporto.infrastructure.models.atleta_model import AtletaModel
    from apps.backend.app.modules.society.desporto.infrastructure.models.clube_model import ClubeModel
    from apps.backend.app.modules.society.desporto.infrastructure.models.competicao_model import CompeticaoModel
    from apps.backend.app.modules.society.desporto.infrastructure.models.jogo_model import JogoModel
    if not hasattr(AtletaModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [AtletaModel.__table__, CompeticaoModel.__table__, ClubeModel.__table__, JogoModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM desporto_jogos'))
    await session.execute(text('DELETE FROM desporto_competicoes'))
    await session.execute(text('DELETE FROM desporto_clubes'))
    await session.execute(text('DELETE FROM desporto_atletas'))
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
def test_fluxo_real_orm_atleta_competicao() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_atleta_repository import SQLAlchemyAtletaRepository
            from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_clube_repository import SQLAlchemyClubeRepository
            from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_competicao_repository import SQLAlchemyCompeticaoRepository
            from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_jogo_repository import SQLAlchemyJogoRepository
            atleta_service = AtletaService(atleta_repo=SQLAlchemyAtletaRepository(session))
            clube_service = ClubeService(clube_repo=SQLAlchemyClubeRepository(session))
            competicao_service = CompeticaoService(competicao_repo=SQLAlchemyCompeticaoRepository(session), turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True))
            jogo_service = JogoService(jogo_repo=SQLAlchemyJogoRepository(session), competicao_repo=SQLAlchemyCompeticaoRepository(session), clube_repo=SQLAlchemyClubeRepository(session), turismo_service=FakeTurismoService(exists=True), obras_publicas_service=FakeObrasPublicasService(exists=True))
            atleta = await atleta_service.cadastrar_atleta(nome='Atleta Integracao', data_nascimento=date.today() - timedelta(days=365 * 24), naturalidade='Luanda', nacionalidade='Angolana', tipo=TipoAtleta.PROFISSIONAL, modalidades=[ModalidadeDesportiva.FUTEBOL])
            competicao = await competicao_service.cadastrar_competicao(nome='Liga Integracao', tipo=TipoCompeticao.LIGA, modalidade=ModalidadeDesportiva.FUTEBOL, data_inicio=date(2026, 9, 1), data_fim=date(2026, 10, 1), municipio='Luanda', provincia='Luanda', organizador_id=uuid4())
            competicao_pub = await competicao_service.atualizar_competicao(competicao_id=competicao.id, status=StatusCompeticao.EM_ANDAMENTO)
            clube_casa = await clube_service.cadastrar_clube(nome='Clube ORM A', sigla='ORMA', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
            clube_fora = await clube_service.cadastrar_clube(nome='Clube ORM B', sigla='ORMB', tipo=TipoClube.PROFISSIONAL, modalidade_principal=ModalidadeDesportiva.FUTEBOL, municipio='Luanda', provincia='Luanda')
            jogo = await jogo_service.agendar_jogo(competicao_id=competicao.id, clube_casa_id=clube_casa.id, clube_fora_id=clube_fora.id, data_jogo=date(2026, 9, 12), local='Estadio Integracao', municipio='Luanda', provincia='Luanda')
            jogo_final = await jogo_service.registrar_resultado(jogo_id=jogo.id, placar_casa=1, placar_fora=0)
            assert atleta.numero_registro.startswith('ATL/')
            assert competicao.codigo_competicao.startswith('CMP/')
            assert competicao_pub.status == StatusCompeticao.EM_ANDAMENTO
            assert clube_casa.codigo_clube.startswith('CLB/')
            assert jogo.codigo_jogo.startswith('JOG/')
            assert jogo_final.status == StatusJogo.ENCERRADO
    asyncio.run(scenario())