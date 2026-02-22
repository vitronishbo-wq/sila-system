# 🛠️ SILA Phase 3 (Auth) — Guia de Implementação das Correções

**Data:** 16 de Novembro de 2025 **Status:** Pronto para Implementação **Tempo
Estimado:** 45 minutos

---

## 📌 Sumário das Correções

| #   | Tarefa                                     | Arquivo             | Prioridade | Status  |
| --- | ------------------------------------------ | ------------------- | ---------- | ------- |
| 1   | Adicionar campo `scopes` ao ORM User       | `models/user.py`    | 🔴 CRÍTICA | ⏳ TODO |
| 2   | Adicionar campo `role` ao ORM User         | `models/user.py`    | 🔴 CRÍTICA | ⏳ TODO |
| 3   | Atualizar DTO `UserRead` com scopes/role   | `models/user.py`    | 🔴 CRÍTICA | ⏳ TODO |
| 4   | Incluir scopes/level em JWT claims         | `endpoints.py`      | 🔴 CRÍTICA | ⏳ TODO |
| 5   | Extrair scopes/level do token decodificado | `auth_utils.py`     | 🔴 CRÍTICA | ⏳ TODO |
| 6   | Criar migration SQL                        | Banco de Dados      | 🟡 MÉDIA   | ⏳ TODO |
| 7   | Re-executar validação                      | validate_phase_3.py | 🟢 BAIXA   | ⏳ TODO |
| 8   | Executar testes                            | pytest              | 🟢 BAIXA   | ⏳ TODO |

---

## ✅ Correção #1: Adicionar Campos ao ORM User

**Arquivo:** `apps/backend/modules/auth/models/user.py`

### Versão Atual (❌ INCOMPLETO)

```python
class User(Base):
    """ORM model representing an application user."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    level = Column(PgEnum(AdministrativeLevel, name="administrativelevel"), nullable=True)
    region_id = Column(UUID(as_uuid=True), nullable=True)
    # ❌ FALTAM: scopes, role
```

### Versão Corrigida (✅ COMPLETO)

```python
from sqlalchemy.dialects.postgresql import JSON  # ✅ NOVO import

class User(Base):
    """ORM model representing an application user."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    level = Column(PgEnum(AdministrativeLevel, name="administrativelevel"), nullable=True)
    region_id = Column(UUID(as_uuid=True), nullable=True)

    # ✅ NOVO: Escopos de permissão
    scopes = Column(JSON, nullable=False, default=lambda: [])

    # ✅ NOVO: Role para controle de acesso
    role = Column(String(50), nullable=True)
```

---

## ✅ Correção #2: Atualizar DTO UserRead

**Arquivo:** `apps/backend/modules/auth/models/user.py`

### Versão Atual (❌ INCOMPLETO)

```python
class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Versão Corrigida (✅ COMPLETO)

```python
from typing import List, Optional  # ✅ Verificar import

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    scopes: List[str] = []  # ✅ NOVO
    role: Optional[str] = None  # ✅ NOVO

    class Config:
        from_attributes = True
```

### Atualizar UserBase também (OPCIONAL)

```python
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    level: AdministrativeLevel | None = None
    region_id: str | None = None
    scopes: List[str] = []  # ✅ NOVO (OPCIONAL)
    role: str | None = None  # ✅ NOVO (OPCIONAL)
```

---

## ✅ Correção #3: Incluir Scopes/Level no JWT

**Arquivo:** `apps/backend/modules/auth/endpoints.py`

### Versão Atual (❌ INCOMPLETO)

```python
@router.post("/login")
async def login(
    request: Request,
    email: Optional[str] = None,
    password: Optional[str] = None,
    db: AsyncSession = Depends(get_db_session),
):
    # ... validação de credenciais ...

    # ❌ PROBLEMA: Sem scopes no token!
    access = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))

    return {
        "status": "success",
        "email": user_dto.email,
        "user_id": user_dto.id,
        "access_token": access,
        "refresh_token": refresh,
    }
```

### Versão Corrigida (✅ COMPLETO)

```python
@router.post("/login")
async def login(
    request: Request,
    email: Optional[str] = None,
    password: Optional[str] = None,
    db: AsyncSession = Depends(get_db_session),
):
    # ... validação de credenciais ...

    # ✅ NOVO: Incluir scopes e level no token
    additional_claims = {
        "scopes": user.scopes or [],
        "level": user.level.value if user.level else "local",
        "role": user.role or "",
    }

    access = create_access_token(
        subject=str(user.id),
        additional_claims=additional_claims  # ✅ NOVO
    )
    refresh = create_refresh_token(subject=str(user.id))

    user_dto = UserRead.model_validate(user)

    return {
        "status": "success",
        "email": user_dto.email,
        "user_id": user_dto.id,
        "is_superuser": user_dto.is_superuser,
        "region_id": user_dto.region_id,
        "scopes": user_dto.scopes,  # ✅ NOVO (retornar ao cliente)
        "access_token": access,
        "refresh_token": refresh,
    }
```

---

## ✅ Correção #4: Extrair Scopes/Level do Token

**Arquivo:** `apps/backend/modules/auth/auth_utils.py` (ou similar)

### Versão Atual (❌ INCOMPLETO)

```python
async def get_current_active_user(
    token: str = Depends(oauth2_scheme)
) -> UserRead:
    payload = decode_access_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Buscar usuário no banco
    user = await get_user_by_id(username)

    # ❌ PROBLEMA: Scopes/level não vêm do token
    return UserRead.model_validate(user)
```

### Versão Corrigida (✅ COMPLETO)

```python
async def get_current_active_user(
    token: str = Depends(oauth2_scheme)
) -> UserRead:
    payload = decode_access_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Buscar usuário no banco
    user = await get_user_by_id(username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=401, detail="User is inactive")

    # ✅ NOVO: Extrair scopes/level do token e atualizar user
    # Isto garante que os claims do token sejam usados se disponíveis
    if "scopes" in payload:
        user.scopes = payload.get("scopes", [])

    if "level" in payload:
        level_str = payload.get("level", "local")
        user.level = AdministrativeLevel(level_str)

    if "role" in payload:
        user.role = payload.get("role")

    user_dto = UserRead.model_validate(user)
    return user_dto
```

---

## ✅ Correção #5: Migration SQL

**Tipo:** PostgreSQL Migration **Arquivo:**
`migrations/versions/XXXXX_add_scopes_role_to_user.py` (ou execute direto)

### Executar Direto (Rápido)

```sql
-- Adicionar coluna scopes (JSON)
ALTER TABLE users ADD COLUMN IF NOT EXISTS scopes JSON NOT NULL DEFAULT '[]';

-- Adicionar coluna role (String)
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) NULL;

-- Criar índice para performance (OPCIONAL)
CREATE INDEX IF NOT EXISTS idx_users_scopes ON users USING gin(scopes);

-- Verificar
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'users' AND column_name IN ('scopes', 'role');
```

### Via Alembic (Recomendado)

```bash
# Gerar migration
alembic revision --autogenerate -m "Add scopes and role to users table"

# Executar
alembic upgrade head
```

---

## 📝 Checklist de Implementação

### Fase 1: Código

- [ ] **1.1** Abrir `apps/backend/modules/auth/models/user.py`
- [ ] **1.2** Adicionar `from sqlalchemy.dialects.postgresql import JSON`
- [ ] **1.3** Adicionar campo `scopes` ao ORM User
- [ ] **1.4** Adicionar campo `role` ao ORM User
- [ ] **1.5** Atualizar DTO `UserRead` com scopes e role
- [ ] **1.6** Verificar que o arquivo compila sem erros
  ```bash
  python3 -c "from modules.auth.models.user import User, UserRead; print('✅ OK')"
  ```

### Fase 2: Endpoints

- [ ] **2.1** Abrir `apps/backend/modules/auth/endpoints.py`
- [ ] **2.2** Localizar função `login()`
- [ ] **2.3** Adicionar `additional_claims` com scopes/level/role
- [ ] **2.4** Usar `additional_claims` em `create_access_token()`
- [ ] **2.5** Adicionar scopes à resposta JSON
- [ ] **2.6** Verificar que o arquivo compila sem erros
  ```bash
  python3 -c "from modules.auth.endpoints import router; print('✅ OK')"
  ```

### Fase 3: Auth Utils

- [ ] **3.1** Abrir `apps/backend/modules/auth/auth_utils.py` (ou locate
      get_current_active_user)
- [ ] **3.2** Localizar função `get_current_active_user()`
- [ ] **3.3** Adicionar extração de scopes/level/role do payload
- [ ] **3.4** Atualizar user object com claims do token
- [ ] **3.5** Verificar que o arquivo compila sem erros

### Fase 4: Database

- [ ] **4.1** Backup do banco de dados
  ```bash
  pg_dump sila_db > backup_$(date +%s).sql
  ```
- [ ] **4.2** Executar migration SQL
  ```bash
  psql sila_db < migration.sql
  ```
- [ ] **4.3** Verificar que as colunas foram criadas
  ```bash
  psql sila_db -c "SELECT scopes, role FROM users LIMIT 1;"
  ```

### Fase 5: Testes

- [ ] **5.1** Executar teste `test_admin_scope_access`
  ```bash
  pytest apps/backend/tests/test_auth.py::test_admin_scope_access -v
  ```
- [ ] **5.2** Esperado: ✅ PASS
- [ ] **5.3** Se FAIL: debugar com `--pdb`
  ```bash
  pytest apps/backend/tests/test_auth.py::test_admin_scope_access -v --pdb
  ```

### Fase 6: Validação

- [ ] **6.1** Re-executar wrapper de validação
  ```bash
  python3 validate_phase_3.py --report --verbose
  ```
- [ ] **6.2** Esperado: ✅ 25+ PASS, ❌ 0 FAIL
- [ ] **6.3** Gerar novo relatório
  ```bash
  cat phase_3_validation_report.json | jq '.summary'
  ```

---

## 🔍 Debugging: Se Algo Der Errado

### Erro: "AttributeError: 'User' object has no attribute 'scopes'"

**Causa:** Campo scopes não foi adicionado ao ORM ou migração não foi executada.

**Solução:**

```bash
# 1. Verificar que o campo existe no DB
psql sila_db -c "\d users;" | grep scopes

# 2. Se não existe, executar SQL
psql sila_db -c "ALTER TABLE users ADD COLUMN scopes JSON NOT NULL DEFAULT '[]';"

# 3. Verificar que o ORM tem o campo
grep -n "scopes = Column" apps/backend/modules/auth/models/user.py

# 4. Re-importar módulo em Python (ou reiniciar servidor)
```

---

### Erro: "test_admin_scope_access ainda falha com 403"

**Causa:** Possível: scopes não estão sendo incluídos no JWT.

**Solução:**

```bash
# 1. Adicionar debug no login
# Adicione ao endpoints.py:
print(f"DEBUG: user.scopes = {user.scopes}")
print(f"DEBUG: additional_claims = {additional_claims}")

# 2. Verificar o token gerado
# Decodificar manualmente:
import jwt
token = "eyJ..."
decoded = jwt.decode(token, options={"verify_signature": False})
print(decoded)

# 3. Verificar se 'scopes' aparece no payload
assert "scopes" in decoded, "scopes não está no token!"
```

---

### Erro: "Migration falha: coluna já existe"

**Solução:**

```sql
-- Verificar se coluna já existe
SELECT column_name FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'scopes';

-- Se já existe, skip a migration ou use IF NOT EXISTS
ALTER TABLE users ADD COLUMN IF NOT EXISTS scopes JSON NOT NULL DEFAULT '[]';
```

---

## 📊 Validation Após Correção

### Teste Rápido (Manual)

```bash
# 1. Iniciar servidor
cd apps/backend
python3 -m uvicorn main:app --reload

# 2. Em outro terminal, fazer login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@sila.gov.ao", "password":"password123"}'

# 3. Decodificar token retornado
# Copie o access_token e vá para jwt.io para decodificar

# 4. Verificar que o payload contém:
# {
#   "sub": "user-uuid",
#   "scopes": ["tenant:admin"],  # ✅ DEVE ESTAR AQUI
#   "level": "central",           # ✅ DEVE ESTAR AQUI
#   "role": "admin",              # ✅ PODE ESTAR AQUI
#   "type": "access",
#   "exp": ...
# }
```

### Teste Automático (Pytest)

```bash
# Executar todos os testes de auth
pytest apps/backend/tests/test_auth.py -v

# Esperado:
# ✅ test_auth_ping PASSED
# ✅ test_login_success PASSED
# ✅ test_admin_scope_access PASSED  ← Este era o falho
# ✅ test_refresh_token PASSED
# ... etc
```

### Validação Final

```bash
# Re-rodar o wrapper
python3 validate_phase_3.py --report --verbose

# Esperar output final:
# ================================================================================
# 📊 SUMMARY
# ================================================================================
# ✅ Passed: 40+
# ❌ Failed: 0
# ⚠️  Warnings: 0-2
# ℹ️  Skipped: 15
#
# 🎉 PHASE 3 VALIDATION PASSED!
```

---

## 📋 Forma de Rollback (Se Necessário)

```bash
# 1. Reverter código Git
git checkout apps/backend/modules/auth/models/user.py
git checkout apps/backend/modules/auth/endpoints.py

# 2. Reverter database
psql sila_db < backup_XXXXX.sql

# 3. Reiniciar servidor
```

---

## 📞 Suporte e Próximas Etapas

Após implementar estas correções:

1. ✅ Phase 3 (Auth) será validado
2. ✅ Testes de escopo tenant:admin passarão
3. ✅ Permissões funcionarão conforme esperado
4. ✅ Preparar para Phase 4 (integração completa)

---

**Fim do Guia de Implementação**

_Versão: 1.0 — 16 de Novembro de 2025_
