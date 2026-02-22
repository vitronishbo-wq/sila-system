# ⚡ Quick Start - CI/CD & Deploy

Guia rápido para começar a usar o sistema de CI/CD e deploy do SILA System.

## 🚀 Início Rápido (5 minutos)

### 1. Configurar Ambiente Local

```bash
# Clonar repositório
git clone <repo-url>
cd sila-system

# Dar permissões aos scripts
chmod +x sila_start.sh sila_stop.sh status_sila.sh
chmod +x scripts/*.sh

# Iniciar sistema
./sila_start.sh dev
```

### 2. Executar Testes

```bash
# Todos os testes
./scripts/run_tests.sh all

# Apenas testes rápidos
./scripts/run_tests.sh unit
./scripts/run_tests.sh smoke
```

### 3. Verificar Status

```bash
# Status completo
./status_sila.sh

# Monitoramento contínuo
./scripts/monitor_system.sh 30
```

---

## 📋 Workflows Comuns

### Desenvolver Nova Feature

```bash
# 1. Criar branch
git checkout -b feature/nova-funcionalidade

# 2. Desenvolver e testar localmente
./scripts/run_tests.sh all

# 3. Commit e push
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade

# 4. Criar Pull Request no GitHub
# CI/CD executa automaticamente:
# - Validação MSIC
# - Testes backend
# - Testes frontend
# - Security scan
```

### Deploy para Staging

```bash
# Opção 1: Automático (recomendado)
git checkout staging
git merge develop
git push origin staging
# GitHub Actions faz deploy automaticamente

# Opção 2: Manual
./scripts/deploy_staging.sh
```

### Deploy para Produção

```bash
# Sempre via Git (automático)
git checkout main
git merge staging
git push origin main
# GitHub Actions faz deploy automaticamente
```

---

## 🔍 Comandos Essenciais

### Desenvolvimento

| Comando                  | Descrição                        |
| ------------------------ | -------------------------------- |
| `./sila_start.sh dev`    | Iniciar ambiente desenvolvimento |
| `./sila_stop.sh`         | Parar todos os containers        |
| `./status_sila.sh`       | Verificar status do sistema      |
| `docker compose logs -f` | Ver logs em tempo real           |

### Testes

| Comando                        | Descrição                    |
| ------------------------------ | ---------------------------- |
| `./scripts/run_tests.sh all`   | Executar todos os testes     |
| `./scripts/run_tests.sh unit`  | Apenas testes unitários      |
| `./scripts/run_tests.sh smoke` | Smoke tests rápidos          |
| `pytest -v`                    | Testes com verbose (backend) |

### Deploy

| Comando                       | Descrição                  |
| ----------------------------- | -------------------------- |
| `./scripts/deploy_staging.sh` | Deploy manual para staging |
| `git push origin staging`     | Deploy automático staging  |
| `git push origin main`        | Deploy automático produção |

### Monitoramento

| Comando                          | Descrição               |
| -------------------------------- | ----------------------- |
| `./scripts/monitor_system.sh 30` | Monitoramento contínuo  |
| `curl localhost:9111/health`     | Healthcheck manual      |
| `curl localhost:9111/metrics`    | Ver métricas            |
| `docker stats`                   | Recursos dos containers |

---

## 🎯 Checklist de Deploy

### Antes do Deploy

- [ ] Todos os testes passando localmente
- [ ] Code review aprovado
- [ ] Branch atualizada com develop/staging
- [ ] Changelog atualizado
- [ ] Variáveis de ambiente configuradas

### Durante o Deploy

- [ ] Monitorar logs do GitHub Actions
- [ ] Aguardar healthcheck passar
- [ ] Verificar smoke tests
- [ ] Confirmar containers healthy

### Após o Deploy

- [ ] Testar endpoints principais
- [ ] Verificar métricas
- [ ] Monitorar logs por 15 minutos
- [ ] Notificar equipe

---

## 🚨 Troubleshooting Rápido

### Testes Falhando

```bash
# Ver detalhes do erro
./scripts/run_tests.sh unit -vv

# Limpar cache e tentar novamente
docker compose down -v
./sila_start.sh dev
./scripts/run_tests.sh all
```

### Deploy Falhou

```bash
# Ver logs do GitHub Actions
# Ir para: Actions > Workflow > Job que falhou

# Deploy manual para investigar
./scripts/deploy_staging.sh

# Ver logs detalhados
docker compose logs backend --tail 100
```

### Container Unhealthy

```bash
# Verificar status
./status_sila.sh

# Ver logs
docker compose logs <service> --tail 50

# Restart
docker compose restart <service>

# Se persistir, rebuild
docker compose down
./sila_start.sh dev
```

### Healthcheck Timeout

```bash
# Verificar se serviço está rodando
docker compose ps

# Ver logs do backend
docker compose logs backend

# Testar healthcheck manualmente
curl -v http://localhost:9111/health

# Aumentar timeout (se necessário)
# Editar MAX_WAIT_SECONDS em sila_start.sh
```

---

## 📚 Documentação Completa

- **[CICD_DEPLOY_GUIDE.md](CICD_DEPLOY_GUIDE.md)** - Guia completo de CI/CD
- **[AUTOMATION_SUMMARY.md](AUTOMATION_SUMMARY.md)** - Resumo executivo
- **[SCRIPTS_ORQUESTRACAO.md](SCRIPTS_ORQUESTRACAO.md)** - Scripts de orquestração
- **[README.md](README.md)** - Documentação principal

---

## 🔗 Links Úteis

### Local

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Healthcheck: http://localhost:9111/health
- Métricas: http://localhost:9111/metrics

### Staging

- Frontend: http://staging.sila-system.com
- Backend API: http://staging.sila-system.com:8000
- API Docs: http://staging.sila-system.com:8000/docs

### Production

- Frontend: https://sila-system.com
- Backend API: https://api.sila-system.com
- API Docs: https://api.sila-system.com/docs

---

## 💡 Dicas

### Performance

- Use `docker compose build --parallel` para builds mais rápidos
- Configure cache do npm/pip para acelerar instalação
- Use `--no-cache` apenas quando necessário

### Debugging

- Adicione `set -x` no início dos scripts para debug
- Use `docker compose logs -f <service>` para logs em tempo real
- Configure `LOG_LEVEL=DEBUG` para mais detalhes

### Segurança

- Nunca commite arquivos `.env.*` com credenciais reais
- Use secrets do GitHub para variáveis sensíveis
- Execute `git secrets --scan` antes de push

---

## ✅ Próximos Passos

1. **Configurar Secrets no GitHub**

   - Settings > Secrets and variables > Actions
   - Adicionar: SSH_KEY, DOCKER_HUB_TOKEN, etc.

2. **Testar Pipeline CI/CD**

   - Criar branch de teste
   - Fazer push
   - Verificar GitHub Actions

3. **Configurar Monitoramento**

   - Configurar alertas (Slack/Discord)
   - Configurar Grafana/Prometheus
   - Definir SLAs e SLOs

4. **Documentar Processos**
   - Runbooks para incidentes
   - Procedimentos de rollback
   - Contatos de emergência

---

**Pronto para começar!** 🚀

Para ajuda: `./sila_start.sh --help` ou consulte a documentação completa.
