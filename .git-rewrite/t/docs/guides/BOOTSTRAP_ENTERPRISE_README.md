# 🚀 Bootstrap Enterprise SILA Backend

**Versão Enterprise v2.0.0** - Script profissional de provisionamento e validação de
ambiente para pipelines DevOps enterprise-grade.

## ✨ Características Distintivas

### 🎛️ Controle Granular

- **Flags inteligentes** para controle preciso da execução
- **Modo dry-run** para simulação sem alterações
- **Configuração modular** - execute apenas as etapas necessárias
- **Modo produção** com configurações otimizadas e seguras

### 📊 Sistema de Logging Profissional

- **Logs estruturados** com timestamps e níveis detalhados
- **Arquivo de log rotativo** em `/var/log/sila-bootstrap.log`
- **Relatório JSON** com estatísticas completas de execução
- **Logging verboso** opcional para debugging avançado

### 🔍 Validações de Serviços Externos

- **Teste de conectividade** com Redis, SMTP, Sentry
- **Validação de bancos externos** e configurações remotas
- **Detecção automática** de serviços disponíveis
- **Relatórios de saúde** dos serviços críticos

### 🏭 Modo Produção Avançado

- **Gunicorn** com múltiplos workers (4 por padrão)
- **Configurações de segurança** habilitadas automaticamente
- **Headers seguros** e otimizações de performance
- **Variáveis de ambiente** específicas para produção

## 🛠️ Como Usar

### Execução Básica

```bash
cd /opt/sila-system
./bootstrap_sila_backend_enterprise.sh
```

### Execução com Flags

```bash
# Modo produção completo
./bootstrap_sila_backend_enterprise.sh --production

# Simulação sem alterações
./bootstrap_sila_backend_enterprise.sh --dry-run --verbose

# Desenvolvimento sem banco local
./bootstrap_sila-backend_enterprise.sh --skip-db

# Apenas validar serviços externos
./bootstrap_sila_backend_enterprise.sh --skip-deps --skip-db

# Forçar recriação de recursos
./bootstrap_sila_backend_enterprise.sh --force --production
```

### Uso em Pipelines CI/CD

```bash
#!/bin/bash
# Em pipeline GitHub Actions, GitLab CI, etc.

# Instalar dependências
./bootstrap_sila_backend_enterprise.sh --skip-deps

# Apenas validar ambiente
./bootstrap_sila_backend_enterprise.sh --dry-run

# Deploy produção
./bootstrap_sila_backend_enterprise.sh --production --skip-deps
```

## 📋 Etapas de Execução

### 1. 📦 Verificação de Dependências do Sistema

- Python 3.12, PostgreSQL, Redis, ferramentas de build
- Detecção automática de pacotes ausentes
- Instalação silenciosa com logs detalhados

### 2. 🧪 Configuração de Ambiente Virtual

- Criação ou atualização do ambiente `.venv`
- Ativação automática do ambiente virtual
- Verificação de integridade da instalação

### 3. 📚 Instalação de Dependências Python

- Atualização automática do pip
- Instalação de todas as dependências do `requirements.txt`
- Verificação de compatibilidade de versões

### 4. 🔐 Configuração de Ambiente

- Criação inteligente do arquivo `.env`
- Geração automática de chaves secretas
- Configurações específicas por ambiente (dev/prod)

### 5. 🗄️ Configuração de Banco de Dados

- Inicialização automática do PostgreSQL
- Criação do banco de dados `sila_dev`
- Configuração de conexões e permissões

### 6. 📜 Aplicação de Migrações

- Execução automática das migrações do Alembic
- Tratamento robusto de erros de migração
- Verificação de estado das migrações

### 7. 🔍 Validação de Serviços Externos

- Teste de conectividade com Redis
- Validação de configurações SMTP
- Verificação de DSN do Sentry
- Teste de bancos de dados remotos

### 8. 🚀 Inicialização do Servidor

- **Desenvolvimento**: Uvicorn com reload automático
- **Produção**: Gunicorn com 4 workers otimizados
- Configurações específicas por ambiente

## 🎯 Funcionalidades Avançadas

### Sistema de Logs Profissional

```bash
# Arquivo de log estruturado
tail -f /var/log/sila-bootstrap.log

# Relatório JSON detalhado
cat /var/log/sila-bootstrap-report.json | jq .
```

**Exemplo de saída do relatório:**

```json
{
  "script_version": "2.0.0-enterprise",
  "start_time": "2024-01-15T10:30:45+00:00",
  "environment": "production",
  "steps": [
    {
      "step": "DEPENDENCIES",
      "message": "Todas as dependências estão instaladas",
      "level": "SUCCESS",
      "timestamp": "2024-01-15T10:30:46+00:00"
    }
  ],
  "summary": {
    "total_steps": 8,
    "successful_steps": 8,
    "failed_steps": 0,
    "warnings": 0,
    "execution_time_seconds": 45
  }
}
```

### Modo Dry-Run Detalhado

```bash
./bootstrap_sila_backend_enterprise.sh --dry-run --verbose

# Saída exemplo:
🔵 [2024-01-15 10:30:45] [INFO] [DEPENDENCIES] Verificando dependências do sistema
🔵 [2024-01-15 10:30:46] [INFO] [DEPENDENCIES] [DRY-RUN] Seria instalar: python3.12 python3.12-venv
🔵 [2024-01-15 10:30:47] [INFO] [VIRTUALENV] [DRY-RUN] Seria criar ambiente virtual em /opt/sila-system/backend/.venv
```

### Modo Produção Configurado

```bash
./bootstrap_sila_backend_enterprise.sh --production

# Configura automaticamente:
# - Gunicorn com 4 workers
# - Headers de segurança
# - Logging em nível WARNING
# - DEBUG=false
# - Configurações otimizadas de performance
```

## 🔧 Personalização Avançada

### Variáveis de Ambiente Personalizadas

```bash
# Configurar serviços externos antes da execução
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SENTRY_DSN=https://your-dsn@sentry.io/project
export EXTERNAL_DB_HOST=remote-db.example.com

./bootstrap_sila_backend_enterprise.sh --production
```

### Configuração de Workers (Produção)

```bash
# Número personalizado de workers
export GUNICORN_WORKERS=8
./bootstrap_sila_backend_enterprise.sh --production
```

### Timeouts e Configurações Avançadas

```bash
# Timeout personalizado para banco remoto
export DB_CONNECTION_TIMEOUT=30
./bootstrap_sila_backend_enterprise.sh
```

## 🚨 Solução de Problemas

### Problema: Permissões de Arquivo de Log

```bash
# Se houver problemas de permissão nos logs
sudo mkdir -p /var/log/sila-bootstrap
sudo chmod 777 /var/log/sila-bootstrap
```

### Problema: Serviços Externos Indisponíveis

```bash
# Verificar conectividade específica
./bootstrap_sila_backend_enterprise.sh --verbose

# Testar apenas validações externas
./bootstrap_sila_backend_enterprise.sh --skip-deps --skip-db --production
```

### Problema: Ambiente Virtual Corrompido

```bash
# Forçar recriação do ambiente
./bootstrap_sila_backend_enterprise.sh --force --skip-deps
```

## 📊 Monitoramento e Health Checks

### Verificar Status dos Serviços

```bash
# Após execução, verificar se tudo está rodando
curl http://localhost:8080/health
curl http://localhost:8080/

# Verificar logs em tempo real
tail -f /var/log/sila-bootstrap.log
```

### Health Check Completo

```bash
# O endpoint /health inclui informações detalhadas:
curl http://localhost:8080/health | jq .

# Saída exemplo:
{
  "status": "healthy",
  "service": "SILA Backend",
  "version": "2.0.0",
  "environment": "production",
  "database": "connected",
  "redis": "connected"
}
```

## 🔄 Integração com Ferramentas DevOps

### GitHub Actions

```yaml
- name: Bootstrap Backend
  run: ./bootstrap_sila_backend_enterprise.sh --production --skip-deps
```

### Docker Compose

```bash
# Em docker-compose.yml
command: ["./bootstrap_sila_backend_enterprise.sh", "--production"]
```

### Kubernetes

```yaml
# Em ConfigMap ou Secret
env:
  - name: PRODUCTION
    value: "true"
```

## 🎉 Diferenças da Versão Standard

| Característica           | Standard | Enterprise |
| ------------------------ | -------- | ---------- |
| **Flags de controle**    | ❌       | ✅         |
| **Logging profissional** | ❌       | ✅         |
| **Relatório JSON**       | ❌       | ✅         |
| **Validações externas**  | ❌       | ✅         |
| **Modo produção**        | ❌       | ✅         |
| **Gunicorn**             | ❌       | ✅         |
| **Dry-run**              | ❌       | ✅         |
| **Sistema modular**      | ❌       | ✅         |

## 🚨 Requisitos

- **Sistema operacional**: Ubuntu/Debian-based
- **Privilégios**: Root para instalação de dependências
- **Python**: 3.12+
- **PostgreSQL**: 16+
- **Ferramentas**: curl, wget, netcat, jq

## 📚 Arquivos Relacionados

- `bootstrap_sila_backend_enterprise.sh` - Script principal
- `backend/main.py` - Ponto de entrada da aplicação
- `backend/requirements.txt` - Dependências Python
- `backend/env.example` - Template de configuração
- `/var/log/sila-bootstrap.log` - Logs detalhados (gerado automaticamente)
- `/var/log/sila-bootstrap-report.json` - Relatório de execução (gerado automaticamente)

---

**🎯 Este script representa o estado-da-arte em automação de ambientes para aplicações
Python/FastAPI, pronto para uso em ambientes enterprise e pipelines DevOps
profissionais.**
