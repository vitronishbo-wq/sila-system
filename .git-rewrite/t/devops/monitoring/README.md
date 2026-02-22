# 📊 SILA System - Unified Monitoring Configuration

> **🚨 FASE 3.2 COMPLETA: Single Source of Truth** for all monitoring infrastructure
> configurations
>
> **Status:** ✅ **DRIFT ELIMINADO** - Configurações duplicadas removidas, fonte única
> validada

This directory is the **authoritative location** for all monitoring configurations in
the SILA project. All Prometheus, Grafana, and alerting configurations must reside here
to prevent config drift and ensure consistency across environments.

---

## 🏆 FASE 3.2: ELIMINAÇÃO DE DRIFT - RESULTADO

### ✅ **Problema Resolvido:**

- ❌ **ANTES:** Configurações duplicadas em 3 arquivos diferentes
- ✅ **DEPOIS:** `docker-compose.monitoring.yml` como fonte única de verdade

### 📋 **Arquivos Corrigidos:**

1. ✅ `devops/docker-compose.yml` - Configurações duplicadas removidas
2. ✅ `docker-compose.production.yml` - Configurações duplicadas removidas
3. ✅ `backend/core/config.py` - Endpoints atualizados para nomes de container corretos

### 🎯 **Stack de Monitoring Completo:**

- ✅ **Prometheus** (v2.40.0) - Coleta de métricas
- ✅ **Grafana** (9.3.0) - Dashboards e visualização
- ✅ **Jaeger** (1.42) - Distributed tracing
- ✅ **AlertManager** (v0.25.0) - Gerenciamento de alertas
- ✅ **Loki** (2.8.0) - Agregação de logs
- ✅ **Promtail** (2.8.0) - Coleta de logs
- ✅ **CAdvisor** (v0.46.0) - Métricas de containers
- ✅ **Node-exporter** (v1.5.0) - Métricas do sistema

---

## 📁 Directory Structure

```
devops/monitoring/
├── README.md                           # This file (updated for Phase 3.2)
├── DRIFT_AUDIT_REPORT.md              # Audit report from Phase 3.2
├── validate_drift.sh                   # Drift validation script
├── docker-compose.monitoring.yml       # ✅ SINGLE SOURCE OF TRUTH
├── prometheus/
│   ├── prometheus.yml                  # Main Prometheus configuration
│   └── rules/
│       └── sila-alerts.yml            # Alert rules and thresholds
├── grafana/
│   ├── dashboards/                     # Pre-configured dashboards
│   │   ├── sila-overview.json         # System overview dashboard
│   │   └── ...                         # Other dashboards
│   └── provisioning/                   # Grafana auto-provisioning configs
│       ├── datasources/               # Data source definitions
│       ├── dashboards/                # Dashboard provisioning
│       └── alerting/                  # Grafana alerting config
└── alertmanager/
    └── alertmanager.yml               # Alertmanager configuration
```

---

## 🚀 How to Use (Post-Phase 3.2)

### **Start Monitoring Stack:**

```bash
# ✅ CORRETO - Usar apenas a fonte única
docker-compose -f devops/monitoring/docker-compose.monitoring.yml up -d

# ❌ ERRADO - Não usar mais (duplicações removidas)
# docker-compose up prometheus grafana  # Isso não funciona mais
```

### **Access Services:**

| Service           | URL                    | Credentials             | Description                   |
| ----------------- | ---------------------- | ----------------------- | ----------------------------- |
| **Prometheus**    | http://localhost:9090  | -                       | Metrics collection & querying |
| **Grafana**       | http://localhost:3000  | admin/Truman1*Marcelo1* | Dashboards & visualization    |
| **Jaeger**        | http://localhost:16686 | -                       | Distributed tracing UI        |
| **AlertManager**  | http://localhost:9093  | -                       | Alert management              |
| **Loki**          | http://localhost:3100  | -                       | Log aggregation API           |
| **CAdvisor**      | http://localhost:8080  | -                       | Container metrics             |
| **Node-exporter** | http://localhost:9100  | -                       | System metrics                |

### **Stop Monitoring Stack:**

```bash
docker-compose -f devops/monitoring/docker-compose.monitoring.yml down
```

### **View Logs:**

```bash
# Todos os logs
docker-compose -f devops/monitoring/docker-compose.monitoring.yml logs -f

# Logs específicos
docker-compose -f devops/monitoring/docker-compose.monitoring.yml logs -f prometheus
docker-compose -f devops/monitoring/docker-compose.monitoring.yml logs -f grafana
```

### **Validate Configuration (Phase 3.2):**

```bash
# Executar validação automática de drift
./devops/monitoring/validate_drift.sh

# Verificar status dos serviços
docker-compose -f devops/monitoring/docker-compose.monitoring.yml ps
```

---

## 🎯 Development Workflow

### **1. Make Changes Only Here:**

```bash
# ❌ ERRADO - Não editar outros arquivos
vim devops/docker-compose.yml      # Não fazer mais
vim docker-compose.production.yml  # Não fazer mais

# ✅ CORRETO - Editar apenas a fonte única
vim devops/monitoring/docker-compose.monitoring.yml
vim devops/monitoring/prometheus/prometheus.yml
vim devops/monitoring/grafana/dashboards/*.json
```

### **2. Test Changes:**

```bash
# Reiniciar apenas os serviços modificados
docker-compose -f devops/monitoring/docker-compose.monitoring.yml up -d prometheus grafana

# Verificar logs para erros
docker-compose -f devops/monitoring/docker-compose.monitoring.yml logs prometheus
```

### **3. Validate No Drift:**

```bash
# Executar validação automática
./devops/monitoring/validate_drift.sh
```

---

## 🔧 Backend Integration (Updated for Phase 3.2)

The backend is configured to send metrics to the monitoring stack:

```python
# In backend/core/config.py
PROMETHEUS_GATEWAY = "http://sila-prometheus:9090"  # ✅ Updated
GRAFANA_PASSWORD = "Truman1*Marcelo1*"                         # ✅ Updated
JAEGER_ENDPOINT = "http://sila-jaeger:14268"         # ✅ Updated
```

### **Environment Variables for Production:**

```bash
export PROMETHEUS_GATEWAY="http://sila-prometheus:9090"
export GRAFANA_PASSWORD="your_grafana_password"
export JAEGER_ENDPOINT="http://sila-jaeger:14268"
export LOKI_ENDPOINT="http://sila-loki:3100"
```

---

## 📊 Monitoring Features

### **Pre-configured Dashboards:**

- 🔍 **System Overview** - CPU, Memory, Disk, Network
- 📈 **Business Metrics** - API performance, user activity
- ⚡ **Performance** - Response times, throughput
- 💾 **Database** - Query performance, connections
- 🔒 **Security** - Failed logins, suspicious activity

### **Alert Rules:**

- 🚨 **Critical System Alerts** - Service down, high CPU
- ⚠️ **Warning Alerts** - High memory, slow responses
- 📊 **Business Alerts** - Unusual traffic patterns

### **Log Aggregation:**

- 📝 **Application Logs** - All backend/frontend logs
- 🔍 **Structured Logging** - JSON format with metadata
- 🎯 **Error Tracking** - Automatic error detection

---

## 🛠️ Troubleshooting (Post-Phase 3.2)

### **Common Issues:**

1. **"Service not found" errors:**

   ```bash
   # ✅ Solution: Use correct compose file
   docker-compose -f devops/monitoring/docker-compose.monitoring.yml up -d
   ```

2. **Port conflicts:**

   ```bash
   # Check what's using the ports
   netstat -tulpn | grep :9090
   netstat -tulpn | grep :3000

   # ✅ Solution: Stop conflicting services
   docker-compose -f devops/monitoring/docker-compose.monitoring.yml down
   ```

3. **Configuration drift detected:**
   ```bash
   # ✅ Solution: Run drift validation
   ./devops/monitoring/validate_drift.sh
   ```

### **Health Checks:**

```bash
# Prometheus health
curl http://localhost:9090/-/healthy

# Grafana health
curl http://localhost:3000/api/health

# Backend metrics endpoint
curl http://localhost:8000/monitoring/health/
```

---

## 📋 Maintenance (Phase 3.2 Compliant)

### **Adding New Metrics:**

1. Update `devops/monitoring/prometheus/prometheus.yml`
2. Add dashboard in `devops/monitoring/grafana/dashboards/`
3. Test with `./validate_drift.sh`
4. Commit changes

### **Updating Versions:**

1. Update versions in `docker-compose.monitoring.yml`
2. Test compatibility
3. Update this README
4. Run drift validation

### **Backup Configuration:**

```bash
# ✅ CORRETO - Backup apenas da fonte única
cp devops/monitoring/docker-compose.monitoring.yml devops/monitoring/backup_$(date +%Y%m%d).yml

# ❌ ERRADO - Não fazer backup de arquivos duplicados
# cp devops/docker-compose.yml backup/
```

---

## 🎉 Phase 3.2 Success Metrics

- ✅ **0 duplicações** de configuração de monitoring
- ✅ **1 fonte única** de verdade validada
- ✅ **8 serviços** de monitoring em stack completo
- ✅ **Validação automática** de drift implementada
- ✅ **Backend integrado** com endpoints corretos

**Result:** **Infrastructure monitoring is now drift-free and maintainable!** 🚀

---

_Updated for Phase 3.2: Drift Elimination - $(date)_

---

## 🚀 Usage

### Starting the Monitoring Stack

```bash
# From project root
cd /opt/sila-system/devops/monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

### Accessing Services

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/sila123)
- **Alertmanager**: http://localhost:9093

### Integration with Docker Compose

All production docker-compose files reference this directory:

```yaml
# Example from docker-compose.production.yml
volumes:
  - ./devops/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
  - ./devops/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
```

---

## 📝 Configuration Files

### Prometheus (`prometheus/prometheus.yml`)

Main Prometheus server configuration including:

- Scrape intervals and targets
- Service discovery configurations
- Remote write/read endpoints
- Storage retention policies

**Update Procedure**:

1. Edit `prometheus/prometheus.yml`
2. Validate syntax: `promtool check config prometheus/prometheus.yml`
3. Reload: `curl -X POST http://localhost:9090/-/reload`

### Alert Rules (`prometheus/rules/sila-alerts.yml`)

Defines alerting rules and thresholds:

- System health alerts (CPU, memory, disk)
- Application performance alerts
- Business metric alerts
- SLA violation alerts

**Update Procedure**:

1. Edit `prometheus/rules/sila-alerts.yml`
2. Validate: `promtool check rules prometheus/rules/sila-alerts.yml`
3. Reload Prometheus configuration

### Grafana Dashboards (`grafana/dashboards/*.json`)

Pre-configured dashboards for various monitoring needs:

- **sila-overview.json**: High-level system overview
- **sila-business.json**: Business KPIs and metrics
- **sila-performance.json**: Application performance metrics
- **sila-backup-monitoring.json**: Backup status and health

**Update Procedure**:

1. Edit dashboard in Grafana UI or modify JSON directly
2. Export from Grafana: Settings → JSON Model → Copy
3. Save to appropriate file in `grafana/dashboards/`
4. Commit to version control

### Grafana Provisioning (`grafana/provisioning/`)

Auto-provisioning configurations for:

- **datasources/**: Prometheus, Loki, and other data sources
- **dashboards/**: Dashboard auto-loading configuration
- **alerting/**: Grafana-managed alert rules

---

## 🔄 Update Procedures

### Adding a New Metric

1. Update application code to expose metric
2. Add scrape target to `prometheus/prometheus.yml` if needed
3. Create/update dashboard in `grafana/dashboards/`
4. Add alert rules to `prometheus/rules/sila-alerts.yml` if needed
5. Test in staging environment
6. Deploy to production

### Adding a New Dashboard

1. Create dashboard in Grafana UI
2. Export JSON: Dashboard Settings → JSON Model
3. Save to `grafana/dashboards/[name].json`
4. Commit and push to version control
5. Dashboard will auto-load on next Grafana restart

### Modifying Alert Thresholds

1. Edit `prometheus/rules/sila-alerts.yml`
2. Validate syntax with promtool
3. Reload Prometheus: `curl -X POST http://localhost:9090/-/reload`
4. Verify alerts in Prometheus UI: http://localhost:9090/alerts

---

## 🛡️ Best Practices

### Configuration Management

- ✅ **Always validate** configs before deployment
- ✅ **Test in staging** before production changes
- ✅ **Document changes** in commit messages
- ✅ **Review PRs** for monitoring config changes
- ❌ **Never create** duplicate monitoring configs elsewhere
- ❌ **Never hardcode** credentials in config files

### Naming Conventions

- **Metrics**: Use snake_case (e.g., `sila_request_duration_seconds`)
- **Labels**: Use lowercase with underscores (e.g., `service_name`, `environment`)
- **Dashboards**: Use kebab-case (e.g., `sila-overview.json`)
- **Alert Rules**: Use descriptive names (e.g., `HighCPUUsage`,
  `DatabaseConnectionPoolExhausted`)

### Alert Design

- Set appropriate thresholds to avoid alert fatigue
- Include runbook links in alert annotations
- Use severity labels: `critical`, `warning`, `info`
- Test alerts before deploying to production

---

## 🔗 Integration Points

### CI/CD Pipelines

All deployment scripts reference this directory:

- `docker-compose.production.yml`
- `docker-compose.prod.yml`
- `scripts/automated_backup.sh`
- `scripts/deploy_secret_key_production.sh`
- `scripts/rotate_secret_key.sh`
- `scripts/restore_backup.sh`

### Application Health Checks

Health check endpoint: `http://localhost:8000/monitoring/health/`

Referenced in:

- Docker Compose healthcheck configurations
- Kubernetes liveness/readiness probes
- Load balancer health checks

---

## 👥 Ownership & Maintenance

### Responsibilities

- **DevOps Team**: Infrastructure configuration, Prometheus setup, alert routing
- **Backend Team**: Application metrics, custom exporters, performance dashboards
- **SRE Team**: Alert rules, on-call runbooks, incident response dashboards

### Change Management

1. All changes must go through pull request review
2. Critical changes require approval from DevOps lead
3. Production changes should be deployed during maintenance windows
4. Document all changes in CHANGELOG.md

---

## 📚 Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- Internal Wiki: [SILA Monitoring Guide](link-to-internal-docs)

---

## 🚨 Troubleshooting

### Prometheus Not Scraping Targets

```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check Prometheus logs
docker logs sila-prometheus
```

### Grafana Dashboards Not Loading

```bash
# Check provisioning logs
docker logs sila-grafana | grep provisioning

# Verify dashboard files exist
ls -la grafana/dashboards/
```

### Alerts Not Firing

```bash
# Check alert rules
curl http://localhost:9090/api/v1/rules

# Validate alert rule syntax
promtool check rules prometheus/rules/sila-alerts.yml
```

---

## 📞 Support

For monitoring-related issues:

- **Slack**: #sila-monitoring
- **Email**: devops@sila-system.com
- **On-Call**: PagerDuty escalation policy

---

**Last Updated**: 2025-10-24 **Maintained By**: SILA DevOps Team
