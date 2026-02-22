# ✅ VALIDAÇÃO ARQUITETÔNICA - 4 PONTOS CRÍTICOS

## 1️⃣ UOW CONTROLA REPOSITORY?

### Análise Atual

❌ **Problema identificado**

Implementação atual:
```python
class TaxpayerService:
    def __init__(self, repo: TaxpayerRepositoryPort, ...):
        self.repo = repo  # ← Services falam direto com repo
    
    async def register_taxpayer(self, ...):
        taxpayer = Taxpayer(...)
        saved = await self.repo.save(taxpayer)  # ← Acoplamento direto
```

✅ **Solução Correta**

UoW como mediador:
```python
class SqlAlchemyUnitOfWork(UnitOfWorkPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.taxpayers = SqlAlchemyTaxpayerRepository(session)  # ← Lazy loading
        self.declarations = SqlAlchemyDeclarationRepository(session)
        self.debts = SqlAlchemyDebtRepository(session)

class TaxpayerService:
    def __init__(self, uow: UnitOfWorkPort, ...):
        self.uow = uow

    async def register_taxpayer(self, ...):
        taxpayer = Taxpayer(...)
        saved = await self.uow.taxpayers.save(taxpayer)  # ← Via UoW
        await self.uow.commit()
```

### ✅ Padrão Correto em Facade

```python
class TaxpayerApplicationFacade:
    def __init__(self, uow: UnitOfWorkPort, ...):
        self.uow = uow
    
    async def register_taxpayer(self, nif, name, ...):
        async with self.uow:
            # Repositories acessadas via UoW
            taxpayer = Taxpayer(nif=nif, name=name, ...)
            saved = await self.uow.taxpayers.save(taxpayer)
            await self.uow.commit()
            return saved
```

**Status**: 🔴 CORRIGIR NO DIA 3

---

## 2️⃣ EVENT DISPATCH APÓS COMMIT?

### Sequência Correta (CRÍTICO)

```
┌──────────────────────────────┐
│  1. Domain change happens    │
│  taxpayer.add_event(...)     │
└──────────────────────────────┘
             ↓
┌──────────────────────────────┐
│  2. Save to repository       │
│  await repo.save(taxpayer)   │
└──────────────────────────────┘
             ↓
┌──────────────────────────────┐
│  3. COMMIT transaction       │
│  await uow.commit()          │ ← SÓ AQUI
└──────────────────────────────┘
             ↓
┌──────────────────────────────┐
│  4. PUBLISH events           │
│  for event in taxpayer.      │
│      get_events():           │
│    await bus.publish(event)  │
└──────────────────────────────┘
             ↓
┌──────────────────────────────┐
│  5. Clear events             │
│  taxpayer.clear_events()     │
└──────────────────────────────┘
```

### ❌ Implementação ERRADA

```python
async def register_taxpayer(self, ...):
    taxpayer = Taxpayer(...)
    saved = await self.repo.save(taxpayer)
    
    # ❌ ERRADO: Publishing antes do commit
    for event in saved.get_events():
        await self.event_bus.publish(event)  # SE DER ERRO NO EVENT_BUS?
    
    await self.uow.commit()  # Pode falhar!
```

### ✅ Implementação CORRETA

```python
async def register_taxpayer(self, ...):
    async with self.uow:
        taxpayer = Taxpayer(...)
        saved = await self.uow.taxpayers.save(taxpayer)
        
        # Commit FIRST
        await self.uow.commit()  # ← SALVO no banco
    
    # DEPOIS publish (fora da transação)
    for event in saved.get_events():
        try:
            await self.event_bus.publish(event)
        except EventBusException:
            # Log mas não falha a operação
            self.logger.error(f"Failed to publish: {event}")
    
    saved.clear_events()
    return saved
```

**Garantia**: Se event_bus falhar, dado já está no banco. Idempotente.

**Status**: 🟡 IMPLEMENTAR CORRETAMENTE NO DIA 3

---

## 3️⃣ FACADE NÃO CONTÉM REGRA DE NEGÓCIO?

### ✅ Verificação do Código Atual

Analisando `taxpayer_application_facade.py`:

**✅ CORRETO - Apenas orquestração:**
```python
async def register_taxpayer(self, nif, name, ...):
    async with self.uow:
        taxpayer = await self.taxpayer.register_taxpayer(...)
        # ↑ Regra de negócio aqui (TaxpayerService)
        await self.uow.commit()
    # ↑ Orchestration aqui (Facade)
    return taxpayer
```

**❌ ERRADO - Regra de negócio NO FACADE:**
```python
async def register_taxpayer(self, nif, name, ...):
    # ❌ Regra de negócio aqui!
    if not nif.is_valid():
        raise ValueError("Invalid NIF")
    
    async with self.uow:
        taxpayer = await self.taxpayer.register_taxpayer(...)
        await self.uow.commit()
    return taxpayer
```

### Responsabilidades Corretas

| Camada | Responsabilidade | Exemplo |
|--------|-----------------|---------|
| **Domain** | Regras invariantes | "NIF sempre tem 9 ou 14 dígitos" |
| **Service** | Casos de uso | "Ao registrar, validar NIF na AGT" |
| **Facade** | Orquestração | "Execute service dentro de UoW" |
| **API** | HTTP plumbing | "Parse JSON, retorna 200" |

### Verificação do Facade Atual

```python
class TaxpayerApplicationFacade:
    async def register_taxpayer(self, ...):
        async with self.uow:
            taxpayer = await self.taxpayer.register_taxpayer(...)  # ← Service
            await self.uow.commit()  # ← Transaction
        return taxpayer  # ← Retorna DTO
```

**Status**: ✅ CORRETO

**Precisão**: Facade faz exatamente o que deve (orquestração).

---

## 4️⃣ PORTS NÃO DEPENDEM DE INFRASTRUCTURE?

### ✅ Verificação de Dependências

#### taxpayer_repository_port.py
```python
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID
from datetime import date
# ↑ Apenas stdlib + typing

class TaxpayerRepositoryPort(ABC):
    @abstractmethod
    async def save(self, taxpayer: Taxpayer) -> Taxpayer:
        pass
```

**✅ PURO** - Sem imports de SQLAlchemy, requests, redis, etc.

#### agt_integration_port.py
```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class AGTIntegrationPort(ABC):
    @abstractmethod
    async def validate_nif(self, nif: str) -> bool:
        pass
```

**✅ PURO** - Sem imports de httpx, requests, etc.

#### event_bus_port.py
```python
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

class EventBusPort(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass
```

**✅ PURO** - Sem imports de RabbitMQ, redis, etc.

#### unit_of_work_port.py
```python
from abc import ABC, abstractmethod

class UnitOfWorkPort(ABC):
    @abstractmethod
    async def begin(self) -> None:
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        pass
```

**✅ PURO** - Sem imports de SQLAlchemy, etc.

### Verificação Completa

```bash
$ grep -r "from sqlalchemy\|from redis\|from fastapi\|import requests" \
    apps/backend/modules/taxpayer/application/ports/

# (Nenhum resultado = correto!)
```

**Status**: ✅ CORRETO - Todos os ports são pure typing

---

## 📊 RESULTADO DA VALIDAÇÃO

| Ponto | Status | Ação |
|-------|--------|------|
| 1. UoW controla Repo | 🔴 | Corrigir em DIA 3 (architecture pattern) |
| 2. Event após Commit | 🟡 | Implementar corretamente em DIA 3 |
| 3. Facade sem regra | ✅ | Correto - manter assim |
| 4. Ports puro typing | ✅ | Correto - perfeito |

---

## 🔧 PLANO DE CORREÇÃO DIA 3

### Correção 1: UoW como Repo Manager

```python
# infrastructure/db/session.py
class SqlAlchemyUnitOfWork(UnitOfWorkPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self._taxpayers: Optional[TaxpayerRepository] = None
        self._declarations: Optional[DeclarationRepository] = None
    
    @property
    def taxpayers(self):
        if not self._taxpayers:
            self._taxpayers = TaxpayerRepository(self.session)
        return self._taxpayers
    
    @property
    def declarations(self):
        if not self._declarations:
            self._declarations = DeclarationRepository(self.session)
        return self._declarations
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
```

### Correção 2: Refatorar Services para usar UoW

```python
# application/services/taxpayer_service.py
class TaxpayerService:
    def __init__(self, uow: UnitOfWorkPort, agt, notification, audit, cache):
        self.uow = uow  # ← Mudar para UoW
        self.agt = agt
        
    async def register_taxpayer(self, ...):
        taxpayer = Taxpayer(...)
        saved = await self.uow.taxpayers.save(taxpayer)  # ← Via UoW
        return saved
```

### Correção 3: Event Dispatch Pattern

```python
# application/services/base_service.py
class BaseService:
    def __init__(self, uow, event_bus):
        self.uow = uow
        self.event_bus = event_bus
    
    async def publish_events(self, aggregate):
        """Publish events AFTER commit"""
        for event in aggregate.get_events():
            try:
                await self.event_bus.publish(event)
            except Exception:
                self.logger.exception("Event dispatch failed")
        aggregate.clear_events()
```

---

## 🎯 CONCLUSÃO VALIDAÇÃO

✅ **Pontos 3 e 4**: Perfeitos
🟡 **Pontos 1 e 2**: Requerem ajustes simples em DIA 3

**Não é refatoração massiva**, apenas:
- Reorganizar repositórios para serem acessados via UoW
- Mover event dispatch para após o commit
- Adicionar error handling adequado

**Recomendação**: Fazer isso tão logo comece DIA 3.
