from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.domain.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.society.juventude.application.services.auxilio_service import AuxilioService
from apps.backend.app.modules.society.juventude.application.services.formacao_service import FormacaoService
from apps.backend.app.modules.society.juventude.application.services.jovem_service import JovemService
from apps.backend.app.modules.society.juventude.application.services.programa_service import ProgramaService
from apps.backend.app.modules.society.juventude.domain.enums import Escolaridade, SituacaoOcupacional, TipoAuxilio, TipoPrograma
from apps.backend.app.modules.society.juventude.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService

def _tables():
    from apps.backend.app.modules.society.juventude.infrastructure.models.auxilio_model import AuxilioModel
    from apps.backend.app.modules.society.juventude.infrastructure.models.formacao_juvenil_model import FormacaoJuvenilModel
    from apps.backend.app.modules.society.juventude.infrastructure.models.jovem_model import JovemModel
    from apps.backend.app.modules.society.juventude.infrastructure.models.programa_juvenil_model import ProgramaJuvenilModel
    if not hasattr(JovemModel, '__table__'):
        pytest.skip('ORM mappers limpos por conftest global apos import de modelos; executar este teste sem tests/conftest ou revisar clear_mappers global.')
    return [JovemModel.__table__, AuxilioModel.__table__, ProgramaJuvenilModel.__table__, FormacaoJuvenilModel.__table__]

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_tables()))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM juventude_formacoes'))
    await session.execute(text('DELETE FROM juventude_programas'))
    await session.execute(text('DELETE FROM juventude_auxilios'))
    await session.execute(text('DELETE FROM juventude_jovens'))
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
def test_fluxo_real_orm_jovem_auxilio_programa_formacao() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_auxilio_repository import SQLAlchemyAuxilioRepository
            from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_formacao_repository import SQLAlchemyFormacaoRepository
            from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_jovem_repository import SQLAlchemyJovemRepository
            from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_programa_repository import SQLAlchemyProgramaRepository
            jovem_repo = SQLAlchemyJovemRepository(session)
            auxilio_repo = SQLAlchemyAuxilioRepository(session)
            programa_repo = SQLAlchemyProgramaRepository(session)
            formacao_repo = SQLAlchemyFormacaoRepository(session)
            jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
            auxilio_service = AuxilioService(auxilio_repo=auxilio_repo, jovem_repo=jovem_repo)
            programa_service = ProgramaService(programa_repo=programa_repo)
            formacao_service = FormacaoService(formacao_repo=formacao_repo, jovem_repo=jovem_repo, programa_repo=programa_repo)
            jovem = await jovem_service.cadastrar_jovem(nome='Jovem Integracao', data_nascimento=date.today() - timedelta(days=365 * 21), genero='M', naturalidade='Luanda', escolaridade=Escolaridade.SUPERIOR_INCOMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA_TRABALHA, endereco='Rua Integracao', municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
            auxilio = await auxilio_service.conceder_auxilio(jovem_id=jovem.id, tipo=TipoAuxilio.ALIMENTACAO, data_inicio=date.today(), valor_mensal=Decimal('25000.00'))
            programa = await programa_service.criar_programa(nome='Programa ORM Juventude', tipo=TipoPrograma.CAPACITACAO, data_inicio=date.today(), vagas=50, municipio='Luanda', provincia='Luanda')
            formacao = await formacao_service.registrar_formacao(jovem_id=jovem.id, programa_id=programa.id, nome_curso='Curso ORM Juventude', instituicao='Centro ORM', carga_horaria=40, data_inicio=date.today())
            assert jovem.numero_registro.startswith('JOV/')
            assert auxilio.codigo_auxilio.startswith('AUX/')
            assert auxilio.jovem_id == jovem.id
            assert programa.codigo_programa.startswith('PRG/')
            assert formacao.codigo_formacao.startswith('FRM/')
            assert formacao.programa_id == programa.id
    asyncio.run(scenario())