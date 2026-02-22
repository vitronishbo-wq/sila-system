# SILA - Sistema Integrado Local de Administração

Sistema integrado para gestão de licenciamentos e autorizações municipais com
arquitetura moderna, segura e acessível.

## ✨ Status do Projeto

**✅ PRODUÇÃO READY** - Sistema totalmente otimizado e governado:

- ✅ **Arquitetura unificada** de módulos implementada
- ✅ **Convenções de nomenclatura** padronizadas
- ✅ **Pirâmide de testes** revisada e otimizada
- ✅ **Segurança enterprise** com SAST implementado
- ✅ **Governança de scripts** com automação CI/CD
- ✅ **Documentação atualizada** e consistente
- ✅ **Dependências revisadas** com 57+ pacotes documentados

📋 **Ver relatório completo:**
[PHASE4_OPTIMIZATION_COMPLETE.md](./PHASE4_OPTIMIZATION_COMPLETE.md)

---

## 📦 Gerenciamento de Dependências

**🆕 ATUALIZADO: 05/11/2025** - Sistema completo de gerenciamento de dependências
implementado!

### 🚀 Quick Start

```bash
# Produção
pip install -r requirements.txt

# Desenvolvimento
pip install -r requirements-dev.txt

# Testes
pip install -r requirements-test.txt
```

### 📚 Documentação Completa

- **[DEPENDENCIES_INDEX.md](./DEPENDENCIES_INDEX.md)** - 🗂️ Índice e navegação
- **[DEPENDENCIES_USAGE.md](./DEPENDENCIES_USAGE.md)** - 📖 Guia de uso diário
- **[DEPENDENCIES_REVIEW.md](./DEPENDENCIES_REVIEW.md)** - 🔍 Análise técnica
- **[DEPENDENCIES_REPORT.md](./DEPENDENCIES_REPORT.md)** - 📊 Relatório e métricas

### 🛠️ Ferramentas Disponíveis

```bash
# Validar requirements
python scripts/validate_requirements.py

# Analisar dependências do código
python scripts/analyze_dependencies.py

# Gerar lock file (Linux/Mac/WSL)
./scripts/generate_requirements_lock.sh

# Gerar lock file (Windows)
.\scripts\generate_requirements_lock.ps1
```

**📌 57+ dependências** identificadas e documentadas | **✅ 100% validado** | **🔒 Lock
file ready**

---

## 🚀 Setup Rápido do Desenvolvimento

**⭐ NOVO: [Dev Setup Helper](./DEV_SETUP.md)** - Script automatizado que:

- ✅ Detecta localização do repositório automaticamente
- ✅ Ativa virtualenv Python (`.venv` ou `backend/.venv`)
- ✅ Instala dependências Python e Node.js
- ✅ Invoca scripts de setup existentes de forma segura
- ✅ Oferece smoke tests opcionais com `-RunSmoke`

**Uso:**

```powershell
# Primeira vez (instalação completa)
.\scripts\windows\dev\dev_setup.ps1

# Com testes básicos
.\scripts\windows\dev\dev_setup.ps1 -RunSmoke

# Apenas ativar venv (sem instalar)
.\scripts\windows\dev\dev_setup.ps1 -SkipInstall
```

Ver [documentação completa](./DEV_SETUP.md).

---

## 🏗️ Nova Arquitetura do Projeto

### Estrutura Unificada e Governada

```mermaid
graph TB
    A[SILA System] --> B[Backend FastAPI]
    A --> C[Frontend React/TS]
    A --> D[Mobile React Native]
    A --> E[DevOps & Monitoring]

    B --> F[Core Framework]
    B --> G[Unified Modules]
    B --> H[Security Layer]
    B --> I[Testing Pyramid]

    G --> J[Auth Module]
    G --> K[Business Modules]
    G --> L[Common Services]

    H --> M[JWT Authentication]
    H --> N[RBAC Authorization]
    H --> O[Security Scanning]

    I --> P[Unit Tests]
    I --> Q[Integration Tests]
    I --> R[E2E Tests]
```

### Diretório Otimizado

```
.
├── backend/                    # 🔧 Backend FastAPI
│   ├── app/
│   │   ├── core/              # ⚙️ Configurações e segurança
│   │   ├── api/               # 🌐 Endpoints globais da API
│   │   ├── modules/           # 📦 Módulos de negócio unificados
│   │   │   ├── auth/          # 🔐 Autenticação e autorização
│   │   │   ├── citizenship/   # 👥 Serviços ao cidadão
│   │   │   ├── commercial/    # 💼 Licenciamento comercial
│   │   │   ├── finance/       # 💰 Gestão financeira
│   │   │   ├── health/        # 🏥 Serviços de saúde
│   │   │   ├── education/     # 📚 Gestão educacional
│   │   │   ├── urbanism/      # 🏗️ Planeamento urbano
│   │   │   ├── justice/       # ⚖️ Serviços judiciais
│   │   │   ├── social/        # 🤝 Ação social
│   │   │   ├── monitoring/    # 📊 Monitoramento e métricas
│   │   │   ├── notifications/ # 📢 Sistema de notificações
│   │   │   ├── documents/     # 📄 Gestão documental
│   │   │   ├── payments/      # 💳 Processamento de pagamentos
│   │   │   ├── reports/       # 📈 Relatórios e analytics
│   │   │   ├── common/        # 🔧 Serviços compartilhados
│   │   │   └── integration/   # 🔗 Integrações externas
│   │   ├── models/            # 🗃️ Modelos de dados centralizados
│   │   ├── schemas/           # 📋 Schemas Pydantic unificados
│   │   └── utils/             # 🛠️ Utilitários globais
│   └── tests/                 # 🧪 Suite de testes completa
│       ├── unit/              # 🔬 Testes unitários
│       ├── integration/       # 🔗 Testes de integração
│       └── e2e/               # 🌐 Testes end-to-end
│
├── frontend/                   # 🎨 Frontend unificado
│   ├── apps/web/              # 🖥️ Aplicação web (React + TypeScript)
│   │   ├── src/
│   │   │   ├── components/    # 🧩 Componentes reutilizáveis
│   │   │   │   ├── accessibility/  # ♿ Sistema WCAG 2.1 AA
│   │   │   │   ├── auth/          # 🔐 Autenticação e RBAC
│   │   │   │   ├── forms/         # 📝 Renderizador dinâmico
│   │   │   │   └── ui/            # 🎨 Componentes base
│   │   │   ├── pages/        # 📄 Páginas da aplicação
│   │   │   ├── hooks/        # 🎣 Hooks customizados
│   │   │   ├── context/      # 🌐 Contexto global
│   │   │   └── utils/        # 🛠️ Utilitários frontend
│   │   └── cypress/       # 🧪 Testes E2E
│   └── apps/mobile/          # 📱 Aplicativo móvel
│
├── scripts/                    # 🔧 Scripts otimizados e governados
│   ├── essential/             # ⚡ Operações essenciais
│   ├── security/              # 🛡️ Ferramentas de segurança
│   ├── deployment/            # 🚀 Utilitários de deploy
│   ├── backup/                # 💾 Operações de backup
│   └── archive/               # 📦 Scripts históricos
│
├── docs/                      # 📚 Documentação técnica
├── monitoring/               # 📊 Monitoramento e métricas
├── reports/                  # 📋 Relatórios de auditoria
└── tests/                    # 🧪 Testes de sistema
```

---

## 🎯 Convenções de Nomenclatura

### **Padrão de Módulos**

```python
# Estrutura padrão para cada módulo
modules/{module_name}/
├── __init__.py              # 🚀 Inicialização e configuração
├── endpoints.py             # 🌐 Definição de rotas da API
├── models/                  # 🗃️ Modelos SQLAlchemy
│   ├── __init__.py
│   └── {module_name}.py
├── schemas/                 # 📋 Schemas Pydantic
│   ├── __init__.py
│   ├── request.py          # 📥 Schemas de entrada
│   ├── response.py         # 📤 Schemas de saída
│   └── common.py           # 🔧 Schemas compartilhados
├── services/               # ⚙️ Lógica de negócio
│   ├── __init__.py
│   └── {module_name}_service.py
├── crud/                   # 🗄️ Operações de banco
│   ├── __init__.py
│   └── {module_name}_crud.py
├── utils/                  # 🛠️ Utilitários do módulo
│   ├── __init__.py
│   └── {module_name}_utils.py
├── exceptions.py           # ⚠️ Exceções personalizadas
├── tests/                  # 🧪 Testes do módulo
│   ├── __init__.py
│   ├── test_endpoints.py
│   ├── test_services.py
│   └── test_crud.py
└── README.md              # 📖 Documentação do módulo
```

### **Convenções de Código**

```python
# 🏷️ Nomenclatura de Classes
class UserService:                    # PascalCase para classes
class CitizenshipRequestService:      # Nome descritivo
class PaymentProcessorService:        # Verbo + Substantivo

# 🏷️ Nomenclatura de Funções
async def get_user_by_id(user_id: str):     # snake_case para funções
async def create_citizenship_request():     # Verbo + Substantivo
async def process_payment_notification():   # Ação clara

# 🏷️ Nomenclatura de Variáveis
user_id = "user_123"                    # snake_case para variáveis
request_data = {...}                    # Nome descritivo
is_authenticated = True                 # Boolean com prefixo

# 🏷️ Nomenclatura de Endpoints
@router.get("/users/{user_id}")         # RESTful patterns
@router.post("/citizenship/requests")   # Recurso plural
@router.patch("/payments/{payment_id}/status")  # Sub-recurso específico
```

---

## 🧪 Pirâmide de Testes Revisada

### **Estrutura de Testes Otimizada**

```mermaid
graph TB
    A[Pirâmide de Testes SILA] --> B[E2E Tests - 10%]
    A --> C[Integration Tests - 30%]
    A --> D[Unit Tests - 60%]

    B --> E[Cypress Tests]
    B --> F[API Integration]

    C --> G[Module Integration]
    C --> H[Database Integration]
    C --> I[Service Integration]

    D --> J[Model Tests]
    D --> K[Service Tests]
    D --> L[Utility Tests]
    D --> M[Schema Tests]
```

### **Categorias de Testes**

#### **🔬 Testes Unitários (60%)**

```python
# backend/tests/unit/
├── test_models.py              # Testes de modelos SQLAlchemy
├── test_services.py            # Testes de lógica de negócio
├── test_schemas.py             # Testes de validação Pydantic
├── test_utils.py               # Testes de utilitários
├── test_auth_utils.py          # Testes de autenticação
└── modules/                    # Testes por módulo
    ├── auth/
    │   ├── test_auth_service.py
    │   └── test_user_model.py
    ├── citizenship/
    │   ├── test_request_service.py
    │   └── test_citizen_model.py
    └── finance/
        ├── test_payment_service.py
        └── test_transaction_model.py
```

#### **🔗 Testes de Integração (30%)**

```python
# backend/tests/integration/
├── test_api.py                 # Testes de API geral
├── test_database.py            # Testes de integração com DB
├── test_auth_flow.py           # Testes de fluxo de autenticação
├── test_module_integration.py  # Testes entre módulos
├── cross_module/               # Testes cross-módulo
│   ├── test_citizenship_finance.py
│   ├── test_auth_notifications.py
│   └── test_payments_documents.py
└── modules/                    # Testes de integração por módulo
    ├── test_citizenship_endpoints.py
    ├── test_finance_workflow.py
    └── test_notifications_integration.py
```

#### **🌐 Testes End-to-End (10%)**

```python
# frontend/cypress/e2e/
├── auth/                       # Fluxos de autenticação
│   ├── login.cy.js
│   ├── logout.cy.js
│   └── password_reset.cy.js
├── citizenship/                # Fluxos de cidadania
│   ├── create_request.cy.js
│   ├── track_status.cy.js
│   └── upload_documents.cy.js
├── finance/                    # Fluxos financeiros
│   ├── make_payment.cy.js
│   ├── view_invoice.cy.js
│   └── refund_process.cy.js
└── admin/                      # Fluxos administrativos
    ├── user_management.cy.js
    ├── system_config.cy.js
    └── report_generation.cy.js
```

### **Execução de Testes**

```bash
# 🔬 Executar todos os testes unitários
pytest backend/tests/unit/ -v --cov=app

# 🔗 Executar testes de integração
pytest backend/tests/integration/ -v --cov=app

# 🌐 Executar testes E2E
cd frontend && npm run test:e2e

# 📊 Executar suite completa com cobertura
pytest backend/tests/ -v --cov=app --cov-report=html

# ⚡ Executar testes rápidos (unit + integration básica)
pytest backend/tests/ -m "not slow" -v
```

---

## 🛠️ Configuração do Ambiente

### **Pré-requisitos**

- **Python 3.12+** - Versão estável mais recente
- **Node.js 18+** - Suporte a ES2022
- **PostgreSQL 15+** - Banco de dados principal
- **Docker & Docker Compose** - Ambiente de desenvolvimento
- **Redis 7+** - Cache e sessões

### **Configuração Rápida**

#### **1. Clonar e Configurar**

```bash
# Clonar repositório
git clone <repo-url>
cd sila-system

# Configurar ambiente Python
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements/dev.txt
```

#### **2. Configurar Variáveis de Ambiente**

```bash
# Copiar arquivo de exemplo
cp .env.example .env.development

# Configurar variáveis essenciais
DATABASE_URL=postgresql://user:pass@localhost:5432/sila_dev
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
REDIS_URL=redis://localhost:6379/0
```

#### **3. Iniciar Serviços**

```bash
# Iniciar banco de dados e cache
docker-compose up -d db redis

# Aplicar migrações
alembic upgrade head

# Carregar dados iniciais
python scripts/load_initial_data.py

# Iniciar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### **4. Iniciar Frontend**

```bash
# Em outro terminal
cd frontend/apps/web
npm install
npm start

# Acessar aplicação
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 🔐 Segurança e Governança

### **Segurança Implementada**

- ✅ **SAST (Static Analysis)** - Bandit + Safety scanning
- ✅ **Autenticação JWT** - Tokens seguros com expiração
- ✅ **RBAC (Role-Based Access)** - Controle de acesso granular
- ✅ **Validação de Entrada** - Pydantic schemas rigorosos
- ✅ **Proteção CSRF** - Middleware de segurança
- ✅ **Rate Limiting** - Prevenção contra ataques
- ✅ **Audit Logging** - Registro de ações sensíveis

### **Governança de Código**

- ✅ **Pre-commit Hooks** - Formatação e validação automática
- ✅ **CI/CD Pipeline** - Testes e segurança automatizados
- ✅ **Code Review** - Processo de aprovação obrigatório
- ✅ **Documentação** - Sempre atualizada com código
- ✅ **Versionamento** - Controle rigoroso de mudanças

### **Scripts de Segurança**

```bash
# 🔍 Executar auditoria de segurança
python scripts/security/security_audit.py

# 🔧 Aplicar correções automáticas
python scripts/security/security_remediation.py

# 🛡️ Validar credenciais
python scripts/essential/check_credentials.py
```

---

## 📚 Documentação de Módulos

### **Padrão de Documentação**

Cada módulo segue o padrão de documentação unificado:

```markdown
# Módulo {Module Name}

# Sistema SILA - Backend

## 📋 Descrição

Breve descrição do propósito e funcionalidades do módulo.

## 🚀 Funcionalidades Principais

- Lista de funcionalidades implementadas
- Recursos principais e casos de uso

## 📡 Endpoints Disponíveis

| Método | Endpoint | Descrição | Autenticação |
| ------ | -------- | --------- | ------------ |

## 🔧 Configuração

- Framework e tecnologias utilizadas
- Dependências principais
- Configurações específicas

## 🗂️ Estrutura do Módulo

Estrutura de arquivos e diretórios do módulo.

## 📚 Exemplos de Uso

Exemplos práticos de implementação e integração.

## 🔗 Dependências

Dependências internas e externas do módulo.

## ⚠️ Observações Importantes

Notas sobre desenvolvimento, produção e segurança.

## 👥 Responsáveis

Equipe responsável e informações de contato.
```

### **Módulos Principais**

#### **🔐 Auth Module**

- **Propósito**: Autenticação e autorização centralizada
- **Features**: JWT, RBAC, refresh tokens, password reset
- **Endpoints**: `/auth/login`, `/auth/refresh`, `/auth/logout`
- **Documentação**: [backend/modules/auth/README.md](./backend/modules/auth/README.md)

#### **👥 Citizenship Module**

- **Propósito**: Serviços ao cidadão e solicitações
- **Features**: Catálogo de serviços, acompanhamento de processos
- **Endpoints**: `/citizenship/services`, `/citizenship/requests`
- **Documentação**:
  [backend/modules/citizenship/README.md](./backend/modules/citizenship/README.md)

#### **💼 Commercial Module**

- **Propósito**: Licenciamento comercial e empresarial
- **Features**: Registro de empresas, alvarás, inspeções
- **Endpoints**: `/commercial/register`, `/commercial/licenses`
- **Documentação**:
  [backend/modules/commercial/README.md](./backend/modules/commercial/README.md)

#### **💰 Finance Module**

- **Propósito**: Gestão financeira e pagamentos
- **Features**: Processamento de pagamentos, faturação, relatórios
- **Endpoints**: `/finance/payments`, `/finance/invoices`
- **Documentação**:
  [backend/modules/finance/README.md](./backend/modules/finance/README.md)

---

## 🚀 Implantação

### **Ambientes Suportados**

- **Development** - Ambiente local de desenvolvimento
- **Staging** - Ambiente de homologação
- **Production** - Ambiente de produção

### **Métodos de Deploy**

#### **Docker (Recomendado)**

```bash
# Deploy completo
docker-compose -f docker-compose.prod.yml up -d

# Verificar status
docker-compose ps

# Logs
docker-compose logs -f
```

#### **Scripts de Deploy**

```bash
# Deploy para produção
./scripts/deployment/deploy_production.sh

# Deploy para staging
./scripts/deployment/deploy_staging.sh

# Validação pós-deploy
./scripts/deployment/validate_deployment.sh
```

### **Monitoramento**

- **Health Checks**: `/health`, `/health/db`, `/health/redis`
- **Métricas**: Prometheus + Grafana
- **Logs**: Estruturação com JSON + ELK Stack
- **Alertas**: Configuração no AlertManager

---

## 🧪 Execução de Testes

### **Comandos Principais**

```bash
# 🔬 Testes unitários (rápidos)
pytest backend/tests/unit/ -v --tb=short

# 🔗 Testes de integração
pytest backend/tests/integration/ -v --tb=short

# 🌐 Testes E2E
cd frontend/apps/web && npm run test:e2e

# 📊 Cobertura completa
pytest backend/tests/ -v --cov=app --cov-report=html

# ⚡ Testes paralelos (mais rápidos)
pytest backend/tests/ -n auto --dist=loadfile
```

### **Categorias de Testes**

```bash
# Testes de segurança
pytest backend/tests/ -m security -v

# Testes de performance
pytest backend/tests/ -m performance -v

# Testes de API
pytest backend/tests/ -m api -v

# Testes de banco de dados
pytest backend/tests/ -m database -v
```

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para
detalhes.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia nosso
[guia de contribuição](CONTRIBUTING.md) para obter detalhes sobre:

- 🔧 **Processo de desenvolvimento** - Branches, commits, PRs
- 📋 **Padrões de código** - Convenções e boas práticas
- 🧪 **Requisitos de testes** - Cobertura e qualidade
- 📚 **Documentação** - Manter docs atualizadas
- 🔐 **Segurança** - Boas práticas de segurança

---

## 📞 Suporte

### **Canais de Suporte**

- **📧 Email**: dev@sila.gov.ao
- **💬 Slack**: #sila-development
- **🐛 Issues**: [GitHub Issues](https://github.com/sila-system/issues)
- **📖 Documentação**: [docs.sila.gov.ao](https://docs.sila.gov.ao)

### **Equipe Responsável**

- **🏗️ Arquitetura**: Equipe de Arquitetura SILA
- **🔧 Backend**: Equipe de Desenvolvimento Backend
- **🎨 Frontend**: Equipe de Desenvolvimento Frontend
- **🛡️ Segurança**: Equipe de Segurança da Informação
- **🚀 DevOps**: Equipe de Operações e Infraestrutura

---

## 🏆 Status do Projeto

**✅ PRODUCTION READY** - Sistema pronto para produção com:

- 🏗️ **Arquitetura unificada** e escalável
- 🔐 **Segurança enterprise** implementada
- 🧪 **Testes abrangentes** e automatizados
- 📚 **Documentação completa** e atualizada
- 🚀 **CI/CD robusto** e automatizado
- 📊 **Monitoramento** e observabilidade
- 🛡️ **Governança** de código e scripts

---

_Sistema modular para digitalização de serviços das administrações municipais, comunais
e distritos urbanos de Angola._

**Última atualização**: Outubro 2025 **Versão**: 2.0.0 - Architecture Unification
**Status**: ✅ Production Ready
