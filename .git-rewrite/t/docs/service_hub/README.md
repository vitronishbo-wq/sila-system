# Service Hub - Catálogo de Serviços Públicos Digitais

## 📋 Visão Geral

O **Service Hub** é o repositório central de serviços públicos digitais do SILA (Sistema
Integrado de Licenciamento e Atendimento). Este módulo cataloga todos os serviços
oferecidos pelo governo, fornecendo dados estruturados que outros módulos utilizam para
funcionalidades como agendamentos, validações de cidadania e notificações.

## 🎯 Objetivos Principais

- **Catalogar** todos os serviços oferecidos pelo governo
- **Fornecer** dados estruturados para outros módulos do sistema
- **Permitir** ativar/desativar serviços por província, município ou nacionalmente
- **Facilitar** a descoberta de serviços pelos cidadãos
- **Suportar** integração com sistemas de agendamento e atendimento

## 🏗️ Arquitetura do Módulo

```
service_hub/
├── models/
│   ├── __init__.py
│   └── service_hub.py          # Modelos Service e ServiceLocation
├── schemas/
│   ├── __init__.py
│   └── service_hub.py          # Schemas de validação Pydantic
├── services/
│   ├── __init__.py
│   └── service_hub_service.py  # Lógica de negócio
├── routes/
│   ├── __init__.py
│   └── service_hub_routes.py   # Endpoints REST
└── tests/
    ├── __init__.py
    └── test_service_hub.py     # Testes abrangentes
```

## 📊 Modelos de Dados

### Service (Serviço)

Representa um serviço público oferecido pelo governo.

| Campo            | Tipo     | Descrição                                             |
| ---------------- | -------- | ----------------------------------------------------- |
| `id`             | UUID     | Identificador único                                   |
| `name`           | String   | Nome do serviço (ex: "Emissão de Passaporte")         |
| `category`       | Enum     | Categoria do serviço (identity, civil_registry, etc.) |
| `description`    | Text     | Descrição detalhada do serviço                        |
| `is_active`      | Boolean  | Status ativo/inativo                                  |
| `scope`          | Enum     | Escopo (national, province, municipality)             |
| `estimated_time` | Integer  | Tempo estimado em minutos                             |
| `requirements`   | JSON     | Documentos e requisitos necessários                   |
| `created_at`     | DateTime | Data de criação                                       |
| `updated_at`     | DateTime | Data da última atualização                            |

### ServiceLocation (Local de Atendimento)

Representa onde um serviço específico pode ser prestado.

| Campo          | Tipo     | Descrição                  |
| -------------- | -------- | -------------------------- |
| `id`           | UUID     | Identificador único        |
| `service_id`   | UUID     | ID do serviço (FK)         |
| `province`     | String   | Província                  |
| `municipality` | String   | Município                  |
| `address`      | Text     | Endereço completo          |
| `contact_info` | JSON     | Informações de contato     |
| `is_active`    | Boolean  | Status ativo/inativo       |
| `created_at`   | DateTime | Data de criação            |
| `updated_at`   | DateTime | Data da última atualização |

## 🏷️ Categorias de Serviços

O sistema suporta as seguintes categorias:

- **`identity`** - Documentos de identidade (BI, Passaporte)
- **`civil_registry`** - Registro civil (Nascimento, Casamento, Óbito)
- **`immigration`** - Imigração e vistos
- **`education`** - Serviços educacionais
- **`health`** - Serviços de saúde
- **`social_security`** - Segurança social
- **`taxes`** - Impostos e taxas
- **`business`** - Serviços para empresas
- **`transport`** - Transporte e mobilidade
- **`housing`** - Habitação
- **`other`** - Outros serviços

## 🌍 Escopos de Aplicação

- **`national`** - Serviço disponível em todo o país
- **`province`** - Serviço disponível em uma província específica
- **`municipality`** - Serviço disponível em um município específico

## 🔌 API Endpoints

### Serviços

| Método  | Endpoint                        | Descrição                 | Permissão     |
| ------- | ------------------------------- | ------------------------- | ------------- |
| `POST`  | `/services/`                    | Criar novo serviço        | Admin         |
| `GET`   | `/services/`                    | Listar serviços           | Cidadão/Admin |
| `GET`   | `/services/{id}`                | Obter detalhes do serviço | Cidadão/Admin |
| `GET`   | `/services/{id}/with-locations` | Serviço com locais        | Cidadão/Admin |
| `PUT`   | `/services/{id}`                | Atualizar serviço         | Admin         |
| `PATCH` | `/services/{id}/deactivate`     | Desativar serviço         | Admin         |
| `PATCH` | `/services/{id}/activate`       | Ativar serviço            | Admin         |

### Locais de Atendimento

| Método   | Endpoint                   | Descrição               | Permissão     |
| -------- | -------------------------- | ----------------------- | ------------- |
| `POST`   | `/services/{id}/locations` | Adicionar local         | Admin         |
| `GET`    | `/services/locations/`     | Listar locais           | Cidadão/Admin |
| `GET`    | `/services/locations/{id}` | Obter detalhes do local | Cidadão/Admin |
| `PUT`    | `/services/locations/{id}` | Atualizar local         | Admin         |
| `DELETE` | `/services/locations/{id}` | Remover local           | Admin         |

### Endpoints Auxiliares

| Método | Endpoint                                   | Descrição              | Permissão     |
| ------ | ------------------------------------------ | ---------------------- | ------------- |
| `GET`  | `/services/categories/{category}/services` | Serviços por categoria | Cidadão/Admin |
| `GET`  | `/services/scopes/{scope}/services`        | Serviços por escopo    | Cidadão/Admin |
| `GET`  | `/services/statistics/overview`            | Estatísticas gerais    | Admin         |

## 📝 Exemplo de Uso

### Criar um Serviço

```json
POST /services/
{
  "name": "Emissão de Passaporte",
  "category": "identity",
  "description": "Emissão de passaporte para cidadãos angolanos",
  "scope": "national",
  "estimated_time": 30,
  "requirements": {
    "documents": [
      "Bilhete de Identidade",
      "Certidão de nascimento",
      "2 fotografias 3x4"
    ],
    "age_requirement": 18,
    "fees": 15000,
    "validity_period": "5 anos"
  }
}
```

### Adicionar Local de Atendimento

```json
POST /services/{service_id}/locations
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

### Buscar Serviços

```json
GET /services/?category=identity&province=Luanda&search=passaporte
```

## 🔗 Integrações com Outros Módulos

### Appointments

- Usa `service_id` para identificar qual serviço foi agendado
- Consulta `estimated_time` para calcular duração do agendamento
- Verifica `requirements` para validar documentos do cidadão

### Identity/Citizenship

- Valida se o cidadão pode acessar determinado serviço
- Consulta `age_requirement` e outros critérios de elegibilidade
- Verifica `scope` para determinar disponibilidade geográfica

### Notifications

- Envia lembretes personalizados baseados no tipo de serviço
- Usa `contact_info` dos locais para notificações locais
- Consulta `estimated_time` para agendar lembretes

### Reports

- Gera estatísticas de serviços mais utilizados
- Analisa tempo médio de atendimento vs `estimated_time`
- Relatórios por categoria, escopo e localização

## 🔒 Segurança e Permissões

### Cidadãos

- **Leitura**: Podem consultar serviços e locais ativos
- **Filtros**: Podem filtrar por localização, categoria, etc.
- **Busca**: Podem buscar serviços por nome/descrição

### Administradores

- **CRUD Completo**: Podem criar, editar e desativar serviços
- **Gestão de Locais**: Podem adicionar/remover locais de atendimento
- **Estatísticas**: Acesso a relatórios e métricas do sistema
- **Ativação/Desativação**: Controle total sobre disponibilidade

## 🧪 Testes

O módulo inclui testes abrangentes cobrindo:

- ✅ Criação de serviços válidos
- ❌ Prevenção de serviços duplicados
- ✅ Listagem com filtros diversos
- ✅ Atualização de serviços e locais
- ✅ Ativação/desativação de serviços
- ✅ Gestão de locais de atendimento
- ✅ Validação de schemas
- ✅ Tratamento de erros
- ✅ Métodos auxiliares e estatísticas

## 📈 Métricas e Monitoramento

O sistema coleta as seguintes métricas:

- Total de serviços cadastrados
- Serviços ativos vs inativos
- Distribuição por categoria e escopo
- Total de locais de atendimento
- Locais ativos vs inativos
- Estatísticas de uso (quando integrado com appointments)

## 🚀 Próximos Passos

1. **Integração com Appointments**: Conectar com sistema de agendamentos
2. **Cache Inteligente**: Implementar cache para consultas frequentes
3. **Busca Avançada**: Adicionar busca semântica e filtros complexos
4. **Versionamento**: Controle de versões para mudanças em serviços
5. **Auditoria**: Log detalhado de alterações em serviços
6. **API Externa**: Integração com sistemas governamentais externos

## 📞 Suporte

Para dúvidas ou problemas relacionados ao Service Hub:

- **Documentação**: Consulte este README e a documentação da API
- **Logs**: Verifique os logs do sistema para detalhes de erros
- **Testes**: Execute os testes para validar funcionalidades
- **Issues**: Reporte problemas através do sistema de issues do projeto

---

**Service Hub** - Centralizando e organizando os serviços públicos digitais de Angola 🇦🇴
