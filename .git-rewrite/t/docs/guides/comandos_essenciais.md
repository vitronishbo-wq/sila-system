# 📋 COMANDOS ESSENCIAIS - SILA SYSTEM

# Referência rápida de todos os comandos automatizados

# Última atualização: $(date +'%Y-%m-%d %H:%M:%S')

# Versão: v2.0 - Sistema Multi-Ambiente + CI/CD + Monitoramento

---

## 🚀 DEPLOY MULTI-AMBIENTE

### **Deploy Básico por Ambiente**

```bash
# Desenvolvimento (sem push remoto)
./deploy_multi_ambiente.sh --env=dev

# Homologação (push limitado)
./deploy_multi_ambiente.sh --env=staging

# Produção (deploy completo)
./deploy_multi_ambiente.sh --env=prod
```

### **Deploy com Opções Avançadas**

```bash
# Modo dry-run (teste sem executar)
./deploy_multi_ambiente.sh --env=dev --dry-run

# Modo verboso (debug detalhado)
./deploy_multi_ambiente.sh --env=prod --verbose

# Modo CI/CD (não-interativo)
./deploy_multi_ambiente.sh --ci-mode --env=staging

# Ajuda completa
./deploy_multi_ambiente.sh --help
```

### **Deploy com CI/CD Manual**

```bash
# Simular GitHub Actions
GITHUB_REF_NAME=dev CI=true ./deploy_multi_ambiente.sh --ci-mode

# Simular GitLab CI
CI_COMMIT_BRANCH=staging CI=true ./deploy_multi_ambiente.sh --ci-mode
```

---

## 📊 MONITORAÇÃO E OBSERVABILIDADE

### **Interface TUI Principal**

```bash
# Monitoramento interativo
./monitor_sila.sh

# Monitoramento específico por ambiente
./monitor_sila.sh --env=prod

# Modo tempo real (monitoramento contínuo)
./monitor_sila.sh --realtime

# Exportar métricas para arquivo
./monitor_sila.sh --export > relatorio_$(date +%Y%m%d).txt

# Testar notificações
./monitor_sila.sh --notify-test
```

### **Verificação Rápida de Status**

```bash
# Containers ativos
docker ps

# Uso de sistema
df -h && free -h

# Últimos logs
tail -f logs/deploy_*.log | head -20
```

---

## 🐳 DOCKER COMPOSE

### **Inicialização por Ambiente**

```bash
# Desenvolvimento
docker compose -f docker-compose.dev.yml up -d

# Homologação
docker compose -f docker-compose.staging.yml up -d

# Produção
docker compose -f docker-compose.prod.yml up -d
```

### **Operações Básicas**

```bash
# Ver status dos containers
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Parar todos os containers
docker compose down

# Reiniciar serviços específicos
docker compose restart nome-do-servico
```

### **Manutenção**

```bash
# Limpar containers parados
docker compose down --remove-orphans

# Atualizar imagens
docker compose pull

# Recriar containers
docker compose up -d --force-recreate
```

---

## 📁 LOGS E MÉTRICAS

### **Visualização de Logs**

```bash
# Últimos logs de deploy
tail -f logs/deploy_*.log

# Logs específicos por ambiente
tail -f logs/deploy_dev_*.log
tail -f logs/deploy_staging_*.log
tail -f logs/deploy_prod_*.log

# Logs detalhados (últimas 50 linhas)
tail -n 50 logs/deploy_prod_$(date +%Y%m%d)*.log
```

### **Análise e Busca**

```bash
# Buscar erros nos logs
grep -r "ERROR" logs/ | head -10

# Buscar por ambiente específico
grep -r "prod" logs/deploy_prod_*.log

# Contar linhas por arquivo
wc -l logs/deploy_*.log
```

### **Limpeza e Organização**

```bash
# Listar logs antigos (>7 dias)
find logs/ -name "*.log" -mtime +7

# Remover logs antigos
find logs/ -name "*.log" -mtime +30 -delete
```

---

## 💾 BACKUP E ROLLBACK

### **Backups Disponíveis**

```bash
# Listar todos os backups
ls -lh backups/

# Backups por ambiente
ls -lh backups/*dev*.tar.gz
ls -lh backups/*prod*.tar.gz

# Últimos 5 backups
ls -lt backups/*.tar.gz | head -5
```

### **Operações de Backup**

```bash
# Criar backup manual
tar -czf "backup_manual_$(date +%Y%m%d_%H%M).tar.gz" -C /opt/sila-system .

# Verificar integridade do backup
tar -tzf backups/prod_backup_*.tar.gz | head -10

# Restaurar backup (CUIDADO!)
# tar -xzf backups/prod_backup_v1.0.0.tar.gz -C /opt/sila-system
```

### **Versionamento Git**

```bash
# Ver tags disponíveis
git tag | grep prod

# Ver histórico de commits
git log --oneline -10

# Ver diferenças entre versões
git diff v1.0.0 v1.1.0
```

---

## 🧪 TESTES E VALIDAÇÕES

### **Testes Básicos**

```bash
# Teste de conectividade
curl -f http://localhost:3001/health || echo "Serviço não responde"

# Teste de banco de dados
docker exec sila-db-prod pg_isready -U postgres

# Teste de Redis
docker exec sila-redis-prod redis-cli ping
```

### **Validações de Ambiente**

```bash
# Verificar variáveis de ambiente
docker compose -f docker-compose.prod.yml config

# Validar sintaxe YAML
yamllint docker-compose.*.yml

# Verificar dependências
docker compose -f docker-compose.dev.yml up --dry-run
```

---

## 🔧 MANUTENÇÃO E ADMINISTRAÇÃO

### **Limpeza do Sistema**

```bash
# Limpar containers Docker parados
docker container prune -f

# Limpar imagens não utilizadas
docker image prune -f

# Limpar volumes órfãos
docker volume prune -f

# Limpeza completa
docker system prune -a -f
```

### **Verificação de Saúde**

```bash
# Status geral do sistema
./monitor_sila.sh --export > health_check_$(date +%Y%m%d).txt

# Verificar serviços críticos
systemctl status docker
systemctl status postgresql

# Espaço em disco
df -h | grep -E '^/dev'
```

### **Atualizações**

```bash
# Atualizar sistema base
sudo apt update && sudo apt upgrade -y

# Atualizar Docker Compose
sudo apt install docker-compose-plugin

# Verificar versões
docker --version && docker compose version
```

---

## 🚨 SOLUÇÃO DE PROBLEMAS

### **Problemas Comuns**

```bash
# Docker não inicia
sudo systemctl restart docker

# Permissões de arquivos
sudo chown -R $USER:$USER /opt/sila-system

# Rede Docker com problemas
docker network prune -f

# Logs cheios (rotação)
find logs/ -name "*.log" -size +100M -exec rm {} \;
```

### **Debug Avançado**

```bash
# Logs detalhados do Docker
docker compose logs -f --tail=100

# Eventos do sistema
journalctl -u docker -f

# Processos consumindo recursos
top -p $(pgrep -f docker)
```

---

## 📚 DOCUMENTAÇÃO E AJUDA

### **Arquivos de Documentação**

```bash
# Guia de deploy multi-ambiente
cat README_DEPLOY_MULTI_AMBIENTE.md

# Guia de monitoramento
cat README_MONITOR_PRO.md

# Guia de CI/CD
cat README_CI_CD.md

# Changelog completo
cat CHANGELOG.md
```

### **Ajuda Rápida**

```bash
# Ajuda do deploy
./deploy_multi_ambiente.sh --help

# Ajuda do monitoramento
./monitor_sila.sh --help

# Versão atual do sistema
cat VERSION.txt
```

---

## 🎯 FLUXO DE TRABALHO RECOMENDADO

### **Desenvolvimento Diário**

```bash
# 1. Verificar status atual
./monitor_sila.sh --env=dev

# 2. Deploy de desenvolvimento
./deploy_multi_ambiente.sh --env=dev

# 3. Testar aplicação
curl http://localhost:3001

# 4. Commit e push
git add . && git commit -m "feat: melhoria X" && git push origin dev
```

### **Deploy para Produção**

```bash
# 1. Backup prévio
cp -r /opt/sila-system /opt/sila-system.backup.$(date +%Y%m%d)

# 2. Teste em staging
./deploy_multi_ambiente.sh --env=staging

# 3. Deploy produção
./deploy_multi_ambiente.sh --env=prod

# 4. Verificar funcionamento
./monitor_sila.sh --env=prod
```

---

## 📈 MÉTRICAS E MONITORAMENTO

### **Métricas Automáticas**

```bash
# Exportar métricas atuais
./monitor_sila.sh --export > metrics_$(date +%Y%m%d_%H%M).txt

# Comparar com baseline
diff metrics_baseline.txt metrics_atual.txt

# Gráfico simples de uso
echo "CPU:$(top -bn1 | grep Cpu | awk '{print $2}') RAM:$(free | grep Mem | awk '{printf "%.0f%%", $3/$2 * 100.0}')"
```

### **Alertas Manuais**

```bash
# Verificar uso de disco (>80%)
df -h | awk '{if(+ $5 > 80) print "ALERTA:" $1 " " $5 " cheio"}'

# Verificar containers parados
docker ps -f status=exited | grep -v NAMES && echo "Containers parados encontrados"
```

---

## 🔐 SEGURANÇA E PERMISSÕES

### **Permissões de Arquivos**

```bash
# Verificar permissões atuais
ls -la /opt/sila-system/

# Corrigir ownership
sudo chown -R $USER:$USER /opt/sila-system

# Scripts executáveis
chmod +x /opt/sila-system/*.sh
chmod +x /opt/sila-system/.github/workflows/*.yml
```

### **Variáveis Sensíveis**

```bash
# Verificar se há arquivos .env expostos
ls -la .env* 2>/dev/null || echo "Nenhum .env encontrado"

# Criar .env seguro (exemplo)
cat > .env.prod << EOF
DB_PASSWORD=senha_segura_$(openssl rand -hex 16)
JWT_SECRET=$(openssl rand -hex 32)
EOF
```

---

## 🚀 INTEGRAÇÃO CI/CD

### **GitHub Actions**

```bash
# Trigger manual de workflow
gh workflow run "Deploy Ambiente Dev"

# Ver status dos workflows
gh run list --workflow=deploy-dev.yml

# Ver logs de execução
gh run view $(gh run list --json databaseId --jq '.[0].databaseId')
```

### **GitLab CI**

```bash
# Trigger manual de pipeline
curl -X POST \
  -F token=glrt-xxxxxxxxxxxx \
  -F ref=main \
  https://gitlab.com/api/v4/projects/PROJECT_ID/trigger/pipeline

# Ver pipelines
curl "https://gitlab.com/api/v4/projects/PROJECT_ID/pipelines"
```

---

## 📋 CHECKLIST DE SAÚDE DO SISTEMA

### **Verificação Diária**

- [ ] Containers Docker ativos e saudáveis
- [ ] Logs sem erros críticos
- [ ] Espaço em disco suficiente (>20% livre)
- [ ] Backups recentes criados
- [ ] Deploy funcionando em todos os ambientes

### **Verificação Semanal**

- [ ] Atualizações de segurança aplicadas
- [ ] Limpeza de logs antigos
- [ ] Verificação de backups
- [ ] Teste de restore de backup
- [ ] Validação de CI/CD

### **Verificação Mensal**

- [ ] Análise de métricas de performance
- [ ] Revisão de logs de segurança
- [ ] Teste completo de failover
- [ ] Documentação atualizada
- [ ] Capacidade de armazenamento

---

## 🎯 COMANDOS MAIS USADOS (TOP 10)

1. **Deploy desenvolvimento:** `./deploy_multi_ambiente.sh --env=dev`
2. **Monitoramento:** `./monitor_sila.sh --env=prod`
3. **Status containers:** `docker ps`
4. **Logs recentes:** `tail -f logs/deploy_*.log`
5. **Deploy produção:** `./deploy_multi_ambiente.sh --env=prod`
6. **Backups disponíveis:** `ls -lh backups/`
7. **Teste containers:** `docker compose ps`
8. **Métricas export:** `./monitor_sila.sh --export`
9. **Limpeza sistema:** `docker system prune -f`
10. **Ajuda rápida:** `./deploy_multi_ambiente.sh --help`

---

## 📞 SUPORTE E CONTATO

### **Para Problemas**

1. Verifique os logs: `tail -f logs/deploy_*.log`
2. Use modo verboso: `--verbose`
3. Consulte documentação: `README_*.md`
4. Teste em modo dry-run: `--dry-run`

### **Para Melhorias**

- Abra issue no repositório Git
- Documente no arquivo de comandos
- Atualize documentação relacionada

---

**🎯 Arquivo mantido automaticamente pelo sistema SILA** **📅 Última atualização:
$(date)** **🔄 Atualize sempre que criar novos comandos automatizados**
