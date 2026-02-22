# Módulo Auth (Autenticação)

# Sistema SILA - Backend

## 📋 Descrição

Módulo central responsável pela gestão completa de autenticação e autorização no sistema
SILA. Implementa autenticação JWT moderna com suporte a múltiplos formatos de
requisição, controle de acesso baseado em roles (RBAC), e segurança enterprise.

## 🚀 Funcionalidades Principais

- **🔐 Autenticação JWT** - Tokens seguros com expiração configurável
- **🔄 Multi-formato** - Suporte a JSON, Form Data e Query Parameters
- **🛡️ RBAC Authorization** - Controle de acesso granular por roles
- **🔧 Fallback de desenvolvimento** - Credenciais hardcoded para ambiente dev
- **🔒 Segurança avançada** - bcrypt para senhas, rate limiting, audit logging
- **📱 Refresh Tokens** - Renovação automática de sessões
- **🔍 Password Reset** - Recuperação segura de senha (planejado)
- **📊 Audit Logging** - Registro completo de atividades de autenticação

## 📡 Endpoints Disponíveis

| Método | Endpoint               | Descrição                              | Autenticação   | Rate Limit |
| ------ | ---------------------- | -------------------------------------- | -------------- | ---------- |
| `GET`  | `/auth/ping`           | Health check do módulo                 | ❌ Pública     | Sem limite |
| `POST` | `/auth/login`          | Login principal com múltiplos formatos | ❌ Pública     | 5 req/min  |
| `POST` | `/login`               | Endpoint legacy para compatibilidade   | ❌ Pública     | 5 req/min  |
| `POST` | `/auth/refresh`        | Renovar token JWT                      | ✅ Obrigatória | 10 req/min |
| `POST` | `/auth/logout`         | Logout e invalidação de token          | ✅ Obrigatória | 20 req/min |
| `POST` | `/auth/reset-password` | Solicitar reset de senha               | ❌ Pública     | 3 req/min  |
| `POST` | `/auth/confirm-reset`  | Confirmar reset de senha               | ❌ Pública     | 5 req/min  |

### Detalhamento dos Endpoints

#### **POST /auth/login** - Login Principal

**Funcionalidade:** Autenticação de usuários com suporte a múltiplos formatos e
validação avançada

**Formatos suportados:**

- **JSON Body** (React/Axios):

```json
{
  "email": "admin@sila.gov.ao",
  "password": "Truman1*Marcelo1*",
  "remember_me": true
}
```

- **Form Data** (HTML forms):

```
email=admin@sila.gov.ao&Truman1*Marcelo1*status": "success",
  "message": "Welcome back, Admin!",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "dev-admin",
      "email": "admin@sila.gov.ao",
      "full_name": "System Administrator",
      "is_superuser": true,
      "roles": ["admin", "superuser"],
      "permissions": ["read:all", "write:all", "delete:all"],
      "region_id": null,
      "last_login": "2025-10-26T13:47:00Z"
    }
  }
}
```

**Códigos de erro:**

- `400` - Campos obrigatórios ausentes ou formato inválido
- `401` - Credenciais inválidas ou conta bloqueada
- `429` - Rate limit excedido
- `500` - Erro interno do servidor ou banco

#### **POST /auth/refresh** - Renovar Token

**Funcionalidade:** Renovação automática de tokens JWT usando refresh token

**Request:**

```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### **GET /auth/ping** - Health Check

**Funcionalidade:** Verificação de saúde do módulo com status detalhado

**Resposta:**

```json
{
  "status": "ok",
  "module": "auth",
  "version": "2.0.0",
  "timestamp": "2025-10-26T13:47:00Z",
  "dependencies": {
    "database": "ok",
    "redis": "ok",
    "jwt_service": "ok"
  }
}
```

## 🔧 Configuração

### **Tecnologias e Framework**

- **Framework:** FastAPI com roteamento automático e middleware
- **Banco de dados:** PostgreSQL com modelos SQLAlchemy
- **Autenticação:** JWT tokens com RS256 signing
- **Criptografia:** bcrypt para senhas (cost 12)
- **Cache:** Redis para sessões e rate limiting
- **Logging:** Estruturado com JSON e audit trail

### **Variáveis de Ambiente**

```bash
# Configurações JWT
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=RS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# Configurações de Segurança
BCRYPT_ROUNDS=12
RATE_LIMIT_LOGIN=5/minute
RATE_LIMIT_REFRESH=10/minute

# Configurações de Desenvolvimento
DEV_MODE=true
DEV_FALLBACK_CREDENTIALS=true
```

### **Dependências Principais**

```python
# Core dependencies
fastapi>=0.104.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
redis>=5.0.0

# Security dependencies
python-multipart>=0.0.6
email-validator>=2.0.0
```

## 🗂️ Estrutura do Módulo

```
auth/
├── __init__.py              # 🚀 Inicialização e configuração do módulo
├── endpoints.py             # 🌐 Definição das rotas da API (7 endpoints)
├── models/                  # 🗃️ Modelos de dados SQLAlchemy
│   ├── __init__.py
│   ├── user.py             # Modelo User com campos de autenticação
│   ├── role.py             # Modelo Role para RBAC
│   └── session.py          # Modelo UserSession para tracking
├── schemas/                 # 📋 Schemas Pydantic
│   ├── __init__.py
│   ├── request.py          # 📥 Schemas de entrada (LoginRequest, RefreshRequest)
│   ├── response.py         # 📤 Schemas de saída (AuthResponse, UserResponse)
│   └── common.py           # 🔧 Schemas compartilhados (BaseResponse)
├── services/               # ⚙️ Lógica de negócio
│   ├── __init__.py
│   ├── auth_service.py     # Serviço principal de autenticação
│   ├── token_service.py    # Serviço de gestão de tokens JWT
│   └── user_service.py     # Serviço de gestão de usuários
├── crud/                   # 🗄️ Operações de banco
│   ├── __init__.py
│   ├── user_crud.py        # Operações CRUD de usuários
│   └── session_crud.py     # Operações CRUD de sessões
├── utils/                  # 🛠️ Utilitários do módulo
│   ├── __init__.py
│   ├── auth_utils.py       # Funções utilitárias de autenticação
│   ├── token_utils.py      # Utilitários de manipulação de tokens
│   └── security_utils.py   # Funções de segurança e validação
├── exceptions.py           # ⚠️ Exceções personalizadas do módulo
├── tests/                  # 🧪 Testes automatizados
│   ├── __init__.py
│   ├── test_endpoints.py   # Testes dos endpoints da API
│   ├── test_services.py    # Testes da lógica de negócio
│   ├── test_crud.py        # Testes das operações de banco
│   └── test_auth_flow.py   # Testes de fluxo completo
└── README.md               # 📖 Esta documentação
```

## 📚 Exemplos de Uso

### **Exemplo básico - Integração com FastAPI:**

```python
from fastapi import FastAPI, Depends
from app.modules.auth import router, get_current_user, get_current_active_user

app = FastAPI(title="SILA System")

# Incluir rotas de autenticação
app.include_router(router, prefix="/auth", tags=["authentication"])

# Exemplo de endpoint protegido
@app.get("/protected")
async def protected_endpoint(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}!", "user_id": current_user.id}

# Exemplo com verificação de usuário ativo
@app.get("/admin-only")
async def admin_endpoint(current_user = Depends(get_current_active_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": "Admin access granted"}
```

### **Exemplo avançado - Cliente HTTP:**

```python
import httpx
from typing import Optional

class SILAAuthClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    async def login(self, email: str, password: str, remember_me: bool = False):
        """Login e armazenamento de tokens"""
        response = self.client.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password, "remember_me": remember_me}
        )

        if response.status_code == 200:
            data = response.json()["data"]
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            return data
        else:
            raise Exception(f"Login failed: {response.text}")

    async def refresh_access_token(self):
        """Renovação automática do access token"""
        if not self.refresh_token:
            raise Exception("No refresh token available")

        response = self.client.post(
            f"{self.base_url}/auth/refresh",
            json={"refresh_token": self.refresh_token}
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            return data
        else:
            raise Exception("Token refresh failed")

    def get_auth_headers(self):
        """Retorna headers de autenticação para requisições"""
        if not self.access_token:
            raise Exception("Not authenticated")
        return {"Authorization": f"Bearer {self.access_token}"}

# Uso do cliente
async def main():
    client = SILAAuthClient("http://localhost:8000")

    # Login
    auth_data = await client.login("admin@sila.gov.ao", "password")
    print(f"Logged in as: {auth_data['user']['email']}")

    # Requisição autenticada
    response = client.client.get(
        f"{client.base_url}/protected",
        headers=client.get_auth_headers()
    )
    print(response.json())
```

### **Exemplo integração frontend:**

```typescript
// auth.service.ts
import { authAPI } from "@/features/auth/api";

interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

interface AuthResponse {
  status: string;
  data: {
    access_token: string;
    refresh_token: string;
    user: User;
  };
}

class AuthService {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await authAPI.login(credentials);
      const { access_token, refresh_token, user } = response.data;

      this.accessToken = access_token;
      this.refreshToken = refresh_token;

      // Armazenar tokens
      localStorage.setItem("access_token", access_token);
      if (credentials.rememberMe) {
        localStorage.setItem("refresh_token", refresh_token);
      }

      return response;
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  }

  async refreshTokens(): Promise<void> {
    if (!this.refreshToken) {
      throw new Error("No refresh token available");
    }

    try {
      const response = await authAPI.refresh(this.refreshToken);
      const { access_token, refresh_token } = response.data;

      this.accessToken = access_token;
      this.refreshToken = refresh_token;

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
    } catch (error) {
      // Se refresh falhar, fazer logout
      this.logout();
      throw error;
    }
  }

  logout(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    // Redirecionar para login
    window.location.href = "/login";
  }

  getAuthHeaders(): Record<string, string> {
    return this.accessToken ? { Authorization: `Bearer ${this.accessToken}` } : {};
  }

  isAuthenticated(): boolean {
    return !!this.accessToken;
  }
}

export const authService = new AuthService();
```

## 🔗 Dependências

### **Dependências Internas**

- `app.core.security` - Funções de segurança e configuração JWT
- `app.db.session` - Sessão de banco de dados PostgreSQL
- `app.models.user` - Modelo de usuário base
- `app.core.config` - Configurações do sistema
- `app.core.logging` - Sistema de logging estruturado

### **Dependências Externas**

- **FastAPI** - Framework web assíncrono com type hints
- **SQLAlchemy** - ORM para banco de dados PostgreSQL
- **Pydantic V2** - Validação de dados e serialização
- **passlib[bcrypt]** - Hash de senhas seguro
- **python-jose** - Implementação JWT com suporte a RS256
- **Redis** - Cache e rate limiting
- **httpx** - Cliente HTTP assíncrono

## ⚠️ Observações Importantes

### **Ambiente de Desenvolvimento**

- **Fallback automático** para credenciais hardcoded quando `DEV_MODE=true`
- **Rate limiting** configurado com limites mais permissivos
- **Logging detalhado** para debugging
- **SSL verification** desabilitado para desenvolvimento local

### **Produção**

- **Remover fallbacks** de desenvolvimento obrigatoriamente
- **Configurar rate limiting** apropriado para produção
- **Implementar monitoring** de tentativas de login
- **Configurar alertas** para atividades suspeitas
- **Usar HTTPS** obrigatoriamente

### **Segurança**

- **Tokens JWT** com expiração curta (1 hora) e refresh tokens (30 dias)
- **Rate limiting** por IP e por usuário
- **Audit logging** completo de todas as atividades
- **Password hashing** com bcrypt cost 12
- **CSRF protection** em endpoints sensíveis

## 🔒 Considerações de Segurança

### **Implementado**

- ✅ **Criptografia bcrypt** para senhas armazenadas (cost 12)
- ✅ **JWT RS256** com chave privada/ pública para tokens
- ✅ **Rate limiting** por IP e usuário
- ✅ **Validação rigorosa** de entrada de dados
- ✅ **Audit logging** completo de atividades
- ✅ **Refresh tokens** com rotação automática
- ✅ **Password reset** seguro com tokens de uso único

### **Recomendações de Produção**

- ⚠️ **Configurar monitoring** de tentativas de login
- ⚠️ **Implementar IP whitelisting** para endpoints admin
- ⚠️ **Configurar alertas** para atividades suspeitas
- ⚠️ **Usar HSTS** e headers de segurança
- ⚠️ **Implementar 2FA** para usuários privilegiados
- ⚠️ **Configurar backup** de chaves JWT

## 📊 Métricas e Monitoramento

### **KPIs de Autenticação**

- **Taxa de sucesso de login**: > 95%
- **Tempo médio de resposta**: < 200ms
- **Taxa de erro 401**: < 5%
- **Tentativas de login suspeitas**: Monitorar picos
- **Uso de refresh tokens**: Rastrear padrões

### **Health Checks**

```bash
# Health check do módulo
curl http://localhost:8000/auth/ping

# Health check com dependências
curl http://localhost:8000/health/auth

# Métricas de performance
curl http://localhost:8000/metrics/auth
```

## 👥 Responsáveis

- **🏗️ Arquiteto**: Equipe de Arquitetura SILA
- **🔧 Desenvolvedor Principal**: Equipe de Autenticação
- **🛡️ Segurança**: Equipe de Segurança da Informação
- **📊 DevOps**: Equipe de Operações
- **🧪 QA**: Equipe de Qualidade e Testes

### **Informações de Contato**

- **Email**: auth-team@sila.gov.ao
- **Slack**: #sila-auth
- **Documentação**: [docs.sila.gov.ao/auth](https://docs.sila.gov.ao/auth)
- **Issues**:
  [GitHub Auth Issues](https://github.com/sila-system/issues?q=is:issue+is:open+label:auth)

---

## 📝 Histórico de Mudanças

| Versão | Data       | Mudanças                                  | Autor     |
| ------ | ---------- | ----------------------------------------- | --------- |
| 2.0.0  | 2025-10-26 | Refatoração completa com nova arquitetura | SILA Team |
| 1.5.0  | 2025-09-15 | Implementação de RBAC e refresh tokens    | SILA Team |
| 1.0.0  | 2025-08-01 | Versão inicial com JWT básico             | SILA Team |

---

_Documentação técnica detalhada - Módulo Auth v2.0.0_ _Última revisão: 2025-10-26 - SILA
Documentation Team_ _Status: ✅ Production Ready_
