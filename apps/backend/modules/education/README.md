# Módulo Education (Sistema Educacional)

# Sistema SILA - Backend

## 📋 Descrição

Módulo responsável pela gestão completa do sistema educacional no SILA, incluindo
matrículas escolares, emissão de documentos, certificados e integração com instituições
de ensino. Implementa funcionalidades essenciais para gestão educacional municipal e
atendimento ao cidadão estudante.

## 🚀 Funcionalidades Principais

- **Matrículas escolares** - Sistema de solicitação e acompanhamento de matrículas
- **Documentos educacionais** - Emissão de históricos, certificados e declarações
- **Gestão de serviços** - Catálogo organizado de serviços educacionais
- **Acompanhamento de processos** - Controle completo do ciclo de vida das solicitações
- **Integração escolar** - Conexão com instituições de ensino municipais

## 📡 Endpoints Disponíveis

| Método | Endpoint          | Descrição              | Autenticação | Funcionalidade       |
| ------ | ----------------- | ---------------------- | ------------ | -------------------- |
| `GET`  | `/education/ping` | Health check do módulo | ❌ Pública   | Verificação de saúde |

### ⚠️ Status Atual - Em Desenvolvimento Básico

**Observação:** Módulo em fase inicial de implementação

**Endpoints planejados (baseado no frontend):**

- `GET /education/services` - Lista de serviços educacionais
- `POST /education/enrollments` - Solicitar matrícula escolar
- `GET /education/enrollments/user` - Matrículas do usuário
- `POST /education/documents` - Solicitar documento escolar
- `GET /education/documents/user` - Documentos do usuário

## 🔧 Configuração

- **Framework:** FastAPI com estrutura modular organizada
- **Banco de dados:** PostgreSQL com modelos SQLAlchemy (12 modelos)
- **Autenticação:** JWT obrigatória em endpoints de usuário
- **Estrutura:** MVC completo com services, routes e schemas
- **Schemas:** 12 schemas Pydantic para validação
- **Testes:** Cobertura básica implementada

## 🗂️ Estrutura do Módulo

```
education/
├── __init__.py          # Inicialização e configuração (714 linhas)
├── endpoints.py         # Definição das rotas da API (7 linhas - básico)
├── models/             # Modelos SQLAlchemy (12 arquivos)
├── schemas/            # Schemas Pydantic (12 arquivos)
├── services/           # Lógica de negócio (2 arquivos)
├── routes/             # Rotas organizadas (12 arquivos)
├── tests/              # Testes automatizados (1 arquivo)
└── README.md           # Esta documentação
```

## 📚 Exemplos de Uso

### Exemplo básico - Health Check:

```python
from fastapi import FastAPI
from app.modules.education import router

app = FastAPI()
app.include_router(router, prefix="/education", tags=["education"])

# Health check público disponível
# GET /education/ping
```

### Exemplo avançado - Cliente HTTP (endpoints planejados):

```bash
# Health check (público)
curl "http://localhost:8000/education/ping"

# Buscar serviços educacionais (autenticado)
curl -X GET "http://localhost:8000/education/services" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Solicitar matrícula escolar (autenticado)
curl -X POST "http://localhost:8000/education/enrollments" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "serviceId": "matricula-fundamental",
    "schoolName": "Escola Municipal Silva Jardim",
    "grade": "5º ano",
    "academicYear": "2024",
    "documents": ["certidao-nascimento", "comprovante-residencia"]
  }'

# Solicitar documento escolar (autenticado)
curl -X POST "http://localhost:8000/education/documents" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "documentType": "historico-escolar"
  }'
```

### Exemplo integração frontend:

```typescript
import { educationAPI } from "@/features/education/api";

try {
  // Em desenvolvimento - endpoints ainda não implementados no backend
  const services = await educationAPI.getServices();
  const enrollments = await educationAPI.getUserEnrollments();
  const documents = await educationAPI.getUserDocuments();

  console.log("Serviços educacionais:", services);
  console.log("Minhas matrículas:", enrollments);
  console.log("Meus documentos:", documents);
} catch (error) {
  console.error("Erro ao carregar dados educacionais:", error);
  // Fallback: dados mockados para desenvolvimento
}
```

## 🔗 Dependências

- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para modelos educacionais
- **Pydantic** - Validação de dados escolares
- **Módulos internos:**
  - `app.core.auth` - Sistema de autenticação
  - `app.db.session` - Gerenciamento de conexão
  - `app.models.base` - Modelos base do sistema

## ⚠️ Observações Importantes

- **Módulo em desenvolvimento** - Implementação básica em andamento
- **Estrutura preparada** - 12 modelos e schemas prontos
- **Dados educacionais sensíveis** - Requer cuidado com informações escolares
- **Conformidade educacional** - Deve seguir normas do MEC e SME
- **Integração necessária** - Conexão com sistemas escolares existentes

## 🚨 Status de Implementação

### **Componentes Implementados:**

- ✅ **Modelos de dados** - 12 modelos SQLAlchemy definidos
- ✅ **Schemas Pydantic** - 12 schemas para validação
- ✅ **Estrutura de services** - 2 serviços básicos criados
- ✅ **Sistema de routes** - 12 arquivos de rotas organizadas
- ✅ **Testes básicos** - Cobertura inicial implementada

### **Componentes Pendentes:**

- ❌ **Endpoints ativos** - Apenas health check implementado
- ❌ **Lógica de negócio** - Services precisam implementação completa
- ❌ **Matrículas escolares** - Sistema de gestão não implementado
- ❌ **Documentos educacionais** - Emissão de certificados pendente

## 🔧 Implementação Recomendada (Próximas Sprints)

### **Prioridade 1 - Endpoints Essenciais:**

1. **Implementar serviços educacionais** - Catálogo de serviços disponíveis
2. **Sistema de matrículas** - Processo completo de inscrição escolar
3. **Gestão de documentos** - Emissão de históricos e certificados
4. **Acompanhamento de processos** - Status e notificações

### **Prioridade 2 - Funcionalidades Avançadas:**

1. **Portal do estudante** - Área personalizada para alunos
2. **Portal da instituição** - Gestão para escolas e professores
3. **Relatórios educacionais** - Métricas e indicadores escolares
4. **Integração MEC** - Conexão com sistemas nacionais

### **Melhorias Técnicas:**

1. **Otimização de consultas** - Índices para dados escolares
2. **Cache inteligente** - Redis para dados frequentemente acessados
3. **Auditoria educacional** - Log completo de operações escolares
4. **Validação de documentos** - Verificação de autenticidade

## 👥 Responsáveis

- **Desenvolvedor:** Equipe SILA - Módulo Educação
- **Última atualização:** $(date +%Y-%m-%d)
- **Status:** Ativo - Em desenvolvimento estrutural
- **Prioridade:** Alta - Sistema crítico para educação municipal

## 📞 Contato

Para dúvidas ou problemas relacionados ao módulo de educação, entre em contato com a
equipe de desenvolvimento.

**Email:** dev@sila.gov.ao **Slack:** #sila-backend-education

## 🎯 Roadmap de Desenvolvimento

### **Sprint Atual:**

- [ ] Implementar endpoints básicos de serviços
- [ ] Desenvolver sistema de matrículas escolares
- [ ] Criar gestão de documentos educacionais

### **Próximo Sprint:**

- [ ] Implementar portal do estudante
- [ ] Adicionar notificações escolares
- [ ] Integrar com sistemas educacionais

### **Sprint Futuro:**

- [ ] Portal institucional para escolas
- [ ] Relatórios avançados de desempenho
- [ ] Integração com plataformas de ensino online

---

_Documentação técnica detalhada - Sistema em desenvolvimento estrutural_ _Última
revisão: $(date +%Y-%m-%d) - SILA Documentation Team_ _Status: Implementação de
funcionalidades educacionais essenciais necessária_
