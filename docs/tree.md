/home/user/sila-system/apps/backend/app/modules:
administracao-local
agricultura
aguas-saneamento
ambiente
api
apoio-empresarial
arquivo-nacional
assistencia-social
audit
aviacao-civil
ciencia-pesquisa
civil_protection
comercio
comercio-externo
compliance
conftest.py
cooperacao-internacional
cultura
defesa-consumidor
desporto
documents
economy
educacao
emprego
energia
energy
estatistica
familia
financas-impostos
florestas
gestao-fundiaria
governance
habitacao
identity
igualdade
industria
industry
infrastructure
infrastructure_sector
__init__.py
integracao-nacional
intelligence
justica
justice
juventude
logistics
marketplace
meteorologia
migracao
migration_service
notifications
obras-publicas
operations
patrimonio-cultural
payment
pecuaria
pescas
pescas-industriais
petroleo-gas
planeamento
portos-logistica
procurement
protecao-civil
protecao-dados
public_security
recursos-minerais
registo-civil
resources
saude
_scaffold
seguranca-alimentar
seguranca-publica
seguranca-social
society
tecnologia-inovacao
telecomunicacoes
tests
tourism
trabalho-inspecao
transportes
turismo
urbanismo
wallet
xroad

/home/user/sila-system/apps/backend/app/modules/administracao-local:
api
application
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/administracao-local/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/administracao-local/application:
event_handlers.py

/home/user/sila-system/apps/backend/app/modules/administracao-local/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/agricultura:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/agricultura/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/agricultura/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/aguas-saneamento:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/aguas-saneamento/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/aguas-saneamento/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/ambiente:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/ambiente/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/ambiente/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/api:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
router.py
tests

/home/user/sila-system/apps/backend/app/modules/api/api:
health.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/api/application:
commands.py
event_handlers.py

/home/user/sila-system/apps/backend/app/modules/api/domain:
enums
events
models.py
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/api/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/api/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/api/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/api/infrastructure:
adapters.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/api/tests:
conftest.py
fixtures
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/api/tests/fixtures:
__init__.py

/home/user/sila-system/apps/backend/app/modules/api/tests/integration:
__init__.py
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/api/tests/unit:
__init__.py
test_domain.py

/home/user/sila-system/apps/backend/app/modules/apoio-empresarial:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/apoio-empresarial/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/apoio-empresarial/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/arquivo-nacional:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/arquivo-nacional/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/arquivo-nacional/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/assistencia-social:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/assistencia-social/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/assistencia-social/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/audit:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
state_audit
tests

/home/user/sila-system/apps/backend/app/modules/audit/api:
endpoints
health.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/audit/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/application:
commands
commands.py
dto
event_handlers.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/audit/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain:
entities
enums
events
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/audit/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/infrastructure:
adapters
adapters.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/audit/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit:
api
application
domain
health.py
infrastructure
__init__.py
module.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/application:
commands
dto
__init__.py
queries
services

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/application/commands:
__init__.py
open_audit_case.py
register_event.py
resolve_audit_case.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/application/dto:
audit_event_dto.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/application/services:
audit_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/domain:
entities
__init__.py
repositories
services
value_objects

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/domain/entities:
audit_alert.py
audit_case.py
audit_log.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/domain/repositories:
audit_case_repository.py
audit_log_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/domain/services:
audit_engine.py
compliance_rules.py
fraud_detection.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/domain/value_objects:
audit_event_type.py
audit_severity.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/infrastructure:
__init__.py
orm
repositories

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/infrastructure/orm:
audit_case_model.py
audit_log_model.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/infrastructure/repositories:
audit_case_repository_impl.py
audit_log_repository_impl.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/state_audit/tests:
__init__.py
test_state_audit_flow.py

/home/user/sila-system/apps/backend/app/modules/audit/tests:
conftest.py
fixtures
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/audit/tests/fixtures:
__init__.py

/home/user/sila-system/apps/backend/app/modules/audit/tests/integration:
__init__.py
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/audit/tests/unit:
__init__.py
test_domain.py

/home/user/sila-system/apps/backend/app/modules/aviacao-civil:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/aviacao-civil/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/aviacao-civil/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/ciencia-pesquisa:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/ciencia-pesquisa/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/ciencia-pesquisa/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/civil_protection:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/civil_protection/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/api/endpoints:
atendimentos.py
bombeiros.py
corporacoes.py
despachos.py
__init__.py
ocorrencias_emergenciais.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/civil_protection/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/application/dto:
atendimento_schema.py
bombeiro_schema.py
corporacao_schema.py
despacho_schema.py
__init__.py
ocorrencia_emergencial_schema.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/application/services:
atendimento_service.py
bombeiro_service.py
corporacao_service.py
despacho_service.py
__init__.py
ocorrencia_emergencial_service.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain:
entities.py
enums
enums.py
events
__init__.py
models
models.py
ports
repositories
repositories.py
services

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain/models:
atendimento.py
bombeiro.py
corporacao.py
despacho.py
__init__.py
ocorrencia_emergencial.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain/ports:
atendimento_repository_port.py
bombeiro_repository_port.py
corporacao_repository_port.py
despacho_repository_port.py
__init__.py
ocorrencia_emergencial_repository_port.py
request_service_port.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/infrastructure/adapters:
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/infrastructure/orm:
atendimento_model.py
bombeiro_model.py
corporacao_model.py
despacho_model.py
__init__.py
ocorrencia_emergencial_model.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/infrastructure/repositories:
__init__.py
sqlalchemy_atendimento_repository.py
sqlalchemy_bombeiro_repository.py
sqlalchemy_corporacao_repository.py
sqlalchemy_despacho_repository.py
sqlalchemy_ocorrencia_emergencial_repository.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests:
api
application
conftest.py
domain
_fakes.py
infrastructure
__init__.py
integration
test_atendimentos.py
test_bombeiros.py
test_corporacoes.py
test_despachos.py
test_ocorrencias_emergenciais.py
test_orm_integration_real.py
unit

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/civil_protection/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/comercio:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/comercio/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/comercio/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/comercio-externo:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/comercio-externo/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/comercio-externo/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/compliance:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/compliance/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/compliance/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
service.py
services

/home/user/sila-system/apps/backend/app/modules/compliance/application/commands:
command_handlers.py
compliance_commands.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/application/queries:
compliance_queries.py
__init__.py
query_handlers.py

/home/user/sila-system/apps/backend/app/modules/compliance/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain:
entities
entities.py
enums
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/compliance/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/models:
compliance_check.py
enums.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/ports:
aggregate_repository_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/infrastructure:
adapters.py
__init__.py
orm
repositories
repositories.py
repository.py

/home/user/sila-system/apps/backend/app/modules/compliance/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/compliance/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/compliance/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/compliance/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/compliance/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/cooperacao-internacional:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/cooperacao-internacional/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/cooperacao-internacional/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/cultura:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/cultura/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/cultura/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/defesa-consumidor:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/defesa-consumidor/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/defesa-consumidor/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/desporto:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/desporto/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/desporto/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/documents:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/documents/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/documents/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/application:
commands
commands.py
documents.py
dto
event_handlers.py
__init__.py
ports
queries
schemas
services

/home/user/sila-system/apps/backend/app/modules/documents/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/application/schemas:
documents.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/application/services:
document_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain:
entities
enums
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/documents/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/documents/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/documents/tests:
conftest.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/documents/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/documents/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/economy:
api
apoio_empresarial
application
ARCHITECTURE.md
core
domain
financas
industria
infrastructure
__init__.py
module.yaml
public_budget
taxpayer
tests
trade

/home/user/sila-system/apps/backend/app/modules/economy/api:
application
domain
health.py
infrastructure
__init__.py
router.py
routers.py
transactions.py

/home/user/sila-system/apps/backend/app/modules/economy/api/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/api/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/api/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/apoio_empresarial:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/economy/apoio_empresarial/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/economy/apoio_empresarial/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/economy/apoio_empresarial/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/apoio_empresarial/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/economy/apoio_empresarial/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/application:
application
commands
commands.py
domain
dto
event_handlers.py
infrastructure
__init__.py
ports
queries

/home/user/sila-system/apps/backend/app/modules/economy/application/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/application/commands:
command_handlers.py
economy_commands.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/application/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/application/dto:
__init__.py
invoice_schema.py
payment_schema.py

/home/user/sila-system/apps/backend/app/modules/economy/application/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/application/queries:
economy_queries.py
__init__.py
query_handlers.py

/home/user/sila-system/apps/backend/app/modules/economy/core:
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/economy/core/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/economy/core/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/core/application/services:
acordo_comercial_service.py
ademe_service.py
admissao_temporaria_service.py
advance_payment_bond_service.py
aeroporto_alfandegado_service.py
agente_carga_service.py
airwaybill_service.py
aladi_service.py
analise_risco_service.py
aperfeicoamento_ativo_service.py
aperfeicoamento_passivo_service.py
apreensao_service.py
arbitragem_cambio_service.py
armazem_alfandegado_service.py
armazenagem_alfandegada_service.py
armazenagem_service.py
assinatura_digital_aduaneira_service.py
assistencia_social_service_port.py
auto_infracao_aduaneiro_service.py
autorizacao_exportacao_service.py
autorizacao_importacao_service.py
awb_service.py
balanca_comercial_service.py
balanco_pagamentos_service.py
baldeacao_service.py
bank_guarantee_service.py
bid_bond_service.py
bill_of_lading_service.py
bloco_economico_service.py
bl_service.py
canal_amarelo_service.py
canal_cinza_service.py
canal_parametrizacao_service.py
canal_verde_service.py
canal_vermelho_service.py
cancelamento_radar_service.py
capatazia_service.py
carta_credito_service.py
certificado_analise_service.py
certificado_digital_aduaneiro_service.py
certificado_fitossanitario_service.py
certificado_fumigacao_service.py
certificado_origem_service.py
certificado_qualidade_service.py
certificado_zoossanitario_service.py
cfr_service.py
cif_service.py
cip_service.py
citizen_service_port.py
cobertura_cambial_service.py
cobranca_documentaria_service.py
cobranca_service.py
cofins_importacao_service.py
comercio_externo_service_port.py
comercio_service_port.py
commercial_invoice_service.py
conferencia_aduaneira_service.py
conferencia_documental_service.py
conferencia_fisica_service.py
conhecimento_embarque_service.py
contrato_cambio_exportacao_service.py
contrato_cambio_importacao_service.py
contrato_cambio_service.py
contrato_exportacao_service.py
contrato_importacao_service.py
conversao_moeda_service.py
cotacao_cambio_service.py
cpt_service.py
credito_documentario_service.py
dap_service.py
ddp_service.py
declaracao_aduaneira_service.py
declaracao_exportacao_service.py
declaracao_importacao_service.py
declaracao_unica_service.py
defesa_aduaneira_service.py
defesa_consumidor_service_port.py
deposito_alfandegado_service.py
deposito_especial_service.py
deposito_industrial_service.py
deposito_sob_controle_service.py
desembaraco_service.py
de_service.py
despachante_service.py
despacho_aduaneiro_service.py
despacho_exportacao_service.py
despacho_importacao_service.py
destino_produto_service.py
di_service.py
dpd_service.py
dpu_service.py
drawback_externo_service.py
drawback_integrado_service.py
drawback_interno_service.py
drawback_isencao_service.py
drawback_restituicao_service.py
drawback_service.py
drawback_substituicao_service.py
drawback_suspensao_service.py
drawback_verde_amarelo_service.py
du_service.py
educacao_service_port.py
emprego_service_port.py
entreposto_aduaneiro_service.py
estabelecimento_comercial_service.py
estacao_aduaneira_service.py
estatistica_exportacao_service.py
estatistica_importacao_service.py
exportacao_temporaria_service.py
exportador_service.py
exw_service.py
fas_service.py
fatura_comercial_service.py
fatura_proforma_service.py
fca_service.py
fechamento_cambio_service.py
financas_impostos_service_port.py
financas_service_port.py
fiscalizacao_aduaneira_service.py
fluxo_cambial_service.py
fob_service.py
futuro_cambio_service.py
garantia_internacional_service.py
geosampa_service_port.py
habilitacao_exportador_service.py
habilitacao_importador_service.py
habilitacao_radar_service.py
habilitacao_service_base.py
hedge_cambial_service.py
house_bill_service.py
hs_code_service.py
icms_exportacao_service.py
icms_importacao_service.py
identidade_service_port.py
ie_service.py
ii_service.py
importador_service.py
imposto_exportacao_service.py
imposto_importacao_service.py
impugnacao_lancamento_service.py
incoterm_service.py
industrializacao_externo_service.py
industrializacao_terceiros_service.py
industria_service_port.py
__init__.py
invoice_service.py
ipi_vinculado_service.py
iss_importacao_service.py
julgamento_administrativo_service.py
juventude_service_port.py
lc_service.py
liberacao_service.py
licenca_exportacao_service.py
licenca_importacao_service.py
li_exportacao_service.py
li_importacao_service.py
liquidacao_cambio_service.py
manifesto_carga_service.py
marinha_mercantil_service.py
master_bill_service.py
mercosul_service.py
movimentacao_carga_service.py
multa_aduaneira_service.py
nacionalizacao_service.py
ncm_service.py
opcao_cambial_service.py
operacao_cambio_service.py
operador_logistico_service_base.py
origem_produto_service.py
packing_list_service.py
pagamento_internacional_service.py
pais_destino_service.py
pais_origem_service.py
parametrizacao_service.py
payment_service.py
pena_administrativa_service.py
perdimento_service.py
performance_bond_service.py
permissao_especial_service.py
pis_pasep_importacao_service.py
porto_alfandegado_service.py
posto_fronteira_service.py
processo_administrativo_aduaneiro_service.py
produto_exportacao_service.py
produto_importacao_service.py
proforma_invoice_service.py
radar_service.py
recinto_alfandegado_service.py
recurso_administrativo_aduaneiro_service.py
reexportacao_service.py
registro_contrato_cambio_service.py
registro_exportacao_service.py
registro_importacao_service.py
reimportacao_service.py
remessa_service.py
request_service_port.py
reservas_internacionais_service.py
re_service.py
retencao_carga_service.py
ri_service.py
romaneio_carga_service.py
sadc_service.py
saque_service.py
saude_service_port.py
seguro_carga_service.py
seguro_internacional_service.py
service.py
service_requests_service_port.py
sgp_service.py
siscomex_carga_service.py
siscomex_drawback_service.py
siscomex_exportacao_service.py
siscomex_importacao_service.py
siscomex_manifesto_service.py
siscomex_pagamento_service.py
siscomex_service.py
siscomex_tratamento_service.py
standby_lc_service.py
suspensao_radar_service.py
swap_cambial_service.py
taxa_cambio_service.py
taxas_aduaneiras_service.py
terminal_alfandegado_service.py
transbordo_service.py
transito_aduaneiro_service.py
transito_internacional_service.py
transportador_internacional_service.py
transportes_logistica_service_port.py
treasury_service.py
tributos_federais_service.py
urbanismo_service_port.py
verificacao_documental_service.py
verificacao_fisica_service.py
warranty_bond_service.py
zona_franca_service.py
zona_processamento_exportacao_service.py
zpe_service.py

/home/user/sila-system/apps/backend/app/modules/economy/core/domain:
entities
events
exceptions.py
__init__.py
value_objects

/home/user/sila-system/apps/backend/app/modules/economy/core/domain/entities:
entities_._apoio_empresarial_domain.py
entities_._public_budget_domain.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/core/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/core/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/core/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/economy/core/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/core/infrastructure/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/core/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/domain:
entities
enums
events
exceptions.py
__init__.py
integrations
models
models.py
module.yaml
ports
repositories
repositories.py
services
tests

/home/user/sila-system/apps/backend/app/modules/economy/domain/entities:
budget_line.py
fiscal_transfer.py
__init__.py
treasury_account.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/enums:
__init__.py
status_enum.py
treasury_entry_type.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/integrations:
fuc_client.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/models:
audit_log.py
enums.py
__init__.py
invoice.py
payment.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/ports:
assistencia_social_service_port.py
educacao_service_port.py
emprego_service_port.py
identidade_service_port.py
__init__.py
invoice_repository_port.py
juventude_service_port.py
payment_repository_port.py
saude_service_port.py
service_requests_service_port.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/services:
__init__.py
treasury_ledger_engine.py

/home/user/sila-system/apps/backend/app/modules/economy/domain/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/financas:
ARCHITECTURE.md
domain
__init__.py
module.yaml
public_budget

/home/user/sila-system/apps/backend/app/modules/economy/financas/domain:
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/economy/financas/domain/models:
enums.py
__init__.py
invoice.py
payment.py

/home/user/sila-system/apps/backend/app/modules/economy/financas/public_budget:
infrastructure

/home/user/sila-system/apps/backend/app/modules/economy/financas/public_budget/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/industria:
ARCHITECTURE.md
domain
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/economy/industria/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure:
adapters
adapters.py
application
domain
__init__.py
mocks
models
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure/adapters:
__init__.py
sqlalchemy_invoice_repository.py
sqlalchemy_payment_repository.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure/mocks:
high_speed_payment_mock.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure/models:
__init__.py
invoice_model.py
payment_model.py

/home/user/sila-system/apps/backend/app/modules/economy/infrastructure/repositories:
__init__.py
tax_ledger_repository.py
treasury_account_repository.py

/home/user/sila-system/apps/backend/app/modules/economy/public_budget:
api
ARCHITECTURE.md
domain
health.py
infrastructure
__init__.py
module.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/economy/public_budget/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/economy/public_budget/domain:
entities.py
exceptions.py
__init__.py
policies.py
services.py

/home/user/sila-system/apps/backend/app/modules/economy/public_budget/infrastructure:
__init__.py
models
repository.py

/home/user/sila-system/apps/backend/app/modules/economy/public_budget/infrastructure/models:
despesa_model.py
__init__.py
orcamento_model.py
receita_model.py

/home/user/sila-system/apps/backend/app/modules/economy/public_budget/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
interfaces
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/api:
deps.py
health.py
__init__.py
middleware.py
openapi.py
rate_limiter.py
router.py
schemas
schemas.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/api/schemas:
audit_schema.py
certificate_schema.py
debt_schema.py
declaration_schema.py
error_schema.py
__init__.py
payment_schema.py
taxpayer_schema.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/application:
commands
dto
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/application/ports:
__init__.py
taxpayer_repository.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/domain:
aggregate_entities.py
entities
enums
events
exceptions.py
__init__.py
value_objects

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/domain/entities:
__init__.py
taxpayer_certificate.py
taxpayer_debt.py
taxpayer.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/domain/enums:
declaration_status.py
__init__.py
payment_status.py
taxpayer_status.py
tax_regime.py
tax_type.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/domain/events:
__init__.py
tax_debt_created.py
tax_declaration_filed.py
tax_paid.py
taxpayer_registered.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/domain/value_objects:
__init__.py
nif.py
tax_amount.py
tax_certificate_number.py
tax_declaration_number.py
tax_period.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/infrastructure:
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/infrastructure/models:
__init__.py
taxpayer_model.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/infrastructure/repositories:
__init__.py
sqlalchemy_taxpayer_repository.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/interfaces:
api
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/interfaces/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/taxpayer/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/economy/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/economy/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/economy/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/economy/trade:
api
ARCHITECTURE.md
domain
external
__init__.py
module.yaml
services
tests

/home/user/sila-system/apps/backend/app/modules/economy/trade/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/domain:
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external:
api
application
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/api/endpoints:
acordo_comercial.py
ademe.py
admissao_temporaria.py
advance_payment_bond.py
aeroporto_alfandegado.py
agente_carga.py
airwaybill.py
aladi.py
analise_risco.py
aperfeicoamento_ativo.py
aperfeicoamento_passivo.py
apreensao.py
arbitragem_cambio.py
armazem_alfandegado.py
armazenagem_alfandegada.py
armazenagem.py
assinatura_digital_aduaneira.py
auto_infracao_aduaneiro.py
autorizacao_exportacao.py
autorizacao_importacao.py
awb.py
balanca_comercial.py
balanco_pagamentos.py
baldeacao.py
bank_guarantee.py
bid_bond.py
bill_of_lading.py
bloco_economico.py
bl.py
canal_amarelo.py
canal_cinza.py
canal_parametrizacao.py
canal_verde.py
canal_vermelho.py
cancelamento_radar.py
capatazia.py
carta_credito.py
certificado_analise.py
certificado_digital_aduaneiro.py
certificado_fitossanitario.py
certificado_fumigacao.py
certificado_origem.py
certificado_qualidade.py
certificado_zoossanitario.py
cfr.py
cif.py
cip.py
cobertura_cambial.py
cobranca_documentaria.py
cobranca.py
cofins_importacao.py
commercial_invoice.py
conferencia_aduaneira.py
conferencia_documental.py
conferencia_fisica.py
conhecimento_embarque.py
contrato_cambio_exportacao.py
contrato_cambio_importacao.py
contrato_cambio.py
contrato_exportacao.py
contrato_importacao.py
conversao_moeda.py
cotacao_cambio.py
cpt.py
credito_documentario.py
dap.py
ddp.py
declaracao_aduaneira.py
declaracao_exportacao.py
declaracao_importacao.py
declaracao_unica.py
defesa_aduaneira.py
deposito_alfandegado.py
deposito_especial.py
deposito_industrial.py
deposito_sob_controle.py
de.py
desembaraco.py
despachante.py
despacho_aduaneiro.py
despacho_exportacao.py
despacho_importacao.py
destino_produto.py
di.py
dpd.py
dpu.py
drawback_externo.py
drawback_integrado.py
drawback_interno.py
drawback_isencao.py
drawback.py
drawback_restituicao.py
drawback_substituicao.py
drawback_suspensao.py
drawback_verde_amarelo.py
du.py
entreposto_aduaneiro.py
estacao_aduaneira.py
estatistica_exportacao.py
estatistica_importacao.py
exportacao_temporaria.py
exportadores.py
exw.py
fas.py
fatura_comercial.py
fatura_proforma.py
fca.py
fechamento_cambio.py
fiscalizacao_aduaneira.py
fluxo_cambial.py
fob.py
futuro_cambio.py
garantia_internacional.py
habilitacao_exportador.py
habilitacao_importador.py
habilitacao_radar.py
_habilitacao_router.py
hedge_cambial.py
house_bill.py
hs_code.py
icms_exportacao.py
icms_importacao.py
ie.py
ii.py
importador.py
imposto_exportacao.py
imposto_importacao.py
impugnacao_lancamento.py
incoterm.py
industrializacao_externo.py
industrializacao_terceiros.py
__init__.py
ipi_vinculado.py
iss_importacao.py
julgamento_administrativo.py
lc.py
liberacao.py
licenca_exportacao.py
licenca_importacao.py
li_exportacao.py
li_importacao.py
liquidacao_cambio.py
manifesto_carga.py
marinha_mercantil.py
master_bill.py
mercosul.py
movimentacao_carga.py
multa_aduaneira.py
nacionalizacao.py
ncm.py
opcao_cambial.py
operacao_cambio.py
_operador_logistico_router.py
origem_produto.py
packing_list.py
pagamento_internacional.py
pais_destino.py
pais_origem.py
parametrizacao.py
pena_administrativa.py
perdimento.py
performance_bond.py
permissao_especial.py
pis_pasep_importacao.py
porto_alfandegado.py
posto_fronteira.py
processo_administrativo_aduaneiro.py
produto_exportacao.py
produto_importacao.py
proforma_invoice.py
radar.py
recinto_alfandegado.py
recurso_administrativo_aduaneiro.py
reexportacao.py
registro_contrato_cambio.py
registro_exportacao.py
registro_importacao.py
reimportacao.py
remessa.py
re.py
reservas_internacionais.py
retencao_carga.py
ri.py
romaneio_carga.py
sadc.py
saque.py
seguro_carga.py
seguro_internacional.py
sgp.py
siscomex_carga.py
siscomex_drawback.py
siscomex_exportacao.py
siscomex_importacao.py
siscomex_manifesto.py
siscomex_pagamento.py
siscomex.py
siscomex_tratamento.py
standby_lc.py
suspensao_radar.py
swap_cambial.py
taxa_cambio.py
taxas_aduaneiras.py
terminal_alfandegado.py
transbordo.py
transito_aduaneiro.py
transito_internacional.py
transportador_internacional.py
tributos_federais.py
verificacao_documental.py
verificacao_fisica.py
warranty_bond.py
zona_franca.py
zona_processamento_exportacao.py
zpe.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/api/schemas:
acordo_comercial_schema.py
ademe_schema.py
admissao_temporaria_schema.py
advance_payment_bond_schema.py
aeroporto_alfandegado_schema.py
agente_carga_schema.py
airwaybill_schema.py
aladi_schema.py
analise_risco_schema.py
aperfeicoamento_ativo_schema.py
aperfeicoamento_passivo_schema.py
apreensao_schema.py
arbitragem_cambio_schema.py
armazem_alfandegado_schema.py
armazenagem_alfandegada_schema.py
armazenagem_schema.py
assinatura_digital_aduaneira_schema.py
auto_infracao_aduaneiro_schema.py
autorizacao_exportacao_schema.py
autorizacao_importacao_schema.py
awb_schema.py
balanca_comercial_schema.py
balanco_pagamentos_schema.py
baldeacao_schema.py
bank_guarantee_schema.py
bid_bond_schema.py
bill_of_lading_schema.py
bloco_economico_schema.py
bl_schema.py
canal_amarelo_schema.py
canal_cinza_schema.py
canal_parametrizacao_schema.py
canal_verde_schema.py
canal_vermelho_schema.py
cancelamento_radar_schema.py
capatazia_schema.py
carta_credito_schema.py
certificado_analise_schema.py
certificado_digital_aduaneiro_schema.py
certificado_fitossanitario_schema.py
certificado_fumigacao_schema.py
certificado_origem_schema.py
certificado_qualidade_schema.py
certificado_zoossanitario_schema.py
cfr_schema.py
cif_schema.py
cip_schema.py
cobertura_cambial_schema.py
cobranca_documentaria_schema.py
cobranca_schema.py
cofins_importacao_schema.py
commercial_invoice_schema.py
conferencia_aduaneira_schema.py
conferencia_documental_schema.py
conferencia_fisica_schema.py
conhecimento_embarque_schema.py
contrato_cambio_exportacao_schema.py
contrato_cambio_importacao_schema.py
contrato_cambio_schema.py
contrato_exportacao_schema.py
contrato_importacao_schema.py
conversao_moeda_schema.py
cotacao_cambio_schema.py
cpt_schema.py
credito_documentario_schema.py
dap_schema.py
ddp_schema.py
declaracao_aduaneira_schema.py
declaracao_exportacao_schema.py
declaracao_importacao_schema.py
declaracao_unica_schema.py
defesa_aduaneira_schema.py
deposito_alfandegado_schema.py
deposito_especial_schema.py
deposito_industrial_schema.py
deposito_sob_controle_schema.py
de_schema.py
desembaraco_schema.py
despachante_schema.py
despacho_aduaneiro_schema.py
despacho_exportacao_schema.py
despacho_importacao_schema.py
destino_produto_schema.py
di_schema.py
dpd_schema.py
dpu_schema.py
drawback_externo_schema.py
drawback_integrado_schema.py
drawback_interno_schema.py
drawback_isencao_schema.py
drawback_restituicao_schema.py
drawback_schema.py
drawback_substituicao_schema.py
drawback_suspensao_schema.py
drawback_verde_amarelo_schema.py
du_schema.py
entreposto_aduaneiro_schema.py
estacao_aduaneira_schema.py
estatistica_exportacao_schema.py
estatistica_importacao_schema.py
exportacao_temporaria_schema.py
exportador_schema.py
exw_schema.py
fas_schema.py
fatura_comercial_schema.py
fatura_proforma_schema.py
fca_schema.py
fechamento_cambio_schema.py
fiscalizacao_aduaneira_schema.py
fluxo_cambial_schema.py
fob_schema.py
futuro_cambio_schema.py
garantia_internacional_schema.py
habilitacao_exportador_schema.py
habilitacao_importador_schema.py
habilitacao_radar_schema.py
habilitacao_schema_base.py
hedge_cambial_schema.py
house_bill_schema.py
hs_code_schema.py
icms_exportacao_schema.py
icms_importacao_schema.py
ie_schema.py
ii_schema.py
importador_schema.py
imposto_exportacao_schema.py
imposto_importacao_schema.py
impugnacao_lancamento_schema.py
incoterm_schema.py
industrializacao_externo_schema.py
industrializacao_terceiros_schema.py
__init__.py
ipi_vinculado_schema.py
iss_importacao_schema.py
julgamento_administrativo_schema.py
lc_schema.py
liberacao_schema.py
licenca_exportacao_schema.py
licenca_importacao_schema.py
li_exportacao_schema.py
li_importacao_schema.py
liquidacao_cambio_schema.py
manifesto_carga_schema.py
marinha_mercantil_schema.py
master_bill_schema.py
mercosul_schema.py
movimentacao_carga_schema.py
multa_aduaneira_schema.py
nacionalizacao_schema.py
ncm_schema.py
opcao_cambial_schema.py
operacao_cambio_schema.py
operador_logistico_schema.py
origem_produto_schema.py
packing_list_schema.py
pagamento_internacional_schema.py
pais_destino_schema.py
pais_origem_schema.py
parametrizacao_schema.py
pena_administrativa_schema.py
perdimento_schema.py
performance_bond_schema.py
permissao_especial_schema.py
pis_pasep_importacao_schema.py
porto_alfandegado_schema.py
posto_fronteira_schema.py
processo_administrativo_aduaneiro_schema.py
produto_exportacao_schema.py
produto_importacao_schema.py
proforma_invoice_schema.py
radar_schema.py
recinto_alfandegado_schema.py
recurso_administrativo_aduaneiro_schema.py
reexportacao_schema.py
registro_contrato_cambio_schema.py
registro_exportacao_schema.py
registro_importacao_schema.py
reimportacao_schema.py
remessa_schema.py
re_schema.py
reservas_internacionais_schema.py
retencao_carga_schema.py
ri_schema.py
romaneio_carga_schema.py
sadc_schema.py
saque_schema.py
seguro_carga_schema.py
seguro_internacional_schema.py
sgp_schema.py
siscomex_carga_schema.py
siscomex_drawback_schema.py
siscomex_exportacao_schema.py
siscomex_importacao_schema.py
siscomex_manifesto_schema.py
siscomex_pagamento_schema.py
siscomex_schema.py
siscomex_tratamento_schema.py
standby_lc_schema.py
suspensao_radar_schema.py
swap_cambial_schema.py
taxa_cambio_schema.py
taxas_aduaneiras_schema.py
terminal_alfandegado_schema.py
transbordo_schema.py
transito_aduaneiro_schema.py
transito_internacional_schema.py
transportador_internacional_schema.py
tributos_federais_schema.py
verificacao_documental_schema.py
verificacao_fisica_schema.py
warranty_bond_schema.py
zona_franca_schema.py
zona_processamento_exportacao_schema.py
zpe_schema.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/application/ports:
acordo_comercial_repository_port.py
ademe_repository_port.py
admissao_temporaria_repository_port.py
advance_payment_bond_repository_port.py
aeroporto_alfandegado_repository_port.py
agente_carga_repository_port.py
airwaybill_repository_port.py
aladi_repository_port.py
analise_risco_repository_port.py
aperfeicoamento_ativo_repository_port.py
aperfeicoamento_passivo_repository_port.py
apreensao_repository_port.py
arbitragem_cambio_repository_port.py
armazem_alfandegado_repository_port.py
armazenagem_alfandegada_repository_port.py
armazenagem_repository_port.py
assinatura_digital_aduaneira_repository_port.py
auto_infracao_aduaneiro_repository_port.py
autorizacao_exportacao_repository_port.py
autorizacao_importacao_repository_port.py
awb_repository_port.py
balanca_comercial_repository_port.py
balanco_pagamentos_repository_port.py
baldeacao_repository_port.py
bank_guarantee_repository_port.py
bid_bond_repository_port.py
bill_of_lading_repository_port.py
bloco_economico_repository_port.py
bl_repository_port.py
canal_amarelo_repository_port.py
canal_cinza_repository_port.py
canal_parametrizacao_repository_port.py
canal_verde_repository_port.py
canal_vermelho_repository_port.py
cancelamento_radar_repository_port.py
capatazia_repository_port.py
carta_credito_repository_port.py
certificado_analise_repository_port.py
certificado_digital_aduaneiro_repository_port.py
certificado_fitossanitario_repository_port.py
certificado_fumigacao_repository_port.py
certificado_origem_repository_port.py
certificado_qualidade_repository_port.py
certificado_zoossanitario_repository_port.py
cfr_repository_port.py
cif_repository_port.py
cip_repository_port.py
citizen_service_port.py
cobertura_cambial_repository_port.py
cobranca_documentaria_repository_port.py
cobranca_repository_port.py
cofins_importacao_repository_port.py
comercio_service_port.py
commercial_invoice_repository_port.py
conferencia_aduaneira_repository_port.py
conferencia_documental_repository_port.py
conferencia_fisica_repository_port.py
conhecimento_embarque_repository_port.py
contrato_cambio_exportacao_repository_port.py
contrato_cambio_importacao_repository_port.py
contrato_cambio_repository_port.py
contrato_exportacao_repository_port.py
contrato_importacao_repository_port.py
conversao_moeda_repository_port.py
cotacao_cambio_repository_port.py
cpt_repository_port.py
credito_documentario_repository_port.py
dap_repository_port.py
ddp_repository_port.py
declaracao_aduaneira_repository_port.py
declaracao_exportacao_repository_port.py
declaracao_importacao_repository_port.py
declaracao_unica_repository_port.py
defesa_aduaneira_repository_port.py
deposito_alfandegado_repository_port.py
deposito_especial_repository_port.py
deposito_industrial_repository_port.py
deposito_sob_controle_repository_port.py
de_repository_port.py
desembaraco_repository_port.py
despachante_repository_port.py
despacho_aduaneiro_repository_port.py
despacho_exportacao_repository_port.py
despacho_importacao_repository_port.py
destino_produto_repository_port.py
di_repository_port.py
dpd_repository_port.py
dpu_repository_port.py
drawback_externo_repository_port.py
drawback_integrado_repository_port.py
drawback_interno_repository_port.py
drawback_isencao_repository_port.py
drawback_repository_port.py
drawback_restituicao_repository_port.py
drawback_substituicao_repository_port.py
drawback_suspensao_repository_port.py
drawback_verde_amarelo_repository_port.py
du_repository_port.py
entreposto_aduaneiro_repository_port.py
estacao_aduaneira_repository_port.py
estatistica_exportacao_repository_port.py
estatistica_importacao_repository_port.py
exportacao_temporaria_repository_port.py
exportador_repository_port.py
exw_repository_port.py
fas_repository_port.py
fatura_comercial_repository_port.py
fatura_proforma_repository_port.py
fca_repository_port.py
fechamento_cambio_repository_port.py
financas_impostos_service_port.py
financas_service_port.py
fiscalizacao_aduaneira_repository_port.py
fluxo_cambial_repository_port.py
fob_repository_port.py
futuro_cambio_repository_port.py
garantia_internacional_repository_port.py
geosampa_service_port.py
habilitacao_exportador_repository_port.py
habilitacao_importador_repository_port.py
habilitacao_radar_repository_port.py
habilitacao_repository_port_base.py
hedge_cambial_repository_port.py
house_bill_repository_port.py
hs_code_repository_port.py
icms_exportacao_repository_port.py
icms_importacao_repository_port.py
ie_repository_port.py
ii_repository_port.py
importador_repository_port.py
imposto_exportacao_repository_port.py
imposto_importacao_repository_port.py
impugnacao_lancamento_repository_port.py
incoterm_repository_port.py
industrializacao_externo_repository_port.py
industrializacao_terceiros_repository_port.py
industria_service_port.py
__init__.py
ipi_vinculado_repository_port.py
iss_importacao_repository_port.py
julgamento_administrativo_repository_port.py
lc_repository_port.py
liberacao_repository_port.py
licenca_exportacao_repository_port.py
licenca_importacao_repository_port.py
li_exportacao_repository_port.py
li_importacao_repository_port.py
liquidacao_cambio_repository_port.py
manifesto_carga_repository_port.py
marinha_mercantil_repository_port.py
master_bill_repository_port.py
mercosul_repository_port.py
movimentacao_carga_repository_port.py
multa_aduaneira_repository_port.py
nacionalizacao_repository_port.py
ncm_repository_port.py
opcao_cambial_repository_port.py
operacao_cambio_repository_port.py
operador_logistico_repository_port.py
origem_produto_repository_port.py
packing_list_repository_port.py
pagamento_internacional_repository_port.py
pais_destino_repository_port.py
pais_origem_repository_port.py
parametrizacao_repository_port.py
pena_administrativa_repository_port.py
perdimento_repository_port.py
performance_bond_repository_port.py
permissao_especial_repository_port.py
pis_pasep_importacao_repository_port.py
porto_alfandegado_repository_port.py
posto_fronteira_repository_port.py
processo_administrativo_aduaneiro_repository_port.py
produto_exportacao_repository_port.py
produto_importacao_repository_port.py
proforma_invoice_repository_port.py
radar_repository_port.py
recinto_alfandegado_repository_port.py
recurso_administrativo_aduaneiro_repository_port.py
reexportacao_repository_port.py
registro_contrato_cambio_repository_port.py
registro_exportacao_repository_port.py
registro_importacao_repository_port.py
reimportacao_repository_port.py
remessa_repository_port.py
request_service_port.py
re_repository_port.py
reservas_internacionais_repository_port.py
retencao_carga_repository_port.py
ri_repository_port.py
romaneio_carga_repository_port.py
sadc_repository_port.py
saque_repository_port.py
seguro_carga_repository_port.py
seguro_internacional_repository_port.py
sgp_repository_port.py
siscomex_carga_repository_port.py
siscomex_drawback_repository_port.py
siscomex_exportacao_repository_port.py
siscomex_importacao_repository_port.py
siscomex_manifesto_repository_port.py
siscomex_pagamento_repository_port.py
siscomex_repository_port.py
siscomex_tratamento_repository_port.py
standby_lc_repository_port.py
suspensao_radar_repository_port.py
swap_cambial_repository_port.py
taxa_cambio_repository_port.py
taxas_aduaneiras_repository_port.py
terminal_alfandegado_repository_port.py
transbordo_repository_port.py
transito_aduaneiro_repository_port.py
transito_internacional_repository_port.py
transportador_internacional_repository_port.py
transportes_logistica_service_port.py
tributos_federais_repository_port.py
verificacao_documental_repository_port.py
verificacao_fisica_repository_port.py
warranty_bond_repository_port.py
zona_franca_repository_port.py
zona_processamento_exportacao_repository_port.py
zpe_repository_port.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/application/services:
acordo_comercial_service.py
ademe_service.py
admissao_temporaria_service.py
advance_payment_bond_service.py
aeroporto_alfandegado_service.py
agente_carga_service.py
airwaybill_service.py
aladi_service.py
analise_risco_service.py
aperfeicoamento_ativo_service.py
aperfeicoamento_passivo_service.py
apreensao_service.py
arbitragem_cambio_service.py
armazem_alfandegado_service.py
armazenagem_alfandegada_service.py
armazenagem_service.py
assinatura_digital_aduaneira_service.py
auto_infracao_aduaneiro_service.py
autorizacao_exportacao_service.py
autorizacao_importacao_service.py
awb_service.py
balanca_comercial_service.py
balanco_pagamentos_service.py
baldeacao_service.py
bank_guarantee_service.py
bid_bond_service.py
bill_of_lading_service.py
bloco_economico_service.py
bl_service.py
canal_amarelo_service.py
canal_cinza_service.py
canal_parametrizacao_service.py
canal_verde_service.py
canal_vermelho_service.py
cancelamento_radar_service.py
capatazia_service.py
carta_credito_service.py
certificado_analise_service.py
certificado_digital_aduaneiro_service.py
certificado_fitossanitario_service.py
certificado_fumigacao_service.py
certificado_origem_service.py
certificado_qualidade_service.py
certificado_zoossanitario_service.py
cfr_service.py
cif_service.py
cip_service.py
cobertura_cambial_service.py
cobranca_documentaria_service.py
cobranca_service.py
cofins_importacao_service.py
commercial_invoice_service.py
conferencia_aduaneira_service.py
conferencia_documental_service.py
conferencia_fisica_service.py
conhecimento_embarque_service.py
contrato_cambio_exportacao_service.py
contrato_cambio_importacao_service.py
contrato_cambio_service.py
contrato_exportacao_service.py
contrato_importacao_service.py
conversao_moeda_service.py
cotacao_cambio_service.py
cpt_service.py
credito_documentario_service.py
dap_service.py
ddp_service.py
declaracao_aduaneira_service.py
declaracao_exportacao_service.py
declaracao_importacao_service.py
declaracao_unica_service.py
defesa_aduaneira_service.py
deposito_alfandegado_service.py
deposito_especial_service.py
deposito_industrial_service.py
deposito_sob_controle_service.py
desembaraco_service.py
de_service.py
despachante_service.py
despacho_aduaneiro_service.py
despacho_exportacao_service.py
despacho_importacao_service.py
destino_produto_service.py
di_service.py
dpd_service.py
dpu_service.py
drawback_externo_service.py
drawback_integrado_service.py
drawback_interno_service.py
drawback_isencao_service.py
drawback_restituicao_service.py
drawback_service.py
drawback_substituicao_service.py
drawback_suspensao_service.py
drawback_verde_amarelo_service.py
du_service.py
entreposto_aduaneiro_service.py
estacao_aduaneira_service.py
estatistica_exportacao_service.py
estatistica_importacao_service.py
exportacao_temporaria_service.py
exportador_service.py
exw_service.py
fas_service.py
fatura_comercial_service.py
fatura_proforma_service.py
fca_service.py
fechamento_cambio_service.py
fiscalizacao_aduaneira_service.py
fluxo_cambial_service.py
fob_service.py
futuro_cambio_service.py
garantia_internacional_service.py
habilitacao_exportador_service.py
habilitacao_importador_service.py
habilitacao_radar_service.py
habilitacao_service_base.py
hedge_cambial_service.py
house_bill_service.py
hs_code_service.py
icms_exportacao_service.py
icms_importacao_service.py
ie_service.py
ii_service.py
importador_service.py
imposto_exportacao_service.py
imposto_importacao_service.py
impugnacao_lancamento_service.py
incoterm_service.py
industrializacao_externo_service.py
industrializacao_terceiros_service.py
__init__.py
ipi_vinculado_service.py
iss_importacao_service.py
julgamento_administrativo_service.py
lc_service.py
liberacao_service.py
licenca_exportacao_service.py
licenca_importacao_service.py
li_exportacao_service.py
li_importacao_service.py
liquidacao_cambio_service.py
manifesto_carga_service.py
marinha_mercantil_service.py
master_bill_service.py
mercosul_service.py
movimentacao_carga_service.py
multa_aduaneira_service.py
nacionalizacao_service.py
ncm_service.py
opcao_cambial_service.py
operacao_cambio_service.py
operador_logistico_service_base.py
origem_produto_service.py
packing_list_service.py
pagamento_internacional_service.py
pais_destino_service.py
pais_origem_service.py
parametrizacao_service.py
pena_administrativa_service.py
perdimento_service.py
performance_bond_service.py
permissao_especial_service.py
pis_pasep_importacao_service.py
porto_alfandegado_service.py
posto_fronteira_service.py
processo_administrativo_aduaneiro_service.py
produto_exportacao_service.py
produto_importacao_service.py
proforma_invoice_service.py
radar_service.py
recinto_alfandegado_service.py
recurso_administrativo_aduaneiro_service.py
reexportacao_service.py
registro_contrato_cambio_service.py
registro_exportacao_service.py
registro_importacao_service.py
reimportacao_service.py
remessa_service.py
reservas_internacionais_service.py
re_service.py
retencao_carga_service.py
ri_service.py
romaneio_carga_service.py
sadc_service.py
saque_service.py
seguro_carga_service.py
seguro_internacional_service.py
sgp_service.py
siscomex_carga_service.py
siscomex_drawback_service.py
siscomex_exportacao_service.py
siscomex_importacao_service.py
siscomex_manifesto_service.py
siscomex_pagamento_service.py
siscomex_service.py
siscomex_tratamento_service.py
standby_lc_service.py
suspensao_radar_service.py
swap_cambial_service.py
taxa_cambio_service.py
taxas_aduaneiras_service.py
terminal_alfandegado_service.py
transbordo_service.py
transito_aduaneiro_service.py
transito_internacional_service.py
transportador_internacional_service.py
tributos_federais_service.py
verificacao_documental_service.py
verificacao_fisica_service.py
warranty_bond_service.py
zona_franca_service.py
zona_processamento_exportacao_service.py
zpe_service.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/domain:
enums.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/domain/models:
acordo_comercial.py
ademe.py
admissao_temporaria.py
advance_payment_bond.py
aeroporto_alfandegado.py
agente_carga.py
airwaybill.py
aladi.py
analise_risco.py
aperfeicoamento_ativo.py
aperfeicoamento_passivo.py
apreensao.py
arbitragem_cambio.py
armazem_alfandegado.py
armazenagem_alfandegada.py
armazenagem.py
assinatura_digital_aduaneira.py
auto_infracao_aduaneiro.py
autorizacao_exportacao.py
autorizacao_importacao.py
awb.py
balanca_comercial.py
balanco_pagamentos.py
baldeacao.py
bank_guarantee.py
bid_bond.py
bill_of_lading.py
bloco_economico.py
bl.py
canal_amarelo.py
canal_cinza.py
canal_parametrizacao.py
canal_verde.py
canal_vermelho.py
cancelamento_radar.py
capatazia.py
carta_credito.py
certificado_analise.py
certificado_digital_aduaneiro.py
certificado_fitossanitario.py
certificado_fumigacao.py
certificado_origem.py
certificado_qualidade.py
certificado_zoossanitario.py
cfr.py
cif.py
cip.py
cobertura_cambial.py
cobranca_documentaria.py
cobranca.py
cofins_importacao.py
commercial_invoice.py
conferencia_aduaneira.py
conferencia_documental.py
conferencia_fisica.py
conhecimento_embarque.py
contrato_cambio_exportacao.py
contrato_cambio_importacao.py
contrato_cambio.py
contrato_exportacao.py
contrato_importacao.py
conversao_moeda.py
cotacao_cambio.py
cpt.py
credito_documentario.py
dap.py
ddp.py
declaracao_aduaneira.py
declaracao_exportacao.py
declaracao_importacao.py
declaracao_unica.py
defesa_aduaneira.py
deposito_alfandegado.py
deposito_especial.py
deposito_industrial.py
deposito_sob_controle.py
de.py
desembaraco.py
despachante.py
despacho_aduaneiro.py
despacho_exportacao.py
despacho_importacao.py
destino_produto.py
di.py
dpd.py
dpu.py
drawback_externo.py
drawback_integrado.py
drawback_interno.py
drawback_isencao.py
drawback.py
drawback_restituicao.py
drawback_substituicao.py
drawback_suspensao.py
drawback_verde_amarelo.py
du.py
entreposto_aduaneiro.py
estacao_aduaneira.py
estatistica_exportacao.py
estatistica_importacao.py
exportacao_temporaria.py
exportador.py
exw.py
fas.py
fatura_comercial.py
fatura_proforma.py
fca.py
fechamento_cambio.py
fiscalizacao_aduaneira.py
fluxo_cambial.py
fob.py
futuro_cambio.py
garantia_internacional.py
habilitacao_base.py
habilitacao_exportador.py
habilitacao_importador.py
habilitacao_radar.py
hedge_cambial.py
house_bill.py
hs_code.py
icms_exportacao.py
icms_importacao.py
ie.py
ii.py
importador.py
imposto_exportacao.py
imposto_importacao.py
impugnacao_lancamento.py
incoterm.py
industrializacao_externo.py
industrializacao_terceiros.py
__init__.py
ipi_vinculado.py
iss_importacao.py
julgamento_administrativo.py
lc.py
liberacao.py
licenca_exportacao.py
licenca_importacao.py
li_exportacao.py
li_importacao.py
liquidacao_cambio.py
manifesto_carga.py
marinha_mercantil.py
master_bill.py
mercosul.py
movimentacao_carga.py
multa_aduaneira.py
nacionalizacao.py
ncm.py
opcao_cambial.py
operacao_cambio.py
operador_logistico_base.py
origem_produto.py
packing_list.py
pagamento_internacional.py
pais_destino.py
pais_origem.py
parametrizacao.py
pena_administrativa.py
perdimento.py
performance_bond.py
permissao_especial.py
pis_pasep_importacao.py
porto_alfandegado.py
posto_fronteira.py
processo_administrativo_aduaneiro.py
produto_exportacao.py
produto_importacao.py
proforma_invoice.py
radar.py
recinto_alfandegado.py
recurso_administrativo_aduaneiro.py
reexportacao.py
registro_contrato_cambio.py
registro_exportacao.py
registro_importacao.py
reimportacao.py
remessa.py
re.py
reservas_internacionais.py
retencao_carga.py
ri.py
romaneio_carga.py
sadc.py
saque.py
seguro_carga.py
seguro_internacional.py
sgp.py
siscomex_carga.py
siscomex_drawback.py
siscomex_exportacao.py
siscomex_importacao.py
siscomex_manifesto.py
siscomex_pagamento.py
siscomex.py
siscomex_tratamento.py
standby_lc.py
suspensao_radar.py
swap_cambial.py
taxa_cambio.py
taxas_aduaneiras.py
terminal_alfandegado.py
transbordo.py
transito_aduaneiro.py
transito_internacional.py
transportador_internacional.py
tributos_federais.py
verificacao_documental.py
verificacao_fisica.py
warranty_bond.py
zona_franca.py
zona_processamento_exportacao.py
zpe.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/infrastructure/adapters:
citizen_service_adapter.py
comercio_service_adapter.py
financas_impostos_service_adapter.py
financas_service_adapter.py
geosampa_service_adapter.py
industria_service_adapter.py
__init__.py
request_service_adapter.py
transportes_logistica_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/infrastructure/models:
acordo_comercial_model.py
ademe_model.py
admissao_temporaria_model.py
advance_payment_bond_model.py
aeroporto_alfandegado_model.py
agente_carga_model.py
airwaybill_model.py
aladi_model.py
analise_risco_model.py
aperfeicoamento_ativo_model.py
aperfeicoamento_passivo_model.py
apreensao_model.py
arbitragem_cambio_model.py
armazem_alfandegado_model.py
armazenagem_alfandegada_model.py
armazenagem_model.py
assinatura_digital_aduaneira_model.py
auto_infracao_aduaneiro_model.py
autorizacao_exportacao_model.py
autorizacao_importacao_model.py
awb_model.py
balanca_comercial_model.py
balanco_pagamentos_model.py
baldeacao_model.py
bank_guarantee_model.py
bid_bond_model.py
bill_of_lading_model.py
bl_model.py
bloco_economico_model.py
canal_amarelo_model.py
canal_cinza_model.py
canal_parametrizacao_model.py
canal_verde_model.py
canal_vermelho_model.py
cancelamento_radar_model.py
capatazia_model.py
carta_credito_model.py
certificado_analise_model.py
certificado_digital_aduaneiro_model.py
certificado_fitossanitario_model.py
certificado_fumigacao_model.py
certificado_origem_model.py
certificado_qualidade_model.py
certificado_zoossanitario_model.py
cfr_model.py
cif_model.py
cip_model.py
cobertura_cambial_model.py
cobranca_documentaria_model.py
cobranca_model.py
cofins_importacao_model.py
commercial_invoice_model.py
conferencia_aduaneira_model.py
conferencia_documental_model.py
conferencia_fisica_model.py
conhecimento_embarque_model.py
contrato_cambio_exportacao_model.py
contrato_cambio_importacao_model.py
contrato_cambio_model.py
contrato_exportacao_model.py
contrato_importacao_model.py
conversao_moeda_model.py
cotacao_cambio_model.py
cpt_model.py
credito_documentario_model.py
dap_model.py
ddp_model.py
declaracao_aduaneira_model.py
declaracao_exportacao_model.py
declaracao_importacao_model.py
declaracao_unica_model.py
defesa_aduaneira_model.py
de_model.py
deposito_alfandegado_model.py
deposito_especial_model.py
deposito_industrial_model.py
deposito_sob_controle_model.py
desembaraco_model.py
despachante_model.py
despacho_aduaneiro_model.py
despacho_exportacao_model.py
despacho_importacao_model.py
destino_produto_model.py
di_model.py
dpd_model.py
dpu_model.py
drawback_externo_model.py
drawback_integrado_model.py
drawback_interno_model.py
drawback_isencao_model.py
drawback_model.py
drawback_restituicao_model.py
drawback_substituicao_model.py
drawback_suspensao_model.py
drawback_verde_amarelo_model.py
du_model.py
entreposto_aduaneiro_model.py
estacao_aduaneira_model.py
estatistica_exportacao_model.py
estatistica_importacao_model.py
exportacao_temporaria_model.py
exportador_model.py
exw_model.py
fas_model.py
fatura_comercial_model.py
fatura_proforma_model.py
fca_model.py
fechamento_cambio_model.py
fiscalizacao_aduaneira_model.py
fluxo_cambial_model.py
fob_model.py
futuro_cambio_model.py
garantia_internacional_model.py
habilitacao_columns_mixin.py
habilitacao_exportador_model.py
habilitacao_importador_model.py
habilitacao_radar_model.py
hedge_cambial_model.py
house_bill_model.py
hs_code_model.py
icms_exportacao_model.py
icms_importacao_model.py
ie_model.py
ii_model.py
importador_model.py
imposto_exportacao_model.py
imposto_importacao_model.py
impugnacao_lancamento_model.py
incoterm_model.py
industrializacao_externo_model.py
industrializacao_terceiros_model.py
__init__.py
ipi_vinculado_model.py
iss_importacao_model.py
julgamento_administrativo_model.py
lc_model.py
liberacao_model.py
licenca_exportacao_model.py
licenca_importacao_model.py
li_exportacao_model.py
li_importacao_model.py
liquidacao_cambio_model.py
manifesto_carga_model.py
marinha_mercantil_model.py
master_bill_model.py
mercosul_model.py
movimentacao_carga_model.py
multa_aduaneira_model.py
nacionalizacao_model.py
ncm_model.py
opcao_cambial_model.py
operacao_cambio_model.py
operador_logistico_columns_mixin.py
origem_produto_model.py
packing_list_model.py
pagamento_internacional_model.py
pais_destino_model.py
pais_origem_model.py
parametrizacao_model.py
pena_administrativa_model.py
perdimento_model.py
performance_bond_model.py
permissao_especial_model.py
pis_pasep_importacao_model.py
porto_alfandegado_model.py
posto_fronteira_model.py
processo_administrativo_aduaneiro_model.py
produto_exportacao_model.py
produto_importacao_model.py
proforma_invoice_model.py
radar_model.py
recinto_alfandegado_model.py
recurso_administrativo_aduaneiro_model.py
reexportacao_model.py
registro_contrato_cambio_model.py
registro_exportacao_model.py
registro_importacao_model.py
reimportacao_model.py
remessa_model.py
re_model.py
reservas_internacionais_model.py
retencao_carga_model.py
ri_model.py
romaneio_carga_model.py
sadc_model.py
saque_model.py
seguro_carga_model.py
seguro_internacional_model.py
sgp_model.py
siscomex_carga_model.py
siscomex_drawback_model.py
siscomex_exportacao_model.py
siscomex_importacao_model.py
siscomex_manifesto_model.py
siscomex_model.py
siscomex_pagamento_model.py
siscomex_tratamento_model.py
standby_lc_model.py
suspensao_radar_model.py
swap_cambial_model.py
taxa_cambio_model.py
taxas_aduaneiras_model.py
terminal_alfandegado_model.py
transbordo_model.py
transito_aduaneiro_model.py
transito_internacional_model.py
transportador_internacional_model.py
tributos_federais_model.py
verificacao_documental_model.py
verificacao_fisica_model.py
warranty_bond_model.py
zona_franca_model.py
zona_processamento_exportacao_model.py
zpe_model.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/infrastructure/repositories:
__init__.py
in_memory_agente_carga_repository.py
in_memory_cancelamento_radar_repository.py
in_memory_despachante_repository.py
in_memory_drawback_externo_repository.py
in_memory_drawback_integrado_repository.py
in_memory_drawback_interno_repository.py
in_memory_drawback_isencao_repository.py
in_memory_drawback_repository.py
in_memory_drawback_restituicao_repository.py
in_memory_drawback_substituicao_repository.py
in_memory_drawback_suspensao_repository.py
in_memory_drawback_verde_amarelo_repository.py
in_memory_exportador_repository.py
in_memory_habilitacao_exportador_repository.py
in_memory_habilitacao_importador_repository.py
in_memory_habilitacao_radar_repository.py
in_memory_habilitacao_repository_base.py
in_memory_importador_repository.py
in_memory_operador_logistico_repository.py
in_memory_radar_repository.py
in_memory_siscomex_drawback_repository.py
in_memory_suspensao_radar_repository.py
in_memory_transportador_internacional_repository.py
sqlalchemy_acordo_comercial_repository.py
sqlalchemy_ademe_repository.py
sqlalchemy_admissao_temporaria_repository.py
sqlalchemy_advance_payment_bond_repository.py
sqlalchemy_aeroporto_alfandegado_repository.py
sqlalchemy_agente_carga_repository.py
sqlalchemy_airwaybill_repository.py
sqlalchemy_aladi_repository.py
sqlalchemy_analise_risco_repository.py
sqlalchemy_aperfeicoamento_ativo_repository.py
sqlalchemy_aperfeicoamento_passivo_repository.py
sqlalchemy_apreensao_repository.py
sqlalchemy_arbitragem_cambio_repository.py
sqlalchemy_armazem_alfandegado_repository.py
sqlalchemy_armazenagem_alfandegada_repository.py
sqlalchemy_armazenagem_repository.py
sqlalchemy_assinatura_digital_aduaneira_repository.py
sqlalchemy_auto_infracao_aduaneiro_repository.py
sqlalchemy_autorizacao_exportacao_repository.py
sqlalchemy_autorizacao_importacao_repository.py
sqlalchemy_awb_repository.py
sqlalchemy_balanca_comercial_repository.py
sqlalchemy_balanco_pagamentos_repository.py
sqlalchemy_baldeacao_repository.py
sqlalchemy_bank_guarantee_repository.py
sqlalchemy_bid_bond_repository.py
sqlalchemy_bill_of_lading_repository.py
sqlalchemy_bloco_economico_repository.py
sqlalchemy_bl_repository.py
sqlalchemy_canal_amarelo_repository.py
sqlalchemy_canal_cinza_repository.py
sqlalchemy_canal_parametrizacao_repository.py
sqlalchemy_canal_verde_repository.py
sqlalchemy_canal_vermelho_repository.py
sqlalchemy_cancelamento_radar_repository.py
sqlalchemy_capatazia_repository.py
sqlalchemy_carta_credito_repository.py
sqlalchemy_certificado_analise_repository.py
sqlalchemy_certificado_digital_aduaneiro_repository.py
sqlalchemy_certificado_fitossanitario_repository.py
sqlalchemy_certificado_fumigacao_repository.py
sqlalchemy_certificado_origem_repository.py
sqlalchemy_certificado_qualidade_repository.py
sqlalchemy_certificado_zoossanitario_repository.py
sqlalchemy_cfr_repository.py
sqlalchemy_cif_repository.py
sqlalchemy_cip_repository.py
sqlalchemy_cobertura_cambial_repository.py
sqlalchemy_cobranca_documentaria_repository.py
sqlalchemy_cobranca_repository.py
sqlalchemy_cofins_importacao_repository.py
sqlalchemy_commercial_invoice_repository.py
sqlalchemy_conferencia_aduaneira_repository.py
sqlalchemy_conferencia_documental_repository.py
sqlalchemy_conferencia_fisica_repository.py
sqlalchemy_conhecimento_embarque_repository.py
sqlalchemy_contrato_cambio_exportacao_repository.py
sqlalchemy_contrato_cambio_importacao_repository.py
sqlalchemy_contrato_cambio_repository.py
sqlalchemy_contrato_exportacao_repository.py
sqlalchemy_contrato_importacao_repository.py
sqlalchemy_conversao_moeda_repository.py
sqlalchemy_cotacao_cambio_repository.py
sqlalchemy_cpt_repository.py
sqlalchemy_credito_documentario_repository.py
sqlalchemy_dap_repository.py
sqlalchemy_ddp_repository.py
sqlalchemy_declaracao_aduaneira_repository.py
sqlalchemy_declaracao_exportacao_repository.py
sqlalchemy_declaracao_importacao_repository.py
sqlalchemy_declaracao_unica_repository.py
sqlalchemy_defesa_aduaneira_repository.py
sqlalchemy_deposito_alfandegado_repository.py
sqlalchemy_deposito_especial_repository.py
sqlalchemy_deposito_industrial_repository.py
sqlalchemy_deposito_sob_controle_repository.py
sqlalchemy_de_repository.py
sqlalchemy_desembaraco_repository.py
sqlalchemy_despachante_repository.py
sqlalchemy_despacho_aduaneiro_repository.py
sqlalchemy_despacho_exportacao_repository.py
sqlalchemy_despacho_importacao_repository.py
sqlalchemy_destino_produto_repository.py
sqlalchemy_di_repository.py
sqlalchemy_dpd_repository.py
sqlalchemy_dpu_repository.py
sqlalchemy_drawback_externo_repository.py
sqlalchemy_drawback_integrado_repository.py
sqlalchemy_drawback_interno_repository.py
sqlalchemy_drawback_isencao_repository.py
sqlalchemy_drawback_repository.py
sqlalchemy_drawback_restituicao_repository.py
sqlalchemy_drawback_substituicao_repository.py
sqlalchemy_drawback_suspensao_repository.py
sqlalchemy_drawback_verde_amarelo_repository.py
sqlalchemy_du_repository.py
sqlalchemy_entreposto_aduaneiro_repository.py
sqlalchemy_estacao_aduaneira_repository.py
sqlalchemy_estatistica_exportacao_repository.py
sqlalchemy_estatistica_importacao_repository.py
sqlalchemy_exportacao_temporaria_repository.py
sqlalchemy_exportador_repository.py
sqlalchemy_exw_repository.py
sqlalchemy_fas_repository.py
sqlalchemy_fatura_comercial_repository.py
sqlalchemy_fatura_proforma_repository.py
sqlalchemy_fca_repository.py
sqlalchemy_fechamento_cambio_repository.py
sqlalchemy_fiscalizacao_aduaneira_repository.py
sqlalchemy_fluxo_cambial_repository.py
sqlalchemy_fob_repository.py
sqlalchemy_futuro_cambio_repository.py
sqlalchemy_garantia_internacional_repository.py
sqlalchemy_habilitacao_exportador_repository.py
sqlalchemy_habilitacao_importador_repository.py
sqlalchemy_habilitacao_radar_repository.py
sqlalchemy_habilitacao_repository_base.py
sqlalchemy_hedge_cambial_repository.py
sqlalchemy_house_bill_repository.py
sqlalchemy_hs_code_repository.py
sqlalchemy_icms_exportacao_repository.py
sqlalchemy_icms_importacao_repository.py
sqlalchemy_ie_repository.py
sqlalchemy_ii_repository.py
sqlalchemy_importador_repository.py
sqlalchemy_imposto_exportacao_repository.py
sqlalchemy_imposto_importacao_repository.py
sqlalchemy_impugnacao_lancamento_repository.py
sqlalchemy_incoterm_repository.py
sqlalchemy_industrializacao_externo_repository.py
sqlalchemy_industrializacao_terceiros_repository.py
sqlalchemy_ipi_vinculado_repository.py
sqlalchemy_iss_importacao_repository.py
sqlalchemy_julgamento_administrativo_repository.py
sqlalchemy_lc_repository.py
sqlalchemy_liberacao_repository.py
sqlalchemy_licenca_exportacao_repository.py
sqlalchemy_licenca_importacao_repository.py
sqlalchemy_li_exportacao_repository.py
sqlalchemy_li_importacao_repository.py
sqlalchemy_liquidacao_cambio_repository.py
sqlalchemy_manifesto_carga_repository.py
sqlalchemy_marinha_mercantil_repository.py
sqlalchemy_master_bill_repository.py
sqlalchemy_mercosul_repository.py
sqlalchemy_movimentacao_carga_repository.py
sqlalchemy_multa_aduaneira_repository.py
sqlalchemy_nacionalizacao_repository.py
sqlalchemy_ncm_repository.py
sqlalchemy_opcao_cambial_repository.py
sqlalchemy_operacao_cambio_repository.py
sqlalchemy_operador_logistico_repository_base.py
sqlalchemy_origem_produto_repository.py
sqlalchemy_packing_list_repository.py
sqlalchemy_pagamento_internacional_repository.py
sqlalchemy_pais_destino_repository.py
sqlalchemy_pais_origem_repository.py
sqlalchemy_parametrizacao_repository.py
sqlalchemy_pena_administrativa_repository.py
sqlalchemy_perdimento_repository.py
sqlalchemy_performance_bond_repository.py
sqlalchemy_permissao_especial_repository.py
sqlalchemy_pis_pasep_importacao_repository.py
sqlalchemy_porto_alfandegado_repository.py
sqlalchemy_posto_fronteira_repository.py
sqlalchemy_processo_administrativo_aduaneiro_repository.py
sqlalchemy_produto_exportacao_repository.py
sqlalchemy_produto_importacao_repository.py
sqlalchemy_proforma_invoice_repository.py
sqlalchemy_radar_repository.py
sqlalchemy_recinto_alfandegado_repository.py
sqlalchemy_recurso_administrativo_aduaneiro_repository.py
sqlalchemy_reexportacao_repository.py
sqlalchemy_registro_contrato_cambio_repository.py
sqlalchemy_registro_exportacao_repository.py
sqlalchemy_registro_importacao_repository.py
sqlalchemy_reimportacao_repository.py
sqlalchemy_remessa_repository.py
sqlalchemy_re_repository.py
sqlalchemy_reservas_internacionais_repository.py
sqlalchemy_retencao_carga_repository.py
sqlalchemy_ri_repository.py
sqlalchemy_romaneio_carga_repository.py
sqlalchemy_sadc_repository.py
sqlalchemy_saque_repository.py
sqlalchemy_seguro_carga_repository.py
sqlalchemy_seguro_internacional_repository.py
sqlalchemy_sgp_repository.py
sqlalchemy_siscomex_carga_repository.py
sqlalchemy_siscomex_drawback_repository.py
sqlalchemy_siscomex_exportacao_repository.py
sqlalchemy_siscomex_importacao_repository.py
sqlalchemy_siscomex_manifesto_repository.py
sqlalchemy_siscomex_pagamento_repository.py
sqlalchemy_siscomex_repository.py
sqlalchemy_siscomex_tratamento_repository.py
sqlalchemy_standby_lc_repository.py
sqlalchemy_suspensao_radar_repository.py
sqlalchemy_swap_cambial_repository.py
sqlalchemy_taxa_cambio_repository.py
sqlalchemy_taxas_aduaneiras_repository.py
sqlalchemy_terminal_alfandegado_repository.py
sqlalchemy_transbordo_repository.py
sqlalchemy_transito_aduaneiro_repository.py
sqlalchemy_transito_internacional_repository.py
sqlalchemy_transportador_internacional_repository.py
sqlalchemy_tributos_federais_repository.py
sqlalchemy_verificacao_documental_repository.py
sqlalchemy_verificacao_fisica_repository.py
sqlalchemy_warranty_bond_repository.py
sqlalchemy_zona_franca_repository.py
sqlalchemy_zona_processamento_exportacao_repository.py
sqlalchemy_zpe_repository.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/external/tests:
__init__.py
test_acordo_comercial.py
test_ademe.py
test_admissao_temporaria.py
test_advance_payment_bond.py
test_aeroporto_alfandegado.py
test_airwaybill.py
test_aladi.py
test_analise_risco.py
test_aperfeicoamento_ativo.py
test_aperfeicoamento_passivo.py
test_apreensao.py
test_arbitragem_cambio.py
test_armazem_alfandegado.py
test_armazenagem_alfandegada.py
test_armazenagem.py
test_assinatura_digital_aduaneira.py
test_auto_infracao_aduaneiro.py
test_autorizacao_exportacao.py
test_autorizacao_importacao.py
test_auto_wiring.py
test_awb.py
test_balanca_comercial.py
test_balanco_pagamentos.py
test_baldeacao.py
test_bank_guarantee.py
test_bid_bond.py
test_bill_of_lading.py
test_bloco_economico.py
test_bl.py
test_canal_amarelo.py
test_canal_cinza.py
test_canal_parametrizacao.py
test_canal_verde.py
test_canal_vermelho.py
test_capatazia.py
test_carta_credito.py
test_certificado_analise.py
test_certificado_digital_aduaneiro.py
test_certificado_fitossanitario.py
test_certificado_fumigacao.py
test_certificado_origem.py
test_certificado_qualidade.py
test_certificado_zoossanitario.py
test_cfr.py
test_cif.py
test_cip.py
test_cobertura_cambial.py
test_cobranca_documentaria.py
test_cobranca.py
test_cofins_importacao.py
test_commercial_invoice.py
test_conferencia_aduaneira.py
test_conferencia_documental.py
test_conferencia_fisica.py
test_conhecimento_embarque.py
test_contrato_cambio_exportacao.py
test_contrato_cambio_importacao.py
test_contrato_cambio.py
test_contrato_exportacao.py
test_contrato_importacao.py
test_conversao_moeda.py
test_cotacao_cambio.py
test_cpt.py
test_credito_documentario.py
test_dap.py
test_ddp.py
test_declaracao_aduaneira.py
test_declaracao_exportacao.py
test_declaracao_importacao.py
test_declaracao_unica.py
test_defesa_aduaneira.py
test_deposito_alfandegado.py
test_deposito_especial.py
test_deposito_industrial.py
test_deposito_sob_controle.py
test_de.py
test_desembaraco.py
test_despacho_aduaneiro.py
test_despacho_exportacao.py
test_despacho_importacao.py
test_destino_produto.py
test_di.py
test_dpd.py
test_dpu.py
test_drawback_externo.py
test_drawback_integrado.py
test_drawback_interno.py
test_drawback_isencao.py
test_drawback.py
test_drawback_restituicao.py
test_drawback_substituicao.py
test_drawback_suspensao.py
test_drawback_verde_amarelo.py
test_du.py
test_entreposto_aduaneiro.py
test_estacao_aduaneira.py
test_estatistica_exportacao.py
test_estatistica_importacao.py
test_exportacao_temporaria.py
test_exportadores.py
test_exw.py
test_fas.py
test_fatura_comercial.py
test_fatura_proforma.py
test_fca.py
test_fechamento_cambio.py
test_fiscalizacao_aduaneira.py
test_fluxo_cambial.py
test_fob.py
test_futuro_cambio.py
test_garantia_internacional.py
test_habilitacoes.py
test_hedge_cambial.py
test_house_bill.py
test_hs_code.py
test_icms_exportacao.py
test_icms_importacao.py
test_ie.py
test_ii.py
test_importador.py
test_imposto_exportacao.py
test_imposto_importacao.py
test_impugnacao_lancamento.py
test_incoterm.py
test_industrializacao_externo.py
test_industrializacao_terceiros.py
test_ipi_vinculado.py
test_iss_importacao.py
test_julgamento_administrativo.py
test_lc.py
test_liberacao.py
test_licenca_exportacao.py
test_licenca_importacao.py
test_li_exportacao.py
test_li_importacao.py
test_liquidacao_cambio.py
test_manifesto_carga.py
test_marinha_mercantil.py
test_master_bill.py
test_mercosul.py
test_movimentacao_carga.py
test_multa_aduaneira.py
test_nacionalizacao.py
test_ncm.py
test_opcao_cambial.py
test_operacao_cambio.py
test_operadores_logisticos.py
test_origem_produto.py
test_packing_list.py
test_pagamento_internacional.py
test_pais_destino.py
test_pais_origem.py
test_parametrizacao.py
test_pena_administrativa.py
test_perdimento.py
test_performance_bond.py
test_permissao_especial.py
test_pis_pasep_importacao.py
test_porto_alfandegado.py
test_posto_fronteira.py
test_processo_administrativo_aduaneiro.py
test_processos_radar.py
test_produto_exportacao.py
test_produto_importacao.py
test_proforma_invoice.py
test_recinto_alfandegado.py
test_recurso_administrativo_aduaneiro.py
test_reexportacao.py
test_registro_contrato_cambio.py
test_registro_exportacao.py
test_registro_importacao.py
test_reimportacao.py
test_remessa.py
test_re.py
test_reservas_internacionais.py
test_retencao_carga.py
test_ri.py
test_romaneio_carga.py
test_sadc.py
test_saque.py
test_seguro_carga.py
test_seguro_internacional.py
test_sgp.py
test_siscomex_carga.py
test_siscomex_drawback.py
test_siscomex_exportacao.py
test_siscomex_importacao.py
test_siscomex_manifesto.py
test_siscomex_pagamento.py
test_siscomex.py
test_siscomex_tratamento.py
test_standby_lc.py
test_swap_cambial.py
test_taxa_cambio.py
test_taxas_aduaneiras.py
test_terminal_alfandegado.py
test_transbordo.py
test_transito_aduaneiro.py
test_transito_internacional.py
test_tributos_federais.py
test_verificacao_documental.py
test_verificacao_fisica.py
test_warranty_bond.py
test_zona_franca.py
test_zona_processamento_exportacao.py
test_zpe.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services:
api
application
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/api/endpoints:
catalogos.py
estabelecimentos_comerciais.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/api/schemas:
catalogo_schema.py
estabelecimento_comercial_schema.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/application/ports:
citizen_service_port.py
comercio_externo_service_port.py
defesa_consumidor_service_port.py
estabelecimento_comercial_repository_port.py
financas_impostos_service_port.py
geosampa_service_port.py
industria_service_port.py
__init__.py
request_service_port.py
transportes_logistica_service_port.py
urbanismo_service_port.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/application/services:
estabelecimento_comercial_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/domain:
enums.py
__init__.py
models
shared

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/domain/models:
estabelecimento_comercial.py
__init__.py
porte_comercial.py
ramo_comercial.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/domain/shared:
catalogs.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/infrastructure/adapters:
citizen_service_adapter.py
comercio_externo_service_adapter.py
defesa_consumidor_service_adapter.py
financas_impostos_service_adapter.py
geosampa_service_adapter.py
industria_service_adapter.py
__init__.py
request_service_adapter.py
transportes_logistica_service_adapter.py
urbanismo_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/infrastructure/models:
estabelecimento_comercial_model.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/infrastructure/repositories:
__init__.py
sqlalchemy_estabelecimento_comercial_repository.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/services/tests:
conftest.py
__init__.py
pytest.ini
run_local_tests.sh
test_catalogos.py
test_estabelecimentos_comerciais.py

/home/user/sila-system/apps/backend/app/modules/economy/trade/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao:
api
application
ARCHITECTURE.md
delegation
domain
emis
exceptions.py
foundation
governance.py
infrastructure
__init__.py
marketplace
module.yaml
organization
rbac
repositories
service
territory
tests
workflows

/home/user/sila-system/apps/backend/app/modules/educacao/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py
schemas
vacancies_router.py

/home/user/sila-system/apps/backend/app/modules/educacao/api/endpoints:
academic_identity.py
academic_wallet.py
boletins.py
certificados.py
concursos.py
emprego.py
escolas_routes.py
formacoes.py
fuc_routes.py
__init__.py
inscricoes.py
marketplace_endpoints.py
matricula_routes.py
metrics_endpoints.py
propinas.py
transferencias_automacao.py
transferencias.py
transfer_wizard.py
turmas_routes.py
universidade.py
vacancies.py
wizard_matricula.py
_workflow_endpoints.py

/home/user/sila-system/apps/backend/app/modules/educacao/api/schemas:
academic_identity_schema.py
academic_record_schema.py
academic_wallet_schema.py
boletim_schema.py
certificado_schema.py
concurso_schema.py
emprego_schema.py
escola_schema.py
formacao_schema.py
__init__.py
inscricao_schema.py
marketplace_schema.py
matricula_schema.py
propina_schema.py
transferencia_schema.py
transfer_wizard_schema.py
turma_schema.py
universidade_schema.py
vacancy_schema.py
wizard_schema.py
workflow_schema.py

/home/user/sila-system/apps/backend/app/modules/educacao/application:
academic_identity_service.py
academic_record_service.py
academic_wallet_service.py
automation_bridge.py
boletim_service.py
canonical
certificado_service.py
commands
commands.py
concurso_service.py
dto
emprego_service.py
encarregados_service.py
enrollment
enrollment_service.py
event_handlers.py
events
formacao_service.py
identity_governance_service.py
identity_merge_service.py
identity_resolution_service.py
__init__.py
inscricao_service.py
marketplace
pagamento_matricula_service.py
ports
propina_service.py
queries
service.py
services
student_number_generator.py
transactional_enrollment_service.py
transferencia_service.py
transfers
universidade_service.py
workflow_service.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/canonical:
wizard_matricula_service.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/enrollment:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/events:
handlers.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/marketplace:
idempotency_service.py
marketplace_service.py
tasks
timeline_service.py
transfer_wizard_service.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/marketplace/tasks:
reservation_sweeper.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/ports:
academic_identity_repository_port.py
boletim_repository_port.py
capacity_repository_port.py
certificado_repository_port.py
concurso_repository_port.py
emprego_repository_port.py
enrollment_repository_port.py
escola_repository_port.py
formacao_repository_port.py
guardian_repository_port.py
identity_service_port.py
__init__.py
inscricao_repository_port.py
matricula_repository_port.py
propina_repository_port.py
transferencia_repository_port.py
transfer_repository_port.py
turma_repository_port.py
universidade_repository_port.py
wizard_session_repository_port.py
workflow_repository_port.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/services:
__init__.py
matricula_service.py

/home/user/sila-system/apps/backend/app/modules/educacao/application/transfers:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/delegation:
ARCHITECTURE.md
delegation_engine.py
domain
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/educacao/delegation/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain:
academic
academic_identity.py
acreditacao_universitaria.py
alfabetizacao.py
ano_letivo.py
apoio_alimentar_escolar.py
apoio_alimentar.py
avaliacao_desempenho.py
avaliacao_institucional.py
avaliacao.py
boletim.py
bolsa_candidatura.py
bolsa_investigacao.py
candidato_emprego.py
cantina.py
capacitacao_qualidade.py
certificacao_competencias.py
certificacao_profissional.py
certificado_conclusao.py
certificado.py
certificado_universitario.py
concurso_inscricao.py
concurso.py
concurso_resultado.py
credenciamento.py
declaracao_desemprego.py
declaracao_escolar.py
educacao_comunitaria.py
educacao_especial.py
emprego.py
entities
entities.py
enums
enums.py
escola.py
estagio_publico.py
estatistica_superior.py
event_catalog.py
events
exceptions.py
fiscalizacao_trabalho.py
formacao_avancada.py
formacao_certificada.py
formacao_gestores.py
formacao_profissional.py
formacao.py
historico_escolar.py
__init__.py
inscricao_basica.py
inscricao.py
inscricao_secundaria.py
inscricao_superior.py
inscricao_tecnico.py
matricula_universidade.py
mediacao_conflito.py
mediacao_emprego.py
mobilidade_academica.py
mobilidade_publica.py
models
models.py
module.yaml
oferta_emprego.py
parceria_universidade.py
ports
professional
propina.py
reclamacao_trabalhista.py
reconhecimento_diploma.py
reconhecimento_grau.py
reconversao.py
registo_contrato.py
repositories
repositories.py
services
territory.py
tests
transferencia.py
transferencia_universitaria.py
transfer_wizard_session.py
turma.py
vaga.py
value_objects
wizard_session.py
workflow
workflow.py
_workflow_record.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/academic:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/models:
ano_letivo.py
enrollment.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/professional:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/domain/workflow:
strategies

/home/user/sila-system/apps/backend/app/modules/educacao/domain/workflow/strategies:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/emis:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/educacao/emis/api:
endpoints.py
__init__.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/educacao/emis/application:
__init__.py
outbox_worker.py
sync_engine.py
tasks.py

/home/user/sila-system/apps/backend/app/modules/educacao/emis/domain:
exceptions.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/educacao/emis/infrastructure:
emis_client.py
__init__.py
sync_log_model.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation:
ARCHITECTURE.md
audit
authorization
domain
eventbus
identity
__init__.py
module.yaml
notification
observability
ports.py
workflow

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/audit:
service.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/authorization:
service.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/eventbus:
adapters
bus.py
dispatcher.py
dispatcher_sql.py
outbox.py
README.md
sql

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/eventbus/adapters:
kafka.py
rabbitmq.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/eventbus/sql:
models.py
repository.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/identity:
service.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/notification:
service.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/observability:
context.py
correlation.py
decorators.py
health.py
__init__.py
logging.py
metrics.py
middleware.py
models.py
telemetry.py
tracing.py

/home/user/sila-system/apps/backend/app/modules/educacao/foundation/workflow:
engine.py

/home/user/sila-system/apps/backend/app/modules/educacao/infrastructure:
adapters
adapters.py
__init__.py
models
orm
repositories
repositories.py
repository.py

/home/user/sila-system/apps/backend/app/modules/educacao/infrastructure/adapters:
__init__.py
payment_adapter.py

/home/user/sila-system/apps/backend/app/modules/educacao/infrastructure/models:
academic_identity_model.py
academic_record_model.py
ano_letivo_model.py
boletim_model.py
certificado_model.py
concurso_model.py
emprego_model.py
enrollment_model.py
escola_model.py
formacao_model.py
guardian_model.py
guardian_student_link.py
idempotency_model.py
identity_merge_model.py
__init__.py
inscricao_model.py
institution_capacity_model.py
institution_marketplace_projection_model.py
marketplace_institution_model.py
marketplace_projection_model.py
marketplace_vacancy_model.py
propina_model.py
seat_reservation_model.py
student_number_counter.py
transferencia_model.py
transfer_model.py
transfer_wizard_model.py
turma_model.py
universidade_model.py
wizard_session_model.py

/home/user/sila-system/apps/backend/app/modules/educacao/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/infrastructure/repositories:
__init__.py
marketplace_institution_repository.py
marketplace_vacancy_repository.py
seat_reservation_repository.py
sqlalchemy_academic_identity_repository.py
sqlalchemy_boletim_repository.py
sqlalchemy_capacity_repository.py
sqlalchemy_certificado_repository.py
sqlalchemy_concurso_repository.py
sqlalchemy_emprego_repository.py
sqlalchemy_enrollment_repository.py
sqlalchemy_escola_repository.py
sqlalchemy_formacao_repository.py
sqlalchemy_guardian_repository.py
sqlalchemy_inscricao_repository.py
sqlalchemy_propina_repository.py
sqlalchemy_transferencia_repository.py
sqlalchemy_transfer_repository.py
sqlalchemy_turma_repository.py
sqlalchemy_universidade_repository.py
sqlalchemy_wizard_session_repository.py
transfer_wizard_repository.py
_workflow_sqlalchemy_repository.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace:
admissions
ARCHITECTURE.md
booking
config.py
discovery
domain
IMPLEMENTATION_REPORT.md
__init__.py
INTEGRATION_GUIDE.md
MARKETPLACE_ARCHITECTURE.md
matching
module.yaml
ranking
recommendation
router.py
search
transfers

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/admissions:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/admissions/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/admissions/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/admissions/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/admissions/infrastructure:
adapters.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/booking:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/booking/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/booking/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/booking/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/booking/infrastructure:
adapters.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/discovery:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/discovery/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/discovery/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/discovery/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/discovery/infrastructure:
adapters.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/matching:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/matching/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/matching/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/matching/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/matching/infrastructure:
adapters.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/ranking:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/ranking/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/ranking/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/ranking/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/ranking/infrastructure:
adapters.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/recommendation:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/recommendation/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/recommendation/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/recommendation/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/recommendation/infrastructure:
adapters.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/search:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/search/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/search/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/search/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/search/infrastructure:
adapters.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/transfers:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/transfers/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/transfers/application:
__init__.py
ports.py
services.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/transfers/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/marketplace/transfers/infrastructure:
adapters.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/organization:
ARCHITECTURE.md
domain
__init__.py
models.py
module.yaml
organizations.yaml
seed.py
service.py

/home/user/sila-system/apps/backend/app/modules/educacao/organization/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/educacao/rbac:
admin_router.py
ARCHITECTURE.md
domain
__init__.py
module.yaml
policies.py
roles.py

/home/user/sila-system/apps/backend/app/modules/educacao/rbac/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/educacao/repositories:

/home/user/sila-system/apps/backend/app/modules/educacao/service:

/home/user/sila-system/apps/backend/app/modules/educacao/territory:
ARCHITECTURE.md
domain
__init__.py
models.py
module.yaml
service.py

/home/user/sila-system/apps/backend/app/modules/educacao/territory/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests:
api
application
conftest.py
domain
e2e
infrastructure
__init__.py
integration
service
test_boletim.py
test_certificado.py
test_concurso.py
test_emprego.py
test_formacao.py
test_inscricao.py
test_matricula.py
test_propina.py
test_transferencia.py
test_transfer_transaction_service.py
test_universidade.py
unit

/home/user/sila-system/apps/backend/app/modules/educacao/tests/api:
health.py
__init__.py
router.py
test_marketplace_instant_transfer.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests/e2e:
conftest.py
__init__.py
test_01_matricula_e2e.py
test_02_transferencia_e2e.py
test_03_certificado_e2e.py
test_03_matricula_wizard_cancel_e2e.py
test_04_bolsa_e2e.py
test_05_cancelamento_e2e.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/educacao/tests/service:

/home/user/sila-system/apps/backend/app/modules/educacao/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/educacao/workflows:
ARCHITECTURE.md
domain
__init__.py
matricula_workflow.py
module.yaml
transferencia_workflow.py

/home/user/sila-system/apps/backend/app/modules/educacao/workflows/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/emprego:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/emprego/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/emprego/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/energia:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/energia/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/energia/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/energy:
api
application
ARCHITECTURE.md
billing
distribution
domain
generation
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/energy/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py
schemas

/home/user/sila-system/apps/backend/app/modules/energy/api/endpoints:
central_geradora.py
consumo.py
faturas.py
geracao.py
__init__.py
linha_transmissao.py
subestacao.py
usinas.py

/home/user/sila-system/apps/backend/app/modules/energy/api/schemas:
central_geradora_schema.py
consumo_schema.py
dashboard_schema.py
fatura_schema.py
__init__.py
linha_transmissao_schema.py
subestacao_schema.py
usina_schema.py

/home/user/sila-system/apps/backend/app/modules/energy/application:
commands
commands.py
dto
event_handlers.py
events
handlers
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/energy/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/application/events:
bus.py
definitions.py
__init__.py
registry.py

/home/user/sila-system/apps/backend/app/modules/energy/application/handlers:
auditoria_handler.py
faturamento_handler.py
__init__.py
notificacao_handler.py

/home/user/sila-system/apps/backend/app/modules/energy/application/ports:
ambiente_service_port.py
central_geradora_repository_port.py
citizen_service_port.py
consumo_repository_port.py
fatura_repository_port.py
financas_publicas_service_port.py
geosampa_service_port.py
gestao_fundiaria_service_port.py
grid_sensor_port.py
__init__.py
linha_transmissao_repository_port.py
obras_publicas_service_port.py
ons_service_port.py
outbox_repository_port.py
request_service_port.py
subestacao_repository_port.py
urbanismo_service_port.py
usina_repository_port.py

/home/user/sila-system/apps/backend/app/modules/energy/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/application/services:
central_geradora_service.py
consumo_service.py
faturamento_service.py
geracao_service.py
__init__.py
linha_transmissao_service.py
subestacao_service.py
usina_service.py

/home/user/sila-system/apps/backend/app/modules/energy/billing:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/billing/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/energy/billing/application:
__init__.py
services

/home/user/sila-system/apps/backend/app/modules/energy/billing/application/services:
billing_service.py

/home/user/sila-system/apps/backend/app/modules/energy/billing/domain:
consumo_energia.py
fatura_energia.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/billing/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/distribution:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/distribution/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/energy/distribution/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/distribution/domain:
__init__.py
linha_transmissao.py
subestacao.py

/home/user/sila-system/apps/backend/app/modules/energy/distribution/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain:
entities
enums
enums.py
events
exceptions
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects
workers.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/exceptions:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/models:
central_geradora.py
consumo_energia.py
fatura_energia.py
__init__.py
linha_transmissao.py
subestacao.py
usina.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/generation:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/generation/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/energy/generation/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/generation/domain:
central_geradora.py
__init__.py
usina.py

/home/user/sila-system/apps/backend/app/modules/energy/generation/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure:
adapters
adapters.py
__init__.py
models
orm
persistence
repositories
repositories.py
resilience

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure/adapters:
ambiente_service_adapter.py
aneel_adapter.py
citizen_service_adapter.py
financas_publicas_service_adapter.py
geosampa_service_adapter.py
gestao_fundiaria_service_adapter.py
__init__.py
obras_publicas_service_adapter.py
ons_adapter.py
request_service_adapter.py
urbanismo_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure/models:
central_geradora_model.py
consumo_model.py
energy_invoice_model.py
energy_telemetry_model.py
fatura_model.py
__init__.py
linha_transmissao_model.py
outbox_event_model.py
subestacao_model.py
usina_model.py

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure/persistence:
__init__.py
outbox.py
repository.py

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure/repositories:
__init__.py
sqlalchemy_central_geradora_repository.py
sqlalchemy_consumo_repository.py
sqlalchemy_fatura_repository.py
sqlalchemy_linha_transmissao_repository.py
sqlalchemy_subestacao_repository.py
sqlalchemy_usina_repository.py

/home/user/sila-system/apps/backend/app/modules/energy/infrastructure/resilience:
circuit_breaker.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/energy/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/energy/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/energy/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/energy/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/estatistica:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/estatistica/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/estatistica/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/familia:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/familia/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/familia/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/financas-impostos:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/financas-impostos/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/financas-impostos/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/florestas:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/florestas/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/florestas/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/gestao-fundiaria:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/gestao-fundiaria/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/gestao-fundiaria/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/governance:
administracao_local
api
application
ARCHITECTURE.md
cooperacao_internacional
domain
infrastructure
__init__.py
module.yaml
planeamento
service_requests
statistics
tests
workflow

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
presentation
tests

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/application:
commands.py
dto.py
__init__.py
queries.py
service.py

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/domain:
entities.py
exceptions.py
__init__.py
value_objects.py

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/infrastructure:
__init__.py
mappers.py
models.py
repositories

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/infrastructure/repositories:
sqlalchemy_repository.py

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/presentation:
dependencies.py
__init__.py
router.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/governance/administracao_local/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/governance/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/governance/application/commands:
command_handlers.py
governance_commands.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/application/queries:
governance_queries.py
__init__.py
query_handlers.py

/home/user/sila-system/apps/backend/app/modules/governance/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
README.md
tests
workers

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/api/endpoints:
acordos.py
__init__.py
projetos.py
vistos.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/api/schemas:
acordo_schema.py
__init__.py
projeto_cooperacao_schema.py
visto_schema.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/application:
events
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/application/events:
bus.py
definitions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/application/ports:
acordo_repository_port.py
__init__.py
projeto_repository_port.py
visto_repository_port.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/application/services:
acordo_service.py
__init__.py
projeto_cooperacao_service.py
visto_service.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/domain/models:
acordo.py
__init__.py
projeto_cooperacao.py
visto.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/infrastructure:
adapters
__init__.py
persistence
repositories
repository.py
resilience

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/infrastructure/adapters:
cambio_adapter.py
__init__.py
mre_adapter.py
onu_adapter.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/infrastructure/persistence:
__init__.py
outbox.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/infrastructure/repositories:
__init__.py
inmemory_acordo_repository.py
inmemory_projeto_repository.py
inmemory_visto_repository.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/infrastructure/resilience:
circuit_breaker.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/tests:
__init__.py
test_acordo_visto_services.py
test_cooperacao_api.py

/home/user/sila-system/apps/backend/app/modules/governance/cooperacao_internacional/workers:
__init__.py
tratado_monitor_worker.py

/home/user/sila-system/apps/backend/app/modules/governance/domain:
entities
enums
events
exceptions.py
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/governance/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/models:
enums.py
governance_request.py
__init__.py
workflow.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/ports:
aggregate_repository_port.py
__init__.py
workflow_port.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/governance/infrastructure/adapters:
__init__.py
inmemory_workflow.py
sqlalchemy_aggregate_repository.py

/home/user/sila-system/apps/backend/app/modules/governance/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/planeamento:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/governance/planeamento/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/governance/planeamento/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/governance/planeamento/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/planeamento/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/governance/planeamento/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
integrations
interfaces
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/api:
deps.py
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/api/schemas:
attachment_schema.py
__init__.py
request_schema.py
timeline_schema.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/application/ports:
assistencia_client_port.py
attachment_repository_port.py
domain_client_port.py
educacao_client_port.py
emprego_client_port.py
event_bus_port.py
identidade_client_port.py
__init__.py
juventude_client_port.py
request_repository_port.py
request_service_port.py
saude_client_port.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/application/services:
attachment_service.py
__init__.py
request_factory.py
request_lifecycle_service.py
request_service.py
timeline_service.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/domain:
enums.py
exceptions.py
__init__.py
models
value_objects

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/domain/models:
attachment.py
__init__.py
request_event.py
service_request.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/domain/value_objects:
__init__.py
priority.py
request_number.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/infrastructure:
clients
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/infrastructure/clients:
assistencia_client.py
educacao_client.py
emprego_client.py
_helpers.py
identidade_client.py
__init__.py
juventude_client.py
saude_client.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/infrastructure/models:
attachment_model.py
__init__.py
request_event_model.py
request_model.py
service_request_model.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/infrastructure/repositories:
attachment_repository.py
event_repository.py
__init__.py
request_repository.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/integrations:
__init__.py
workflow_client.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/interfaces:
api
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/interfaces/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/service_requests/tests:
__init__.py
test_attachments.py
test_domain_clients_orm_integration.py
test_request_service_domain_clients.py
test_requests.py
test_workflow_integration.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics:
api
application
ARCHITECTURE.md
config.py
data_sources
domain
events
infrastructure
__init__.py
integrations
interfaces
kpis_service.py
module.yaml
resilience
tests
workers

/home/user/sila-system/apps/backend/app/modules/governance/statistics/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/governance/statistics/api/endpoints:
agregacoes.py
alertas.py
analises.py
comparativos.py
dashboards.py
exportacoes.py
indicadores.py
__init__.py
kpis.py
metricas.py
previsoes.py
rankings.py
relatorios.py
tendencias.py
timeseries.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/api/schemas:
agregacao_schema.py
alerta_schema.py
analise_schema.py
comparativo_schema.py
dashboard_schema.py
exportacao_schema.py
generic_named_schema.py
indicador_schema.py
__init__.py
kpi_schema.py
metrica_schema.py
previsao_schema.py
ranking_schema.py
relatorio_schema.py
statistics_schema.py
tendencia_schema.py
timeseries_schema.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/application:
bus.py
events
handlers
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/governance/statistics/application/events:
definitions.py
__init__.py
metrica_events.py
registry.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/application/handlers:
agregacao_handler.py
__init__.py
notificacao_handler.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/application/ports:
aggregation_service_port.py
agregacao_repository_port.py
agricultura_data_source_port.py
alerta_repository_port.py
ambiente_data_source_port.py
analise_repository_port.py
assistencia_social_data_source_port.py
base_data_source_port.py
comercio_externo_data_source_port.py
comparativo_repository_port.py
dashboard_repository_port.py
educacao_data_source_port.py
emprego_data_source_port.py
energia_data_source_port.py
exportacao_repository_port.py
financas_data_source_port.py
indicador_repository_port.py
__init__.py
kpi_repository_port.py
metrica_repository_port.py
named_entity_repository_port.py
outbox_repository_port.py
previsao_repository_port.py
ranking_repository_port.py
relatorio_repository_port.py
saude_data_source_port.py
statistics_repository_port.py
tendencia_repository_port.py
timeseries_repository_port.py
transportes_data_source_port.py
turismo_data_source_port.py
urbanismo_data_source_port.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/application/services:
aggregation_service.py
agregacao_service.py
alerta_service.py
analise_service.py
comparativo_service.py
dashboard_service.py
exportacao_service.py
forecasting_service.py
indicador_service.py
__init__.py
kpi_service.py
metrica_service.py
named_entity_service.py
previsao_service.py
ranking_service.py
relatorio_service.py
statistics_service.py
tendencia_service.py
timeseries_service.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/data_sources:
base_data_source.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/domain:
entities.py
enums.py
exceptions.py
__init__.py
models
value_objects

/home/user/sila-system/apps/backend/app/modules/governance/statistics/domain/models:
aggregation.py
dashboard.py
__init__.py
kpi.py
metrica.py
statistic.py
timeseries_point.py
timeseries.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/domain/value_objects:
__init__.py
kpi_id.py
metrica_id.py
periodo.py
valor_metrica.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/events:
bus.py
definitions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/infrastructure:
adapters
__init__.py
models
persistence
repositories
repository.py
resilience

/home/user/sila-system/apps/backend/app/modules/governance/statistics/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/infrastructure/models:
aggregation_model.py
agregacao_model.py
alerta_model.py
analise_model.py
comparativo_model.py
dashboard_model.py
exportacao_model.py
_generic_named_model.py
indicador_model.py
__init__.py
kpi_model.py
metrica_model.py
outbox_event_model.py
previsao_model.py
ranking_model.py
relatorio_model.py
statistic_model.py
tendencia_model.py
timeseries_model.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/infrastructure/persistence:
__init__.py
outbox.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/infrastructure/repositories:
base_named_repository.py
__init__.py
sqlalchemy_agregacao_repository.py
sqlalchemy_alerta_repository.py
sqlalchemy_analise_repository.py
sqlalchemy_comparativo_repository.py
sqlalchemy_dashboard_repository.py
sqlalchemy_exportacao_repository.py
sqlalchemy_indicador_repository.py
sqlalchemy_kpi_repository.py
sqlalchemy_metrica_repository.py
sqlalchemy_outbox_repository.py
sqlalchemy_previsao_repository.py
sqlalchemy_ranking_repository.py
sqlalchemy_relatorio_repository.py
sqlalchemy_tendencia_repository.py
sqlalchemy_timeseries_repository.py
statistics_repository.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/infrastructure/resilience:
circuit_breaker.py
__init__.py
retry.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/integrations:
assistencia_data_source.py
base_data_source.py
bi_connector.py
data_sources.py
educacao_data_source.py
emprego_data_source.py
identidade_data_source.py
__init__.py
juventude_data_source.py
saude_data_source.py
service_requests_data_source.py
workflow_data_source.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/interfaces:
api
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/interfaces/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/resilience:
circuit_breaker.py
__init__.py
retry.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/tests:
conftest.py
_fakes.py
__init__.py
test_aggregation.py
test_agregacoes.py
test_alertas.py
test_analises.py
test_comparativos.py
test_dashboards.py
test_e2e_fluxo_completo.py
test_exportacoes.py
test_forecasting.py
test_indicadores.py
test_integracao_multimodulo_orm.py
test_kpis.py
test_metricas.py
test_previsoes.py
test_rankings.py
test_relatorios.py
test_statistics_service.py
test_tendencias.py
test_timeseries.py

/home/user/sila-system/apps/backend/app/modules/governance/statistics/workers:
agregacao_worker.py
__init__.py
kpi_calculation_worker.py
outbox_worker.py
relatorio_worker.py
timeseries_worker.py

/home/user/sila-system/apps/backend/app/modules/governance/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/governance/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/governance/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/governance/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
integrations
interfaces
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/governance/workflow/api:
deps.py
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/governance/workflow/api/schemas:
__init__.py
task_schema.py
workflow_schema.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/governance/workflow/application/ports:
assistencia_social_adapter_port.py
educacao_adapter_port.py
emprego_adapter_port.py
identidade_adapter_port.py
__init__.py
juventude_adapter_port.py
saude_adapter_port.py
task_repository_port.py
workflow_repository_port.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/application/services:
__init__.py
sla_service.py
transition_service.py
workflow_engine.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/governance/workflow/domain/models:
__init__.py
workflow_definition.py
workflow_history.py
workflow_instance.py
workflow_state.py
workflow_task.py
workflow_transition.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/governance/workflow/infrastructure/adapters:
assistencia_social_adapter.py
educacao_adapter.py
emprego_adapter.py
identidade_adapter.py
__init__.py
juventude_adapter.py
saude_adapter.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/infrastructure/models:
__init__.py
workflow_definition_model.py
workflow_history_model.py
workflow_instance_model.py
workflow_state_model.py
workflow_task_model.py
workflow_transition_model.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/infrastructure/repositories:
__init__.py
task_repository.py
workflow_repository.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/integrations:
__init__.py
notification_client.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/interfaces:
api
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/interfaces/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/governance/workflow/tests:
__init__.py
test_di_runtime_adapters.py
test_engine.py
test_transitions.py
test_workflow_e2e.py
test_workflow_endpoints_testclient.py

/home/user/sila-system/apps/backend/app/modules/habitacao:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/habitacao/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/habitacao/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/identity:
api
application
ARCHITECTURE.md
domain
governance.py
infrastructure
__init__.py
middleware
module.yaml
subdomains
tests

/home/user/sila-system/apps/backend/app/modules/identity/api:
endpoints
health.py
__init__.py
router.py
routers.py
schemas

/home/user/sila-system/apps/backend/app/modules/identity/api/endpoints:
biometrics.py
__init__.py
qr.py
qr_validator.py

/home/user/sila-system/apps/backend/app/modules/identity/api/schemas:
biometrics.py
qr.py

/home/user/sila-system/apps/backend/app/modules/identity/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/identity/application/commands:
command_handlers.py
identity_commands.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/application/queries:
identity_queries.py
__init__.py
query_handlers.py

/home/user/sila-system/apps/backend/app/modules/identity/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/domain:
entities
enums
events
models
models.py
ports
repositories
repositories.py
services
trust_score.py
value_objects

/home/user/sila-system/apps/backend/app/modules/identity/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/models:
enums.py
identity.py
__init__.py
trust_score.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/ports:
aggregate_repository_port.py
event_publisher_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/services:
__init__.py
qr_service.py
qr_signature_validator.py

/home/user/sila-system/apps/backend/app/modules/identity/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/infrastructure:
adapters
adapters.py
models
orm
repositories
repositories.py
security

/home/user/sila-system/apps/backend/app/modules/identity/infrastructure/adapters:
__init__.py
inmemory_event_publisher.py
sqlalchemy_aggregate_repository.py

/home/user/sila-system/apps/backend/app/modules/identity/infrastructure/models:
biometric_model.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/infrastructure/repositories:
biometric_repository.py
citizen_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/infrastructure/security:
__init__.py
jwt_engine.py

/home/user/sila-system/apps/backend/app/modules/identity/middleware:
api
application
domain
infrastructure
__init__.py
trust_middleware.py

/home/user/sila-system/apps/backend/app/modules/identity/middleware/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/middleware/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/middleware/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/middleware/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains:
biometric_identity
citizen_digital_wallet
citizen_identity_graph
cross_border_identity
decentralized_identity
device_identity
digital_signature_service
__init__.py
legal_signature_validation
national_certificate_authority
national_login
oidc_provider
permission_graph
policy_evaluator
role_engine
saml_gateway
smartcard_identity
sovereign_access_control
sovereign_trust_engine
verifiable_credentials

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/biometric_identity:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/biometric_identity/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/biometric_identity/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/biometric_identity/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/biometric_identity/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_digital_wallet:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_digital_wallet/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_digital_wallet/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_digital_wallet/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_digital_wallet/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_identity_graph:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_identity_graph/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_identity_graph/application:
identity_graph_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_identity_graph/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/citizen_identity_graph/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/cross_border_identity:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/cross_border_identity/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/cross_border_identity/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/cross_border_identity/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/cross_border_identity/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/decentralized_identity:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/decentralized_identity/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/decentralized_identity/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/decentralized_identity/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/decentralized_identity/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/device_identity:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/device_identity/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/device_identity/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/device_identity/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/device_identity/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/digital_signature_service:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/digital_signature_service/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/digital_signature_service/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/digital_signature_service/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/digital_signature_service/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/legal_signature_validation:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/legal_signature_validation/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/legal_signature_validation/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/legal_signature_validation/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/legal_signature_validation/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_certificate_authority:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_certificate_authority/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_certificate_authority/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_certificate_authority/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_certificate_authority/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_login:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_login/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_login/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_login/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/national_login/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/oidc_provider:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/oidc_provider/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/oidc_provider/application:
__init__.py
oidc_service.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/oidc_provider/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/oidc_provider/infrastructure:
__init__.py
jwks.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/permission_graph:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/permission_graph/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/permission_graph/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/permission_graph/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/permission_graph/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/policy_evaluator:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/policy_evaluator/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/policy_evaluator/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/policy_evaluator/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/policy_evaluator/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/role_engine:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/role_engine/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/role_engine/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/role_engine/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/role_engine/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/saml_gateway:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/saml_gateway/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/saml_gateway/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/saml_gateway/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/saml_gateway/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/smartcard_identity:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/smartcard_identity/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/smartcard_identity/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/smartcard_identity/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/smartcard_identity/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_access_control:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_access_control/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_access_control/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_access_control/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_access_control/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_trust_engine:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_trust_engine/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_trust_engine/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_trust_engine/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/sovereign_trust_engine/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/application:
__init__.py
services

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/application/services:
credential_signer.py
revocation_service.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/domain:
entities
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/domain/entities:
credential.py

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/infrastructure:
__init__.py
repositories

/home/user/sila-system/apps/backend/app/modules/identity/subdomains/verifiable_credentials/infrastructure/repositories:
revocation_repository.py

/home/user/sila-system/apps/backend/app/modules/identity/tests:
conftest.py
fixtures
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/identity/tests/fixtures:
__init__.py

/home/user/sila-system/apps/backend/app/modules/identity/tests/integration:
__init__.py
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/identity/tests/unit:
__init__.py
test_domain.py
test_qr_validator.py

/home/user/sila-system/apps/backend/app/modules/igualdade:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/igualdade/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/igualdade/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/industria:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/industria/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/industria/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/industry:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/industry/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py
schemas

/home/user/sila-system/apps/backend/app/modules/industry/api/endpoints:
catalogos.py
estabelecimentos_industriais.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/api/schemas:
catalogo_schema.py
estabelecimento_industrial_schema.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/industry/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/application/dto:
catalogo_schema.py
estabelecimento_industrial_schema.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/application/ports:
aguas_saneamento_service_port.py
ambiente_service_port.py
citizen_service_port.py
comercio_externo_service_port.py
energia_service_port.py
estabelecimento_industrial_repository_port.py
financas_impostos_service_port.py
geosampa_service_port.py
gestao_fundiaria_service_port.py
__init__.py
request_service_port.py
transportes_logistica_service_port.py
urbanismo_service_port.py

/home/user/sila-system/apps/backend/app/modules/industry/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/application/services:
estabelecimento_industrial_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain:
api
entities
enums
enums.py
events
exceptions.py
__init__.py
models
models.py
module.yaml
ports
repositories
repositories.py
services
shared
tests
value_objects

/home/user/sila-system/apps/backend/app/modules/industry/domain/api:
deps.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/models:
estabelecimento_industrial.py
__init__.py
porte_industrial.py
ramo_industrial.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/shared:
catalogs.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/infrastructure:
adapters
adapters.py
__init__.py
models
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/industry/infrastructure/adapters:
aguas_saneamento_service_adapter.py
ambiente_service_adapter.py
citizen_service_adapter.py
comercio_externo_service_adapter.py
energia_service_adapter.py
financas_impostos_service_adapter.py
geosampa_service_adapter.py
gestao_fundiaria_service_adapter.py
__init__.py
request_service_adapter.py
transportes_logistica_service_adapter.py
urbanismo_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/industry/infrastructure/models:
estabelecimento_industrial_model.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/industry/infrastructure/repositories:
__init__.py
sqlalchemy_estabelecimento_industrial_repository.py

/home/user/sila-system/apps/backend/app/modules/industry/tests:
conftest.py
__init__.py
integration
pytest.ini
run_local_tests.sh
test_catalogos.py
test_estabelecimentos_industriais.py
unit

/home/user/sila-system/apps/backend/app/modules/industry/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/industry/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/infrastructure:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/infrastructure/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/api/endpoints:
dashboard.py
editais.py
__init__.py
licitacoes.py
obras.py
projetos.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/application:
commands
commands.py
dto
event_handlers.py
events
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/infrastructure/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/application/dto:
edital_schema.py
__init__.py
licitacao_schema.py
obra_schema.py
projeto_schema.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/application/events:
contracts.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/application/ports:
asset_reporting_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain:
entities
entities.py
enums
enums.py
events
__init__.py
models
models.py
module.yaml
ports
repositories
repositories.py
services
tests
value_objects

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/models:
aditivo_contratual.py
edital.py
fiscalizacao_obra.py
__init__.py
licitacao.py
medicao_obra.py
obra.py
projeto_obra.py
termo_recebimento.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/ports:
aguas_saneamento_service_port.py
ambiente_service_port.py
citizen_service_port.py
edital_repository_port.py
financas_publicas_service_port.py
gestao_fundiaria_service_port.py
__init__.py
justica_service_port.py
licitacao_repository_port.py
obra_repository_port.py
outbox_repository_port.py
projeto_repository_port.py
request_service_port.py
service_requests_service_port.py
transportes_service_port.py
urbanismo_habitacao_service_port.py
workflow_service_port.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/tests:
__init__.py
test_dashboard_projection.py
test_dashboard_query_endpoint.py
test_editais.py
test_event_sourcing_governance.py
test_licitacoes.py
test_obras.py
test_orm_integration_real.py
test_outbox_sqlalchemy_integration.py
test_projetos.py
test_saga_execucao_obra.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure:
adapters
adapters.py
eventsourcing
governance
__init__.py
messaging
models
multi_region
observability
orm
persistence
read_model
repositories
repositories.py
repository.py
resilience
streaming

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/adapters:
aguas_saneamento_service_adapter.py
ambiente_service_adapter.py
citizen_service_adapter.py
economy_asset_adapter.py
financas_publicas_adapter.py
financas_publicas_service_adapter.py
gestao_fundiaria_service_adapter.py
__init__.py
justica_service_adapter.py
request_service_adapter.py
service_requests_service_adapter.py
tcu_adapter.py
transportes_service_adapter.py
urbanismo_habitacao_service_adapter.py
workflow_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/eventsourcing:
event_store_model.py
event_store_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/governance:
event_catalog_model.py
event_governance.py
__init__.py
schema_validator.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/messaging:
__init__.py
outbox_worker.py
runner.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/models:
edital_model.py
__init__.py
licitacao_model.py
obra_model.py
projeto_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/multi_region:
global_id.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/observability:
__init__.py
tracing.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/persistence:
__init__.py
outbox_model.py
outbox_repository.py
saga_model.py
saga_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/read_model:
dashboard_model.py
dashboard_projection_repository.py
__init__.py
session.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/repositories:
__init__.py
sqlalchemy_edital_repository.py
sqlalchemy_licitacao_repository.py
sqlalchemy_obra_repository.py
sqlalchemy_projeto_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/resilience:
bulkhead.py
circuit_breaker.py
__init__.py
rate_limit.py
retry.py
timeout.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/infrastructure/streaming:
bi_producer.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/infrastructure/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector:
api
application
ARCHITECTURE.md
aviacao_civil
domain
gestao_fundiaria
infrastructure
__init__.py
logistica
meteorologia
module.yaml
obras_publicas
telecomunicacoes
tests
urbanismo_habitacao

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
README.md
tests
workers

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/api/endpoints:
aeronaves.py
__init__.py
ocorrencias.py
voos.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/api/schemas:
aeronave_schema.py
aeroporto_schema.py
__init__.py
ocorrencia_schema.py
voo_schema.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/application:
events
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/application/events:
bus.py
definitions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/application/ports:
aeronave_repository_port.py
__init__.py
ocorrencia_repository_port.py
voo_repository_port.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/application/services:
aeronave_service.py
__init__.py
ocorrencia_service.py
voo_service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/domain/models:
aeronave.py
aeroporto.py
__init__.py
ocorrencia.py
voo.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/infrastructure:
adapters
__init__.py
persistence
repositories
repository.py
resilience

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/infrastructure/adapters:
anac_adapter.py
decea_adapter.py
__init__.py
meteorologia_adapter.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/infrastructure/persistence:
__init__.py
outbox.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/infrastructure/repositories:
__init__.py
inmemory_aeronave_repository.py
inmemory_ocorrencia_repository.py
inmemory_voo_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/infrastructure/resilience:
circuit_breaker.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/tests:
__init__.py
test_aviacao_api.py
test_voo_service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/aviacao_civil/workers:
__init__.py
voo_monitor_worker.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain:
entities
enums
events
exceptions.py
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/api/endpoints:
desapropriacoes.py
georreferenciamentos.py
imoveis.py
__init__.py
matriculas.py
oneracoes.py
proprietarios.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/api/schemas:
desapropriacao_schema.py
georreferenciamento_schema.py
imovel_schema.py
__init__.py
matricula_schema.py
oneracao_schema.py
proprietario_schema.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/application/ports:
agricultura_service_port.py
ambiente_service_port.py
citizen_service_port.py
desapropriacao_repository_port.py
georreferenciamento_repository_port.py
geosampa_service_port.py
imovel_repository_port.py
__init__.py
justica_service_port.py
matricula_imovel_repository_port.py
oneracao_repository_port.py
proprietario_repository_port.py
request_service_port.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/application/services:
desapropriacao_service.py
georreferenciamento_service.py
imovel_service.py
__init__.py
matricula_imovel_service.py
oneracao_service.py
proprietario_service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/domain/models:
desapropriacao.py
georreferenciamento.py
imovel.py
__init__.py
matricula_imovel.py
oneracao.py
proprietario.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/infrastructure/adapters:
agricultura_service_adapter.py
ambiente_service_adapter.py
citizen_service_adapter.py
geosampa_service_adapter.py
__init__.py
justica_service_adapter.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/infrastructure/models:
desapropriacao_model.py
georreferenciamento_model.py
imovel_model.py
__init__.py
matricula_imovel_model.py
oneracao_model.py
proprietario_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/infrastructure/repositories:
__init__.py
sqlalchemy_desapropriacao_repository.py
sqlalchemy_georreferenciamento_repository.py
sqlalchemy_imovel_repository.py
sqlalchemy_matricula_imovel_repository.py
sqlalchemy_oneracao_repository.py
sqlalchemy_proprietario_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/gestao_fundiaria/tests:
__init__.py
test_desapropriacoes.py
test_georreferenciamentos.py
test_imoveis.py
test_matriculas.py
test_oneracoes.py
test_orm_integration_real.py
test_proprietarios.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
ports
tests
transport

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/domain:
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/ports:
api
application
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/ports/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/ports/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/ports/domain:
entities.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/ports/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/transport:
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/transport/infrastructure:
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/logistica/transport/infrastructure/models:
bilhetagem_evento_model.py
frota_model.py
__init__.py
linha_model.py
veiculo_model.py
viagem_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/api/endpoints:
estacoes.py
__init__.py
observacoes.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/api/schemas:
estacao_schema.py
__init__.py
observacao_schema.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/application/ports:
alerta_service_port.py
estacao_repository_port.py
__init__.py
observacao_repository_port.py
request_service_port.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/application/services:
alerta_service.py
estacao_service.py
__init__.py
processamento_service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/domain/models:
estacao.py
__init__.py
observacao.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/infrastructure/adapters:
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/infrastructure/models:
estacao_model.py
__init__.py
observacao_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/infrastructure/repositories:
__init__.py
sqlalchemy_estacao_repository.py
sqlalchemy_observacao_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/tests:
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/tests/integration:
__init__.py
test_http_endpoints.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/tests/unit:
domain
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/meteorologia/tests/unit/domain:
__init__.py
test_observacao.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas:
api
application
ARCHITECTURE.md
core
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/core:
application
domain
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/core/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/core/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/domain:
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/infrastructure:
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/infrastructure/models:
edital_model.py
__init__.py
licitacao_model.py
obra_model.py
projeto_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/obras_publicas/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests
workers

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/api/endpoints:
assinantes.py
espectros.py
faturas.py
indicadores_qualidade.py
infraestruturas.py
__init__.py
operadoras.py
outorgas_espectro.py
qualidade_servico.py
reclamacoes.py
slas.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/api/schemas:
assinante_schema.py
espectro_schema.py
fatura_schema.py
indicador_qualidade_schema.py
infraestrutura_schema.py
__init__.py
operadora_schema.py
outorga_espectro_schema.py
qualidade_servico_schema.py
reclamacao_schema.py
sla_schema.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/application:
events
handlers
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/application/events:
bus.py
definitions.py
__init__.py
registry.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/application/handlers:
anatel_handler.py
faturamento_handler.py
__init__.py
qualidade_handler.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/application/ports:
assinante_repository_port.py
citizen_service_port.py
espectro_repository_port.py
fatura_repository_port.py
indicador_qualidade_repository_port.py
infraestrutura_repository_port.py
__init__.py
operadora_repository_port.py
outbox_repository_port.py
outorga_espectro_repository_port.py
qualidade_servico_repository_port.py
reclamacao_repository_port.py
request_service_port.py
sla_repository_port.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/application/services:
assinante_service.py
espectro_service.py
faturamento_service.py
indicador_qualidade_service.py
infraestrutura_service.py
__init__.py
operadora_service.py
outorga_espectro_service.py
qualidade_servico_service.py
reclamacao_service.py
sla_service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/domain:
enums.py
events
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/domain/models:
assinante.py
cobertura.py
consumo_dados.py
espectro.py
fatura_telecom.py
franquia.py
indicador_qualidade.py
infraestrutura_telco.py
__init__.py
operadora.py
outorga_espectro.py
qualidade_servico.py
reclamacao.py
sla.py
velocidade.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/infrastructure:
adapters
__init__.py
models
persistence
repositories
resilience

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/infrastructure/adapters:
ambiente_adapter.py
anacom_adapter.py
anatel_adapter.py
citizen_service_adapter.py
energia_adapter.py
financas_adapter.py
geosampa_adapter.py
__init__.py
obras_publicas_adapter.py
request_service_adapter.py
urbanismo_adapter.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/infrastructure/models:
assinante_model.py
espectro_model.py
fatura_model.py
indicador_qualidade_model.py
infraestrutura_telco_model.py
__init__.py
operadora_model.py
outorga_espectro_model.py
qualidade_servico_model.py
reclamacao_model.py
sla_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/infrastructure/persistence:
__init__.py
outbox_model.py
outbox.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/infrastructure/repositories:
base.py
__init__.py
sqlalchemy_assinante_repository.py
sqlalchemy_espectro_repository.py
sqlalchemy_fatura_repository.py
sqlalchemy_indicador_qualidade_repository.py
sqlalchemy_infraestrutura_repository.py
sqlalchemy_operadora_repository.py
sqlalchemy_outorga_espectro_repository.py
sqlalchemy_qualidade_servico_repository.py
sqlalchemy_reclamacao_repository.py
sqlalchemy_sla_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/infrastructure/resilience:
circuit_breaker.py
__init__.py
retry.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/tests:
_fakes.py
__init__.py
test_anatel_adapter.py
test_assinantes.py
test_espectros.py
test_indicadores_qualidade.py
test_infraestruturas.py
test_operadoras.py
test_orm_integration_real.py
test_outorgas_espectro.py
test_qualidade_servico.py
test_slas.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/telecomunicacoes/workers:
anatel_reporter.py
__init__.py
outbox_worker.py
qualidade_monitor.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/api/endpoints:
alvaras.py
habitese.py
__init__.py
licencas_urbanisticas.py
loteamentos.py
operacoes_urbanas.py
parcelamentos.py
planos_diretores.py
zoneamento.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/api/schemas:
alvara_schema.py
habite_se_schema.py
__init__.py
licenca_urbanistica_schema.py
loteamento_schema.py
operacao_urbana_schema.py
parcelamento_schema.py
plano_diretor_schema.py
zoneamento_schema.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/application/ports:
aguas_saneamento_service_port.py
alvara_repository_port.py
ambiente_service_port.py
citizen_service_port.py
financas_service_port.py
geosampa_service_port.py
gestao_fundiaria_service_port.py
habite_se_repository_port.py
__init__.py
licenca_urbanistica_repository_port.py
loteamento_repository_port.py
obras_publicas_service_port.py
operacao_urbana_repository_port.py
parcelamento_repository_port.py
plano_diretor_repository_port.py
request_service_port.py
seguranca_social_service_port.py
transportes_service_port.py
workflow_service_port.py
zoneamento_repository_port.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/application/services:
alvara_service.py
habite_se_service.py
__init__.py
licenciamento_urbano_service.py
loteamento_service.py
operacao_urbana_service.py
parcelamento_service.py
plano_diretor_service.py
zoneamento_service.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/domain/models:
alvara.py
habite_se.py
__init__.py
licenca_urbanistica.py
loteamento.py
operacao_urbana.py
parcelamento.py
plano_diretor.py
zoneamento.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/infrastructure/adapters:
aguas_saneamento_service_adapter.py
ambiente_service_adapter.py
citizen_service_adapter.py
financas_service_adapter.py
geosampa_service_adapter.py
gestao_fundiaria_service_adapter.py
__init__.py
obras_publicas_service_adapter.py
request_service_adapter.py
seguranca_social_service_adapter.py
transportes_service_adapter.py
workflow_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/infrastructure/models:
alvara_model.py
habite_se_model.py
__init__.py
licenca_urbanistica_model.py
loteamento_model.py
operacao_urbana_model.py
parcelamento_model.py
plano_diretor_model.py
zoneamento_model.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/infrastructure/repositories:
__init__.py
sqlalchemy_alvara_repository.py
sqlalchemy_habite_se_repository.py
sqlalchemy_licenca_urbanistica_repository.py
sqlalchemy_loteamento_repository.py
sqlalchemy_operacao_urbana_repository.py
sqlalchemy_parcelamento_repository.py
sqlalchemy_plano_diretor_repository.py
sqlalchemy_zoneamento_repository.py

/home/user/sila-system/apps/backend/app/modules/infrastructure_sector/urbanismo_habitacao/tests:
__init__.py
test_licencas_urbanisticas.py
test_loteamentos.py
test_operacoes_urbanas.py
test_orm_integration_real.py
test_parcelamentos.py
test_planos_diretores.py
test_zoneamento.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
subdomains

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/api:
health.py
__init__.py
routers.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains:
bi
__init__.py
moradas
nif
verificacao-documental

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi:
api
application
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/api:
health.py
__init__.py
router.py
routers.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/application/ports:
bi_provider_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/application/services:
bi_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/domain:
enums
exceptions.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/domain/enums:
__init__.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/bi/infrastructure:
adapters.py
adapters_real.py
__init__.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas:
api
application
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/api:
health.py
__init__.py
router.py
routers.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/application/ports:
__init__.py
morada_provider_port.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/application/services:
__init__.py
morada_service.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/domain:
enums
exceptions.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/domain/enums:
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/moradas/infrastructure:
adapters.py
__init__.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif:
api
application
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/api:
health.py
__init__.py
router.py
routers.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/application/ports:
__init__.py
nif_provider_port.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/application/services:
__init__.py
nif_service.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/domain:
enums
exceptions.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/domain/enums:
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/nif/infrastructure:
adapters.py
adapters_real.py
__init__.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental:
api
application
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/api:
health.py
__init__.py
router.py
routers.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/application/ports:
documento_provider_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/application/services:
__init__.py
verificacao_service.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/domain:
enums
exceptions.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/domain/enums:
__init__.py

/home/user/sila-system/apps/backend/app/modules/integracao-nacional/subdomains/verificacao-documental/infrastructure:
adapters.py
__init__.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/intelligence:
api
application
ARCHITECTURE.md
arquivo_nacional
bi
ciencia_pesquisa
defesa_consumidor
domain
infrastructure
__init__.py
module.yaml
operations
tecnologia_inovacao
tests

/home/user/sila-system/apps/backend/app/modules/intelligence/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/intelligence/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/intelligence/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/api:
health.py
__init__.py
router.py
routers
schemas

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/api/routers:
documento_router.py
__init__.py
plano_classificacao_router.py
processo_router.py
tabela_temporalidade_router.py

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/api/schemas:
documento_schema.py
__init__.py
plano_classificacao_schema.py
processo_schema.py
tabela_temporalidade_schema.py

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/application:
__init__.py
service.py
services

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/application/services:
_base.py
documento_service.py
__init__.py
plano_classificacao_service.py
processo_service.py
tabela_temporalidade_service.py

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/intelligence/arquivo_nacional/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
integrations
interfaces
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/api:
deps.py
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/api/schemas:
dashboard_schema.py
__init__.py
kpi_schema.py
report_schema.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/application/ports:
__init__.py
metrics_repository_port.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/application/services:
analytics_service.py
dashboard_service.py
__init__.py
kpi_service.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/domain/models:
dashboard.py
__init__.py
metric.py
report.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/infrastructure:
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/infrastructure/models:
dashboard_model.py
__init__.py
metric_model.py
report_model.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/infrastructure/repositories:
dashboard_repository.py
__init__.py
metrics_repository.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/integrations:
data_sources.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/interfaces:
api
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/interfaces/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/bi/tests:
conftest.py
__init__.py
test_dashboard.py
test_data_sources_orm_integration.py
test_kpis.py
test_reports.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/api/endpoints:
__init__.py
instituicoes.py
pesquisadores.py
projetos.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/api/schemas:
__init__.py
instituicao_pesquisa_schema.py
pesquisador_schema.py
projeto_pesquisa_schema.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/application/ports:
__init__.py
instituicao_pesquisa_repository_port.py
instituicao_repository_port.py
pesquisador_repository_port.py
projeto_pesquisa_repository_port.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/application/services:
__init__.py
instituicao_pesquisa_service.py
pesquisador_service.py
projeto_pesquisa_service.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/domain/models:
__init__.py
instituicao_pesquisa.py
pesquisador.py
projeto_pesquisa.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/infrastructure/models:
__init__.py
instituicao_pesquisa_model.py
pesquisador_model.py
projeto_pesquisa_model.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/infrastructure/repositories:
__init__.py
in_memory_repositories.py
sqlalchemy_instituicao_pesquisa_repository.py
sqlalchemy_pesquisador_repository.py
sqlalchemy_projeto_pesquisa_repository.py

/home/user/sila-system/apps/backend/app/modules/intelligence/ciencia_pesquisa/tests:
_fakes.py
__init__.py
test_instituicoes.py
test_pesquisadores.py
test_ports_contratuais.py
test_projetos.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests
workers

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/api:
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/api/endpoints:
arbitragem.py
consumidores.py
estabelecimentos.py
__init__.py
mediacao.py
produtos.py
recalls.py
reclamacoes.py
sancoes.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/api/schemas:
consumidor_schema.py
estabelecimento_schema.py
__init__.py
mediacao_schema.py
reclamacao_schema.py
sancao_schema.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/application:
events
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/application/events:
__init__.py
reclamacao_events.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/application/ports:
citizen_service_port.py
comercio_servicos_service_port.py
__init__.py
mediacao_repository_port.py
reclamacao_repository_port.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/application/services:
__init__.py
mediacao_service.py
reclamacao_service.py
sancao_service.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/domain/models:
consumidor.py
estabelecimento.py
mediacao.py
reclamacao.py
sancao.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/infrastructure:
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/infrastructure/models:
__init__.py
reclamacao_model.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/infrastructure/repositories:
__init__.py
sqlalchemy_mediacao_repository.py
sqlalchemy_reclamacao_repository.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/tests:
__init__.py
test_e2e_fluxo_completo.py
test_mediacoes.py
test_orm_integration_real.py
test_reclamacoes.py

/home/user/sila-system/apps/backend/app/modules/intelligence/defesa_consumidor/workers:
__init__.py
outbox_worker.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain:
entities
enums
events
exceptions.py
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/intelligence/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/operations:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/api:
deps.py
health.py
__init__.py
router.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/application:
__init__.py
services

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/application/services:
__init__.py
operations_service.py

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/domain:
enums.py
exceptions.py
__init__.py
state_machine.py

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/infrastructure:
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/infrastructure/models:
__init__.py
order_model.py
payment_model.py

/home/user/sila-system/apps/backend/app/modules/intelligence/operations/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tecnologia_inovacao:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/intelligence/tecnologia_inovacao/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tecnologia_inovacao/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tecnologia_inovacao/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tecnologia_inovacao/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tecnologia_inovacao/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/intelligence/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/intelligence/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/justica:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/justica/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/justica/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/justice:
api
application
ARCHITECTURE.md
civil_registry
_deprecated
domain
events
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/justice/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/justice/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/justice/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry:
adapters
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/application:
__init__.py
services

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/application/services:
__init__.py
queries.py
routing_engine.py

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/domain:
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/domain/models:
document.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/infrastructure:
__init__.py
repositories

/home/user/sila-system/apps/backend/app/modules/justice/civil_registry/infrastructure/repositories:
citizen_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated:
api
application
ARCHITECTURE.md
bounded_contexts
civil_registry
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts:
application
cemetery_management
civil_registry_core
identity_documents
infrastructure
__init__.py
permissions
vital_events

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/application/ports:
assistencia_social_service_port.py
bi_repository_port.py
birth_repository_port.py
cemetery_inspection_repository_port.py
citizen_fuc_client_port.py
citizen_port.py
citizen_repository_port.py
death_repository_port.py
document_repository_port.py
educacao_service_port.py
emprego_service_port.py
identity_request_repository_port.py
__init__.py
juventude_service_port.py
marriage_repository_port.py
platform_shared_ports.py
saude_service_port.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/application/services:
services

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/application/services/services:
document_service.py
__init__.py
request_service.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/cemetery_management:
api
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/cemetery_management/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/cemetery_management/application:
cemetery_inspection_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/cemetery_management/domain:
cemetery_inspection_record.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/cemetery_management/infrastructure:
cemetery_inspection_model.py
cemetery_inspection_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core:
api
application
domain
infrastructure
__init__.py
projections

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/api:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/application/ports:
citizen_repository_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/application/services:
citizen_service.py
__init__.py
profile_queries.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/domain:
aggregates
__init__.py
value_objects

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/domain/aggregates:
citizen_aggregate.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/domain/value_objects:
__init__.py
nationality.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/infrastructure:
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/infrastructure/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/infrastructure/repositories:
citizen_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/civil_registry_core/projections:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents:
api
application
domain
infrastructure
__init__.py
integrations
projections

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/api:
bi_routes.py
documents_routes.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/application/services:
bi_emission_service.py
certificate_service.py
document_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/domain:
entities
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/infrastructure:
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/infrastructure/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/infrastructure/repositories:
bi_repository.py
document_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/integrations:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/identity_documents/projections:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/infrastructure:
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/infrastructure/models:
bi_event.py
bi_event_record.py
bi.py
bi_record.py
birth_record.py
cemetery_inspection_model.py
cemetery_inspection_record.py
certificate_record.py
citizen_event_model.py
citizen_model.py
citizen.py
civil_event.py
death_record.py
document.py
fuc_projection.py
identity_request.py
identity_request_record.py
__init__.py
marriage_record.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/infrastructure/repositories:
bi_repository.py
birth_repository.py
cemetery_inspection_repository.py
citizen_repository.py
civil_event_repository.py
death_repository.py
document_repository.py
identity_request_repository.py
__init__.py
marriage_repository.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/permissions:
access_control.py
__init__.py
policies.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events:
api
application
domain
events
infrastructure
__init__.py
projections

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/api:
birth_routes.py
death_routes.py
__init__.py
marriage_routes.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/application/services:
birth_service.py
death_service.py
__init__.py
marriage_service.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/domain:
entities
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/infrastructure:
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/infrastructure/models:
birth_model.py
death_model.py
__init__.py
marriage_model.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/infrastructure/repositories:
birth_repository.py
death_repository.py
__init__.py
marriage_repository.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/bounded_contexts/vital_events/projections:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry:
adapters
application
domain
infrastructure
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/application:
__init__.py
services

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/domain:
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/domain/models:
document.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/infrastructure:
__init__.py
repositories

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/civil_registry/infrastructure/repositories:
citizen_repository.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/domain:
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/_deprecated/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain:
adapters
bilhete_identidade.py
birth_record.py
citizen.py
death_record.py
entities
enums
events
exceptions.py
identity_request.py
__init__.py
marriage_record.py
models
models.py
module.yaml
ports
repositories
repositories.py
services
tests
value_objects

/home/user/sila-system/apps/backend/app/modules/justice/domain/adapters:
traffic_violation_adapter.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/tests:
__init__.py
test_sanity.py

/home/user/sila-system/apps/backend/app/modules/justice/domain/value_objects:
__init__.py
nationality.py

/home/user/sila-system/apps/backend/app/modules/justice/events:
api
application
ARCHITECTURE.md
bus.py
definitions.py
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/justice/events/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/justice/events/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/events/domain:
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/events/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/events/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure:
adapters
adapters.py
__init__.py
legacy_adapters
models
orm
ports
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure/legacy_adapters:
assistencia_social_service_adapter.py
attestation_service_adapter.py
certificate_service_adapter.py
civil_registry_adapter.py
educacao_service_adapter.py
emprego_service_adapter.py
finances_service_adapter.py
__init__.py
juventude_service_adapter.py
notification_service_adapter.py
request_tracking_service_adapter.py
saude_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure/models:
__init__.py
traffic_violation_model.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure/ports:
civil_registry_port.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests:
api
application
cemetery_management
civil_registry_core
conftest.py
domain
identity_documents
infrastructure
__init__.py
integration
test_e2e_civil_registry.py
unit
vital_events

/home/user/sila-system/apps/backend/app/modules/justice/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/cemetery_management:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/civil_registry_core:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/identity_documents:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/justice/tests/vital_events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/juventude:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/juventude/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/juventude/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/logistics:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
observability
tests

/home/user/sila-system/apps/backend/app/modules/logistics/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/logistics/api/endpoints:
analytics.py
bilhetagem.py
frotas.py
__init__.py
linhas.py
viagens.py

/home/user/sila-system/apps/backend/app/modules/logistics/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/logistics/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/application/dto:
analytics_schema.py
bilhetagem_schema.py
frota_schema.py
__init__.py
linha_schema.py
viagem_schema.py

/home/user/sila-system/apps/backend/app/modules/logistics/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/application/services:
bilhetagem_service.py
frota_service.py
__init__.py
linha_service.py
operacao_analytics_service.py
toll_service.py
viagem_service.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain:
entities
enums
enums.py
events
__init__.py
models
models.py
module.yaml
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/logistics/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/models:
bilhetagem_eletronica.py
bilhete.py
demanda.py
fiscalizacao_transporte.py
frota.py
__init__.py
linha.py
manutencao.py
qualidade_servico.py
rodovia.py
tarifa.py
veiculo.py
viagem.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/ports:
ambiente_service_port.py
bilhetagem_repository_port.py
citizen_service_port.py
comercio_externo_service_port.py
financas_service_port.py
frota_repository_port.py
geosampa_service_port.py
__init__.py
linha_repository_port.py
obras_publicas_service_port.py
request_service_port.py
seguranca_publica_service_port.py
service_requests_service_port.py
urbanismo_service_port.py
veiculo_repository_port.py
viagem_repository_port.py
workflow_service_port.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/services:
bilhetagem_domain_service.py
frota_domain_service.py
__init__.py
linha_domain_service.py
viagem_domain_service.py

/home/user/sila-system/apps/backend/app/modules/logistics/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/logistics/infrastructure/adapters:
ambiente_service_adapter.py
citizen_service_adapter.py
comercio_externo_service_adapter.py
financas_service_adapter.py
geosampa_service_adapter.py
__init__.py
obras_publicas_service_adapter.py
request_service_adapter.py
seguranca_publica_service_adapter.py
service_requests_service_adapter.py
urbanismo_service_adapter.py
workflow_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/logistics/infrastructure/orm:
bilhetagem_evento_model.py
frota_model.py
__init__.py
linha_model.py
toll_passage_model.py
veiculo_model.py
viagem_model.py

/home/user/sila-system/apps/backend/app/modules/logistics/infrastructure/repositories:
__init__.py
sqlalchemy_bilhetagem_repository.py
sqlalchemy_frota_repository.py
sqlalchemy_linha_repository.py
sqlalchemy_veiculo_repository.py
sqlalchemy_viagem_repository.py

/home/user/sila-system/apps/backend/app/modules/logistics/observability:
__init__.py
logging
metrics
tracing

/home/user/sila-system/apps/backend/app/modules/logistics/observability/logging:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/observability/metrics:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/observability/tracing:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/logistics/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/logistics/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/tests/domain:
__init__.py
test_analytics.py
test_bilhetagem.py
test_frotas.py
test_linhas.py
test_orm_integration_real.py
test_viagens.py

/home/user/sila-system/apps/backend/app/modules/logistics/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/logistics/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/logistics/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/marketplace:
api
application
ARCHITECTURE.md
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/marketplace/api:
router.py

/home/user/sila-system/apps/backend/app/modules/marketplace/application:
adapters.py
dto.py
service.py

/home/user/sila-system/apps/backend/app/modules/marketplace/infrastructure:
redis_orchestration_store.py
redis_store.py

/home/user/sila-system/apps/backend/app/modules/meteorologia:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/meteorologia/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/meteorologia/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/migracao:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/migracao/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/migracao/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/migration_service:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/migration_service/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/migration_service/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
service.py
services

/home/user/sila-system/apps/backend/app/modules/migration_service/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain:
entities
entities.py
enums
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py
repository.py

/home/user/sila-system/apps/backend/app/modules/migration_service/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/unit:
domain
test_domain.py

/home/user/sila-system/apps/backend/app/modules/migration_service/tests/unit/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/notifications:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
models.py
module.yaml
router.py
schemas.py
service.py

/home/user/sila-system/apps/backend/app/modules/notifications/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/notifications/application:
commands.py
event_handlers.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/notifications/domain:
models.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/notifications/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/obras-publicas:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/obras-publicas/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/obras-publicas/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/operations:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/operations/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/operations/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/operations/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/application/services:
__init__.py
operations_service.py

/home/user/sila-system/apps/backend/app/modules/operations/domain:
entities
enums
enums.py
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
state_machine.py
value_objects

/home/user/sila-system/apps/backend/app/modules/operations/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/operations/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/operations/tests:
conftest.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/operations/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/operations/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/patrimonio-cultural:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/patrimonio-cultural/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/patrimonio-cultural/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/payment:
api
application
ARCHITECTURE.md
domain
governance.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/payment/api:
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/payment/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/payment/application/commands:
command_handlers.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/application/dto:
__init__.py
payment_schema.py

/home/user/sila-system/apps/backend/app/modules/payment/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/application/queries:
__init__.py
query_handlers.py

/home/user/sila-system/apps/backend/app/modules/payment/application/services:
__init__.py
payment_service.py
webhook_service.py

/home/user/sila-system/apps/backend/app/modules/payment/domain:
enums
events
exceptions.py
__init__.py
models
models.py
ports
repositories
repositories.py
services

/home/user/sila-system/apps/backend/app/modules/payment/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/payment/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/domain/models:
__init__.py
payment.py

/home/user/sila-system/apps/backend/app/modules/payment/domain/ports:
__init__.py
payment_provider_port.py
payment_repository_port.py

/home/user/sila-system/apps/backend/app/modules/payment/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/payment/infrastructure/adapters:
generic_payment_provider_adapter.py
__init__.py
multicaixa_provider.py
multicaixa_real_provider.py
sqlalchemy_payment_repository.py

/home/user/sila-system/apps/backend/app/modules/payment/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/payment/tests:
conftest.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/payment/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/payment/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/pecuaria:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/pecuaria/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/pecuaria/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/pescas:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/pescas/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/pescas/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/pescas-industriais:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/pescas-industriais/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/pescas-industriais/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/petroleo-gas:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/petroleo-gas/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/petroleo-gas/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/planeamento:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/planeamento/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/planeamento/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/portos-logistica:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/portos-logistica/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/portos-logistica/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/procurement:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/procurement/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/procurement/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/procurement/application/commands:
command_handlers.py
__init__.py
procurement_commands.py

/home/user/sila-system/apps/backend/app/modules/procurement/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/application/queries:
__init__.py
procurement_queries.py
query_handlers.py

/home/user/sila-system/apps/backend/app/modules/procurement/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain:
entities
enums
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/procurement/domain/entities:
bid.py
contract.py
__init__.py
supplier.py
tender.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/models:
bid.py
contract.py
enums.py
__init__.py
supplier.py
tender.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/ports:
bid_repository_port.py
contract_repository_port.py
economy_payment_port.py
__init__.py
supplier_repository_port.py
tender_repository_port.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/repositories:
contract_repository.py
__init__.py
supplier_repository.py
tender_repository.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/services:
__init__.py
procurement_engine.py

/home/user/sila-system/apps/backend/app/modules/procurement/domain/value_objects:
contract_status.py
__init__.py
procurement_method.py
tender_status.py

/home/user/sila-system/apps/backend/app/modules/procurement/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/procurement/infrastructure/adapters:
__init__.py
sqlalchemy_bid_repository.py
sqlalchemy_contract_repository.py
sqlalchemy_supplier_repository.py
sqlalchemy_tender_repository.py

/home/user/sila-system/apps/backend/app/modules/procurement/infrastructure/orm:
bid_model.py
contract_model.py
__init__.py
supplier_model.py
tender_model.py

/home/user/sila-system/apps/backend/app/modules/procurement/infrastructure/repositories:
contract_repository_impl.py
__init__.py
supplier_repository_impl.py
tender_repository_impl.py

/home/user/sila-system/apps/backend/app/modules/procurement/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
test_procurement_flow.py
unit

/home/user/sila-system/apps/backend/app/modules/procurement/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/procurement/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/procurement/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/procurement/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/protecao-civil:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/protecao-civil/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/protecao-civil/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/protecao-dados:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/protecao-dados/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/protecao-dados/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/public_security:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/public_security/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py
schemas

/home/user/sila-system/apps/backend/app/modules/public_security/api/endpoints:
cadeias_custodia.py
evidencias.py
__init__.py
investigacoes.py
laudos_periciais.py
mandados.py
ocorrencias.py
policiais.py
provas_periciais.py
unidades_policiais.py
vestigios.py

/home/user/sila-system/apps/backend/app/modules/public_security/api/schemas:
cadeia_custodia_schema.py
evidencia_schema.py
__init__.py
investigacao_schema.py
laudo_pericial_schema.py
mandado_schema.py
ocorrencia_schema.py
policial_schema.py
prova_pericial_schema.py
unidade_policial_schema.py
vestigio_schema.py

/home/user/sila-system/apps/backend/app/modules/public_security/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/public_security/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/application/ports:
cadeia_custodia_repository_port.py
evidencia_repository_port.py
__init__.py
investigacao_repository_port.py
laudo_pericial_repository_port.py
mandado_repository_port.py
ocorrencia_repository_port.py
policial_repository_port.py
prova_pericial_repository_port.py
request_service_port.py
unidade_policial_repository_port.py
vestigio_repository_port.py

/home/user/sila-system/apps/backend/app/modules/public_security/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/application/services:
cadeia_custodia_service.py
evidencia_service.py
__init__.py
investigacao_service.py
laudo_pericial_service.py
mandado_service.py
ocorrencia_service.py
policial_service.py
prova_pericial_service.py
unidade_policial_service.py
vestigio_service.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain:
entities
enums
enums.py
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/public_security/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/models:
cadeia_custodia.py
evidencia.py
__init__.py
investigacao.py
laudo_pericial.py
mandado.py
ocorrencia.py
policial.py
prova_pericial.py
unidade_policial.py
vestigio.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/infrastructure:
adapters
adapters.py
__init__.py
models
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/public_security/infrastructure/adapters:
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/public_security/infrastructure/models:
cadeia_custodia_model.py
evidencia_model.py
__init__.py
investigacao_model.py
laudo_pericial_model.py
mandado_model.py
ocorrencia_model.py
policial_model.py
prova_pericial_model.py
unidade_policial_model.py
vestigio_model.py

/home/user/sila-system/apps/backend/app/modules/public_security/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/infrastructure/repositories:
__init__.py
sqlalchemy_cadeia_custodia_repository.py
sqlalchemy_evidencia_repository.py
sqlalchemy_investigacao_repository.py
sqlalchemy_laudo_pericial_repository.py
sqlalchemy_mandado_repository.py
sqlalchemy_ocorrencia_repository.py
sqlalchemy_policial_repository.py
sqlalchemy_prova_pericial_repository.py
sqlalchemy_unidade_policial_repository.py
sqlalchemy_vestigio_repository.py

/home/user/sila-system/apps/backend/app/modules/public_security/tests:
api
application
conftest.py
domain
_fakes.py
infrastructure
__init__.py
integration
test_cadeias_custodia.py
test_evidencias.py
test_investigacoes.py
test_laudos_periciais.py
test_mandados.py
test_ocorrencias.py
test_orm_integration_real.py
test_policiais.py
test_provas_periciais.py
test_unidades_policiais.py
test_vestigios.py
unit

/home/user/sila-system/apps/backend/app/modules/public_security/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/public_security/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/public_security/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/public_security/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/recursos-minerais:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/recursos-minerais/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/recursos-minerais/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/registo-civil:
api
application
ARCHITECTURE.md
domain
governance.py
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/registo-civil/api:
health.py
__init__.py
router.py
routers.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/registo-civil/application:
__init__.py
services

/home/user/sila-system/apps/backend/app/modules/registo-civil/application/services:
__init__.py
registo_service.py

/home/user/sila-system/apps/backend/app/modules/registo-civil/domain:
enums
event_catalog.py
exceptions.py
__init__.py
models.py

/home/user/sila-system/apps/backend/app/modules/registo-civil/domain/enums:
__init__.py

/home/user/sila-system/apps/backend/app/modules/registo-civil/infrastructure:
adapters.py
adapters_real.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources:
agricultura
aguas_saneamento
ambiente
api
application
ARCHITECTURE.md
domain
florestas
infrastructure
__init__.py
module.yaml
pecuaria
pescas
petroleo_gas
recursos_minerais
seguranca_alimentar
tests

/home/user/sila-system/apps/backend/app/modules/resources/agricultura:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/api/endpoints:
assistencia.py
certificacoes.py
colheitas.py
comercializacao.py
creditos.py
culturas.py
equipamentos.py
estoques.py
fitossanidade.py
__init__.py
insumos.py
operacoes.py
plantios.py
produtores.py
propriedades.py
safras.py
talhoes.py
zoneamento.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/api/schemas:
assistencia_schema.py
certificacao_schema.py
colheita_schema.py
comercializacao_schema.py
credito_schema.py
cultura_schema.py
equipamento_schema.py
estoque_schema.py
__init__.py
insumo_schema.py
ocorrencia_schema.py
operacao_schema.py
plantio_schema.py
produtor_schema.py
propriedade_schema.py
safra_schema.py
talhao_schema.py
zoneamento_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/application/ports:
assistencia_repository_port.py
certificacao_repository_port.py
citizen_service_port.py
comercializacao_repository_port.py
credito_repository_port.py
cultura_repository_port.py
estoque_repository_port.py
financas_service_port.py
__init__.py
insumo_repository_port.py
ocorrencia_repository_port.py
operacao_repository_port.py
produtor_repository_port.py
propriedade_repository_port.py
request_service_port.py
safra_repository_port.py
zoneamento_repository_port.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/application/services:
assistencia_service.py
certificacao_service.py
colheita_service.py
comercializacao_service.py
credito_service.py
equipamento_service.py
estoque_service.py
fitossanidade_service.py
__init__.py
insumo_service.py
operacao_service.py
plantio_service.py
producao_service.py
produtor_service.py
propriedade_service.py
safra_service.py
talhao_service.py
zoneamento_service.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/domain/models:
assistencia_tecnica.py
cadastro_ambiental.py
certificacao.py
colheita.py
comercializacao.py
credito_rural.py
cultura.py
equipamento.py
estoque.py
__init__.py
insumo.py
ocorrencia_fitossanitaria.py
operacao.py
plantio.py
produtor.py
propriedade_rural.py
safra.py
talhao.py
zoneamento.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/infrastructure/adapters:
citizen_service_adapter.py
financas_service_adapter.py
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/infrastructure/models:
assistencia_model.py
certificacao_model.py
comercializacao_model.py
credito_model.py
cultura_model.py
equipamento_model.py
estoque_model.py
__init__.py
insumo_model.py
ocorrencia_model.py
operacao_model.py
produtor_model.py
propriedade_model.py
safra_model.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/infrastructure/repositories:
__init__.py
sqlalchemy_assistencia_repository.py
sqlalchemy_certificacao_repository.py
sqlalchemy_comercializacao_repository.py
sqlalchemy_credito_repository.py
sqlalchemy_cultura_repository.py
sqlalchemy_estoque_repository.py
sqlalchemy_insumo_repository.py
sqlalchemy_ocorrencia_repository.py
sqlalchemy_operacao_repository.py
sqlalchemy_produtor_repository.py
sqlalchemy_propriedade_repository.py
sqlalchemy_safra_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/agricultura/tests:
__init__.py
test_assistencia.py
test_certificacoes.py
test_colheitas.py
test_comercializacao.py
test_creditos.py
test_culturas.py
test_entidades_derivadas.py
test_equipamentos.py
test_estoques.py
test_fitossanidade.py
test_insumos.py
test_operacoes.py
test_plantios.py
test_produtores.py
test_propriedades.py
test_safras.py
test_talhoes.py
test_zoneamento.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests
workers

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/api/endpoints:
abastecimento.py
consumo.py
faturas.py
infraestrutura.py
__init__.py
outorgas.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/api/schemas:
abastecimento_schema.py
consumo_schema.py
fatura_schema.py
infraestrutura_schema.py
__init__.py
outorga_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/application:
bus.py
events
handlers
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/application/events:
fatura_events.py
__init__.py
registry.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/application/handlers:
financas_integration_handler.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/application/ports:
abastecimento_repository_port.py
ambiente_service_port.py
citizen_service_port.py
consumo_repository_port.py
fatura_repository_port.py
financas_gateway_port.py
geosampa_service_port.py
infraestrutura_repository_port.py
__init__.py
outbox_repository_port.py
outorga_repository_port.py
request_service_port.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/application/services:
abastecimento_service.py
consumo_service.py
faturamento_service.py
infraestrutura_service.py
__init__.py
outorga_service.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/domain/models:
abastecimento.py
consumo_agua.py
fatura_agua.py
infraestrutura.py
__init__.py
outorga.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/infrastructure:
adapters
__init__.py
models
persistence
repositories
repository.py
resilience

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/infrastructure/adapters:
ambiente_service_adapter.py
citizen_service_adapter.py
financas_gateway.py
geosampa_service_adapter.py
__init__.py
message_publishers.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/infrastructure/models:
abastecimento_model.py
consumo_model.py
fatura_model.py
infraestrutura_model.py
__init__.py
outbox_event_model.py
outorga_model.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/infrastructure/persistence:
__init__.py
outbox.py
repository.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/infrastructure/repositories:
__init__.py
sqlalchemy_abastecimento_repository.py
sqlalchemy_consumo_repository.py
sqlalchemy_fatura_repository.py
sqlalchemy_infraestrutura_repository.py
sqlalchemy_outorga_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/infrastructure/resilience:
circuit.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/tests:
__init__.py
test_abastecimento.py
test_consumo.py
test_faturamento_eventos.py
test_faturamento.py
test_financas_gateway_publisher.py
test_infraestrutura.py
test_outbox_sqlalchemy_integration.py
test_outorgas.py

/home/user/sila-system/apps/backend/app/modules/resources/aguas_saneamento/workers:
__init__.py
outbox_worker.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/api/endpoints:
autos_infracao.py
car.py
condicionantes.py
embargos.py
estudos.py
fiscalizacoes.py
__init__.py
licencas.py
multas.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/api/schemas:
auto_infracao_schema.py
car_schema.py
condicionante_schema.py
embargo_schema.py
estudo_schema.py
fiscalizacao_schema.py
__init__.py
licenca_schema.py
multa_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/application/ports:
agricultura_service_port.py
auto_infracao_repository_port.py
car_repository_port.py
citizen_service_port.py
condicionante_repository_port.py
embargo_repository_port.py
estudo_repository_port.py
fiscalizacao_repository_port.py
geosampa_service_port.py
imovel_repository_port.py
__init__.py
licenca_repository_port.py
multa_repository_port.py
proprietario_repository_port.py
request_service_port.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/application/services:
cadastro_service.py
condicionante_service.py
estudo_service.py
fiscalizacao_service.py
__init__.py
licenciamento_service.py
penalidade_service.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/domain/models:
auto_infracao.py
car.py
condicionante.py
eia.py
embargo.py
estudo_impacto.py
fiscalizacao.py
imovel_rural.py
__init__.py
licenca_ambiental.py
licenca_instalacao.py
licenca_operacao.py
licenca_previa.py
licenca_unica.py
multa.py
proprietario.py
rima.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/infrastructure/adapters:
agricultura_service_adapter.py
citizen_service_adapter.py
geosampa_service_adapter.py
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/infrastructure/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/infrastructure/repositories:
__init__.py
sqlalchemy_auto_infracao_repository.py
sqlalchemy_car_repository.py
sqlalchemy_condicionante_repository.py
sqlalchemy_embargo_repository.py
sqlalchemy_estudo_repository.py
sqlalchemy_fiscalizacao_repository.py
sqlalchemy_imovel_repository.py
sqlalchemy_licenca_repository.py
sqlalchemy_multa_repository.py
sqlalchemy_proprietario_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/ambiente/tests:
__init__.py
test_car.py
test_estudos.py
test_fiscalizacao.py
test_licenciamento.py
test_penalidades.py

/home/user/sila-system/apps/backend/app/modules/resources/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/resources/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/resources/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain:
entities
enums
events
exceptions.py
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/resources/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/florestas/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/florestas/api/endpoints:
alertas_desmatamento.py
apreensoes_madeira.py
autorizacoes_supressao.py
autos_infracao_florestais.py
car_florestal.py
certificacoes_florestais.py
combates_incendio.py
comercializacao_florestal.py
comunidades.py
concessoes_florestais.py
cras.py
creditos_carbono.py
desmatamentos_ilegais.py
dofs.py
embargos_florestais.py
empresas_florestais.py
especies_florestais.py
estatisticas_florestais.py
exploracoes.py
exportacoes_madeira.py
fiscalizacoes_florestais.py
focos_calor.py
incendios_florestais.py
__init__.py
inventarios.py
licencas_manejo.py
madeiras.py
monitoramentos_satelite.py
multas_florestais.py
ocorrencias_incendio.py
operadores_florestais.py
outorgas_florestais.py
planos_manejo.py
pnfms.py
produtos_florestais.py
projetos_carbono.py
recuperacoes_area.py
redds.py
reflorestamentos.py
reposicoes_florestais.py
reservas_legais.py
talhoes.py
unidades_manejo.py
viveiros.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/api/schemas:
alerta_desmatamento_schema.py
apreensao_madeira_schema.py
arvore_schema.py
auto_infracao_florestal_schema.py
autorizacao_supressao_schema.py
car_schema.py
certificacao_florestal_schema.py
combate_incendio_schema.py
comercializacao_florestal_schema.py
comunidade_schema.py
concessao_florestal_schema.py
cra_schema.py
credito_carbono_schema.py
desmatamento_ilegal_schema.py
dof_schema.py
embargo_florestal_schema.py
empresa_florestal_schema.py
especie_florestal_schema.py
estatistica_florestal_schema.py
exploracao_florestal_schema.py
exportacao_madeira_schema.py
foco_calor_schema.py
incendio_florestal_schema.py
__init__.py
inventario_florestal_schema.py
licenca_manejo_schema.py
madeira_schema.py
monitoramento_satelite_schema.py
multa_florestal_schema.py
ocorrencia_incendio_schema.py
operador_florestal_schema.py
outorga_florestal_schema.py
plano_manejo_florestal_schema.py
pnfm_schema.py
produto_florestal_schema.py
projeto_carbono_schema.py
recuperacao_area_schema.py
redd_schema.py
reflorestamento_schema.py
reposicao_florestal_schema.py
reserva_legal_schema.py
talhao_florestal_schema.py
unidade_manejo_schema.py
viveiro_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/resources/florestas/application/ports:
agricultura_service_port.py
alerta_desmatamento_repository_port.py
ambiente_service_port.py
apreensao_madeira_repository_port.py
arvore_repository_port.py
auto_infracao_florestal_repository_port.py
autorizacao_supressao_repository_port.py
car_repository_port.py
certificacao_florestal_repository_port.py
citizen_service_port.py
combate_incendio_repository_port.py
comercializacao_florestal_repository_port.py
comercio_externo_service_port.py
comunidade_repository_port.py
concessao_florestal_repository_port.py
concessionario_florestal_repository_port.py
cra_repository_port.py
credito_carbono_repository_port.py
desmatamento_ilegal_repository_port.py
dof_repository_port.py
embargo_florestal_repository_port.py
empresa_florestal_repository_port.py
energia_service_port.py
especie_florestal_repository_port.py
estatistica_florestal_repository_port.py
exploracao_florestal_repository_port.py
exportacao_madeira_repository_port.py
fiscalizacao_florestal_repository_port.py
foco_calor_repository_port.py
geosampa_service_port.py
gestao_fundiaria_service_port.py
incendio_florestal_repository_port.py
__init__.py
inventario_florestal_repository_port.py
licenca_manejo_repository_port.py
madeira_repository_port.py
monitoramento_satelite_repository_port.py
multa_florestal_repository_port.py
ocorrencia_incendio_repository_port.py
outorga_florestal_repository_port.py
plano_manejo_florestal_repository_port.py
pnfm_repository_port.py
produto_florestal_repository_port.py
projeto_carbono_repository_port.py
recuperacao_area_repository_port.py
redd_repository_port.py
reflorestamento_repository_port.py
reposicao_florestal_repository_port.py
request_service_port.py
reserva_legal_repository_port.py
talhao_florestal_repository_port.py
unidade_manejo_repository_port.py
viveiro_repository_port.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/application/services:
car_florestal_service.py
certificacao_florestal_service.py
comercializacao_florestal_service.py
concessao_florestal_service.py
credito_carbono_service.py
desmatamento_service.py
dof_service.py
estatistica_florestal_service.py
exploracao_service.py
exportacao_florestal_service.py
fiscalizacao_florestal_service.py
incendio_service.py
__init__.py
inventario_service.py
licenciamento_florestal_service.py
manejo_service.py
monitoramento_fogo_service.py
operador_florestal_service.py
penalidade_florestal_service.py
plano_manejo_service.py
produto_florestal_service.py
recuperacao_service.py
redd_service.py
reflorestamento_service.py
reposicao_service.py
reserva_legal_service.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/florestas/domain/models:
aceiro.py
alerta_desmatamento.py
altura_comercial.py
app.py
apreensao_madeira.py
area_concedida.py
area_desmatada.py
area_manejada.py
area_queimada.py
area_recuperada.py
area_reflorestada.py
arraste.py
arvore.py
assentamento.py
asv.py
auto_infracao_florestal.py
autorizacao_supressao.py
biomassa.py
borracha.py
brigada.py
cadastro_ambiental_rural.py
carbono.py
car.py
carvao.py
castanha.py
censo_florestal.py
cerflor.py
certificacao_florestal.py
ciclo_corte.py
combate_incendio.py
comercializacao_florestal.py
compensados.py
comunidade_tradicional.py
concessao_florestal.py
concessionario_florestal.py
corte_seletivo.py
cota_reserva_ambiental.py
cra.py
credito_carbono.py
dap.py
depósito_madeira.py
desmatamento_ilegal.py
deter.py
doação_madeira.py
documento_origem_florestal.py
dof.py
embargo_florestal.py
empresa_florestal.py
especie_florestal.py
estatistica_florestal.py
estoque_carbono.py
exploracao_florestal.py
exportacao_madeira.py
extração.py
fiscalizacao_florestal.py
foco_calor.py
frutos.py
fsc.py
guia_transporte_florestal.py
importacao_madeira.py
incêndio_florestal.py
__init__.py
inventario_florestal.py
iso_14001.py
laminados.py
leilão_madeira.py
lenha.py
licenca_manejo.py
madeira_serrada.py
monitoramento_satelite.py
muda.py
multa_florestal.py
nota_fiscal_florestal.py
ocorrencia_incendio.py
óleos_essenciais.py
outorga_florestal.py
parcela.py
pefc.py
plano_manejo_florestal.py
plantas_medicinais.py
plantio.py
pmfs.py
pnfm.py
prodes.py
produção_madeireira.py
produção_nao_madeireira.py
produtos_nao_madeireiros.py
projeto_carbono.py
rad.py
recuperacao_area_degradada.py
redd.py
reflorestamento.py
reposicao_florestal.py
reserva_legal.py
resina.py
semente_florestal.py
servidao_ambiental.py
talhao_florestal.py
termo_apreensao.py
toras.py
unidade_manejo.py
verificacao_carbono.py
viveiro.py
volume_madeira.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/resources/florestas/infrastructure/adapters:
agricultura_service_adapter.py
ambiente_service_adapter.py
citizen_service_adapter.py
comercio_externo_service_adapter.py
energia_service_adapter.py
geosampa_service_adapter.py
gestao_fundiaria_service_adapter.py
__init__.py
_integration_runtime.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/infrastructure/models:
alerta_desmatamento_model.py
arvore_model.py
auto_infracao_florestal_model.py
autorizacao_supressao_model.py
certificacao_florestal_model.py
concessao_florestal_model.py
cra_model.py
credito_carbono_model.py
desmatamento_ilegal_model.py
dof_model.py
especie_florestal_model.py
exploracao_florestal_model.py
fiscalizacao_florestal_model.py
foco_calor_model.py
incendio_florestal_model.py
__init__.py
inventario_florestal_model.py
licenca_manejo_model.py
madeira_model.py
monitoramento_satelite_model.py
operador_florestal_model.py
plano_manejo_florestal_model.py
produto_florestal_model.py
unidade_manejo_model.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/infrastructure/repositories:
__init__.py
sqlalchemy_alerta_desmatamento_repository.py
sqlalchemy_auto_infracao_florestal_repository.py
sqlalchemy_autorizacao_supressao_repository.py
sqlalchemy_certificacao_florestal_repository.py
sqlalchemy_concessao_florestal_repository.py
sqlalchemy_cra_repository.py
sqlalchemy_credito_carbono_repository.py
sqlalchemy_desmatamento_ilegal_repository.py
sqlalchemy_dof_repository.py
sqlalchemy_especie_florestal_repository.py
sqlalchemy_exploracao_florestal_repository.py
sqlalchemy_fiscalizacao_florestal_repository.py
sqlalchemy_foco_calor_repository.py
sqlalchemy_incendio_florestal_repository.py
sqlalchemy_inventario_florestal_repository.py
sqlalchemy_licenca_manejo_repository.py
sqlalchemy_monitoramento_satelite_repository.py
sqlalchemy_operador_florestal_repository.py
sqlalchemy_plano_manejo_florestal_repository.py
sqlalchemy_produto_florestal_repository.py
sqlalchemy_unidade_manejo_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/florestas/tests:
__init__.py
test_alertas.py
test_autorizacoes_supressao.py
test_autos_infracao.py
test_certificacoes.py
test_concessoes.py
test_cras.py
test_creditos_carbono.py
test_desmatamentos.py
test_dofs.py
test_exploracoes.py
test_fiscalizacoes.py
test_focos_calor.py
test_incendios.py
test_inventarios.py
test_licencas_manejo.py
test_monitoramento.py
test_operadores_florestais.py
test_planos_manejo.py
test_produtos_florestais.py
test_unidades_manejo.py

/home/user/sila-system/apps/backend/app/modules/resources/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/resources/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/api/endpoints:
animais.py
__init__.py
pecuaristas.py
producao.py
propriedades.py
rebanhos.py
sanidade.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/api/schemas:
animal_schema.py
__init__.py
pecuarista_schema.py
producao_schema.py
propriedade_schema.py
rebanho_schema.py
sanidade_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/application/ports:
agricultura_service_port.py
ambiente_service_port.py
animal_repository_port.py
citizen_service_port.py
gestao_fundiaria_service_port.py
__init__.py
pecuarista_repository_port.py
producao_repository_port.py
propriedade_pecuaria_repository_port.py
rastreabilidade_repository_port.py
rebanho_repository_port.py
reproducao_repository_port.py
request_service_port.py
sanidade_repository_port.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/application/services:
animal_service.py
__init__.py
pecuarista_service.py
producao_service.py
propriedade_service.py
rebanho_service.py
reproducao_service.py
sanidade_service.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/domain/models:
alimentacao.py
animal.py
bovino.py
caprino.py
comercializacao.py
equino.py
__init__.py
inseminacao.py
instalacao.py
medicamento.py
ovino.py
parto.py
pasto.py
pecuarista.py
producao_carne.py
producao_leite.py
propriedade_pecuaria.py
raca.py
rastreabilidade.py
rebanho.py
reproducao.py
suino.py
vacina.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/infrastructure/adapters:
agricultura_service_adapter.py
ambiente_service_adapter.py
citizen_service_adapter.py
gestao_fundiaria_service_adapter.py
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/infrastructure/models:
animal_model.py
__init__.py
pecuarista_model.py
producao_leite_model.py
propriedade_pecuaria_model.py
rebanho_model.py
vacina_model.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/infrastructure/repositories:
__init__.py
sqlalchemy_animal_repository.py
sqlalchemy_pecuarista_repository.py
sqlalchemy_propriedade_pecuaria_repository.py
sqlalchemy_rebanho_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/pecuaria/tests:
__init__.py
test_animais.py
test_pecuaristas.py
test_propriedades.py
test_rebanhos.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas:
api
application
ARCHITECTURE.md
domain
industrial
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/pescas/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/pescas/api/endpoints:
armadores.py
capturas.py
comercializacao.py
defesos.py
desembarques.py
embarcacoes.py
especies.py
fiscalizacao.py
__init__.py
licencas_pesca.py
pescadores.py
producao.py
quotas.py
rastreabilidade.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/api/schemas:
armador_schema.py
captura_schema.py
defeso_schema.py
desembarque_schema.py
embarcacao_schema.py
especie_schema.py
fiscalizacao_schema.py
__init__.py
licenca_pesca_schema.py
pescador_schema.py
producao_schema.py
quota_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/resources/pescas/application/ports:
ambiente_service_port.py
armador_repository_port.py
captura_repository_port.py
citizen_service_port.py
comercializacao_pesca_repository_port.py
comercio_externo_service_port.py
defeso_repository_port.py
desembarque_repository_port.py
embarcacao_repository_port.py
especie_repository_port.py
fiscalizacao_pesca_repository_port.py
geosampa_service_port.py
__init__.py
licenca_pesca_repository_port.py
pescador_repository_port.py
producao_pesca_repository_port.py
quota_repository_port.py
rastreabilidade_pesca_repository_port.py
request_service_port.py
transportes_logistica_service_port.py
zona_pesca_repository_port.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/application/services:
armador_service.py
captura_service.py
comercializacao_service.py
defeso_service.py
desembarque_service.py
embarcacao_service.py
fiscalizacao_service.py
__init__.py
licenciamento_pesca_service.py
pescador_service.py
producao_pesca_service.py
quota_service.py
rastreabilidade_service.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/pescas/domain/models:
apreensao_embarcacao.py
area_pesca.py
armador.py
arte_pesca.py
auto_infracao_pesca.py
autorizacao_pesca.py
beneficiamento.py
bitola_minima.py
cadeia_frio.py
captura.py
certificado_origem_pesca.py
comercializacao_pesca.py
cooperativa_pesca.py
defeso.py
desembarque.py
embarcacao.py
embargo_pesca.py
empresa_pesca.py
especie.py
estatistica_pesca.py
exportacao_pesca.py
fiscalizacao_pesca.py
frigorifico.py
importacao_pesca.py
industria_pesca.py
__init__.py
inspecao_sanitaria_pesca.py
laboratorio_qualidade.py
licenca_pesca.py
monitoramento_satelite.py
multa_pesca.py
observador_bordo.py
periodo_defeso.py
permissao_pesca.py
pescador.py
pesquisa_pesqueira.py
petrecho.py
producao_pesca.py
quota.py
rastreabilidade_pesca.py
recurso_pesqueiro.py
safra.py
sistema_rastreamento.py
tamanho_minimo_captura.py
tipo_embarcacao.py
vms.py
zona_pesca.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial:
api
application
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/api/endpoints:
armadores_industriais.py
certificacoes.py
embarcacoes_industriais.py
estatisticas.py
exportacoes_industriais.py
frigorificos.py
__init__.py
inspecoes_sanitarias.py
licencas_operacao.py
lotes_producao.py
produtos_processados.py
rastreabilidade.py
unidades_processamento.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/api/schemas:
armador_industrial_schema.py
certificacao_schema.py
embarcacao_industrial_schema.py
exportacao_industrial_schema.py
frigorifico_schema.py
__init__.py
inspecao_schema.py
lote_producao_schema.py
produto_processado_schema.py
rastreabilidade_schema.py
unidade_processamento_schema.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/application/ports:
ambiente_service_port.py
armador_industrial_repository_port.py
certificacao_industrial_repository_port.py
citizen_service_port.py
comercio_externo_service_port.py
embarcacao_industrial_repository_port.py
estatistica_industrial_repository_port.py
exportacao_industrial_repository_port.py
frigorifico_industrial_repository_port.py
geosampa_service_port.py
industria_service_port.py
__init__.py
inspecao_sanitaria_industrial_repository_port.py
licenca_operacao_industrial_repository_port.py
lote_producao_repository_port.py
pescas_service_port.py
produto_processado_repository_port.py
rastreabilidade_industrial_repository_port.py
request_service_port.py
unidade_processamento_repository_port.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/application/services:
armador_industrial_service.py
certificacao_industrial_service.py
embarcacao_industrial_service.py
estatistica_industrial_service.py
exportacao_industrial_service.py
frigorifico_service.py
__init__.py
inspecao_industrial_service.py
licenciamento_industrial_service.py
lote_producao_service.py
produto_processado_service.py
qualidade_industrial_service.py
rastreabilidade_industrial_service.py
unidade_processamento_service.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/domain:
entities.py
enums.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/domain/models:
alvara_sanitario_industrial.py
armador_industrial.py
auto_infracao_industrial.py
cadeia_frio_industrial.py
capacidade_processamento.py
certificacao_industrial.py
cold_storage.py
congelado.py
conserva.py
container_reefer.py
controle_qualidade_industrial.py
defumado.py
embarcacao_industrial.py
embargo_industrial.py
enlatado.py
entressafra.py
estatistica_industrial.py
exportacao_industrial.py
farinha_pescado.py
filetagem.py
frigorifico_industrial.py
haccp.py
__init__.py
inspecao_sanitaria_industrial.py
interdicao_industrial.py
iso_22000.py
laboratorio_industrial.py
licenca_operacao_industrial.py
linha_processamento.py
lote_producao.py
ociosidade.py
oleo_peixe.py
outorga_industrial.py
produtividade_industrial.py
produto_processado.py
rastreabilidade_industrial.py
relatorio_producao.py
residuo_industrial.py
safra_industrial.py
salgado.py
seco.py
selo_inspecao.py
sie.py
sif.py
sim.py
subproduto.py
unidade_processamento.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/infrastructure/adapters:
ambiente_service_adapter.py
citizen_service_adapter.py
comercio_externo_service_adapter.py
geosampa_service_adapter.py
industria_service_adapter.py
__init__.py
pescas_service_adapter.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/infrastructure/models:
frigorifico_model.py
__init__.py
inspecao_model.py
lote_producao_model.py
produto_processado_model.py
rastreabilidade_model.py
unidade_processamento_model.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/infrastructure/repositories:
__init__.py
sqlalchemy_frigorifico_repository.py
sqlalchemy_inspecao_repository.py
sqlalchemy_lote_producao_repository.py
sqlalchemy_produto_processado_repository.py
sqlalchemy_unidade_processamento_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/industrial/tests:
_fakes.py
__init__.py
test_inspecoes.py
test_lotes.py
test_orm_integration_real.py
test_produtos_processados.py
test_unidades_processamento.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/resources/pescas/infrastructure/adapters:
ambiente_service_adapter.py
citizen_service_adapter.py
comercio_externo_service_adapter.py
geosampa_service_adapter.py
__init__.py
request_service_adapter.py
transportes_logistica_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/infrastructure/models:
armador_model.py
captura_model.py
desembarque_model.py
embarcacao_model.py
especie_model.py
__init__.py
licenca_pesca_model.py
pescador_model.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/infrastructure/repositories:
__init__.py
sqlalchemy_captura_repository.py
sqlalchemy_embarcacao_repository.py
sqlalchemy_licenca_pesca_repository.py
sqlalchemy_pescador_repository.py

/home/user/sila-system/apps/backend/app/modules/resources/pescas/tests:
__init__.py
test_capturas.py
test_embarcacoes.py
test_licencas.py
test_pescadores.py

/home/user/sila-system/apps/backend/app/modules/resources/petroleo_gas:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/petroleo_gas/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/resources/petroleo_gas/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/resources/petroleo_gas/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/petroleo_gas/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/resources/petroleo_gas/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/recursos_minerais:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/recursos_minerais/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/resources/recursos_minerais/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/resources/recursos_minerais/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/recursos_minerais/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/resources/recursos_minerais/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/seguranca_alimentar:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/resources/seguranca_alimentar/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/resources/seguranca_alimentar/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/resources/seguranca_alimentar/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/seguranca_alimentar/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/resources/seguranca_alimentar/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/resources/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/resources/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/resources/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/resources/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/saude:
api
application
ARCHITECTURE.md
domain
governance.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/saude/api:
deps.py
endpoints
health.py
__init__.py
router.py
routers.py
v1

/home/user/sila-system/apps/backend/app/modules/saude/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/api/v1:
endpoints.py
__init__.py
schemas.py

/home/user/sila-system/apps/backend/app/modules/saude/application:
clinical
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services
vaccine

/home/user/sila-system/apps/backend/app/modules/saude/application/clinical:
exame_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/application/ports:
appointment_repository_port.py
health_unit_repository_port.py
__init__.py
juventude_service_port.py
workflow_service_port.py

/home/user/sila-system/apps/backend/app/modules/saude/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/application/vaccine:
__init__.py
vaccine_service.py

/home/user/sila-system/apps/backend/app/modules/saude/domain:
entities
enums
enums.py
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/saude/domain/entities:
__init__.py
medical_record.py
prescription.py
vaccine.py
vigilancia_epidemiologica.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/infrastructure:
adapters
adapters.py
external_apis
__init__.py
models.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/saude/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/infrastructure/external_apis:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/saude/infrastructure/repositories:
appointment_repository.py
health_unit_repository.py
__init__.py
medical_record_repository.py

/home/user/sila-system/apps/backend/app/modules/saude/tests:
conftest.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/saude/tests/integration:
__init__.py
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/saude/tests/unit:
__init__.py
test_domain.py

/home/user/sila-system/apps/backend/app/modules/_scaffold:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/_scaffold/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/_scaffold/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/seguranca-alimentar:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/seguranca-alimentar/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/seguranca-alimentar/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/seguranca-publica:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/seguranca-publica/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/seguranca-publica/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/seguranca-social:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/seguranca-social/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/seguranca-social/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/society:
api
application
ARCHITECTURE.md
assistencia_social
cultura
desporto
domain
educacao
emprego
familia
igualdade
infrastructure
__init__.py
juventude
module.yaml
patrimonio_cultural
seguranca_social
tests
trabalho_inspecao

/home/user/sila-system/apps/backend/app/modules/society/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/society/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/society/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social:
api
application
ARCHITECTURE.md
domain
handlers.py
infrastructure
__init__.py
module.yaml
tests
workflows

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/api/endpoints:
atendimentos.py
beneficiarios.py
beneficios.py
cadastros_unicos.py
criancas_risco.py
_errors.py
idosos_vulneraveis.py
__init__.py
pcd.py
programas_sociais.py
situacoes_rua.py
visitas_domiciliares.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/api/schemas:
atendimento_schema.py
beneficiario_schema.py
beneficio_schema.py
cadastro_unico_schema.py
crianca_risco_schema.py
idoso_vulneravel_schema.py
__init__.py
pcd_schema.py
programa_social_schema.py
situacao_rua_schema.py
visita_domiciliar_schema.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/application/ports:
atendimento_repository_port.py
beneficiario_repository_port.py
beneficio_repository_port.py
cadastro_unico_repository_port.py
crianca_risco_repository_port.py
idoso_vulneravel_repository_port.py
__init__.py
pcd_repository_port.py
programa_social_repository_port.py
services_port
situacao_rua_repository_port.py
visita_domiciliar_repository_port.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/application/ports/services_port:
citizen_service_port.py
educacao_service_port.py
emprego_service_port.py
__init__.py
juventude_service_port.py
request_service_port.py
saude_service_port.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/application/services:
atendimento_service.py
beneficiario_service.py
beneficio_service.py
cadastro_unico_service.py
_codegen.py
crianca_risco_service.py
idoso_vulneravel_service.py
__init__.py
pcd_service.py
programa_social_service.py
situacao_rua_service.py
visita_domiciliar_service.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/domain/models:
atendimento.py
beneficiario.py
beneficio.py
cadastro_unico.py
crianca_risco.py
idoso_vulneravel.py
__init__.py
pessoa_com_deficiencia.py
programa_social.py
situacao_rua.py
visita_domiciliar.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/infrastructure/adapters:
citizen_service_adapter.py
educacao_service_adapter.py
emprego_service_adapter.py
__init__.py
juventude_service_adapter.py
request_service_adapter.py
saude_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/infrastructure/models:
atendimento_model.py
beneficiario_model.py
beneficio_model.py
cadastro_unico_model.py
crianca_risco_model.py
idoso_vulneravel_model.py
__init__.py
pcd_model.py
programa_social_model.py
situacao_rua_model.py
visita_domiciliar_model.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/infrastructure/repositories:
__init__.py
sqlalchemy_atendimento_repository.py
sqlalchemy_beneficiario_repository.py
sqlalchemy_beneficio_repository.py
sqlalchemy_cadastro_unico_repository.py
sqlalchemy_crianca_risco_repository.py
sqlalchemy_idoso_vulneravel_repository.py
sqlalchemy_pcd_repository.py
sqlalchemy_programa_social_repository.py
sqlalchemy_situacao_rua_repository.py
sqlalchemy_visita_domiciliar_repository.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/tests:
e2e
_fakes.py
__init__.py
test_atendimento.py
test_beneficiario.py
test_beneficio_bpc_pcd.py
test_cadastro_unico.py
test_crianca_risco.py
test_endpoints.py
test_fluxo_completo_assistencia.py
test_idoso_vulneravel.py
test_orm_integration_real.py
test_pcd.py
test_programa_social.py
test_situacao_rua.py
test_visita_domiciliar.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/tests/e2e:
test_00_generate_evidence.py
test_01_beneficio_success_e2e.py
test_02_beneficio_reject_e2e.py
test_03_beneficio_cancel_e2e.py

/home/user/sila-system/apps/backend/app/modules/society/assistencia_social/workflows:
beneficio_workflow.py

/home/user/sila-system/apps/backend/app/modules/society/cultura:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests
workers

/home/user/sila-system/apps/backend/app/modules/society/cultura/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/cultura/api/endpoints:
artistas.py
bens_culturais.py
editais.py
espacos_culturais.py
eventos_culturais.py
grupos_artisticos.py
__init__.py
patrimonios_imateriais.py
projetos_culturais.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/api/schemas:
artista_schema.py
bem_cultural_schema.py
edital_schema.py
espaco_cultural_schema.py
evento_cultural_schema.py
grupo_artistico_schema.py
__init__.py
patrimonio_imaterial_schema.py
projeto_cultural_schema.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/application:
events
handlers
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/society/cultura/application/events:
bus.py
definitions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/application/handlers:
ecad_handler.py
__init__.py
iphan_handler.py
minc_handler.py
turismo_handler.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/application/ports:
arquivo_nacional_service_port.py
artista_repository_port.py
bem_cultural_repository_port.py
citizen_service_port.py
edital_repository_port.py
educacao_service_port.py
espaco_cultural_repository_port.py
evento_cultural_repository_port.py
grupo_artistico_repository_port.py
__init__.py
patrimonio_imaterial_repository_port.py
projeto_cultural_repository_port.py
request_service_port.py
turismo_service_port.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/application/services:
artista_service.py
bem_cultural_service.py
edital_service.py
espaco_cultural_service.py
evento_cultural_service.py
grupo_artistico_service.py
__init__.py
patrimonio_imaterial_service.py
projeto_cultural_service.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/society/cultura/domain/models:
artista.py
bem_cultural.py
edital.py
espaco_cultural.py
evento_cultural.py
grupo_artistico.py
__init__.py
patrimonio_imaterial.py
projeto_cultural.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/infrastructure:
adapters
__init__.py
models
persistence
repositories
resilience

/home/user/sila-system/apps/backend/app/modules/society/cultura/infrastructure/adapters:
arquivo_nacional_service_adapter.py
citizen_service_adapter.py
ecad_adapter.py
educacao_service_adapter.py
funcultura_adapter.py
__init__.py
iphan_adapter.py
minc_adapter.py
request_service_adapter.py
sav_adapter.py
turismo_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/infrastructure/models:
artista_model.py
bem_cultural_model.py
edital_model.py
espaco_cultural_model.py
evento_cultural_model.py
grupo_artistico_model.py
__init__.py
patrimonio_imaterial_model.py
projeto_cultural_model.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/infrastructure/persistence:
__init__.py
outbox.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/infrastructure/repositories:
__init__.py
sqlalchemy_artista_repository.py
sqlalchemy_bem_cultural_repository.py
sqlalchemy_edital_repository.py
sqlalchemy_espaco_cultural_repository.py
sqlalchemy_evento_cultural_repository.py
sqlalchemy_grupo_artistico_repository.py
sqlalchemy_patrimonio_imaterial_repository.py
sqlalchemy_projeto_cultural_repository.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/infrastructure/resilience:
circuit_breaker.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/tests:
_fakes.py
__init__.py
test_artistas.py
test_bens_culturais.py
test_editais.py
test_espacos_culturais.py
test_eventos_culturais.py
test_grupos_artisticos.py
test_integracao_iphan.py
test_orm_integration_real.py
test_patrimonios_imateriais.py
test_projetos_culturais.py

/home/user/sila-system/apps/backend/app/modules/society/cultura/workers:
edital_worker.py
__init__.py
outbox_worker.py
patrimonio_worker.py

/home/user/sila-system/apps/backend/app/modules/society/desporto:
api
application
ARCHITECTURE.md
config.py
domain
events
infrastructure
__init__.py
module.yaml
resilience
tests
workers

/home/user/sila-system/apps/backend/app/modules/society/desporto/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/desporto/api/endpoints:
atletas.py
clubes.py
competicoes.py
estadios.py
__init__.py
jogos.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/api/schemas:
atleta_schema.py
clube_schema.py
competicao_schema.py
estadio_schema.py
__init__.py
jogo_schema.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/application:
events
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/society/desporto/application/events:
bus.py
definitions.py
__init__.py
registry.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/application/ports:
atleta_repository_port.py
citizen_service_port.py
clube_repository_port.py
competicao_repository_port.py
contrato_repository_port.py
educacao_service_port.py
estadio_repository_port.py
federacao_service_port.py
__init__.py
jogo_repository_port.py
obras_publicas_service_port.py
outbox_repository_port.py
request_service_port.py
saude_service_port.py
transferencia_repository_port.py
turismo_service_port.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/application/services:
atleta_service.py
clube_service.py
competicao_service.py
estadio_service.py
__init__.py
jogo_service.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/domain:
enums.py
exceptions.py
__init__.py
models
value_objects

/home/user/sila-system/apps/backend/app/modules/society/desporto/domain/models:
atleta.py
clube.py
competicao.py
contrato.py
estadio.py
__init__.py
jogo.py
transferencia.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/domain/value_objects:
__init__.py
numero_camisa.py
placar.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/events:
bus.py
definitions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/infrastructure:
adapters
__init__.py
models
persistence
repositories
resilience

/home/user/sila-system/apps/backend/app/modules/society/desporto/infrastructure/adapters:
citizen_service_adapter.py
educacao_service_adapter.py
federacao_service_adapter.py
__init__.py
obras_publicas_service_adapter.py
request_service_adapter.py
saude_service_adapter.py
turismo_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/infrastructure/models:
atleta_model.py
clube_model.py
competicao_model.py
contrato_model.py
estadio_model.py
__init__.py
jogo_model.py
outbox_event_model.py
transferencia_model.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/infrastructure/persistence:
__init__.py
outbox.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/infrastructure/repositories:
__init__.py
sqlalchemy_atleta_repository.py
sqlalchemy_clube_repository.py
sqlalchemy_competicao_repository.py
sqlalchemy_contrato_repository.py
sqlalchemy_estadio_repository.py
sqlalchemy_jogo_repository.py
sqlalchemy_transferencia_repository.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/infrastructure/resilience:
circuit_breaker.py
__init__.py
retry.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/resilience:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/tests:
_fakes.py
__init__.py
test_atletas.py
test_clubes.py
test_competicoes.py
test_estadios.py
test_events.py
test_jogos.py
test_orm_integration_real.py
test_workers.py

/home/user/sila-system/apps/backend/app/modules/society/desporto/workers:
estatistica_worker.py
__init__.py
notificacao_worker.py
outbox_worker.py
ranking_worker.py

/home/user/sila-system/apps/backend/app/modules/society/domain:
entities
enums
events
exceptions.py
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/society/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/society/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/educacao:
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/society/educacao/domain:
exceptions.py

/home/user/sila-system/apps/backend/app/modules/society/educacao/infrastructure:
__init__.py
repositories

/home/user/sila-system/apps/backend/app/modules/society/educacao/infrastructure/repositories:
__init__.py
sqlalchemy_escola_repository.py
sqlalchemy_matricula_repository.py
sqlalchemy_propina_repository.py
sqlalchemy_turma_repository.py

/home/user/sila-system/apps/backend/app/modules/society/emprego:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/society/emprego/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/emprego/api/endpoints:
candidatos.py
certificacoes.py
concursos.py
formacoes.py
__init__.py
mediacoes.py
ofertas.py
trabalhistas.py
_workflow_endpoints.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/api/schemas:
candidato_schema.py
certificacao_schema.py
concurso_schema.py
formacao_schema.py
__init__.py
mediacao_schema.py
oferta_schema.py
trabalhista_schema.py
workflow_schema.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/society/emprego/application/ports:
alfabetizacao_repository_port.py
avaliacao_repository_port.py
candidato_repository_port.py
certificacao_repository_port.py
citizen_service_port.py
concurso_repository_port.py
contrato_repository_port.py
credenciamento_repository_port.py
declaracao_repository_port.py
estagio_repository_port.py
fiscalizacao_repository_port.py
formacao_repository_port.py
__init__.py
inscricao_repository_port.py
mediacao_repository_port.py
mobilidade_repository_port.py
oferta_repository_port.py
reclamacao_repository_port.py
request_service_port.py
resultado_repository_port.py
workflow_repository_port.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/application/services:
candidato_service.py
certificacao_service.py
concurso_service.py
formacao_service.py
__init__.py
mediacao_service.py
oferta_service.py
trabalho_service.py
workflow_service.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/society/emprego/domain/models:
alfabetizacao.py
avaliacao_desempenho.py
candidato.py
capacitacao_qualidade.py
certificacao_competencias.py
certificacao_profissional.py
concurso_publico.py
credenciamento.py
declaracao_desemprego.py
estagio_publico.py
fiscalizacao_trabalho.py
formacao_avancada.py
formacao_certificada.py
formacao_gestores.py
formacao_profissional.py
__init__.py
inscricao_tecnica.py
mediacao_conflito.py
mediacao.py
mobilidade_publica.py
oferta_emprego.py
reclamacao_trabalhista.py
reconversao.py
registro_contrato.py
resultado_concurso.py
_workflow_record.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/infrastructure/adapters:
citizen_service_adapter.py
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/infrastructure/models:
alfabetizacao_model.py
avaliacao_model.py
candidato_model.py
certificacao_model.py
concurso_model.py
contrato_model.py
credenciamento_model.py
declaracao_model.py
estagio_model.py
fiscalizacao_model.py
formacao_avancada_model.py
formacao_model.py
__init__.py
inscricao_model.py
mediacao_model.py
mobilidade_model.py
oferta_model.py
reclamacao_model.py
resultado_model.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/infrastructure/repositories:
__init__.py
sqlalchemy_alfabetizacao_repository.py
sqlalchemy_avaliacao_repository.py
sqlalchemy_candidato_repository.py
sqlalchemy_certificacao_repository.py
sqlalchemy_concurso_repository.py
sqlalchemy_contrato_repository.py
sqlalchemy_credenciamento_repository.py
sqlalchemy_declaracao_repository.py
sqlalchemy_estagio_repository.py
sqlalchemy_fiscalizacao_repository.py
sqlalchemy_formacao_avancada_repository.py
sqlalchemy_formacao_repository.py
sqlalchemy_inscricao_repository.py
sqlalchemy_mediacao_repository.py
sqlalchemy_mobilidade_repository.py
sqlalchemy_oferta_repository.py
sqlalchemy_reclamacao_repository.py
sqlalchemy_resultado_repository.py
_workflow_sqlalchemy_repository.py

/home/user/sila-system/apps/backend/app/modules/society/emprego/tests:
__init__.py
test_candidatos.py
test_certificacoes.py
test_concursos.py
test_emprego_e2e.py
test_formacoes.py
test_mediacoes.py
test_ofertas.py
test_trabalhistas.py

/home/user/sila-system/apps/backend/app/modules/society/familia:
api
application
ARCHITECTURE.md
config.py
domain
exceptions.py
infrastructure
__init__.py
module.yaml
README.md
tests

/home/user/sila-system/apps/backend/app/modules/society/familia/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/familia/api/endpoints:
aggregates.py
dependencies.py
history.py
__init__.py
members.py
projections.py
relationships.py

/home/user/sila-system/apps/backend/app/modules/society/familia/api/schemas:
dependency_schema.py
family_aggregate_schema.py
family_member_schema.py
__init__.py
projection_schema.py
relationship_schema.py

/home/user/sila-system/apps/backend/app/modules/society/familia/application:
events
__init__.py
ports
sagas
service.py
services

/home/user/sila-system/apps/backend/app/modules/society/familia/application/events:
bus.py
definitions.py
__init__.py
registry.py

/home/user/sila-system/apps/backend/app/modules/society/familia/application/ports:
citizen_service_port.py
civil_registry_service_port.py
dependency_repository_port.py
event_bus_port.py
family_aggregate_repository_port.py
family_member_repository_port.py
__init__.py
outbox_repository_port.py
projection_repository_port.py
relationship_repository_port.py

/home/user/sila-system/apps/backend/app/modules/society/familia/application/sagas:
family_lifecycle_saga.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/familia/application/services:
dependency_service.py
family_aggregate_service.py
family_projection_handler.py
family_query_service.py
__init__.py
relationship_service.py

/home/user/sila-system/apps/backend/app/modules/society/familia/domain:
aggregates
entities.py
enums.py
events
exceptions
exceptions.py
__init__.py
rules
value_objects

/home/user/sila-system/apps/backend/app/modules/society/familia/domain/aggregates:
family_aggregate_root.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/familia/domain/events:
dependency_registered.py
family_created.py
family_dissolved.py
family_head_transferred.py
__init__.py
member_added.py
member_removed.py
relationship_created.py

/home/user/sila-system/apps/backend/app/modules/society/familia/domain/exceptions:
family_exceptions.py
__init__.py
validation_errors.py

/home/user/sila-system/apps/backend/app/modules/society/familia/domain/rules:
biological_coherence_rule.py
exclusive_marriage_rule.py
head_must_be_adult_rule.py
__init__.py
minor_requires_guardian_rule.py
one_active_family_rule.py

/home/user/sila-system/apps/backend/app/modules/society/familia/domain/value_objects:
age_range.py
dependency_type.py
family_code.py
__init__.py
relationship_type.py

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure:
adapters
event_handlers
__init__.py
models
projections
repositories
repository.py
resilience

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure/adapters:
citizen_service_adapter.py
civil_registry_adapter.py
__init__.py
social_programs_adapter.py
statistics_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure/event_handlers:
__init__.py
on_adoption_finalized.py
on_citizen_deceased.py
on_marriage_registered.py

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure/models:
dependency_model.py
event_outbox_model.py
family_aggregate_model.py
family_member_model.py
__init__.py
projection_models.py
relationship_model.py

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure/projections:
benefit_eligibility_projector.py
dependency_summary_projector.py
family_composition_projector.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure/repositories:
__init__.py
outbox_repository.py
redis_projection_repository.py
sqlalchemy_dependency_repository.py
sqlalchemy_family_aggregate_repository.py
sqlalchemy_relationship_repository.py

/home/user/sila-system/apps/backend/app/modules/society/familia/infrastructure/resilience:
circuit_breaker.py
__init__.py
retry_policy.py

/home/user/sila-system/apps/backend/app/modules/society/familia/tests:
e2e
_fakes.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/society/familia/tests/e2e:
test_citizen_deceased_cascade.py
test_family_lifecycle.py

/home/user/sila-system/apps/backend/app/modules/society/familia/tests/integration:
test_api_endpoints.py
test_event_publishing.py
test_repository_orm.py

/home/user/sila-system/apps/backend/app/modules/society/familia/tests/unit:
application
domain

/home/user/sila-system/apps/backend/app/modules/society/familia/tests/unit/application:
__init__.py
test_family_service.py
test_projection_handlers.py

/home/user/sila-system/apps/backend/app/modules/society/familia/tests/unit/domain:
__init__.py
test_dependency_validation.py
test_family_aggregate.py
test_relationship_rules.py

/home/user/sila-system/apps/backend/app/modules/society/igualdade:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/society/igualdade/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/society/igualdade/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/society/igualdade/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/igualdade/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/society/igualdade/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/infrastructure:
adapters
adapters.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/society/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/juventude:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/society/juventude/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/juventude/api/endpoints:
acompanhamentos.py
auxilios.py
bolsas_estudo.py
empreendedorismo_juvenil.py
estagios.py
eventos_juvenis.py
formacoes.py
__init__.py
inscricoes_programa.py
intercambios.py
jovens.py
mentores.py
politicas_juventude.py
programas.py
risco_evasao.py
saude_juvenil.py
voluntariados.py
_workflow_endpoints.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/api/schemas:
acompanhamento_juvenil_schema.py
auxilio_schema.py
bolsa_estudo_schema.py
empreendedorismo_juvenil_schema.py
estagio_juvenil_schema.py
evento_juvenil_schema.py
formacao_schema.py
__init__.py
inscricao_programa_schema.py
intercambio_juvenil_schema.py
jovem_schema.py
mentor_schema.py
politica_juventude_schema.py
programa_schema.py
risco_evasao_schema.py
saude_juvenil_schema.py
voluntariado_schema.py
workflow_schema.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/application:
__init__.py
ports
services

/home/user/sila-system/apps/backend/app/modules/society/juventude/application/ports:
acompanhamento_juvenil_repository_port.py
auxilio_repository_port.py
bolsa_estudo_repository_port.py
citizen_service_port.py
educacao_service_port.py
empreendedorismo_juvenil_repository_port.py
emprego_service_port.py
estagio_juvenil_repository_port.py
evento_juvenil_repository_port.py
formacao_repository_port.py
__init__.py
inscricao_programa_repository_port.py
intercambio_juvenil_repository_port.py
jovem_repository_port.py
mentor_repository_port.py
politica_juventude_repository_port.py
programa_repository_port.py
request_service_port.py
risco_evasao_repository_port.py
saude_juvenil_repository_port.py
voluntariado_repository_port.py
workflow_repository_port.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/application/services:
acompanhamento_juvenil_service.py
auxilio_service.py
bolsa_estudo_service.py
empreendedorismo_juvenil_service.py
estagio_juvenil_service.py
evento_juvenil_service.py
formacao_service.py
__init__.py
inscricao_programa_service.py
intercambio_juvenil_service.py
jovem_service.py
mentor_service.py
politica_juventude_service.py
programa_service.py
risco_evasao_service.py
saude_juvenil_service.py
voluntariado_service.py
workflow_service.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/domain:
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/society/juventude/domain/models:
acompanhamento_juvenil.py
auxilio.py
bolsa_estudo.py
empreendedorismo_juvenil.py
estagio_juvenil.py
evento_juvenil.py
formacao_juvenil.py
__init__.py
inscricao_programa.py
intercambio_juvenil.py
jovem.py
mentor.py
politica_juventude.py
programa_juvenil.py
risco_evasao.py
saude_juvenil.py
voluntariado.py
_workflow_record.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/infrastructure:
adapters
__init__.py
models
repositories

/home/user/sila-system/apps/backend/app/modules/society/juventude/infrastructure/adapters:
citizen_service_adapter.py
educacao_service_adapter.py
emprego_service_adapter.py
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/infrastructure/models:
acompanhamento_juvenil_model.py
auxilio_model.py
bolsa_estudo_model.py
empreendedorismo_juvenil_model.py
estagio_juvenil_model.py
evento_juvenil_model.py
formacao_juvenil_model.py
__init__.py
inscricao_programa_model.py
intercambio_juvenil_model.py
jovem_model.py
mentor_model.py
politica_juventude_model.py
programa_juvenil_model.py
risco_evasao_model.py
saude_juvenil_model.py
voluntariado_model.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/infrastructure/repositories:
__init__.py
sqlalchemy_acompanhamento_juvenil_repository.py
sqlalchemy_auxilio_repository.py
sqlalchemy_bolsa_estudo_repository.py
sqlalchemy_empreendedorismo_juvenil_repository.py
sqlalchemy_estagio_juvenil_repository.py
sqlalchemy_evento_juvenil_repository.py
sqlalchemy_formacao_repository.py
sqlalchemy_inscricao_programa_repository.py
sqlalchemy_intercambio_juvenil_repository.py
sqlalchemy_jovem_repository.py
sqlalchemy_mentor_repository.py
sqlalchemy_politica_juventude_repository.py
sqlalchemy_programa_repository.py
sqlalchemy_risco_evasao_repository.py
sqlalchemy_saude_juvenil_repository.py
sqlalchemy_voluntariado_repository.py
_workflow_sqlalchemy_repository.py

/home/user/sila-system/apps/backend/app/modules/society/juventude/tests:
_fakes.py
__init__.py
test_auxilios.py
test_formacoes.py
test_jovens.py
test_novos_slices_prioritarios.py
test_orm_integration_real.py
test_programas.py
test_risco_evasao_com_educacao.py
test_workflow_service.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/api/endpoints:
assets.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/api/schemas:
cultural_asset_schema.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/application/ports:
cultural_asset_repository_port.py
__init__.py
tourism_service_port.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/application/services:
cultural_asset_service.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/domain/models:
cultural_asset.py
cultural_event.py
heritage_classification.py
__init__.py
preservation_action.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/infrastructure:
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/infrastructure/models:
cultural_asset_model.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/infrastructure/repositories:
__init__.py
sqlalchemy_cultural_asset_repository.py

/home/user/sila-system/apps/backend/app/modules/society/patrimonio_cultural/tests:
_fakes.py
__init__.py
test_patrimonio_cultural_endpoints.py
test_patrimonio_cultural_service.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social:
api
application
ARCHITECTURE.md
domain
exceptions.py
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/api:
deps.py
endpoints
health.py
__init__.py
router.py
schemas

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/api/endpoints:
beneficiarios.py
__init__.py
pensoes.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/api/schemas:
beneficiario_schema.py
__init__.py
pensao_schema.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/application:
__init__.py
ports
service.py
services

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/application/ports:
beneficiario_repository_port.py
citizen_service_port.py
emprego_service_port.py
__init__.py
pensao_repository_port.py
request_service_port.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/application/services:
beneficiario_service.py
__init__.py
pensao_service.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/domain:
entities.py
enums.py
exceptions.py
__init__.py
models

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/domain/models:
beneficiario.py
__init__.py
pensao.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/infrastructure:
adapters
__init__.py
models
repositories
repository.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/infrastructure/adapters:
citizen_service_adapter.py
emprego_service_adapter.py
__init__.py
request_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/infrastructure/models:
beneficiario_model.py
__init__.py
pensao_model.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/infrastructure/repositories:
__init__.py
sqlalchemy_beneficiario_repository.py
sqlalchemy_pensao_repository.py

/home/user/sila-system/apps/backend/app/modules/society/seguranca_social/tests:
__init__.py
test_beneficiarios.py
test_pensoes.py

/home/user/sila-system/apps/backend/app/modules/society/tests:
api
application
conftest.py
domain
infrastructure
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/society/tests/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/society/tests/application:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/tests/domain:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/tests/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/society/tests/unit:
test_domain.py

/home/user/sila-system/apps/backend/app/modules/society/trabalho_inspecao:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/society/trabalho_inspecao/api:
health.py
__init__.py
router.py

/home/user/sila-system/apps/backend/app/modules/society/trabalho_inspecao/application:
__init__.py
service.py

/home/user/sila-system/apps/backend/app/modules/society/trabalho_inspecao/domain:
entities.py
exceptions.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/society/trabalho_inspecao/infrastructure:
__init__.py
repository.py

/home/user/sila-system/apps/backend/app/modules/society/trabalho_inspecao/tests:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tecnologia-inovacao:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/tecnologia-inovacao/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/tecnologia-inovacao/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/telecomunicacoes:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/telecomunicacoes/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/telecomunicacoes/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/tests:
ARCHITECTURE.md
conftest.py
__init__.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/tourism:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/tourism/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/tourism/api/endpoints:
agencias_viagens.py
atracao_turisticas.py
autos_infracao_turismo.py
avaliacoes.py
cadastro_turistas.py
cadastur.py
certificacoes_turisticas.py
chegadas_turistas.py
classificacoes_hoteleiras.py
estatisticas_turismo.py
eventos.py
fiscalizacoes_turismo.py
fluxo_turistico.py
guias_turismo.py
hoteis.py
__init__.py
licencas_turismo.py
multas_turismo.py
ocupacao_hoteleira.py
operadores_turisticos.py
pacotes.py
pontos_turisticos.py
pousadas.py
promocoes_turisticas.py
receitas_turisticas.py
reclamacoes_turismo.py
registros_guia.py
reservas.py
resorts.py
roteiros.py
tarifas_hotel.py
temporadas.py

/home/user/sila-system/apps/backend/app/modules/tourism/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services

/home/user/sila-system/apps/backend/app/modules/tourism/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/application/dto:
agencia_viagens_schema.py
atracao_turistica_schema.py
auto_infracao_turismo_schema.py
avaliacao_schema.py
cadastro_turista_schema.py
cadastur_schema.py
certificacao_turistica_schema.py
classificacao_hoteleira_schema.py
credencial_schema.py
estatistica_turismo_schema.py
evento_turistico_schema.py
fluxo_turistico_schema.py
guia_turismo_schema.py
hotel_schema.py
__init__.py
licenca_turismo_schema.py
multa_turismo_schema.py
ocupacao_hoteleira_schema.py
operador_turistico_schema.py
pacote_turistico_schema.py
ponto_turistico_schema.py
pousada_schema.py
promocao_turistica_schema.py
receita_turistica_schema.py
reclamacao_turismo_schema.py
registro_guia_schema.py
reserva_hotel_schema.py
reserva_pacote_schema.py
roteiro_schema.py
tarifa_hotel_schema.py
temporada_schema.py
visitante_schema.py

/home/user/sila-system/apps/backend/app/modules/tourism/application/ports:
agencia_viagens_repository_port.py
ambiente_service_port.py
atracao_turistica_repository_port.py
auto_infracao_turismo_repository_port.py
avaliacao_repository_port.py
cadastro_turista_repository_port.py
cadastur_repository_port.py
certificacao_turistica_repository_port.py
chegada_turistas_repository_port.py
citizen_service_port.py
classificacao_hoteleira_repository_port.py
comercio_servicos_service_port.py
condutor_visitantes_repository_port.py
credencial_repository_port.py
cultura_service_port.py
estatistica_turismo_repository_port.py
evento_turistico_repository_port.py
fiscalizacao_turismo_repository_port.py
fluxo_turistico_repository_port.py
geosampa_service_port.py
guia_turismo_repository_port.py
hotel_repository_port.py
__init__.py
licenca_turismo_repository_port.py
multa_turismo_repository_port.py
ocupacao_hoteleira_repository_port.py
operador_turistico_repository_port.py
pacote_turistico_repository_port.py
ponto_turistico_repository_port.py
pousada_repository_port.py
promocao_turistica_repository_port.py
receita_turistica_repository_port.py
reclamacao_turismo_repository_port.py
registro_guia_repository_port.py
request_service_port.py
reserva_hotel_repository_port.py
reserva_pacote_repository_port.py
resort_repository_port.py
roteiro_repository_port.py
tarifa_hotel_repository_port.py
temporada_repository_port.py
transportes_logistica_service_port.py
visitante_repository_port.py

/home/user/sila-system/apps/backend/app/modules/tourism/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/application/services:
agencia_viagens_service.py
atracao_service.py
avaliacao_service.py
cadastro_turista_service.py
cadastur_service.py
certificacao_service.py
classificacao_service.py
estatistica_turismo_service.py
evento_service.py
fiscalizacao_turismo_service.py
fluxo_turistico_service.py
guia_turismo_service.py
__init__.py
inteligencia_turismo_service.py
licenciamento_turismo_service.py
meio_hospedagem_service.py
ocupacao_service.py
operador_turistico_service.py
pacote_service.py
penalidade_turismo_service.py
promocao_service.py
reclamacao_service.py
registro_guia_service.py
reserva_service.py
roteiro_service.py
tarifa_service.py
temporada_service.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain:
entities
enums
enums.py
events
__init__.py
models
models.py
module.yaml
ports
repositories
repositories.py
services
tests
value_objects

/home/user/sila-system/apps/backend/app/modules/tourism/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/models:
acessibilidade.py
agencia_viagens.py
alta_temporada.py
atracao_turistica.py
auto_infracao_turismo.py
avaliacao.py
baixa_temporada.py
cadastro_turista.py
cadastur.py
camping.py
certificacao_turistica.py
checkin.py
checkout.py
chegada_turistas.py
classificacao_hoteleira.py
condutor_visitantes.py
credencial.py
divisas.py
ecoturismo.py
entrada_saida.py
estatistica_turismo.py
estrelas.py
evento_turistico.py
excursao.py
feedback_turista.py
festival.py
fiscalizacao_turismo.py
fluxo_turistico.py
gasto_medio.py
guia_turismo.py
hotel.py
impacto_economico.py
__init__.py
interdicao_hotel.py
licenca_turismo.py
lodge.py
monumento.py
multa_turismo.py
museu.py
nacionalidade.py
ocupacao_hoteleira.py
operador_turistico.py
pacote_turistico.py
parque_nacional.py
perfil_turista.py
permanencia_media.py
ponto_turistico.py
pousada.py
praia.py
promocao_turistica.py
receita_turistica.py
reclamacao_turismo.py
registro_guia.py
reserva_hotel.py
reserva_natural.py
reserva_pacote.py
resort.py
restaurante_turistico.py
roteiro.py
sazonalidade.py
selo_sustentabilidade.py
sitio_historico.py
tarifa_hotel.py
temporada.py
turismo_acessivel.py
turismo_aventura.py
turismo_educacional.py
turismo_eventos.py
turismo_gastronomico.py
turismo_historico.py
turismo_negocios.py
turismo_religioso.py
turismo_saude.py
visita_guiada.py
visitante.py
visto.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/tests:
__init__.py
test_agencias_viagens.py
test_atracoes.py
test_autos_infracao.py
test_avaliacoes.py
test_cadastro_turistas.py
test_cadastur.py
test_certificacoes.py
test_classificacoes.py
test_estatisticas.py
test_eventos.py
test_fiscalizacoes.py
test_fluxo_turistico.py
test_guias_turismo.py
test_hoteis.py
test_licencas.py
test_multas.py
test_ocupacao_hoteleira.py
test_operadores_turisticos.py
test_pacotes.py
test_pontos_turisticos.py
test_pousadas.py
test_promocoes.py
test_receitas.py
test_reclamacoes.py
test_registro_guia.py
test_reservas.py
test_roteiros.py
test_tarifas.py
test_temporadas.py

/home/user/sila-system/apps/backend/app/modules/tourism/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/infrastructure:
adapters
adapters.py
__init__.py
models
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/tourism/infrastructure/adapters:
ambiente_service_adapter.py
citizen_service_adapter.py
comercio_servicos_service_adapter.py
cultura_service_adapter.py
geosampa_service_adapter.py
__init__.py
request_service_adapter.py
transportes_logistica_service_adapter.py

/home/user/sila-system/apps/backend/app/modules/tourism/infrastructure/models:
agencia_viagens_model.py
atracao_turistica_model.py
auto_infracao_turismo_model.py
avaliacao_model.py
cadastro_turista_model.py
cadastur_model.py
certificacao_turistica_model.py
classificacao_hoteleira_model.py
credencial_model.py
estatistica_turismo_model.py
evento_turistico_model.py
fiscalizacao_turismo_model.py
fluxo_turistico_model.py
guia_turismo_model.py
hotel_model.py
__init__.py
licenca_turismo_model.py
multa_turismo_model.py
ocupacao_hoteleira_model.py
operador_turistico_model.py
pacote_turistico_model.py
ponto_turistico_model.py
pousada_model.py
promocao_turistica_model.py
receita_turistica_model.py
reclamacao_turismo_model.py
registro_guia_model.py
reserva_hotel_model.py
reserva_pacote_model.py
roteiro_model.py
tarifa_hotel_model.py
temporada_model.py
visitante_model.py

/home/user/sila-system/apps/backend/app/modules/tourism/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/tourism/infrastructure/repositories:
__init__.py
sqlalchemy_agencia_viagens_repository.py
sqlalchemy_atracao_turistica_repository.py
sqlalchemy_auto_infracao_turismo_repository.py
sqlalchemy_avaliacao_repository.py
sqlalchemy_cadastro_turista_repository.py
sqlalchemy_cadastur_repository.py
sqlalchemy_certificacao_turistica_repository.py
sqlalchemy_classificacao_hoteleira_repository.py
sqlalchemy_credencial_repository.py
sqlalchemy_estatistica_turismo_repository.py
sqlalchemy_evento_turistico_repository.py
sqlalchemy_fiscalizacao_turismo_repository.py
sqlalchemy_fluxo_turistico_repository.py
sqlalchemy_guia_turismo_repository.py
sqlalchemy_hotel_repository.py
sqlalchemy_licenca_turismo_repository.py
sqlalchemy_multa_turismo_repository.py
sqlalchemy_ocupacao_hoteleira_repository.py
sqlalchemy_operador_turistico_repository.py
sqlalchemy_pacote_turistico_repository.py
sqlalchemy_ponto_turistico_repository.py
sqlalchemy_pousada_repository.py
sqlalchemy_promocao_turistica_repository.py
sqlalchemy_receita_turistica_repository.py
sqlalchemy_reclamacao_turismo_repository.py
sqlalchemy_registro_guia_repository.py
sqlalchemy_reserva_hotel_repository.py
sqlalchemy_reserva_pacote_repository.py
sqlalchemy_roteiro_repository.py
sqlalchemy_tarifa_hotel_repository.py
sqlalchemy_temporada_repository.py
sqlalchemy_visitante_repository.py

/home/user/sila-system/apps/backend/app/modules/tourism/tests:
conftest.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/tourism/tests/integration:
__init__.py
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/tourism/tests/unit:
__init__.py
test_domain.py

/home/user/sila-system/apps/backend/app/modules/trabalho-inspecao:
api
ARCHITECTURE.md
domain
governance.py
module.yaml

/home/user/sila-system/apps/backend/app/modules/trabalho-inspecao/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/trabalho-inspecao/domain:
event_catalog.py
models.py

/home/user/sila-system/apps/backend/app/modules/transportes:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/transportes/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/transportes/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/turismo:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/turismo/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/turismo/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/urbanismo:
api
ARCHITECTURE.md
domain
module.yaml

/home/user/sila-system/apps/backend/app/modules/urbanismo/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/urbanismo/domain:
models.py

/home/user/sila-system/apps/backend/app/modules/wallet:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
models.py
module.yaml
router.py
schemas.py
service.py

/home/user/sila-system/apps/backend/app/modules/wallet/api:
health.py
routers.py

/home/user/sila-system/apps/backend/app/modules/wallet/application:
commands.py
event_handlers.py
__init__.py

/home/user/sila-system/apps/backend/app/modules/wallet/domain:
models.py
repositories.py

/home/user/sila-system/apps/backend/app/modules/wallet/infrastructure:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad:
api
application
ARCHITECTURE.md
domain
infrastructure
__init__.py
module.yaml
tests

/home/user/sila-system/apps/backend/app/modules/xroad/api:
endpoints
health.py
__init__.py
router.py
routers.py

/home/user/sila-system/apps/backend/app/modules/xroad/api/endpoints:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/application:
commands
commands.py
dto
event_handlers.py
__init__.py
ports
queries
services
xroad_service.py

/home/user/sila-system/apps/backend/app/modules/xroad/application/commands:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/application/dto:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/application/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/application/queries:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/application/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain:
audit_log.py
entities
enums
envelope.py
events
__init__.py
models
models.py
ports
repositories
repositories.py
services
value_objects

/home/user/sila-system/apps/backend/app/modules/xroad/domain/entities:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/enums:
__init__.py
status_enum.py
type_enum.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/events:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/models:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/ports:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/services:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/domain/value_objects:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/infrastructure:
adapters
adapters.py
audit_repository.py
__init__.py
orm
repositories
repositories.py

/home/user/sila-system/apps/backend/app/modules/xroad/infrastructure/adapters:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/infrastructure/orm:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/infrastructure/repositories:
__init__.py

/home/user/sila-system/apps/backend/app/modules/xroad/tests:
conftest.py
__init__.py
integration
unit

/home/user/sila-system/apps/backend/app/modules/xroad/tests/integration:
test_repositories.py

/home/user/sila-system/apps/backend/app/modules/xroad/tests/unit:
test_domain.py
