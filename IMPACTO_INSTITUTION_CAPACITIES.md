# IMPACTO: tabela `educacao_institution_capacities`

Data: 2026-06-10

**Resumo executivo**
- A tabela `educacao_institution_capacities` é a persistência canônica para "gestão de vagas" (capacity per institution/grade/shift).
- Uso direto: repositório/adapter de capacity + motores transacionais e adapters de marketplace.
- Consequência para demo: BLOQUEIO. Pelo critério indicado, como a tabela impacta gestão de vagas / transferências transacionais, isso bloqueia a demo (Classificação global: **A — BLOQUEIA DEMO**).
- Nota: o endpoint de criação de matrícula (`/matriculas`) usa `turma.capacidade` via `turma_repo` e **não** referencia diretamente esta tabela; porém transferências e reservas no marketplace dependem fortemente dela.

**Mapeamento de ocorrências (usos diretos)**

1) Modelo (definição da tabela)
- Arquivo: [apps/backend/app/modules/educacao/infrastructure/models/institution_capacity_model.py](apps/backend/app/modules/educacao/infrastructure/models/institution_capacity_model.py)
- Função / símbolo: `InstitutionCapacityModel` (classe, `__tablename__ = "educacao_institution_capacities"`)
- Endpoint(s) afetado(s): indireto — qualquer endpoint que use o repositório/adapters de capacity (listados abaixo)
- Fluxo de negócio afetado: Gestão de vagas (capacidade por instituição/ano/classe/turno)
- Crítico para demo?: SIM
- Classificação: A

2) Repositório — acesso e operações (CRUD + reserva/lock)
- Arquivo: [apps/backend/app/modules/educacao/infrastructure/repositories/sqlalchemy_capacity_repository.py](apps/backend/app/modules/educacao/infrastructure/repositories/sqlalchemy_capacity_repository.py)
- Funções: `save`, `get_by_id`, `get_by_institution_grade_shift`, `list_capacities`, `reserve_capacity`, `release_capacity`, `get_available`, `update_capacity_used`
- Endpoint(s) afetado(s): `/transferencias/transacional` (via TransferTransactionService), `/marketplace/instant-transfer` (quando usar RealReservationAdapter/RealTransferAdapter), fluxos de reserva/booking
- Fluxo de negócio afetado: Reserva de vagas, liberação de reservas, cálculo de vagas disponíveis, atualização de uso (capacity_used)
- Crítico para demo?: SIM
- Classificação: A

3) Adapter transacional (ponte para o repositório)
- Arquivo: [apps/backend/app/foundation/transactional/adapters/sqlalchemy_capacity_adapter.py](apps/backend/app/foundation/transactional/adapters/sqlalchemy_capacity_adapter.py)
- Funções: `reserve`, `release`, `get_available` (delegam para o repositório)
- Endpoint(s) afetado(s): usado pelo `TransferTransactionalEngine` e, por consequência, por adaptadores de transferência (marketplace)
- Fluxo de negócio afetado: Orquestração transacional de reserva + transferência
- Crítico para demo?: SIM
- Classificação: A

4) Motor transacional (porta de execução de transferências)
- Arquivo: [apps/backend/app/foundation/transactional/core.py](apps/backend/app/foundation/transactional/core.py)
- Função: `TransferTransactionalEngine.execute_transfer` (chama `capacity.reserve`)
- Endpoint(s) afetado(s): `POST /marketplace/instant-transfer` (quando via RealTransferAdapter), `POST /transferencias/transacional`
- Fluxo de negócio afetado: Execução atômica de transferência (reservar capacidade → transitar matrícula → emitir eventos)
- Crítico para demo?: SIM
- Classificação: A

5) Serviço de transferência transacional (aplicação)
- Arquivo: [apps/backend/app/modules/educacao/application/transfer_transaction_service.py](apps/backend/app/modules/educacao/application/transfer_transaction_service.py)
- Função: `execute_transfer` (chama `capacity_repo.reserve_capacity` dentro do fluxo)
- Endpoint(s) afetado(s): [apps/backend/app/modules/educacao/api/endpoints/transferencias.py](apps/backend/app/modules/educacao/api/endpoints/transferencias.py) → `POST /transferencias/transacional`; também exposto via marketplace instant-transfer (`apps/backend/app/modules/educacao/marketplace/router.py`)
- Fluxo de negócio afetado: Transferência estudantil atômica (reservar vaga na instituição destino)
- Crítico para demo?: SIM
- Classificação: A

6) Adapters de Marketplace (reserva/transferência)
- Arquivo: [apps/backend/app/modules/marketplace/application/adapters.py](apps/backend/app/modules/marketplace/application/adapters.py)
- Funções/classes: `RealReservationAdapter.reserve` (faz `SELECT ... FROM InstitutionCapacityModel ... WITH FOR UPDATE`), `RealTransferAdapter.execute` (invoca `TransferTransactionalEngine`)
- Endpoint(s) afetado(s): [apps/backend/app/modules/marketplace/api/router.py](apps/backend/app/modules/marketplace/api/router.py) → `POST /marketplace/instant-transfer` (via default orchestrator)
- Fluxo de negócio afetado: Matching → Reserva de vaga → Transferência/inscrição via Marketplace
- Crítico para demo?: NÃO (somente se demo for *apenas* marketplace; se demo incluir transferências transacionais, então é crítico)
- Classificação: C

7) Orquestrador Marketplace (entrada e wiring de adapters)
- Arquivo: [apps/backend/app/modules/marketplace/api/router.py](apps/backend/app/modules/marketplace/api/router.py)
- Função/endpoint: `post_instant_transfer` (POST `/marketplace/instant-transfer`) e `get_default_orchestrator` (wiring que injeta `RealReservationAdapter` / `RealTransferAdapter`)
- Fluxo de negócio afetado: Orquestração instant-transfer (matching, reserva, pagamento, transferência, notificação)
- Crítico para demo?: NÃO (se demo for apenas cadastro/matrícula), caso contrário SIM
- Classificação: C

8) Router Educacao — Marketplace (usa TransferTransactionService)
- Arquivo: [apps/backend/app/modules/educacao/marketplace/router.py](apps/backend/app/modules/educacao/marketplace/router.py)
- Função/endpoint: `instant_transfer` (POST `/marketplace/instant-transfer` dentro do submódulo `educacao`) — chama `TransferTransactionService.execute_transfer`
- Fluxo de negócio afetado: mesma lógica transacional de transferências via marketplace
- Crítico para demo?: SIM
- Classificação: A

9) Dependency wiring (constrói service com capacity_repo)
- Arquivo: [apps/backend/app/modules/educacao/api/deps.py](apps/backend/app/modules/educacao/api/deps.py)
- Função: `get_transfer_transaction_service` (injeta `SQLAlchemyCapacityRepository(session)` no `TransferTransactionService`)
- Endpoint(s) afetado(s): endpoints que dependem deste get (por ex. `/transferencias/transacional`, `/marketplace/instant-transfer` do submódulo `educacao`)
- Fluxo de negócio afetado: injecção de dependência para transferências/reservas
- Crítico para demo?: SIM
- Classificação: A

10) Uso em serviços de matrícula transacional (não exposto diretamente nos endpoints principais)
- Arquivo: [apps/backend/app/modules/educacao/application/enrollment_transaction_service.py](apps/backend/app/modules/educacao/application/enrollment_transaction_service.py)
- Função: `enroll_student_with_lock` (usa `capacity_repo.reserve_capacity` para matrícula atômica)
- Endpoint(s) afetado(s): *nenhuma* rota pública atualmente depende diretamente deste serviço (é um serviço de aplicação reutilizável)
- Fluxo de negócio afetado: matrícula segura com lock pessimista (future-proof)
- Crítico para demo?: NÃO (funcionalidade de futuro / não diretamente exposta)
- Classificação: D

**Ocorrências em testes / código auxiliar**
- `apps/backend/app/foundation/transactional/tests/test_sqlalchemy_capacity_adapter.py` (tests) — Classificação: D
- `apps/backend/app/modules/educacao/foundation/transactional/tests/test_transfer_engine_integration.py` — Classificação: D

**Observações adicionais e conclusão**
- A tabela é parte central da *gestão de vagas* e é utilizada por repositórios/adapters que suportam reserva atômica e transferências. Mesmo que o endpoint `POST /matriculas` utilize atualmente `turma_repo` (campo `turma.capacidade`), fluxos relevantes para demo (transferências transacionais e reservas do marketplace) dependem de `educacao_institution_capacities`.
- Pela regra fornecida: por afetar `gestão de vagas`/transferências, a ausência desta tabela deve ser tratada como bloqueio imediato para a demo (Classificação global: **A**).

**Próximo passo sugerido (sem alterações de código)**
- Gerar DDL de criação da tabela e um plano de migração (apenas documentação) para revisão — eu posso produzir o DDL e instruções, sem criar migrações nem aplicar nada, se desejar.

---
Relatório gerado automaticamente pelo diagnóstico read-only solicitado. Se quiser, eu gero o DDL de criação da tabela e checklist de passos para aplicação segura (sem aplicar nada).# IMPACTO: `educacao_institution_capacities`

Data: 2026-06-10

Resumo executivo
- A tabela referenciada por `InstitutionCapacityModel` é utilizada por componentes de *capacity reservation* (reserva/liberação/consulta) que suportam: transferências transacionais e o Marketplace (reservas + instant-transfer).
- Entradas principais: TransferTransactionService, SQLAlchemyCapacityRepository, RealReservationAdapter/RealTransferAdapter, e TransferTransactionalEngine.
- Consequência prática: a ausência da tabela no banco (migração inexistente) causa falha imediata nas rotas de *transferência transacional* e no *instant-transfer* do Marketplace. Portanto o problema BLOQUEIA a demo caso a demo inclua transfers/marketplace.

Ocorrências mapeadas (arquivo → função → endpoint afetado → fluxo de negócio → crítico?)

1) File: [apps/backend/app/modules/educacao/infrastructure/repositories/sqlalchemy_capacity_repository.py](apps/backend/app/modules/educacao/infrastructure/repositories/sqlalchemy_capacity_repository.py#L1-L200)
- Function: `class SQLAlchemyCapacityRepository` (methods: `reserve_capacity`, `release_capacity`, `get_available`, `update_capacity_used`, `get_by_institution_grade_shift`, `save`, ...)
- Endpoint(s) afetado(s): Indiretamente por `/transferencias/transacional` and `/marketplace/instant-transfer` (veja pontos 6 e 7 abaixo)
- Fluxo de negócio afetado: Gestão de vagas (reserva/liberação), reservas do Marketplace, suporte a transferência e finalização de matrícula (quando usada em transações)
- Crítico para demo?: SIM
- Classificação: A) BLOQUEIA DEMO

2) File: [apps/backend/app/modules/educacao/application/transfer_transaction_service.py](apps/backend/app/modules/educacao/application/transfer_transaction_service.py#L1-L260)
- Function: `TransferTransactionService.execute_transfer`
- Endpoint(s) afetado(s): `/transferencias/transacional` ([apps/backend/app/modules/educacao/api/endpoints/transferencias.py](apps/backend/app/modules/educacao/api/endpoints/transferencias.py#L1-L120)) e `/marketplace/instant-transfer` (via orchestrator/adapters)
- Fluxo de negócio afetado: Transferências (lock de vaga, reservar capacidade, encerrar matrícula anterior, criar nova matrícula, audit/outbox)
- Crítico para demo?: SIM
- Classificação: A) BLOQUEIA DEMO

3) File: [apps/backend/app/modules/marketplace/application/adapters.py](apps/backend/app/modules/marketplace/application/adapters.py#L1-L220)
- Function: `class RealReservationAdapter.reserve` / `class RealReservationAdapter.release` e `RealTransferAdapter.execute` (usa `TransferTransactionalEngine`)
- Endpoint(s) afetado(s): `/marketplace/instant-transfer` (default orchestrator constrói `RealReservationAdapter` / `RealTransferAdapter`) — [apps/backend/app/modules/marketplace/api/router.py](apps/backend/app/modules/marketplace/api/router.py#L1-L260)
- Fluxo de negócio afetado: Reserva de vagas no Marketplace, liberação, e execução do fluxo de transferência/enrollment via engine
- Crítico para demo?: SIM (se demo inclui Marketplace/instant-transfer)
- Classificação: C) BLOQUEIA APENAS MARKETPLACE (nota: se a demo de Marketplace executar também a etapa que cria matrícula via engine, então ele também passa a BLOQUEAR DEMO — ver ponto 2)

4) File: [apps/backend/app/foundation/transactional/adapters/sqlalchemy_capacity_adapter.py](apps/backend/app/foundation/transactional/adapters/sqlalchemy_capacity_adapter.py#L1-L140)
- Function: `SQLAlchemyCapacityReservationAdapter.reserve/release/get_available` (delegam para `SQLAlchemyCapacityRepository`)
- Endpoint(s) afetado(s): usadas pelo `TransferTransactionalEngine` / RealTransferAdapter → impacta `/marketplace/instant-transfer` e `/transferencias/transacional`
- Fluxo de negócio afetado: camada transacional de reserva de capacidade (porta entre engine e repository)
- Crítico para demo?: SIM
- Classificação: A) BLOQUEIA DEMO

5) File: [apps/backend/app/foundation/transactional/core.py](apps/backend/app/foundation/transactional/core.py#L1-L120)
- Function: `TransferTransactionalEngine.execute_transfer` (orquestra: reserva de capacidade → transição de enrollment → recibo)
- Endpoint(s) afetado(s): invocado por `RealTransferAdapter` usado no orchestrator do Marketplace e por fluxos transacionais de transferência
- Fluxo de negócio afetado: Orquestração transacional de transferências (inclui reserva de vaga)
- Crítico para demo?: SIM
- Classificação: A) BLOQUEIA DEMO

6) File: [apps/backend/app/modules/marketplace/api/router.py](apps/backend/app/modules/marketplace/api/router.py#L1-L260)
- Function / Endpoint: `POST /marketplace/instant-transfer` (function `post_instant_transfer`)
- Como usa a tabela: o *default orchestrator* constrói `RealReservationAdapter` e `RealTransferAdapter` que consultam/atualizam `InstitutionCapacityModel` via repository
- Fluxo de negócio afetado: Instant transfer orchestration (matching → reserva → pagamento → transferência/matrícula)
- Crítico para demo?: SIM (se demo inclui instant-transfer)
- Classificação: A) BLOQUEIA DEMO

7) File: [apps/backend/app/modules/educacao/api/endpoints/transferencias.py](apps/backend/app/modules/educacao/api/endpoints/transferencias.py#L1-L160)
- Function / Endpoint: `POST /transferencias/transacional` (`executar_transferencia_transacional`)
- Como usa a tabela: depende de `get_transfer_transaction_service` que injeta `SQLAlchemyCapacityRepository` (reservas são feitas dentro de `TransferTransactionService`)
- Fluxo de negócio afetado: Transferência transacional (reserva de vaga + nova matrícula)
- Crítico para demo?: SIM
- Classificação: A) BLOQUEIA DEMO

8) File: [apps/backend/app/modules/educacao/application/enrollment_transaction_service.py](apps/backend/app/modules/educacao/application/enrollment_transaction_service.py#L1-L220)
- Function: `EnrollmentTransactionService.enroll_student_with_lock` and helpers (`reserve_capacity` usage)
- Endpoint(s) afetado(s): nenhum endpoint público direto identificado que injete este service (nenhuma dependência pública encontrada). Usado como componente de aplicação
- Fluxo de negócio afetado: matriculas atômicas com lock (alternativa segura ao fluxo `MatriculaService`)
- Crítico para demo?: NÃO (conforme análise atual, `MatriculaService` usado por endpoints não depende desta tabela); classificação para funcionalidades futuras
- Classificação: D) BLOQUEIA APENAS FUNCIONALIDADES FUTURAS

9) Arquivos de teste e infra auxiliar (referências, não endpoints):
- `apps/backend/app/foundation/transactional/tests/test_sqlalchemy_capacity_adapter.py` (testes do adapter)
- `apps/backend/app/foundation/transactional/tests/test_capacity_adapter.py`
- `apps/backend/app/modules/educacao/tests/...` (mocks/fixtures)
- Impacto: apenas testes e validação; não diretamente crítico para a demo em produção
- Classificação: B) NÃO BLOQUEIA DEMO

---

Conclusão operacional (diagnóstico, sem alterações)
- Escopo: a tabela é central para reservas e transferências do Marketplace; a sua ausência causa erros imediatos nas rotas de transferências e no instant-transfer.
- Decisão de bloqueio: como `TransferTransactionService` e os endpoints `/transferencias/transacional` e `/marketplace/instant-transfer` dependem dela, **considero isto um bloqueio imediato para a demo** se a demo incluir transfers/marketplace (Classificação global: A).
- Se a sua demo for apenas leitura ou focada em `criar_matricula` via `MatriculaService` (que usa `turma.capacidade`), então o impacto é menor e a questão pode ser estacionada (apenas Marketplace afetado).

Próxima ação recomendada (apenas diagnóstico)
- Confirmar se a demo planeada inclui `/marketplace/instant-transfer` ou `/transferencias/transacional`.
- Se sim: o impedimento técnico real é a falta da tabela no BD. Será necessário (fora deste diagnóstico) criar/aplicar migração ou criar manualmente a tabela no BD de demo.

Ficheiro gerado automaticamente pelo assistente: `IMPACTO_INSTITUTION_CAPACITIES.md`
