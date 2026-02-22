# Módulo Dashboard (Painel Administrativo)

# Sistema SILA - Backend

## 📋 Descrição

Módulo responsável pelo painel administrativo e monitoramento em tempo real do sistema
SILA. Fornece estatísticas, métricas de saúde do sistema e atividades recentes para
tomada de decisões estratégicas.

## 🚀 Funcionalidades Principais

- **Estatísticas em tempo real** - Métricas atualizadas de usuários e serviços
- **Monitoramento de saúde** - Status de todos os serviços do sistema
- **Rastreamento de atividades** - Histórico de ações recentes
- **Indicadores de performance** - Tempos de resposta e throughput
- **Alertas proativos** - Notificações de problemas potenciais

## 📡 Endpoints Disponíveis

| Método | Endpoint                | Descrição               | Autenticação   | Retorno             |
| ------ | ----------------------- | ----------------------- | -------------- | ------------------- |
| `GET`  | `/dashboard/resumo`     | Resumo geral do sistema | ✅ Obrigatória | Dados básicos       |
| `GET`  | `/dashboard/municipios` | Lista de municípios     | ✅ Obrigatória | Array de municípios |

### ⚠️ Endpoints Planejados (Frontend vs Backend)

**Observação:** Há incompatibilidade entre frontend e backend:

**Frontend espera:**

- `GET /dashboard/stats` - Estatísticas detalhadas
- `GET /dashboard/service-stats` - Estatísticas por serviço
- `GET /dashboard/health` - Saúde do sistema
- `GET /dashboard/activities` - Atividades recentes

**Backend atual oferece:**

- `GET /dashboard/resumo` - Resumo básico
- `GET /dashboard/municipios` - Apenas municípios

## 🔧 Configuração

- **Framework:** FastAPI com cache automático
- **Banco de dados:** PostgreSQL (múltiplas tabelas)
- **Autenticação:** JWT obrigatória em todos endpoints
- **Cache:** Redis para estatísticas (recomendado)
- **Monitoramento:** Integração com health checks

## 🗂️ Estrutura do Módulo

```
dashboard/
├── __init__.py          # Inicialização do módulo
├── endpoints.py         # Definição das rotas da API (2 endpoints atuais)
├── models/              # Modelos de dados (em desenvolvimento)
├── schemas/             # Schemas Pydantic (StatsResponse, HealthResponse)
├── services/            # Lógica de negócio (planejado)
└── README.md           # Esta documentação
```

## 📚 Exemplos de Uso

### Exemplo básico - Health Check:

```python
from fastapi import FastAPI
from app.modules.dashboard import router

app = FastAPI()
app.include_router(router, prefix="/dashboard", tags=["dashboard"])

# Endpoints disponíveis:
# GET /dashboard/resumo
# GET /dashboard/municipios
```

### Exemplo avançado - Cliente HTTP:

```bash
# Resumo do sistema (autenticado)
curl -X GET "http://localhost:8000/dashboard/resumo" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Municípios disponíveis
curl -X GET "http://localhost:8000/dashboard/municipios" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Exemplo integração frontend:

```typescript
import { dashboardAPI } from "@/features/dashboard/api";

try {
  // Em desenvolvimento - endpoints ainda não implementados no backend
  const stats = await dashboardAPI.getStats();
  const health = await dashboardAPI.getSystemHealth();
  const activities = await dashboardAPI.getRecentActivities();

  console.log("Dashboard data loaded:", { stats, health, activities });
} catch (error) {
  console.error("Erro ao carregar dashboard:", error);
  // Fallback: usar dados mockados
}
```

## 🔗 Dependências

- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para consultas complexas
- **Pydantic** - Validação e serialização de dados
- **Redis** - Cache de estatísticas (opcional)
- **Módulos internos:**
  - `app.core.auth` - Verificação de autenticação
  - `app.db.session` - Conexão com banco de dados
  - `app.models.*` - Modelos de usuários, serviços, etc.

## ⚠️ Observações Importantes

- **Autenticação obrigatória** - Todos os endpoints requerem JWT válido
- **Dados em tempo real** - Estatísticas atualizadas automaticamente
- **Performance crítica** - Módulo acessado frequentemente por admins
- **Cache recomendado** - Para reduzir carga no banco de dados
- **Monitoramento ativo** - Health checks devem ser rápidos (< 100ms)

## 🚨 Inconsistências Identificadas

- **Frontend/backend desalinhados** - 4 endpoints esperados vs 2 implementados
- **Dados mockados necessários** - Frontend funciona com dados simulados
- **Falta de modelos de dados** - Estrutura de banco não definida
- **Schemas ausentes** - Tipagem de respostas não padronizada

## 🔧 Implementação Recomendada (Próximas Sprints)

### **Endpoints a Implementar:**

1. `GET /dashboard/stats` - Estatísticas gerais do sistema
2. `GET /dashboard/service-stats` - Performance por serviço
3. `GET /dashboard/health` - Status de saúde detalhado
4. `GET /dashboard/activities` - Atividades recentes com paginação

### **Melhorias de Performance:**

1. **Cache Redis** para estatísticas
2. **Consultas otimizadas** com índices adequados
3. **Paginação** para grandes volumes de dados
4. **Compressão** de respostas JSON

## 👥 Responsáveis

- **Desenvolvedor:** Equipe SILA - Módulo Dashboard
- **Última atualização:** $(date +%Y-%m-%d)
- **Status:** Ativo - Requer implementação completa
- **Prioridade:** Crítica - Interface principal do sistema

## 📞 Contato

Para dúvidas ou problemas relacionados ao módulo de dashboard, entre em contato com a
equipe de desenvolvimento.

**Email:** dev@sila.gov.ao **Slack:** #sila-backend-dashboard

## 🎯 Roadmap de Desenvolvimento

### **Sprint Atual:**

- [ ] Implementar endpoints básicos faltantes
- [ ] Criar modelos de dados para estatísticas
- [ ] Adicionar cache Redis básico

### **Próximo Sprint:**

- [ ] Implementar métricas avançadas
- [ ] Adicionar gráficos e visualizações
- [ ] Integrar com sistema de alertas

---

_Documentação técnica detalhada - Sistema em desenvolvimento ativo_ _Última revisão:
$(date +%Y-%m-%d) - SILA Documentation Team_ _Status: Requer implementação urgente dos
endpoints esperados pelo frontend_
