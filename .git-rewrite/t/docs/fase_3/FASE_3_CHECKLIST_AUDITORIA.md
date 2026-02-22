# ✅ Checklist Técnico da Fase 3 (Auth) — Auditoria Completa

**Data:** 16 de Novembro de 2025 **Versão:** 1.0 **Status:** Pendente de Execução

---

## 📋 Estrutura de Auditoria

Este checklist foi organizado em **6 camadas hierárquicas** conforme a especificação do
projeto:

1. **Núcleo do Módulo de Autenticação** (`modules/auth/`)
2. **Testes do Módulo Antigo** (`modules/auth/tests/`)
3. **Camada Core** (`core/`)
4. **Novo Módulo de Autenticação** (`apps/backend/src/sila_auth/`) — _não existe ainda_
5. **Testes do Novo Módulo** (`apps/backend/src/sila_auth/tests/`)
6. **Relatórios de Migração** (`reports/onboarding/`)

---

# 🔐 Camada 1: Núcleo do Módulo de Autenticação

## Item 1: `modules/auth/permissions.py`

### 🎯 Objetivo

Validar que a lógica de permissões (escopos e níveis) está implementada corretamente e
compatível com o novo sistema.

### ✔️ Critérios de Validação

| Critério                                   | Esperado                                              | Status | Observação                        |
| ------------------------------------------ | ----------------------------------------------------- | ------ | --------------------------------- |
| **1.1** Classe `Scopes` (Enum) existe      | `TENANT_ADMIN`, `GLOBAL_ADMIN`, etc.                  | [ ]    | Deve incluir `tenant:admin`       |
| **1.2** Função `requires_scopes()` existe  | Decorator funcional                                   | [ ]    | Aceita `Scopes` ou `List[Scopes]` |
| **1.3** Validação de scopes                | Compara `user.scopes` contra `required_scope_strings` | [ ]    | Usa `all()` logic                 |
| **1.4** Erro 403 com detalhes              | HTTPException com mensagem clara                      | [ ]    | Inclui escopos faltantes          |
| **1.5** Classe `AccessLevel` (Enum) existe | `local`, `provincial`, `central`                      | [ ]    | Mantém hierarquia                 |
| **1.6** Função `requires_level()` existe   | Decorator funcional                                   | [ ]    | Compara hierarquicamente          |
| **1.7** Ordem de níveis correta            | `LEVEL_ORDER = {local: 1, provincial: 2, central: 3}` | [ ]    | Crescente = crescente poder       |
| **1.8** Validação de nivel                 | `user_level >= min_level`                             | [ ]    | Ordem respeitada                  |
| **1.9** Enum casting                       | Converte `Enum` → string corretamente                 | [ ]    | Trata `user_level.value`          |

### 🔍 Validação de Código

```python
# ✅ Esperado
from enum import Enum
from functools import wraps

class Scopes(str, Enum):
    TENANT_ADMIN = "tenant:admin"
    GLOBAL_ADMIN = "global:admin"

def requires_scopes(required_scopes: Union[Scopes, List[Scopes]]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            user_scopes = getattr(user, "scopes", [])
            required_scope_strings = [s.value for s in required_scopes]
            if not all(scope in user_scopes for scope in required_scope_strings):
                raise HTTPException(status_code=403, detail="Escopos insuficientes")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator
```

### 📝 Comando de Auditoria

```bash
grep -n "class Scopes\|def requires_scopes\|TENANT_ADMIN\|tenant:admin" \
  apps/backend/modules/auth/permissions.py
```

---

## Item 2: `modules/auth/endpoints.py`

### 🎯 Objetivo

Validar que os endpoints implementam autenticação e aplicam permissões corretamente.

### ✔️ Critérios de Validação

| Critério                                | Esperado                              | Status | Observação                          |
| --------------------------------------- | ------------------------------------- | ------ | ----------------------------------- |
| **2.1** Endpoint `POST /login` existe   | Aceita email + password               | [ ]    | Suporta JSON, form, query           |
| **2.2** Endpoint retorna access token   | `access_token` em response            | [ ]    | Bearer token válido                 |
| **2.3** Endpoint retorna refresh token  | `refresh_token` em response           | [ ]    | TTL 7 dias                          |
| **2.4** UserRepository é chamado        | `repo.authenticate()` chamado         | [ ]    | Valida credenciais                  |
| **2.5** Tokens são criados corretamente | `create_access_token()` chamado       | [ ]    | Inclui `subject` (user.id)          |
| **2.6** Decorators de permissão existem | `@requires_scopes`, `@requires_level` | [ ]    | Podem ser usados em endpoints       |
| **2.7** Logout endpoint existe          | `POST /auth/logout`                   | [ ]    | Retorna sucesso                     |
| **2.8** Refresh endpoint existe         | `POST /auth/refresh`                  | [ ]    | Aceita refresh_token                |
| **2.9** Test token endpoint existe      | `POST /auth/test-token`               | [ ]    | Requer autenticação (401 sem token) |

### 🔍 Validação de Código

```python
# ✅ Esperado
@router.post("/login")
async def login(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
):
    # ... validação de credenciais ...
    access = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))
    return {..., "access_token": access, "refresh_token": refresh}

@router.post("/auth/test-token", response_model=UserRead)
@requires_scopes(Scopes.READ)  # ✅ Decorator aplicado
async def test_token(current_user: UserRead = Depends(get_current_active_user)):
    return current_user
```

### 📝 Comando de Auditoria

```bash
grep -n "@router.post\|def login\|create_access_token\|@requires_scopes\|@requires_level" \
  apps/backend/modules/auth/endpoints.py
```

---

## Item 3: `modules/auth/security.py`

### 🎯 Objetivo

Validar que a geração, leitura e verificação de JWT tokens está correta.

### ✔️ Critérios de Validação

| Critério                                    | Esperado                   | Status | Observação                          |
| ------------------------------------------- | -------------------------- | ------ | ----------------------------------- |
| **3.1** `JWTHandler` ou funções JWT existem | Criação/decode de tokens   | [ ]    | Algoritmo HS256                     |
| **3.2** Access token expiração              | 15 minutos                 | [ ]    | Configurável via settings           |
| **3.3** Refresh token expiração             | 7 dias                     | [ ]    | Configurável via settings           |
| **3.4** Função `_encode()`                  | Cria JWT com exp + iat     | [ ]    | Usa `jwt.encode()`                  |
| **3.5** Função `create_access_token()`      | Inclui claims adicionais   | [ ]    | Suporta `additional_claims`         |
| **3.6** Função `create_refresh_token()`     | Refresh separado do access | [ ]    | Tipo diferente no payload           |
| **3.7** Função `_decode()`                  | Tenta múltiplas secrets    | [ ]    | Fallback para secrets antigos       |
| **3.8** Função `decode_access_token()`      | Valida tipo "access"       | [ ]    | Verifica `exp` se `verify_exp=True` |
| **3.9** Função `decode_refresh_token()`     | Valida tipo "refresh"      | [ ]    | Separado do access                  |
| **3.10** Tratamento de erro                 | Lança `InvalidTokenError`  | [ ]    | Para tokens expirados/inválidos     |

### 🔍 Validação de Código

```python
# ✅ Esperado
from jwt import InvalidTokenError

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(
    *,
    subject: str,
    additional_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    claims: Dict[str, Any] = {"sub": subject, "type": "access"}
    if additional_claims:
        claims.update(additional_claims)
    # ... encode com expiração ...
    return _encode(claims, ACCESS_SECRET, expiry)

def decode_access_token(token: str, *, verify_exp: bool = True) -> DecodedToken:
    secrets = _iter_secrets(ACCESS_SECRET, ACCESS_FALLBACK_SECRET)
    return _decode(token, expected_type="access", secrets=secrets, verify_exp=verify_exp)
```

### 📝 Comando de Auditoria

```bash
grep -n "def create_access_token\|def decode_access_token\|ACCESS_TOKEN_EXPIRE\|additional_claims" \
  apps/backend/modules/auth/security.py
```

---

## Item 4: `modules/auth/models/user.py`

### 🎯 Objetivo

Validar que o modelo de usuário possui todos os campos necessários para autenticação e
permissões.

### ✔️ Critérios de Validação

| Critério                                              | Esperado                        | Status | Observação                                |
| ----------------------------------------------------- | ------------------------------- | ------ | ----------------------------------------- |
| **4.1** ORM `User` possui campo `id`                  | UUID primary key                | [ ]    | Gerado automaticamente                    |
| **4.2** ORM `User` possui campo `email`               | String, unique, indexed         | [ ]    | Para login                                |
| **4.3** ORM `User` possui campo `hashed_password`     | String                          | [ ]    | Nunca armazenar plain                     |
| **4.4** ORM `User` possui campo `level`               | Enum (local/provincial/central) | [ ]    | Hierarquia administrativa                 |
| **4.5** ORM `User` possui campo `scopes`              | 🔴 **CRÍTICO**                  | [ ]    | List ou JSON, valores como "tenant:admin" |
| **4.6** ORM `User` possui campo `role`                | 🔴 **CRÍTICO**                  | [ ]    | Enum ou String para controle              |
| **4.7** ORM `User` possui `is_active`                 | Boolean, default True           | [ ]    | Para desativação lógica                   |
| **4.8** ORM `User` possui `is_superuser`              | Boolean, default False          | [ ]    | Super admin flag                          |
| **4.9** ORM `User` possui `is_verified`               | Boolean                         | [ ]    | Email verification                        |
| **4.10** ORM `User` possui `created_at`, `updated_at` | DateTime, timezone-aware        | [ ]    | Auditoria                                 |
| **4.11** DTO `UserRead` existe                        | Pydantic BaseModel              | [ ]    | Para resposta da API                      |
| **4.12** DTO `UserRead.scopes`                        | `List[str]` em UserRead         | [ ]    | 🔴 CRÍTICO                                |
| **4.13** DTO `UserRead.level`                         | String ou Enum em UserRead      | [ ]    | Compatível com permissions                |

### 🔍 Validação de Código

```python
# ❌ Atual (INCOMPLETO)
class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    level = Column(PgEnum(AdministrativeLevel), nullable=True)
    # ❌ FALTA: scopes, role

# ✅ Esperado
class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    level = Column(PgEnum(AdministrativeLevel), nullable=True)
    scopes = Column(JSON, nullable=False, default=[])  # ✅ NOVO
    role = Column(String, nullable=True)  # ✅ NOVO
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

class UserRead(BaseModel):
    id: str
    email: EmailStr
    scopes: List[str] = []  # ✅ NOVO
    level: Optional[str] = None
    role: Optional[str] = None
```

### 📝 Comando de Auditoria

```bash
grep -n "scopes\|role\|level\|class User\|class UserRead" \
  apps/backend/modules/auth/models/user.py
```

---

# 🧪 Camada 2: Testes do Módulo Antigo

## Item 5: `modules/auth/tests/test_endpoints.py`

### 🎯 Objetivo

Validar que os testes de endpoints cobrem casos de uso críticos de autenticação.

### ✔️ Critérios de Validação

| Critério                                                | Esperado                                | Status | Observação           |
| ------------------------------------------------------- | --------------------------------------- | ------ | -------------------- |
| **5.1** Teste `test_auth_ping()` existe                 | Valida endpoint de healthcheck          | [ ]    | GET /auth/ping → 200 |
| **5.2** Teste `test_login_success()` existe             | Login com credenciais válidas           | [ ]    | Status 200 + tokens  |
| **5.3** Teste `test_login_invalid_credentials()` existe | Login com senha errada                  | [ ]    | Status 401           |
| **5.4** Teste `test_admin_scope_access()` **CRÍTICO**   | User com `tenant:admin` acessa endpoint | [ ]    | 🔴 **ESTE FALHOU**   |
| **5.5** Teste `test_non_admin_scope_denied()`           | User SEM `tenant:admin` é bloqueado     | [ ]    | Status 403           |
| **5.6** Teste `test_level_hierarchy()`                  | User `local` não acessa `central`       | [ ]    | Status 403           |
| **5.7** Teste `test_refresh_token()`                    | Refresh token válido gera novo access   | [ ]    | Status 200           |
| **5.8** Teste `test_expired_token()`                    | Token expirado é rejeitado              | [ ]    | Status 401           |
| **5.9** Cobertura de código                             | >= 85%                                  | [ ]    | Via pytest-cov       |

### 📝 Comando de Auditoria

```bash
grep -n "def test_\|@pytest.mark\|assert.*status_code\|tenant:admin" \
  apps/backend/modules/auth/tests/test_endpoints.py
```

### 🔴 Teste Crítico: `test_admin_scope_access()`

```python
# ✅ Esperado
@pytest.mark.asyncio
async def test_admin_scope_access(async_client: AsyncClient, db_session):
    """Testa acesso de admin ao endpoint protegido com tenant:admin"""

    # 1. Cria usuário com scopes=['tenant:admin']
    user = User(
        email="admin@test.com",
        hashed_password=hash_password("password123"),
        scopes=["tenant:admin"],  # ✅ CRÍTICO
        level=AdministrativeLevel.CENTRAL
    )
    db_session.add(user)
    await db_session.commit()

    # 2. Login
    response = await async_client.post("/login", json={
        "email": "admin@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 3. Acessa endpoint protegido
    response = await async_client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    # ✅ Esperado: 200 (não 403!)
    assert response.status_code == 200
```

---

## Item 6: `modules/auth/tests/test_security.py`

### 🎯 Objetivo

Validar que os testes de JWT cobrem criação, leitura e validação de tokens.

### ✔️ Critérios de Validação

| Critério                                     | Esperado                               | Status | Observação                         |
| -------------------------------------------- | -------------------------------------- | ------ | ---------------------------------- |
| **6.1** Teste `test_create_access_token()`   | Token criado com subject               | [ ]    | Decodificável                      |
| **6.2** Teste `test_decode_access_token()`   | Token decodificado corretamente        | [ ]    | Extrai `sub`                       |
| **6.3** Teste `test_expired_token()`         | Token expirado lança erro              | [ ]    | InvalidTokenError                  |
| **6.4** Teste `test_invalid_signature()`     | Token com secret errado falha          | [ ]    | InvalidTokenError                  |
| **6.5** Teste `test_token_type_validation()` | Access token não funciona como refresh | [ ]    | Type mismatch rejeitado            |
| **6.6** Teste com `additional_claims`        | Claims extras incluídos no token       | [ ]    | Scopes/level no token              |
| **6.7** Teste de secret fallback             | Tenta múltiplas secrets                | [ ]    | Compatibilidade com tokens antigos |

### 📝 Comando de Auditoria

```bash
grep -n "def test_\|@pytest.mark\|create_access_token\|decode_access_token\|InvalidTokenError" \
  apps/backend/modules/auth/tests/test_security.py
```

---

# 🧩 Camada 3: Camada Core de Autenticação

## Item 7: `core/auth.py`

### 🎯 Objetivo

Validar que a camada core injeta serviços de autenticação corretamente.

### ✔️ Critérios de Validação

| Critério                                         | Esperado                                | Status | Observação               |
| ------------------------------------------------ | --------------------------------------- | ------ | ------------------------ |
| **7.1** Função `create_access_token()` delegada  | Chama função de `modules.auth.security` | [ ]    | Re-exporta ou wrapper    |
| **7.2** Função `create_refresh_token()` delegada | Chama função de `modules.auth.security` | [ ]    | Re-exporta ou wrapper    |
| **7.3** Função `decode_access_token()` delegada  | Chama função de `modules.auth.security` | [ ]    | Re-exporta ou wrapper    |
| **7.4** Função `decode_refresh_token()` delegada | Chama função de `modules.auth.security` | [ ]    | Re-exporta ou wrapper    |
| **7.5** `get_current_active_user()` importada    | De `modules.auth.auth_utils`            | [ ]    | Para usar como Depends() |
| **7.6** Sem lógica duplicada                     | Core não reimplementa JWT               | [ ]    | Puro wrapper/injection   |
| **7.7** Imports estão corretos                   | Não há ImportError                      | [ ]    | Caminhos relativos ok    |

### 📝 Comando de Auditoria

```bash
grep -n "from modules.auth\|import.*create_access_token\|import.*get_current_active_user" \
  apps/backend/core/auth.py
```

---

## Item 8: `core/security.py`

### 🎯 Objetivo

Validar que a camada core de security não conflita com o novo módulo de auth.

### ✔️ Critérios de Validação

| Critério                             | Esperado                                | Status | Observação                             |
| ------------------------------------ | --------------------------------------- | ------ | -------------------------------------- |
| **8.1** Arquivo existe               | Pode estar vazio ou com helpers         | [ ]    | Não deve conflitar                     |
| **8.2** Sem duplicação de JWT        | Não reimplementa token creation         | [ ]    | Delegue para auth.security             |
| **8.3** Sem conflict com permissions | Não redefine `requires_scopes`          | [ ]    | Delegue para auth.permissions          |
| **8.4** Helpers de segurança         | Se existente, apenas funções auxiliares | [ ]    | Ex: hash_password(), verify_password() |

### 📝 Comando de Auditoria

```bash
wc -l apps/backend/core/security.py
head -20 apps/backend/core/security.py
```

---

# 🧱 Camada 4: Novo Módulo de Autenticação

## Item 9: `apps/backend/src/sila_auth/__init__.py`

### 🎯 Objetivo

Validar inicialização do módulo (se existir).

### ✔️ Critérios de Validação

| Critério                             | Esperado                                  | Status | Observação                       |
| ------------------------------------ | ----------------------------------------- | ------ | -------------------------------- |
| **9.1** Arquivo `__init__.py` existe | Inicialização do módulo                   | [ ]    | ℹ️ Módulo pode não existir ainda |
| **9.2** Imports principais           | Exporta `AuthService`, `JWTHandler`, etc. | [ ]    | Público da API                   |
| **9.3** Sem ImportError              | Importações resolvem                      | [ ]    | Dependências ok                  |

---

## Item 10: `apps/backend/src/sila_auth/services/auth_service.py`

### 🎯 Objetivo

Validar implementação principal (se existir).

### ✔️ Critérios de Validação

| Critério                             | Esperado             | Status | Observação                     |
| ------------------------------------ | -------------------- | ------ | ------------------------------ |
| **10.1** Classe `AuthService` existe | Serviço central      | [ ]    | ℹ️ Pode estar em modules/auth/ |
| **10.2** Método `authenticate()`     | Valida credenciais   | [ ]    | Retorna User com scopes        |
| **10.3** User object com scopes      | Inclui `user.scopes` | [ ]    | 🔴 CRÍTICO                     |
| **10.4** User object com level       | Inclui `user.level`  | [ ]    | Compatível com permissions     |

---

## Item 11: `apps/backend/src/sila_auth/schemas/user.py`

### 🎯 Objetivo

Validar schema de usuário (se existir).

### ✔️ Critérios de Validação

| Critério                            | Esperado           | Status | Observação                 |
| ----------------------------------- | ------------------ | ------ | -------------------------- |
| **11.1** Schema `UserSchema` existe | Pydantic BaseModel | [ ]    | Para resposta API          |
| **11.2** Campo `scopes`             | `List[str]`        | [ ]    | 🔴 CRÍTICO                 |
| **11.3** Campo `level`              | String ou Enum     | [ ]    | Compatível com permissions |

---

## Item 12: `apps/backend/src/sila_auth/api/v1/endpoints.py`

### 🎯 Objetivo

Validar endpoints finais (se existir).

### ✔️ Critérios de Validação

| Critério                              | Esperado                              | Status | Observação              |
| ------------------------------------- | ------------------------------------- | ------ | ----------------------- |
| **12.1** Endpoints aplicam decorators | `@requires_scopes`, `@requires_level` | [ ]    | Segurança ativa         |
| **12.2** Responses incluem scopes     | DTO tem scopes field                  | [ ]    | Para auditoria frontend |

---

# 🧪 Camada 5: Testes do Novo Módulo

## Item 13: `apps/backend/src/sila_auth/tests/test_admin_scope_access.py`

### 🎯 Objetivo

Espelho do teste crítico, mas para o novo módulo.

### ✔️ Critérios de Validação

| Critério                                        | Esperado                        | Status | Observação                   |
| ----------------------------------------------- | ------------------------------- | ------ | ---------------------------- |
| **13.1** Teste `test_tenant_admin_can_access()` | Admin com `tenant:admin` acessa | [ ]    | 200 OK                       |
| **13.2** Teste `test_non_admin_denied()`        | Usuário sem escopo é bloqueado  | [ ]    | 403 Forbidden                |
| **13.3** Token inclui scopes                    | Payload do JWT contém scopes    | [ ]    | Verificável no decoded token |

---

## Item 14: `apps/backend/src/sila_auth/tests/test_permissions.py`

### 🎯 Objetivo

Validar lógica de permissões (escopos + níveis).

### ✔️ Critérios de Validação

| Critério                                     | Esperado                       | Status | Observação                 |
| -------------------------------------------- | ------------------------------ | ------ | -------------------------- |
| **14.1** Teste `test_requires_scopes_pass()` | Usuário com escopo passa       | [ ]    | Não levanta HTTPException  |
| **14.2** Teste `test_requires_scopes_fail()` | Usuário sem escopo falha       | [ ]    | Levanta HTTPException(403) |
| **14.3** Teste `test_requires_level_pass()`  | Usuário com level >= min passa | [ ]    | Não levanta HTTPException  |
| **14.4** Teste `test_requires_level_fail()`  | Usuário com level < min falha  | [ ]    | Levanta HTTPException(403) |
| **14.5** Teste `test_level_hierarchy()`      | local < provincial < central   | [ ]    | Ordem verificada           |
| **14.6** Cobertura de código                 | >= 90%                         | [ ]    | Via pytest-cov             |

---

# 📊 Camada 6: Relatórios de Onboarding

## Item 15: `reports/onboarding/onboarding_validation_dryrun.json`

### 🎯 Objetivo

Documentar falhas de validação anteriores.

### ✔️ Critérios de Validação

| Critério                                  | Esperado                     | Status | Observação         |
| ----------------------------------------- | ---------------------------- | ------ | ------------------ |
| **15.1** Arquivo existe                   | JSON com histórico de falhas | [ ]    | Baseline da Fase 3 |
| **15.2** Inclui `test_admin_scope_access` | Falha registrada             | [ ]    | Ponto de partida   |
| **15.3** Inclui missing fields            | `scopes`, `role` em User     | [ ]    | Raiz do problema   |

### 📝 Comando de Auditoria

```bash
cat reports/onboarding/onboarding_validation_dryrun.json | jq '.failures[] | .test_name'
```

---

## Item 16: `reports/onboarding/onboarding_migration_dryrun.json`

### 🎯 Objetivo

Documentar como arquivos foram refatorados.

### ✔️ Critérios de Validação

| Critério                           | Esperado                        | Status | Observação          |
| ---------------------------------- | ------------------------------- | ------ | ------------------- |
| **16.1** Arquivo existe            | JSON com mapeamento de migração | [ ]    | Rastreabilidade     |
| **16.2** `permissions.py` incluído | Refatoração documentada         | [ ]    | Versão antes/depois |
| **16.3** `User.py` incluído        | Novos campos mapeados           | [ ]    | Schema evolution    |

---

## Item 17: `reports/onboarding/onboarding_analysis.json`

### 🎯 Objetivo

Análise de impacto e risco da Fase 3.

### ✔️ Critérios de Validação

| Critério                            | Esperado                     | Status | Observação            |
| ----------------------------------- | ---------------------------- | ------ | --------------------- |
| **17.1** Arquivo existe             | JSON com análise estruturada | [ ]    | Risk assessment       |
| **17.2** Risco da Fase 3 = `HIGH`   | Confirmado                   | [ ]    | Muitas dependências   |
| **17.3** Arquivos críticos listados | 17 arquivos mapeados         | [ ]    | Este checklist valida |
| **17.4** Recomendações incluídas    | Ações corretivas             | [ ]    | Roadmap de fix        |

---

# 🎯 Resumo de Auditoria

## Matriz de Risco por Item

| Item                    | Risco    | Status | Bloqueador                         |
| ----------------------- | -------- | ------ | ---------------------------------- |
| 1. permissions.py       | 🔴 ALTO  | ❓     | Sim — sem scopes validation        |
| 2. endpoints.py         | 🟡 MÉDIO | ❓     | Parcial — falta aplicar decorators |
| 3. security.py          | 🟢 BAIXO | ✅     | Não — JWT geração ok               |
| 4. models/user.py       | 🔴 ALTO  | ❓     | Sim — faltam campos scopes/role    |
| 5. test_endpoints.py    | 🔴 ALTO  | ❌     | Sim — teste admin falha            |
| 6. test_security.py     | 🟡 MÉDIO | ❓     | Parcial — falta validar claims     |
| 7. core/auth.py         | 🟡 MÉDIO | ❓     | Não — injection ok                 |
| 8. core/security.py     | 🟢 BAIXO | ✅     | Não — stub inofensivo              |
| 9-12. sila_auth/\*      | 🟢 BAIXO | ℹ️     | Não — módulo pode não existir      |
| 13-14. sila_auth/tests/ | 🟢 BAIXO | ℹ️     | Não — espelho dos testes           |
| 15-17. reports/         | 🟡 MÉDIO | ❓     | Parcial — baseline importante      |

---

## ✅ Próximas Ações

1. **Executar wrapper automático** (Artefato 3) para gerar relatório detalhado
2. **Corrigir Item 4** (`models/user.py`) — adicionar campos `scopes` e `role`
3. **Corrigir Item 1** (`permissions.py`) — garantir validação de `tenant:admin`
4. **Executar Item 5** (`test_endpoints.py`) — verificar se `test_admin_scope_access`
   passa
5. **Validar Itens 6-8** — segurança de tokens
6. **Gerar relatório final** com status de cada item

---

**Fim do Checklist Técnico**
