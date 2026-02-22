# 🏗️ DESIGN NOTES - ARCHITECTURE DECISIONS

## 1. FACADE PATTERN (Service Aggregator)

### Problema
- 6 services independentes = risco de service explosion
- API se acoplaria a múltiplos services
- Difícil de manter coordenação entre services
- Sem ponto único de entrada

### Solução: TaxpayerApplicationFacade
```python
facade = TaxpayerApplicationFacade(
    taxpayer_service,
    declaration_service,
    debt_service,
    certificate_service,
    agt_sync_service,
    payment_service,
    unit_of_work,
    event_bus
)

# API usa APENAS facade
taxpayer = await facade.register_taxpayer(...)
```

### Benefícios
✅ Única entrada para API (evita 6 imports)
✅ Coordenação centralizada entre services
✅ Escalável: novos services = novo método no facade
✅ Fácil para DI (dependency injection)
✅ Testabilidade mantida

---

## 2. UNIT OF WORK PATTERN (Transaction Boundary)

### Problema
- Sem transaction management explícito
- Risco de saves parciais
- Dados inconsistentes em cascata
- Sem rollback automático

### Solução: UnitOfWorkPort
```python
# Context manager automático
async with self.uow:
    taxpayer = await self.taxpayer.register_taxpayer(...)
    await self.uow.commit()  # Ou auto-rollback on exception
```

### Garantias
✅ ACID transactions
✅ Auto-rollback on exception
✅ Múltiplos saves = única transação
✅ Pronto para SQLAlchemy AsyncSession

---

## 3. EVENT BUS / EVENT DISPATCHER

### Problema
- Domain events criados em aggregates
- Mas não publicados em lugar nenhum
- Events presos no aggregate = inúteis
- Sem subscribers para reagir

### Solução: EventBusPort + Dispatcher
```python
# Em domain aggregate
taxpayer.add_event(TaxpayerRegistered(...))

# Em application service
for event in taxpayer.get_events():
    await event_bus.publish(event)
    taxpayer.clear_events()
```

### Fluxo Completo
Domain → Service → EventBus → Subscribers (Infrastructure)
- Subscribers podem enviar email, SMS, notifs, logs
- Sem acoplamento de domínio com infraestrutura

---

## 4. PORTS ESTRUTURA FINAL

```
ports/
├── taxpayer_repository_port.py    → Persistência
├── agt_integration_port.py        → Externa (AGT)
├── notification_port.py           → Notificações
├── audit_port.py                  → Auditoria/Logs
├── cache_port.py                  → Cache distribuído
├── event_bus_port.py              → Event dispatching
├── unit_of_work_port.py           → Transaction management
└── __init__.py                    → Exports
```

---

## 5. ARQUITETURA COMPLETA AGORA

```
DOMAIN LAYER (95% complete)
├── Entities (Aggregate Root + children)
├── Value Objects (5 classes)
├── Enums (5 types)
└── Domain Events (4 types)

APPLICATION LAYER (95% complete)
├── Facade (coordenação uniificada)
├── Services (6 classes)
├── Ports (7 interfaces)
├── Commands (CQRS write)
└── Queries (CQRS read)

INFRASTRUCTURE LAYER (0% - DIA 3)
├── Repositories (SQLAlchemy)
├── AGT Client (HTTP/async)
├── Event Bus (async pub/sub)
├── Cache (Redis)
├── Unit of Work (session management)
├── Notifications (Email/SMS)
└── Audit (PostgreSQL)

API LAYER (0% - DIA 3)
└── FastAPI endpoints
    └── /taxpayers
    └── /taxpayers/{id}/declarations
    └── /taxpayers/{id}/debts
    └── /taxpayers/{id}/certificates
```

---

## 6. CRITICALIDADE PARA DIA 3

| Item | Crítico | Razão |
|------|---------|-------|
| UnitOfWork | 🔴 CRÍTICO | Sem isso = dados inconsistentes |
| EventBus | 🟠 ALTO | Eventos precisam ser propagados |
| Repositories | 🔴 CRÍTICO | Sem isso = Application inútil |
| Cache | 🟡 MÉDIO | Otimização, pode ser adicionado depois |
| Audit | 🟡 MÉDIO | Compliance, pode ser async depois |

---

## 7. ORDEM DE IMPLEMENTAÇÃO DIA 3

```
1. UnitOfWorkPort implementation (AsyncSession wrapper)
2. RepositoryPort implementations (SQLAlchemy)
3. EventBusPort implementation (in-memory ou RabbitMQ)
4. Dependency Injection container (FastAPI)
5. API Endpoints (FastAPI routers)
6. Migrations (Alembic)
7. Tests (pytest)
```

---

## 8. INTEGRAÇÃO COM DIA 2

**Dataflow actual:**
```
API Request
  ↓
FastAPI Endpoint (DIA 3)
  ↓
Facade.register_taxpayer()  ← ENTRY POINT (DIA 2)
  ↓
TaxpayerService.register_taxpayer()
  ↓
Domain Aggregate Root creation
  ↓
RepositoryPort.save()  ← Implementation in DIA 3
  ↓
Database write
```

**Sem o Facade = 6 imports diferentes na API**
**Com Facade = 1 import + coordenação centralizada**

---

## 9. PADRÕES APLICADOS

- ✅ **Domain-Driven Design (DDD)** - Rich domain model
- ✅ **Layered Architecture** - Clean separation of concerns
- ✅ **Facade Pattern** - Service aggregation
- ✅ **Unit of Work Pattern** - Transaction boundary
- ✅ **CQRS (Light)** - Commands + Queries separation
- ✅ **Event Sourcing (Ready)** - Events in domain
- ✅ **Dependency Inversion (IoC)** - Ports everywhere
- ✅ **SOLID Principles** - All 5 applied

---

## 10. ESCALABILIDADE FUTURA

```
Se adicionar novo caso de negócio:

+ New Service (ex: WaiverService)
  ↓
+ Interface no Facade
  ↓
API continua usando façade.novo_metodo()
  ↓
Zero mudanças nos endpoints
```

Isso é **verdadeira escalabilidade sem breaking changes**.
