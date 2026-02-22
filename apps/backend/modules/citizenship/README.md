# Módulo Citizenship (Serviços ao Cidadão)

# Sistema SILA - Backend

## 📋 Descrição

Módulo estratégico responsável pela gestão completa de serviços e solicitações de
cidadania no sistema SILA. Implementa funcionalidades essenciais para atendimento ao
cidadão, incluindo catálogo de serviços, registro de solicitações, acompanhamento de
processos, e integração com serviços públicos municipais. Arquitetura moderna com
microserviços, eventos assíncronos, e analytics avançados.

## 🚀 Funcionalidades Principais

- **📋 Catálogo de Serviços** - Lista organizada de serviços disponíveis por categoria e
  região
- **📝 Sistema de Solicitações** - Abertura e acompanhamento completo de pedidos
- **🔄 Gestão de Status** - Controle completo do ciclo de vida das solicitações
- **📢 Notificações Automáticas** - Comunicação proativa com o cidadão via múltiplos
  canais
- **📊 Analytics e Relatórios** - Métricas detalhadas de atendimento e KPIs
- **🔐 Integração com Auth** - Controle de acesso e permissões granular
- **📱 Interface Mobile-Ready** - API otimizada para aplicativos móveis
- **🌐 Integração Externa** - Conexão com sistemas governamentais

## 📡 Endpoints Disponíveis

| Método  | Endpoint                               | Descrição                      | Autenticação   | Rate Limit  |
| ------- | -------------------------------------- | ------------------------------ | -------------- | ----------- |
| `GET`   | `/citizenship/ping`                    | Health check do módulo         | ❌ Pública     | Sem limite  |
| `GET`   | `/citizenship/services`                | Lista de serviços disponíveis  | ✅ Obrigatória | 100 req/min |
| `GET`   | `/citizenship/services/{id}`           | Detalhes de serviço específico | ✅ Obrigatória | 200 req/min |
| `POST`  | `/citizenship/requests`                | Criar nova solicitação         | ✅ Obrigatória | 20 req/min  |
| `GET`   | `/citizenship/requests/user`           | Solicitações do usuário logado | ✅ Obrigatória | 100 req/min |
| `GET`   | `/citizenship/requests/{id}`           | Detalhes de solicitação        | ✅ Obrigatória | 200 req/min |
| `PATCH` | `/citizenship/requests/{id}/cancel`    | Cancelar solicitação           | ✅ Obrigatória | 10 req/min  |
| `POST`  | `/citizenship/requests/{id}/documents` | Upload de documentos           | ✅ Obrigatória | 10 req/min  |
| `GET`   | `/citizenship/requests/{id}/timeline`  | Timeline de solicitação        | ✅ Obrigatória | 100 req/min |
| `GET`   | `/citizenship/categories`              | Categorias de serviços         | ❌ Pública     | 50 req/min  |
| `GET`   | `/citizenship/analytics/dashboard`     | Dashboard analytics            | ✅ Admin       | 30 req/min  |

### Detalhamento dos Endpoints

#### **GET /citizenship/services** - Catálogo de Serviços

**Funcionalidade:** Lista completa de serviços disponíveis com filtros avançados

**Query Parameters:**

```bash
# Filtros disponíveis
?category=licenciamento&region=luanda&status=active&page=1&limit=20&search=alvará
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "services": [
      {
        "id": "lic_comercial_001",
        "name": "Alvará de Licença Comercial",
        "description": "Licença para estabelecimentos comerciais",
        "category": "licenciamento",
        "subcategory": "comercial",
        "region": "luanda",
        "estimated_days": 15,
        "requirements": [
          "Documento de identificação",
          "Comprovativo de residência",
          "Planta do estabelecimento"
        ],
        "fees": {
          "amount": 15000,
          "currency": "AOA",
          "payment_methods": ["multicaixa", "transferencia"]
        },
        "status": "active",
        "created_at": "2025-10-26T13:47:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 156,
      "pages": 8
    }
  }
}
```

#### **POST /citizenship/requests** - Criar Solicitação

**Funcionalidade:** Abertura de nova solicitação de serviço

**Request:**

```json
{
  "service_id": "lic_comercial_001",
  "applicant_data": {
    "full_name": "João Silva",
    "email": "joao.silva@email.com",
    "phone": "+244923456789",
    "address": "Rua Principal, 123, Luanda",
    "document_type": "BI",
    "document_number": "001234567LA001"
  },
  "business_data": {
    "business_name": "Comércio Silva Lda",
    "business_type": "retail",
    "employees_count": 5,
    "annual_revenue": 5000000
  },
  "priority": "normal",
  "notes": "Solicitação urgente para abertura de loja"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Solicitação criada com sucesso",
  "data": {
    "request_id": "REQ-2025-001234",
    "protocol": "2025/CIT/001234",
    "service": {
      "id": "lic_comercial_001",
      "name": "Alvará de Licença Comercial"
    },
    "status": "submitted",
    "estimated_completion": "2025-11-10T13:47:00Z",
    "next_steps": [
      "Aguardar validação de documentos",
      "Pagamento da taxa de licenciamento",
      "Inspeção do estabelecimento"
    ],
    "created_at": "2025-10-26T13:47:00Z"
  }
}
```

#### **GET /citizenship/requests/{id}/timeline** - Timeline da Solicitação

**Funcionalidade:** Histórico completo de atualizações da solicitação

**Response:**

```json
{
  "status": "success",
  "data": {
    "request_id": "REQ-2025-001234",
    "timeline": [
      {
        "id": "timeline_001",
        "status": "submitted",
        "description": "Solicitação submetida com sucesso",
        "actor": "system",
        "timestamp": "2025-10-26T13:47:00Z",
        "attachments": []
      },
      {
        "id": "timeline_002",
        "status": "under_review",
        "description": "Documentos em análise pela equipe de licenciamento",
        "actor": "officer_joao",
        "timestamp": "2025-10-27T09:15:00Z",
        "attachments": ["review_report.pdf"]
      },
      {
        "id": "timeline_003",
        "status": "payment_pending",
        "description": "Aguardando pagamento da taxa de licenciamento",
        "actor": "system",
        "timestamp": "2025-10-27T14:30:00Z",
        "attachments": ["payment_invoice.pdf"]
      }
    ],
    "current_status": "payment_pending",
    "progress_percentage": 35
  }
}
```

## 🔧 Configuração

### **Tecnologias e Framework**

- **Framework:** FastAPI com estrutura modular avançada
- **Banco de dados:** PostgreSQL com modelos SQLAlchemy otimizados
- **Autenticação:** JWT obrigatória com integração ao módulo auth
- **Cache:** Redis para performance e sessões
- **Eventos:** Sistema de eventos assíncronos com background tasks
- **Analytics:** PostgreSQL + TimescaleDB para métricas temporais
- **Documentos:** Armazenamento em S3-compatible storage
- **Notificações:** Sistema multi-canal (email, SMS, push)

### **Variáveis de Ambiente**

```bash
# Configurações do Módulo
CITIZENSHIP_MODULE_ENABLED=true
CITIZENSHIP_DB_URL=postgresql://user:pass@localhost:5432/sila_citizenship
CITIZENSHIP_REDIS_URL=redis://localhost:6379/1

# Configurações de Processamento
MAX_REQUESTS_PER_USER_PER_DAY=10
DEFAULT_REQUEST_EXPIRY_DAYS=365
AUTO_APPROVE_THRESHOLD=1000

# Configurações de Documentos
DOCUMENT_STORAGE_TYPE=s3
DOCUMENT_BUCKET_NAME=sila-documents
DOCUMENT_MAX_SIZE_MB=10
DOCUMENT_ALLOWED_TYPES=pdf,jpg,png,doc,docx

# Configurações de Notificações
NOTIFICATION_ENABLED=true
EMAIL_FROM_ADDRESS=noreply@sila.gov.ao
SMS_GATEWAY_URL=https://sms-gateway.gov.ao
PUSH_NOTIFICATION_KEY=${PUSH_KEY}

# Configurações de Analytics
ANALYTICS_ENABLED=true
ANALYTICS_RETENTION_DAYS=730
REAL_TIME_DASHBOARD=true
```

### **Dependências Principais**

```python
# Core dependencies
fastapi>=0.104.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
alembic>=1.12.0
redis>=5.0.0

# Background processing
celery>=5.3.0
kombu>=5.3.0

# Document handling
boto3>=1.29.0
python-multipart>=0.0.6
pillow>=10.0.0

# Analytics
timescaledb-psycopg2>=0.1.0
pandas>=2.1.0

# Notifications
jinja2>=3.1.0
smtplib-ssl>=1.0.0
twilio>=8.10.0
```

## 🗂️ Estrutura do Módulo

```
citizenship/
├── __init__.py              # 🚀 Inicialização e configuração (1897 linhas)
├── endpoints.py             # 🌐 Definição das rotas da API (11 endpoints)
├── models/                  # 🗃️ Modelos SQLAlchemy
│   ├── __init__.py
│   ├── service.py          # Modelo Service (catálogo de serviços)
│   ├── request.py          # Modelo Request (solicitações)
│   ├── applicant.py        # Modelo Applicant (dados do solicitante)
│   ├── document.py         # Modelo Document (documentos anexos)
│   ├── timeline.py         # Modelo Timeline (histórico)
│   ├── category.py         # Modelo Category (categorias)
│   └── analytics.py        # Modelo Analytics (métricas)
├── schemas/                 # 📋 Schemas Pydantic
│   ├── __init__.py
│   ├── request.py          # 📥 Schemas de solicitação (RequestCreate, RequestUpdate)
│   ├── response.py         # 📤 Schemas de resposta (ServiceResponse, RequestResponse)
│   ├── service.py          # 📋 Schemas de serviço (ServiceCreate, ServiceResponse)
│   ├── applicant.py        # 📋 Schemas de solicitante (ApplicantCreate, ApplicantResponse)
│   ├── document.py         # 📋 Schemas de documento (DocumentUpload, DocumentResponse)
│   ├── timeline.py         # 📋 Schemas de timeline (TimelineEntry, TimelineResponse)
│   ├── analytics.py        # 📋 Schemas de analytics (DashboardMetrics, ServiceStats)
│   └── common.py           # 🔧 Schemas compartilhados (BaseResponse, Pagination)
├── services/               # ⚙️ Lógica de negócio
│   ├── __init__.py
│   ├── citizenship_service.py     # Serviço principal de cidadania
│   ├── service_catalog_service.py  # Serviço de catálogo de serviços
│   ├── request_service.py          # Serviço de gestão de solicitações
│   ├── document_service.py         # Serviço de gestão de documentos
│   ├── notification_service.py     # Serviço de notificações
│   ├── analytics_service.py        # Serviço de analytics e relatórios
│   └── validation_service.py       # Serviço de validação de regras
├── crud/                   # 🗄️ Operações de banco
│   ├── __init__.py
│   ├── service_crud.py     # CRUD de serviços
│   ├── request_crud.py     # CRUD de solicitações
│   ├── applicant_crud.py   # CRUD de solicitantes
│   ├── document_crud.py    # CRUD de documentos
│   ├── timeline_crud.py    # CRUD de timeline
│   └── analytics_crud.py   # CRUD de analytics
├── utils/                  # 🛠️ Utilitários do módulo
│   ├── __init__.py
│   ├── citizenship_utils.py       # Utilitários gerais
│   ├── document_utils.py          # Utilitários de documentos
│   ├── validation_utils.py        # Utilitários de validação
│   ├── notification_utils.py      # Utilitários de notificações
│   └── analytics_utils.py         # Utilitários de analytics
├── exceptions.py           # ⚠️ Exceções personalizadas (3096 linhas)
├── handlers.py             # 🎯 Handlers para eventos (4089 linhas)
├── tasks/                  # 📋 Tarefas assíncronas
│   ├── __init__.py
│   ├── notification_tasks.py      # Tarefas de notificação
│   ├── processing_tasks.py        # Tarefas de processamento
│   └── analytics_tasks.py         # Tarefas de analytics
├── routes/                 # 🛣️ Rotas organizadas (13 arquivos)
│   ├── __init__.py
│   ├── services.py         # Rotas de serviços
│   ├── requests.py         # Rotas de solicitações
│   ├── documents.py        # Rotas de documentos
│   ├── analytics.py        # Rotas de analytics
│   └── admin.py            # Rotas administrativas
├── tests/                  # 🧪 Testes automatizados
│   ├── __init__.py
│   ├── test_endpoints.py   # Testes dos endpoints
│   ├── test_services.py    # Testes dos serviços
│   ├── test_crud.py        # Testes das operações CRUD
│   ├── test_integration.py # Testes de integração
│   └── test_analytics.py   # Testes de analytics
└── README.md               # 📖 Esta documentação
```

## 📚 Exemplos de Uso

### **Exemplo básico - Integração com FastAPI:**

```python
from fastapi import FastAPI, Depends, HTTPException
from app.modules.citizenship import router
from app.modules.auth import get_current_user

app = FastAPI(title="SILA Citizenship System")

# Incluir rotas de cidadania
app.include_router(
    router,
    prefix="/citizenship",
    tags=["citizenship"],
    dependencies=[Depends(get_current_user)]
)

# Endpoint customizado usando serviços do módulo
@app.get("/my-services")
async def get_user_services(current_user = Depends(get_current_user)):
    """Serviços personalizados para o usuário"""
    from app.modules.citizenship.services import CitizenshipService

    service = CitizenshipService()
    user_requests = await service.get_user_requests(current_user.id)
    recommended_services = await service.get_recommended_services(current_user.id)

    return {
        "active_requests": user_requests,
        "recommended_services": recommended_services,
        "user_profile": current_user.dict()
    }
```

### **Exemplo avançado - Cliente Completo:**

```python
import httpx
from typing import List, Optional
from datetime import datetime

class SILACitizenshipClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    async def get_services(
        self,
        category: Optional[str] = None,
        region: Optional[str] = None,
        search: Optional[str] = None
    ) -> dict:
        """Buscar catálogo de serviços"""
        params = {}
        if category:
            params["category"] = category
        if region:
            params["region"] = region
        if search:
            params["search"] = search

        response = self.client.get(
            f"{self.base_url}/citizenship/services",
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def create_request(self, service_id: str, request_data: dict) -> dict:
        """Criar nova solicitação"""
        response = self.client.post(
            f"{self.base_url}/citizenship/requests",
            json={
                "service_id": service_id,
                **request_data
            }
        )
        response.raise_for_status()
        return response.json()

    async def get_request_timeline(self, request_id: str) -> dict:
        """Obter timeline da solicitação"""
        response = self.client.get(
            f"{self.base_url}/citizenship/requests/{request_id}/timeline"
        )
        response.raise_for_status()
        return response.json()

    async def upload_document(
        self,
        request_id: str,
        document_type: str,
        file_path: str
    ) -> dict:
        """Upload de documento para solicitação"""
        with open(file_path, "rb") as file:
            files = {"document": (file_path, file, "application/pdf")}
            data = {"document_type": document_type}

            response = self.client.post(
                f"{self.base_url}/citizenship/requests/{request_id}/documents",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()

# Uso do cliente
async def main():
    # Autenticar primeiro (usando cliente auth)
    auth_client = SILAAuthClient("http://localhost:8000")
    auth_data = await auth_client.login("citizen@email.com", "password")

    # Cliente de cidadania
    citizenship_client = SILACitizenshipClient(
        "http://localhost:8000",
        auth_data["access_token"]
    )

    # Buscar serviços disponíveis
    services = await citizenship_client.get_services(category="licenciamento")
    print(f"Found {len(services['data']['services'])} services")

    # Criar solicitação
    request_data = {
        "applicant_data": {
            "full_name": "João Silva",
            "email": "joao.silva@email.com",
            "phone": "+244923456789"
        }
    }

    new_request = await citizenship_client.create_request(
        "lic_comercial_001",
        request_data
    )

    print(f"Request created: {new_request['data']['request_id']}")

    # Upload de documento
    await citizenship_client.upload_document(
        new_request['data']['request_id'],
        "identification",
        "/path/to/document.pdf"
    )
```

### **Exemplo integração frontend:**

```typescript
// citizenship.service.ts
import { apiClient } from "@/lib/api-client";

interface Service {
  id: string;
  name: string;
  description: string;
  category: string;
  estimated_days: number;
  fees: {
    amount: number;
    currency: string;
  };
}

interface CreateRequestData {
  service_id: string;
  applicant_data: {
    full_name: string;
    email: string;
    phone: string;
    address: string;
  };
  business_data?: {
    business_name: string;
    business_type: string;
  };
}

class CitizenshipService {
  async getServices(filters?: {
    category?: string;
    region?: string;
    search?: string;
  }): Promise<{ services: Service[] }> {
    const response = await apiClient.get("/citizenship/services", {
      params: filters,
    });
    return response.data;
  }

  async createRequest(data: CreateRequestData): Promise<any> {
    const response = await apiClient.post("/citizenship/requests", data);
    return response.data;
  }

  async getUserRequests(): Promise<any[]> {
    const response = await apiClient.get("/citizenship/requests/user");
    return response.data.requests;
  }

  async getRequestTimeline(requestId: string): Promise<any> {
    const response = await apiClient.get(`/citizenship/requests/${requestId}/timeline`);
    return response.data;
  }

  async uploadDocument(
    requestId: string,
    documentType: string,
    file: File,
  ): Promise<any> {
    const formData = new FormData();
    formData.append("document", file);
    formData.append("document_type", documentType);

    const response = await apiClient.post(
      `/citizenship/requests/${requestId}/documents`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );
    return response.data;
  }

  async cancelRequest(requestId: string, reason: string): Promise<any> {
    const response = await apiClient.patch(
      `/citizenship/requests/${requestId}/cancel`,
      { reason },
    );
    return response.data;
  }
}

export const citizenshipService = new CitizenshipService();

// React Hook para usar o serviço
export const useCitizenshipServices = (filters?: any) => {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchServices = async () => {
      setLoading(true);
      try {
        const data = await citizenshipService.getServices(filters);
        setServices(data.services);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, [filters]);

  return { services, loading, error };
};
```

## 🔗 Dependências

### **Dependências Internas**

- `app.modules.auth` - Autenticação e autorização de usuários
- `app.core.database` - Conexão com banco de dados PostgreSQL
- `app.core.redis` - Cache e sessões
- `app.core.storage` - Armazenamento de documentos (S3)
- `app.core.notifications` - Sistema de notificações
- `app.core.analytics` - Analytics e métricas
- `app.core.logging` - Logging estruturado

### **Dependências Externas**

- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic V2** - Validação de dados
- **Redis** - Cache e message broker
- **Celery** - Background tasks
- **Boto3** - Cliente AWS S3
- **Pillow** - Processamento de imagens
- **Pandas** - Analytics e processamento de dados

## ⚠️ Observações Importantes

### **Performance e Escalabilidade**

- **Cache Redis** para catálogo de serviços (TTL: 1 hora)
- **Background tasks** para processamento assíncrono
- **Database indexing** otimizado para consultas frequentes
- **Rate limiting** por usuário e por endpoint
- **Pagination** implementado em todos os listados

### **Segurança e Privacidade**

- **Validação rigorosa** de todos os dados de entrada
- **Sanitização de uploads** para prevenção de malware
- **Criptografia** de dados sensíveis no banco
- **Audit logging** completo de todas as operações
- **RBAC integration** para controle de acesso fino

### **Integrações Externas**

- **Sistema de Notificações** - Email, SMS, Push notifications
- **Storage de Documentos** - S3-compatible com backup automático
- **Analytics Platform** - TimescaleDB para métricas temporais
- **Payment Gateway** - Integração com Multicaixa e sistemas bancários

## 📊 Analytics e Monitoramento

### **KPIs do Módulo**

- **Taxa de conclusão de solicitações**: > 85%
- **Tempo médio de processamento**: < 15 dias
- **Satisfação do cidadão**: > 4.2/5.0
- **Taxa de adoção digital**: > 70%
- **Documentos processados**: > 10.000/mês

### **Métricas de Performance**

```bash
# Health check do módulo
curl http://localhost:8000/citizenship/ping

# Métricas de performance
curl http://localhost:8000/citizenship/metrics

# Dashboard analytics
curl http://localhost:8000/citizenship/analytics/dashboard
```

### **Alertas e Monitoramento**

- **Latency alerts** > 2 segundos para endpoints críticos
- **Error rate alerts** > 5% para qualquer endpoint
- **Database connection alerts** > 80% utilização
- **Storage alerts** > 90% capacidade utilizada

## 🔄 Fluxos de Trabalho

### **Fluxo de Solicitação Padrão**

```mermaid
graph TD
    A[Usuário seleciona serviço] --> B[Preenche formulário]
    B --> C[Anexa documentos]
    C --> D[Submete solicitação]
    D --> E[Validação automática]
    E --> F{Validação OK?}
    F -->|Sim| G[Pagamento da taxa]
    F -->|Não| H[Solicita correção]
    G --> I[Análise técnica]
    I --> J[Inspeção se necessário]
    J --> K[Aprovação final]
    K --> L[Emissão de documento]
    L --> M[Notificação ao cidadão]
    H --> B
```

### **Fluxo de Notificações**

```mermaid
graph LR
    A[Evento do Sistema] --> B[Queue de Notificações]
    B --> C[Processamento Assíncrono]
    C --> D{Tipo de Notificação}
    D -->|Email| E[Template Engine]
    D -->|SMS| F[SMS Gateway]
    D -->|Push| G[Push Service]
    E --> H[Envio]
    F --> H
    G --> H
    H --> I[Log de Entrega]
    I --> J[Analytics]
```

## 👥 Responsáveis

- **🏗️ Product Owner**: Equipe de Produtos SILA
- **🔧 Desenvolvedor Principal**: Equipe de Cidadania Digital
- **🎨 UX/UI Designer**: Equipe de Experiência do Usuário
- **📊 Analytics Engineer**: Equipe de Dados e Analytics
- **🛡️ Segurança**: Equipe de Segurança da Informação
- **🧪 QA**: Equipe de Qualidade e Testes

### **Informações de Contato**

- **Email**: citizenship-team@sila.gov.ao
- **Slack**: #sila-citizenship
- **Documentação**: [docs.sila.gov.ao/citizenship](https://docs.sila.gov.ao/citizenship)
- **Issues**:
  [GitHub Citizenship Issues](https://github.com/sila-system/issues?q=is:issue+is:open+label:citizenship)

---

## 📝 Histórico de Mudanças

| Versão | Data       | Mudanças                                            | Autor     |
| ------ | ---------- | --------------------------------------------------- | --------- |
| 2.0.0  | 2025-10-26 | Refatoração completa com nova arquitetura unificada | SILA Team |
| 1.8.0  | 2025-09-20 | Implementação de analytics avançados                | SILA Team |
| 1.6.0  | 2025-08-15 | Sistema de notificações multi-canal                 | SILA Team |
| 1.4.0  | 2025-07-10 | Integração com sistema de pagamentos                | SILA Team |
| 1.0.0  | 2025-06-01 | Versão inicial com funcionalidades básicas          | SILA Team |

---

## 🚀 Roadmap Futuro

### **Próximas Funcionalidades (Q4 2025)**

- **🤖 IA Assistant** - Chatbot para auxílio em solicitações
- **📱 Mobile App** - Aplicativo nativo para iOS/Android
- **🔗 Blockchain Integration** - Verificação de autenticidade de documentos
- **🌐 Multi-language Support** - Suporte para inglês e francês

### **Melhorias Técnicas (2026)**

- **Microservices Architecture** - Decomposição em microsserviços
- **GraphQL API** - Alternativa à REST API
- **Real-time Updates** - WebSocket para atualizações ao vivo
- **Advanced Analytics** - Machine learning para previsões

---

_Documentação técnica detalhada - Módulo Citizenship v2.0.0_ _Última revisão:
2025-10-26 - SILA Documentation Team_ _Status: ✅ Production Ready_
