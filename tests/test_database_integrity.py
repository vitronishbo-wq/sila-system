"""
Testes de Integridade do Banco de Dados SILA

Valida:
- Estrutura Lei 14/24 (21 províncias, 6 municípios, 5 comunas)
- Usuários corretos (5 usuários com roles e regions)
- Relacionamentos e FK integridade
- Sem registros órfãos
"""

import os

import asyncpg
import pytest

RUN_DB_INTEGRATION = os.getenv("RUN_DB_INTEGRATION", "0") == "1"
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not RUN_DB_INTEGRATION,
        reason="Requires seeded Postgres dataset. Set RUN_DB_INTEGRATION=1 to run.",
    ),
]


async def fetch_location_id(conn, name: str, territory_type: str):
    return await conn.fetchval(
        "SELECT id FROM locations WHERE name=$1 AND type=$2",
        name,
        territory_type,
    )


@pytest.fixture
async def db_connection():
    """Conexão direta ao banco PostgreSQL para testes."""
    conn = await asyncpg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        user=os.getenv("DB_USER", "sila_user"),
        password=os.getenv("DB_PASSWORD", "Trumanmarcelo_1983"),
        database=os.getenv("DB_NAME", "sila_db"),
    )
    yield conn
    await conn.close()


@pytest.mark.asyncio
async def test_01_locations_table_exists(db_connection):
    """Valida que tabela locations existe."""
    result = await db_connection.fetchval(
        "SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name = 'locations')"
    )
    assert result, "Tabela 'locations' não existe"


@pytest.mark.asyncio
async def test_02_provinces_count(db_connection):
    """Valida Lei 14/24: exatamente 21 províncias."""
    count = await db_connection.fetchval("SELECT COUNT(*) FROM locations WHERE type = 'PROVINCIA'")
    assert count == 21, f"Esperado 21 províncias, encontrado {count}"


@pytest.mark.asyncio
async def test_03_municipalities_count(db_connection):
    """Valida Lei 14/24: exatamente 6 municípios."""
    count = await db_connection.fetchval("SELECT COUNT(*) FROM locations WHERE type = 'MUNICIPIO'")
    assert count == 6, f"Esperado 6 municípios, encontrado {count}"


@pytest.mark.asyncio
async def test_04_communes_count(db_connection):
    """Valida Lei 14/24: exatamente 5 comunas."""
    count = await db_connection.fetchval("SELECT COUNT(*) FROM locations WHERE type = 'COMUNA'")
    assert count == 5, f"Esperado 5 comunas, encontrado {count}"


@pytest.mark.asyncio
async def test_05_users_table_exists(db_connection):
    """Valida que tabela users existe."""
    result = await db_connection.fetchval(
        "SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name = 'users')"
    )
    assert result, "Tabela 'users' não existe"


@pytest.mark.asyncio
async def test_06_users_count_is_5(db_connection):
    """Valida que existem exatamente 5 usuários."""
    count = await db_connection.fetchval("SELECT COUNT(*) FROM users")
    assert count == 5, f"Esperado 5 usuários, encontrado {count}"


@pytest.mark.asyncio
async def test_07_admin_user_exists(db_connection):
    """Valida que admin central existe."""
    user = await db_connection.fetchrow(
        """
        SELECT email, administrative_level, region_id 
        FROM users 
        WHERE email = 'central@sila.gov.ao'
        """
    )
    assert user is not None, "Admin central@sila.gov.ao não existe"
    assert user["administrative_level"] == "SUPER", (
        f"Admin deve ser SUPER, é {user['administrative_level']}"
    )
    assert user["region_id"] is None, f"Admin region_id deve ser NULL, é {user['region_id']}"


@pytest.mark.asyncio
async def test_08_provincial_manager_exists(db_connection):
    """Valida que gerente provincial existe."""
    huambo_id = await fetch_location_id(db_connection, "Huambo", "PROVINCIA")
    user = await db_connection.fetchrow(
        """
        SELECT email, administrative_level, region_id 
        FROM users 
        WHERE email = 'prov.huambo@sila.gov.ao'
        """
    )
    assert user is not None, "Provincial prov.huambo@sila.gov.ao não existe"
    assert user["administrative_level"] == "PROVINCIAL", (
        f"Deve ser PROVINCIAL, é {user['administrative_level']}"
    )
    assert user["region_id"] == huambo_id, (
        f"Huambo region_id deve ser {huambo_id}, é {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_09_municipal_manager_exists(db_connection):
    """Valida que gerente municipal existe."""
    huambo_mun_id = await fetch_location_id(db_connection, "Huambo (Município)", "MUNICIPIO")
    user = await db_connection.fetchrow(
        """
        SELECT email, administrative_level, region_id 
        FROM users 
        WHERE email = 'mun.huambo@sila.gov.ao'
        """
    )
    assert user is not None, "Municipal mun.huambo@sila.gov.ao não existe"
    assert user["administrative_level"] == "MUNICIPAL", (
        f"Deve ser MUNICIPAL, é {user['administrative_level']}"
    )
    assert user["region_id"] == huambo_mun_id, (
        f"Huambo mun region_id deve ser {huambo_mun_id}, é {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_10_communal_officer_exists(db_connection):
    """Valida que oficial comunal existe."""
    comuna_centro_id = await fetch_location_id(db_connection, "Comuna Centro", "COMUNA")
    user = await db_connection.fetchrow(
        """
        SELECT email, administrative_level, region_id 
        FROM users 
        WHERE email = 'comun.huambo@sila.gov.ao'
        """
    )
    assert user is not None, "Communal comun.huambo@sila.gov.ao não existe"
    assert user["administrative_level"] == "COMMUNAL", (
        f"Deve ser COMMUNAL, é {user['administrative_level']}"
    )
    assert user["region_id"] == comuna_centro_id, (
        f"Comuna region_id deve ser {comuna_centro_id}, é {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_11_citizen_exists(db_connection):
    """Valida que cidadão existe."""
    comuna_centro_id = await fetch_location_id(db_connection, "Comuna Centro", "COMUNA")
    user = await db_connection.fetchrow(
        """
        SELECT email, administrative_level, region_id 
        FROM users 
        WHERE email = 'truman@gmail.com'
        """
    )
    assert user is not None, "Citizen truman@gmail.com não existe"
    assert user["administrative_level"] == "LOCAL", (
        f"Deve ser LOCAL, é {user['administrative_level']}"
    )
    assert user["region_id"] == comuna_centro_id, (
        f"Cidadão region_id deve ser {comuna_centro_id}, é {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_12_no_orphaned_users(db_connection):
    """Valida que não há usuários órfãos (sem region_id válido quando necessário)."""
    orphaned = await db_connection.fetch(
        """
        SELECT u.id, u.email, u.region_id 
        FROM users u
        LEFT JOIN locations l ON u.region_id = l.id
        WHERE u.region_id IS NOT NULL AND l.id IS NULL
        """
    )
    assert len(orphaned) == 0, f"Encontrados usuários órfãos: {orphaned}"


@pytest.mark.asyncio
async def test_13_all_provinces_have_null_parent(db_connection):
    """Valida que todas as províncias têm parent_id = NULL."""
    invalid = await db_connection.fetch(
        """
        SELECT id, name, parent_id 
        FROM locations 
        WHERE type = 'PROVINCIA' AND parent_id IS NOT NULL
        """
    )
    assert len(invalid) == 0, f"Províncias com parent_id != NULL: {invalid}"


@pytest.mark.asyncio
async def test_14_all_municipalities_have_parent(db_connection):
    """Valida que todos os municípios têm parent_id válido."""
    invalid = await db_connection.fetch(
        """
        SELECT id, name, parent_id 
        FROM locations 
        WHERE type = 'MUNICIPIO' AND parent_id IS NULL
        """
    )
    assert len(invalid) == 0, f"Municípios sem parent_id: {invalid}"


@pytest.mark.asyncio
async def test_15_all_communes_have_parent(db_connection):
    """Valida que todas as comunas têm parent_id válido."""
    invalid = await db_connection.fetch(
        """
        SELECT id, name, parent_id 
        FROM locations 
        WHERE type = 'COMUNA' AND parent_id IS NULL
        """
    )
    assert len(invalid) == 0, f"Comunas sem parent_id: {invalid}"


@pytest.mark.asyncio
async def test_16_no_circular_references(db_connection):
    """Valida que não há referências circulares."""
    circular = await db_connection.fetch(
        """
        WITH RECURSIVE path AS (
          SELECT id, parent_id, 1 as depth
          FROM locations
          WHERE parent_id IS NOT NULL
          UNION ALL
          SELECT p.id, l.parent_id, p.depth + 1
          FROM path p
          JOIN locations l ON p.parent_id = l.id
          WHERE p.depth < 10
        )
        SELECT DISTINCT id FROM path WHERE depth > 5
        """
    )
    assert len(circular) == 0, f"Referências circulares encontradas: {circular}"


@pytest.mark.asyncio
async def test_17_huambo_hierarchy(db_connection):
    """Valida hierarquia Huambo: prov(7) -> mun(22) -> com(28)."""
    prov = await db_connection.fetchval(
        "SELECT id FROM locations WHERE name = 'Huambo' AND type = 'PROVINCIA'"
    )
    mun = await db_connection.fetchrow(
        "SELECT id, parent_id FROM locations WHERE name = 'Huambo (Município)' AND type = 'MUNICIPIO'"
    )
    com = await db_connection.fetchrow(
        "SELECT id, parent_id FROM locations WHERE name = 'Comuna Centro' AND type = 'COMUNA'"
    )

    assert prov is not None, "Huambo província não encontrada"
    assert mun is not None, "Huambo município não encontrado"
    assert com is not None, "Comuna Centro não encontrada"
    assert mun["parent_id"] == prov, f"Huambo mun deve ter parent_id=Huambo, tem {mun['parent_id']}"
    assert com["parent_id"] == mun["id"], (
        f"Comuna Centro deve ter parent_id=Huambo Município, tem {com['parent_id']}"
    )


@pytest.mark.asyncio
async def test_18_all_users_active(db_connection):
    """Valida que todos os 5 usuários estão ativos."""
    inactive = await db_connection.fetchval("SELECT COUNT(*) FROM users WHERE is_active = false")
    assert inactive == 0, f"Encontrados {inactive} usuários inativos"
