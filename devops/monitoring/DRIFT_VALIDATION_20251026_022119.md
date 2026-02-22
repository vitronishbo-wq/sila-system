# Relatório de Validação de Drift - Monitoring

## Data: Sun Oct 26 02:21:19 UTC 2025

## Status: ❌ DRIFT DETECTADO

### 📋 Resumo da Validação:

- **Fonte única de verdade**: devops/monitoring/docker-compose.monitoring.yml ✅
- **Duplicações removidas**: ❌ Não
- **Rede monitoring**: ✅ External
- **Backend configurado**: ✅ Sim
- **Versões fixas**: ✅ Sim

### 🎯 Stack de Monitoring Validado:

- ✅ Prometheus: v2.40.0
- ✅ Grafana: 9.3.0 (com plugins e provisioning)
- ✅ Jaeger: 1.42 (tracing completo)
- ✅ AlertManager: Configurado para alertas
- ✅ Loki: Agregação de logs
- ✅ Promtail: Coleta de logs
- ✅ CAdvisor: Métricas de containers
- ✅ Node-exporter: Métricas do sistema

### 🚨 Ações Pendentes:

- ❌ Remover duplicações de devops/docker-compose.yml
- ❌ Remover duplicações de docker-compose.production.yml
- ⚠️ Criar diretórios de provisionamento faltando

### ✅ Como usar o sistema de monitoring:

```bash
# Iniciar apenas o stack de monitoring
docker-compose -f devops/monitoring/docker-compose.monitoring.yml up -d

# Verificar status
docker-compose -f devops/monitoring/docker-compose.monitoring.yml ps

# Ver logs
docker-compose -f devops/monitoring/docker-compose.monitoring.yml logs -f prometheus
```

**Relatório gerado por:** Script de validação automática - Fase 3.2
