# Catálogo Canónico de Serviços — Módulo Educação

## Princípios

1. **Orientado ao objectivo do cidadão** — cada serviço resolve um problema real que o cidadão reconhece.
2. **Entregável de forma independente** — cada serviço canónico tem um fluxo completo (início → validação → execução → confirmação).
3. **Operações internas não são serviços públicos** — acções como "Agendamento de matrícula" ou "Licenciamento de matrícula" são subfluxos, não serviços autónomos.

---

## Mapeamento Serviço Canónico → Endpoint Actual

Legenda:
- `[canónico]` = serviço público orientado ao cidadão
- `[legado]` = endpoint existente que continuará a funcionar mas não aparece no catálogo público
- `[interno]` = subfluxo que não é exposto como serviço independente

---

### 1. ENSINO BÁSICO

| # | Serviço Canónico | Endpoint Actual | Tipo |
|---|-----------------|-----------------|------|
| 1 | **Nova Matrícula Escolar** | `POST /educacao/matriculas/` + novo wizard | `[canónico]` |
| 2 | **Renovação de Matrícula** | (novo) | `[canónico]` |
| 3 | **Transferência Escolar** | `POST /educacao/transferencias/` | `[canónico]` |
| 4 | **Consultar Matrícula** | `GET /educacao/matriculas/citizen/{id}` | `[canónico]` |
| 5 | **Consultar Histórico Escolar** | `POST /educacao/historicos` | `[canónico]` |
| 6 | **Declaração Escolar** | `POST /educacao/declaracoes` | `[canónico]` |
| 7 | **Certificado Escolar** | `POST /educacao/certificados/conclusao` | `[canónico]` |
| 8 | **Segunda Via de Documento Escolar** | (novo — reutiliza certificados/declaracoes) | `[canónico]` |

---

### 2. ENSINO TÉCNICO

| # | Serviço Canónico | Endpoint Actual | Tipo |
|---|-----------------|-----------------|------|
| 9 | **Inscrição em Curso Técnico** | `POST /educacao/inscricoes/tecnico` | `[canónico]` |
| 10 | **Transferência Técnica** | `POST /educacao/transferencias/` + filtro técnico | `[canónico]` |
| 11 | **Certificação Profissional** | `POST /educacao/certificacoes/profissionais` | `[canónico]` |

---

### 3. ENSINO SUPERIOR

| # | Serviço Canónico | Endpoint Actual | Tipo |
|---|-----------------|-----------------|------|
| 12 | **Candidatura Universitária** | `POST /educacao/inscricoes/superior` | `[canónico]` |
| 13 | **Matrícula Universitária** | `POST /educacao/matriculas/universidade` | `[canónico]` |
| 14 | **Transferência Universitária** | (utiliza `POST /educacao/marketplace/transfers/request`) | `[canónico]` |
| 15 | **Mobilidade Académica** | `POST /educacao/mobilidade/academica` | `[canónico]` |
| 16 | **Reconhecimento de Diploma** | `POST /educacao/reconhecimentos/diploma` | `[canónico]` |
| 17 | **Reconhecimento de Grau** | `POST /educacao/reconhecimentos/grau` | `[canónico]` |
| 18 | **Certificado Universitário** | `POST /educacao/certificados/universitario` | `[canónico]` |

---

### 4. BOLSAS

| # | Serviço Canónico | Endpoint Actual | Tipo |
|---|-----------------|-----------------|------|
| 19 | **Candidatura a Bolsa** | `POST /educacao/bolsas/candidaturas` | `[canónico]` |
| 20 | **Renovação de Bolsa** | (novo — reutiliza workflow) | `[canónico]` |
| 21 | **Consultar Bolsa** | `GET /educacao/workflow/citizen/{id}` + filtro bolsa | `[canónico]` |

---

### 5. FORMAÇÃO E EMPREGO

| # | Serviço Canónico | Endpoint Actual | Tipo |
|---|-----------------|-----------------|------|
| 22 | **Inscrição em Formação** | `POST /educacao/formacoes/profissional` | `[canónico]` |
| 23 | **Consultar Formação** | (via marketplace/search) | `[canónico]` |
| 24 | **Estágio** | `POST /educacao/estagios/publicos` | `[canónico]` |
| 25 | **Intermediação de Emprego** | `POST /educacao/emprego/mediacoes` | `[canónico]` |

---

### 6. LEGACY / INTERNOS (não aparecem no catálogo público)

Estes endpoints existem mas são marcados como subfluxos internos, não serviços autónomos.

| Endpoint Actual | Motivo |
|----------------|--------|
| `POST /educacao/matriculas/{id}/ativar` | Subfluxo da Nova Matrícula (passo de activação) |
| `POST /educacao/inscricoes/{id}/confirmar` | Subfluxo da Inscrição |
| `POST /educacao/inscricoes/{id}/cancelar` | Subfluxo da Inscrição |
| `POST /educacao/transferencias/{id}/aprovar` | Subfluxo interno da Transferência |
| `POST /educacao/transferencias/{id}/rejeitar` | Subfluxo interno da Transferência |
| `POST /educacao/transferencias/automacao/*` | Canal interno de automação |
| `POST /educacao/transferencias/transacional` | Subfluxo ACID (chamado internamente) |
| `POST /educacao/marketplace/instant-transfer` | Subfluxo interno do marketplace |
| `GET /educacao/vacancies/` | Recurso auxiliar (não é serviço) |
| `POST /educacao/concursos/*` | Serviço administrativo (não cidadão) |
| `POST /educacao/trabalho/*` | Serviço de fiscalização (não cidadão comum) |
| `POST /educacao/avaliacoes/*` | Processo interno institucional |
| `POST /educacao/parcerias/*` | Processo interno institucional |
| `POST /educacao/acreditacoes/*` | Processo interno institucional |
| `POST /educacao/estatisticas/*` | Consulta interna (não cidadão) |
| `POST /educacao/cantinas` | Operacional (não serviço público) |
| `POST /educacao/credenciamentos` | Processo interno |
| `POST /educacao/capacitacoes/qualidade` | Processo interno |
| `POST /educacao/formacoes/gestores` | Processo interno |

---

## Catálogo Público Consolidado (26 serviços canónicos)

### Educação Básica (8)
1. Nova Matrícula Escolar
2. Renovação de Matrícula
3. Transferência Escolar
4. Consultar Matrícula
5. Consultar Histórico Escolar
6. Declaração Escolar
7. Certificado Escolar
8. Segunda Via de Documento Escolar

### Ensino Técnico (3)
9. Inscrição em Curso Técnico
10. Transferência Técnica
11. Certificação Profissional

### Ensino Superior (7)
12. Candidatura Universitária
13. Matrícula Universitária
14. Transferência Universitária
15. Mobilidade Académica
16. Reconhecimento de Diploma
17. Reconhecimento de Grau
18. Certificado Universitário

### Bolsas (3)
19. Candidatura a Bolsa
20. Renovação de Bolsa
21. Consultar Bolsa

### Formação e Emprego (4)
22. Inscrição em Formação
23. Consultar Formação
24. Estágio
25. Intermediação de Emprego

### Administrativo (1)
26. Segunda Via de Documento

---

## Plano de Migração (Etapa 2)

| Passo | Acção |
|-------|-------|
| 1 | Marcar endpoints legados com `tags=["interno"]` e `deprecated=True` |
| 2 | Adicionar `description` nos schemas indicando "Subfluxo interno — use o serviço canónico" |
| 3 | Criar rota `GET /educacao/catalogo` que retorna apenas os 26 serviços canónicos |
| 4 | UI consumir apenas `GET /educacao/catalogo` para renderizar o menu |
| 5 | Após validação, remover endpoints redundantes do router público |
