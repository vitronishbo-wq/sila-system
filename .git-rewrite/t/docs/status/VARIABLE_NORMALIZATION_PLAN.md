# 🔧 Plano de Normalização de Variáveis - SILA System

## Problema Identificado

Existem **inconsistências** entre as variáveis de configuração de base de dados:

### Padrão Atual (Inconsistente)

- ✅ **Variáveis individuais**: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`,
  `POSTGRES_HOST`, `POSTGRES_PORT`
- ✅ **URLs completas**: `DATABASE_URL`, `ASYNC_DATABASE_URL`, `TEST_DATABASE_URL`
- ❌ **Problema**: Alguns ficheiros usam apenas URLs, outros apenas variáveis
  individuais
- ❌ **Duplicação**: Mesma informação em formatos diferentes

## Análise de Uso Atual

### Ficheiros que usam POSTGRES\_\* (variáveis individuais)

- `apps/backend/config/settings.py` - **Preferência**: Constrói URLs a partir de
  variáveis individuais
- `core/config.py` - **Preferência**: Usa variáveis individuais como padrão
- `infrastructure/docker/docker-compose.yml` - **Usa ambos**: URLs e variáveis
  individuais
- Todos os ficheiros `.env*` - **Ambos**: Definem URLs e variáveis individuais

### Ficheiros que usam apenas DATABASE_URL

- `apps/backend/alembic/env.py` - **Apenas URLs**
- `apps/backend/core/database.py` - **Apenas URLs**
- Scripts de teste e CI/CD - **Principalmente URLs**

## 🎯 Estratégia de Normalização Recomendada

### Opção A: **Variáveis Individuais como Fonte da Verdade** (Recomendada)

**Vantagens:**

- ✅ Maior flexibilidade para configuração
- ✅ Mais fácil de debugar (valores individuais visíveis)
- ✅ Melhor para ambientes Docker (variáveis separadas)
- ✅ Compatível com Kubernetes ConfigMaps/Secrets
- ✅ Permite override individual de componentes

**Implementação:**

1. **Manter variáveis individuais** como configuração primária
2. **URLs são geradas automaticamente** a partir das variáveis individuais
3. **Fallback para URLs** se variáveis individuais não estiverem definidas

### Opção B: URLs como Fonte da Verdade

**Desvantagens:**

- ❌ Menos flexível para configuração
- ❌ Mais difícil de debugar
- ❌ Problemas com caracteres especiais em passwords
- ❌ Menos compatível com orquestradores

## 📋 Plano de Implementação (Opção A)

### Fase 1: Atualizar Settings Classes

```python
# apps/backend/config/settings.py
class Settings(BaseSettings):
    # Variáveis individuais (fonte da verdade)
    POSTGRES_USER: str = Field(default="sila_user")
    POSTGRES_PASSWORD: str = Field(default="change_me")
    POSTGRES_DB: str = Field(default="sila_db")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)

    # URLs opcionais (para override manual)
    DATABASE_URL: Optional[str] = Field(default=None)
    ASYNC_DATABASE_URL: Optional[str] = Field(default=None)

    @property
    def get_database_url(self) -> str:
        """Retorna DATABASE_URL ou constrói a partir de variáveis individuais"""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        user_encoded = quote_plus(self.POSTGRES_USER)
        password_encoded = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{user_encoded}:{password_encoded}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def get_async_database_url(self) -> str:
        """Retorna ASYNC_DATABASE_URL ou constrói a partir de variáveis individuais"""
        if self.ASYNC_DATABASE_URL:
            return self.ASYNC_DATABASE_URL

        return self.get_database_url.replace("postgresql://", "postgresql+asyncpg://")
```

### Fase 2: Atualizar Ficheiros .env

```bash
# Prioridade: Variáveis individuais
POSTGRES_USER=sila_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=sila_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# URLs opcionais (apenas se necessário override)
# DATABASE_URL=postgresql://custom_user:custom_pass@custom_host:5432/custom_db
# ASYNC_DATABASE_URL=postgresql+asyncpg://custom_user:custom_pass@custom_host:5432/custom_db
```

### Fase 3: Atualizar Docker Compose

```yaml
services:
  backend:
    environment:
      # Usar variáveis individuais
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_HOST=${POSTGRES_HOST}
      - POSTGRES_PORT=${POSTGRES_PORT}
      # URLs opcionais para override
      - DATABASE_URL=${DATABASE_URL:-}
      - ASYNC_DATABASE_URL=${ASYNC_DATABASE_URL:-}

  db:
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

### Fase 4: Atualizar Código de Aplicação

```python
# apps/backend/core/database.py
from apps.backend.config.settings import get_settings

settings = get_settings()

# Usar método que prioriza variáveis individuais
DATABASE_URL = settings.get_database_url
ASYNC_DATABASE_URL = settings.get_async_database_url
```

## 🔄 Migração Gradual

### Etapa 1: Preparação (Sem Breaking Changes)

- [x] Criar novos ficheiros `.env.development` e `.env.production` com ambos os formatos
- [x] Atualizar `settings.py` para suportar ambos os métodos
- [ ] Adicionar métodos `get_database_url()` e `get_async_database_url()`

### Etapa 2: Transição

- [ ] Atualizar `core/database.py` para usar novos métodos
- [ ] Atualizar `alembic/env.py` para usar variáveis individuais
- [ ] Atualizar scripts de teste

### Etapa 3: Limpeza

- [ ] Remover URLs hardcoded dos ficheiros `.env`
- [ ] Manter URLs apenas como override opcional
- [ ] Documentar nova convenção

## 🧪 Testes de Validação

```python
def test_database_url_priority():
    """Testar prioridade: URL manual > variáveis individuais"""

    # Caso 1: Apenas variáveis individuais
    settings = Settings(
        POSTGRES_USER="user1",
        POSTGRES_PASSWORD="pass1",
        POSTGRES_HOST="host1",
        POSTGRES_PORT=5432,
        POSTGRES_DB="db1"
    )
    assert "user1:pass1@host1:5432/db1" in settings.get_database_url

    # Caso 2: URL manual override
    settings = Settings(
        POSTGRES_USER="user1",
        DATABASE_URL="postgresql://user2:pass2@host2:5432/db2"
    )
    assert settings.get_database_url == "postgresql://user2:pass2@host2:5432/db2"
```

## 📊 Impacto da Mudança

### Benefícios

- ✅ **Consistência**: Uma única fonte da verdade
- ✅ **Flexibilidade**: Fácil configuração por ambiente
- ✅ **Debuggabilidade**: Variáveis individuais visíveis
- ✅ **Compatibilidade**: Funciona com Docker, K8s, etc.

### Riscos

- ⚠️ **Mudança de comportamento**: Código que depende de URLs específicas
- ⚠️ **Testes**: Podem precisar de atualização
- ⚠️ **Documentação**: Precisa ser atualizada

## 🚀 Próximos Passos

1. **Implementar Fase 1**: Atualizar `settings.py` com métodos híbridos
2. **Testar**: Validar que ambos os métodos funcionam
3. **Migrar gradualmente**: Atualizar ficheiros um por um
4. **Documentar**: Atualizar README e documentação
5. **Limpar**: Remover código obsoleto após migração completa

---

**Status**: 📋 Plano criado - Aguardando aprovação para implementação
