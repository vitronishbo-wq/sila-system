# 🚀 SILA System Backend - Guia de Desenvolvimento

## 📋 Sumário

- [Início Rápido](#início-rápido)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Scripts de Desenvolvimento](#scripts-de-desenvolvimento)
- [Como Adicionar Novos Módulos](#como-adicionar-novos-módulos)
- [Teste de Módulos](#teste-de-módulos)
- [Troubleshooting](#troubleshooting)

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.12+
- PostgreSQL
- Ambiente virtual ativado

### 1. Ambiente Virtual

```bash
cd /opt/sila-system/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Iniciar Servidor de Desenvolvimento

```bash
# Opção 1: Script completo (recomendado)
./start_dev.sh

# Opção 2: Manual
export ENVIRONMENT=development
export DEBUG=true
python main.py
```

### 3. Verificar Funcionamento

```bash
# Health check
curl http://localhost:8000/health

# Documentação Swagger
# Abra no navegador: http://localhost:8000/docs
```

## 🏗️ Estrutura do Projeto

```
backend/
├── main.py                 # Ponto de entrada da aplicação
├── core/                   # Configurações e utilitários
│   ├── config.py          # Configurações do sistema
│   └── database.py        # Conexão com banco de dados
├── modules/                # Módulos de negócio
│   ├── auth/              # Autenticação
│   ├── dashboard/         # Painéis de controle
│   ├── finance/           # Financeiro
│   └── ...                # Outros módulos
├── docs/                   # Documentação
├── scripts/                # Scripts utilitários
└── tests/                  # Testes automatizados
```

## 🛠️ Scripts de Desenvolvimento

### start_dev.sh

**Propósito**: Inicia servidor completo com configurações de desenvolvimento

```bash
./start_dev.sh
```

**O que faz**:

- Verifica e libera porta 8000
- Configura variáveis de ambiente
- Ativa ambiente virtual
- Exibe todos os endpoints disponíveis
- Inicia servidor com auto-reload

### check_docs.sh

**Propósito**: Verifica se a documentação Swagger está ativa

```bash
./check_docs.sh
```

**O que faz**:

- Testa conectividade do backend
- Verifica documentação em /docs
- Reinicia servidor se necessário
- Exibe status completo

### test_modules.py

**Propósito**: Testa descoberta e validação de módulos

```bash
source venv/bin/activate
python test_modules.py
```

**O que faz**:

- Lista todos os módulos encontrados
- Mostra quantidade de rotas por módulo
- Exibe erros de importação
- Valida estrutura dos routers

## 📦 Como Adicionar Novos Módulos

### Padrão Esperado

Cada módulo deve seguir esta estrutura:

```
modules/novo_modulo/
├── __init__.py           # Inicialização do módulo
├── endpoints.py          # Definição das rotas (OBRIGATÓRIO)
├── models/               # Modelos de dados
│   └── __init__.py
├── schemas/              # Schemas de API
│   └── __init__.py
└── README.md             # Documentação do módulo
```

### endpoints.py - Template

```python
# modules/novo_modulo/endpoints.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/novo_modulo",
    tags=["Novo Módulo"]
)

@router.get("/ping")
async def ping():
    """Health check do módulo"""
    return {"status": "ok", "module": "novo_modulo"}

@router.get("/")
async def list_items():
    """Lista recursos do módulo"""
    return {"items": []}

@router.post("/")
async def create_item(item: dict):
    """Cria novo recurso"""
    return {"item": item, "id": 1}
```

### Passo a Passo

1. **Criar estrutura**: `mkdir -p modules/novo_modulo/{models,schemas}`
2. **Criar endpoints.py**: Copie o template acima
3. **Implementar lógica**: Adicione seus endpoints específicos
4. **Testar**: `python test_modules.py`
5. **Validar**: Acesse `http://localhost:8000/docs`

### Registro Automático

O sistema descobre automaticamente novos módulos que:

- Estão em `/modules/`
- Contêm `endpoints.py`
- Exportam variável `router` do tipo `APIRouter`

## 🧪 Teste de Módulos

### Testes Manuais

```bash
# Testar health check do módulo
curl http://localhost:8000/api/v1/nome_modulo/ping

# Listar rotas do módulo
curl http://localhost:8000/api/v1/nome_modulo/

# Verificar documentação
# Abra: http://localhost:8000/docs
```

### Testes Automatizados

```python
# tests/test_modules.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_module_ping():
    response = client.get("/api/v1/dashboard/ping")
    assert response.status_code == 200
    assert response.json()["module"] == "dashboard"
    assert response.json()["status"] == "ok"

def test_module_list():
    response = client.get("/api/v1/notifications/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Executar Testes

```bash
# Todos os testes
pytest tests/ -v

# Testes específicos
pytest tests/test_modules.py -v

# Com coverage
pytest tests/ --cov=modules --cov-report=html
```

## 📊 Módulos Atuais (Status)

### ✅ Funcionais (22/27)

| Módulo               | Rotas | Status   |
| -------------------- | ----- | -------- |
| notifications        | 11    | ✅ Ativo |
| analytics            | 15    | ✅ Ativo |
| finance              | 9     | ✅ Ativo |
| health               | 11    | ✅ Ativo |
| documents            | 13    | ✅ Ativo |
| dashboard            | 5     | ✅ Ativo |
| citizenship          | 7     | ✅ Ativo |
| education            | 1     | ✅ Ativo |
| training             | 2     | ✅ Ativo |
| E mais 13 módulos... |       | ✅ Ativo |

### ⚠️ Com Erros (5/27)

| Módulo   | Erro                                   | Solução                |
| -------- | -------------------------------------- | ---------------------- |
| auth     | 'bool' object has no attribute 'lower' | Corrigir configuração  |
| payment  | No module named 'modules.models'       | Adicionar dependências |
| location | Missing 'CommuneCreate'                | Completar modelos      |
| common   | Pydantic V2 incompatibilidade          | Atualizar schemas      |
| services | Pasta não encontrada                   | Criar estrutura        |

## 🔧 Troubleshooting

### Backend não inicia

```bash
# Verificar ambiente virtual
source venv/bin/activate

# Verificar dependências
pip install -r requirements.txt

# Verificar porta livre
./start_dev.sh  # Já faz isso automaticamente
```

### Módulos não carregam

```bash
# Testar descoberta
python test_modules.py

# Verificar logs
tail -f logs/app.log

# Verificar estrutura
ls -la modules/nome_modulo/endpoints.py
```

### Documentação não aparece

```bash
# Verificar configuração
grep -n "docs_url" main.py

# Forçar modo dev
export DEBUG=true
python main.py

# Testar script
./check_docs.sh
```

### Erros de CORS

```bash
# Verificar origens permitidas
grep -n "BACKEND_CORS_ORIGINS" .env

# Adicionar sua origem se necessário
export BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

## 🚀 Deploy e Produção

### Variáveis de Ambiente

```bash
# Desenvolvimento
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Produção
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

### Docker

```bash
# Build
docker build -t sila-backend .

# Run
docker run -p 8000:8000 sila-backend
```

### Health Checks

- **Health**: `GET /health`
- **Info**: `GET /info`
- **Módulos**: `GET /api/v1/{module}/ping`

## 📚 Recursos Adicionais

- [Documentação Swagger](http://localhost:8000/docs)
- [ReDoc Alternative](http://localhost:8000/redoc)
- [OpenAPI Spec](http://localhost:8000/openapi.json)
- [API Status Summary](./API_STATUS_SUMMARY.md)

---

**Última atualização**: 2025-10-28 **Versão**: 1.0.0 **Ambiente**: Development
