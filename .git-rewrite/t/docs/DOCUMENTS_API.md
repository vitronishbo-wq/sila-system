# 📋 SILA System - Módulo Documents API Documentation

## 📖 Visão Geral

O **Módulo Documents** do SILA System fornece uma API RESTful completa para gestão
segura de documentos digitais, incluindo upload, organização, controle de acesso,
auditoria e compartilhamento.

## 🚀 Características Principais

- ✅ **Upload Seguro**: Validação de tipos, tamanho e checksum
- ✅ **Controle Granular de Acesso**: Permissões específicas por documento
- ✅ **Organização Hierárquica**: Pastas com estrutura de árvore
- ✅ **Busca Avançada**: Filtros múltiplos e texto livre
- ✅ **Compartilhamento Seguro**: Tokens únicos com controle de uso
- ✅ **Auditoria Completa**: Log de todas as operações
- ✅ **Versionamento**: Controle de alterações de documentos
- ✅ **Templates**: Modelos reutilizáveis de documentos

## 🔗 Endpoints Principais

### Base URL

```
http://localhost:8000/api/v1/documents
```

---

## 📡 API Endpoints

### 🏥 Health Check

#### `GET /ping`

Verifica se o módulo está operacional.

**Response:**

```json
{
  "status": "healthy",
  "module": "documents",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "features": [
    "document_upload",
    "document_management",
    "folder_organization",
    "access_control",
    "audit_logging",
    "secure_sharing"
  ]
}
```

---

### 📄 Gestão de Documentos

#### `GET /user`

Lista documentos do usuário autenticado com filtros e paginação.

**Query Parameters:**

- `category` (string): Filtrar por categoria
- `document_type` (string): Filtrar por tipo de documento
- `status_filter` (string): Filtrar por status
- `folder_id` (string): Filtrar por pasta
- `search_text` (string): Texto de busca
- `page` (int): Página (padrão: 1)
- `size` (int): Itens por página (padrão: 20, máximo: 100)

**Response:**

```json
{
  "documents": [
    {
      "id": "uuid-string",
      "title": "Contrato Social",
      "description": "Contrato social da empresa",
      "category": "contrato",
      "document_type": "pdf",
      "status": "active",
      "file_size": 245760,
      "tags": ["contrato", "empresa"],
      "is_public": false,
      "permission_level": "restricted",
      "download_count": 5,
      "version": 1,
      "created_by": "uuid-user",
      "created_by_name": "João Silva",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "folder_id": "uuid-folder",
      "folder_name": "Contratos",
      "download_url": "/api/v1/documents/uuid/download",
      "preview_url": "/api/v1/documents/uuid/preview"
    }
  ],
  "total": 25,
  "page": 1,
  "size": 20,
  "total_pages": 2
}
```

#### `POST /upload`

Realiza upload de novo documento.

**Form Data:**

- `file` (file): Arquivo a ser enviado
- `title` (string): Título do documento
- `description` (string, opcional): Descrição detalhada
- `category` (string): Categoria do documento
- `tags` (string): Tags como JSON array
- `is_public` (boolean): Se o documento é público
- `permission_level` (string): Nível de permissão
- `parent_folder_id` (string, opcional): ID da pasta pai

**Response:** Documento criado (ver estrutura em `/user`)

---

### 📁 Gestão de Pastas

#### `POST /folders`

Cria nova pasta para organização.

**Form Data:**

- `name` (string): Nome da pasta
- `description` (string, opcional): Descrição da pasta
- `parent_folder_id` (string, opcional): ID da pasta pai
- `is_public` (boolean): Se a pasta é pública

**Response:**

```json
{
  "id": "uuid-string",
  "name": "Contratos",
  "description": "Documentos contratuais",
  "parent_folder_id": null,
  "is_public": false,
  "created_by": "uuid-user",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "document_count": 0
}
```

---

### 🔗 Compartilhamento Seguro

#### `POST /{document_id}/share`

Cria link de compartilhamento para documento.

**Form Data:**

- `expires_at` (string, opcional): Data de expiração (ISO format)
- `max_downloads` (int, opcional): Número máximo de downloads
- `password_protected` (boolean): Se requer senha
- `allow_download` (boolean): Permite download

**Response:**

```json
{
  "id": "uuid-string",
  "document_id": "uuid-document",
  "share_token": "abc123...",
  "created_by": "uuid-user",
  "created_at": "2024-01-15T10:30:00Z",
  "download_count": 0,
  "is_active": true,
  "expires_at": "2024-01-22T10:30:00Z",
  "max_downloads": 10,
  "password_protected": false,
  "allow_download": true
}
```

#### `GET /shared/{share_token}`

Acesso público a documento compartilhado.

**Response:** Informações básicas do documento (sem dados sensíveis)

#### `GET /shared/{share_token}/download`

Download público de documento compartilhado.

---

### 📊 Estatísticas e Métricas

#### `GET /statistics/me`

Obtém estatísticas pessoais de documentos.

**Response:**

```json
{
  "total_documents": 15,
  "documents_by_category": {
    "contrato": 8,
    "certidao": 3,
    "relatorio": 4
  },
  "documents_by_status": {
    "active": 14,
    "archived": 1
  },
  "total_size_bytes": 52428800,
  "avg_file_size_bytes": 3495253.33,
  "recent_uploads": 5,
  "top_uploaders": [
    {
      "name": "Maria Santos",
      "shared_count": 3
    }
  ]
}
```

---

## 🔐 Autenticação e Autorização

### Headers Obrigatórios

```
Authorization: Bearer <jwt_token>
Content-Type: application/json (para JSON)
Content-Type: multipart/form-data (para uploads)
```

### Níveis de Permissão

| Nível          | Descrição         | Acesso                                             |
| -------------- | ----------------- | -------------------------------------------------- |
| `public`       | Documento público | Todos os usuários autenticados                     |
| `restricted`   | Acesso restrito   | Apenas criador e usuários com permissão específica |
| `confidential` | Confidencial      | Apenas usuários autorizados explicitamente         |
| `secret`       | Alto sigilo       | Controle rigoroso de acesso                        |

### Permissões Granulares

- `can_download`: Permite download do arquivo
- `can_edit`: Permite edição de metadados
- `can_delete`: Permite exclusão do documento
- `can_share`: Permite compartilhamento com outros usuários

---

## 📁 Categorias de Documentos

| Categoria            | Descrição                       | Ícone |
| -------------------- | ------------------------------- | ----- |
| `contrato`           | Contratos e acordos             | 📄    |
| `certidao`           | Certidões e documentos oficiais | 🏛️    |
| `ato_administrativo` | Atos administrativos            | 📋    |
| `processo`           | Processos e procedimentos       | ⚖️    |
| `relatorio`          | Relatórios e análises           | 📊    |
| `comprovante`        | Comprovantes e recibos          | ✅    |
| `outros`             | Outros tipos de documentos      | 📄    |

---

## 📋 Tipos de Arquivo Suportados

| Tipo   | Extensões   | MIME Types                                                              |
| ------ | ----------- | ----------------------------------------------------------------------- |
| `pdf`  | .pdf        | application/pdf                                                         |
| `doc`  | .doc        | application/msword                                                      |
| `docx` | .docx       | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| `xls`  | .xls        | application/vnd.ms-excel                                                |
| `xlsx` | .xlsx       | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet       |
| `txt`  | .txt        | text/plain                                                              |
| `rtf`  | .rtf        | application/rtf                                                         |
| `jpg`  | .jpg, .jpeg | image/jpeg                                                              |
| `png`  | .png        | image/png                                                               |
| `gif`  | .gif        | image/gif                                                               |
| `tiff` | .tiff       | image/tiff                                                              |
| `zip`  | .zip        | application/zip                                                         |
| `rar`  | .rar        | application/x-rar-compressed                                            |

---

## 🚨 Tratamento de Erros

### Códigos de Status HTTP

| Código | Descrição                | Cenários                             |
| ------ | ------------------------ | ------------------------------------ |
| `200`  | Sucesso                  | Operação realizada com sucesso       |
| `201`  | Criado                   | Recurso criado com sucesso           |
| `400`  | Requisição Inválida      | Dados inválidos ou formato incorreto |
| `401`  | Não Autorizado           | Token inválido ou expirado           |
| `403`  | Proibido                 | Sem permissão para a operação        |
| `404`  | Não Encontrado           | Recurso não existe                   |
| `413`  | Entidade Muito Grande    | Arquivo excede limite de tamanho     |
| `422`  | Entidade Não Processável | Dados não podem ser processados      |
| `500`  | Erro Interno             | Erro inesperado no servidor          |

### Exemplos de Erro

**Erro de validação:**

```json
{
  "detail": "Dados de entrada inválidos",
  "errors": [
    {
      "field": "title",
      "message": "Título deve ter entre 1 e 255 caracteres",
      "code": "string_too_short"
    }
  ]
}
```

**Erro de permissão:**

```json
{
  "detail": "Sem permissão para acessar este documento",
  "code": "insufficient_permissions"
}
```

**Erro de arquivo:**

```json
{
  "detail": "Tipo de arquivo não permitido: .exe",
  "code": "file_type_not_allowed"
}
```

---

## 🔄 Versionamento de Documentos

Cada documento mantém controle de versão automático:

- **Versão inicial**: 1 (ao fazer upload)
- **Incremento automático**: A cada atualização significativa
- **Histórico preservado**: Todas as versões ficam disponíveis
- **Restauração**: Possibilidade de reverter para versão anterior

---

## 📊 Auditoria e Logs

Todas as operações são registradas automaticamente:

### Tipos de Ação Auditados

- `UPLOAD`: Novo documento enviado
- `DOWNLOAD`: Arquivo baixado
- `ACCESS`: Documento visualizado
- `UPDATE`: Metadados alterados
- `DELETE`: Documento removido
- `SHARE`: Compartilhamento criado
- `SHARED_ACCESS`: Acesso via link público
- `SHARED_DOWNLOAD`: Download via link público

### Campos do Log de Auditoria

```json
{
  "id": "uuid-log",
  "document_id": "uuid-document",
  "user_id": "uuid-user",
  "user_name": "Nome do Usuário",
  "action": "UPLOAD",
  "details": "Documento 'Contrato.pdf' enviado",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 📈 Métricas e Monitoramento

### Métricas Coletadas

- **Operações por hora**: Uploads, downloads, compartilhamentos
- **Taxa de erro**: Percentual de operações com falha
- **Tempo de resposta**: Média de duração das operações
- **Uso de storage**: Espaço ocupado por documentos
- **Usuários ativos**: Contagem de usuários únicos
- **Categorias populares**: Documentos por categoria

### Monitoramento em Tempo Real

- **Verificação automática**: A cada 30 segundos
- **Detecção de anomalias**: Alertas automáticos
- **Relatórios periódicos**: Geração automática de relatórios
- **Integração externa**: Webhooks e notificações

---

## 🔧 Configurações do Sistema

### Limites e Restrições

- **Tamanho máximo de arquivo**: 50MB
- **Arquivos por upload**: 1 arquivo por vez
- **Compartilhamentos ativos**: Sem limite
- **Logs de auditoria**: Retenção de 1 ano
- **Versões por documento**: Todas preservadas

### Configurações de Storage

- **Diretório padrão**: `/opt/sila-system/uploads/documents/`
- **Organização**: Por UUID do documento
- **Backup automático**: Configurável via política
- **Compressão**: Opcional para tipos específicos

---

## 🚀 Exemplos de Uso

### 1. Upload de Documento (Frontend)

```typescript
import { DocumentsAPI } from "@/packages/shared-api";

const handleUpload = async (file: File) => {
  try {
    const document = await DocumentsAPI.uploadDocument(file, {
      title: file.name,
      description: "Documento enviado via interface web",
      category: "outros",
      tags: ["web-upload"],
      is_public: false,
      permission_level: "restricted",
    });

    console.log("Documento enviado:", document);
    return document;
  } catch (error) {
    console.error("Erro no upload:", error);
    throw error;
  }
};
```

### 2. Busca com Filtros (Frontend)

```typescript
const searchDocuments = async (filters: DocumentSearchFilters) => {
  try {
    const result = await DocumentsAPI.getUserDocuments(
      filters,
      1, // página
      20, // itens por página
    );

    setDocuments(result.documents);
    setTotal(result.total);
    return result;
  } catch (error) {
    console.error("Erro na busca:", error);
  }
};
```

### 3. Compartilhamento Seguro (Frontend)

```typescript
const shareDocument = async (documentId: string) => {
  try {
    const share = await DocumentsAPI.shareDocument(documentId, {
      expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      max_downloads: 10,
      allow_download: true,
    });

    const shareUrl = `${window.location.origin}/shared/${share.share_token}`;
    await navigator.clipboard.writeText(shareUrl);

    return shareUrl;
  } catch (error) {
    console.error("Erro no compartilhamento:", error);
  }
};
```

---

## 🔗 Integrações Externas

### Webhooks

Configure webhooks para receber notificações de eventos:

```json
{
  "url": "https://seusistema.com/webhook/documents",
  "events": ["document.uploaded", "document.shared", "document.downloaded"],
  "secret": "seu-webhook-secret"
}
```

### Sistemas de Storage

- **Local**: Sistema de arquivos padrão
- **S3 Compatible**: MinIO, AWS S3, Google Cloud Storage
- **NFS**: Network File System para ambientes distribuídos

---

## 🛠️ Desenvolvimento e Testes

### Ambiente de Desenvolvimento

```bash
# Instalar dependências
pip install fastapi sqlalchemy pydantic python-multipart aiofiles

# Executar servidor de desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testes Automatizados

```bash
# Executar testes de integração
python modules/documents/test_integration.py

# Executar validação do módulo
python modules/documents/validate_module.py

# Monitoramento em tempo real
python monitor_documents.py
```

### Debugging

```bash
# Logs detalhados
export LOG_LEVEL=DEBUG

# Profiling de performance
python -m cProfile -s time modules/documents/test_integration.py
```

---

## 📚 Recursos Adicionais

### Guias de Implementação

- [Frontend Integration Guide](./frontend-integration.md)
- [Authentication Setup](./auth-setup.md)
- [Storage Configuration](./storage-config.md)

### Exemplos Completos

- [Upload com Progresso](./examples/upload-progress.tsx)
- [Busca Avançada](./examples/advanced-search.tsx)
- [Compartilhamento Seguro](./examples/secure-sharing.tsx)

### Ferramentas de Desenvolvimento

- [API Testing Tool](./tools/api-tester.html)
- [Schema Validator](./tools/schema-validator.py)
- [Performance Monitor](./tools/performance-monitor.py)

---

## 🆘 Suporte e Troubleshooting

### Problemas Comuns

**1. Upload falhando**

```bash
# Verificar tamanho do arquivo
# Máximo: 50MB por arquivo

# Verificar tipo de arquivo suportado
# Apenas extensões listadas são permitidas
```

**2. Permissões insuficientes**

```bash
# Verificar autenticação
# Token JWT deve estar válido

# Verificar permissões específicas
# Usuário deve ter can_download, can_edit, etc.
```

**3. Performance lenta**

```bash
# Verificar índices do banco
# Consultas devem usar índices adequados

# Verificar recursos do sistema
# Monitorar CPU, memória e disco
```

### Logs de Diagnóstico

```bash
# Logs da aplicação
tail -f /var/log/sila/documents.log

# Métricas de performance
python monitor_documents.py --metrics

# Verificar saúde do sistema
curl http://localhost:8000/api/v1/documents/ping
```

### Contato da Equipe

- **Email**: dev@sila.gov.ao
- **Slack**: #sila-backend-documents
- **GitHub Issues**:
  [sila-system/documents](https://github.com/sila-system/documents/issues)

---

## 🎯 Roadmap de Desenvolvimento

### Próximo Sprint

- [ ] Implementar OCR automático para PDFs
- [ ] Adicionar assinatura digital integrada
- [ ] Melhorar interface de busca com filtros visuais
- [ ] Implementar versionamento colaborativo

### Melhorias Técnicas

- [ ] Otimização de consultas com caching Redis
- [ ] Compressão automática de arquivos grandes
- [ ] Integração com sistemas de backup automático
- [ ] API de webhook para eventos em tempo real

### Recursos Avançados

- [ ] Workflows de aprovação automática
- [ ] Integração com IA para classificação automática
- [ ] Sincronização multi-dispositivo
- [ ] Modo offline para documentos críticos

---

_Documentação técnica atualizada em: $(date +%Y-%m-%d)_ _SILA System - Módulo Documents
v1.0.0_ _Status: Produção - Sistema operacional e documentado_
