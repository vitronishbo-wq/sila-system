# Wizard de Nova Matrícula Escolar — Especificação Completa

## Visão Geral

O serviço **Nova Matrícula Escolar** é o primeiro serviço canónico do módulo Educação. Substitui o fluxo actual de POST simples por um wizard de 7 passos orientado ao cidadão.

### Operação Híbrida (Fase Inicial)

- Cidadão fornece BI, nome, data de nascimento manualmente
- Sistema valida internamente sem dependência externa de registo civil
- Interoperabilidade futura: consulta automática via BI

---

## Fluxo do Wizard

```
Passo 1 ──> Passo 2 ──> Passo 3 ──> Passo 4 ──> Passo 5 ──> Passo 6 ──> Passo 7
Estudante   Encarregado   Escola       Documentos   Elegibilidade  Pagamento   Confirmação
```

### Estado por Passo

Cada passo do wizard tem um estado que persiste no backend:

```
RASCUNHO → PREENCHIDO → VALIDADO → CONFIRMADO
```

O wizard inteiro só pode ser submetido quando todos os 7 passos estão `CONFIRMADO`.

---

## Passo 1 — Dados do Estudante

### Objectivo
Recolher os dados fundamentais do estudante. Nesta fase híbrida, o cidadão fornece manualmente.

### Campos

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| `nome_completo` | string (200) | sim | >= 3 caracteres |
| `data_nascimento` | date | sim | >= 4 anos e <= 25 anos |
| `sexo` | enum (M/F) | sim | — |
| `bi` | string (14) | sim | Formato: 000000000AA000 |
| `nif` | string (10) | não | Formato: 000000000 |
| `nacionalidade` | string (50) | sim | Default: "Angolana" |
| `naturalidade` | string (100) | não | — |
| `filiacao_pai` | string (200) | não | — |
| `filiacao_mae` | string (200) | sim | — |
| `deficiencia` | enum | não | `nenhuma`, `motora`, `visual`, `auditiva`, `intelectual`, `multipla` |
| `necessidades_especiais` | text | não | — |
| `email` | string (100) | não | Formato email |
| `telefone` | string (20) | não | — |

### Endpoints

```
POST /educacao/matriculas/wizard/passo1/estudante
  → Salva dados do estudante (sessão wizard)
  → Retorna passo_id + dados validados

PUT /educacao/matriculas/wizard/passo1/estudante/{wizard_id}
  → Actualiza dados do estudante

GET /educacao/matriculas/wizard/passo1/estudante/{wizard_id}
  → Retorna dados do estudante
```

### Resposta

```json
{
  "wizard_id": "uuid",
  "passo": 1,
  "status": "CONFIRMADO",
  "dados": {
    "nome_completo": "João Agostinho Neto",
    "data_nascimento": "2012-03-15",
    "sexo": "M",
    "bi": "001234567LA045",
    "nacionalidade": "Angolana",
    "filiacao_mae": "Maria Neto"
  },
  "proximo_passo": "/educacao/matriculas/wizard/passo2"
}
```

---

## Passo 2 — Dados do Encarregado de Educação

### Objectivo
Identificar o responsável legal pelo estudante.

### Campos

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| `nome_completo` | string (200) | sim | >= 3 caracteres |
| `parentesco` | enum | sim | `pai`, `mae`, `tutor_legal`, `avô`, `outro` |
| `bi` | string (14) | sim | Formato BI |
| `telefone` | string (20) | sim | — |
| `email` | string (100) | sim | Formato email |
| `morada` | text | sim | — |
| `provincia` | string (50) | sim | — |
| `municipio` | string (50) | sim | — |
| `comuna` | string (50) | não | — |
| `profissao` | string (100) | não | — |
| `local_trabalho` | string (200) | não | — |

### Endpoints

```
POST /educacao/matriculas/wizard/passo2/encarregado
PUT /educacao/matriculas/wizard/passo2/encarregado/{wizard_id}
GET /educacao/matriculas/wizard/passo2/encarregado/{wizard_id}
```

---

## Passo 3 — Escolha da Escola / Turma

### Objectivo
Pesquisar e seleccionar a escola e turma pretendidas.

### Fluxo

1. Cidadão pesquisa escola por:
   - Nome
   - Província/Município
   - Tipo (pública/privada/comunitária)

2. Para cada resultado, ver:
   - Vagas disponíveis (por turno)
   - Distância (se georreferenciado)
   - Turnos disponíveis (manhã/tarde/noite)
   - Propina (se aplicável)

3. Seleccionar escola + turno + classe/ano

### Campos

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| `escola_id` | UUID | sim | Escola existe e tem vagas |
| `turma_id` | UUID | sim | Turma pertence à escola |
| `turno` | enum | sim | `manha`, `tarde`, `noite`, `integral` |
| `classe` | string (20) | sim | Compatível com idade do estudante |
| `ano_letivo_id` | UUID | sim | Ano lectivo vigente |
| `tipo_ensino` | enum | sim | `pre_escolar`, `primario`, `secundario_1`, `secundario_2` |

### Endpoints

```
GET  /educacao/matriculas/wizard/passo3/escolas?nome=&provincia=&tipo=
     → Lista escolas disponíveis com vagas

GET  /educacao/matriculas/wizard/passo3/escolas/{escola_id}/turmas?ano_letivo=
     → Lista turmas com vagas

POST /educacao/matriculas/wizard/passo3/selecionar
     → Seleciona escola + turma

PUT  /educacao/matriculas/wizard/passo3/selecionar/{wizard_id}
     → Altera selecção

GET  /educacao/matriculas/wizard/passo3/selecionar/{wizard_id}
     → Retorna selecção actual
```

### Regras de Negócio

- Escola deve ter vagas (validação em tempo real com lock optimista)
- Turno seleccionado deve ser compatível com o tipo de ensino
- Classe deve ser compatível com a idade do estudante (regra actual do `MatriculaService._idade_minima_para_contexto`)
- Não pode haver matrícula activa noutra escola no mesmo ano lectivo

---

## Passo 4 — Documentos

### Objectivo
Anexar os documentos obrigatórios para a matrícula.

### Documentos Obrigatórios

| # | Documento | Formato | Tamanho | Notas |
|---|-----------|---------|---------|-------|
| 1 | BI do Estudante | PDF/JPG | <= 5MB | Frente e verso |
| 2 | BI do Encarregado | PDF/JPG | <= 5MB | Frente e verso |
| 3 | Fotografia do Estudante | JPG/PNG | <= 2MB | 200x200px min |
| 4 | Certificado Anterior | PDF | <= 10MB | Se aplicável |
| 5 | Boletim Anterior | PDF | <= 10MB | Se aplicável |
| 6 | Comprovativo de Morada | PDF/JPG | <= 5MB | Factura ou declaração |

### Endpoints

```
POST /educacao/matriculas/wizard/passo4/documentos/upload
     → Upload multipart de documento
     → Retorna document_id + url temporário

GET  /educacao/matriculas/wizard/passo4/documentos/{wizard_id}
     → Lista documentos anexados (metadados, não conteúdo)

DELETE /educacao/matriculas/wizard/passo4/documentos/{wizard_id}/{document_id}
     → Remove documento anexado
```

### Resposta Upload

```json
{
  "document_id": "uuid",
  "tipo": "bi_estudante",
  "nome_original": "bi_joao.pdf",
  "tamanho_bytes": 245000,
  "content_type": "application/pdf",
  "url": "/api/v1/educacao/documentos/{document_id}/download",
  "uploaded_at": "2026-06-06T10:30:00Z"
}
```

---

## Passo 5 — Elegibilidade

### Objectivo
Validação automática da elegibilidade com base nos dados dos passos anteriores.

### Validações Executadas

| # | Validação | Origem dos Dados | Acção em Falha |
|---|-----------|------------------|----------------|
| 1 | Idade mínima para a classe/turno | Passo 1 + Passo 3 | Bloqueante |
| 2 | Escola tem vagas (lock) | Passo 3 | Bloqueante |
| 3 | BI do estudante válido (formato) | Passo 1 | Bloqueante |
| 4 | BI do encarregado válido (formato) | Passo 2 | Bloqueante |
| 5 | Duplicidade: matrícula activa? | Passo 1 + ano lectivo | Bloqueante |
| 6 | Documentos obrigatórios anexados | Passo 4 | Bloqueante |
| 7 | Conflito de horário/turno | Passo 3 | Warning |

### Endpoints

```
POST /educacao/matriculas/wizard/passo5/elegibilidade/{wizard_id}
     → Executa todas as validações
     → Retorna resultado por validação

GET  /educacao/matriculas/wizard/passo5/elegibilidade/{wizard_id}
     → Retorna resultado da última validação
```

### Resposta

```json
{
  "wizard_id": "uuid",
  "elegivel": true,
  "validacoes": [
    {"nome": "idade_minima", "status": "APROVADO", "detalhe": "12 anos >= 6 anos"},
    {"nome": "vagas_disponiveis", "status": "APROVADO", "detalhe": "15 vagas disponiveis"},
    {"nome": "documentos_obrigatorios", "status": "APROVADO", "detalhe": "6/6 documentos"},
    {"nome": "duplicidade", "status": "APROVADO", "detalhe": "Sem matricula activa"},
    {"nome": "bi_valido", "status": "APROVADO", "detalhe": "Formato BI valido"}
  ],
  "bloqueantes": 0,
  "warnings": 0
}
```

---

## Passo 6 — Pagamento

### Objectivo
Gerar referência ou processar pagamento da propina/matrícula.

### Operação Híbrida (Fase Inicial)

- Gerar referência multicaixa (simulada)
- Opções: `multicaixa`, `referencia`, `wallet` (simulados)
- Sem integração real com sistemas de pagamento

### Campos

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| `modalidade` | enum | sim |
| `comprovativo` | file | se multicaixa/wallet |
| `referencia_id` | string | gerado pelo sistema |

### Endpoints

```
POST /educacao/matriculas/wizard/passo6/pagamento/gerar-referencia/{wizard_id}
     → Gera referência de pagamento
     → Retorna entidade + referência + valor

POST /educacao/matriculas/wizard/passo6/pagamento/comprovativo/{wizard_id}
     → Upload de comprovativo de pagamento

GET  /educacao/matriculas/wizard/passo6/pagamento/{wizard_id}
     → Retorna status do pagamento
```

### Resposta

```json
{
  "wizard_id": "uuid",
  "modalidade": "referencia",
  "entidade": "12345",
  "referencia": "123456789",
  "valor": "2500.00",
  "moeda": "AOA",
  "status": "PENDENTE",
  "comprovativo_url": null
}
```

---

## Passo 7 — Confirmação

### Objectivo
Finalizar o processo, gerar número de matrícula e comprovativo.

### Acções Executadas

1. Criar entidade `Matricula` com status `PENDENTE`
2. Atribuir `numero_processo` (formato `MAT-{ano}-{escola}-{sequencial}`)
3. Associar todos os documentos ao processo
4. Notificar via `ServiceRequestLifecycleBridge` (já existente)
5. Emitir evento de domínio `StudentEnrolled` (já existente)
6. Gerar comprovativo PDF (simulado)
7. Gerar QR code da matrícula (simulado)

### Endpoints

```
POST /educacao/matriculas/wizard/passo7/confirmar/{wizard_id}
     → Finaliza o wizard, cria a matrícula
     → Retorna comprovativo + QR + numero processo

GET  /educacao/matriculas/wizard/passo7/comprovativo/{wizard_id}
     → Retorna comprovativo em PDF (ou link)

GET  /educacao/matriculas/wizard/passo7/qrcode/{wizard_id}
     → Retorna QR code da matrícula
```

### Resposta Final

```json
{
  "wizard_id": "uuid",
  "matricula_id": "uuid",
  "numero_processo": "MAT-2026-001-000452",
  "status": "PENDENTE",
  "estudante": "João Agostinho Neto",
  "escola": "Escola Primária 1234",
  "classe": "6ª Classe",
  "turno": "manha",
  "ano_letivo": "2026",
  "data_matricula": "2026-06-06",
  "qr_code_url": "/api/v1/educacao/matriculas/wizard/{wizard_id}/qrcode",
  "comprovativo_url": "/api/v1/educacao/matriculas/wizard/{wizard_id}/comprovativo"
}
```

---

## Estrutura de Dados (Backend)

### WizardSession (tabela: `educacao_wizard_matricula`)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | UUID PK | Identificador da sessão |
| `citizen_id` | UUID FK | Cidadão |
| `status` | enum | `em_curso`, `confirmado`, `cancelado`, `expirado` |
| `passo_atual` | int | 1-7 |
| `dados_estudante` | JSONB | Passo 1 |
| `dados_encarregado` | JSONB | Passo 2 |
| `selecao_escola` | JSONB | Passo 3 |
| `documentos` | JSONB[] | Passo 4 |
| `resultado_elegibilidade` | JSONB | Passo 5 |
| `pagamento` | JSONB | Passo 6 |
| `matricula_id` | UUID FK | Passo 7 (após confirmação) |
| `created_at` | timestamptz | |
| `updated_at` | timestamptz | |
| `expires_at` | timestamptz | TTL: 24h |

### Armazenamento de Documentos

- Fase inicial: sistema de ficheiros local (`storage/media/educacao/documentos/`)
- Futuro: Azure Blob Storage / S3
- Metadados em tabela `educacao_documentos`
- Hash SHA-256 para integridade

---

## Plano de Implementação (Backend)

### Fase 1 — Estrutura

| Tarefa | Ficheiros |
|--------|-----------|
| Criar modelo `WizardSessionModel` | `infrastructure/models/wizard_session_model.py` |
| Criar repositório `WizardSessionRepository` | `infrastructure/repositories/sqlalchemy_wizard_session_repository.py` |
| Criar porta `WizardSessionRepositoryPort` | `application/ports/wizard_session_repository_port.py` |
| Criar entidade `WizardSession` | `domain/wizard_session.py` |
| Criar schema `WizardPasso1Schema` | `api/schemas/wizard_schema.py` |
| Adicionar `migration` | `migrations/versions/` |

### Fase 2 — Wizard API

| Tarefa | Ficheiros |
|--------|-----------|
| Criar router do wizard | `api/endpoints/wizard_matricula.py` |
| Criar WizardService | `application/wizard_matricula_service.py` |
| Implementar Passo 1-4 | (no service) |
| Implementar Passo 5 (elegibilidade) | reutiliza `MatriculaService` existente |
| Implementar Passo 7 (confirmação) | chama `MatriculaService.criar_matricula` |

### Fase 3 — Integração Router Principal

| Tarefa | Ficheiros |
|--------|-----------|
| Incluir wizard_router no `router.py` | `api/router.py` |
| Adicionar dependências no `deps.py` | `api/deps.py` |
| Mapear excepções | `api/endpoints/wizard_matricula.py` |

---

## Integração com Serviços Existentes

| Serviço Existente | Utilização no Wizard |
|-------------------|---------------------|
| `MatriculaService.criar_matricula()` | Chamado no Passo 7 para criar a matrícula real |
| `MatriculaService._idade_minima_para_contexto()` | Reutilizado no Passo 5 |
| `TurmaRepository.count_matriculas_ativas()` | Reutilizado no Passo 5 |
| `EscolaRepository.get_by_id()` | Reutilizado no Passo 3 |
| `CitizenRepository` | Validação do cidadão (fase futura) |
| `ServiceRequestLifecycleBridge` | Notificação no Passo 7 |
| `RedisIdempotencyStore` | Idempotência da submissão final |

---

## Frontend

### Rotas (React Router)

```
/matriculas/nova           → Wizard página inicial (resumo dos 7 passos)
/matriculas/nova/passo1    → Dados do estudante
/matriculas/nova/passo2    → Dados do encarregado
/matriculas/nova/passo3    → Escolha da escola
/matriculas/nova/passo4    → Documentos
/matriculas/nova/passo5    → Elegibilidade (auto)
/matriculas/nova/passo6    → Pagamento
/matriculas/nova/passo7    → Confirmação
/matriculas/{id}           → Consultar matrícula
```

### Componentes

```
components/
  wizard/
    WizardProgressBar.tsx   → Barra de progresso (passo 1-7)
    WizardStep.tsx          → Wrapper de passo
    WizardNavigation.tsx    → Botões anterior/próximo/submeter
    Passo1Estudante.tsx     → Formulário estudante
    Passo2Encarregado.tsx   → Formulário encarregado
    Passo3Escola.tsx        → Pesquisa + selecção escola/turma
    Passo4Documentos.tsx    → Upload documentos
    Passo5Validacao.tsx     → Resultado validação
    Passo6Pagamento.tsx     → Pagamento
    Passo7Confirmacao.tsx   → Comprovativo + QR
```

### Estado (Zustand ou Context)

```typescript
interface WizardState {
  wizardId: string | null;
  passoAtual: Passo;
  passos: Record<Passo, PassoStatus>;
  estudante: DadosEstudante | null;
  encarregado: DadosEncarregado | null;
  escola: SelecaoEscola | null;
  documentos: DocumentoAnexado[];
  elegibilidade: ResultadoElegibilidade | null;
  pagamento: DadosPagamento | null;
  matricula: MatriculaConfirmada | null;
}
```
