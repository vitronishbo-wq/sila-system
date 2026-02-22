# 🛡️ MSIC - Metodologia SILA de Intercâmbio de Configurações

## 📋 Visão Geral

A **MSIC (Metodologia SILA de Intercâmbio de Configurações)** é um framework de
gerenciamento de configurações que garante:

- ✅ **Zero duplicatas** no projeto
- ✅ **Configuração centralizada** e validada
- ✅ **Segurança por design** (sem credenciais hardcoded)
- ✅ **Automação inteligente** (detecção de ambiente)
- ✅ **Fácil manutenção** (um único ponto de verdade)

---

## 🚀 Quick Start

### 1. Primeira Inicialização (Desenvolvimento)

```bash
# Copiar template de configuração
cp .env.template .env.development

# Ajustar credenciais locais (opcional)
nano .env.development

# Iniciar sistema
./sila_start.sh dev
```

### 2. Primeira Inicialização (Produção)

```bash
# Copiar template de configuração
cp .env.template .env.production

# IMPORTANTE: Configurar credenciais de produção
nano .env.production

# Iniciar sistema
./sila_start.sh prod
```

---

## 📁 Estrutura de Arquivos MSIC

```
sila-system/
├── 📄 .env.template           # Template unificado (commitar)
├── 📄 .env.example            # Sincronizado com template (commitar)
├── 🔒 .env.development        # Config de dev (NÃO commitar)
├── 🔒 .env.production         # Config de prod (NÃO commitar)
├── 🔗 .env                    # Link simbólico (NÃO commitar)
├── 🐳 docker-compose.yml      # Orquestração unificada
├── 🚀 sila_start.sh           # Script MSIC consolidado
└── backend/
    └── config/
        └── ⚙️ settings.py     # Settings único (Pydantic V2)
```

### Legenda:

- 📄 = Arquivo de template/exemplo (commitar)
- 🔒 = Arquivo com credenciais (NÃO commitar)
- 🔗 = Link simbólico (gerado automaticamente)
- 🐳 = Configuração Docker
- 🚀 = Script de automação
- ⚙️ = Código Python

---

## 🎯 Categorias MSIC

### 1. ⚙️ Orquestração (Docker)

**Arquivo:** `docker-compose.yml`

**Responsabilidades:**

- Definir serviços (backend, frontend, db, redis)
- Configurar networks e volumes
- Definir healthchecks
- Gerenciar dependências entre serviços

**Variáveis de Ambiente Suportadas:**

```bash
ENVIRONMENT=development|production
BACKEND_PORT=8000
FRONTEND_PORT=80
FRONTEND_DEV_PORT=5173
DB_PORT=5434
FRONTEND_TARGET=dev|runtime
```

---

### 2. 🌐 Configuração (Ambiente)

**Arquivos:**

- `.env.template` - Template base (commitar)
- `.env.development` - Config de desenvolvimento (não commitar)
- `.env.production` - Config de produção (não commitar)
- `.env.example` - Exemplo sincronizado (commitar)

**Seções do Template:**

1. Configuração do Ambiente
2. Portas Docker Compose
3. Banco de Dados
4. Segurança e Autenticação
5. CORS e Frontend
6. Cache e Redis
7. Logging e Monitoramento
8. Armazenamento MinIO
9. Upload e Arquivos
10. Limitação de Taxa
11. Feature Flags
12. Backup e Retenção
13. Security Headers
14. SSL e Segurança
15. BNA Integration
16. Payment Configuration
17. Email Configuration
18. External APIs
19. Analytics

---

### 3. ⚙️ Settings (Backend)

**Arquivo:** `backend/config/settings.py`

**Características:**

- ✅ Pydantic V2 (validação automática)
- ✅ Type hints completos
- ✅ Validators customizados
- ✅ Defaults seguros
- ✅ Propriedades computadas
- ✅ Métodos utilitários

**Carregamento Inteligente:**

```python
# Prioridade de busca:
1. .env.{ENVIRONMENT}  # Ex: .env.development
2. .env.template       # Template base
3. .env                # Fallback
```

**Uso no Código:**

```python
from backend.config.settings import settings

# Acessar configurações
print(settings.DATABASE_URL)
print(settings.ENVIRONMENT)
print(settings.is_development())

# Info sem credenciais
db_info = settings.get_database_info()
```

---

### 4. 🧰 Automação (Scripts)

**Arquivo:** `sila_start.sh`

**Funcionalidades:**

#### Detecção Automática de Modo

```bash
./sila_start.sh              # Auto-detecta
./sila_start.sh dev          # Desenvolvimento
./sila_start.sh prod         # Produção
./sila_start.sh staging      # Staging
```

#### Verificações Inteligentes

- ✅ Dependências do sistema (Docker, Docker Compose)
- ✅ Arquivos essenciais (docker-compose.yml, Dockerfile, settings.py)
- ✅ Configurações de ambiente (.env.{mode})

#### Configuração Automática

- ✅ Cria `.env.{mode}` a partir de `.env.template` se não existir
- ✅ Ajusta variáveis automaticamente (DEBUG, LOG_LEVEL, FRONTEND_TARGET)
- ✅ Cria link simbólico `.env` -> `.env.{mode}`

#### Limpeza Inteligente

```bash
./sila_start.sh dev --clean  # Limpa volumes e reconstrói
```

---

## 🔒 Segurança

### Boas Práticas Implementadas:

1. **Separação de Credenciais:**

   - ✅ Template sem credenciais reais
   - ✅ Arquivos `.env.{ambiente}` no `.gitignore`
   - ✅ Validação automática de configurações

2. **Validação de Produção:**

   ```python
   # Em settings.py
   @model_validator(mode="after")
   def validate_security_settings(self):
       if self.ENVIRONMENT == "production":
           if self.SECRET_KEY == "supersecretkey_2025_sila":
               raise ValueError("SECRET_KEY must be changed in production")
           if not self.SESSION_COOKIE_SECURE:
               raise ValueError("SESSION_COOKIE_SECURE must be True in production")
   ```

3. **Logs Seguros:**
   - ✅ Métodos `get_*_info()` sem credenciais
   - ✅ Senhas nunca logadas
   - ✅ URLs de database mascaradas

---

## 🧪 Testes

### Teste 1: Validar Configuração

```bash
# Entrar no container backend
docker-compose exec backend bash

# Verificar settings
python -c "from backend.config.settings import settings; settings.print_settings_summary()"
```

### Teste 2: Verificar Carregamento de .env

```bash
# Verificar qual arquivo está sendo carregado
docker-compose exec backend python -c "
from backend.config.settings import settings
print(f'Ambiente: {settings.ENVIRONMENT}')
print(f'Debug: {settings.DEBUG}')
print(f'Database: {settings.POSTGRES_HOST}')
"
```

### Teste 3: Validar Docker Compose

```bash
# Verificar configuração
docker-compose config

# Verificar variáveis de ambiente
docker-compose exec backend env | grep -E "ENVIRONMENT|DEBUG|DATABASE"
```

---

## 📚 Comandos Úteis

### Gerenciamento do Sistema:

```bash
# Iniciar (desenvolvimento)
./sila_start.sh dev

# Iniciar (produção)
./sila_start.sh prod

# Parar sistema
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuild completo
./sila_start.sh dev --clean
```

### Logs e Debug:

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Ver logs apenas do frontend
docker-compose logs -f frontend

# Ver últimas 100 linhas
docker-compose logs --tail=100
```

### Acesso aos Containers:

```bash
# Entrar no container backend
docker-compose exec backend bash

# Entrar no container frontend
docker-compose exec frontend sh

# Entrar no container database
docker-compose exec db psql -U postgres -d sila_db
```

### Status e Informações:

```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats

# Inspecionar container
docker inspect sila-backend

# Ver networks
docker network ls
```

---

## 🔄 Workflow de Desenvolvimento

### 1. Setup Inicial (Uma Vez)

```bash
# Clonar repositório
git clone <repo-url>
cd sila-system

# Copiar template
cp .env.template .env.development

# Ajustar credenciais locais
nano .env.development

# Iniciar sistema
./sila_start.sh dev
```

### 2. Desenvolvimento Diário

```bash
# Iniciar sistema
./sila_start.sh dev

# Fazer alterações no código
# Hot reload automático (backend e frontend)

# Ver logs
docker-compose logs -f

# Parar sistema
docker-compose down
```

### 3. Testes e Validação

```bash
# Rebuild completo
./sila_start.sh dev --clean

# Executar testes
docker-compose exec backend pytest

# Verificar linting
docker-compose exec backend flake8
```

---

## 🚨 Troubleshooting

### Problema: "Arquivo .env não encontrado"

**Solução:**

```bash
cp .env.template .env.development
./sila_start.sh dev
```

### Problema: "Settings validation failed"

**Solução:**

```bash
# Verificar variáveis obrigatórias
cat .env.development | grep -E "DATABASE_URL|SECRET_KEY|ENVIRONMENT"

# Validar settings
docker-compose exec backend python -c "from backend.config.settings import validate_settings; validate_settings()"
```

### Problema: "Port already in use"

**Solução:**

```bash
# Verificar portas em uso
docker-compose ps
netstat -tulpn | grep -E "8000|5173|5434"

# Parar containers antigos
docker-compose down
```

### Problema: "Database connection failed"

**Solução:**

```bash
# Verificar se database está rodando
docker-compose ps db

# Ver logs do database
docker-compose logs db

# Reiniciar database
docker-compose restart db
```

---

## 📖 Referências

### Documentos Relacionados:

- `MSIC_CONSOLIDATION_REPORT.md` - Relatório completo de consolidação
- `docker-compose.yml` - Configuração de orquestração
- `backend/config/settings.py` - Código de configurações
- `.env.template` - Template de variáveis de ambiente

### Links Úteis:

- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)

---

## 🎯 Próximos Passos

### Para Novos Desenvolvedores:

1. ✅ Ler este README
2. ✅ Copiar `.env.template` para `.env.development`
3. ✅ Executar `./sila_start.sh dev`
4. ✅ Verificar URLs em http://localhost:8000/docs

### Para Deploy em Produção:

1. ✅ Copiar `.env.template` para `.env.production`
2. ✅ Configurar credenciais de produção
3. ✅ Validar configurações de segurança
4. ✅ Executar `./sila_start.sh prod`
5. ✅ Monitorar logs e healthchecks

---

## 📞 Suporte

**Desenvolvedor:** Marcelo Truman **Sistema:** SILA System 3.0 **Metodologia:** MSIC
(Metodologia SILA de Intercâmbio de Configurações) **Versão:** 3.0

---

**Última Atualização:** 2025-01-05 **Status:** ✅ Consolidação Completa
