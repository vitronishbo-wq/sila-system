# 🚀 DIA 3 - COMEÇAR AQUI

**Guia de Ação para Infrastructure Layer**

---

## ⚡ QUICK START

**Você está aqui**: Fim do DIA 2 (100% Application pronto)
**Próximo**: DIA 3 (Infrastructure implementation)
**Duração**: 13 horas
**Resultado**: API funcional, database pronto, eventos disparando

---

## 📖 LEIA ANTES DE COMEÇAR

1. **5 minutos**: Este arquivo (você está aqui)
2. **30 minutos**: `DIA3_INFRAESTRUCTURE_ROADMAP.md` (overview dos 7 passos)
3. **15 minutos**: `DIA3_CARTA_INTENÇÃO.md` (expectativas finais)
4. **10 minutos**: `VALIDATION_4_CRITICAL_POINTS.md` (padrões a corrigir)

**Total**: 1 hora de preparação mental antes de codar

---

## 🎯 OS 7 PASSOS

```
PASSO 1: SQLAlchemy Models (2h)
  ├─ Taxpayer model
  ├─ TaxDeclaration model
  ├─ TaxDebt model
  ├─ TaxPayment model
  └─ TaxCertificate model

PASSO 2: Repository Implementations (3h)
  ├─ TaxpayerRepository
  ├─ DeclarationRepository
  ├─ DebtRepository
  ├─ PaymentRepository
  └─ CertificateRepository

PASSO 3: UnitOfWork Wrapper (1h)
  └─ SqlAlchemyUnitOfWork with repositories as properties

PASSO 4: InMemory EventBus (1h)
  └─ InMemoryEventBus implementation

PASSO 5: Dependency Injection (2h)
  ├─ Container setup
  ├─ Service registration
  └─ Factory patterns

PASSO 6: FastAPI Endpoints (2h)
  ├─ TaxpayerRoutes
  ├─ DeclarationRoutes
  ├─ DebtRoutes
  ├─ PaymentRoutes
  └─ CertificateRoutes

PASSO 7: Alembic Migrations (2h)
  ├─ Initial schema
  ├─ Relationships
  ├─ Indexes
  └─ Schema isolation

TOTAL ESTIMATED: 13 hours
```

---

## 🔧 SETUP ANTES DE COMEÇAR

```bash
# 1. Verifique estrutura de diretórios
ls -la apps/backend/modules/taxpayer/

# Esperado:
# domain/              ✅ EXISTE
# application/         ✅ EXISTE
# infrastructure/      ⏳ CRIAR (vazio ou /db /repositories /event_bus /di)
# api/                 ⏳ CRIAR (vazio)

# 2. Crie estrutura
mkdir -p apps/backend/modules/taxpayer/infrastructure/{db,repositories,event_bus,di}
mkdir -p apps/backend/modules/taxpayer/api

# 3. Verifique Python environment
python --version  # Deve ser 3.12+
pip list | grep sqlalchemy  # Deve estar instalado

# 4. Verifique conftest.py
cat conftest.py | grep -i "asyncio\|async"  # Deve ter asyncio setup
```

---

## 🎬 ORDEM DE EXECUÇÃO

### DIA 3A: INFRAESTRUTURA (1º dia - 7 horas)

**Horário**: Manhã (3-4 horas contínuas)

```bash
# PASSO 1: Models
cd apps/backend/modules/taxpayer/infrastructure/db
# Crie models/taxpayer.py, models/tax_declaration.py, etc
# (Veja templates em DIA3_INFRAESTRUCTURE_ROADMAP.md)

# PASSO 2: Repositories
cd ../repositories
# Crie taxpayer_repository.py, declaration_repository.py, etc
# (Base: apps/backend/core/repository.py ou template)

# PASSO 3: UnitOfWork
cd ../
# Crie unit_of_work.py
# Wraps AsyncSession, properties para cada repo

# PASSO 4: EventBus
cd event_bus
# Crie in_memory_event_bus.py
# (Implementa EventBusPort)
```

**Horário**: Tarde (4 horas contínuas / com pausa)

```bash
# PASSO 5: DI
cd ../di
# Crie container.py
# Registre todas as dependências

# PASSO 6: API
cd ../../api
# Crie taxpayers.py (router)
# Use Facade via DI

# PASSO 7: Migrations
cd ../../../..
# Alembic create migration
# Alembic upgrade

# TEST
pytest tests/modules/taxpayer/ -v
```

---

## ✅ VALIDATION CHECKLIST

### Antes de PASSO 1

- [ ] Leu `DIA3_INFRAESTRUCTURE_ROADMAP.md`
- [ ] Compreendeu padrão UoW = mediator de repos
- [ ] Compreendeu padrão Events = publish após commit
- [ ] Setup de diretórios feito
- [ ] Python environment OK

### Depois de PASSO 1 (Models)

- [ ] 5 models criados
- [ ] schema="taxpayer" em todos
- [ ] Timestamps (created_at, updated_at)
- [ ] Foreign keys corretos
- [ ] Relationships bidirecionais

### Depois de PASSO 2 (Repos)

- [ ] BaseRepository implementado
- [ ] 5 repos herdam BaseRepository
- [ ] CRUD methods: save, get, get_all, delete
- [ ] Query builders implementados

### Depois de PASSO 3 (UoW)

- [ ] SqlAlchemyUnitOfWork implementado
- [ ] Context manager: __aenter__, __aexit__
- [ ] Properties: taxpayers, declarations, debts, payments, certificates
- [ ] Commit/rollback gerenciados

### Depois de PASSO 4 (EventBus)

- [ ] InMemoryEventBus implementado
- [ ] publish() e publish_all() funcionando
- [ ] subscribe() e unsubscribe() OK
- [ ] Thread-safe (se needed)

### Depois de PASSO 5 (DI)

- [ ] Container criado
- [ ] Services registrados
- [ ] Repos registrados
- [ ] UoW registrado
- [ ] EventBus registrado

### Depois de PASSO 6 (API)

- [ ] FastAPI router criado
- [ ] POST /taxpayers/register OK
- [ ] GET /taxpayers/{id} OK
- [ ] 5+ endpoints implementados

### Depois de PASSO 7 (Migrations)

- [ ] Alembic migration criada
- [ ] Schema 'taxpayer' isolado
- [ ] Alembic upgrade funciona
- [ ] Tabelas criadas em PostgreSQL

### Validação Final

- [ ] Integration test passa
  ```bash
  pytest tests/modules/taxpayer/test_integration.py -v
  ```
- [ ] Facade recebe via DI
- [ ] Service executa em UoW
- [ ] Repo salva em DB
- [ ] Transaction commita
- [ ] GET consegue recuperar dados
- [ ] Events dispararam
- [ ] Audit trail preenchida

---

## 🎓 TEMPLATES & PADRÕES

Todos os templates estão em `DIA3_INFRAESTRUCTURE_ROADMAP.md`:

### Model Template
```python
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from core.db.base_class import Base
from datetime import datetime

class Taxpayer(Base):
    __tablename__ = "taxpayer_taxpayers"
    __table_args__ = ({"schema": "taxpayer"},)
    
    id = Column(Integer, primary_key=True)
    nif = Column(String(11), unique=True, nullable=False, index=True)
    status = Column(Enum(...), default=..., nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    declarations = relationship("TaxDeclaration", back_populates="taxpayer")
    debts = relationship("TaxDebt", back_populates="taxpayer")
```

### Repository Template
```python
from core.db.base_repository import BaseRepository
from .taxpayer import Taxpayer
from ...domain.value_objects import NIF

class TaxpayerRepository(BaseRepository[Taxpayer]):
    
    async def get_by_nif(self, nif: NIF) -> Optional[Taxpayer]:
        stmt = select(Taxpayer).where(Taxpayer.nif == nif.value)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def get_active_taxpayers(self) -> List[Taxpayer]:
        stmt = select(Taxpayer).where(Taxpayer.status == TaxpayerStatus.ACTIVE)
        result = await self.db.execute(stmt)
        return result.scalars().all()
```

### UoW Template
```python
class SqlAlchemyUnitOfWork(UnitOfWorkPort):
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._taxpayers = None
        self._declarations = None
    
    @property
    def taxpayers(self) -> TaxpayerRepository:
        if self._taxpayers is None:
            self._taxpayers = TaxpayerRepository(self.session)
        return self._taxpayers
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
```

### Endpoint Template
```python
@router.post("/register", response_model=TaxpayerResponseSchema)
async def register_taxpayer(
    data: RegisterTaxpayerSchema,
    container: DIContainer = Depends(get_di_container)
):
    facade = container.get(TaxpayerApplicationFacade)
    result = await facade.register_taxpayer(
        nif=data.nif,
        name=data.name
    )
    return result
```

---

## ⚠️ PONTOS CRÍTICOS (Do VALIDATION_4_CRITICAL_POINTS.md)

### ❌ PADRÃO ERRADO
```python
# Services acessam repos diretamente
class TaxpayerService:
    def __init__(self, repo: TaxpayerRepository):  # WRONG!
        self.repo = repo
```

### ✅ PADRÃO CORRETO
```python
# UoW medeia acesso aos repos
class TaxpayerService:
    def __init__(self, uow: UnitOfWorkPort):  # RIGHT!
        self.uow = uow
    
    async def get_taxpayer(self, nif: NIF):
        # Services usam UoW, não direto
        taxpayer = await self.uow.taxpayers.get_by_nif(nif)
```

### ❌ TIMING ERRADO
```python
# Events publicados ANTES de commit
async def register_taxpayer(self):
    taxpayer = Taxpayer(...)
    await self.repo.save(taxpayer)
    await self.event_bus.publish(TaxpayerRegistered(...))  # WRONG!
    await self.uow.commit()
```

### ✅ TIMING CORRETO
```python
# Events publicados DEPOIS de commit
async def register_taxpayer(self):
    taxpayer = Taxpayer(...)
    await self.uow.taxpayers.save(taxpayer)
    await self.uow.commit()
    # AGORA publica - se falhar, não perde dados
    await self.event_bus.publish_all(taxpayer.get_events())
```

---

## 🐛 TROUBLESHOOTING COMUM

### "ImportError: No module named 'sqlalchemy'"
```bash
pip install sqlalchemy[asyncio]
pip install asyncpg  # PostgreSQL driver
```

### "asyncio.InvalidStateError: Event loop is closed"
```python
# Verifique conftest.py tem:
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

### "Can't find any foreign key relationships"
```python
# Verifique ForeignKey usa TABLE COMPLETO:
payment_id = Column(Integer, ForeignKey("taxpayer_taxpayer_payments.id"))  # ✅
# Não:
payment_id = Column(Integer, ForeignKey("payments.id"))  # ❌
```

### "Column error: 'metadata' is a reserved keyword"
```python
# Use alias + Field mapping:
class Taxpayer(Base):
    metadata_ = Column("metadata", JSON)  # Stored as 'metadata' in DB

class TaxpayerSchema(BaseModel):
    metadata: Optional[Dict] = Field(None, alias="metadata_")
```

### "Transaction already started"
```python
# Certifique que UoW usa context manager:
async with self.uow:  # ✅ Context manager
    await self.uow.taxpayers.save(...)
    # Auto commit/rollback aqui

# Não:
await self.uow.commit()  # ❌ Manual commit
```

---

## 🎯 SUCCESS CRITERIA

Depois de DIA 3, você deve ter:

✅ **Database**
- [x] PostgreSQL schema 'taxpayer' criado
- [x] 5 tabelas (taxpayer_*, com module prefix)
- [x] Índices em NIF, status
- [x] Foreign keys bidirecionais

✅ **Infrastructure**
- [x] 5 SQLAlchemy models
- [x] 5 repository implementations
- [x] UoW com context manager
- [x] InMemory EventBus
- [x] DI container

✅ **API**
- [x] 5+ FastAPI endpoints
- [x] CRUD completo
- [x] Erro handling
- [x] Validação Pydantic

✅ **Integration**
- [x] POST /taxpayers/register → DB
- [x] GET /taxpayers/{id} → responde
- [x] Events disparados
- [x] Transactions gerenciadas

✅ **Testing**
- [x] Unit tests para repos
- [x] Integration test full flow
- [x] Coverage 80%+

---

## 📊 TIMING REALISTA

| Tarefa | Tempo | Notas |
|--------|-------|-------|
| 1a leitura docs | 1h | Preparação |
| PASSO 1-2 (Models+Repos) | 4h | Código repetitivo |
| PASSO 3-4 (UoW+Bus) | 2h | Wrappers simples |
| PASSO 5-6 (DI+API) | 3h | Testes frequentes |
| PASSO 7 (Migrations) | 2h | Alembic boilerplate |
| Troubleshooting | 1h | Sempre há problemas |
| **TOTAL** | **13h** | **2 dias completos** |

---

## 🚀 GO/NO-GO DECISION

**Antes de começar, confirme**:

- [ ] DIA 1 + 2 completo (este arquivo existe? SIM = ✅)
- [ ] Documentação lida (DIA3_INFRAESTRUCTURE_ROADMAP.md)
- [ ] Timeboxed para 13 horas contínuas
- [ ] Database PostgreSQL running
- [ ] Python 3.12+ com venv ativo
- [ ] Team aligned (se for equipe)

**Se tudo acima**: ✅ GO FOR DIA 3

**Se algum não**: ⛔ WAIT (não comece com falhas)

---

## 📞 QUICK REFERENCE

| Problema | Consultar |
|----------|-----------|
| "Como fazer UoW?" | DIA3_INFRAESTRUCTURE_ROADMAP.md PASSO 3 |
| "Como fazer EventBus?" | DIA3_INFRAESTRUCTURE_ROADMAP.md PASSO 4 |
| "Qual pattern correto?" | VALIDATION_4_CRITICAL_POINTS.md |
| "Arch full picture?" | CRITICAL_IMPLEMENTATIONS.md |
| "Validation final?" | DIA3_CARTA_INTENÇÃO.md |

---

## ✨ GOOD LUCK

Você tem:
- ✅ Arquitetura sólida (Domain + Application)
- ✅ Documentação clara
- ✅ Templates prontos
- ✅ Roadmap exato

Você precisa de:
- ⏳ 13 horas de código
- ⏳ Disciplina
- ⏳ Atenção aos detalhes
- ⏳ Múltiplos testes

**Resultado final**: API gov-scale, pronta para produção

---

**Status**: ✅ Ready to start DIA 3
**Recommendation**: START NOW (infrastructure is well-planned)
**Risk**: VERY LOW (patterns are validated)
**Effort**: 13 hours (but very systematic)

**Let's build.**

---

*DIA 3 START GUIDE*
*Generated 22-FEB-2026*
*Infrastructure Layer Ready*
