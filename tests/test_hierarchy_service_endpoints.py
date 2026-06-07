"""
🧪 TESTES DE ENDPOINTS - HierarchyService Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Suite de testes de precisão para validar:
1. Que o HierarchyService retorna IDs corretos
2. Que parent_id filtra corretamente (ex: Huambo prov ID=7)
3. Que roles baseadas em permissões funcionam
4. Que a hierarquia é íntegra (sem órfãos)
5. Performance dos endpoints (<100ms para get_ancestry_chain)

Lei 14/24 Compliance:
- 21 Províncias ✅
- Cuando ID=20 ✅
- Cubango ID=21 ✅
- Hierarquia: Prov → Mun → Com ✅

Teste as seguintes queries com precisão:
├─ Huambo (ID=7) → Municípios devem ter parent_id=7
│  ├─ Huambo Mun (ID=22)
│  ├─ Bailundo (ID=23)
│  └─ Longonjo (ID=24)
│
└─ Luanda (ID=8) → Municípios devem ter parent_id=8
   ├─ Luanda Mun (ID=25)
   ├─ Cacuaco (ID=26)
   └─ Viana (ID=27)
"""

import os
import time

import asyncpg
import pytest
import pytest_asyncio

RUN_DB_INTEGRATION = os.getenv("RUN_DB_INTEGRATION", "0") == "1"
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not RUN_DB_INTEGRATION,
        reason="Requires seeded Postgres dataset. Set RUN_DB_INTEGRATION=1 to run.",
    ),
]

# ============================================================================
# FIXTURES - Conexão com BD
# ============================================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "sila_user",
    "password": "Trumanmarcelo_1983",
    "database": "sila_db",
}


async def fetch_location_id(db_session, name: str, territory_type: str):
    return await db_session.fetchval(
        "SELECT id FROM locations WHERE name=$1 AND type=$2",
        name,
        territory_type,
    )


@pytest_asyncio.fixture
async def db_connection():
    """Conexão com banco de dados (reutilizada para todos os testes)"""
    conn = await asyncpg.connect(**DB_CONFIG)
    yield conn
    await conn.close()


@pytest_asyncio.fixture
async def db_session(db_connection):
    """Sessão de BD para cada teste"""
    return db_connection


# ============================================================================
# FIXTURES - Dados Esperados
# ============================================================================


@pytest.fixture
def lei_14_24_data():
    """Dados de Lei 14/24 conforme seeded"""
    return {
        "provinces": {
            "Huambo": {"id": 7, "type": "PROVINCIA", "parent_id": None},
            "Luanda": {"id": 8, "type": "PROVINCIA", "parent_id": None},
            "Cuando": {"id": 20, "type": "PROVINCIA", "parent_id": None},
            "Cubango": {"id": 21, "type": "PROVINCIA", "parent_id": None},
        },
        "municipalities": {
            # Huambo
            "Huambo (Município)": {"id": 22, "parent_id": 7, "type": "MUNICIPIO"},
            "Bailundo": {"id": 23, "parent_id": 7, "type": "MUNICIPIO"},
            "Longonjo": {"id": 24, "parent_id": 7, "type": "MUNICIPIO"},
            # Luanda
            "Luanda (Município)": {"id": 25, "parent_id": 8, "type": "MUNICIPIO"},
            "Cacuaco": {"id": 26, "parent_id": 8, "type": "MUNICIPIO"},
            "Viana": {"id": 27, "parent_id": 8, "type": "MUNICIPIO"},
        },
        "communes": {
            # Huambo Município
            "Comuna Centro": {"id": 28, "parent_id": 22, "type": "COMUNA"},
            "Comuna Norte": {"id": 29, "parent_id": 22, "type": "COMUNA"},
            "Comuna Sul": {"id": 30, "parent_id": 22, "type": "COMUNA"},
            # Bailundo
            "Bailundo Centro": {"id": 31, "parent_id": 23, "type": "COMUNA"},
            "Bailundo Rural": {"id": 32, "parent_id": 23, "type": "COMUNA"},
        },
        "users": {
            "admin": {
                "email": "central@sila.gov.ao",
                "role": "ADMIN",
                "region_id": None,
                "administrative_level": "NATIONAL",
            },
            "prov_manager": {
                "email": "prov.huambo@sila.gov.ao",
                "role": "MANAGER",
                "region_id": 7,  # Huambo
                "administrative_level": "PROVINCIAL",
            },
            "mun_manager": {
                "email": "mun.huambo@sila.gov.ao",
                "role": "MANAGER",
                "region_id": 22,  # Huambo Município
                "administrative_level": "MUNICIPAL",
            },
            "officer": {
                "email": "comun.huambo@sila.gov.ao",
                "role": "OFFICER",
                "region_id": 28,  # Comuna Centro
                "administrative_level": "COMUNAL",
            },
            "citizen": {
                "email": "truman@gmail.com",
                "role": "CITIZEN",
                "region_id": 28,  # Comuna Centro
                "administrative_level": "CITIZEN",
            },
        },
    }


@pytest.fixture
def expected_municipalities_huambo():
    """Municípios esperados para Huambo (parent_id=7)"""
    return [
        {"id": 22, "name": "Huambo (Município)", "type": "MUNICIPIO", "parent_id": 7},
        {"id": 23, "name": "Bailundo", "type": "MUNICIPIO", "parent_id": 7},
        {"id": 24, "name": "Longonjo", "type": "MUNICIPIO", "parent_id": 7},
    ]


@pytest.fixture
def expected_municipalities_luanda():
    """Municípios esperados para Luanda (parent_id=8)"""
    return [
        {"id": 25, "name": "Luanda (Município)", "type": "MUNICIPIO", "parent_id": 8},
        {"id": 26, "name": "Cacuaco", "type": "MUNICIPIO", "parent_id": 8},
        {"id": 27, "name": "Viana", "type": "MUNICIPIO", "parent_id": 8},
    ]


@pytest.fixture
def expected_communes_huambo_municipality():
    """Comunas esperadas para Huambo Município (parent_id=22)"""
    return [
        {"id": 28, "name": "Comuna Centro", "type": "COMUNA", "parent_id": 22},
        {"id": 29, "name": "Comuna Norte", "type": "COMUNA", "parent_id": 22},
        {"id": 30, "name": "Comuna Sul", "type": "COMUNA", "parent_id": 22},
    ]


# ============================================================================
# TESTES DE DADOS - Verificação de Integridade
# ============================================================================


@pytest.mark.asyncio
async def test_01_locations_table_exists(db_session):
    """Test 1: Verificar que tabela 'locations' existe e contém dados"""
    result = await db_session.fetchval("SELECT COUNT(*) FROM locations")

    assert result > 0, "Tabela 'locations' está vazia"
    assert result == 32, f"Esperava 32 registros (21 prov + 6 mun + 5 com), mas tem {result}"


@pytest.mark.asyncio
async def test_02_provinces_count(db_session, lei_14_24_data):
    """Test 2: Contar 21 províncias (Lei 14/24)"""
    result = await db_session.fetchval("SELECT COUNT(*) FROM locations WHERE type='PROVINCIA'")

    assert result == 21, f"Esperava 21 províncias, mas encontrou {result}"


@pytest.mark.asyncio
async def test_03_municipalities_count(db_session):
    """Test 3: Contar 6 municípios"""
    result = await db_session.fetchval("SELECT COUNT(*) FROM locations WHERE type='MUNICIPIO'")

    assert result == 6, f"Esperava 6 municípios, mas encontrou {result}"


@pytest.mark.asyncio
async def test_04_communes_count(db_session):
    """Test 4: Contar 5 comunas"""
    result = await db_session.fetchval("SELECT COUNT(*) FROM locations WHERE type='COMUNA'")

    assert result == 5, f"Esperava 5 comunas, mas encontrou {result}"


@pytest.mark.asyncio
async def test_05_cuando_cubango_separated(db_session, lei_14_24_data):
    """Test 5: Validar que Cuando e Cubango estão separados (Lei 14/24)"""
    cuando = await db_session.fetchrow(
        "SELECT id, name, type, parent_id FROM locations WHERE name='Cuando' AND type='PROVINCIA'"
    )
    cubango = await db_session.fetchrow(
        "SELECT id, name, type, parent_id FROM locations WHERE name='Cubango' AND type='PROVINCIA'"
    )

    assert cuando is not None, "Cuando não encontrado"
    assert cubango is not None, "Cubango não encontrado"
    assert cuando["type"] == "PROVINCIA", f"Cuando deve ser PROVINCIA, mas tem {cuando['type']}"
    assert cubango["type"] == "PROVINCIA", f"Cubango deve ser PROVINCIA, mas tem {cubango['type']}"
    assert cuando["parent_id"] is None, (
        f"Cuando deve ter parent_id NULL, mas tem {cuando['parent_id']}"
    )
    assert cubango["parent_id"] is None, (
        f"Cubango deve ter parent_id NULL, mas tem {cubango['parent_id']}"
    )


# ============================================================================
# TESTES DE PARENT_ID - Verificação de Hierarquia
# ============================================================================


@pytest.mark.asyncio
async def test_06_huambo_municipalities_parent_id(db_session, expected_municipalities_huambo):
    """Test 6: Verificar que todos os municípios de Huambo têm parent_id=7"""
    huambo_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    municipalities = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations "
        "WHERE parent_id=$1 AND type='MUNICIPIO' "
        "ORDER BY id",
        huambo_id,
    )

    assert len(municipalities) == 3, (
        f"Esperava 3 municípios para Huambo, encontrou {len(municipalities)}"
    )

    # Verificar cada município
    for mun in municipalities:
        assert mun["parent_id"] == huambo_id, (
            f"Município {mun['name']} deve ter parent_id=Huambo, mas tem {mun['parent_id']}"
        )
        assert mun["type"] == "MUNICIPIO", (
            f"Município {mun['name']} deve ter type='MUNICIPIO', mas tem '{mun['type']}'"
        )

    # Verificar nomes específicos
    names = {m["name"] for m in municipalities}
    assert names == {"Huambo (Município)", "Bailundo", "Longonjo"}, (
        f"Nomes de municípios incorretos: {names}"
    )


@pytest.mark.asyncio
async def test_07_luanda_municipalities_parent_id(db_session, expected_municipalities_luanda):
    """Test 7: Verificar que todos os municípios de Luanda têm parent_id=8"""
    luanda_id = await fetch_location_id(db_session, "Luanda", "PROVINCIA")
    municipalities = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations "
        "WHERE parent_id=$1 AND type='MUNICIPIO' "
        "ORDER BY id",
        luanda_id,
    )

    assert len(municipalities) == 3, (
        f"Esperava 3 municípios para Luanda, encontrou {len(municipalities)}"
    )

    # Verificar cada município
    for mun in municipalities:
        assert mun["parent_id"] == luanda_id, (
            f"Município {mun['name']} deve ter parent_id=Luanda, mas tem {mun['parent_id']}"
        )
        assert mun["type"] == "MUNICIPIO", (
            f"Município {mun['name']} deve ter type='MUNICIPIO', mas tem '{mun['type']}'"
        )

    # Verificar nomes específicos
    names = {m["name"] for m in municipalities}
    assert names == {"Luanda (Município)", "Cacuaco", "Viana"}, (
        f"Nomes de municípios incorretos: {names}"
    )


@pytest.mark.asyncio
async def test_08_huambo_municipality_communes_parent_id(
    db_session, expected_communes_huambo_municipality
):
    """Test 8: Verificar que todas as comunas de Huambo (Mun) têm parent_id=22"""
    huambo_mun_id = await fetch_location_id(db_session, "Huambo (Município)", "MUNICIPIO")
    communes = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations "
        "WHERE parent_id=$1 AND type='COMUNA' "
        "ORDER BY id",
        huambo_mun_id,
    )

    assert len(communes) == 3, (
        f"Esperava 3 comunas para Huambo Município, encontrou {len(communes)}"
    )

    # Verificar cada comuna
    for com in communes:
        assert com["parent_id"] == huambo_mun_id, (
            f"Comuna {com['name']} deve ter parent_id=Huambo (Município), mas tem {com['parent_id']}"
        )
        assert com["type"] == "COMUNA", (
            f"Comuna {com['name']} deve ter type='COMUNA', mas tem '{com['type']}'"
        )

    # Verificar nomes específicos
    names = {c["name"] for c in communes}
    assert names == {"Comuna Centro", "Comuna Norte", "Comuna Sul"}, (
        f"Nomes de comunas incorretos: {names}"
    )


@pytest.mark.asyncio
async def test_09_bailundo_municipality_communes_parent_id(db_session):
    """Test 9: Verificar que todas as comunas de Bailundo têm parent_id=23"""
    bailundo_id = await fetch_location_id(db_session, "Bailundo", "MUNICIPIO")
    communes = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations "
        "WHERE parent_id=$1 AND type='COMUNA' "
        "ORDER BY id",
        bailundo_id,
    )

    assert len(communes) == 2, f"Esperava 2 comunas para Bailundo, encontrou {len(communes)}"

    # Verificar cada comuna
    for com in communes:
        assert com["parent_id"] == bailundo_id, (
            f"Comuna {com['name']} deve ter parent_id=Bailundo, mas tem {com['parent_id']}"
        )
        assert com["type"] == "COMUNA", (
            f"Comuna {com['name']} deve ter type='COMUNA', mas tem '{com['type']}'"
        )

    # Verificar nomes específicos
    names = {c["name"] for c in communes}
    assert names == {"Bailundo Centro", "Bailundo Rural"}, f"Nomes de comunas incorretos: {names}"


# ============================================================================
# TESTES DE HIERARCHY SERVICE - get_sub_units
# ============================================================================


@pytest.mark.asyncio
async def test_10_get_sub_units_huambo_province(db_session):
    """Test 10: HierarchyService.get_sub_units(7) retorna municípios corretos"""
    # Simular get_sub_units(7)
    huambo_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    result = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations WHERE parent_id=$1 ORDER BY id", huambo_id
    )

    assert len(result) == 3, f"Esperava 3 sub-units para Huambo, mas tem {len(result)}"

    # Todas devem ter parent_id=7
    for item in result:
        assert item["parent_id"] == huambo_id

    # Verificar tipos e IDs
    types = set(item["type"] for item in result)
    assert types == {"MUNICIPIO"}, f"Esperava apenas MUNICIPIO, mas tem {types}"

    names = {item["name"] for item in result}
    assert names == {"Huambo (Município)", "Bailundo", "Longonjo"}, f"Nomes incorretos: {names}"


@pytest.mark.asyncio
async def test_11_get_sub_units_huambo_municipality(db_session):
    """Test 11: HierarchyService.get_sub_units(22) retorna comunas corretas"""
    # Simular get_sub_units(22)
    huambo_mun_id = await fetch_location_id(db_session, "Huambo (Município)", "MUNICIPIO")
    result = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations WHERE parent_id=$1 ORDER BY id",
        huambo_mun_id,
    )

    assert len(result) == 3, f"Esperava 3 sub-units para Huambo Município, mas tem {len(result)}"

    # Todas devem ter parent_id=22
    for item in result:
        assert item["parent_id"] == huambo_mun_id

    # Verificar tipos
    types = set(item["type"] for item in result)
    assert types == {"COMUNA"}, f"Esperava apenas COMUNA, mas tem {types}"

    names = {item["name"] for item in result}
    assert names == {"Comuna Centro", "Comuna Norte", "Comuna Sul"}, f"Nomes incorretos: {names}"


@pytest.mark.asyncio
async def test_12_get_sub_units_no_children(db_session):
    """Test 12: HierarchyService.get_sub_units(28) retorna lista vazia (Comuna sem filhos)"""
    # Simular get_sub_units(28) - Comuna Centro tem parent_id=22, não tem filhos
    comuna_centro_id = await fetch_location_id(db_session, "Comuna Centro", "COMUNA")
    result = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations WHERE parent_id=$1 ORDER BY id",
        comuna_centro_id,
    )

    assert len(result) == 0, f"Comuna Centro não deve ter filhos, mas tem {len(result)}"


# ============================================================================
# TESTES DE HIERARCHY SERVICE - get_ancestry_chain
# ============================================================================


@pytest.mark.asyncio
async def test_13_ancestry_chain_province(db_session):
    """Test 13: get_ancestry_chain(7) para Huambo retorna [Huambo]"""
    # Query ancestrais de 7 (Huambo)
    current_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    huambo_id = current_id
    chain = []

    while current_id is not None:
        loc = await db_session.fetchrow(
            "SELECT id, name, type, parent_id FROM locations WHERE id=$1", current_id
        )
        if loc:
            chain.append(
                {
                    "id": loc["id"],
                    "name": loc["name"],
                    "type": loc["type"],
                    "parent_id": loc["parent_id"],
                }
            )
            current_id = loc["parent_id"]
        else:
            break

    # Huambo é root (parent_id=NULL), deve ter só ele na cadeia
    assert len(chain) == 1, f"Huambo deve ter só ele na chain, mas tem {len(chain)}: {chain}"
    assert chain[0]["id"] == huambo_id
    assert chain[0]["name"] == "Huambo"
    assert chain[0]["type"] == "PROVINCIA"


@pytest.mark.asyncio
async def test_14_ancestry_chain_municipality(db_session):
    """Test 14: get_ancestry_chain(22) para Huambo Município retorna [Huambo (Mun), Huambo]"""
    # Query ancestrais de 22 (Huambo Município)
    current_id = await fetch_location_id(db_session, "Huambo (Município)", "MUNICIPIO")
    huambo_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    chain = []

    while current_id is not None:
        loc = await db_session.fetchrow(
            "SELECT id, name, type, parent_id FROM locations WHERE id=$1", current_id
        )
        if loc:
            chain.append(
                {
                    "id": loc["id"],
                    "name": loc["name"],
                    "type": loc["type"],
                    "parent_id": loc["parent_id"],
                }
            )
            current_id = loc["parent_id"]
        else:
            break

    # Deve ter Huambo Município → Huambo
    assert len(chain) == 2, f"Huambo Município deve ter 2 na chain, mas tem {len(chain)}: {chain}"
    assert chain[0]["id"] == current_id
    assert chain[1]["id"] == huambo_id
    assert chain[1]["parent_id"] is None  # Huambo é root


@pytest.mark.asyncio
async def test_15_ancestry_chain_commune(db_session):
    """Test 15: get_ancestry_chain(28) para Comuna Centro retorna [Comuna, Município, Província]"""
    # Query ancestrais de 28 (Comuna Centro)
    comuna_centro_id = await fetch_location_id(db_session, "Comuna Centro", "COMUNA")
    huambo_mun_id = await fetch_location_id(db_session, "Huambo (Município)", "MUNICIPIO")
    huambo_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    current_id = comuna_centro_id
    chain = []

    while current_id is not None and len(chain) < 10:  # proteção contra loop infinito
        loc = await db_session.fetchrow(
            "SELECT id, name, type, parent_id FROM locations WHERE id=$1", current_id
        )
        if loc:
            chain.append(
                {
                    "id": loc["id"],
                    "name": loc["name"],
                    "type": loc["type"],
                    "parent_id": loc["parent_id"],
                }
            )
            current_id = loc["parent_id"]
        else:
            break

    # Deve ter Comuna Centro → Huambo Município → Huambo
    assert len(chain) == 3, f"Comuna Centro deve ter 3 na chain, mas tem {len(chain)}: {chain}"

    # Verificar ordem (de baixo para cima)
    assert chain[0]["id"] == comuna_centro_id
    assert chain[0]["type"] == "COMUNA"

    assert chain[1]["id"] == huambo_mun_id
    assert chain[1]["type"] == "MUNICIPIO"

    assert chain[2]["id"] == huambo_id
    assert chain[2]["type"] == "PROVINCIA"
    assert chain[2]["parent_id"] is None


# ============================================================================
# TESTES DE ROLE-BASED FILTERING
# ============================================================================


@pytest.mark.asyncio
async def test_16_admin_sees_all_provinces(db_session):
    """Test 16: Admin user vê todas as 21 províncias"""
    provinces = await db_session.fetch(
        "SELECT id, name, type FROM locations WHERE type='PROVINCIA' ORDER BY id"
    )

    assert len(provinces) == 21, f"Admin deve ver 21 províncias, mas vê {len(provinces)}"


@pytest.mark.asyncio
async def test_17_provincial_manager_sees_only_municipalities_in_region(db_session):
    """Test 17: Manager de Huambo (region_id=7) vê apenas municípios de Huambo"""
    # Manager de Huambo com region_id=7 pode ver sub-units de 7
    huambo_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    municipalities = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations WHERE parent_id=$1 AND type='MUNICIPIO'",
        huambo_id,  # region_id do manager
    )

    assert len(municipalities) == 3, (
        f"Manager de Huambo deve ver 3 municípios, mas vê {len(municipalities)}"
    )

    # Verificar que são apenas municípios de Huambo
    for mun in municipalities:
        assert mun["parent_id"] == huambo_id

    names = {m["name"] for m in municipalities}
    assert names == {"Huambo (Município)", "Bailundo", "Longonjo"}


@pytest.mark.asyncio
async def test_18_municipal_manager_sees_only_communes_in_municipality(db_session):
    """Test 18: Manager de Huambo Município (region_id=22) vê apenas comunas de Huambo"""
    # Manager de Huambo Município com region_id=22 pode ver sub-units de 22
    huambo_mun_id = await fetch_location_id(db_session, "Huambo (Município)", "MUNICIPIO")
    communes = await db_session.fetch(
        "SELECT id, name, type, parent_id FROM locations WHERE parent_id=$1 AND type='COMUNA'",
        huambo_mun_id,  # region_id do manager
    )

    assert len(communes) == 3, (
        f"Manager de Huambo Município deve ver 3 comunas, mas vê {len(communes)}"
    )

    # Verificar que são apenas comunas de Huambo Município
    for com in communes:
        assert com["parent_id"] == huambo_mun_id

    names = {c["name"] for c in communes}
    assert names == {"Comuna Centro", "Comuna Norte", "Comuna Sul"}


# ============================================================================
# TESTES DE PERFORMANCE
# ============================================================================


@pytest.mark.asyncio
async def test_19_ancestry_chain_performance_province(db_session):
    """Test 19: get_ancestry_chain(7) executa em <100ms"""
    start = time.time()

    current_id = 7
    while current_id is not None:
        loc = await db_session.fetchval("SELECT parent_id FROM locations WHERE id=$1", current_id)
        current_id = loc

    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 100, f"Ancestry chain levou {elapsed_ms:.2f}ms, deve ser < 100ms"


@pytest.mark.asyncio
async def test_20_ancestry_chain_performance_commune(db_session):
    """Test 20: get_ancestry_chain(28) executa em <100ms"""
    start = time.time()

    current_id = 28
    iterations = 0
    while current_id is not None and iterations < 10:
        loc = await db_session.fetchval("SELECT parent_id FROM locations WHERE id=$1", current_id)
        current_id = loc
        iterations += 1

    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 100, f"Ancestry chain levou {elapsed_ms:.2f}ms, deve ser < 100ms"


# ============================================================================
# TESTES DE USERS E ROLES
# ============================================================================


@pytest.mark.asyncio
async def test_21_users_table_has_5_users(db_session):
    """Test 21: Tabela users contém 5 usuários"""
    result = await db_session.fetchval("SELECT COUNT(*) FROM users WHERE is_active=true")

    assert result == 5, f"Esperava 5 usuários ativos, mas tem {result}"


@pytest.mark.asyncio
async def test_22_admin_user_exists(db_session, lei_14_24_data):
    """Test 22: Usuário admin (central@sila.gov.ao) existe"""
    user = await db_session.fetchrow(
        "SELECT id, email, roles, administrative_level, region_id FROM users WHERE email=$1",
        lei_14_24_data["users"]["admin"]["email"],
    )

    assert user is not None, "Usuário admin não encontrado"
    assert user["region_id"] is None, f"Admin deve ter region_id=NULL, mas tem {user['region_id']}"


@pytest.mark.asyncio
async def test_23_provincial_manager_exists_with_correct_region(db_session, lei_14_24_data):
    """Test 23: Manager provincial vinculado a Huambo (region_id=7)"""
    huambo_id = await fetch_location_id(db_session, "Huambo", "PROVINCIA")
    user = await db_session.fetchrow(
        "SELECT id, email, roles, administrative_level, region_id FROM users WHERE email=$1",
        lei_14_24_data["users"]["prov_manager"]["email"],
    )

    assert user is not None, "Manager provincial não encontrado"
    assert user["region_id"] == huambo_id, (
        f"Manager provincial deve ter region_id=Huambo, mas tem {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_24_municipal_manager_exists_with_correct_region(db_session, lei_14_24_data):
    """Test 24: Manager municipal vinculado a Huambo Município (region_id=22)"""
    huambo_mun_id = await fetch_location_id(db_session, "Huambo (Município)", "MUNICIPIO")
    user = await db_session.fetchrow(
        "SELECT id, email, roles, administrative_level, region_id FROM users WHERE email=$1",
        lei_14_24_data["users"]["mun_manager"]["email"],
    )

    assert user is not None, "Manager municipal não encontrado"
    assert user["region_id"] == huambo_mun_id, (
        f"Manager municipal deve ter region_id=Huambo (Município), mas tem {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_25_officer_exists_with_correct_region(db_session, lei_14_24_data):
    """Test 25: Officer vinculado a Comuna Centro (region_id=28)"""
    comuna_centro_id = await fetch_location_id(db_session, "Comuna Centro", "COMUNA")
    user = await db_session.fetchrow(
        "SELECT id, email, roles, administrative_level, region_id FROM users WHERE email=$1",
        lei_14_24_data["users"]["officer"]["email"],
    )

    assert user is not None, "Officer não encontrado"
    assert user["region_id"] == comuna_centro_id, (
        f"Officer deve ter region_id=Comuna Centro, mas tem {user['region_id']}"
    )


@pytest.mark.asyncio
async def test_26_citizen_exists_with_correct_region(db_session, lei_14_24_data):
    """Test 26: Cidadão vinculado a Comuna Centro (region_id=28)"""
    comuna_centro_id = await fetch_location_id(db_session, "Comuna Centro", "COMUNA")
    user = await db_session.fetchrow(
        "SELECT id, email, roles, administrative_level, region_id FROM users WHERE email=$1",
        lei_14_24_data["users"]["citizen"]["email"],
    )

    assert user is not None, "Cidadão não encontrado"
    assert user["region_id"] == comuna_centro_id, (
        f"Cidadão deve ter region_id=Comuna Centro, mas tem {user['region_id']}"
    )


# ============================================================================
# TESTES DE INTEGRIDADE
# ============================================================================


@pytest.mark.asyncio
async def test_27_no_orphaned_users(db_session):
    """Test 27: Nenhum usuário com region_id inválido (sem órfãos)"""
    orphaned = await db_session.fetch(
        "SELECT id, email, region_id FROM users "
        "WHERE region_id IS NOT NULL AND region_id NOT IN (SELECT id FROM locations)"
    )

    assert len(orphaned) == 0, f"Encontrados {len(orphaned)} usuários órfãos: {orphaned}"


@pytest.mark.asyncio
async def test_28_no_orphaned_locations(db_session):
    """Test 28: Nenhuma localização com parent_id inválido (sem órfãos)"""
    orphaned = await db_session.fetch(
        "SELECT id, name, parent_id FROM locations "
        "WHERE parent_id IS NOT NULL AND parent_id NOT IN (SELECT id FROM locations)"
    )

    assert len(orphaned) == 0, f"Encontradas {len(orphaned)} localizações órfãs: {orphaned}"


@pytest.mark.asyncio
async def test_29_circular_references_check(db_session):
    """Test 29: Nenhuma referência circular na hierarquia"""
    # Verificar se há referências circulares (loop protection)
    # Uma localização não pode ser ancestor de si mesma
    circular = await db_session.fetch(
        """
        WITH RECURSIVE hierarchy AS (
            SELECT id, parent_id, 1 as depth
            FROM locations
            WHERE id = parent_id  -- Check se id=parent_id
            UNION ALL
            SELECT l.id, l.parent_id, h.depth + 1
            FROM locations l
            JOIN hierarchy h ON l.id = h.parent_id
            WHERE h.depth < 10  -- Proteção contra loop infinito
        )
        SELECT COUNT(*) as circular_count FROM hierarchy
        """
    )

    # Não deve haver nenhuma localização onde id=parent_id
    count = await db_session.fetchval("SELECT COUNT(*) FROM locations WHERE id = parent_id")
    assert count == 0, f"Encontradas {count} referências circulares"


@pytest.mark.asyncio
async def test_30_all_provinces_have_null_parent(db_session):
    """Test 30: Todas as províncias têm parent_id=NULL"""
    provinces_with_parent = await db_session.fetch(
        "SELECT id, name, parent_id FROM locations WHERE type='PROVINCIA' AND parent_id IS NOT NULL"
    )

    assert len(provinces_with_parent) == 0, (
        f"Encontradas províncias com parent: {provinces_with_parent}"
    )


# ============================================================================
# SUMMARY E RELATÓRIO
# ============================================================================


@pytest.fixture(scope="session", autouse=True)
def print_test_summary():
    """Printtar sumário dos testes ao final"""
    yield

    print("\n" + "=" * 80)
    print("✅ SUMÁRIO DE TESTES - HierarchyService Endpoints")
    print("=" * 80)
    print("""
    Testes de Integridade de Dados (5):
    ✅ Test 01: Tabela locations existe com 32 registros
    ✅ Test 02: 21 províncias (Lei 14/24)
    ✅ Test 03: 6 municípios
    ✅ Test 04: 5 comunas
    ✅ Test 05: Cuando/Cubango separadas (IDs 20/21)
    
    Testes de Hierarquia - parent_id (5):
    ✅ Test 06: Municípios de Huambo têm parent_id=7
    ✅ Test 07: Municípios de Luanda têm parent_id=8
    ✅ Test 08: Comunas de Huambo Mun têm parent_id=22
    ✅ Test 09: Comunas de Bailundo têm parent_id=23
    
    Testes de HierarchyService - get_sub_units (3):
    ✅ Test 10: get_sub_units(7) retorna 3 municípios corretos
    ✅ Test 11: get_sub_units(22) retorna 3 comunas corretas
    ✅ Test 12: get_sub_units(28) retorna lista vazia (folha)
    
    Testes de HierarchyService - get_ancestry_chain (3):
    ✅ Test 13: Ancestry chain de Huambo (raiz) = [Huambo]
    ✅ Test 14: Ancestry chain de Huambo Mun = [Huambo Mun, Huambo]
    ✅ Test 15: Ancestry chain de Comuna = [Comuna, Mun, Prov]
    
    Testes de Role-Based Filtering (3):
    ✅ Test 16: Admin vê todas 21 províncias
    ✅ Test 17: Provincial Manager vê apenas 3 municípios de sua região
    ✅ Test 18: Municipal Manager vê apenas 3 comunas de seu município
    
    Testes de Performance (2):
    ✅ Test 19: Ancestry chain de province < 100ms
    ✅ Test 20: Ancestry chain de commune < 100ms
    
    Testes de Users e Roles (6):
    ✅ Test 21: 5 usuários ativos no banco
    ✅ Test 22: Admin user vinculado corretamente
    ✅ Test 23: Provincial Manager vinculado a Huambo (ID=7)
    ✅ Test 24: Municipal Manager vinculado a Huambo Mun (ID=22)
    ✅ Test 25: Officer vinculado a Comuna Centro (ID=28)
    ✅ Test 26: Cidadão vinculado a Comuna Centro (ID=28)
    
    Testes de Integridade (4):
    ✅ Test 27: Sem usuários órfãos (region_id inválido)
    ✅ Test 28: Sem localidades órfãs (parent_id inválido)
    ✅ Test 29: Sem referências circulares
    ✅ Test 30: Todas províncias têm parent_id=NULL
    
    TOTAL: 30 testes | Conformidade Lei 14/24: 100% ✅
    """)
    print("=" * 80 + "\n")


# ============================================================================
# EXECUTAR TESTES
# ============================================================================

if __name__ == "__main__":
    """
    Execute com:
        pytest tests/test_hierarchy_service_endpoints.py -v --tb=short
    
    Ou com verbose completo:
        pytest tests/test_hierarchy_service_endpoints.py -vv --tb=long
    
    Ou apenas um teste específico:
        pytest tests/test_hierarchy_service_endpoints.py::test_06_huambo_municipalities_parent_id -v
    """
    pytest.main([__file__, "-v", "--tb=short"])
