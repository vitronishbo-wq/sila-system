from __future__ import annotations

import os
from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.georreferenciamento_service import (
    GeorreferenciamentoService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.matricula_imovel_service import (
    MatriculaImovelService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    NaturezaImovel,
    TipoDesapropriacao,
    TipoImovel,
    TipoOneracao,
    TipoRegistro,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.desapropriacao import (
    Desapropriacao,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.imovel import (
    Imovel,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.oneracao import (
    Oneracao,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import (
    SQLAlchemyDesapropriacaoRepository,
    SQLAlchemyGeorreferenciamentoRepository,
    SQLAlchemyImovelRepository,
    SQLAlchemyMatriculaImovelRepository,
    SQLAlchemyOneracaoRepository,
)


def _get_database_url() -> str:
    url = os.environ.get(
        "DATABASE_URL", "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db"
    )
    if "sqlite" in url:
        raise RuntimeError("Testes ORM reais exigem PostgreSQL")
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(_get_database_url(), echo=False, poolclass=NullPool)
    async with engine.connect() as conn:
        trans = await conn.begin()
        factory = sessionmaker(
            bind=conn, class_=AsyncSession, expire_on_commit=False, autocommit=False
        )
        async with factory() as session:
            await session.begin()
            try:
                yield session
            finally:
                try:
                    await session.rollback()
                except Exception:
                    pass
        try:
            await trans.rollback()
        except Exception:
            pass
    await engine.dispose()


async def _assert_table_exists(db_session: AsyncSession, table_name: str) -> None:
    result = await db_session.execute(
        text("SELECT to_regclass(:table_name)"), {"table_name": table_name}
    )
    assert result.scalar_one_or_none() is not None, f"Tabela fisica ausente: {table_name}"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_oneracoes_desapropriacoes_repositories_com_orm_real(
    db_session: AsyncSession,
) -> None:
    await _assert_table_exists(db_session, "gestao_fundiaria_imoveis")
    await _assert_table_exists(db_session, "gestao_fundiaria_oneracoes")
    await _assert_table_exists(db_session, "gestao_fundiaria_desapropriacoes")
    imovel_repo = SQLAlchemyImovelRepository(db_session)
    oneracao_repo = SQLAlchemyOneracaoRepository(db_session)
    desapropriacao_repo = SQLAlchemyDesapropriacaoRepository(db_session)
    imovel = await imovel_repo.save(
        Imovel.cadastrar(
            tipo=TipoImovel.URBANO,
            natureza=NaturezaImovel.PRIVADO,
            area_total=Decimal("750.00"),
            endereco="Rua do ORM, 1",
            bairro="Centro",
            municipio="Luanda",
            provincia="Luanda",
            inscricao_imobiliaria=f"IMV/{date.today().year}/{uuid4().hex[:6]}",
        )
    )
    numero_oneracao = await oneracao_repo.next_numero()
    oneracao = await oneracao_repo.save(
        Oneracao.registrar(
            numero_oneracao=numero_oneracao,
            imovel_inscricao=imovel.inscricao_imobiliaria,
            tipo=TipoOneracao.HIPOTECA,
            credor_nome="Banco Integracao",
            valor=Decimal("250000.00"),
        )
    )
    oneracao_db = await oneracao_repo.get_by_numero(numero_oneracao)
    numero_processo = await desapropriacao_repo.next_numero_processo()
    desapropriacao = await desapropriacao_repo.save(
        Desapropriacao.instaurar(
            numero_processo=numero_processo,
            imovel_inscricao=imovel.inscricao_imobiliaria,
            tipo=TipoDesapropriacao.UTILIDADE_PUBLICA,
            ente_publico="Governo Provincial",
            finalidade="Ampliacao viaria",
            valor_indenizacao=Decimal("980000.00"),
        )
    )
    desapropriacao_db = await desapropriacao_repo.get_by_numero_processo(numero_processo)
    oneracoes_imovel = await oneracao_repo.list(imovel_inscricao=imovel.inscricao_imobiliaria)
    desapropriacoes_imovel = await desapropriacao_repo.list(
        imovel_inscricao=imovel.inscricao_imobiliaria
    )
    assert oneracao.id == oneracao_db.id
    assert desapropriacao.id == desapropriacao_db.id
    assert len(oneracoes_imovel) == 1
    assert len(desapropriacoes_imovel) == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_slice_matricula_georreferenciamento_cross_modulo_com_orm_real(
    db_session: AsyncSession,
) -> None:
    await _assert_table_exists(db_session, "gestao_fundiaria_imoveis")
    await _assert_table_exists(db_session, "gestao_fundiaria_matriculas_imovel")
    await _assert_table_exists(db_session, "gestao_fundiaria_georreferenciamentos")
    imovel_repo = SQLAlchemyImovelRepository(db_session)
    matricula_repo = SQLAlchemyMatriculaImovelRepository(db_session)
    geo_repo = SQLAlchemyGeorreferenciamentoRepository(db_session)
    imovel = await imovel_repo.save(
        Imovel.cadastrar(
            tipo=TipoImovel.RURAL,
            natureza=NaturezaImovel.PRIVADO,
            area_total=Decimal("5000.00"),
            endereco="Via Rural 20",
            bairro="Zona 7",
            municipio="Huambo",
            provincia="Huambo",
            inscricao_imobiliaria=f"IMV/{date.today().year}/{uuid4().hex[:6]}",
        )
    )
    justica_adapter = AsyncMock()
    justica_adapter.validar_matricula = AsyncMock(return_value=True)
    matricula_service = MatriculaImovelService(
        matricula_repo=matricula_repo, imovel_repo=imovel_repo, justica_adapter=justica_adapter
    )
    geosampa_adapter = AsyncMock()
    geosampa_adapter.validar_coordenadas = AsyncMock(return_value=True)
    georreferenciamento_service = GeorreferenciamentoService(
        georreferenciamento_repo=geo_repo,
        imovel_repo=imovel_repo,
        geosampa_adapter=geosampa_adapter,
    )
    matricula = await matricula_service.registrar(
        imovel_inscricao=imovel.inscricao_imobiliaria,
        tipo_registro=TipoRegistro.MATRICULA,
        cartorio_nome="Cartorio Integracao",
        livro="10",
        folha="22",
        comarca="Huambo",
        provincia="Huambo",
        proprietario_documento="BI998877",
    )
    georreferenciamento = await georreferenciamento_service.registrar(
        imovel_inscricao=imovel.inscricao_imobiliaria,
        latitude=Decimal("-12.50000000"),
        longitude=Decimal("15.70000000"),
        precisao_metros=Decimal("1.00"),
        area_calculada=Decimal("5000.15"),
    )
    imovel_atualizado = await imovel_repo.get_by_inscricao(imovel.inscricao_imobiliaria)
    matriculas = await matricula_repo.list(imovel_inscricao=imovel.inscricao_imobiliaria)
    georreferenciamentos = await geo_repo.list(imovel_inscricao=imovel.inscricao_imobiliaria)
    assert matricula.id == matriculas[0].id
    assert georreferenciamento.id == georreferenciamentos[0].id
    assert imovel_atualizado is not None
    assert imovel_atualizado.matricula_id == matricula.id
    assert imovel_atualizado.coordenadas_lat == Decimal("-12.50000000")
    assert imovel_atualizado.coordenadas_long == Decimal("15.70000000")
    justica_adapter.validar_matricula.assert_awaited_once()
    geosampa_adapter.validar_coordenadas.assert_awaited()
