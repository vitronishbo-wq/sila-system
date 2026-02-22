# 🚀 Guia Completo de CI/CD com GitHub Actions

## 📋 Visão Geral

Este repositório possui um pipeline CI/CD completo usando GitHub Actions que automatiza:

- ✅ **Testes automatizados** com cobertura de código
- ✅ **Construção e publicação de imagens Docker**
- ✅ **Deploy automático** para ambientes DEV e PROD
- ✅ **Varredura de segurança** com múltiplas ferramentas
- ✅ **Monitoramento e métricas** com Prometheus/Grafana
- ✅ **Notificações** via Slack/Discord
- ✅ **Estratégia de rollback** em caso de falha

## 🔐 Configuração de Secrets no GitHub

### Secrets Obrigatórios

Acesse **Settings > Secrets and variables > Actions** no seu repositório e adicione:

#### Para Deploy

```bash
DEPLOY_HOST=seu-servidor-dev.com
DEPLOY_USER=seu-usuario
DEPLOY_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----...-----END OPENSSH PRIVATE KEY-----

PROD_HOST=seu-servidor-prod.com
PROD_USER=seu-usuario-prod
PROD_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----...-----END OPENSSH PRIVATE KEY-----
```

#### Para Docker Registry

```bash
DOCKER_HUB_USERNAME=seu_usuario_docker
DOCKER_HUB_TOKEN=seu_token_docker_hub
```

#### Para Notificações

```bash
SLACK_WEBHOOK_URL=[REMOVED]
```

#### Para Segurança e Monitoramento

```bash
SECRET_KEY=sua-chave-secreta-para-jwt
SENTRY_DSN=https://sentry-dsn
```

## 🏗️ Arquivos de Workflow

### 1. `ci-cd.yml` - Pipeline Principal

- **Build e Test**: Executa testes com PostgreSQL
- **Docker Build**: Constrói e publica imagens
- **Deploy**: Deploy automático baseado na branch
- **Segurança**: Varredura com Trivy, CodeQL e GitLeaks

### 2. `notifications.yml` - Notificações

- Notifica sucesso/falha via Slack e Discord
- Integrado com outros workflows

### 3. `rollback.yml` - Rollback Manual

- Permite rollback para commit anterior
- Disponível via GitHub Actions UI

## 🌍 Deploy por Ambiente

### Ambiente de Desenvolvimento (develop branch)

- Deploy automático quando há push na branch `develop`
- Usa `docker-compose.yml` padrão

### Ambiente de Produção (main branch)

- Deploy automático quando há push na branch `main`
- Usa `docker-compose.prod.yml` otimizado
- Inclui validação prévia com `env_validator.py`

## 🔒 Recursos de Segurança

### Varredura de Vulnerabilidades

- **Trivy**: Análise de dependências e imagens
- **CodeQL**: Análise estática de código Python
- **GitLeaks**: Detecção de secrets e credenciais

### Boas Práticas Implementadas

- Secrets criptografados no GitHub
- Validação de ambiente antes do deploy
- Health checks pós-deploy
- Logs de auditoria

## 📊 Monitoramento

### Métricas Disponíveis

- Endpoint `/metrics` com Prometheus
- Dashboards no Grafana (porta 3000)
- Métricas de requests, erros e performance

### Logs e Tracing

- Integração com Sentry para rastreamento de erros
- Logs estruturados no container

## 🚨 Procedimentos de Emergência

### Rollback Manual

1. Vá para **Actions** no GitHub
2. Selecione **Rollback Deployment**
3. Escolha o ambiente e confirme

### Rollback Automático (Futuro)

- Pode ser implementado verificando health checks
- Restaura automaticamente o último commit funcional

## 🔧 Comandos Úteis para Deploy Manual

```bash
# Deploy DEV
git push origin develop

# Deploy PROD
git push origin main

# Verificar status
curl http://seu-servidor/health

# Ver métricas
curl http://seu-servidor/metrics

# Logs do container
docker-compose logs -f backend
```

## 📈 Próximas Melhorias

1. **CDN Integration**: CloudFlare ou AWS CloudFront
2. **Blue-Green Deploy**: Zero-downtime deployments
3. **Performance Testing**: Load testing com k6 ou Artillery
4. **Database Migrations**: Migrações automatizadas com Alembic
5. **Multi-Region Deploy**: Suporte a múltiplas regiões

## 🆘 Suporte

Para problemas com CI/CD:

1. Verifique os logs no **Actions** tab
2. Teste manualmente com `docker-compose up`
3. Verifique configurações de secrets
4. Abra issue no repositório se necessário

---

🎉 **Seu pipeline está pronto!** Cada push na branch correta triggerá automaticamente o
deploy completo.
