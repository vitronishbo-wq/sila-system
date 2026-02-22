# 🧪 SILA Backend - Suíte de Testes Automatizados

## 📋 Visão Geral

Suíte completa de testes automatizados para o SILA Backend utilizando **pytest**,
**httpx**, **pydantic** e **jsonschema**. Inclui testes para endpoints principais,
validação de schemas e verificação de todos os módulos do sistema.

## 🛠️ Tecnologias Utilizadas

- **pytest**: Framework de testes principal
- **httpx**: Cliente HTTP assíncrono/síncrono para testes de API
- **pydantic**: Validação de schemas de resposta
- **jsonschema**: Validação adicional de schemas
- **pytest-asyncio**: Suporte a testes assíncronos
- **pytest-cov**: Relatórios de cobertura de código

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py                 # Inicialização do pacote
├── conftest.py                 # Fixtures e configurações compartilhadas
├── test_main_endpoints.py      # Testes dos endpoints principais
├── test_modules_ping.py        # Testes de ping dos módulos
└── README.md                   # Este arquivo
```

## 🚀 Começando Rápido

### 1. Iniciar o Servidor de Testes

```bash
# Opção 1: Script automatizado (recomendado)
cd /opt/sila-system/backend
python start_test_server.py

# Opção 2: Manualmente
cd /opt/sila-system/backend
uvicorn main:app --host 0.0.0.0 --port 8003
```

### 2. Executar Testes Rápidos (Smoke Tests)

```bash
# Script automatizado
python run_tests.py --type smoke

# Ou diretamente com pytest
python -m pytest tests/test_main_endpoints.py::TestMainEndpoints::test_health_endpoint_sync -v
```

## 📊 Tipos de Testes Disponíveis

### 🔥 Smoke Tests (Verificação Básica)

Testes rápidos para verificar se o sistema está funcional:

```bash
python run_tests.py --type smoke
```

**Endpoints testados:**

- ✅ `/health` - Verificação de saúde do sistema
- ✅ `/ping` - Conectividade básica
- ⚡ Tempo de resposta < 2s

### 🌐 Endpoints Principais

Testes completos dos endpoints principais da API:

```bash
python run_tests.py --type endpoints
```

**Endpoints testados:**

- ✅ `/health` - Validação completa com Pydantic + JSON Schema
- ✅ `/ping` - Schema validation e consistência
- ✅ `/info` - Informações do sistema e database
- ✅ `/` - Endpoint raiz
- ✅ `/docs` - Swagger UI
- ✅ `/redoc` - ReDoc documentation
- ✅ `/openapi.json` - OpenAPI schema
- 🔒 CORS headers
- ⚡ Performance e tempo de resposta

### 📦 Módulos do Sistema

Testes de ping para todos os 27 módulos do SILA Backend:

```bash
python run_tests.py --type modules
```

**Módulos funcionais testados (15):**

- ✅ `urbanism`, `justice`, `commercial`, `education`, `address`
- ✅ `registry`, `reports`, `identity`, `social`, `common`
- ✅ `governance`, `journeys`, `services`, `training`, `internal`

**Módulos com problemas conhecidos (12):**

- ⚠️ `auth`, `dashboard`, `health`, `documents`, `notifications`
- ⚠️ `analytics`, `citizenship`, `monitoring`, `finance`, `payment`
- ⚠️ `complaints`, `location`

### 📈 Cobertura de Código

Relatórios detalhados de cobertura de código:

```bash
python run_tests.py --type coverage
```

**Resultados gerados:**

- 📊 Terminal com cobertura
- 🌐 HTML (`htmlcov/index.html`)
- 📄 XML (`coverage.xml`)

### ⚡ Performance Tests

Testes de performance e tempo de resposta:

```bash
python run_tests.py --type performance
```

**Métricas avaliadas:**

- ⏱️ Tempo de resposta < 2s para endpoints principais
- 🏃 Teste concorrente de módulos
- 📊 Análise de lentidão

### 🔍 Suite Completa

Executar todos os testes com relatórios:

```bash
python run_tests.py --type full
```

## 🛠️ Opções de Execução

### Script `run_tests.py`

```bash
# Uso básico
python run_tests.py --type smoke

# Opções disponíveis
python run_tests.py [OPÇÕES]

OPÇÕES:
  --type {smoke,full,endpoints,modules,coverage,performance}
    Tipo de teste a ser executado (default: smoke)

  --port PORT
    Porta do servidor a ser testada (default: 8003)

  --verbose, -v
    Saída detalhada dos testes

  --skip-server-check
    Pular verificação de servidor rodando
```

### Script `start_test_server.py`

```bash
# Iniciar servidor padrão
python start_test_server.py

# Opções disponíveis
python start_test_server.py [OPÇÕES]

OPÇÕES:
  --port, -p PORT
    Porta do servidor (default: 8003)

  --log-level, -l {debug,info,warning,error}
    Nível de log (default: info)

  --no-kill
    Não matar processos existentes na porta

  --wait-only
    Apenas aguardar servidor ficar pronto
```

## 📊 Fixtures e Configurações

### Fixtures Disponíveis no `conftest.py`

```python
@pytest.fixture
def client() -> httpx.Client:
    """Cliente HTTP síncrono para testes"""

@pytest.fixture
async def async_client() -> httpx.AsyncClient:
    """Cliente HTTP assíncrono para testes"""

@pytest.fixture
def base_url() -> str:
    """URL base da API para testes"""

@pytest.fixture
def test_settings() -> dict:
    """Configurações de teste (timeouts, tentativas, etc.)"""

@pytest.fixture
def sample_ping_response() -> dict:
    """Resposta de exemplo para /ping"""

@pytest.fixture
def sample_health_response() -> dict:
    """Resposta de exemplo para /health"""

@pytest.fixture
def working_modules() -> List[str]:
    """Lista dos 15 módulos funcionais"""
```

## 🔍 Validações Implementadas

### Pydantic Schemas

```python
class PingResponseSchema(BaseModel):
    status: str
    message: str
    timestamp: str
    service: str

class HealthResponseSchema(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    timestamp: str

class InfoResponseSchema(BaseModel):
    system: dict
    database: dict
    features: dict
```

### JSON Schema Validation

- ✅ Validação de estrutura e tipos
- ✅ Verificação de campos obrigatórios
- ✅ Validação de valores permitidos
- ✅ Suporte a propriedades adicionais

## 📈 Relatórios e Resultados

### Saída de Testes

```
🧪 SILA Backend - Suíte de Testes Automatizados
============================================================
🔍 Verificando servidor na porta 8003...
✅ Servidor está rodando na porta 8003

🚀 Testes de Fumaça (Smoke Tests)
📝 Comando: python -m pytest tests/test_main_endpoints.py::TestMainEndpoints::test_health_endpoint_sync tests/test_main_endpoints.py::TestMainEndpoints::test_ping_endpoint -m not slow -v -s
------------------------------------------------------------
============================= test session starts ==============================
...
✅ 2 passed in 1.23s

============================================================
✅ Todos os testes passaram com sucesso!
```

### Relatório de Cobertura

```
Name                              Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
backend/core/config.py              185     45    76%   120-145
backend/main.py                     234     89    62%   67-120
...
TOTAL                              1245    389    69%

📊 Relatório de cobertura gerado: htmlcov/index.html
```

## 🎯 Marcadores (Markers)

```python
@pytest.mark.slow          # Testes lentos
@pytest.mark.integration   # Testes de integração
@pytest.mark.unit         # Testes unitários
@pytest.mark.api          # Testes de API
@pytest.mark.smoke        # Testes de fumaça
@pytest.mark.regression   # Testes de regressão
@pytest.mark.modules      # Testes específicos para módulos
@pytest.mark.health       # Testes de health check
@pytest.mark.performance  # Testes de performance
```

## 🔧 Configuração do Pytest

Arquivo `pytest.ini` com configurações otimizadas:

```ini
[tool:pytest]
testpaths = tests
addopts = --strict-markers --verbose --tb=short --cov=backend
markers =
    slow: testes lentos
    api: testes de API
    modules: testes de módulos
    performance: testes de performance
```

## 🚨 Códigos de Saída

- **0**: ✅ Todos os testes passaram
- **1**: ❌ Alguns testes falharam
- **2**: ❌ Erro de execução dos testes

## 🐛 Troubleshooting

### Servidor Não Está Rodando

```bash
❌ Servidor não está rodando na porta 8003
💡 Inicie o servidor com:
   cd /opt/sila-system/backend && uvicorn main:app --host 0.0.0.0 --port 8003
```

**Solução:**

```bash
python start_test_server.py
```

### Timeout em Testes

```bash
❌ Timeout ao testar módulo auth
```

**Solução:** Aumentar timeout ou verificar módulo específico.

### Erros de Importação

```bash
❌ ImportError: cannot import name 'app'
```

**Solução:** Verificar PYTHONPATH e ambiente virtual.

## 📝 Exemplos de Uso

### Testar Endpoint Específico

```bash
python -m pytest tests/test_main_endpoints.py::TestMainEndpoints::test_health_endpoint_sync -v
```

### Testar com Saída Detalhada

```bash
python run_tests.py --type endpoints --verbose
```

### Testar em Porta Diferente

```bash
python start_test_server.py --port 8004
python run_tests.py --port 8004
```

### Executar Testes de um Módulo Específico

```bash
python -m pytest tests/test_modules_ping.py::TestModulePingEndpoints::test_working_module_ping_async -v -k "urbanism"
```

## 🏆 Metas de Qualidade

- ✅ **Cobertura**: Mínimo 70% do código
- ⚡ **Performance**: Resposta < 2s para endpoints principais
- 🔍 **Validação**: Pydantic + JSON Schema para todas as respostas
- 📦 **Modularidade**: Testes independentes e reutilizáveis
- 🚀 **Automação**: Scripts facilitados para CI/CD

---

**Desenvolvido para o SILA Backend** _Versão 1.0.0_ _Atualizado em 2025-10-28_
