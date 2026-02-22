# Módulo Reports (Relatórios e Análises)

# Sistema SILA - Backend

## Descrição

Módulo responsável pela geração completa de relatórios, análises de dados, métricas de
performance e dashboards executivos no sistema SILA. Implementa funcionalidades
avançadas para geração de relatórios customizáveis, exportação de dados e visualização
de métricas estratégicas para tomada de decisões.

## Funcionalidades Principais

- **Relatórios customizáveis** - Geração de relatórios por período, módulo e formato
- **Métricas de performance** - Indicadores de desempenho em tempo real
- **Dashboards executivos** - Visualizações consolidadas para gestores
- **Exportação de dados** - Múltiplos formatos (PDF, Excel, JSON, CSV)
- **Análises avançadas** - Correlações e tendências automáticas
- **Agendamento de relatórios** - Geração automática periódica

## Endpoints Disponíveis

| Método | Endpoint        | Descrição              | Autenticação | Funcionalidade       |
| ------ | --------------- | ---------------------- | ------------ | -------------------- |
| `GET`  | `/reports/ping` | Health check do módulo | ❌ Pública   | Verificação de saúde |

### Status Atual - Em Desenvolvimento Básico

**Observação:** Módulo em fase inicial de implementação

**Endpoints planejados (baseado no frontend):**

- `POST /reports/generate` - Solicitar geração de relatório
- `GET /reports/{id}/status` - Status de geração de relatório
- `GET /reports/metrics` - Métricas de performance
- `GET /reports/dashboards/{id}` - Dados de dashboard
- `POST /reports/export/{format}` - Exportar dados
- `GET /reports/available` - Relatórios disponíveis

## Configuração

- **Framework:** FastAPI com processamento assíncrono
- **Banco de dados:** PostgreSQL com agregações complexas
- **Processamento:** Background tasks para geração pesada
- **Autenticação:** JWT obrigatória em operações sensíveis
- **Estrutura:** MVC com templates de relatório
- **Schemas:** 2 schemas Pydantic para validação
- **Testes:** Cobertura básica implementada

## Estrutura do Módulo

reports/ ├── **init**.py # Inicialização e configuração (87 linhas) ├── endpoints.py #
Definição das rotas da API (7 linhas - básico) ├── models/ # Modelos SQLAlchemy (2
arquivos) ├── schemas/ # Schemas Pydantic (2 arquivos) ├── services/ # Lógica de negócio
(2 arquivos) ├── routes/ # Rotas organizadas (2 arquivos) ├── utils/ # Utilitários
diversos (2 arquivos) ├── tests/ # Testes automatizados (1 arquivo) └── README.md # Esta
documentação

## Exemplos de Uso

### Exemplo básico - Health Check:

```python
from fastapi import FastAPI
from app.modules.reports import router

app = FastAPI()
app.include_router(router, prefix="/reports", tags=["reports"])

# Health check público disponível
# GET /reports/ping
```

### Exemplo avançado - Cliente HTTP (endpoints planejados):

```bash
# Health check (público)
curl "http://localhost:8000/reports/ping"

# Solicitar relatório mensal (autenticado)
curl -X POST "http://localhost:8000/reports/generate" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reportType": "monthly",
    "period": "2024-01",
    "modules": ["citizenship", "health"],
    "format": "pdf"
  }'

# Buscar métricas de performance (autenticado)
curl -X GET "http://localhost:8000/reports/metrics?module=citizenship&period=2024-Q1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Exportar dados para Excel (autenticado)
curl -X POST "http://localhost:8000/reports/export/excel" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "module": "citizenship",
    "period": "2024-01"
  }'
```
