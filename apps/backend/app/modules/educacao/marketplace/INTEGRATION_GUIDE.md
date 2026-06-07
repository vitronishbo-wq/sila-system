# Guia de Integração do Marketplace ao Módulo Educação

## 1. Integração no Router Principal do Módulo

### Arquivo: `educacao/api/router.py`

Adicionar import e montagem do marketplace router:

```python
from fastapi import APIRouter
from ..marketplace.router import router as marketplace_router

router = APIRouter(prefix="/v1/educacao", tags=["educacao"])

# Incluir marketplace
router.include_router(marketplace_router)

# Outros routers existentes...
```

## 2. Registrar no Módulo Registry

### Arquivo: `app/core/module_registry.py`

Verificar e atualizar o registro do marketplace:

```python
MODULES = {
    # ...
    "educacao": {
        # ...
        "submodules": [
            # ...
            "marketplace",  # Novo submodulo
        ]
    }
}
```

## 3. Implementação da Persistência

### Criar migrations Alembic

```bash
cd apps/backend
alembic revision --autogenerate -m "Add marketplace tables: opportunities, bookings, admissions, transfers"
```

### Criar modelos SQLAlchemy

Arquivos a criar em `educacao/marketplace/{subdomain}/infrastructure/orm/`:

```
discovery/infrastructure/orm/opportunity_model.py
booking/infrastructure/orm/booking_model.py
admissions/infrastructure/orm/admission_model.py
transfers/infrastructure/orm/transfer_model.py
```

## 4. Implementação dos Adapters

### Discovery - Adapters

```python
# discovery/infrastructure/adapters.py - COMPLETAR

class OpportunityRepository(OpportunityRepositoryPort):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def find_all(self, filters: Optional[dict] = None):
        query = select(OpportunityModel)
        if filters:
            if level := filters.get("level"):
                query = query.where(OpportunityModel.level == level)
            if institution_id := filters.get("institution_id"):
                query = query.where(OpportunityModel.institution_id == institution_id)
        
        result = await self.db.execute(query)
        return result.scalars().all()
```

## 5. Configuração de Dependências

### Arquivo: `educacao/marketplace/{subdomain}/api/deps.py`

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.core.db import get_db

from ..application.services import DiscoveryService
from ..infrastructure.adapters import (
    OpportunityRepository,
    InstitutionRepository,
    ProgramRepository,
)


async def get_discovery_service(
    db: AsyncSession = Depends(get_db),
) -> DiscoveryService:
    return DiscoveryService(
        opportunity_repo=OpportunityRepository(db),
        institution_repo=InstitutionRepository(db),
        program_repo=ProgramRepository(db),
    )
```

## 6. Schemas Pydantic

### Arquivo: `educacao/marketplace/{subdomain}/api/schemas.py`

Criar schemas de request/response para cada endpoint:

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OpportunitySchema(BaseModel):
    id: str
    institution_id: str
    program_id: str
    level: str
    vacancies_total: int
    vacancies_available: int
    price: Optional[float] = None
    
    class Config:
        from_attributes = True


class OpportunityCreateSchema(BaseModel):
    institution_id: str
    program_id: str
    level: str
    vacancies_total: int
    price: Optional[float] = None
```

## 7. Integração com Celery (Processamento Assíncrono)

### Arquivo: `educacao/marketplace/common/tasks.py`

```python
from celery import shared_task
from ..discovery.application.services import DiscoveryService


@shared_task
def update_opportunity_availability():
    """Tarefa assíncrona para atualizar disponibilidade de vagas"""
    # Implementar lógica de atualização
    pass


@shared_task
def process_matching_engine(citizen_id: str):
    """Tarefa assíncrona para rodar matching engine"""
    # Implementar lógica de matching
    pass
```

## 8. Eventos de Domínio

### Arquivo: `educacao/marketplace/common/events.py`

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VacancyReservedEvent:
    booking_id: str
    citizen_id: str
    opportunity_id: str
    created_at: datetime


@dataclass
class AdmissionApprovedEvent:
    admission_id: str
    citizen_id: str
    opportunity_id: str
    approved_at: datetime


@dataclass
class TransferApprovedEvent:
    transfer_id: str
    citizen_id: str
    source_institution: str
    destination_institution: str
    approved_at: datetime
```

## 9. Testes Unitários

### Arquivo: `educacao/marketplace/discovery/tests/test_discovery_service.py`

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from ..application.services import DiscoveryService


@pytest.fixture
async def discovery_service():
    opportunity_repo = AsyncMock()
    institution_repo = AsyncMock()
    program_repo = AsyncMock()
    
    return DiscoveryService(
        opportunity_repo=opportunity_repo,
        institution_repo=institution_repo,
        program_repo=program_repo,
    )


@pytest.mark.asyncio
async def test_list_opportunities(discovery_service):
    # Arrange
    expected_opportunities = [
        {"id": "opp_1", "level": "superior", "vacancies": 10}
    ]
    discovery_service.opportunity_repo.find_all.return_value = expected_opportunities
    
    # Act
    result = await discovery_service.list_opportunities()
    
    # Assert
    assert len(result) == 1
    assert result[0]["level"] == "superior"
```

## 10. Configuração de Cache Redis

### Arquivo: `educacao/marketplace/common/cache.py`

```python
from redis import Redis
from typing import Any, Optional


class MarketplaceCache:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    async def get_ranking(self, key: str, ttl: int = 3600) -> Optional[Any]:
        return self.redis.get(f"marketplace:ranking:{key}")
    
    async def set_ranking(self, key: str, value: Any, ttl: int = 3600) -> None:
        self.redis.setex(f"marketplace:ranking:{key}", ttl, value)
```

## 11. Integração com X-Road

### Arquivo: `educacao/marketplace/common/xroad_client.py`

```python
from typing import Optional, Any
from httpx import AsyncClient


class XRoadClient:
    def __init__(self, client: AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url
    
    async def get_citizen_profile(self, citizen_id: str) -> Optional[dict]:
        """Obter perfil do cidadão via X-Road"""
        response = await self.client.get(
            f"{self.base_url}/citizens/{citizen_id}",
            headers={"X-Road-Client": "marketplace"}
        )
        return response.json() if response.status_code == 200 else None
    
    async def validate_eligibility(self, citizen_id: str, rules: dict) -> bool:
        """Validar elegibilidade via X-Road"""
        response = await self.client.post(
            f"{self.base_url}/validate-eligibility",
            json={"citizen_id": citizen_id, "rules": rules}
        )
        return response.json().get("eligible", False)
```

## 12. Próximas Ações

1. **Implementar modelos SQLAlchemy** para persistência
2. **Criar migrations Alembic**
3. **Implementar repositories concretos**
4. **Adicionar testes unitários e integração**
5. **Configurar Celery tasks**
6. **Implementar X-Road adapters**
7. **Criar documentação OpenAPI**
8. **Fazer deploy em dev/staging**

## 13. Verificação de Integridade

```bash
# Validar estrutura
find apps/backend/app/modules/educacao/marketplace -type f -name "*.py" | wc -l

# Validar imports
python3 -c "from apps.backend.app.modules.educacao.marketplace.config import MARKETPLACE_CONFIG; print(MARKETPLACE_CONFIG)"

# Rodar linters
flake8 apps/backend/app/modules/educacao/marketplace/
black --check apps/backend/app/modules/educacao/marketplace/
mypy apps/backend/app/modules/educacao/marketplace/

# Rodar testes
pytest apps/backend/app/modules/educacao/marketplace/ -v
```

---

**Status**: Estrutura pronta para implementação  
**Próximo Passo**: Começar com Discovery (Batch 1 do MVP)
