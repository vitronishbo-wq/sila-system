# HIGH COUPLING EVENTS ANALYSIS

> Gerado em: 2026-06-08
> Proposito: Investigar eventos `citizen_updated` e `identity_verified` — acoplamento, risco e plano

---

## Secao 1: citizen_updated

### Publisher
identity

### Subscribers (12 modulos)
- educacao
- saude
- justica
- payment
- registo-civil
- financas-impostos
- administracao-local
- seguranca-social
- apoio-empresarial
- comercio
- emprego
- trabalho-inspecao

### Risco Estrutural
| Fator | Avaliacao |
|---|---|
| Single point of failure | **ALTO** — identity e o unico publisher para 11 consumidores |
| Acoplamento temporal | **ALTO** — todos os 11 modulos dependem deste evento para funcionar |
| Residencia a falhas | **BAIXA** — se identity falha, 11 modulos param de receber atualizacoes |
| Escalabilidade | **CRITICO** — 11 subscribers num unico publisher cria gargalo |

### Dependencias (Processos que dependem de citizen_updated)
- educacao -> Matricula Escolar
- saude -> Marcacao Consulta
- justica -> Emissao Documentos
- payment -> Pagamentos
- registo-civil -> Registo Nascimento
- financas-impostos -> Emissao NIF
- administracao-local -> Licenciamento
- seguranca-social -> Pensoes
- apoio-empresarial -> Abertura Empresa
- comercio -> Alvara Comercial
- emprego -> Contratacao Laboral
- trabalho-inspecao -> Inspecao

## Secao 2: identity_verified

### Publisher
identity

### Subscribers (12 modulos)
- educacao
- saude
- justica
- payment
- registo-civil
- financas-impostos
- administracao-local
- seguranca-social
- apoio-empresarial
- comercio
- emprego
- trabalho-inspecao

### Risco Estrutural
| Fator | Avaliacao |
|---|---|
| Single point of failure | **ALTO** — mesmo publisher que citizen_updated |
| Duplicacao | **MEDIO** — identity_verified e sempre precedido por citizen_updated |
| Carga | **ALTA** — 11 subscribers x 2 eventos = 22 entregas por transacao |

## Secao 3: Analise de Codigo vs Registry

### Problema Identificado: Eventos Fantasma

Os eventos registados no `RegistryCatalog` (governanca) **NAO correspondem** aos eventos implementados no codigo:

| Registry (bootstrap.py) | Codigo Real (events.py) | Gap |
|---|---|---|
| citizen_updated | IdentityDocumentVerified, IdentityDocumentStatusChanged | **NAO EXISTE** |
| identity_verified | IdentityDocumentVerified | **NOME DIFERENTE** |
| student_enrolled | StudentEnrolled (classe) | Correspondencia, mas nome diferente |
| payment_confirmed | PaymentProcessed | **NAO EXISTE** |
| bi_issued | IdentityCredentialIssued | **NAO EXISTE** |

### Consequencias
1. **Eventos orfaos a nivel de governanca** — `citizen_updated` nao e publicado por nenhum modulo real
2. **Acoplamento ficticio** — os 11 subscribers declarados nunca recebem `citizen_updated`
3. **Rastreabilidade quebrada** — nao e possivel auditar o fluxo de eventos

## Secao 4: Plano de Remediacao

### Acao Imediata
1. **Renomear registry events** para corresponder aos eventos reais:
   - `citizen_updated` -> `IdentityDocumentVerified`, `IdentityDocumentStatusChanged`
   - `identity_verified` -> `IdentityDocumentVerified`
   - `payment_confirmed` -> `PaymentProcessed`
   - `bi_issued` -> `IdentityCredentialIssued`

### Acao Curto Prazo
2. **Adicionar eventos reais** nos 29 modulos que tem `application/event_handlers.py`
3. **Sincronizar RegistryCatalog** com eventos reais via scan automatizado

### Acao Longo Prazo
4. **Implementar Event Mesh real** com:
   - Schema registry para eventos
   - Publisher/subscriber discovery automatico
   - Validacao de contratos entre publishers e subscribers

## Secao 5: Matriz de Eventos Reais (Code Level)

Modulos com `application/event_handlers.py` (28 modulos):
- administracao-local
- audit
- civil_protection
- compliance
- documents
- economy
- educacao
- energy
- governance
- identity
- industry
- infrastructure
- infrastructure_sector
- intelligence
- justice
- logistics
- migration_service
- notifications
- operations
- payment
- procurement
- public_security
- resources
- saude
- society
- tourism
- wallet
- xroad

## Conclusao

| Evento | Risco | Acao |
|---|---|---|
| citizen_updated | ALTO — fantasma, 11 subscribers ficticios | Renomear/sincronizar com codigo real |
| identity_verified | ALTO — fantasma, 11 subscribers ficticios | Renomear/sincronizar com codigo real |
| Ambos | **ACOPLAMENTO ESTRUTURAL** | Implementar Event Mesh ou fila de eventos |
