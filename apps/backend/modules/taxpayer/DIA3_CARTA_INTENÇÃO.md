# 📋 DIA 3 - CARTA DE INTENÇÃO FINAL

**Documento de referência para Infrastructure Layer**

---

## 🎯 OBJETIVO

Implementar Infrastructure Layer transformando:

```
Domain + Application (100%)
    ↓
+ Infrastructure (0% → 100%)
    ↓
= Funcionando end-to-end
```

---

## ✅ PRÉ-REQUISITOS VALIDADOS

### Validação 4-Pontos Críticos

- ✅ Ponto 1: UoW será mediador de repositories (corrigir no DIA 3)
- ✅ Ponto 2: Events publicados APÓS commit (implementar corretamente)
- ✅ Ponto 3: Facade sem regra de negócio (correto)
- ✅ Ponto 4: Ports 100% pure typing (correto)

### Preparação

- ✅ Domain Layer: Rich model, events, value objects
- ✅ Application Layer: Facade, Services, Commands, Queries
- ✅ Ports: 7 interfaces definidas
- ✅ Documentação: Regras claras em cada guia

---

## 🚀 EXECUTE NA ORDEM EXATA

### 🏗️ FASE 1: Database Foundation

**PASSO 1: SQLAlchemy Models** (2h)
```
apps/backend/modules/taxpayer/infrastructure/db/models/
  ├─ __init__.py
  ├─ taxpayer.py
  ├─ tax_declaration.py
  ├─ tax_debt.py
  ├─ tax_payment.py
  └─ tax_certificate.py
```

Checklist:
- [ ] Schema `taxpayer` em `__table_args__`
- [ ] UUID primary keys
- [ ] Timestamps (created_at, updated_at)
- [ ] Índices em campos de busca
- [ ] Relationships com back_populates

**PASSO 2: Repositories** (3h)
```
apps/backend/modules/taxpayer/infrastructure/repositories/
  ├─ __init__.py
  ├─ base_repository.py
  ├─ taxpayer_repository.py
  ├─ tax_declaration_repository.py
  ├─ tax_debt_repository.py
  ├─ tax_payment_repository.py
  └─ tax_certificate_repository.py
```

Checklist:
- [ ] Herdam de *RepositoryPort
- [ ] Domain ↔ Model conversion
- [ ] Sem commit() dentro
- [ ] Paginação com skip/limit

**PASSO 3: UnitOfWork** (1h)
```
apps/backend/modules/taxpayer/infrastructure/db/
  └─ unit_of_work.py
```

Checklist:
- [ ] Lazy-load repositories
- [ ] Context manager (__aenter__, __aexit__)
- [ ] commit() e rollback() explícitos
- [ ] Auto-rollback on exception

---

### 📡 FASE 2: Event Infrastructure

**PASSO 4: InMemory EventBus** (1h)
```
apps/backend/modules/taxpayer/infrastructure/event_bus/
  ├─ __init__.py
  └─ in_memory_event_bus.py
```

Checklist:
- [ ] publish() e publish_all()
- [ ] subscribe() e unsubscribe()
- [ ] Error handling (não falha se subscriber cair)
- [ ] Asyncio-safe (gather, tasks)

---

### 🔧 FASE 3: Dependency Injection

**PASSO 5: DI Container** (2h)
```
apps/backend/modules/taxpayer/infrastructure/di/
  ├─ __init__.py
  └─ container.py
```

Checklist:
- [ ] TaxpayerContainer com todas dependências
- [ ] get_facade() retorna TaxpayerApplicationFacade
- [ ] Mocks para AGT, Notification, Audit, Cache (por enquanto)
- [ ] FastAPI integration pattern

---

### 🌐 FASE 4: API Layer

**PASSO 6: FastAPI Endpoints** (2h)
```
apps/backend/modules/taxpayer/api/
  ├─ __init__.py
  └─ taxpayers.py
```

Endpoints:
```
POST   /taxpayers/register          - RegisterTaxpayerCommand
GET    /taxpayers/{id}              - GetTaxpayerQuery
GET    /taxpayers                   - ListTaxpayers
PATCH  /taxpayers/{id}              - UpdateTaxpayer

POST   /taxpayers/{id}/declarations - FileDeclarationCommand
GET    /taxpayers/{id}/declarations - GetDeclarationHistoryQuery
PATCH  /declarations/{id}           - ProcessDeclaration

GET    /taxpayers/{id}/debts        - GetTaxDebtQuery
POST   /taxpayers/{id}/debts/{debt_id}/pay - PayTaxCommand

POST   /taxpayers/{id}/certificates - RequestCertificateCommand
GET    /taxpayers/{id}/certificates - GetTaxCertificateQuery
```

Checklist:
- [ ] Todos endpoints usam Facade (1 entrada)
- [ ] DTOs em input/output (não domain entities)
- [ ] Error handling com HTTPException
- [ ] CORS configured
- [ ] Documentation (docstrings)

---

### 📦 FASE 5: Database Setup

**PASSO 7: Alembic Migrations** (2h)
```
alembic/
  ├─ versions/
  │   └─ 001_taxpayer_create_tables.py
  └─ env.py
```

Checklist:
- [ ] Alembic init (async template)
- [ ] Primeira migration auto-generated
- [ ] Schema `taxpayer` criado
- [ ] Constraints e índices
- [ ] Testes de up/down migration

---

## 📊 TIMELINE TOTAL

| Fase | Passos | Tempo | Cumulativo |
|------|--------|-------|-----------|
| 1 | Models, Repos, UoW | 6h | 6h |
| 2 | EventBus | 1h | 7h |
| 3 | DI Container | 2h | 9h |
| 4 | API Endpoints | 2h | 11h |
| 5 | Migrations | 2h | 13h |
| **TOTAL** | **7 passos** | **13h** | **1-2 dias** |

---

## ✨ RESULT ESPERADO AO FINAL DIA 3

```
✅ Full Integration Test:

1. POST /taxpayers/register
   ├─ Facade.register_taxpayer()
   ├─ TaxpayerService.register_taxpayer()
   ├─ UoW.taxpayers.save() [sem commit]
   ├─ Service.add_event()
   └─ UoW.commit()
   
2. Event Published
   ├─ InMemory EventBus.publish()
   ├─ Subscribers execute
   └─ Logging + Notifications
   
3. Verify in Database
   ├─ SELECT * FROM taxpayer.taxpayers
   └─ Data persisted

4. GET /taxpayers/{id}
   └─ Returns domain data
```

---

## 🞗 CRÍTICO: NÃO FAZER

❌ **Nunca**:
- Commit dentro do repository
- Publicar eventos antes do commit
- Query direto sem UoW
- Domain entities em API response
- Sem error handling em endpoints
- Sem indices em findBy fields
- Sem schema isolation

✅ **Sempre**:
- UoW controla transações
- Eventos após commit (fora transação)
- Repositories via UoW
- DTOs em responses
- Try/except mapping para HTTP
- Índices estratégicos
- `__table_args__ = {"schema": "taxpayer"}`

---

## 🔍 VALIDAÇÃO PÓS-DIA 3

Rodar este teste:

```python
# tests/test_integration_full.py

@pytest.mark.asyncio
async def test_full_flow():
    # 1. Setup
    async with AsyncSession(engine) as session:
        uow = SqlAlchemyUnitOfWork(session)
        facade = get_facade_from_container(uow)
    
    # 2. Register
    cmd = RegisterTaxpayerCommand(
        nif="123456789012",
        name="João Silva",
        email="joao@example.com",
        phone="961234567",
        address="Rua A",
        tax_regime="GERAL",
        registered_by=user_id
    )
    taxpayer = await facade.register_taxpayer(**asdict(cmd))
    
    # 3. Verify
    assert taxpayer.id is not None
    assert taxpayer.status == "DRAFT"
    
    # 4. Query back
    found = await facade.get_taxpayer(taxpayer.id)
    assert found.name == "João Silva"
    
    # 5. Database check
    from sqlalchemy import text
    result = await session.execute(
        text("SELECT COUNT(*) FROM taxpayer.taxpayers")
    )
    count = result.scalar()
    assert count > 0
```

---

## 📚 REFERÊNCIA RÁPIDA

### Commands Úteis

```bash
# Criar migration
alembic revision --autogenerate -m "Create tables"

# Rodar migration
alembic upgrade head

# Reverter
alembic downgrade -1

# Test database connection
psql -h localhost -U user -d sila_gov -c "SELECT 1"

# Check schemas
psql sila_gov -c "\dn"

# Check tables in schema
psql sila_gov -c "\dt taxpayer.*"
```

### Test FastAPI Endpoints

```bash
# Via cURL
curl -X POST http://localhost:8000/taxpayers/register \
  -H "Content-Type: application/json" \
  -d '{
    "nif": "123456789012",
    "name": "João Silva",
    "tax_regime": "GERAL",
    "registered_by": "uuid-here"
  }'

# Via Python
import httpx
client = httpx.AsyncClient(base_url="http://localhost:8000")
r = await client.post("/taxpayers/register", json={...})
assert r.status_code == 201
```

---

## 🞗 MATRIX VERIFICAÇÃO FINAL

| Item | Status | Evidência |
|------|--------|-----------|
| Models criados | ✅ | 5 files em `infrastructure/db/models/` |
| Repositories implementados | ✅ | Têm métodos save(), find_by_id(), etc |
| UoW funciona | ✅ | `async with uow:` e commit executa |
| EventBus funciona | ✅ | Events publicados, subscribers em log |
| DI configurado | ✅ | Facade injetável via Depends() |
| Endpoints funcionam | ✅ | Curl/pytest passa 201 Created |
| Migration executa | ✅ | `alembic upgrade head` sem erros |
| Schema isolado | ✅ | `\dt taxpayer.*` mostra tabelas |

---

## 🎓 APRENDIZADO ESPERADO

Ao final DIA 3, você entenderá:

- ✅ SQLAlchemy async patterns
- ✅ Repository pattern com domain entities
- ✅ Unit of Work com SQLAlchemy sessions
- ✅ Event-driven architecture propagation
- ✅ Dependency injection com FastAPI
- ✅ Alembic migrations com schemas
- ✅ PostgreSQL schema isolation
- ✅ Full DDD integration

---

## 📞 TROUBLESHOOTING COMUM

**"ModuleNotFoundError: No module named 'sqlalchemy'"**
→ `pip install sqlalchemy[asyncio]`

**"psycopg2: connection refused"**
→ PostgreSQL não está rodando: `docker run postgres`

**"No schemas named 'taxpayer'"**
→ Adicionar `CREATE SCHEMA taxpayer` antes de migrations

**"UoW commit não é async"**
→ Use `await self.session.commit()` não `self.session.commit()`

**"Events nunca foram publicados"**
→ Verificar se subscribers foram registrados: `event_bus.subscribe(...)`

---

## ✅ GO/NO-GO DECISION

Você está pronto para DIA 3 se:

- ✅ Entendeu os 4 pontos críticos
- ✅ Leu o roadmap completo
- ✅ Entendeu schema per module
- ✅ Tem 2-3 dias disponíveis
- ✅ PostgreSQL rodando localmente
- ✅ Python environment pronto

---

## 🚀 PRÓXIMO COMANDO

```bash
cd /home/dev12cls/sila-system
source .venv/bin/activate
mkdir -p apps/backend/modules/taxpayer/infrastructure/{db,repositories,event_bus,di}
# COMECE PELO PASSO 1: SQLAlchemy Models
```

---

**Você está pronto. A arquitetura está sólida. Executa o plano.**

**60% do trabalho difícil foi feito. Os 40% restantes são "just code".**
