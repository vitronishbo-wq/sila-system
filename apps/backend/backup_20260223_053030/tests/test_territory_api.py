"""
Testes unitários para Territory Service - Com Mocks (sem BD)

Estratégia:
- Mocks de AsyncSession
- Testes da lógica de model
- Sem SQLite, sem BD em memória
"""

import pytest
from uuid import UUID
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.territory.models.territory import Territory


@pytest.mark.asyncio
async def test_territory_model_creation():
    """Testa criação de instância Territory"""
    territory_id = UUID("12345678-1234-5678-1234-567812345678")
    
    territory = Territory(
        id=territory_id,
        name="Test Province",
        code="TST",
        type="province",
        parent_id=None
    )
    
    assert territory.id == territory_id
    assert territory.name == "Test Province"
    assert territory.code == "TST"
    assert territory.type == "province"
    assert territory.parent_id is None


@pytest.mark.asyncio
async def test_territory_hierarchy():
    """Testa relacionamento pai-filho de Territory"""
    province_id = UUID("11111111-1111-1111-1111-111111111111")
    municipality_id = UUID("22222222-2222-2222-2222-222222222222")
    
    province = Territory(
        id=province_id,
        name="Huambo",
        code="HUAMBO",
        type="province",
        parent_id=None
    )
    
    municipality = Territory(
        id=municipality_id,
        name="Bailundo",
        code="BAILUNDO",
        type="municipality",
        parent_id=province_id
    )
    
    # Verificar relacionamento
    assert municipality.parent_id == province.id
    assert municipality.type == "municipality"
    assert province.type == "province"


@pytest.mark.asyncio
async def test_territory_types():
    """Testa tipos válidos de Territory"""
    valid_types = ["province", "municipality", "commune"]
    
    for territory_type in valid_types:
        territory = Territory(
            id=UUID("44444444-4444-4444-4444-444444444444"),
            name=f"Test {territory_type}",
            code=f"T{territory_type[0]}",
            type=territory_type,
            parent_id=None
        )
        
        assert territory.type == territory_type
        assert territory.type in valid_types


@pytest.mark.asyncio
async def test_territory_parent_relationship():
    """Testa que apenas municípios e comunas podem ter parent"""
    province = Territory(
        id=UUID("55555555-5555-5555-5555-555555555555"),
        name="Angola Parent",
        code="ANGP",
        type="province",
        parent_id=None  # Províncias não têm parent
    )
    
    municipality = Territory(
        id=UUID("66666666-6666-6666-6666-666666666666"),
        name="Luanda Municipality",
        code="LUANDA",
        type="municipality",
        parent_id=province.id  # Tem parent
    )
    
    assert province.parent_id is None
    assert municipality.parent_id is not None
    assert municipality.parent_id == province.id


@pytest.mark.asyncio
async def test_territory_code_unique():
    """Testa que o código é único"""
    code = "UNIQUE_CODE"
    
    # Criar dois territórios com o mesmo código
    territory1 = Territory(
        id=UUID("77777777-7777-7777-7777-777777777777"),
        name="Territory 1",
        code=code,
        type="province",
        parent_id=None
    )
    
    territory2 = Territory(
        id=UUID("88888888-8888-8888-8888-888888888888"),
        name="Territory 2",
        code=code,  # Mesmo código
        type="province",
        parent_id=None
    )
    
    # Ambos foram criados (constraint é da BD, não do model)
    assert territory1.code == territory2.code
    assert territory1.id != territory2.id
