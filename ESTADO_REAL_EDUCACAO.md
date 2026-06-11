# ESTADO_REAL_EDUCACAO — Fotografia atual

Data: 2026-06-10

Resumo rápido
- Bootstrap: `AGENT_RULES.md` carregado e seguido.
- Código: foram adicionados `territory_id`, `created_by`, `managed_by` em 6 modelos do módulo `educacao` (código ORM apenas). Também adicionei chamadas a `verify_territorial_access` em vários endpoints públicos/admin quando foi possível resolver a entidade/instituição.
- Import/Startup/Tests: Execução parcial falhou (ver seção Evidência).

**1) Matriz CRUD (estado atual — código / endpoints / persistência)**

Entidade | Criar | Editar | Consultar | Remover | Nota (Demo)
---|---:|---:|---:|---:|---
Escola | Parcial (search, get, repo.save) | Parcial (repo.save via admin flows) | Sim (`/marketplace/escolas`, `/marketplace/escolas/{id}`) | Parcial/Não exposto publicamente | Model: `apps/backend/app/modules/educacao/infrastructure/models/escola_model.py`
Aluno (AcademicIdentity) | Parcial (repositorio existe) | Parcial | Sim (APIs EMIS / internal) | Não exposto | Model: `apps/backend/app/modules/educacao/infrastructure/models/academic_identity_model.py`
Matrícula | Sim (POST `/matriculas`) | Sim (ativar `/matriculas/{id}/ativar`) | Sim (`/matriculas/citizen/{id}`) | Não (soft flows via state transitions) | Model: `apps/backend/app/modules/educacao/infrastructure/models/matricula_model.py`
Professor | Não existe modelo dedicado no módulo `educacao` | — | — | — | Política `gerir_professores` existe em `rbac/policies.py` mas sem modelo correspondente
Turma | Parcial (persistência via repo) | Parcial | Sim (via repos) | Não exposto | Model: `apps/backend/app/modules/educacao/infrastructure/models/turma_model.py`
Boletim | Parcial | Parcial | Sim (repos) | Não | Model: `apps/backend/app/modules/educacao/infrastructure/models/boletim_model.py`
Certificado | Parcial (issuance workflows exist) | Parcial | Sim | Não | Model: `apps/backend/app/modules/educacao/infrastructure/models/certificado_model.py`

Observações:
- "Parcial" indica que a API/repositório existe no código, mas algumas operações são administradas via workflows internos ou não expostas publicamente.
- Muitos modelos não tinham `territory_id`, `created_by`, `managed_by` originalmente — **agora** estão presentes no ORM, porém a persistência precisa ser atualizada para popular esses campos em runtime.

**2) Endpoints que escrevem/alteram e verificação territorial**
- Antes: lista de endpoints públicos sem verificação territorial identificada (ex.: `POST /matriculas`, `POST /marketplace/reservar`, `/reservas/confirmar`, `/reservas/cancelar`, transfers, admissions, booking, EMIS sync).
- Ações tomadas (código): acrescentei chamadas a `verify_territorial_access` em arquivos:
  - `apps/backend/app/modules/educacao/api/endpoints/matricula_routes.py`
  - `apps/backend/app/modules/educacao/api/endpoints/marketplace_endpoints.py`
  - `apps/backend/app/modules/educacao/marketplace/booking/api/router.py`
  - `apps/backend/app/modules/educacao/marketplace/admissions/api/router.py`
  - `apps/backend/app/modules/educacao/marketplace/transfers/api/router.py`
  - `apps/backend/app/modules/educacao/emis/api/endpoints.py`
- Limitação: em fluxos onde o request contém `opportunity_id` ou `booking_id` sem `institution_id`, a resolução para `Escola` é "best-effort" (tenta converter UUID → `Escola`). Onde não encontrado, `verify_territorial_access` recebe `resource_territory_id=None` (sem restrição). Recomendo normalizar para enviar `institution_id`/`territory_id` nesses fluxos.

**3) Territorialidade — evidência de execução (tentativa)**
- Ação: executei testes unitários e tentativa de import do app para validar runtime.
- Resultado:
  - `Import`: FALHOU — erro: ModuleNotFoundError: No module named 'pythonjsonlogger' ao importar `apps.backend.app.main`.
  - `Tests (pytest)`: FALHOU — erro: tabela `educacao_institution_capacities` não existe (UndefinedTableError) ao rodar testes que esperam schema criado.

Trechos relevantes (resumo):
- Import error:
  - File: `apps/backend/app/main.py` imports `apps.backend.app.modules.educacao.foundation.observability.logging` which requires `pythonjsonlogger` package not installed in environment.
- Tests error:
  - `asyncpg.exceptions.UndefinedTableError: relation "educacao_institution_capacities" does not exist` — tests expect DB fixtures/migrations applied.

Implicação: não foi possível executar validações runtime end-to-end (HTTP) nem obter OpenAPI do servidor rodando, porque a aplicação não importa cleanly and the test DB schema is not prepared.

**4) RBAC runtime checks**
- Diretiva: validar cenários como "Director Escola não consegue criar município" — requires running server with seeded users/roles and DB schema. Não possível devido aos bloqueios acima.

**5) FUC (eventos) — investigação estática**
- Código: serviços de `matricula`, `certificado`, `boletim`, `transferencia` chamam `ServiceRequestLifecycleBridge` e outras integrações (e.g. `request_service.create_education_request`, `mark_education_request_completed`). Há hooks para criar requests/integrações.
- Observação prática: não foi possível confirmar envio real de eventos ao FUC (message-broker/queue) em runtime porque a aplicação não executou com DB/infra.
- Conclusão: FUC — `PENDENTE` (não verificado em runtime). Alguns pontos do código indicam integração, mas sem execução não confirmamos.

**6) Bloqueadores principais (para demo / validação runtime)**
- Dependência ausente: `pythonjsonlogger` — impede import do app (`ImportError`). Instalar via `pip install python-json-logger`.
- Schema ausente no DB de testes/ambiente — testes falham por `UndefinedTableError`. É necessário executar migrações ou providenciar DB de teste com schema. (Você especificou: não gerar migrations; portanto, providenciar um DB já migrado/seeded é a opção.)
- Dados seed/usuários/territórios: necessários para validar territorialidade (ex.: Governor Huambo user with territory_id pointing to Huambo). Precisam existir no DB ou serem criados por seed scripts (não aplicar backfill aqui).

**7) Checklist Demo (estados — VALIDADO / PENDENTE / BLOQUEADO)**
- Login: PENDENTE (não foi possível iniciar servidor)
- Dashboard: PENDENTE
- Escola (search/get): PENDENTE (APIs existem no código, mas server não rodou)
- Aluno: PENDENTE
- Matrícula (criar/ativar): PENDENTE
- Boletim: PENDENTE
- Certificado: PENDENTE
- FUC integration: PENDENTE

**8) Recomendação mínima para permitir validações runtime (não inclui migrações ou backfills automáticos, apenas passos operacionais)**
1. Instalar dependências ausentes na environment (ex.: `python-json-logger`).
2. Fornecer um banco Postgres de desenvolvimento com o schema já migrado (prod-like or dev DB). Alternativa: run Alembic migrations manually in a controlled environment (you said: do not generate migrations; running existing Alembic migrations to create schema is acceptable if you permit).
3. Seed minimal users: Governor Huambo (user with territory_id pointing to Huambo), at least two schools with territory ids (Huambo, Benguela) and one test citizen.
4. Start the backend (uvicorn) and call the endpoints to capture HTTP evidence.

---

Se confirma que quer que eu:
- instale `python-json-logger` na environment e/ou
- tente iniciar o servidor apontando para um DB já migrado que você disponibilize (fornecendo `DATABASE_URL`),
posso proceder e tentar validar os pontos runtime (territorialidade, RBAC, FUC) e gerar screenshots/requests de evidência.

Arquivo gerado por automação: `ESTADO_REAL_EDUCACAO.md` (nesta pasta raiz do repositório).

