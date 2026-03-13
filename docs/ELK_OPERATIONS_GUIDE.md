# 🔧 Guia de Operação do Stack ELK - Fase 18.1

## Conteúdo
1. [Iniciar Stack](#iniciar-stack)
2. [Verificar Status](#verificar-status)
3. [Criar Dashboards](#criar-dashboards)
4. [Queries KQL](#queries-kql)
5. [Troubleshooting](#troubleshooting)

---

## Iniciar Stack

### Pré-requisitos
- Docker e Docker Compose instalados
- WSL2 com Ubuntu 24.04 ou equivalente

### Comando de Inicialização

```bash
# Navegar até o diretório raiz do projeto
cd /home/dev03wsl/sila-system

# Iniciar stack ELK (além do Redis que já existe)
docker-compose -f docker-compose.elk.yml up -d

# Verificar status
docker-compose -f docker-compose.elk.yml ps
```

### Esperar pela Inicialização

O stack leva ~60 segundos para estar pronto:

```bash
# Verificar Elasticsearch
curl -s http://localhost:9200 | jq .

# Verificar Kibana
curl -s http://localhost:5601/api/status | jq .
```

---

## Verificar Status

### Endpoints

| Serviço | URL |
|---------|-----|
| **Elasticsearch** | http://localhost:9200 |
| **Kibana** | http://localhost:5601 |
| **Logstash** | http://localhost:9600 |
| **Redis** | localhost:6379 |

### Health Check

```bash
# Todos os serviços
docker-compose -f docker-compose.elk.yml ps

# Logs específicos
docker-compose -f docker-compose.elk.yml logs elasticsearch
docker-compose -f docker-compose.elk.yml logs logstash
docker-compose -f docker-compose.elk.yml logs filebeat
docker-compose -f docker-compose.elk.yml logs kibana
```

---

## Criar Dashboards

### 1. Acessar Kibana

Abra: http://localhost:5601

### 2. Criar Index Pattern

**Menu → Analytics → Discover**

1. Clique em "Create index pattern"
2. Nome: `sila-audit-*`
3. Selecione `@timestamp` como time field
4. Clique "Create index pattern"

### 3. Dashboard 1: Login Events

**Menu → Dashboards → Create Dashboard**

#### Visualization 1: Login Events by User

```
Type: Pie Chart
Index: sila-audit-*

Metrics: Count
Buckets: Terms (user_id, size 10)

Filter: action: "UPDATE_LOGIN"
```

#### Visualization 2: Timeline de Logins

```
Type: Area Chart
Index: sila-audit-*

X-Axis: Date(@timestamp)
Y-Axis: Count
Split series: Terms (action)

Filter: tags: "login_event"
```

#### Visualization 3: Failed Logins

```
Type: Table
Index: sila-audit-*

Metric: Count
Buckets:
  - Terms: user_id
  - Terms: source_ip

Order: Descending

Filter: action: "INCREMENT_FAILED"
```

### 4. Dashboard 2: Session Lifecycle

**Create New Visualization**

#### Visualization 1: Sessions Revoked

```
Type: Metric
Index: sila-audit-*

Count with filter:
  action: REVOKE OR action: REVOKE_ALL

Display: Revoked Sessions
```

#### Visualization 2: Session Events Timeline

```
Type: Bar Chart
Index: sila-audit-*

X-Axis: Date(@timestamp)
Y-Axis: Count
Split series: Terms (action)

Filter: resource: "SESSION"
```

#### Visualization 3: Revocation Activity

```
Type: Heatmap
Index: sila-audit-*

Rows: Terms (user_id)
Columns: Date(@timestamp)
Values: Count

Filter: tags: "revocation_event"
```

### 5. Dashboard 3: Audit Trail

#### Visualization 1: All Audit Events

```
Type: Table
Index: sila-audit-*

Columns:
  - @timestamp
  - user_id
  - tenant_id
  - action
  - resource
  - status

Sort: @timestamp DESC
```

#### Visualization 2: Event Distribution

```
Type: Pie Chart
Index: sila-audit-*

Metric: Count
Buckets: Terms (action)
```

#### Visualization 3: By Tenant

```
Type: Bar Chart
Index: sila-audit-*

X-Axis: Terms (tenant_id)
Y-Axis: Count
Split series: Terms (action)
```

---

## Queries KQL

### KQL Patterns para Investigação

#### 1. Buscar por Usuário

```
user_id: "550e8400-e29b-41d4-a716-446655440000"
```

#### 2. Buscar por Tenant

```
tenant_id: "LUANDA" AND @timestamp >= now-24h
```

#### 3. Buscar Falhas de Login

```
action: "INCREMENT_FAILED" AND action: "INCREMENT_FAILED"
```

#### 4. Buscar Revogações

```
tags: "revocation_event" AND @timestamp >= now-7d
```

#### 5. Buscar por IP

```
source_ip: "192.168.1.*"
```

#### 6. Buscar por Roles (Adm/Manager)

```
roles: ("admin" or "manager") AND @timestamp >= now-1h
```

#### 7. Criar Alertas de Anomalia

```
# Muitas falhas de login em pouco tempo
action: "INCREMENT_FAILED" AND @timestamp >= now-10m | stats count by user_id
# Se count > 3, disparar alerta
```

#### 8. Rastrear Request através de Trace

```
request_id: "abc123" OR trace_id: "abc123"
```

#### 9. Buscar Password Changes

```
action: "UPDATE_PASSWORD"
```

#### 10. Buscar Cleanup Automático

```
action: "CLEANUP"
```

---

## Troubleshooting

### Problema: Elasticsearch não inicia

```bash
# Verificar logs
docker-compose -f docker-compose.elk.yml logs elasticsearch

# Limpar e reiniciar
docker-compose -f docker-compose.elk.yml down -v
docker-compose -f docker-compose.elk.yml up -d elasticsearch
```

### Problema: Logstash não processa eventos

```bash
# Verificar se há erros na pipeline
docker-compose -f docker-compose.elk.yml logs logstash | tail -50

# Recarregar o arquivo de configuração
docker exec logstash curl -X POST http://localhost:9600/_node/reload_pipelines \
  -H 'Content-Type: application/json' \
  -d '{"target": "main"}'
```

### Problema: Filebeat não coleta logs

```bash
# Verificar permissões
docker exec filebeat ls -la /var/lib/docker/containers

# Reiniciar Filebeat
docker-compose -f docker-compose.elk.yml restart filebeat
```

### Problema: Kibana não exibe dados

1. Esperar 2-3 minutos após inicialização
2. Verificar index pattern: `sila-audit-*` foi criado?
3. Executar query simples em Discover:

```
request_id: *
```

### Limpar Dados (Reset Completo)

```bash
# Parar stack
docker-compose -f docker-compose.elk.yml down

# Remover volumes de dados
docker volume rm \
  sila-system_elasticsearch_data \
  sila-system_logstash_data \
  sila-system_filebeat_data

# Reiniciar
docker-compose -f docker-compose.elk.yml up -d
```

---

## Informações de Conexão para Aplicação

### Environment Variables (docker-compose da App)

```yaml
# Para publicar eventos no Logstash
LOGSTASH_HOST=logstash
LOGSTASH_PORT=5000

# Para usar Elasticsearch diretamente (opcional)
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200

# Para usar Kibana
KIBANA_URL=http://kibana:5601
```

### URL para Dashboard

- **Kibana**: http://localhost:5601
- **índex**: `sila-audit-*`
- **Time Field**: `@timestamp`

---

## Performance & Maintenance

### Rotação de Índices

Por padrão, índices são criados por dia: `sila-audit-YYYY.MM.dd`

Para limpar índices antigos:

```bash
# Deletar índices com mais de 30 dias
DELETE /sila-audit-2024.01.*
DELETE /sila-audit-2024.02.*
```

### Monitoramento de Disk Space

```bash
# Verificar uso de disco
docker exec elasticsearch curl -s http://localhost:9200/_cat/indices?v
```

### Aumentar Retenção

No `elasticsearch-template.json`, ajustar:

```json
"settings": {
  "index.lifecycle.name": "sila-audit-policy",
  "index.lifecycle.rollover_alias": "sila-audit",
  "index.lifecycle.parse_strict_size_type": true,
  "index.routing.allocation.total_shards_per_node": 5
}
```

---

## Próximos Passos

1. ✅ Stack ELK inicializado
2. ✅ Filebeat coleta logs dos containers
3. ✅ Logstash processa e enriquece eventos
4. ✅ Elasticsearch indexa com fields específicos
5. ✅ Kibana visualiza dados em dashboards

**Próxima Fase**: 
- Integrar Application Insights (APM)
- Configurar alertas automáticos
- Exportar relatórios de conformidade
