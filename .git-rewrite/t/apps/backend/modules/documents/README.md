# Módulo Documents (Gestão Documental)

# Sistema SILA - Backend

## 📋 Descrição

Módulo responsável pela gestão completa do sistema de documentos no SILA, incluindo
armazenamento seguro, organização, busca avançada e controle de acesso a documentos
oficiais, contratos, certidões e arquivos municipais. Implementa funcionalidades
essenciais para arquivamento digital e compliance documental.

## 🚀 Funcionalidades Principais

- **Armazenamento seguro** - Upload e organização de documentos digitais
- **Categorização inteligente** - Classificação automática por tipo e conteúdo
- **Busca avançada** - Filtros por data, categoria, tamanho e conteúdo
- **Controle de acesso** - Permissões granulares por usuário e documento
- **Auditoria completa** - Log de todas as operações documentais
- **Integração storage** - Suporte a múltiplos provedores de armazenamento

## 📡 Endpoints Disponíveis

| Método | Endpoint          | Descrição              | Autenticação | Funcionalidade       |
| ------ | ----------------- | ---------------------- | ------------ | -------------------- |
| `GET`  | `/documents/ping` | Health check do módulo | ❌ Pública   | Verificação de saúde |

### ⚠️ Status Atual - Em Desenvolvimento Básico

**Observação:** Módulo em fase inicial de implementação

**Endpoints planejados (baseado no frontend):**

- `GET /documents/user` - Documentos do usuário autenticado
- `POST /documents/upload` - Upload de novo documento
- `GET /documents/{id}` - Buscar documento específico
- `DELETE /documents/{id}` - Remover documento
- `PATCH /documents/{id}` - Atualizar metadados

## 🔧 Configuração

- **Framework:** FastAPI com upload multipart
- **Banco de dados:** PostgreSQL com modelos relacionais
- **Armazenamento:** Sistema de arquivos + S3 (planejado)
- **Autenticação:** JWT obrigatória em operações documentais
- **Estrutura:** MVC completo com validação robusta
- **Schemas:** 5 schemas Pydantic para validação
- **Testes:** Cobertura básica implementada

## 🗂️ Estrutura do Módulo

```
documents/
├── __init__.py          # Inicialização e configuração (181 linhas)
├── endpoints.py         # Definição das rotas da API (7 linhas - básico)
├── crud.py             # Operações de banco de dados (29 linhas)
├── models/             # Modelos SQLAlchemy (5 arquivos)
│   └── models.py       # Definições principais (242 linhas)
├── schemas/            # Schemas Pydantic (5 arquivos)
│   └── schemas.py      # Validação de dados (188 linhas)
├── services/           # Lógica de negócio (3 arquivos)
├── routes/             # Rotas organizadas (5 arquivos)
├── tests/              # Testes automatizados (1 arquivo)
└── README.md           # Esta documentação
```

## 📚 Exemplos de Uso

### Exemplo básico - Health Check:

```python
from fastapi import FastAPI
from app.modules.documents import router

app = FastAPI()
app.include_router(router, prefix="/documents", tags=["documents"])

# Health check público disponível
# GET /documents/ping
```

### Exemplo avançado - Cliente HTTP (endpoints planejados):

```bash
# Health check (público)
curl "http://localhost:8000/documents/ping"

# Buscar documentos do usuário (autenticado)
curl -X GET "http://localhost:8000/documents/user" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Upload de documento (autenticado + multipart)
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@contrato.pdf" \
  -F "title=Contrato Social" \
  -F "category=contrato" \
  -F "description=Contrato social da empresa"

# Buscar documento específico (autenticado)
curl -X GET "http://localhost:8000/documents/DOCUMENT_ID" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Exemplo integração frontend:

```typescript
import { documentsAPI } from "@/features/documents/api";

try {
  // Em desenvolvimento - endpoints ainda não implementados no backend
  const documents = await documentsAPI.getUserDocuments({
    category: "contrato",
    status: "active",
  });

  console.log("Documentos encontrados:", documents.length);

  // Upload de novo documento
  const fileInput = document.getElementById("fileInput") as HTMLInputElement;
  if (fileInput.files?.[0]) {
    await documentsAPI.uploadDocument(fileInput.files[0], "Novo Contrato", "contrato");
  }
} catch (error) {
  console.error("Erro ao gerenciar documentos:", error);
  // Fallback: dados mockados para desenvolvimento
}
```

## 🔗 Dependências

- **FastAPI** - Framework web com suporte a upload
- **SQLAlchemy** - ORM para metadados documentais
- **Pydantic** - Validação de dados de documentos
- **Python-multipart** - Processamento de uploads
- **Módulos internos:**
  - `app.core.auth` - Sistema de autenticação
  - `app.db.session` - Gerenciamento de conexão
  - `app.models.base` - Modelos base do sistema

## ⚠️ Observações Importantes

- **Módulo em desenvolvimento** - Implementação básica em andamento
- **Estrutura preparada** - 5 modelos e schemas prontos
- **Dados sensíveis** - Requer criptografia adequada
- **Conformidade LGPD** - Controle rigoroso de dados pessoais
- **Storage externo** - Recomenda-se S3 para produção

## 🚨 Status de Implementação

### **Componentes Implementados:**

- ✅ **Modelos de dados** - 5 modelos SQLAlchemy definidos
- ✅ **Schemas Pydantic** - 5 schemas para validação
- ✅ **Estrutura de services** - 3 serviços básicos criados
- ✅ **Sistema de routes** - 5 arquivos de rotas organizadas
- ✅ **Testes básicos** - Cobertura inicial implementada

### **Componentes Pendentes:**

- ❌ **Endpoints ativos** - Apenas health check implementado
- ❌ **Sistema de upload** - Funcionalidade de armazenamento não implementada
- ❌ **Busca avançada** - Filtros e pesquisa não funcionais
- ❌ **Storage externo** - Integração com S3 pendente

## 🔧 Implementação Recomendada (Próximas Sprints)

### **Prioridade 1 - Funcionalidades Básicas:**

1. **Implementar upload** - Sistema completo de armazenamento seguro
2. **Busca e filtros** - Pesquisa avançada por metadados
3. **Controle de acesso** - Permissões granulares por documento
4. **Organização por pastas** - Estrutura hierárquica de documentos

### **Prioridade 2 - Recursos Avançados:**

1. **Versionamento** - Controle de versões de documentos
2. **Compartilhamento** - Links públicos seguros para documentos
3. **OCR automático** - Extração de texto de PDFs/imagens
4. **Categorias inteligentes** - Classificação automática por IA

### **Melhorias Técnicas:**

1. **Otimização de storage** - Compressão e deduplicação
2. **Cache inteligente** - Redis para metadados frequentes
3. **Auditoria completa** - Log de todas as operações
4. **Backup automático** - Proteção contra perda de dados

## 👥 Responsáveis

- **Desenvolvedor:** Equipe SILA - Módulo Documentos
- **Última atualização:** $(date +%Y-%m-%d)
- **Status:** Ativo - Em desenvolvimento estrutural
- **Prioridade:** Alta - Sistema crítico para compliance

## 📞 Contato

Para dúvidas ou problemas relacionados ao módulo de documentos, entre em contato com a
equipe de desenvolvimento.

**Email:** dev@sila.gov.ao **Slack:** #sila-backend-documents

## 🎯 Roadmap de Desenvolvimento

### **Sprint Atual:**

- [ ] Implementar sistema básico de upload
- [ ] Desenvolver busca e filtros simples
- [ ] Criar controle de acesso básico

### **Próximo Sprint:**

- [ ] Implementar versionamento de documentos
- [ ] Adicionar compartilhamento seguro
- [ ] Integrar com storage externo (S3)

### **Sprint Futuro:**

- [ ] OCR e indexação automática
- [ ] Workflows de aprovação
- [ ] Integração com assinatura digital

---

_Documentação técnica detalhada - Sistema em desenvolvimento estrutural_ _Última
revisão: $(date +%Y-%m-%d) - SILA Documentation Team_ _Status: Implementação de
funcionalidades documentais essenciais necessária_
