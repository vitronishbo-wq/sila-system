# 🚀 DIA 3 - INFRASTRUCTURE LAYER (ROADMAP EXATO)

**Ordem disciplinada. Sem desvios. Sem gambling.**

---

## PASSO 1: SQLAlchemy Models

### Localização
```
apps/backend/modules/taxpayer/infrastructure/db/models/
├── __init__.py
├── taxpayer.py
├── tax_declaration.py
├── tax_debt.py
├── tax_payment.py
└── tax_certificate.py
```

### Padrão

```python
# infrastructure/db/models/taxpayer.py

from sqlalchemy import Column, String, DateTime, Enum, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from core.db.base_class import Base

class TaxpayerModel(Base):
    __tablename__ = "taxpayer_taxpayers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nif = Column(String(14), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    tax_regime = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="DRAFT")
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    registered_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
```

### Checklist
- [ ] Models seguem naming `taxpayer_*` (módulo prefix)
- [ ] UUIDs como primary keys
- [ ] Timestamps (created_at, updated_at)
- [ ] Índices em campos de busca (nif, email, phone)
- [ ] Enums mapeados
- [ ] ForeignKeys corretos
- [ ] Relationships bidirecionais com `back_populates`

---

## PASSO 2: Repository Implementation

### Localização
```
apps/backend/modules/taxpayer/infrastructure/repositories/
├── __init__.py
├── base_repository.py
├── taxpayer_repository.py
├── tax_declaration_repository.py
├── tax_debt_repository.py
├── tax_payment_repository.py
└── tax_certificate_repository.py
```

### Padrão

```python
# infrastructure/repositories/taxpayer_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Tuple
from uuid import UUID

from application.ports import TaxpayerRepositoryPort
from domain.entities.taxpayer import Taxpayer
from infrastructure.db.models.taxpayer import TaxpayerModel

class SqlAlchemyTaxpayerRepository(TaxpayerRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, taxpayer: Taxpayer) -> Taxpayer:
        """Save or update taxpayer"""
        # Convert domain entity to model
        model = self._to_model(taxpayer)
        
        # Check if exists
        existing = await self.session.execute(
            select(TaxpayerModel).where(TaxpayerModel.id == taxpayer.id)
        )
        existing = existing.scalar_one_or_none()
        
        if existing:
            # Update
            existing.name = model.name
            existing.email = model.email
            # ... outros campos
            self.session.add(existing)
        else:
            # Insert
            self.session.add(model)
        
        # NÃO fazer commit aqui! UoW controla
        return taxpayer
    
    async def find_by_id(self, taxpayer_id: UUID) -> Optional[Taxpayer]:
        """Find by ID"""
        result = await self.session.execute(
            select(TaxpayerModel).where(TaxpayerModel.id == taxpayer_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    def _to_model(self, taxpayer: Taxpayer) -> TaxpayerModel:
        """Convert domain to model"""
        return TaxpayerModel(
            id=taxpayer.id,
            nif=taxpayer.nif,
            name=taxpayer.name,
            # ...
        )
    
    def _to_domain(self, model: TaxpayerModel) -> Taxpayer:
        """Convert model to domain"""
        return Taxpayer(
            id=model.id,
            nif=model.nif,
            name=model.name,
            # ...
        )
```

### Regras Críticas
- ✅ Nunca fazer `commit()` no repository
- ✅ Sempre retornar domain entity, não model
- ✅ Use `select()` syntax (SQLAlchemy 2.0)
- ✅ Índices em campos críticos
- ✅ Paginação com `skip` e `limit`

---

## PASSO 3: UnitOfWork Implementation

### Localização
```
apps/backend/modules/taxpayer/infrastructure/db/
├── unit_of_work.py
```

### Padrão

```python
# infrastructure/db/unit_of_work.py

from sqlalchemy.ext.asyncio import AsyncSession
from application.ports import UnitOfWorkPort
from infrastructure.repositories import (
    SqlAlchemyTaxpayerRepository,
    SqlAlchemyDeclarationRepository,
    SqlAlchemyDebtRepository,
    SqlAlchemyPaymentRepository,
    SqlAlchemyCertificateRepository
)

class SqlAlchemyUnitOfWork(UnitOfWorkPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self._taxpayers = None
        self._declarations = None
        self._debts = None
        self._payments = None
        self._certificates = None
    
    @property
    def taxpayers(self):
        if not self._taxpayers:
            self._taxpayers = SqlAlchemyTaxpayerRepository(self.session)
        return self._taxpayers
    
    @property
    def declarations(self):
        if not self._declarations:
            self._declarations = SqlAlchemyDeclarationRepository(self.session)
        return self._declarations
    
    # ... outras repositories
    
    async def begin(self) -> None:
        """Start transaction"""
        # SQLAlchemy AsyncSession starts automatically
        pass
    
    async def commit(self) -> None:
        """Commit transaction"""
        await self.session.commit()
    
    async def rollback(self) -> None:
        """Rollback transaction"""
        await self.session.rollback()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        # Não commita automaticamente - deixa ao método chamar
```

### Regras Críticas
- ✅ Lazy-load repositories (só cria quando precisa)
- ✅ Context manager funciona com `async with`
- ✅ Auto-rollback on exception
- ✅ Explicit `await self.uow.commit()`

---

## PASSO 4: EventBus Simple (InMemory)

### Localização
```
apps/backend/modules/taxpayer/infrastructure/event_bus/
├── __init__.py
└── in_memory_event_bus.py
```

### Padrão

```python
# infrastructure/event_bus/in_memory_event_bus.py

import asyncio
from typing import Callable, List, Dict
from application.ports import EventBusPort, DomainEvent
import logging

class InMemoryEventBus(EventBusPort):
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger(__name__)
    
    async def publish(self, event: DomainEvent) -> None:
        """Publish event to subscribers"""
        event_type = event.event_type
        
        if event_type not in self.subscribers:
            self.logger.warning(f"No subscribers for {event_type}")
            return
        
        # Execute all handlers (não falhar se um cair)
        tasks = []
        for handler in self.subscribers[event_type]:
            task = asyncio.create_task(self._safe_handle(handler, event))
            tasks.append(task)
        
        # Wait all (mas não falhar)
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def publish_all(self, events: List[DomainEvent]) -> None:
        """Publish multiple events"""
        for event in events:
            await self.publish(event)
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to event"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from event"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(handler)
    
    async def _safe_handle(self, handler, event):
        """Execute handler with error handling"""
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
        except Exception as e:
            self.logger.exception(f"Handler failed for {event.event_type}: {e}")
```

### Regras Críticas
- ✅ Não falhar se subscriber cair
- ✅ Log de erros
- ✅ Asyncio-safe (gather, tasks)
- ✅ RabbitMQ depois (não agora)

---

## PASSO 5: Dependency Injection Container

### Localização
```
apps/backend/modules/taxpayer/infrastructure/di/
├── __init__.py
└── container.py
```

### Padrão

```python
# infrastructure/di/container.py

from sqlalchemy.ext.asyncio import AsyncSession
from application import TaxpayerApplicationFacade
from application.services import *
from application.ports import *
from infrastructure.repositories import *
from infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.event_bus import InMemoryEventBus

class TaxpayerContainer:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def get_unit_of_work(self) -> UnitOfWorkPort:
        return SqlAlchemyUnitOfWork(self.session)
    
    def get_event_bus(self) -> EventBusPort:
        return InMemoryEventBus()
    
    def get_taxpayer_repository(self) -> TaxpayerRepositoryPort:
        return SqlAlchemyTaxpayerRepository(self.session)
    
    # ... outras repositories
    
    def get_taxpayer_service(self) -> TaxpayerService:
        return TaxpayerService(
            taxpayer_repo=self.get_taxpayer_repository(),
            agt_client=self.get_agt_integration(),  # Mock por enquanto
            notification=self.get_notification(),   # Mock por enquanto
            audit=self.get_audit(),                 # Mock por enquanto
            cache=self.get_cache()                  # Mock por enquanto
        )
    
    # ... outros services
    
    def get_facade(self) -> TaxpayerApplicationFacade:
        return TaxpayerApplicationFacade(
            taxpayer_service=self.get_taxpayer_service(),
            declaration_service=self.get_tax_declaration_service(),
            debt_service=self.get_tax_debt_service(),
            certificate_service=self.get_tax_certificate_service(),
            agt_sync_service=self.get_agt_sync_service(),
            payment_service=self.get_tax_payment_service(),
            unit_of_work=self.get_unit_of_work(),
            event_bus=self.get_event_bus()
        )
```

### Uso no FastAPI

```python
# main.py
from fastapi import Depends
from infrastructure.di import TaxpayerContainer

async def get_container(session: AsyncSession = Depends(get_session)) -> TaxpayerContainer:
    return TaxpayerContainer(session)

async def get_facade(container: TaxpayerContainer = Depends(get_container)):
    return container.get_facade()
```

---

## PASSO 6: FastAPI Endpoints

### Localização
```
apps/backend/modules/taxpayer/api/
├── __init__.py
└── taxpayers.py
```

### Padrão

```python
# api/taxpayers.py

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from application import TaxpayerApplicationFacade, RegisterTaxpayerCommand

router = APIRouter(prefix="/taxpayers", tags=["taxpayers"])

async def get_facade() -> TaxpayerApplicationFacade:
    # From DI container
    pass

@router.post("/register", status_code=201)
async def register_taxpayer(
    cmd: RegisterTaxpayerCommand,
    facade: TaxpayerApplicationFacade = Depends(get_facade)
):
    """Register new taxpayer"""
    try:
        taxpayer = await facade.register_taxpayer(
            nif=cmd.nif,
            name=cmd.name,
            email=cmd.email,
            phone=cmd.phone,
            address=cmd.address,
            tax_regime=cmd.tax_regime,
            registered_by=cmd.registered_by,
            ip_address=cmd.ip_address
        )
        return {
            "id": str(taxpayer.id),
            "nif": taxpayer.nif,
            "name": taxpayer.name,
            "status": "created"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")

@router.get("/{taxpayer_id}")
async def get_taxpayer(
    taxpayer_id: UUID,
    facade: TaxpayerApplicationFacade = Depends(get_facade)
):
    """Get taxpayer"""
    taxpayer = await facade.get_taxpayer(taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": str(taxpayer.id),
        "nif": taxpayer.nif,
        "name": taxpayer.name
    }
```

### Regras Críticas
- ✅ Use Facade (1 entrada)
- ✅ Use Commands para requests
- ✅ Maper exceptions para HTTP status
- ✅ Sempre retornar DTOs (não domain entities)

---

## PASSO 7: Alembic Migrations

### Inicializar

```bash
cd apps/backend
alembic init --template async alembic
```

### Configuração

```python
# alembic/env.py
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import all models
from core.db.base_class import Base
from modules.taxpayer.infrastructure.db.models import *

target_metadata = Base.metadata

async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    connectable = create_async_engine(
        configuration["sqlalchemy.url"],
        poolclass=pool.NullPool,
    )
    
    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)
```

### Criar primeira migration

```bash
alembic revision --autogenerate -m "Create taxpayer tables"
```

### Revisão

```python
# alembic/versions/xxx_create_taxpayer_tables.py

def upgrade() -> None:
    op.create_table(
        'taxpayer_taxpayers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('nif', sa.String(14), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        # ...
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nif'),
        schema='taxpayer'
    )

def downgrade() -> None:
    op.drop_table('taxpayer_taxpayers', schema='taxpayer')
```

---

## 📋 CHECKLIST DIA 3

### PASSO 1: SQLAlchemy Models
- [ ] 5 models criados
- [ ] Timestamps em todos
- [ ] Índices em campos críticos
- [ ] ForeignKeys corretos
- [ ] Relationships com back_populates

### PASSO 2: Repositories
- [ ] 5 repositories implementados
- [ ] Herdam de ports
- [ ] Conversão domain ↔ model
- [ ] Sem commit() dentro deles
- [ ] Paginação implementada

### PASSO 3: UnitOfWork
- [ ] Lazy-load repositories
- [ ] Context manager funciona
- [ ] Auto-rollback on exception
- [ ] Explicit commit

### PASSO 4: EventBus
- [ ] InMemory implementation
- [ ] Publish/Subscribe funções
- [ ] Error handling (não falha)
- [ ] Logging de eventos

### PASSO 5: DI Container
- [ ] Todos services injetados
- [ ] Facade disponível
- [ ] Mocks para AGT, Notification, etc

### PASSO 6: Endpoints
- [ ] POST /taxpayers/register
- [ ] GET /taxpayers/{id}
- [ ] Usa Facade
- [ ] Error handling

### PASSO 7: Migrations
- [ ] Alembic init
- [ ] Primeira migration
- [ ] Schema per module (taxpayer.*)

---

## 🎯 RESULTADO ESPERADO

```
✅ Full integration test funcionando:
  1. POST /taxpayers/register
  2. Service executa dentro de UoW
  3. Repository salva no banco
  4. Commit executa
  5. Events publicados
  6. InMemory subscribers reagem
  7. GET /taxpayers/{id} retorna dado
```

---

## ⚠️ ARMADILHAS COMUNS

❌ **NÃO FAZER**:

1. Commit dentro do repository
2. Publicar eventos antes do commit
3. Services sem DI
4. Models sem índices
5. Endpoints sem DTOs
6. Sem error handling

✅ **FAZER**:

1. UoW controla commit
2. Publicar após commit (fora transação)
3. Tudo injetado
4. Índices em findBy
5. Sempre retornar DTOs
6. Try/except com HTTP status

---

## 🚀 VELOCIDADE

Cada passo deve levar ~2 horas.

Total DIA 3: ~12-14 horas (1-2 dias).

Não tente paralelizar. Ordem importa.
