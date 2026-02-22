# Módulo de Autenticação e Autorização - SILA System

Este documento descreve o sistema de autenticação e autorização implementado no SILA
System, seguindo as melhores práticas de segurança.

## Visão Geral

O sistema de autenticação utiliza:

- **JWT (JSON Web Tokens)** para autenticação stateless
- **Refresh Tokens** para renovação segura de tokens
- **RBAC (Role-Based Access Control)** para autorização
- **Middleware de segurança** para proteção de rotas

## Arquitetura

### Modelos (Models)

#### User

```python
class User(Base):
    id: UUID (Primary Key)
    email: str (Unique, Indexed)
    username: str (Optional, Unique)
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    full_name: str
    phone_number: str
    role_id: int (Foreign Key)
    last_login: datetime
    failed_login_attempts: int
    locked_until: datetime
    # ... outros campos
```

#### Role

```python
class Role(Base):
    id: int (Primary Key)
    name: str (Unique)
    description: str
    is_default: bool
    # Relacionamentos com User e Permission
```

#### Permission

```python
class Permission(Base):
    id: int (Primary Key)
    name: str (Unique)
    description: str
    # Relacionamentos com Role e User
```

#### RefreshToken

```python
class RefreshToken(Base):
    id: int (Primary Key)
    token: str (Unique)
    user_id: UUID (Foreign Key)
    expires_at: datetime
    created_at: datetime
    revoked: bool
    revoked_at: datetime
    replaced_by: str
```

### Relacionamentos

- **User ↔ Role**: Many-to-One (um usuário tem um role)
- **User ↔ Permission**: Many-to-Many (usuários podem ter permissões diretas)
- **Role ↔ Permission**: Many-to-Many (roles têm múltiplas permissões)
- **User ↔ RefreshToken**: One-to-Many (um usuário pode ter múltiplos refresh tokens)

## Endpoints de Autenticação

### POST /api/v1/auth/login/access-token

**Descrição**: Autenticação com email/senha e obtenção de tokens

**Request**:

```json
{
  "username": "user@example.com",
  "password": "senha123"
}
```

**Response**:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "refresh_token": "refresh_token_here"
}
```

### POST /api/v1/auth/refresh

**Descrição**: Renovação de access token usando refresh token

**Request**:

```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response**:

```json
{
  "access_token": "new_access_token",
  "token_type": "bearer",
  "refresh_token": "new_refresh_token"
}
```

### POST /api/v1/auth/logout

**Descrição**: Logout revogando o refresh token

**Request**:

```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response**:

```json
{
  "message": "Successfully logged out"
}
```

### POST /api/v1/auth/register

**Descrição**: Registro de novo usuário

**Request**:

```json
{
  "email": "newuser@example.com",
  "name": "New User",
  "password": "SecurePassword123!@#",
  "role": "user",
  "user_type": "citizen"
}
```

**Response**:

```json
{
  "id": 1,
  "email": "newuser@example.com",
  "name": "New User",
  "role": "user",
  "user_type": "citizen",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### POST /api/v1/auth/logout-all

**Descrição**: Logout de todos os dispositivos (revoga todos os refresh tokens)

**Headers**: `Authorization: Bearer <access_token>`

**Response**:

```json
{
  "message": "Successfully logged out from 3 devices",
  "devices_logged_out": 3
}
```

### POST /api/v1/auth/login/test-token

**Descrição**: Teste de validade do access token

**Headers**: `Authorization: Bearer <access_token>`

**Response**: Dados do usuário autenticado

## Segurança

### Configuração de Tokens

- **Access Token**: Expira em 30 minutos (configurável)
- **Refresh Token**: Expira em 30 dias (configurável)
- **Algoritmo**: HS256
- **Formato**: JWT com claims personalizados

### Middleware de Autenticação

O sistema utiliza `OAuth2PasswordBearer` para extrair tokens do header `Authorization`:

```
Authorization: Bearer <access_token>
```

### Decoradores de Autorização

#### @require_role(role_name)

```python
@require_role("admin")
async def admin_only_endpoint(current_user: User = Depends(get_current_user)):
    # Apenas usuários com role "admin" podem acessar
    pass
```

#### @require_scope(scope)

```python
@require_scope("national")
async def national_endpoint(current_user: User = Depends(get_current_user)):
    # Apenas usuários com escopo "national" podem acessar
    pass
```

#### @require_permission(permission)

```python
@require_permission("users:write")
async def write_users_endpoint(current_user: User = Depends(get_current_user)):
    # Apenas usuários com permissão "users:write" podem acessar
    pass
```

### Escopos de Usuário

- **national**: Acesso a nível nacional
- **province**: Acesso a nível provincial
- **municipality**: Acesso a nível municipal (padrão)

## Serviços

### AuthService

Centraliza toda a lógica de autenticação:

```python
class AuthService:
    @classmethod
    async def authenticate(cls, db, email, password) -> Optional[User]

    @classmethod
    def create_access_token(cls, user_id, expires_delta=None) -> str

    @classmethod
    async def create_refresh_token(cls, db, user_id, expires_delta=None) -> str

    @classmethod
    async def revoke_refresh_token(cls, db, token) -> bool

    @classmethod
    async def revoke_all_user_tokens(cls, db, user_id) -> int

    @classmethod
    async def verify_refresh_token(cls, db, token) -> Optional[User]

    @classmethod
    async def refresh_access_token(cls, db, refresh_token) -> RefreshTokenResponse
```

## Dependências

### Python

- `python-jose[cryptography]`: Para JWT
- `passlib[bcrypt]`: Para hash de senhas
- `bcrypt`: Para criptografia de senhas

### Instalação

```bash
pip install python-jose[cryptography] passlib[bcrypt] bcrypt
```

## Fluxos de Autenticação

### 1. Login

```mermaid
sequenceDiagram
    participant C as Client
    participant A as AuthService
    participant D as Database

    C->>A: POST /auth/login (email, password)
    A->>D: Verify credentials
    D-->>A: User data
    A->>A: Generate access token
    A->>D: Store refresh token
    A-->>C: Access + Refresh tokens
```

### 2. Token Refresh

```mermaid
sequenceDiagram
    participant C as Client
    participant A as AuthService
    participant D as Database

    C->>A: POST /auth/refresh (refresh_token)
    A->>D: Verify refresh token
    D-->>A: Token valid
    A->>D: Revoke old refresh token
    A->>A: Generate new access token
    A->>D: Store new refresh token
    A-->>C: New tokens
```

### 3. Logout

```mermaid
sequenceDiagram
    participant C as Client
    participant A as AuthService
    participant D as Database

    C->>A: POST /auth/logout (refresh_token)
    A->>D: Revoke refresh token
    D-->>A: Token revoked
    A-->>C: Success message
```

## Testes

O módulo inclui testes abrangentes:

```bash
# Executar testes de autenticação
pytest tests/test_auth.py -v

# Executar testes com cobertura
pytest tests/test_auth.py --cov=app.services.auth_service --cov=app.api.v1.endpoints.auth
```

### Casos de Teste

- ✅ Login válido/inválido
- ✅ Refresh token válido/inválido
- ✅ Acesso a rota protegida com/sem token
- ✅ Registro de usuário
- ✅ Logout individual e de todos os dispositivos
- ✅ Verificação de permissões e roles

## Configuração

### Variáveis de Ambiente

```bash
# Configuração de tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Segurança
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Banco de dados
ASYNC_DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
```

### Configuração de Produção

1. **SECRET_KEY**: Use uma chave segura e única
2. **HTTPS**: Sempre use HTTPS em produção
3. **Rate Limiting**: Implemente rate limiting para endpoints de auth
4. **Logs**: Configure logs de segurança para auditoria
5. **Backup**: Faça backup regular dos refresh tokens

## Troubleshooting

### Problemas Comuns

1. **Token expirado**: Use refresh token para obter novo access token
2. **Refresh token inválido**: Usuário deve fazer login novamente
3. **Permissão negada**: Verificar roles e permissões do usuário
4. **Erro de conexão**: Verificar configuração do banco de dados

### Logs de Debug

```python
import logging
logging.getLogger("app.services.auth_service").setLevel(logging.DEBUG)
```

## Roadmap

- [ ] Implementar 2FA (Two-Factor Authentication)
- [ ] Adicionar rate limiting
- [ ] Implementar blacklist de tokens
- [ ] Adicionar auditoria de segurança
- [ ] Implementar SSO (Single Sign-On)
- [ ] Adicionar suporte a OAuth2 providers

## Contribuição

Para contribuir com o módulo de autenticação:

1. Siga as convenções de código existentes
2. Adicione testes para novas funcionalidades
3. Atualize a documentação
4. Verifique a segurança das implementações
5. Execute todos os testes antes de submeter

## Licença

Este módulo faz parte do SILA System e está sujeito à licença do projeto principal.
