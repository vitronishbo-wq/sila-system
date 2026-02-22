# Service Hub API - Documentação Técnica

## 🔧 Configuração e Instalação

### Dependências

```python
# requirements.txt
fastapi>=0.104.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### Configuração do Banco de Dados

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco
DATABASE_URL = "postgresql://user:password@localhost/sila_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## 📋 Schemas Detalhados

### ServiceCreate

```python
class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    category: ServiceCategory = Field(...)
    description: Optional[str] = Field(None, max_length=2000)
    scope: ServiceScope = Field(...)
    estimated_time: Optional[int] = Field(None, ge=1, le=480)
    requirements: Optional[Dict[str, Any]] = Field(None)
```

**Validações:**

- `name`: Mínimo 3 caracteres, máximo 255
- `estimated_time`: Entre 1 e 480 minutos (8 horas)
- `requirements`: Objeto JSON válido com estrutura específica

### ServiceUpdate

```python
class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    category: Optional[ServiceCategory] = None
    description: Optional[str] = Field(None, max_length=2000)
    is_active: Optional[bool] = None
    scope: Optional[ServiceScope] = None
    estimated_time: Optional[int] = Field(None, ge=1, le=480)
    requirements: Optional[Dict[str, Any]] = None
```

### ServiceLocationCreate

```python
class ServiceLocationCreate(BaseModel):
    province: str = Field(..., min_length=2, max_length=100)
    municipality: str = Field(..., min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    contact_info: Optional[Dict[str, Any]] = Field(None)
```

**Validações de Contato:**

- `phone`: Mínimo 8 dígitos
- `email`: Formato válido de email
- `working_hours`: Objeto com horários por dia da semana

## 🔌 Endpoints Detalhados

### POST /services/

Cria um novo serviço público.

**Headers:**

```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Emissão de Passaporte",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 30,
  "requirements": {
    "documents": ["BI", "Certidão de nascimento", "Fotografias"],
    "age_requirement": 18,
    "fees": 15000,
    "validity_period": "5 anos"
  }
}
```

**Response (201):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Emissão de Passaporte",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 30,
  "requirements": {
    "documents": ["BI", "Certidão de nascimento", "Fotografias"],
    "age_requirement": 18,
    "fees": 15000,
    "validity_period": "5 anos"
  },
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "locations_count": 0
}
```

**Erros Possíveis:**

- `409 Conflict`: Serviço com mesmo nome/categoria já existe
- `422 Unprocessable Entity`: Dados inválidos
- `401 Unauthorized`: Token inválido ou expirado
- `403 Forbidden`: Usuário não é administrador

### GET /services/

Lista serviços com filtros opcionais.

**Query Parameters:**

- `category` (string): Filtrar por categoria
- `scope` (string): Filtrar por escopo
- `is_active` (boolean): Filtrar por status ativo (default: true)
- `province` (string): Filtrar por província
- `municipality` (string): Filtrar por município
- `search` (string): Buscar por nome ou descrição
- `skip` (integer): Número de registros para pular (default: 0)
- `limit` (integer): Número máximo de registros (default: 100, max: 1000)

**Example Request:**

```
GET /services/?category=identity&province=Luanda&search=passaporte&limit=20
```

**Response (200):**

```json
{
  "services": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Emissão de Passaporte",
      "category": "identity",
      "description": "Emissão de passaporte para cidadãos angolanos",
      "scope": "national",
      "estimated_time": 30,
      "requirements": {...},
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "locations_count": 3
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 20,
  "has_more": false
}
```

### GET /services/{service_id}

Obtém detalhes de um serviço específico.

**Response (200):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Emissão de Passaporte",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 30,
  "requirements": {...},
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "locations_count": 3
}
```

**Erros Possíveis:**

- `404 Not Found`: Serviço não encontrado

### GET /services/{service_id}/with-locations

Obtém serviço com seus locais de atendimento.

**Response (200):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Emissão de Passaporte",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 30,
  "requirements": {...},
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "locations_count": 2,
  "locations": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174001",
      "service_id": "123e4567-e89b-12d3-a456-426614174000",
      "province": "Luanda",
      "municipality": "Luanda",
      "address": "Rua Amílcar Cabral, 123",
      "contact_info": {
        "phone": "+244 923 456 789",
        "email": "passaporte.luanda@mint.gov.ao",
        "working_hours": {
          "monday": "08:00-17:00",
          "tuesday": "08:00-17:00",
          "friday": "08:00-15:00"
        }
      },
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### PUT /services/{service_id}

Atualiza um serviço existente.

**Headers:**

```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Emissão de Passaporte - Atualizado",
  "estimated_time": 45,
  "requirements": {
    "documents": [
      "BI",
      "Certidão de nascimento",
      "Fotografias",
      "Comprovativo de residência"
    ],
    "age_requirement": 18,
    "fees": 18000,
    "validity_period": "5 anos"
  }
}
```

**Response (200):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Emissão de Passaporte - Atualizado",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 45,
  "requirements": {...},
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:45:00Z",
  "locations_count": 3
}
```

### PATCH /services/{service_id}/deactivate

Desativa um serviço.

**Headers:**

```
Authorization: Bearer <admin_token>
```

**Response (200):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Emissão de Passaporte",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 30,
  "requirements": {...},
  "is_active": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z",
  "locations_count": 3
}
```

### POST /services/{service_id}/locations

Adiciona um local de atendimento para um serviço.

**Headers:**

```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "province": "Luanda",
  "municipality": "Luanda",
  "address": "Rua Amílcar Cabral, 123 - Luanda",
  "contact_info": {
    "phone": "+244 923 456 789",
    "email": "passaporte.luanda@mint.gov.ao",
    "working_hours": {
      "monday": "08:00-17:00",
      "tuesday": "08:00-17:00",
      "wednesday": "08:00-17:00",
      "thursday": "08:00-17:00",
      "friday": "08:00-15:00"
    }
  }
}
```

**Response (201):**

```json
{
  "id": "456e7890-e89b-12d3-a456-426614174001",
  "service_id": "123e4567-e89b-12d3-a456-426614174000",
  "province": "Luanda",
  "municipality": "Luanda",
  "address": "Rua Amílcar Cabral, 123 - Luanda",
  "contact_info": {
    "phone": "+244 923 456 789",
    "email": "passaporte.luanda@mint.gov.ao",
    "working_hours": {
      "monday": "08:00-17:00",
      "tuesday": "08:00-17:00",
      "wednesday": "08:00-17:00",
      "thursday": "08:00-17:00",
      "friday": "08:00-15:00"
    }
  },
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### GET /services/locations/

Lista locais de atendimento com filtros.

**Query Parameters:**

- `service_id` (UUID): Filtrar por ID do serviço
- `province` (string): Filtrar por província
- `municipality` (string): Filtrar por município
- `is_active` (boolean): Filtrar por status ativo (default: true)
- `skip` (integer): Número de registros para pular (default: 0)
- `limit` (integer): Número máximo de registros (default: 100, max: 1000)

**Response (200):**

```json
{
  "locations": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174001",
      "service_id": "123e4567-e89b-12d3-a456-426614174000",
      "province": "Luanda",
      "municipality": "Luanda",
      "address": "Rua Amílcar Cabral, 123",
      "contact_info": {...},
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100,
  "has_more": false
}
```

### GET /services/statistics/overview

Retorna estatísticas gerais dos serviços.

**Headers:**

```
Authorization: Bearer <admin_token>
```

**Response (200):**

```json
{
  "services": {
    "total": 25,
    "active": 23,
    "inactive": 2,
    "by_category": {
      "identity": 8,
      "civil_registry": 5,
      "immigration": 3,
      "education": 4,
      "health": 2,
      "social_security": 1,
      "taxes": 1,
      "business": 1
    },
    "by_scope": {
      "national": 15,
      "province": 7,
      "municipality": 3
    }
  },
  "locations": {
    "total": 45,
    "active": 42,
    "inactive": 3
  }
}
```

## 🔒 Autenticação e Autorização

### Tokens de Acesso

Todos os endpoints requerem autenticação via Bearer Token:

```
Authorization: Bearer <jwt_token>
```

### Níveis de Permissão

**Cidadãos:**

- Leitura de serviços e locais ativos
- Filtros e busca
- Consulta de detalhes

**Administradores:**

- CRUD completo de serviços
- Gestão de locais de atendimento
- Ativação/desativação
- Acesso a estatísticas

### Validação de Tokens

```python
# Exemplo de middleware de autenticação
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # Validação do token JWT
    # Retorna dados do usuário
    pass

async def require_admin_role(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Permissão de administrador necessária."
        )
    return current_user
```

## 🚨 Códigos de Erro

| Código | Descrição             | Exemplo                        |
| ------ | --------------------- | ------------------------------ |
| `400`  | Bad Request           | Dados malformados              |
| `401`  | Unauthorized          | Token inválido ou expirado     |
| `403`  | Forbidden             | Permissão insuficiente         |
| `404`  | Not Found             | Recurso não encontrado         |
| `409`  | Conflict              | Conflito de dados (duplicação) |
| `422`  | Unprocessable Entity  | Dados inválidos                |
| `500`  | Internal Server Error | Erro interno do servidor       |

### Exemplo de Resposta de Erro

```json
{
  "detail": "Já existe um serviço com o nome 'Emissão de Passaporte' na categoria 'identity'"
}
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest app/modules/service_hub/tests/

# Testes específicos
pytest app/modules/service_hub/tests/test_service_hub.py::TestServiceHubService::test_create_service_success

# Com cobertura
pytest --cov=app.modules.service_hub app/modules/service_hub/tests/
```

### Exemplo de Teste

```python
@pytest.mark.asyncio
async def test_create_service_success():
    # Arrange
    service_data = ServiceCreate(
        name="Emissão de BI",
        category=ServiceCategory.IDENTITY,
        scope=ServiceScope.NATIONAL
    )

    # Act
    result = await service_hub_service.create_service(service_data)

    # Assert
    assert result.name == service_data.name
    assert result.category == service_data.category
    assert result.is_active is True
```

## 📊 Monitoramento e Logs

### Logs Estruturados

```python
import logging

logger = logging.getLogger(__name__)

# Exemplo de log
logger.info(f"Serviço criado: {service.id} - {service.name}")
logger.error(f"Erro ao criar serviço: {str(e)}")
```

### Métricas Importantes

- Tempo de resposta dos endpoints
- Taxa de erro por endpoint
- Número de serviços criados/atualizados
- Consultas mais frequentes
- Uso de filtros

## 🔧 Configurações Avançadas

### Cache Redis

```python
# Configuração de cache para consultas frequentes
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_services(category: str):
    cache_key = f"services:category:{category}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    # Busca no banco e cacheia
    services = await service_hub_service.get_services_by_category(category)
    redis_client.setex(cache_key, 3600, json.dumps(services))
    return services
```

### Paginação Otimizada

```python
# Implementação de cursor-based pagination para grandes volumes
async def list_services_cursor(cursor: str = None, limit: int = 100):
    query = db.query(Service)

    if cursor:
        query = query.filter(Service.id > cursor)

    services = query.order_by(Service.id).limit(limit + 1).all()

    has_more = len(services) > limit
    if has_more:
        services = services[:-1]

    next_cursor = services[-1].id if services and has_more else None

    return {
        "services": services,
        "next_cursor": next_cursor,
        "has_more": has_more
    }
```

---

Esta documentação técnica fornece todas as informações necessárias para implementar,
testar e manter o módulo Service Hub do SILA.
