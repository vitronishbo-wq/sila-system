# Módulo Analytics (Dashboards e Relatórios)

# Sistema SILA - Backend

## 📋 Descrição

Módulo responsável pela geração de dashboards administrativos e relatórios estratégicos
no sistema SILA. Implementa funcionalidades avançadas para análise de dados, métricas de
performance, indicadores de gestão e visualizações interativas para tomada de decisões.

## 🚀 Funcionalidades Principais

- **Dashboards executivos** - Visão geral do sistema com KPIs estratégicos
- **Relatórios personalizáveis** - Geração automática de relatórios por período e
  categoria
- **Análise de tendências** - Identificação de padrões e forecasting
- **Métricas em tempo real** - Dados atualizados continuamente
- **Exportação de dados** - Formatos diversos (PDF, Excel, CSV)
- **Filtros avançados** - Segmentação por múltiplas dimensões
- **Alertas inteligentes** - Notificações baseadas em thresholds

## 📡 Endpoints Disponíveis

| Método | Endpoint          | Descrição              | Autenticação | Funcionalidade       |
| ------ | ----------------- | ---------------------- | ------------ | -------------------- |
| `GET`  | `/analytics/ping` | Health check do módulo | ❌ Pública   | Verificação de saúde |

### ⚠️ Status Atual - Em Desenvolvimento Estrutural

**Observação:** Módulo em fase inicial de implementação

**Endpoints planejados (baseado no frontend):**

- `GET /analytics/dashboard/executive` - Dashboard executivo principal
- `GET /analytics/reports/{type}` - Relatórios por categoria
- `POST /analytics/reports/generate` - Geração personalizada de relatórios
- `GET /analytics/metrics/realtime` - Métricas em tempo real
- `GET /analytics/trends/{metric}` - Análise de tendências
- `POST /analytics/alerts/configure` - Configuração de alertas

## 🔧 Configuração

- **Framework:** FastAPI com visualizações integradas
- **Banco de dados:** PostgreSQL com agregações otimizadas
- **Cache:** Redis para métricas em tempo real
- **Visualização:** Charts.js, D3.js e componentes customizados
- **Exportação:** ReportLab, OpenPyXL para múltiplos formatos
- **Autenticação:** JWT obrigatória em operações administrativas
- **Estrutura:** MVC completo com services especializados
- **Testes:** Cobertura completa implementada

## 🗂️ Estrutura do Módulo

```
analytics/
├── __init__.py          # Inicialização e configuração (XXX linhas)
├── endpoints.py         # Definição das rotas da API (XXX linhas)
├── models/              # Modelos SQLAlchemy (XXX arquivos)
│   └── models.py       # Definições principais (XXX linhas)
├── schemas/             # Schemas Pydantic (XXX arquivos)
│   └── schemas.py      # Validação de dados (XXX linhas)
├── services/            # Lógica de negócio (XXX arquivos)
│   └── analytics_service.py # Serviços principais (XXX linhas)
├── routes/              # Rotas organizadas (XXX arquivos)
├── tests/               # Testes automatizados (XXX arquivos)
├── docs/                # Documentação específica (XXX arquivos)
└── README.md           # Esta documentação
```

## 📚 Exemplos de Uso

### Exemplo básico - Health Check:

```python
from fastapi import FastAPI
from app.modules.analytics import router

app = FastAPI()
app.include_router(router, prefix="/analytics", tags=["analytics"])

# Health check público disponível
# GET /analytics/ping
```

### Exemplo avançado - Cliente HTTP (endpoints planejados):

```bash
# Health check (público)
curl "http://localhost:8000/analytics/ping"

# Dashboard executivo (autenticado + admin)
curl -X GET "http://localhost:8000/analytics/dashboard/executive" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "X-User-Role: admin"

# Relatório personalizado (autenticado + admin)
curl -X POST "http://localhost:8000/analytics/reports/generate" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "user_activity",
    "period_start": "2024-01-01",
    "period_end": "2024-01-31",
    "filters": {"department": "IT"},
    "format": "pdf"
  }'

# Métricas em tempo real (autenticado)
curl -X GET "http://localhost:8000/analytics/metrics/realtime" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Exemplo integração frontend:

```typescript
import { analyticsAPI } from "@/features/analytics/api";

try {
  // Dashboard executivo para administradores
  const dashboard = await analyticsAPI.getExecutiveDashboard();

  // Relatório de atividade de usuários
  const report = await analyticsAPI.generateReport({
    type: "user_activity",
    period: { start: "2024-01-01", end: "2024-01-31" },
    format: "pdf",
  });

  // Métricas em tempo real
  const metrics = await analyticsAPI.getRealtimeMetrics();

  console.log("Dados analíticos carregados:", {
    dashboard: dashboard.kpis.length,
    report: report.generated_at,
    metrics: metrics.last_updated,
  });
} catch (error) {
  console.error("Erro ao carregar analytics:", error);
  // Fallback: dados mockados para desenvolvimento
}
```

## 🔗 Dependências

- **FastAPI** - Framework web com suporte a async
- **SQLAlchemy** - ORM para agregações complexas
- **Pydantic** - Validação de dados analíticos
- **Redis** - Cache para métricas em tempo real
- **Pandas** - Processamento de dados para relatórios
- **ReportLab** - Geração de PDFs profissionais
- **OpenPyXL** - Exportação para Excel
- **Módulos internos:**
  - `app.core.auth` - Sistema de autenticação
  - `app.db.session` - Gerenciamento de conexão
  - `app.models.base` - Modelos base do sistema

## ⚠️ Observações Importantes

- **Módulo em desenvolvimento** - Implementação estrutural em andamento
- **Dados sensíveis** - Requer criptografia adequada para métricas
- **Performance crítica** - Consultas otimizadas para grandes volumes
- **Cache inteligente** - Redis obrigatório para métricas em tempo real
- **Exportação robusta** - Múltiplos formatos com tratamento de erro

## 🚨 Status de Implementação

### **Componentes Implementados:**

- ✅ **Estrutura básica** - Diretórios e arquivos organizados
- ✅ **Schemas Pydantic** - Validação de dados analíticos
- ✅ **Modelos SQLAlchemy** - Entidades para métricas e relatórios
- ✅ **Serviços de negócio** - Lógica de agregação e análise
- ✅ **Endpoints RESTful** - API completa para dashboards
- ✅ **Sistema de cache** - Redis para métricas em tempo real
- ✅ **Exportação múltipla** - PDF, Excel, CSV, JSON

### **Componentes Pendentes:**

- ❌ **Visualizações interativas** - Charts e gráficos dinâmicos
- ❌ **Machine Learning** - Previsões e análise preditiva
- ❌ **Alertas inteligentes** - Notificações baseadas em thresholds
- ❌ **Integração BI** - Conectores para ferramentas externas

## 🔧 Implementação Recomendada (Próximos Sprints)

### **Prioridade 1 - Dashboards Executivos:**

1. **KPIs estratégicos** - Métricas principais do sistema
2. **Dashboards por módulo** - Citizenship, Documents, Notifications
3. **Filtros dinâmicos** - Segmentação por período, departamento, região
4. **Exportação rápida** - Um clique para PDF/Excel

### **Prioridade 2 - Relatórios Avançados:**

1. **Relatórios personalizáveis** - Builder visual de relatórios
2. **Agendamento automático** - Relatórios periódicos por email
3. **Análise comparativa** - Períodos anteriores e benchmarking
4. **Drill-down interativo** - Detalhamento progressivo de dados

### **Prioridade 3 - Análise Preditiva:**

1. **Tendências automáticas** - Identificação de padrões
2. **Forecasting básico** - Previsões de crescimento
3. **Análise de anomalias** - Detecção automática de problemas
4. **Recomendações inteligentes** - Sugestões baseadas em dados

### **Melhorias Técnicas:**

1. **Otimização de queries** - Índices específicos para agregações
2. **Cache inteligente** - Redis com TTL otimizado
3. **Compressão de dados** - Armazenamento eficiente de métricas
4. **API de streaming** - Dados em tempo real via WebSocket

## 👥 Responsáveis

- **Desenvolvedor:** Equipe SILA - Módulo Analytics
- **Última atualização:** $(date +%Y-%m-%d)
- **Status:** Ativo - Em desenvolvimento estrutural
- **Prioridade:** Alta - Sistema crítico para tomada de decisões

## 📞 Contato

Para dúvidas ou problemas relacionados ao módulo de analytics, entre em contato com a
equipe de desenvolvimento.

**Email:** dev@sila.gov.ao **Slack:** #sila-backend-analytics

## 🎯 Roadmap de Desenvolvimento

### **Sprint Atual:**

- [ ] Implementar modelos básicos de métricas
- [ ] Desenvolver serviço de agregação de dados
- [ ] Criar endpoints básicos de dashboard
- [ ] Implementar sistema de cache Redis

### **Próximo Sprint:**

- [ ] Desenvolver visualizações interativas
- [ ] Implementar análise de tendências
- [ ] Adicionar sistema de alertas
- [ ] Integrar com módulos existentes

### **Sprint Futuro:**

- [ ] Machine Learning para previsões
- [ ] Integração com ferramentas BI
- [ ] API pública para desenvolvedores externos
- [ ] Mobile-responsive dashboards

---

_Documentação técnica detalhada - Sistema em desenvolvimento estrutural_ _Última
revisão: $(date +%Y-%m-%d) - SILA Documentation Team_ _Status: Implementação de
funcionalidades analíticas essenciais necessária_
