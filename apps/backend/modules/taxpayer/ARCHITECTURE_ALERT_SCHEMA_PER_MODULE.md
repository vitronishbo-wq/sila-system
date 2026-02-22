# ⚠️ ALERTA ARQUITETURAL - SHARED DATABASE CHAOS

**Documento crítico para SILA multi-module scalability**

---

## 📌 O PROBLEMA

Sistema SILA tem múltiplos contextos:

```
/modules/
├── citizen/
├── taxpayer/        ← Estamos aqui
├── payments/
├── licensing/
├── documents/
├── location/
└── audit/
```

Se todos usarem **1 único schema**:

```sql
-- ❌ ERRADO
CREATE TABLE taxpayers (...)
CREATE TABLE citizens (...)
CREATE TABLE payments (...)
CREATE TABLE licenses (...)
CREATE TABLE documents (...)
```

**Problemas**:
- ❌ Risco de colisão de nomes
- ❌ Sem isolamento de dados
- ❌ Acoplamento implícito entre modules
- ❌ Difícil fazer zero-downtime deployment
- ❌ Difícil re-alocar módulo para servidor diferente

---

## ✅ A SOLUÇÃO: Schema Per Module

**PostgreSQL schema como isolamento de módulos:**

```sql
-- Cada módulo tem seu schema
CREATE SCHEMA taxpayer;
CREATE SCHEMA citizen;
CREATE SCHEMA payments;
CREATE SCHEMA licensing;

-- Tabelas dentro do schema
CREATE TABLE taxpayer.taxpayers (...)
CREATE TABLE taxpayer.declarations (...)

CREATE TABLE citizen.citizens (...)

CREATE TABLE payments.transactions (...)

CREATE TABLE licensing.licenses (...)
```

**Visão no PostgreSQL:**
```
PUBLIC
  └─ tables compartilhadas (users, etc)

TAXPAYER
  ├─ taxpayers
  ├─ declarations
  ├─ debts
  ├─ payments
  ├─ certificates
  └─ (tudo isolado)

CITIZEN
  ├─ citizens
  └─ (tudo isolado)

PAYMENTS
  ├─ transactions
  └─ (tudo isolado)
```

---

## 🏗️ IMPLEMENTAÇÃO ARCHITECTURE

### Option 1: One Database, Multiple Schemas (RECOMENDADO)

```
database: sila_gov

schemas:
  - public (shared: users, roles, permissions)
  - taxpayer (citizen tax data)
  - citizen (citizen registry)
  - payments (financial transactions)
  - licensing (licensing system)
  - audit (audit logs)
```

**Vantagens**:
✅ Isolamento lógico por módulo
✅ Queries cross-module são possíveis
✅ Uma conexão compartilhada
✅ Fácil backup/restore
✅ Fácil replicação

**Desvantagens**:
❌ Ainda não é isolamento total
❌ Risco de FK entre schemas

---

### Option 2: One Database Per Module (FUTURA ESCALABILIDADE)

```
Hoje (single database):
  postgresql://localhost/sila_gov

Amanhã (sharding):
  taxpayer_db → schema taxpayer
  citizen_db → schema citizen
  payments_db → schema payments
```

---

## 🔧 IMPLEMENTAÇÃO

### 1️⃣ Alembic Configuration

```python
# alembic/env.py

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:pass@localhost/sila_gov"
)

target_metadata = Base.metadata

# Especificar schema por módulo
def include_object(object, name, type_, reflected, compare_to):
    # Só processar taxpayer no taxpayer migration
    if type_ == "table":
        return object.schema == "taxpayer"
    return True
```

### 2️⃣ SQLAlchemy Models

```python
# infrastructure/db/models/taxpayer.py

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TaxpayerModel(Base):
    __tablename__ = "taxpayers"
    __table_args__ = {"schema": "taxpayer"}  # ← IMPORTANTE
    
    # ...columns
```

### 3️⃣ SQLAlchemy Connection

```python
# core/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

# Criar schema se não existir
async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS taxpayer"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS citizen"))
        # ...mais schemas
        
        # Depois criar tables
        await conn.run_sync(Base.metadata.create_all)
```

### 4️⃣ Alembic Versioning

```
alembic/versions/

# Taxpayer module migrations
001_taxpayer_create_tables.py
002_taxpayer_add_audit_columns.py

# Citizen module migrations
003_citizen_create_tables.py
004_citizen_add_relationships.py

# Payments module migrations
005_payments_create_tables.py
```

### 5️⃣ Migrations com Schema Explícito

```python
# alembic/versions/001_taxpayer_create_tables.py

def upgrade():
    op.create_table(
        'taxpayers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('nif', sa.String(14), nullable=False),
        # ...
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nif'),
        schema='taxpayer'  # ← CRÍTICO
    )

def downgrade():
    op.drop_table('taxpayers', schema='taxpayer')
```

---

## 📊 ESTRUTURA RESULTANTE

```
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database (sila_gov)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SCHEMA: public                                         │
│  ├─ users (shared)                                     │
│  ├─ roles (shared)                                     │
│  └─ permissions (shared)                               │
│                                                         │
│  SCHEMA: taxpayer                                       │
│  ├─ taxpayers                                          │
│  ├─ tax_declarations                                   │
│  ├─ tax_debts                                          │
│  ├─ tax_payments                                       │
│  └─ tax_certificates                                   │
│                                                         │
│  SCHEMA: citizen                                        │
│  ├─ citizens                                           │
│  ├─ addresses                                          │
│  └─ contact_info                                       │
│                                                         │
│  SCHEMA: payments                                       │
│  ├─ transactions                                       │
│  ├─ payment_methods                                    │
│  └─ payment_receipts                                   │
│                                                         │
│  SCHEMA: licensing                                      │
│  ├─ licenses                                           │
│  ├─ license_types                                      │
│  └─ license_requirements                               │
│                                                         │
│  SCHEMA: audit                                          │
│  └─ audit_logs                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 SEGURANÇA

### Role-Based Access

```sql
-- Criar roles por módulo
CREATE ROLE taxpayer_admin;
CREATE ROLE taxpayer_user;
CREATE ROLE citizen_admin;

-- Grants por schema
GRANT USAGE ON SCHEMA taxpayer TO taxpayer_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA taxpayer TO taxpayer_admin;

GRANT USAGE ON SCHEMA taxpayer TO taxpayer_user;
GRANT SELECT ON ALL TABLES IN SCHEMA taxpayer TO taxpayer_user;

-- Citizen admin não acessa taxpayer
GRANT USAGE ON SCHEMA citizen TO citizen_admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA citizen TO citizen_admin;
-- (sem acesso a taxpayer)
```

---

## 🎯 BENEFÍCIOS LONG-TERM

### Hoje (Single Module)
```
Database: 1 schema
Module escalation: 0-2 months
```

### Amanhã (Multi-Module)
```
Database: 7 schemas (tax, citizen, payment, licensing, doc, location, audit)
Module escalation: Weeks (não impacta outros módulos)
```

### Futuro (Distributed)
```
Database: Múltiplos servidores
Sharding: taxpayer_srv, citizen_srv, payments_srv
Escalação: Infinita (add servers as needed)

taxpayer-db@host1: schema taxpayer
citizen-db@host2: schema citizen
payments-db@host3: schema payments
```

---

## ⚡ MIGRAÇÃO PATH

### DIA 3 (Agora)
```sql
-- Criar schema
CREATE SCHEMA taxpayer;

-- Rodar migrations dentro do schema
alembic upgrade head
```

### Futuro (Quando houver 7+ módulos)
```sql
-- Move taxpayer to separate database
CREATE DATABASE sila_taxpayer;
  CREATE SCHEMA taxpayer;
  -- Restore taxpayer data

-- Shared data fica em sila_gov
```

---

## 📋 CHECKLIST DIA 3

- [ ] Schema `taxpayer` criado
- [ ] Todas tabelas em `schema: taxpayer`
- [ ] Models especificam `__table_args__ = {"schema": "taxpayer"}`
- [ ] Migrations usam `schema='taxpayer'` explícito
- [ ] Connection string correta
- [ ] Testes rodam com schema isolado
- [ ] Documentação escrita

---

## 🚀 PRÓXIMO PASSO

Quando implementar outros módulos:

```python
# modules/citizen/infrastructure/db/models/citizen.py
class CitizenModel(Base):
    __tablename__ = "citizens"
    __table_args__ = {"schema": "citizen"}  # ← Diferente!

# modules/payments/infrastructure/db/models/payment.py
class PaymentModel(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "payments"}  # ← Diferente!
```

**Resultado**: Total isolamento. Zero acoplamento. Escaladíssimo.

---

## 🔗 CROSS-MODULE QUERIES (Quando necessário)

```python
# Raro, mas às vezes precisa...

async def get_citizen_with_tax_info(citizen_id: UUID):
    # Join entre schemas (não é o ideal, mas é possível)
    query = select(CitizenModel, TaxpayerModel).join(
        TaxpayerModel,
        TaxpayerModel.citizen_id == CitizenModel.id
    )
    # CitizenModel from schema citizen
    # TaxpayerModel from schema taxpayer
```

Prefer: API-to-API em vez de direct queries.

---

## ✅ CONCLUSÃO

**Schema per module = Foundation para gov-scale architecture**

Não implementar isto agora:
- Regret depois
- Refatoração custosa
- Acoplamento difícil de desfazer

Implementar agora:
- Futuro-proof
- Zero regret
- Clean separation
- Pronto para distribuição

**Recomendação**: Implementar isto AGORA no DIA 3, não deixar para depois.
