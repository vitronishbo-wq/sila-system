from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date
from uuid import uuid4
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.society.cultura.application.services.artista_service import ArtistaService
from apps.backend.app.modules.society.cultura.application.services.bem_cultural_service import BemCulturalService
from apps.backend.app.modules.society.cultura.application.services.evento_cultural_service import EventoCulturalService
from apps.backend.app.modules.society.cultura.domain.enums import CategoriaPatrimonioImaterial, StatusEventoCultural, StatusPatrimonioImaterial, StatusTombamento, TipoArtista, TipoEventoCultural, TipoGrupoArtistico, TipoPatrimonio
from apps.backend.app.modules.society.cultura.tests._fakes import FakeEducacaoService, FakeTurismoService

def _tables():
    from apps.backend.app.modules.society.cultura.infrastructure.models.artista_model import ArtistaModel
    from apps.backend.app.modules.society.cultura.infrastructure.models.bem_cultural_model import BemCulturalModel
    from apps.backend.app.modules.society.cultura.infrastructure.models.evento_cultural_model import EventoCulturalModel
    from apps.backend.app.modules.society.cultura.infrastructure.models.grupo_artistico_model import GrupoArtisticoModel
    from apps.backend.app.modules.society.cultura.infrastructure.models.patrimonio_imaterial_model import PatrimonioImaterialModel
    if not hasattr(ArtistaModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [ArtistaModel.__table__, BemCulturalModel.__table__, EventoCulturalModel.__table__, GrupoArtisticoModel.__table__, PatrimonioImaterialModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM cultura_eventos_culturais'))
    await session.execute(text('DELETE FROM cultura_patrimonios_imateriais'))
    await session.execute(text('DELETE FROM cultura_grupos_artisticos'))
    await session.execute(text('DELETE FROM cultura_bens_culturais'))
    await session.execute(text('DELETE FROM cultura_artistas'))
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
def test_fluxo_real_orm_artista_bem_evento() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_artista_repository import SQLAlchemyArtistaRepository
            from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_bem_cultural_repository import SQLAlchemyBemCulturalRepository
            from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_evento_cultural_repository import SQLAlchemyEventoCulturalRepository
            from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_grupo_artistico_repository import SQLAlchemyGrupoArtisticoRepository
            from apps.backend.app.modules.society.cultura.infrastructure.repositories.sqlalchemy_patrimonio_imaterial_repository import SQLAlchemyPatrimonioImaterialRepository
            from apps.backend.app.modules.society.cultura.application.services.grupo_artistico_service import GrupoArtisticoService
            from apps.backend.app.modules.society.cultura.application.services.patrimonio_imaterial_service import PatrimonioImaterialService
            artista_repo = SQLAlchemyArtistaRepository(session)
            bem_repo = SQLAlchemyBemCulturalRepository(session)
            evento_repo = SQLAlchemyEventoCulturalRepository(session)
            grupo_repo = SQLAlchemyGrupoArtisticoRepository(session)
            patrimonio_repo = SQLAlchemyPatrimonioImaterialRepository(session)
            artista_service = ArtistaService(artista_repo=artista_repo)
            bem_service = BemCulturalService(bem_repo=bem_repo)
            evento_service = EventoCulturalService(evento_repo=evento_repo, artista_repo=artista_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True))
            grupo_service = GrupoArtisticoService(grupo_repo=grupo_repo, artista_repo=artista_repo, educacao_service=FakeEducacaoService(exists=True))
            patrimonio_service = PatrimonioImaterialService(patrimonio_repo=patrimonio_repo, turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True))
            artista = await artista_service.cadastrar_artista(nome='Artista Integracao', tipo=[TipoArtista.MUSICO, TipoArtista.ESCRITOR])
            bem = await bem_service.cadastrar_bem(nome='Monumento Integracao', tipo=TipoPatrimonio.HISTORICO, descricao='Monumento de valor historico', localizacao='Centro', municipio='Luanda', provincia='Luanda')
            evento = await evento_service.cadastrar_evento(nome='Festival Integracao', tipo=TipoEventoCultural.FESTIVAL, descricao='Evento integrado', data_inicio=date(2026, 7, 1), data_fim=date(2026, 7, 2), local='Memorial', municipio='Luanda', provincia='Luanda', realizador_id=artista.id, atracao_turistica_id=uuid4(), instituicao_educacional_id=uuid4())
            tombado = await bem_service.tombar_bem(bem.id)
            evento_atualizado = await evento_service.atualizar_evento(evento_id=evento.id, status=StatusEventoCultural.PUBLICADO)
            grupo = await grupo_service.cadastrar_grupo(nome='Grupo Integracao', tipo=TipoGrupoArtistico.COLETIVO, lider_artista_id=artista.id, instituicao_educacional_id=uuid4())
            patrimonio = await patrimonio_service.registrar_patrimonio(nome='Tradicao Integracao', categoria=CategoriaPatrimonioImaterial.TRADICAO, descricao='Tradicao comunitaria viva e registrada no sistema.', comunidade='Comunidade Integracao', municipio='Luanda', provincia='Luanda', atracao_turistica_id=uuid4(), instituicao_educacional_id=uuid4())
            patrimonio_atualizado = await patrimonio_service.atualizar_patrimonio(patrimonio_id=patrimonio.id, status=StatusPatrimonioImaterial.REGISTRADO)
            assert artista.registro_cultural.startswith('ART/')
            assert tombado.status_tombamento == StatusTombamento.TOMBADO
            assert evento_atualizado.status == StatusEventoCultural.PUBLICADO
            assert grupo.codigo_grupo.startswith('GRP/')
            assert patrimonio_atualizado.status == StatusPatrimonioImaterial.REGISTRADO
    asyncio.run(scenario())