# 🚀 Guia Completo de CI/CD e Deploy - SILA System

Sistema profissional de integração contínua, testes automatizados e deploy para
ambientes staging e produção.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura CI/CD](#arquitetura-cicd)
- [Testes Automatizados](#testes-automatizados)
- [Deploy Staging](#deploy-staging)
- [Deploy Produção](#deploy-produção)
- [Monitoramento](#monitoramento)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O SILA System implementa um pipeline CI/CD completo com:

- ✅ **Validação MSIC** - Verificação de configurações e arquivos essenciais
- ✅ **Testes Automatizados** - Unit, integration, frontend e smoke tests
- ✅ **Security Scanning** - Trivy, Safety, TruffleHog
- ✅ **Build Docker** - Imagens otimizadas com cache
- ✅ **Deploy Automatizado** - Staging e produção com rollback
- ✅ **Healthcheck Inteligente** - Validação pós-deploy
- ✅ **Monitoramento Contínuo** - Métricas e alertas

---

## 🏗️ Arquitetura CI/CD

### Pipeline Completo

```
┌─────────────────────────────────────────────────────────────┐
│                     MSIC Validation                         │
│  ✓ Config files  ✓ Environment vars  ✓ Docker Compose     │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼────────┐
│ Backend Tests  │  │ Frontend Tests│
│ • Unit         │  │ • Lint        │
│ • Integration  │  │ • Type Check  │
│ • Coverage     │  │ • Build       │
└───────┬────────┘  └──────┬────────┘
        │                   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │ Security Scanning │
        │ • Trivy           │
        │ • Safety          │
        │ • TruffleHog      │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │  Build Images     │
        │ • Backend Docker  │
        │ • Frontend Docker │
        └─────────┬─────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼────────┐
│ Deploy Staging │  │ Deploy Prod   │
│ • Backup DB    │  │ • Backup DB   │
│ • Healthcheck  │  │ • Healthcheck │
│ • Smoke Tests  │  │ • Monitoring  │
└────────────────┘  └───────────────┘
```

### Ambientes

| Ambiente    | Branch    | URL                     | Auto-Deploy |
| ----------- | --------- | ----------------------- | ----------- |
| Development | `develop` | localhost               | Manual      |
| Staging     | `staging` | staging.sila-system.com | ✅ Auto     |
| Production  | `main`    | sila-system.com         | ✅ Auto     |

---

## 🧪 Testes Automatizados

### Script de Testes

```bash
# Executar todos os testes
./scripts/run_tests.sh all

# Testes específicos
./scripts/run_tests.sh unit          # Testes unitários
./scripts/run_tests.sh integration   # Testes de integração
./scripts/run_tests.sh frontend      # Testes frontend
./scripts/run_tests.sh smoke         # Smoke tests
./scripts/run_tests.sh e2e           # End-to-end tests
```

### Estrutura de Testes

```
tests/
├── unit/                    # Testes unitários
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Testes de integração
│   ├── test_api.py
│   ├── test_database.py
│   └── test_auth.py
├── e2e/                     # Testes end-to-end
│   └── test_user_flow.py
└── conftest.py              # Configuração pytest
```

### Coverage

O sistema exige **80% de cobertura** mínima:

```bash
cd backend
pytest --cov=modules --cov=app --cov-report=html
# Abrir: backend/htmlcov/index.html
```

### Testes no CI/CD

O workflow `.github/workflows/msic-cicd.yml` executa automaticamente:

1. **Backend Tests**

   - Linting (flake8, black, isort)
   - Unit tests com coverage
   - Integration tests
   - Upload para Codecov

2. **Frontend Tests**

   - ESLint
   - TypeScript type checking
   - Unit tests (Vitest/Jest)
   - Build validation

3. **Security Tests**
   - Trivy vulnerability scan
   - Python dependency check (Safety)
   - Secret detection (TruffleHog)

---

## 🚀 Deploy Staging

### Configuração

**Arquivo**: `.env.staging`

```bash
ENVIRONMENT=staging
DATABASE_URL=postgresql://user:pass@postgres:5432/sila_staging
SECRET_KEY=your-staging-secret-key
# ... outras variáveis
```

### Deploy Manual

```bash
# Executar script de deploy
./scripts/deploy_staging.sh
```

### Fluxo de Deploy Staging

```
1. Validação de Ambiente
   ├─ Verificar .env.staging
   ├─ Validar variáveis obrigatórias
   └─ Verificar dependências

2. Backup
   ├─ Backup do banco de dados
   └─ Salvar estado dos containers

3. Deploy
   ├─ Pull do código (branch staging)
   ├─ Build das imagens Docker
   └─ Subir novos containers

4. Healthcheck
   ├─ Aguardar backend (120s max)
   ├─ Verificar métricas
   └─ Validar API docs

5. Smoke Tests
   ├─ Test /health endpoint
   ├─ Test /docs endpoint
   ├─ Test /metrics endpoint
   └─ Verificar containers

6. Monitoramento
   ├─ Verificar logs
   ├─ Checar recursos (CPU/RAM)
   └─ Confirmar deploy
```

### Deploy Automático (CI/CD)

O deploy para staging é **automático** ao fazer push para a branch `staging`:

```bash
git checkout staging
git merge develop
git push origin staging
# GitHub Actions executa deploy automaticamente
```

### Rollback

Em caso de falha, o script executa rollback automático:

```bash
# Rollback manual
docker compose down
# Restaurar último backup
gunzip -c /opt/sila-backups/sila_staging_*.sql.gz | \
  docker compose exec -T postgres psql -U sila_staging sila_staging
```

---

## 🏭 Deploy Produção

### Pré-requisitos

- ✅ Testes passando em staging
- ✅ Aprovação de code review
- ✅ Merge para branch `main`
- ✅ Secrets configurados no GitHub

### Configuração de Secrets

No GitHub: `Settings > Secrets and variables > Actions`

```
PROD_SSH_KEY          # Chave SSH para servidor de produção
PROD_HOST             # Hostname do servidor
PROD_USER             # Usuário SSH
DOCKER_HUB_USERNAME   # Docker Hub username
DOCKER_HUB_TOKEN      # Docker Hub token
```

### Deploy Manual

```bash
# No servidor de produção
cd /opt/sila-system
git pull origin main
./sila_start.sh production
```

### Deploy Automático

Push para `main` dispara deploy automático:

```bash
git checkout main
git merge staging
git push origin main
# GitHub Actions executa deploy
```

### Checklist Pré-Deploy

- [ ] Todos os testes passando
- [ ] Code review aprovado
- [ ] Changelog atualizado
- [ ] Backup do banco de dados
- [ ] Notificar equipe
- [ ] Janela de manutenção agendada

### Validação Pós-Deploy

```bash
# Healthcheck
curl https://sila-system.com/health

# Verificar métricas
curl https://sila-system.com/metrics

# Smoke tests
./scripts/run_tests.sh smoke
```

---

## 📊 Monitoramento

### Monitoramento Contínuo

```bash
# Iniciar monitoramento (intervalo de 30s)
./scripts/monitor_system.sh 30
```

### Métricas Monitoradas

- **Healthcheck**: Status do backend
- **Container Resources**: CPU, memória, disco
- **Database**: Conexão e performance
- **Application Metrics**: Requests, latência, erros
- **Logs**: Erros e exceções recentes

### Dashboard de Monitoramento

```
╔═══════════════════════════════════════════════════════════════╗
║                    Monitoring Summary                        ║
╚═══════════════════════════════════════════════════════════════╝

  ✅ Healthcheck: OK
  ✅ Database: OK
  ✅ Containers: 4/4 healthy

  CPU Usage:
    backend:   45%
    frontend:  12%
    postgres:  23%
    redis:     8%

  Memory Usage:
    backend:   512MB / 1GB (51%)
    frontend:  128MB / 512MB (25%)
    postgres:  256MB / 1GB (25%)
    redis:     64MB / 256MB (25%)

  Disk Usage: 45%

  Recent Errors: 0

  Next check in: 30s
```

### Alertas

O sistema alerta quando:

- CPU > 80%
- Memória > 80%
- Disco > 90%
- Healthcheck falha
- Erros nos logs
- Container unhealthy

### Integração com Prometheus/Grafana

```yaml
# Métricas disponíveis em:
http://localhost:9111/metrics

# Principais métricas:
- http_requests_total
- http_request_duration_seconds
- process_cpu_seconds_total
- process_resident_memory_bytes
- database_connections_active
```

---

## 🔧 Troubleshooting

### Deploy Falha

**Problema**: Deploy falha no healthcheck

```bash
# Verificar logs
docker compose logs backend

# Verificar status
./status_sila.sh

# Tentar restart
docker compose restart backend

# Se persistir, rollback
./scripts/deploy_staging.sh  # Executa rollback automático
```

### Testes Falhando

**Problema**: Testes unitários falhando

```bash
# Executar testes com verbose
cd backend
pytest -vv tests/

# Verificar coverage
pytest --cov-report=term-missing

# Executar teste específico
pytest tests/test_specific.py::test_function -vv
```

### Container Unhealthy

**Problema**: Container marcado como unhealthy

```bash
# Verificar healthcheck
docker inspect <container_id> | grep -A 10 Health

# Ver logs
docker logs <container_id> --tail 100

# Restart container
docker compose restart <service_name>
```

### Banco de Dados

**Problema**: Erro de conexão com banco

```bash
# Verificar se PostgreSQL está rodando
docker compose ps postgres

# Testar conexão
docker compose exec postgres pg_isready -U postgres

# Ver logs do PostgreSQL
docker compose logs postgres

# Restart PostgreSQL
docker compose restart postgres
```

### Performance Issues

**Problema**: Sistema lento

```bash
# Monitorar recursos
./scripts/monitor_system.sh 10

# Ver estatísticas Docker
docker stats

# Verificar logs por erros
docker compose logs | grep -i error

# Analisar métricas
curl http://localhost:9111/metrics | grep duration
```

---

## 📚 Recursos Adicionais

### Scripts Disponíveis

| Script                      | Descrição                |
| --------------------------- | ------------------------ |
| `sila_start.sh`             | Inicialização do sistema |
| `sila_stop.sh`              | Encerramento seguro      |
| `status_sila.sh`            | Status e healthcheck     |
| `scripts/run_tests.sh`      | Testes automatizados     |
| `scripts/deploy_staging.sh` | Deploy staging           |
| `scripts/monitor_system.sh` | Monitoramento contínuo   |
| `scripts/build_frontend.sh` | Build do frontend        |

### Workflows GitHub Actions

| Workflow        | Trigger | Descrição               |
| --------------- | ------- | ----------------------- |
| `msic-cicd.yml` | Push/PR | Pipeline completo CI/CD |
| `ci-cd.yml`     | Push    | Pipeline legado         |

### Documentação

- [SCRIPTS_ORQUESTRACAO.md](SCRIPTS_ORQUESTRACAO.md) - Scripts de orquestração
- [ARQUITETURA.md](ARQUITETURA.md) - Arquitetura do sistema
- [README.md](README.md) - Documentação principal

---

## 🎓 Boas Práticas

### Desenvolvimento

1. **Sempre criar branch** para novas features
2. **Escrever testes** antes de implementar
3. **Executar testes localmente** antes de push
4. **Manter coverage** acima de 80%
5. **Seguir padrões** de código (linting)

### Deploy

1. **Testar em staging** antes de produção
2. **Fazer backup** antes de deploy
3. **Validar healthcheck** pós-deploy
4. **Monitorar logs** após deploy
5. **Ter plano de rollback** pronto

### Segurança

1. **Nunca commitar secrets** em código
2. **Usar variáveis de ambiente** para credenciais
3. **Manter dependências** atualizadas
4. **Executar security scan** regularmente
5. **Revisar logs** de segurança

### Monitoramento

1. **Configurar alertas** para métricas críticas
2. **Revisar logs** diariamente
3. **Monitorar recursos** (CPU, RAM, disco)
4. **Validar backups** regularmente
5. **Documentar incidentes** e soluções

---

## 📞 Suporte

Em caso de problemas:

1. Verificar logs: `docker compose logs -f`
2. Executar status: `./status_sila.sh`
3. Consultar troubleshooting acima
4. Verificar issues no GitHub
5. Contatar equipe de DevOps

---

**Versão**: 4.0 **Última Atualização**: 2025-01-06 **Autor**: SILA System DevOps Team
