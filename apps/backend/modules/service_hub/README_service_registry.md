# Service Hub - Service Registry

O módulo **service_hub** é o ponto central de orquestração entre os demais módulos do
sistema SILA. Funciona como um hub de serviços digitais que consolida acesso,
integrações e fluxos entre módulos distintos.

## 🎯 Objetivo

- **Centralizar acesso** aos serviços disponíveis no sistema
- **Fornecer catálogo** pesquisável e categorizado de serviços
- **Encaminhar chamadas** para os módulos corretos (appointments, documents,
  citizenship, education etc.)
- **Monitorar uso** e métricas de atendimento digital
- **Garantir segurança** (controle de acesso e trilhas de auditoria)

## 🏗️ Arquitetura

### Modelo ServiceRegistry

```python
class ServiceRegistry(Base):
    id: int (Primary Key)
    module_name: str          # Ex.: "citizenship"
    service_name: str         # Ex.: "request_id_card"
    description: str          # Descrição do serviço
    category: str             # Ex.: "identity", "education"
    is_active: bool           # Status do serviço
    created_at: datetime      # Data de criação
    updated_at: datetime      # Última atualização
```

### Schemas Principais

- **ServiceCreate**: Para registro de novos serviços
- **ServiceUpdate**: Para atualizações parciais
- **ServiceOut**: Para respostas da API
- **ServiceForwardRequest**: Para encaminhamento de requisições
- **ServiceForwardResponse**: Para respostas de encaminhamento

## 📡 Endpoints da API

### Gestão de Serviços

```http
POST   /service_hub/register              # Registrar serviço
GET    /service_hub/                      # Listar serviços (com filtros)
GET    /service_hub/{service_id}          # Obter serviço específico
PUT    /service_hub/{service_id}          # Atualizar serviço
DELETE /service_hub/{service_id}          # Remover serviço
POST   /service_hub/{service_id}/deactivate  # Desativar serviço
```

### Encaminhamento

```http
POST   /service_hub/{module}/{service}    # Encaminhar requisição
```

### Descoberta e Estatísticas

```http
GET    /service_hub/stats/overview        # Estatísticas gerais
GET    /service_hub/categories/list       # Listar categorias
GET    /service_hub/modules/list          # Listar módulos
GET    /service_hub/category/{category}   # Serviços por categoria
GET    /service_hub/module/{module}       # Serviços por módulo
```

## 🚀 Exemplos de Uso

### 1. Registrar um Serviço

```bash
curl -X POST "/service_hub/register" \
  -H "Content-Type: application/json" \
  -d '{
    "module_name": "citizenship",
    "service_name": "apply_passport",
    "description": "Solicitação de passaporte",
    "category": "identity"
  }'
```

**Resposta:**

```json
{
  "id": 1,
  "module_name": "citizenship",
  "service_name": "apply_passport",
  "description": "Solicitação de passaporte",
  "category": "identity",
  "is_active": true,
  "created_at": "2024-09-14T08:30:00Z"
}
```

### 2. Listar Serviços por Categoria

```bash
curl "/service_hub/?category=identity"
```

**Resposta:**

```json
[
  {
    "id": 1,
    "module_name": "citizenship",
    "service_name": "apply_passport",
    "category": "identity",
    "is_active": true
  },
  {
    "id": 2,
    "module_name": "citizenship",
    "service_name": "request_id_card",
    "category": "identity",
    "is_active": true
  }
]
```

### 3. Encaminhar Requisição

```bash
curl -X POST "/service_hub/citizenship/apply_passport" \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "citizen_id": "123456789",
      "passport_type": "ordinary"
    },
    "timeout": 30
  }'
```

**Resposta:**

```json
{
  "success": true,
  "status_code": 200,
  "data": {
    "application_id": "PASS-2024-001",
    "status": "submitted"
  },
  "execution_time": 1.25
}
```

### 4. Obter Estatísticas

```bash
curl "/service_hub/stats/overview"
```

**Resposta:**

```json
{
  "total_services": 15,
  "active_services": 14,
  "inactive_services": 1,
  "by_category": {
    "identity": 4,
    "education": 3,
    "health": 5,
    "social_security": 2
  },
  "by_module": {
    "citizenship": 4,
    "education": 3,
    "health": 5,
    "social": 2,
    "finance": 1
  }
}
```

## 🔗 Integração com Módulos

### Citizenship

- `apply_passport`: Solicitação de passaporte
- `request_id_card`: Solicitação de BI
- `verify_document`: Verificação de documentos

### Education

- `enroll_student`: Matrícula de estudante
- `request_certificate`: Solicitação de certificados
- `transfer_school`: Transferência escolar

### Health

- `book_appointment`: Marcação de consultas
- `get_medical_record`: Acesso a registros médicos
- `vaccination_schedule`: Agendamento de vacinas

### Social Security

- `apply_benefit`: Solicitação de benefícios
- `pension_request`: Solicitação de pensão

### Finance

- `pay_taxes`: Pagamento de impostos
- `tax_declaration`: Declaração de impostos

## 🛡️ Segurança

### Autenticação

- Todos os endpoints de modificação requerem autenticação
- Tokens JWT validados via `get_current_active_user`

### Autorização

- Registro de serviços limitado a usuários autenticados
- Encaminhamento com controle de acesso
- Auditoria de todas as operações

### Validação

- Schemas Pydantic para validação de entrada
- Sanitização de dados antes do encaminhamento
- Timeout configurável para evitar bloqueios

## 📊 Monitoramento

### Métricas Disponíveis

- Total de serviços registrados
- Serviços ativos/inativos
- Distribuição por categoria e módulo
- Tempo de execução de encaminhamentos
- Taxa de sucesso/erro

### Logs de Auditoria

- Registro de todas as operações
- Rastreamento de encaminhamentos
- Monitoramento de performance

## 🧪 Testes

### Cobertura de Testes

- ✅ Registro e atualização de serviços
- ✅ Listagem com filtros
- ✅ Encaminhamento bem-sucedido
- ✅ Tratamento de erros
- ✅ Estatísticas e descoberta
- ✅ Segurança e autorização

### Executar Testes

```bash
pytest backend/app/modules/service_hub/tests/test_service_registry.py -v
```

## 🔧 Configuração

### Variáveis de Ambiente

```env
# URLs base dos módulos (para encaminhamento)
CITIZENSHIP_SERVICE_URL=http://localhost:8000/api/v1/citizenship
EDUCATION_SERVICE_URL=http://localhost:8000/api/v1/education
HEALTH_SERVICE_URL=http://localhost:8000/api/v1/health

# Timeouts padrão
DEFAULT_SERVICE_TIMEOUT=10
MAX_SERVICE_TIMEOUT=60
```

### Inicialização

```python
from app.modules.service_hub.services.service_registry_service import ServiceHubService

# Registrar serviços automaticamente na inicialização
def register_default_services(db: Session):
    services = [
        ServiceCreate(
            module_name="citizenship",
            service_name="apply_passport",
            description="Solicitação de passaporte",
            category="identity"
        ),
        # ... outros serviços
    ]

    for service in services:
        ServiceHubService.register_service(db, service)
```

## 🚦 Status e Roadmap

### ✅ Implementado

- Registro e gestão de serviços
- Encaminhamento básico via HTTP
- Descoberta por categoria/módulo
- Estatísticas e monitoramento
- Testes abrangentes

### 🔄 Em Desenvolvimento

- Service discovery automático
- Load balancing entre instâncias
- Circuit breaker para resiliência
- Cache de respostas

### 📋 Planejado

- Integração com API Gateway
- Métricas avançadas (Prometheus)
- Dashboard de monitoramento
- Versionamento de APIs

## 💡 Casos de Uso

### 1. Portal do Cidadão

```python
# Listar todos os serviços disponíveis para o cidadão
services = ServiceHubService.list_services(db, is_active=True)
categories = {}
for service in services:
    if service.category not in categories:
        categories[service.category] = []
    categories[service.category].append(service)
```

### 2. Integração entre Módulos

```python
# Módulo Education consultando Citizenship
response = ServiceHubService.forward_request(
    db,
    "citizenship",
    "verify_document",
    ServiceForwardRequest(payload={"document_id": "123456"})
)
```

### 3. Dashboard Administrativo

```python
# Obter visão geral do sistema
stats = ServiceHubService.get_service_statistics(db)
print(f"Total de serviços: {stats['total_services']}")
print(f"Módulos ativos: {len(stats['by_module'])}")
```

O Service Hub é o coração da arquitetura de microserviços do SILA, proporcionando
descoberta, orquestração e monitoramento centralizados de todos os serviços públicos
digitais.
