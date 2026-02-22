# Módulo Health (Sistema de Saúde)

# Sistema SILA - Backend

## 📋 Descrição

Módulo responsável pela gestão completa do sistema de saúde no SILA, incluindo
agendamentos, serviços médicos, prontuários eletrônicos e integração com unidades de
saúde. Implementa operações CRUD com banco de dados mockado para desenvolvimento.

## 🚀 Funcionalidades Principais

- **Gestão de serviços médicos** - Cadastro e controle de consultas, exames e
  procedimentos
- **Agendamentos inteligentes** - Sistema de marcação e gestão de consultas
- **Prontuários eletrônicos** - Registro completo de atendimentos médicos
- **Categorias de serviços** - Organização por tipo (consulta, exame, vacina,
  medicamento, internação)
- **Status em tempo real** - Controle de disponibilidade de serviços

## 📡 Endpoints Disponíveis

| Método   | Endpoint              | Descrição                  | Autenticação   | Funcionalidade       |
| -------- | --------------------- | -------------------------- | -------------- | -------------------- |
| `GET`    | `/health/ping`        | Health check do módulo     | ❌ Pública     | Verificação de saúde |
| `POST`   | `/health/`            | Criar registro de saúde    | ✅ Obrigatória | CRUD básico          |
| `GET`    | `/health/{record_id}` | Buscar registro específico | ✅ Obrigatória | Consulta individual  |
| `GET`    | `/health/`            | Listar todos os registros  | ✅ Obrigatória | Listagem completa    |
| `PUT`    | `/health/{record_id}` | Atualizar registro         | ✅ Obrigatória | Modificação          |
| `DELETE` | `/health/{record_id}` | Deletar registro           | ✅ Obrigatória | Exclusão             |

### ⚠️ Inconsistência Frontend/Backend Identificada

**Situação Atual:**

- **Backend oferece:** CRUD básico de registros de saúde (`/health/`, `/health/{id}`)
- **Frontend espera:** Sistema completo de saúde com serviços, agendamentos e
  prontuários

**Endpoints esperados pelo frontend:**

- `GET /health/services` - Lista de serviços médicos disponíveis
- `POST /health/appointments` - Agendar consulta/exame
- `GET /health/appointments/user` - Agendamentos do usuário
- `PATCH /health/appointments/{id}/cancel` - Cancelar agendamento
- `GET /health/records/{appointment_id}` - Prontuário médico

## 🔧 Configuração

- **Framework:** FastAPI com roteamento automático
- **Banco de dados:** PostgreSQL (planejado) + Mock em memória (atual)
- **Autenticação:** JWT obrigatória (exceto health check)
- **Estrutura:** MVC com services, models e schemas separados
- **Testes:** Cobertura básica implementada

## 🗂️ Estrutura do Módulo

```
health/
├── __init__.py          # Inicialização e configuração
├── endpoints.py         # Definição das rotas da API (6 endpoints)
├── crud.py             # Operações de banco de dados
├── models/             # Modelos SQLAlchemy (14 arquivos)
│   ├── __init__.py
│   ├── base.py
│   └── [12 modelos específicos]
├── schemas/            # Schemas Pydantic (13 arquivos)
│   ├── __init__.py
│   └── schemas.py
├── services/           # Lógica de negócio (3 arquivos)
├── routes/             # Rotas organizadas (12 arquivos)
├── tests/              # Testes automatizados (1 arquivo)
└── README.md           # Esta documentação
```

## 📚 Exemplos de Uso

### Exemplo básico - Health Check:

```python
from fastapi import FastAPI
from app.modules.health import router

app = FastAPI()
app.include_router(router, prefix="/health", tags=["health"])

# Health check público disponível
# GET /health/ping
```

### Exemplo avançado - Cliente HTTP:

```bash
# Health check (público)
curl "http://localhost:8000/health/ping"

# Criar registro de saúde (autenticado)
curl -X POST "http://localhost:8000/health/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "João Silva",
    "symptoms": "Febre alta",
    "diagnosis": "Gripe comum"
  }'

# Buscar registro específico
curl -X GET "http://localhost:8000/health/RECORD_ID" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Listar todos os registros
curl -X GET "http://localhost:8000/health/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Exemplo integração frontend:

```typescript
import { healthAPI } from "@/features/health/api";

try {
  // Em desenvolvimento - endpoints ainda não implementados no backend
  const services = await healthAPI.getServices();
  const appointments = await healthAPI.getUserAppointments();

  console.log("Serviços de saúde:", services);
  console.log("Meus agendamentos:", appointments);
} catch (error) {
  console.error("Erro ao carregar dados de saúde:", error);
  // Fallback: dados mockados para desenvolvimento
}
```

## 🔗 Dependências

- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para modelos de dados
- **Pydantic** - Validação e serialização
- **UUID** - Geração de identificadores únicos
- **Módulos internos:**
  - `app.core.auth` - Verificação de autenticação
  - `app.db.session` - Conexão com banco de dados

## ⚠️ Observações Importantes

- **Banco mockado** - Atualmente usa dicionário em memória
- **Produção:** Migrar para PostgreSQL com modelos reais
- **Autenticação obrigatória** - Exceto endpoint de ping
- **Dados sensíveis** - Requer cuidado com informações médicas
- **Conformidade** - Deve seguir normas de saúde (LGPD, HIPAA)

## 🚨 Inconsistências Críticas Identificadas

- **Estrutura incompatível** - Frontend espera sistema de agendamentos completo
- **Banco mockado** - Não adequado para produção
- **Falta de serviços médicos** - Apenas registros básicos implementados
- **Schemas inadequados** - Não correspondem às expectativas do frontend

## 🔧 Implementação Recomendada (Próximas Sprints)

### **Estrutura Necessária:**

1. **Modelos de Serviços** - Tabela de serviços médicos disponíveis
2. **Sistema de Agendamentos** - Gestão de consultas e exames
3. **Prontuários Eletrônicos** - Integração com registros médicos
4. **Banco de Dados Real** - Migração do mock para PostgreSQL

### **Endpoints a Implementar:**

1. `GET /health/services` - Lista de serviços médicos
2. `POST /health/appointments` - Criar agendamento
3. `GET /health/appointments/user` - Agendamentos do usuário
4. `PATCH /health/appointments/{id}/cancel` - Cancelar agendamento
5. `GET /health/records/{appointment_id}` - Prontuário médico

### **Melhorias de Segurança:**

1. **Auditoria médica** - Log de todas as operações
2. **Controle de acesso** - Permissões por especialidade médica
3. **Criptografia** - Dados médicos sensíveis
4. **Backup automático** - Proteção de dados críticos

## 👥 Responsáveis

- **Desenvolvedor:** Equipe SILA - Módulo Saúde
- **Última atualização:** $(date +%Y-%m-%d)
- **Status:** Ativo - Requer implementação completa
- **Prioridade:** Alta - Sistema crítico para cidadãos

## 📞 Contato

Para dúvidas ou problemas relacionados ao módulo de saúde, entre em contato com a equipe
de desenvolvimento.

**Email:** dev@sila.gov.ao **Slack:** #sila-backend-health

## 🎯 Roadmap de Desenvolvimento

### **Sprint Atual:**

- [ ] Implementar modelos de serviços médicos
- [ ] Criar sistema básico de agendamentos
- [ ] Migrar do banco mockado para PostgreSQL básico

### **Próximo Sprint:**

- [ ] Implementar prontuários eletrônicos
- [ ] Adicionar notificações de agendamento
- [ ] Integrar com unidades de saúde reais

### **Sprint Futuro:**

- [ ] Telemedicina básica
- [ ] Integração com SUS
- [ ] Relatórios epidemiológicos

---

_Documentação técnica detalhada - Sistema em desenvolvimento ativo_ _Última revisão:
$(date +%Y-%m-%d) - SILA Documentation Team_ _Status: Requer implementação urgente dos
endpoints esperados pelo frontend_
