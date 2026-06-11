# Checklist da Demo — Educação (fotografia atual)

Estado gerado em: 2026-06-10

Objetivo: lista concisa de pontos a validar na demo e estado atual (VALIDADO / PENDENTE / BLOQUEADO)

- Login: PENDENTE — servidor não iniciado (ImportError: pythonjsonlogger ausente)
- Dashboard: PENDENTE
- Escola: PENDENTE — endpoints existem (`/marketplace/escolas`) mas não testados em runtime
- Aluno: PENDENTE — modelos e repositórios existem
- Matrícula: PENDENTE — POST `/matriculas` implementado (com idempotência), falta validar runtime
- Boletim: PENDENTE
- Certificado: PENDENTE
- FUC → integração de eventos: PENDENTE — hooks existem (`ServiceRequestLifecycleBridge`) mas não verificados em execução

Requisitos para transformar PENDENTE → VALIDADO (prioridade):
1. Corrigir dependências da environment (`pip install python-json-logger`).
2. Fornecer DB Postgres migrado/seeded (ou permitir executar Alembic migrations existentes) com:
   - usuários seed (Governor Huambo com `territory_id`),
   - escolas com `territory_id` para Huambo e Benguela,
   - um cidadão de teste.
3. Start backend (`uvicorn apps.backend.app.main:app --reload`) e executar os testes de fluxo (requests HTTP) listados abaixo.

Passos rápidos de verificação (após infra pronta):

1. Login: POST `/auth/token` (ou fluxo Keycloak) — obter token bearer.
2. Governor Huambo (token): GET `/marketplace/escolas?provincia=Huambo` → esperar 200.
3. Governor Huambo (token): GET `/marketplace/escolas/{escola_benguela_id}` → esperar 403.
4. Criar matrícula: POST `/matriculas` com body `MatriculaCreate` — verificar 201 e que `request_service` gerou um education request.
5. Reservar vaga: POST `/marketplace/reservar` → verificar 201/200. Confirmar/reservar/confirmar/cancelar com usuários apropriados.
6. Verificar FUC: confirmar que `ServiceRequestLifecycleBridge` gerou entrada de request / event (DB table / external broker).

