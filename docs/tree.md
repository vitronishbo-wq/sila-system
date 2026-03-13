(.venv) dev03wsl@Rochete-consultoria:~/sila-system$ tree -L 8 -I "venv|__pycache__|*.egg-info|node_modules|dist|build"
.
├── AI_ENTRYPOINTS.yaml
├── AI_FILE_SCOPE.yaml
├── API_MAP.yaml
├── ARCHITECTURE_DEPENDENCIES.yaml
├── ARCHITECTURE_INDEX.yaml
├── BATCH_ACTIONS_APPLIED.md
├── CONSOLIDATION_COMPLIANCE_2026-03-13.md
├── CONSOLIDATION_HANDOFF_2026-03-13.txt
├── DIAGNOSTIC_REPORT.sh
├── Dockerfile.alerts
├── FINAL_SILA3_AUDIT.txt
├── Makefile
├── Makefile.db
├── NEXT_SPRINT_COMMANDS.md
├── SILA3.0_FINAL_ARTIFACTS.md
├── VISUAL_COMPLIANCE_DASHBOARD.txt
├── access_db.sh
├── alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 001_create_taxpayer_tables.py
│       ├── 002_create_debt_payment_tables.py
│       ├── 003_create_certificate_audit_tables.py
│       ├── 004_create_sequence_table.py
│       ├── 005_add_constraints.py
│       ├── 006_add_triggers.py
│       ├── 007_add_views_performance.py
│       └── 008_add_citizen_hierarchy_columns.py
├── alert-rules.yml
├── alertmanager.yml
├── app
│   └── modules
│       ├── educacao
│       │   └── core
│       │       ├── application
│       │       │   └── ports
│       │       │       └── identity_service_port.py
│       │       └── domain
│       │           ├── academic
│       │           │   └── __init__.py
│       │           ├── professional
│       │           │   └── __init__.py
│       │           └── workflow
│       │               └── strategies
│       │                   └── __init__.py
│       ├── health
│       │   └── core
│       │       ├── application
│       │       │   └── ports
│       │       │       └── identity_service_port.py
│       │       └── domain
│       │           ├── clinical
│       │           │   └── __init__.py
│       │           ├── public_health
│       │           │   └── __init__.py
│       │           └── shared
│       │               └── __init__.py
│       ├── identity
│       │   └── core
│       │       ├── application
│       │       │   └── services
│       │       ├── domain
│       │       │   └── entities
│       │       └── infrastructure
│       │           ├── models
│       │           ├── repositories
│       │           └── security
│       ├── justice
│       │   ├── _deprecated
│       │   └── core
│       │       ├── application
│       │       ├── domain
│       │       └── infrastructure
│       │           └── legacy_adapters
│       └── xroad
│           ├── __init__.py
│           ├── application
│           │   ├── __init__.py
│           │   └── xroad_service.py
│           ├── domain
│           │   ├── __init__.py
│           │   ├── audit_log.py
│           │   └── envelope.py
│           └── infrastructure
│               ├── __init__.py
│               └── audit_repository.py
├── apps
│   ├── __init__.py
│   ├── api_gateway
│   ├── backend
│   │   ├── 0.1.4
│   │   ├── 01_eliminate_db_duplication.sh
│   │   ├── 01_fix_imports_pragmatic.py
│   │   ├── 09_final_verification.sh
│   │   ├── Dockerfile
│   │   ├── Dockerfile.prod
│   │   ├── FASE3_DEPLOYMENT_CHECK.sh
│   │   ├── Makefile
│   │   ├── STRATEGIC_DECISION_POINT.py
│   │   ├── TEMPLATE_DDD_MODULE.py
│   │   ├── __init__.py
│   │   ├── _backup_modules
│   │   │   └── justice_backup_
│   │   │       ├── ARCHITECTURE.md
│   │   │       ├── api
│   │   │       │   └── router.py
│   │   │       ├── application
│   │   │       ├── bounded_contexts
│   │   │       │   ├── __init__.py
│   │   │       │   ├── application
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── ports
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── assistencia_social_service_port.py
│   │   │       │   │   │   ├── bi_repository_port.py
│   │   │       │   │   │   ├── birth_repository_port.py
│   │   │       │   │   │   ├── cemetery_inspection_repository_port.py
│   │   │       │   │   │   ├── citizen_fuc_client_port.py
│   │   │       │   │   │   ├── citizen_port.py
│   │   │       │   │   │   ├── citizen_repository_port.py
│   │   │       │   │   │   ├── death_repository_port.py
│   │   │       │   │   │   ├── document_repository_port.py
│   │   │       │   │   │   ├── educacao_service_port.py
│   │   │       │   │   │   ├── emprego_service_port.py
│   │   │       │   │   │   ├── identity_request_repository_port.py
│   │   │       │   │   │   ├── juventude_service_port.py
│   │   │       │   │   │   ├── marriage_repository_port.py
│   │   │       │   │   │   ├── platform_shared_ports.py
│   │   │       │   │   │   └── saude_service_port.py
│   │   │       │   │   └── services
│   │   │       │   │       ├── __init__.py
│   │   │       │   │       ├── bi_emission_service.py
│   │   │       │   │       ├── birth_service.py
│   │   │       │   │       ├── certificate_service.py
│   │   │       │   │       ├── citizen_service.py
│   │   │       │   │       ├── death_service.py
│   │   │       │   │       ├── document_service.py
│   │   │       │   │       ├── marriage_service.py
│   │   │       │   │       ├── profile_queries.py
│   │   │       │   │       ├── service.py
│   │   │       │   │       └── services
│   │   │       │   ├── cemetery_management
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── api
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── router.py
│   │   │       │   │   ├── application
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── cemetery_inspection_service.py
│   │   │       │   │   ├── domain
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── cemetery_inspection_record.py
│   │   │       │   │   └── infrastructure
│   │   │       │   │       ├── __init__.py
│   │   │       │   │       ├── cemetery_inspection_model.py
│   │   │       │   │       └── cemetery_inspection_repository.py
│   │   │       │   ├── civil_registry_core
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── api
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── router.py
│   │   │       │   │   ├── application
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── ports
│   │   │       │   │   │   └── services
│   │   │       │   │   ├── domain
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── aggregates
│   │   │       │   │   │   ├── entities
│   │   │       │   │   │   └── value_objects
│   │   │       │   │   ├── infrastructure
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── models
│   │   │       │   │   │   └── repositories
│   │   │       │   │   └── projections
│   │   │       │   │       └── __init__.py
│   │   │       │   ├── identity_documents
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── api
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── bi_routes.py
│   │   │       │   │   │   ├── documents_routes.py
│   │   │       │   │   │   └── router.py
│   │   │       │   │   ├── application
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── ports
│   │   │       │   │   │   └── services
│   │   │       │   │   ├── domain
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── entities
│   │   │       │   │   ├── infrastructure
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── models
│   │   │       │   │   │   └── repositories
│   │   │       │   │   ├── integrations
│   │   │       │   │   │   └── __init__.py
│   │   │       │   │   └── projections
│   │   │       │   │       └── __init__.py
│   │   │       │   ├── infrastructure
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── adapters
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── assistencia_social_service_adapter.py
│   │   │       │   │   │   ├── educacao_service_adapter.py
│   │   │       │   │   │   ├── emprego_service_adapter.py
│   │   │       │   │   │   ├── juventude_service_adapter.py
│   │   │       │   │   │   └── saude_service_adapter.py
│   │   │       │   │   ├── models
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── bi.py
│   │   │       │   │   │   ├── bi_event.py
│   │   │       │   │   │   ├── bi_event_record.py
│   │   │       │   │   │   ├── bi_record.py
│   │   │       │   │   │   ├── birth_record.py
│   │   │       │   │   │   ├── cemetery_inspection_model.py
│   │   │       │   │   │   ├── cemetery_inspection_record.py
│   │   │       │   │   │   ├── certificate_record.py
│   │   │       │   │   │   ├── citizen.py
│   │   │       │   │   │   ├── citizen_event_model.py
│   │   │       │   │   │   ├── citizen_model.py
│   │   │       │   │   │   ├── civil_event.py
│   │   │       │   │   │   ├── death_record.py
│   │   │       │   │   │   ├── document.py
│   │   │       │   │   │   ├── fuc_projection.py
│   │   │       │   │   │   ├── identity_request.py
│   │   │       │   │   │   ├── identity_request_record.py
│   │   │       │   │   │   └── marriage_record.py
│   │   │       │   │   └── repositories
│   │   │       │   │       ├── __init__.py
│   │   │       │   │       ├── bi_repository.py
│   │   │       │   │       ├── birth_repository.py
│   │   │       │   │       ├── cemetery_inspection_repository.py
│   │   │       │   │       ├── citizen_repository.py
│   │   │       │   │       ├── civil_event_repository.py
│   │   │       │   │       ├── death_repository.py
│   │   │       │   │       ├── document_repository.py
│   │   │       │   │       ├── identity_request_repository.py
│   │   │       │   │       └── marriage_repository.py
│   │   │       │   ├── permissions
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── access_control.py
│   │   │       │   │   └── policies.py
│   │   │       │   └── vital_events
│   │   │       │       ├── __init__.py
│   │   │       │       ├── api
│   │   │       │       │   ├── __init__.py
│   │   │       │       │   ├── birth_routes.py
│   │   │       │       │   ├── death_routes.py
│   │   │       │       │   ├── marriage_routes.py
│   │   │       │       │   └── router.py
│   │   │       │       ├── application
│   │   │       │       │   ├── __init__.py
│   │   │       │       │   ├── ports
│   │   │       │       │   └── services
│   │   │       │       ├── domain
│   │   │       │       │   ├── __init__.py
│   │   │       │       │   └── entities
│   │   │       │       ├── events
│   │   │       │       │   └── __init__.py
│   │   │       │       ├── infrastructure
│   │   │       │       │   ├── __init__.py
│   │   │       │       │   ├── models
│   │   │       │       │   └── repositories
│   │   │       │       └── projections
│   │   │       │           └── __init__.py
│   │   │       ├── civil_registry
│   │   │       │   ├── ARCHITECTURE.md
│   │   │       │   ├── __init__.py
│   │   │       │   ├── adapters
│   │   │       │   │   └── __init__.py
│   │   │       │   ├── api
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── atestados_routes.py
│   │   │       │   │   ├── bi_routes.py
│   │   │       │   │   ├── certificates
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── certificate_routes.py
│   │   │       │   │   ├── citizen_documents.py
│   │   │       │   │   ├── citizens
│   │   │       │   │   │   └── citizens_routes.py
│   │   │       │   │   ├── documents
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── documents_routes.py
│   │   │       │   │   ├── events
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── birth_routes.py
│   │   │       │   │   │   ├── death_routes.py
│   │   │       │   │   │   └── marriage_routes.py
│   │   │       │   │   ├── health.py
│   │   │       │   │   ├── historico_routes.py
│   │   │       │   │   ├── public_router.py
│   │   │       │   │   ├── router.py
│   │   │       │   │   └── validacao_routes.py
│   │   │       │   ├── application
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── ports
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── assistencia_social_service_port.py
│   │   │       │   │   │   ├── bi_repository_port.py
│   │   │       │   │   │   ├── birth_repository_port.py
│   │   │       │   │   │   ├── cemetery_inspection_repository_port.py
│   │   │       │   │   │   ├── citizen_fuc_client_port.py
│   │   │       │   │   │   ├── citizen_port.py
│   │   │       │   │   │   ├── citizen_repository_port.py
│   │   │       │   │   │   ├── death_repository_port.py
│   │   │       │   │   │   ├── document_repository_port.py
│   │   │       │   │   │   ├── educacao_service_port.py
│   │   │       │   │   │   ├── emprego_service_port.py
│   │   │       │   │   │   ├── identity_request_repository_port.py
│   │   │       │   │   │   ├── juventude_service_port.py
│   │   │       │   │   │   ├── marriage_repository_port.py
│   │   │       │   │   │   ├── platform_shared_ports.py
│   │   │       │   │   │   └── saude_service_port.py
│   │   │       │   │   ├── ports.py
│   │   │       │   │   ├── service.py
│   │   │       │   │   └── services
│   │   │       │   │       ├── __init__.py
│   │   │       │   │       ├── alter_data_service.py
│   │   │       │   │       ├── audit.py
│   │   │       │   │       ├── bi_event_handler.py
│   │   │       │   │       ├── cemetery_inspection_service.py
│   │   │       │   │       ├── certificate_state_service.py
│   │   │       │   │       ├── citizen_query_service.py
│   │   │       │   │       ├── events.py
│   │   │       │   │       ├── identity_request_service.py
│   │   │       │   │       ├── late_birth_service.py
│   │   │       │   │       ├── queries.py
│   │   │       │   │       ├── request_service.py
│   │   │       │   │       ├── routing_engine.py
│   │   │       │   │       ├── schemas.py
│   │   │       │   │       └── services
│   │   │       │   ├── domain
│   │   │       │   │   ├── aggregates
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   └── citizen_aggregate.py
│   │   │       │   │   ├── entities
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── base.py
│   │   │       │   │   │   ├── bilhete_identidade.py
│   │   │       │   │   │   ├── citizen.py
│   │   │       │   │   │   └── identity_request.py
│   │   │       │   │   ├── entities.py
│   │   │       │   │   ├── exceptions.py
│   │   │       │   │   ├── models
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── bi.py
│   │   │       │   │   │   ├── bi_event.py
│   │   │       │   │   │   ├── bi_event_record.py
│   │   │       │   │   │   ├── bi_record.py
│   │   │       │   │   │   ├── cemetery_inspection_record.py
│   │   │       │   │   │   ├── certificate_record.py
│   │   │       │   │   │   ├── citizen.py
│   │   │       │   │   │   ├── civil_event.py
│   │   │       │   │   │   ├── document.py
│   │   │       │   │   │   ├── fuc_projection.py
│   │   │       │   │   │   ├── identity_request.py
│   │   │       │   │   │   └── identity_request_record.py
│   │   │       │   │   └── value_objects
│   │   │       │   │       ├── __init__.py
│   │   │       │   │       ├── document_number.py
│   │   │       │   │       └── nationality.py
│   │   │       │   ├── enums.py
│   │   │       │   ├── events
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── models.py
│   │   │       │   │   └── service.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── infrastructure
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── adapters
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── assistencia_social_service_adapter.py
│   │   │       │   │   │   ├── educacao_service_adapter.py
│   │   │       │   │   │   ├── emprego_service_adapter.py
│   │   │       │   │   │   ├── juventude_service_adapter.py
│   │   │       │   │   │   └── saude_service_adapter.py
│   │   │       │   │   ├── citizen_repository.py
│   │   │       │   │   ├── fuc_adapter.py
│   │   │       │   │   ├── logging_config.py
│   │   │       │   │   ├── models
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── bi.py
│   │   │       │   │   │   ├── bi_event.py
│   │   │       │   │   │   ├── bi_event_record.py
│   │   │       │   │   │   ├── bi_record.py
│   │   │       │   │   │   ├── birth_record.py
│   │   │       │   │   │   ├── cemetery_inspection_model.py
│   │   │       │   │   │   ├── cemetery_inspection_record.py
│   │   │       │   │   │   ├── certificate_record.py
│   │   │       │   │   │   ├── citizen.py
│   │   │       │   │   │   ├── citizen_event_model.py
│   │   │       │   │   │   ├── citizen_model.py
│   │   │       │   │   │   ├── civil_event.py
│   │   │       │   │   │   ├── death_record.py
│   │   │       │   │   │   ├── document.py
│   │   │       │   │   │   ├── fuc_projection.py
│   │   │       │   │   │   ├── identity_request.py
│   │   │       │   │   │   ├── identity_request_record.py
│   │   │       │   │   │   └── marriage_record.py
│   │   │       │   │   ├── persistence
│   │   │       │   │   └── repositories
│   │   │       │   │       ├── __init__.py
│   │   │       │   │       ├── bi_repository.py
│   │   │       │   │       ├── cemetery_inspection_repository.py
│   │   │       │   │       ├── citizen_repository.py
│   │   │       │   │       ├── civil_event_repository.py
│   │   │       │   │       ├── document_repository.py
│   │   │       │   │       └── identity_request_repository.py
│   │   │       │   ├── integrations
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── citizen_fuc_client.py
│   │   │       │   │   ├── fuc
│   │   │       │   │   │   ├── __init__.py
│   │   │       │   │   │   ├── adapter.py
│   │   │       │   │   │   └── client.py
│   │   │       │   │   └── fuc_client.py
│   │   │       │   ├── interfaces
│   │   │       │   │   └── api
│   │   │       │   │       ├── endpoints
│   │   │       │   │       └── schemas
│   │   │       │   ├── migrations
│   │   │       │   │   └── 2026_create_civil_registry_projection.sql
│   │   │       │   ├── module.yaml
│   │   │       │   ├── permissions
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── access_control.py
│   │   │       │   │   └── policies.py
│   │   │       │   ├── projection
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   └── civil_registry_projector.py
│   │   │       │   ├── projections
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── citizen_projector.py
│   │   │       │   │   ├── projectors.py
│   │   │       │   │   └── rebuild.py
│   │   │       │   ├── scripts
│   │   │       │   │   └── start_justice_workers.sh
│   │   │       │   ├── service.py
│   │   │       │   ├── shared
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   └── orm_base.py
│   │   │       │   ├── tests
│   │   │       │   │   ├── __init__.py
│   │   │       │   │   ├── conftest.py
│   │   │       │   │   ├── test_adapters.py
│   │   │       │   │   ├── test_auth.py
│   │   │       │   │   ├── test_bi_routes.py
│   │   │       │   │   ├── test_birth_events.py
│   │   │       │   │   ├── test_certificates.py
│   │   │       │   │   ├── test_citizen_entity.py
│   │   │       │   │   ├── test_citizen_model.py
│   │   │       │   │   ├── test_citizen_repository.py
│   │   │       │   │   ├── test_citizens_integracao_routes.py
│   │   │       │   │   ├── test_death_events.py
│   │   │       │   │   ├── test_historico_routes.py
│   │   │       │   │   ├── test_integracao_assistencia.py
│   │   │       │   │   ├── test_integracao_educacao.py
│   │   │       │   │   ├── test_integracao_emprego.py
│   │   │       │   │   ├── test_integracao_juventude.py
│   │   │       │   │   ├── test_integracao_saude.py
│   │   │       │   │   ├── test_marriage_events.py
│   │   │       │   │   └── test_validacao_routes.py
│   │   │       │   └── workers
│   │   │       │       └── civil_registry_projection_worker.py
│   │   │       ├── domain
│   │   │       │   └── exceptions.py
│   │   │       ├── events
│   │   │       │   ├── ARCHITECTURE.md
│   │   │       │   ├── __init__.py
│   │   │       │   ├── api
│   │   │       │   ├── application
│   │   │       │   ├── bus.py
│   │   │       │   ├── definitions.py
│   │   │       │   ├── domain
│   │   │       │   │   └── exceptions.py
│   │   │       │   ├── infrastructure
│   │   │       │   ├── module.yaml
│   │   │       │   └── tests
│   │   │       ├── exceptions.py
│   │   │       ├── infrastructure
│   │   │       ├── module.yaml
│   │   │       └── tests
│   │   │           ├── api
│   │   │           │   ├── health.py
│   │   │           │   └── router.py
│   │   │           ├── application
│   │   │           ├── cemetery_management
│   │   │           │   └── __init__.py
│   │   │           ├── civil_registry_core
│   │   │           │   └── __init__.py
│   │   │           ├── domain
│   │   │           ├── identity_documents
│   │   │           │   └── __init__.py
│   │   │           ├── infrastructure
│   │   │           ├── test_e2e_civil_registry.py
│   │   │           └── vital_events
│   │   │               └── __init__.py
│   │   ├── alembic
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   │       ├── 001_initial_schema.py
│   │   │       ├── 002_create_citizen_table.py
│   │   │       ├── 003_add_iam_system.py
│   │   │       ├── 20231027_001_add_saude_primaria.py
│   │   │       ├── 20260220_001_create_citizen_documents.py
│   │   │       ├── 20260228_001_merge_legacy_heads.py
│   │   │       ├── 20260228_002_catalog_schema_governance.py
│   │   │       ├── 20260228_003_operational_flow_tables.py
│   │   │       ├── 20260228_004_educacao_foundation.py
│   │   │       ├── 20260228_005_saude_fases_4_7.py
│   │   │       ├── 20260228_006_saude_status_constraints.py
│   │   │       ├── 20260228_007_educacao_fases_2_7.py
│   │   │       ├── 20260301_001_comercio_externo_exportadores.py
│   │   │       ├── 20260301_002_comercio_externo_importadores.py
│   │   │       ├── 20260301_003_comercio_externo_operadores_logisticos.py
│   │   │       ├── 20260301_004_comercio_externo_transportadores_internacionais.py
│   │   │       ├── 20260301_005_comercio_externo_habilitacoes.py
│   │   │       ├── 20260301_006_comercio_externo_radar.py
│   │   │       ├── 20260301_007_comercio_externo_processos_radar.py
│   │   │       ├── 20260301_008_pecuaria_foundation.py
│   │   │       ├── 20260301_009_comercio_externo_drawback.py
│   │   │       ├── 20260301_010_comercio_externo_drawback_modalidades.py
│   │   │       ├── 20260301_011_comercio_externo_drawback_modalidades_complementares.py
│   │   │       ├── 20260301_012_comercio_externo_drawback_modalidades_externo_interno.py
│   │   │       ├── 20260301_013_comercio_externo_drawback_modalidades_siscomex_verde_amarelo.py
│   │   │       ├── 20260301_014_pescas_foundation.py
│   │   │       ├── 20260301_015_florestas_foundation.py
│   │   │       ├── 20260302_016_pescas_industriais_foundation.py
│   │   │       ├── 20260302_017_cultura_foundation.py
│   │   │       ├── 20260302_018_cultura_slice2_grupos_patrimonio_imaterial.py
│   │   │       ├── 20260302_019_desporto_foundation.py
│   │   │       ├── 20260302_020_desporto_slice2_clubes_jogos.py
│   │   │       ├── 20260302_021_juventude_foundation.py
│   │   │       ├── 20260302_022_juventude_programas_formacoes.py
│   │   │       ├── 20260302_023_telecomunicacoes_foundation.py
│   │   │       ├── 20260302_024_telecomunicacoes_infra_espectro_outorgas.py
│   │   │       ├── 20260302_025_telecomunicacoes_qualidade_sla_indicadores.py
│   │   │       ├── 20260302_026_seguranca_publica_foundation.py
│   │   │       ├── 20260302_027_seguranca_publica_mandados_investigacoes_provas.py
│   │   │       ├── 20260302_028_seguranca_publica_cadeia_custodia_laudos.py
│   │   │       ├── 20260302_029_seguranca_publica_vestigios_evidencias.py
│   │   │       ├── 20260302_030_protecao_civil_foundation.py
│   │   │       ├── 20260302_031_protecao_civil_despachos_atendimentos.py
│   │   │       ├── 20260302_032_ciencia_pesquisa_foundation.py
│   │   │       ├── 20260303_033_juventude_risco_evasao.py
│   │   │       ├── 20260303_034_juventude_expansao_slices.py
│   │   │       ├── 20260304_035_gestao_fundiaria_orm_core.py
│   │   │       ├── 20260304_036_urbanismo_habitacao_orm_core.py
│   │   │       ├── 20260304_037_obras_publicas_orm_core.py
│   │   │       ├── 20260304_038_transportes_logistica_orm_core.py
│   │   │       ├── 20260304_039_transportes_logistica_linhas_bilhetagem.py
│   │   │       ├── 20260304_040_aguas_saneamento_outbox_events.py
│   │   │       ├── 20260304_041_energia_outbox_events.py
│   │   │       ├── 20260304_042_obras_publicas_outbox_events.py
│   │   │       ├── 20260305_043_obras_publicas_saga_cqrs.py
│   │   │       ├── 20260305_044_obras_publicas_dashboard_projection_offsets.py
│   │   │       ├── 20260305_045_obras_publicas_event_sourcing_governance.py
│   │   │       ├── 20260305_046_cultura_slice3_espacos_projetos_editais.py
│   │   │       ├── 20260305_047_estatistica_enterprise_foundation.py
│   │   │       ├── 20260305_047_familia_foundation.py
│   │   │       ├── 20260305_048_justica_add_materia_processual.py
│   │   │       ├── 20260305_048_meteorologia_foundation.py
│   │   │       ├── 20260306_049_patrimonio_cultural_foundation.py
│   │   │       ├── 20260306_050_defesa_consumidor_reclamacoes.py
│   │   │       ├── 20260313_051_energy_logistics_justice_pillars.py
│   │   │       ├── 2026_03_03_1304-3261f0e24605_modulo_juventude.py
│   │   │       ├── 2026_03_08_0847-47abb2f40d12_taxation_domain.py
│   │   │       ├── add_import_audit_table.py
│   │   │       └── add_import_batch_id_to_territory.py
│   │   ├── alembic.ini
│   │   ├── analyze_duplicates.py
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   ├── api
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── deps.py
│   │   │   │   ├── middleware
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── role_router.py
│   │   │   │   └── router.py
│   │   │   ├── config.py
│   │   │   ├── conftest.py
│   │   │   ├── conftest_auth.py
│   │   │   ├── core
│   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   ├── AUDIT_REPORT.json
│   │   │   │   ├── __init__.py
│   │   │   │   ├── audit
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── analytics.py
│   │   │   │   │   ├── audit_logger.py
│   │   │   │   │   └── sla_definitions.py
│   │   │   │   ├── audit_compliance.py
│   │   │   │   ├── auth_gateway
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── rate_limiter.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── services
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── service_token_service.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── gateway.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── cache
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── permission_cache.py
│   │   │   │   │   │   └── security
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── auth_resilience.py
│   │   │   │   │   │       └── jwt_engine.py
│   │   │   │   │   ├── middleware
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── auth_middleware.py
│   │   │   │   │   ├── policy_enforcement
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── policy_engine.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── request_authenticator
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── request_authenticator.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── service_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service_identity_manager.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── token_introspection
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── token_introspection.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── autonomous_economic_engine
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── economic_engine.py
│   │   │   │   │   ├── markets
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── market_model.py
│   │   │   │   │   └── policies
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── economic_policy.py
│   │   │   │   ├── autonomous_government_agents
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── agents
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── agent.py
│   │   │   │   │   ├── execution
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── agent_executor.py
│   │   │   │   │   └── registry
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── agent_registry.py
│   │   │   │   ├── autonomous_state
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── autonomous_government_agents
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── agent.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── digital_twin_country
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── digital_twin.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── engine.py
│   │   │   │   │   ├── national_policy_engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── policy_engine.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── strategic_decision_ai
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── decision_ai.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── bridges
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── citizen_repository_bridge.py
│   │   │   │   │   ├── citizen_repository_port_bridge.py
│   │   │   │   │   ├── civil_identity_bridge.py
│   │   │   │   │   ├── cross_domain_ports_bridge.py
│   │   │   │   │   ├── emprego_bridge.py
│   │   │   │   │   ├── finance_bridge.py
│   │   │   │   │   ├── governance_service_requests_bridge.py
│   │   │   │   │   ├── identity_bridge.py
│   │   │   │   │   ├── infrastructure_sector_bridge.py
│   │   │   │   │   ├── intelligence_bi_sources_bridge.py
│   │   │   │   │   ├── justice_public_safety_bridge.py
│   │   │   │   │   ├── resources_agricultura_bridge.py
│   │   │   │   │   ├── resources_external_services_bridge.py
│   │   │   │   │   ├── service_requests_bridge.py
│   │   │   │   │   ├── society_domain_enums_bridge.py
│   │   │   │   │   ├── society_repository_bridges.py
│   │   │   │   │   └── society_statistics_models_bridge.py
│   │   │   │   ├── business
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── models
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── business.py
│   │   │   │   ├── cache
│   │   │   │   │   └── service.py
│   │   │   │   ├── catalog
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── blueprint.py
│   │   │   │   │   └── models
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── module.py
│   │   │   │   │       └── service.py
│   │   │   │   ├── celery
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── app.py
│   │   │   │   ├── cloud_control
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── autonomous_resource_scheduler
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── scheduler.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── control_plane.py
│   │   │   │   │   ├── government_cloud_api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── cloud_api.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── national_container_orchestrator
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── orchestrator.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── sovereign_compute_grid
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── compute_grid.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── communication
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── config
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── constants.py
│   │   │   │   ├── data_exchange
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── cross_ministry_data_fabric
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── government_service_registry
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── secure_data_channels
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── sovereign_xroad
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── data_platform
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── ai_training_pipeline
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── training_pipeline.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── national_data_lake
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── data_lake.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── platform.py
│   │   │   │   │   ├── real_time_data_stream
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── event_stream.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── sovereign_data_warehouse
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── warehouse.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── database
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── repositories
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── base_repository.py
│   │   │   │   │   ├── session.py
│   │   │   │   │   └── uow
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── unit_of_work.py
│   │   │   │   ├── db
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   └── base_class.py
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── dev_platform
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── architecture_guard
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── guard.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── module_generator
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── module_generator.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── platform.py
│   │   │   │   │   ├── policy_linter
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── linter.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── service_scaffolder
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── scaffolder.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── document
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── storage
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── local_storage.py
│   │   │   │   │   ├── models
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── document_file.py
│   │   │   │   │   └── services
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── document_service.py
│   │   │   │   ├── domain
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base_aggregate.py
│   │   │   │   │   └── user_aggregate.py
│   │   │   │   ├── enums.py
│   │   │   │   ├── events
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── adapters
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── event_bus_adapter.py
│   │   │   │   │   ├── aggregates
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── audit_chain
│   │   │   │   │   │   ├── audit_event.py
│   │   │   │   │   │   ├── audit_ledger.py
│   │   │   │   │   │   └── hash_chain.py
│   │   │   │   │   ├── base_event.py
│   │   │   │   │   ├── bridge
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── event_bus_bridge.py
│   │   │   │   │   ├── broker
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── redis_broker.py
│   │   │   │   │   │   └── redis_stream_broker.py
│   │   │   │   │   ├── bus
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── event_bus_v2.py
│   │   │   │   │   ├── bus.py
│   │   │   │   │   ├── bus_enhanced.py
│   │   │   │   │   ├── config.py
│   │   │   │   │   ├── cqrs
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── bus
│   │   │   │   │   │   │   ├── command_bus.py
│   │   │   │   │   │   │   └── query_bus.py
│   │   │   │   │   │   ├── commands
│   │   │   │   │   │   │   └── command.py
│   │   │   │   │   │   ├── handlers
│   │   │   │   │   │   │   ├── command_handler.py
│   │   │   │   │   │   │   └── query_handler.py
│   │   │   │   │   │   ├── queries
│   │   │   │   │   │   │   └── query.py
│   │   │   │   │   │   └── registry.py
│   │   │   │   │   ├── decorators
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── publish.py
│   │   │   │   │   ├── event_versioning
│   │   │   │   │   │   ├── event_upcaster.py
│   │   │   │   │   │   └── version_registry.py
│   │   │   │   │   ├── exceptions.py
│   │   │   │   │   ├── handlers
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── event_handler.py
│   │   │   │   │   │   └── example_handlers.py
│   │   │   │   │   ├── migrations
│   │   │   │   │   │   └── 001_create_outbox_table.py
│   │   │   │   │   ├── models
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── event.py
│   │   │   │   │   │   └── user_events.py
│   │   │   │   │   ├── multi_region_replication
│   │   │   │   │   │   ├── region_node.py
│   │   │   │   │   │   └── replication_manager.py
│   │   │   │   │   ├── orchestrator
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── saga_orchestrator.py
│   │   │   │   │   ├── outbox
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── outbox_model.py
│   │   │   │   │   │   ├── outbox_publisher.py
│   │   │   │   │   │   └── outbox_repository.py
│   │   │   │   │   ├── ports
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── event_bus_port.py
│   │   │   │   │   ├── projection
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── base_projection.py
│   │   │   │   │   │   └── projection_manager.py
│   │   │   │   │   ├── projections
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── registry.py
│   │   │   │   │   │   └── user_projection.py
│   │   │   │   │   ├── registry
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── handler_registry.py
│   │   │   │   │   ├── replay
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── engine.py
│   │   │   │   │   │   └── event_replay.py
│   │   │   │   │   ├── saga
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── saga.py
│   │   │   │   │   │   ├── saga_registry.py
│   │   │   │   │   │   └── saga_state.py
│   │   │   │   │   ├── setup.py
│   │   │   │   │   ├── snapshots
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── snapshot_engine.py
│   │   │   │   │   │   └── snapshot_manager.py
│   │   │   │   │   ├── store
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── event_repository.py
│   │   │   │   │   │   ├── event_store.py
│   │   │   │   │   │   ├── models.py
│   │   │   │   │   │   ├── repositories.py
│   │   │   │   │   │   └── sqlalchemy_repository.py
│   │   │   │   │   ├── test_event_bus.py
│   │   │   │   │   ├── types.py
│   │   │   │   │   └── workers
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── event_worker.py
│   │   │   │   │       ├── outbox_worker.py
│   │   │   │   │       └── projection_worker.py
│   │   │   │   ├── exceptions
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── base.py
│   │   │   │   ├── feature_flags
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── service.py
│   │   │   │   ├── global_governance_protocol
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── consensus
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── global_consensus.py
│   │   │   │   │   ├── identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── global_identity.py
│   │   │   │   │   └── treaties
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── treaty_model.py
│   │   │   │   ├── governance
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── governance_ai
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── crisis_response_ai
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── crisis_engine.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── economic_forecasting
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── economic_forecaster.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── engine.py
│   │   │   │   │   ├── national_risk_model
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── risk_engine.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── policy_simulation
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── policy_simulator.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── identity
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── context.py
│   │   │   │   ├── integration
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── integrations
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── fuc_client.py
│   │   │   │   ├── intelligence
│   │   │   │   │   ├── behavioral_ai
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── behavior_model.py
│   │   │   │   │   ├── crisis_prediction
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── crisis_engine.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── intelligence_event.py
│   │   │   │   │   ├── economic_simulation
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── economy_model.py
│   │   │   │   │   ├── national_analytics
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── analytics_engine.py
│   │   │   │   │   └── predictive_governance
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── application
│   │   │   │   │           ├── __init__.py
│   │   │   │   │           └── policy_predictor.py
│   │   │   │   ├── locks
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── manager.py
│   │   │   │   ├── models
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── module_manifest.py
│   │   │   │   ├── module_registry.py
│   │   │   │   ├── monitoring
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── national_ai_superintelligence
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── ai_engine.py
│   │   │   │   │   ├── knowledge
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── knowledge_graph.py
│   │   │   │   │   ├── learning
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── training_pipeline.py
│   │   │   │   │   └── models
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── ai_model.py
│   │   │   │   ├── notifications
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── models
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── notification.py
│   │   │   │   │   └── services
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── notification_service.py
│   │   │   │   ├── observability
│   │   │   │   │   ├── MIDDLEWARE_NOTE.txt
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── alert_handler.py
│   │   │   │   │   ├── anomaly_detector.py
│   │   │   │   │   ├── anomaly_monitoring
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── anomaly_detector.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── audit_auth.py
│   │   │   │   │   ├── context.py
│   │   │   │   │   ├── distributed_tracing
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── tracer.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── enterprise_formatter.py
│   │   │   │   │   ├── enterprise_logging.py
│   │   │   │   │   ├── logging_config.py
│   │   │   │   │   ├── middleware.py
│   │   │   │   │   ├── national_logging_grid
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── national_logger.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── otel_integration.py
│   │   │   │   │   ├── platform.py
│   │   │   │   │   ├── sovereign_metrics
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── metrics_registry.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   └── test_observability_validation.py
│   │   │   │   ├── planetary_civilization_model
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── civilization_engine.py
│   │   │   │   │   ├── models
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── civilization_entity.py
│   │   │   │   │   │   └── civilization_event.py
│   │   │   │   │   └── simulation
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── civilization_simulator.py
│   │   │   │   ├── planetary_policy_optimizer
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── metrics
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── policy_metrics.py
│   │   │   │   │   ├── models
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── policy_model.py
│   │   │   │   │   └── optimizer
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── policy_optimizer.py
│   │   │   │   ├── platform
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── quantum_internet_integration
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── crypto
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── quantum_key_exchange.py
│   │   │   │   │   ├── network
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── quantum_node.py
│   │   │   │   │   └── transport
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── quantum_transport.py
│   │   │   │   ├── rate_limit
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── limiter.py
│   │   │   │   ├── rbac
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── territorial_access.py
│   │   │   │   ├── registry
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── resilience
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── circuit_breaker.py
│   │   │   │   │   ├── circuit_breaker_patterns.py
│   │   │   │   │   ├── config.py
│   │   │   │   │   ├── decorators.py
│   │   │   │   │   ├── exceptions.py
│   │   │   │   │   ├── http_client.py
│   │   │   │   │   ├── policy.py
│   │   │   │   │   ├── registry.py
│   │   │   │   │   └── state.py
│   │   │   │   ├── schemas
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── user.py
│   │   │   │   ├── security
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── anomaly_detection
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── anomaly_engine.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── security_middleware.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── security_event.py
│   │   │   │   │   ├── fraud_detection
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── fraud_engine.py
│   │   │   │   │   ├── national_soc
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── soc_monitor.py
│   │   │   │   │   ├── runtime_policy_enforcement
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── runtime_policy_engine.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── service_mutual_tls
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── mtls_service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── threat_detection
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── threat_engine.py
│   │   │   │   │   ├── workload_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── workload_identity_service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── zero_trust_engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── application
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── zero_trust.py
│   │   │   │   │   └── zero_trust_gateway
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── zero_trust_gateway.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── sequencing.py
│   │   │   │   ├── services
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base_request_service.py
│   │   │   │   │   └── base_request_service_diagrams.py
│   │   │   │   ├── settings.py
│   │   │   │   ├── sila_os
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── autonomous_deployment
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── deployer.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── government_sdk
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── sdk.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── national_cli
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── cli.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── os.py
│   │   │   │   │   └── service_portal
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── portal.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── sovereign_infrastructure
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── autonomous_scaling
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── national_service_mesh
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── planetary_edge_network
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   └── sovereign_api_fabric
│   │   │   │   │       └── __init__.py
│   │   │   │   ├── sovereign_quantum_security
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── crypto
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── post_quantum_crypto.py
│   │   │   │   │   ├── key_management
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── key_manager.py
│   │   │   │   │   └── verification
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── signature_verifier.py
│   │   │   │   ├── tenants
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── territory
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── models
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   └── territory.py
│   │   │   │   │   └── service.py
│   │   │   │   ├── use-cases
│   │   │   │   ├── utils
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── dates.py
│   │   │   │   │   ├── hashing.py
│   │   │   │   │   ├── identity_safe.py
│   │   │   │   │   └── parsing.py
│   │   │   │   ├── validate_refactor_simple.py
│   │   │   │   └── workflow
│   │   │   │       ├── __init__.py
│   │   │   │       ├── infrastructure
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   └── repositories
│   │   │   │       │       ├── __init__.py
│   │   │   │       │       └── request_repository.py
│   │   │   │       └── models
│   │   │   │           ├── __init__.py
│   │   │   │           ├── process.py
│   │   │   │           ├── request.py
│   │   │   │           └── workflow.py
│   │   │   ├── db
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── migrations
│   │   │   │   │   └── versions
│   │   │   │   │       ├── 001_001_create_workflow_tables.py
│   │   │   │   │       ├── 002_003_create_request_events.py
│   │   │   │   │       ├── 003_002_create_attachments.py
│   │   │   │   │       ├── 004_001_create_service_requests.py
│   │   │   │   │       ├── 005_002_create_payments_table.py
│   │   │   │   │       ├── 006_004_add_citizen_id_to_invoices.py
│   │   │   │   │       ├── 007_001_create_invoices_table.py
│   │   │   │   │       ├── 008_003_create_audit_logs_table.py
│   │   │   │   │       ├── 009_001_create_health_tables.py
│   │   │   │   │       ├── 010_002_add_health_indexes.py
│   │   │   │   │       ├── 011_001_create_operational_flow_tables.py
│   │   │   │   │       └── 012_001_expand_service_catalog_governance.py
│   │   │   │   └── seeds
│   │   │   ├── infrastructure
│   │   │   │   └── repositories
│   │   │   │       └── citizen_repository.py
│   │   │   ├── main.py
│   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   └── iam_user.py
│   │   │   ├── modules
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── router.py
│   │   │   │   ├── audit
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── state_audit
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── commands
│   │   │   │   │       │   ├── dto
│   │   │   │   │       │   └── services
│   │   │   │   │       ├── domain
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── entities
│   │   │   │   │       │   ├── repositories
│   │   │   │   │       │   ├── services
│   │   │   │   │       │   └── value_objects
│   │   │   │   │       ├── health.py
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── orm
│   │   │   │   │       │   └── repositories
│   │   │   │   │       ├── module.py
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       └── tests
│   │   │   │   │           └── test_state_audit_flow.py
│   │   │   │   ├── civil_protection
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── atendimentos.py
│   │   │   │   │   │   │   ├── bombeiros.py
│   │   │   │   │   │   │   ├── corporacoes.py
│   │   │   │   │   │   │   ├── despachos.py
│   │   │   │   │   │   │   └── ocorrencias_emergenciais.py
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   └── schemas
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── atendimento_schema.py
│   │   │   │   │   │       ├── bombeiro_schema.py
│   │   │   │   │   │       ├── corporacao_schema.py
│   │   │   │   │   │       ├── despacho_schema.py
│   │   │   │   │   │       └── ocorrencia_emergencial_schema.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── atendimento_repository_port.py
│   │   │   │   │   │   │   ├── bombeiro_repository_port.py
│   │   │   │   │   │   │   ├── corporacao_repository_port.py
│   │   │   │   │   │   │   ├── despacho_repository_port.py
│   │   │   │   │   │   │   ├── ocorrencia_emergencial_repository_port.py
│   │   │   │   │   │   │   └── request_service_port.py
│   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   └── services
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── atendimento_service.py
│   │   │   │   │   │       ├── bombeiro_service.py
│   │   │   │   │   │       ├── corporacao_service.py
│   │   │   │   │   │       ├── despacho_service.py
│   │   │   │   │   │       └── ocorrencia_emergencial_service.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── models
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── atendimento.py
│   │   │   │   │   │       ├── bombeiro.py
│   │   │   │   │   │       ├── corporacao.py
│   │   │   │   │   │       ├── despacho.py
│   │   │   │   │   │       └── ocorrencia_emergencial.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── request_service_adapter.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── atendimento_model.py
│   │   │   │   │   │   │   ├── bombeiro_model.py
│   │   │   │   │   │   │   ├── corporacao_model.py
│   │   │   │   │   │   │   ├── despacho_model.py
│   │   │   │   │   │   │   └── ocorrencia_emergencial_model.py
│   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── sqlalchemy_atendimento_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_bombeiro_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_corporacao_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_despacho_repository.py
│   │   │   │   │   │   │   └── sqlalchemy_ocorrencia_emergencial_repository.py
│   │   │   │   │   │   └── repository.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── _fakes.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       ├── test_atendimentos.py
│   │   │   │   │       ├── test_bombeiros.py
│   │   │   │   │       ├── test_corporacoes.py
│   │   │   │   │       ├── test_despachos.py
│   │   │   │   │       ├── test_ocorrencias_emergenciais.py
│   │   │   │   │       └── test_orm_integration_real.py
│   │   │   │   ├── compliance
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── service.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── repository.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── conftest.py
│   │   │   │   ├── documents
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── infrastructure
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── economy
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── apoio_empresarial
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── commands.py
│   │   │   │   │   │   │   ├── handlers.py
│   │   │   │   │   │   │   ├── invoice_service.py
│   │   │   │   │   │   │   ├── payment_service.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── enums
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── mocks
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── integrations
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── fuc_client.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── public_budget
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── policies.py
│   │   │   │   │   │   │   └── services.py
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── taxpayer
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── middleware.py
│   │   │   │   │   │   │   ├── openapi.py
│   │   │   │   │   │   │   ├── rate_limiter.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   ├── schemas
│   │   │   │   │   │   │   └── schemas.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── commands
│   │   │   │   │   │   │   ├── dto
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── queries
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── aggregate_entities.py
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── enums
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── interfaces
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── api
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── tests
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── trade
│   │   │   │   │       ├── ARCHITECTURE.md
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── exceptions.py
│   │   │   │   │       ├── external
│   │   │   │   │       │   ├── ARCHITECTURE.md
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── api
│   │   │   │   │       │   ├── application
│   │   │   │   │       │   ├── domain
│   │   │   │   │       │   ├── exceptions.py
│   │   │   │   │       │   ├── infrastructure
│   │   │   │   │       │   ├── module.yaml
│   │   │   │   │       │   └── tests
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       ├── services
│   │   │   │   │       │   ├── ARCHITECTURE.md
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── api
│   │   │   │   │       │   ├── application
│   │   │   │   │       │   ├── domain
│   │   │   │   │       │   ├── exceptions.py
│   │   │   │   │       │   ├── infrastructure
│   │   │   │   │       │   ├── module.yaml
│   │   │   │   │       │   └── tests
│   │   │   │   │       └── tests
│   │   │   │   ├── educacao
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _workflow_endpoints.py
│   │   │   │   │   │   │   ├── boletins.py
│   │   │   │   │   │   │   ├── certificados.py
│   │   │   │   │   │   │   ├── concursos.py
│   │   │   │   │   │   │   ├── emprego.py
│   │   │   │   │   │   │   ├── formacoes.py
│   │   │   │   │   │   │   ├── inscricoes.py
│   │   │   │   │   │   │   ├── matricula_routes.py
│   │   │   │   │   │   │   ├── propinas.py
│   │   │   │   │   │   │   ├── transferencias.py
│   │   │   │   │   │   │   └── universidade.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   └── schemas
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── boletim_schema.py
│   │   │   │   │   │       ├── certificado_schema.py
│   │   │   │   │   │       ├── concurso_schema.py
│   │   │   │   │   │       ├── emprego_schema.py
│   │   │   │   │   │       ├── escola_schema.py
│   │   │   │   │   │       ├── formacao_schema.py
│   │   │   │   │   │       ├── inscricao_schema.py
│   │   │   │   │   │       ├── matricula_schema.py
│   │   │   │   │   │       ├── propina_schema.py
│   │   │   │   │   │       ├── transferencia_schema.py
│   │   │   │   │   │       ├── universidade_schema.py
│   │   │   │   │   │       └── workflow_schema.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── handlers.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── boletim_repository_port.py
│   │   │   │   │   │   │   ├── certificado_repository_port.py
│   │   │   │   │   │   │   ├── concurso_repository_port.py
│   │   │   │   │   │   │   ├── emprego_repository_port.py
│   │   │   │   │   │   │   ├── escola_repository_port.py
│   │   │   │   │   │   │   ├── formacao_repository_port.py
│   │   │   │   │   │   │   ├── inscricao_repository_port.py
│   │   │   │   │   │   │   ├── matricula_repository_port.py
│   │   │   │   │   │   │   ├── propina_repository_port.py
│   │   │   │   │   │   │   ├── transferencia_repository_port.py
│   │   │   │   │   │   │   ├── turma_repository_port.py
│   │   │   │   │   │   │   ├── universidade_repository_port.py
│   │   │   │   │   │   │   └── workflow_repository_port.py
│   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   └── services
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── matricula_service.py
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── boletim_service.py
│   │   │   │   │   │   │   ├── certificado_service.py
│   │   │   │   │   │   │   ├── concurso_service.py
│   │   │   │   │   │   │   ├── emprego_service.py
│   │   │   │   │   │   │   ├── formacao_service.py
│   │   │   │   │   │   │   ├── inscricao_service.py
│   │   │   │   │   │   │   ├── matricula_service.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── propina_service.py
│   │   │   │   │   │   │   ├── transferencia_service.py
│   │   │   │   │   │   │   ├── universidade_service.py
│   │   │   │   │   │   │   └── workflow_service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _workflow_record.py
│   │   │   │   │   │   │   ├── acreditacao_universitaria.py
│   │   │   │   │   │   │   ├── alfabetizacao.py
│   │   │   │   │   │   │   ├── ano_letivo.py
│   │   │   │   │   │   │   ├── apoio_alimentar.py
│   │   │   │   │   │   │   ├── apoio_alimentar_escolar.py
│   │   │   │   │   │   │   ├── avaliacao.py
│   │   │   │   │   │   │   ├── avaliacao_desempenho.py
│   │   │   │   │   │   │   ├── avaliacao_institucional.py
│   │   │   │   │   │   │   ├── boletim.py
│   │   │   │   │   │   │   ├── bolsa_candidatura.py
│   │   │   │   │   │   │   ├── bolsa_investigacao.py
│   │   │   │   │   │   │   ├── candidato_emprego.py
│   │   │   │   │   │   │   ├── cantina.py
│   │   │   │   │   │   │   ├── capacitacao_qualidade.py
│   │   │   │   │   │   │   ├── certificacao_competencias.py
│   │   │   │   │   │   │   ├── certificacao_profissional.py
│   │   │   │   │   │   │   ├── certificado_conclusao.py
│   │   │   │   │   │   │   ├── certificado_universitario.py
│   │   │   │   │   │   │   ├── concurso_inscricao.py
│   │   │   │   │   │   │   ├── concurso_resultado.py
│   │   │   │   │   │   │   ├── credenciamento.py
│   │   │   │   │   │   │   ├── declaracao_desemprego.py
│   │   │   │   │   │   │   ├── declaracao_escolar.py
│   │   │   │   │   │   │   ├── educacao_comunitaria.py
│   │   │   │   │   │   │   ├── educacao_especial.py
│   │   │   │   │   │   │   ├── escola.py
│   │   │   │   │   │   │   ├── estagio_publico.py
│   │   │   │   │   │   │   ├── estatistica_superior.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── fiscalizacao_trabalho.py
│   │   │   │   │   │   │   ├── formacao_avancada.py
│   │   │   │   │   │   │   ├── formacao_certificada.py
│   │   │   │   │   │   │   ├── formacao_gestores.py
│   │   │   │   │   │   │   ├── formacao_profissional.py
│   │   │   │   │   │   │   ├── historico_escolar.py
│   │   │   │   │   │   │   ├── inscricao_basica.py
│   │   │   │   │   │   │   ├── inscricao_secundaria.py
│   │   │   │   │   │   │   ├── inscricao_superior.py
│   │   │   │   │   │   │   ├── inscricao_tecnico.py
│   │   │   │   │   │   │   ├── matricula.py
│   │   │   │   │   │   │   ├── matricula_universidade.py
│   │   │   │   │   │   │   ├── mediacao_conflito.py
│   │   │   │   │   │   │   ├── mediacao_emprego.py
│   │   │   │   │   │   │   ├── mobilidade_academica.py
│   │   │   │   │   │   │   ├── mobilidade_publica.py
│   │   │   │   │   │   │   ├── oferta_emprego.py
│   │   │   │   │   │   │   ├── parceria_universidade.py
│   │   │   │   │   │   │   ├── propina.py
│   │   │   │   │   │   │   ├── reclamacao_trabalhista.py
│   │   │   │   │   │   │   ├── reconhecimento_diploma.py
│   │   │   │   │   │   │   ├── reconhecimento_grau.py
│   │   │   │   │   │   │   ├── reconversao.py
│   │   │   │   │   │   │   ├── registo_contrato.py
│   │   │   │   │   │   │   ├── transferencia.py
│   │   │   │   │   │   │   ├── transferencia_universitaria.py
│   │   │   │   │   │   │   ├── turma.py
│   │   │   │   │   │   │   └── vaga.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── entities
│   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── ano_letivo.py
│   │   │   │   │   │   └── value_objects
│   │   │   │   │   ├── exceptions.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ano_letivo_model.py
│   │   │   │   │   │   │   ├── boletim_model.py
│   │   │   │   │   │   │   ├── certificado_model.py
│   │   │   │   │   │   │   ├── concurso_model.py
│   │   │   │   │   │   │   ├── emprego_model.py
│   │   │   │   │   │   │   ├── escola_model.py
│   │   │   │   │   │   │   ├── formacao_model.py
│   │   │   │   │   │   │   ├── inscricao_model.py
│   │   │   │   │   │   │   ├── matricula_model.py
│   │   │   │   │   │   │   ├── propina_model.py
│   │   │   │   │   │   │   ├── transferencia_model.py
│   │   │   │   │   │   │   ├── turma_model.py
│   │   │   │   │   │   │   └── universidade_model.py
│   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _workflow_sqlalchemy_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_boletim_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_certificado_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_concurso_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_emprego_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_escola_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_formacao_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_inscricao_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_matricula_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_propina_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_transferencia_repository.py
│   │   │   │   │   │   │   ├── sqlalchemy_turma_repository.py
│   │   │   │   │   │   │   └── sqlalchemy_universidade_repository.py
│   │   │   │   │   │   └── repository.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       ├── test_boletim.py
│   │   │   │   │       ├── test_certificado.py
│   │   │   │   │       ├── test_concurso.py
│   │   │   │   │       ├── test_emprego.py
│   │   │   │   │       ├── test_formacao.py
│   │   │   │   │       ├── test_inscricao.py
│   │   │   │   │       ├── test_matricula.py
│   │   │   │   │       ├── test_propina.py
│   │   │   │   │       ├── test_transferencia.py
│   │   │   │   │       └── test_universidade.py
│   │   │   │   ├── energy
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── central_geradora.py
│   │   │   │   │   │   │   ├── consumo.py
│   │   │   │   │   │   │   ├── faturas.py
│   │   │   │   │   │   │   ├── geracao.py
│   │   │   │   │   │   │   ├── linha_transmissao.py
│   │   │   │   │   │   │   ├── subestacao.py
│   │   │   │   │   │   │   └── usinas.py
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   └── schemas
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── central_geradora_schema.py
│   │   │   │   │   │       ├── consumo_schema.py
│   │   │   │   │   │       ├── dashboard_schema.py
│   │   │   │   │   │       ├── fatura_schema.py
│   │   │   │   │   │       ├── linha_transmissao_schema.py
│   │   │   │   │   │       ├── subestacao_schema.py
│   │   │   │   │   │       └── usina_schema.py
│   │   │   │   │   ├── billing
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── consumo_energia.py
│   │   │   │   │   │   │   └── fatura_energia.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── commands
│   │   │   │   │   │   │   ├── dto
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── handlers
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── services
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── adapters
│   │   │   │   │   │       ├── models
│   │   │   │   │   │       ├── orm
│   │   │   │   │   │       ├── persistence
│   │   │   │   │   │       ├── repositories
│   │   │   │   │   │       └── resilience
│   │   │   │   │   ├── distribution
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── linha_transmissao.py
│   │   │   │   │   │   │   └── subestacao.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── generation
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── central_geradora.py
│   │   │   │   │   │   │   └── usina.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── governance
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── administracao_local
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── commands.py
│   │   │   │   │   │   │   ├── dto.py
│   │   │   │   │   │   │   ├── queries.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── value_objects.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── mappers.py
│   │   │   │   │   │   │   ├── models.py
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── presentation
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── dependencies.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas.py
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── cooperacao_internacional
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── README.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── repository.py
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── test_acordo_visto_services.py
│   │   │   │   │   │   │   └── test_cooperacao_api.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── tratado_monitor_worker.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── planeamento
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── service_requests
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── clients
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── integrations
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── workflow_client.py
│   │   │   │   │   │   ├── interfaces
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── api
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_attachments.py
│   │   │   │   │   │       ├── test_domain_clients_orm_integration.py
│   │   │   │   │   │       ├── test_request_service_domain_clients.py
│   │   │   │   │   │       ├── test_requests.py
│   │   │   │   │   │       └── test_workflow_integration.py
│   │   │   │   │   ├── statistics
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── bus.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── handlers
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── config.py
│   │   │   │   │   │   ├── data_sources
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── base_data_source.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── bus.py
│   │   │   │   │   │   │   └── definitions.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── repository.py
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── integrations
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── assistencia_data_source.py
│   │   │   │   │   │   │   ├── base_data_source.py
│   │   │   │   │   │   │   ├── bi_connector.py
│   │   │   │   │   │   │   ├── data_sources.py
│   │   │   │   │   │   │   ├── educacao_data_source.py
│   │   │   │   │   │   │   ├── emprego_data_source.py
│   │   │   │   │   │   │   ├── identidade_data_source.py
│   │   │   │   │   │   │   ├── juventude_data_source.py
│   │   │   │   │   │   │   ├── saude_data_source.py
│   │   │   │   │   │   │   ├── service_requests_data_source.py
│   │   │   │   │   │   │   └── workflow_data_source.py
│   │   │   │   │   │   ├── interfaces
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── api
│   │   │   │   │   │   ├── kpis_service.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── resilience
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── circuit_breaker.py
│   │   │   │   │   │   │   └── retry.py
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _fakes.py
│   │   │   │   │   │   │   ├── conftest.py
│   │   │   │   │   │   │   ├── test_aggregation.py
│   │   │   │   │   │   │   ├── test_agregacoes.py
│   │   │   │   │   │   │   ├── test_alertas.py
│   │   │   │   │   │   │   ├── test_analises.py
│   │   │   │   │   │   │   ├── test_comparativos.py
│   │   │   │   │   │   │   ├── test_dashboards.py
│   │   │   │   │   │   │   ├── test_e2e_fluxo_completo.py
│   │   │   │   │   │   │   ├── test_exportacoes.py
│   │   │   │   │   │   │   ├── test_forecasting.py
│   │   │   │   │   │   │   ├── test_indicadores.py
│   │   │   │   │   │   │   ├── test_integracao_multimodulo_orm.py
│   │   │   │   │   │   │   ├── test_kpis.py
│   │   │   │   │   │   │   ├── test_metricas.py
│   │   │   │   │   │   │   ├── test_previsoes.py
│   │   │   │   │   │   │   ├── test_rankings.py
│   │   │   │   │   │   │   ├── test_relatorios.py
│   │   │   │   │   │   │   ├── test_statistics_service.py
│   │   │   │   │   │   │   ├── test_tendencias.py
│   │   │   │   │   │   │   └── test_timeseries.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── agregacao_worker.py
│   │   │   │   │   │       ├── kpi_calculation_worker.py
│   │   │   │   │   │       ├── outbox_worker.py
│   │   │   │   │   │       ├── relatorio_worker.py
│   │   │   │   │   │       └── timeseries_worker.py
│   │   │   │   │   ├── tests
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── workflow
│   │   │   │   │       ├── ARCHITECTURE.md
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── deps.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   ├── router.py
│   │   │   │   │       │   └── schemas
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── ports
│   │   │   │   │       │   └── services
│   │   │   │   │       ├── domain
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── enums.py
│   │   │   │   │       │   ├── exceptions.py
│   │   │   │   │       │   └── models
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── adapters
│   │   │   │   │       │   ├── models
│   │   │   │   │       │   ├── persistence
│   │   │   │   │       │   └── repositories
│   │   │   │   │       ├── integrations
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── notification_client.py
│   │   │   │   │       ├── interfaces
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── api
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       └── tests
│   │   │   │   │           ├── __init__.py
│   │   │   │   │           ├── test_di_runtime_adapters.py
│   │   │   │   │           ├── test_engine.py
│   │   │   │   │           ├── test_transitions.py
│   │   │   │   │           ├── test_workflow_e2e.py
│   │   │   │   │           └── test_workflow_endpoints_testclient.py
│   │   │   │   ├── identity
│   │   │   │   │   ├── _deprecated
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── credential_management
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── sovereign_identity_wallet
│   │   │   │   │   │       ├── application
│   │   │   │   │   │       ├── domain
│   │   │   │   │   │       └── infrastructure
│   │   │   │   │   ├── biometric_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── bounded_contexts
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── access_control
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── iam
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── application
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── citizen_digital_wallet
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── citizen_identity_graph
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── identity_graph_service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       └── __init__.py
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       ├── legacy_adapters
│   │   │   │   │   │       ├── models
│   │   │   │   │   │       └── repositories
│   │   │   │   │   ├── cross_border_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── decentralized_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── device_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── digital_signature_service
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── trust_score.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── user_model.py
│   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── citizen_repository.py
│   │   │   │   │   │   │   └── user_repository.py
│   │   │   │   │   │   └── security
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── jwt_engine.py
│   │   │   │   │   ├── legal_signature_validation
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── middleware
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── trust_middleware.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── national_certificate_authority
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── national_login
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── oidc_provider
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── oidc_service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── permission_graph
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── policy_evaluator
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── role_engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── saml_gateway
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── smartcard_identity
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── sovereign_access_control
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── sovereign_trust_engine
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── tests
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── test_oidc_service.py
│   │   │   │   │   │   ├── test_vc_issuance.py
│   │   │   │   │   │   └── test_vc_revocation.py
│   │   │   │   │   └── verifiable_credentials
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   └── services
│   │   │   │   │       ├── domain
│   │   │   │   │       │   └── entities
│   │   │   │   │       └── infrastructure
│   │   │   │   │           └── repositories
│   │   │   │   ├── industry
│   │   │   │   │   └── core
│   │   │   │   │       ├── ARCHITECTURE.md
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── deps.py
│   │   │   │   │       │   ├── endpoints
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   ├── router.py
│   │   │   │   │       │   └── schemas
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── ports
│   │   │   │   │       │   └── services
│   │   │   │   │       ├── domain
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── enums.py
│   │   │   │   │       │   ├── exceptions.py
│   │   │   │   │       │   ├── models
│   │   │   │   │       │   └── shared
│   │   │   │   │       ├── exceptions.py
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── adapters
│   │   │   │   │       │   ├── models
│   │   │   │   │       │   └── repositories
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       └── tests
│   │   │   │   │           ├── __init__.py
│   │   │   │   │           ├── conftest.py
│   │   │   │   │           ├── pytest.ini
│   │   │   │   │           ├── run_local_tests.sh
│   │   │   │   │           ├── test_catalogos.py
│   │   │   │   │           └── test_estabelecimentos_industriais.py
│   │   │   │   ├── infrastructure
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── commands
│   │   │   │   │   │   │   ├── dto
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── services
│   │   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       ├── orm
│   │   │   │   │   │       └── repositories
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   └── economy_asset_adapter.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── infrastructure_sector
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── aviacao_civil
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── README.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── repository.py
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── test_aviacao_api.py
│   │   │   │   │   │   │   └── test_voo_service.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── voo_monitor_worker.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── gestao_fundiaria
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_desapropriacoes.py
│   │   │   │   │   │       ├── test_georreferenciamentos.py
│   │   │   │   │   │       ├── test_imoveis.py
│   │   │   │   │   │       ├── test_matriculas.py
│   │   │   │   │   │       ├── test_oneracoes.py
│   │   │   │   │   │       ├── test_orm_integration_real.py
│   │   │   │   │   │       └── test_proprietarios.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── logistica
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   └── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   └── transport
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── infrastructure
│   │   │   │   │   ├── meteorologia
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── integration
│   │   │   │   │   │       └── unit
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── obras_publicas
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── core
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── domain
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── telecomunicacoes
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── handlers
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _fakes.py
│   │   │   │   │   │   │   ├── test_anatel_adapter.py
│   │   │   │   │   │   │   ├── test_assinantes.py
│   │   │   │   │   │   │   ├── test_espectros.py
│   │   │   │   │   │   │   ├── test_indicadores_qualidade.py
│   │   │   │   │   │   │   ├── test_infraestruturas.py
│   │   │   │   │   │   │   ├── test_operadoras.py
│   │   │   │   │   │   │   ├── test_orm_integration_real.py
│   │   │   │   │   │   │   ├── test_outorgas_espectro.py
│   │   │   │   │   │   │   ├── test_qualidade_servico.py
│   │   │   │   │   │   │   └── test_slas.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── anatel_reporter.py
│   │   │   │   │   │       ├── outbox_worker.py
│   │   │   │   │   │       └── qualidade_monitor.py
│   │   │   │   │   ├── tests
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── urbanismo_habitacao
│   │   │   │   │       ├── ARCHITECTURE.md
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── deps.py
│   │   │   │   │       │   ├── endpoints
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   ├── router.py
│   │   │   │   │       │   └── schemas
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── ports
│   │   │   │   │       │   ├── service.py
│   │   │   │   │       │   └── services
│   │   │   │   │       ├── domain
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── entities.py
│   │   │   │   │       │   ├── enums.py
│   │   │   │   │       │   ├── exceptions.py
│   │   │   │   │       │   └── models
│   │   │   │   │       ├── exceptions.py
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── adapters
│   │   │   │   │       │   ├── models
│   │   │   │   │       │   ├── repositories
│   │   │   │   │       │   └── repository.py
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       └── tests
│   │   │   │   │           ├── __init__.py
│   │   │   │   │           ├── test_licencas_urbanisticas.py
│   │   │   │   │           ├── test_loteamentos.py
│   │   │   │   │           ├── test_operacoes_urbanas.py
│   │   │   │   │           ├── test_orm_integration_real.py
│   │   │   │   │           ├── test_parcelamentos.py
│   │   │   │   │           ├── test_planos_diretores.py
│   │   │   │   │           └── test_zoneamento.py
│   │   │   │   ├── intelligence
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── arquivo_nacional
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   ├── routers
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── bi
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── integrations
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── data_sources.py
│   │   │   │   │   │   ├── interfaces
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── api
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── conftest.py
│   │   │   │   │   │       ├── test_dashboard.py
│   │   │   │   │   │       ├── test_data_sources_orm_integration.py
│   │   │   │   │   │       ├── test_kpis.py
│   │   │   │   │   │       └── test_reports.py
│   │   │   │   │   ├── ciencia_pesquisa
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── _fakes.py
│   │   │   │   │   │       ├── test_instituicoes.py
│   │   │   │   │   │       ├── test_pesquisadores.py
│   │   │   │   │   │       ├── test_ports_contratuais.py
│   │   │   │   │   │       └── test_projetos.py
│   │   │   │   │   ├── defesa_consumidor
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── test_e2e_fluxo_completo.py
│   │   │   │   │   │   │   ├── test_mediacoes.py
│   │   │   │   │   │   │   ├── test_orm_integration_real.py
│   │   │   │   │   │   │   └── test_reclamacoes.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── outbox_worker.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── operations
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── state_machine.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── tecnologia_inovacao
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── justice
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── _deprecated
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── bounded_contexts
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── cemetery_management
│   │   │   │   │   │   │   ├── civil_registry_core
│   │   │   │   │   │   │   ├── identity_documents
│   │   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── permissions
│   │   │   │   │   │   │   └── vital_events
│   │   │   │   │   │   ├── civil_registry
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   └── traffic_violation_adapter.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── bi_emission_service.py
│   │   │   │   │   │   │   ├── birth_service.py
│   │   │   │   │   │   │   ├── certificate_service.py
│   │   │   │   │   │   │   ├── citizen_service.py
│   │   │   │   │   │   │   ├── death_service.py
│   │   │   │   │   │   │   ├── document_service.py
│   │   │   │   │   │   │   ├── marriage_service.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── profile_queries.py
│   │   │   │   │   │   │   ├── queries.py
│   │   │   │   │   │   │   ├── routing_engine.py
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── bilhete_identidade.py
│   │   │   │   │   │   │   ├── birth_record.py
│   │   │   │   │   │   │   ├── citizen.py
│   │   │   │   │   │   │   ├── death_record.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── identity_request.py
│   │   │   │   │   │   │   └── marriage_record.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── legacy_adapters
│   │   │   │   │   │   │   └── ports
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── test_sanity.py
│   │   │   │   │   │   └── value_objects
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── nationality.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── events
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── bus.py
│   │   │   │   │   │   ├── definitions.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── exceptions.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── models
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── traffic_violation_model.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── cemetery_management
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       ├── civil_registry_core
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── identity_documents
│   │   │   │   │       │   └── __init__.py
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       ├── test_e2e_civil_registry.py
│   │   │   │   │       └── vital_events
│   │   │   │   │           └── __init__.py
│   │   │   │   ├── logistics
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── commands
│   │   │   │   │   │   │   ├── dto
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── services
│   │   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       ├── orm
│   │   │   │   │   │       └── repositories
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── migration_service
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   └── schemas
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── ports
│   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   └── services
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── models
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── models
│   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   └── repository.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       ├── integration
│   │   │   │   │       └── unit
│   │   │   │   │           └── domain
│   │   │   │   ├── operations
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── services
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── operations_service.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── state_machine.py
│   │   │   │   │   └── infrastructure
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── payment
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── services
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       └── payment_service.py
│   │   │   │   ├── procurement
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── commands
│   │   │   │   │   │   │   ├── dto
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── entities
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── services
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   │       ├── orm
│   │   │   │   │   │       └── repositories
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       └── test_procurement_flow.py
│   │   │   │   ├── public_security
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── cadeias_custodia.py
│   │   │   │   │   │   │   ├── evidencias.py
│   │   │   │   │   │   │   ├── investigacoes.py
│   │   │   │   │   │   │   ├── laudos_periciais.py
│   │   │   │   │   │   │   ├── mandados.py
│   │   │   │   │   │   │   ├── ocorrencias.py
│   │   │   │   │   │   │   ├── policiais.py
│   │   │   │   │   │   │   ├── provas_periciais.py
│   │   │   │   │   │   │   ├── unidades_policiais.py
│   │   │   │   │   │   │   └── vestigios.py
│   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   └── schemas
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── cadeia_custodia_schema.py
│   │   │   │   │   │       ├── evidencia_schema.py
│   │   │   │   │   │       ├── investigacao_schema.py
│   │   │   │   │   │       ├── laudo_pericial_schema.py
│   │   │   │   │   │       ├── mandado_schema.py
│   │   │   │   │   │       ├── ocorrencia_schema.py
│   │   │   │   │   │       ├── policial_schema.py
│   │   │   │   │   │       ├── prova_pericial_schema.py
│   │   │   │   │   │       ├── unidade_policial_schema.py
│   │   │   │   │   │       └── vestigio_schema.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── cadeia_custodia_repository_port.py
│   │   │   │   │   │   │   ├── evidencia_repository_port.py
│   │   │   │   │   │   │   ├── investigacao_repository_port.py
│   │   │   │   │   │   │   ├── laudo_pericial_repository_port.py
│   │   │   │   │   │   │   ├── mandado_repository_port.py
│   │   │   │   │   │   │   ├── ocorrencia_repository_port.py
│   │   │   │   │   │   │   ├── policial_repository_port.py
│   │   │   │   │   │   │   ├── prova_pericial_repository_port.py
│   │   │   │   │   │   │   ├── request_service_port.py
│   │   │   │   │   │   │   ├── unidade_policial_repository_port.py
│   │   │   │   │   │   │   └── vestigio_repository_port.py
│   │   │   │   │   │   └── services
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── cadeia_custodia_service.py
│   │   │   │   │   │       ├── evidencia_service.py
│   │   │   │   │   │       ├── investigacao_service.py
│   │   │   │   │   │       ├── laudo_pericial_service.py
│   │   │   │   │   │       ├── mandado_service.py
│   │   │   │   │   │       ├── ocorrencia_service.py
│   │   │   │   │   │       ├── policial_service.py
│   │   │   │   │   │       ├── prova_pericial_service.py
│   │   │   │   │   │       ├── unidade_policial_service.py
│   │   │   │   │   │       └── vestigio_service.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── models
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── cadeia_custodia.py
│   │   │   │   │   │       ├── evidencia.py
│   │   │   │   │   │       ├── investigacao.py
│   │   │   │   │   │       ├── laudo_pericial.py
│   │   │   │   │   │       ├── mandado.py
│   │   │   │   │   │       ├── ocorrencia.py
│   │   │   │   │   │       ├── policial.py
│   │   │   │   │   │       ├── prova_pericial.py
│   │   │   │   │   │       ├── unidade_policial.py
│   │   │   │   │   │       └── vestigio.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── request_service_adapter.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── cadeia_custodia_model.py
│   │   │   │   │   │   │   ├── evidencia_model.py
│   │   │   │   │   │   │   ├── investigacao_model.py
│   │   │   │   │   │   │   ├── laudo_pericial_model.py
│   │   │   │   │   │   │   ├── mandado_model.py
│   │   │   │   │   │   │   ├── ocorrencia_model.py
│   │   │   │   │   │   │   ├── policial_model.py
│   │   │   │   │   │   │   ├── prova_pericial_model.py
│   │   │   │   │   │   │   ├── unidade_policial_model.py
│   │   │   │   │   │   │   └── vestigio_model.py
│   │   │   │   │   │   └── repositories
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── sqlalchemy_cadeia_custodia_repository.py
│   │   │   │   │   │       ├── sqlalchemy_evidencia_repository.py
│   │   │   │   │   │       ├── sqlalchemy_investigacao_repository.py
│   │   │   │   │   │       ├── sqlalchemy_laudo_pericial_repository.py
│   │   │   │   │   │       ├── sqlalchemy_mandado_repository.py
│   │   │   │   │   │       ├── sqlalchemy_ocorrencia_repository.py
│   │   │   │   │   │       ├── sqlalchemy_policial_repository.py
│   │   │   │   │   │       ├── sqlalchemy_prova_pericial_repository.py
│   │   │   │   │   │       ├── sqlalchemy_unidade_policial_repository.py
│   │   │   │   │   │       └── sqlalchemy_vestigio_repository.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── _fakes.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       ├── test_cadeias_custodia.py
│   │   │   │   │       ├── test_evidencias.py
│   │   │   │   │       ├── test_investigacoes.py
│   │   │   │   │       ├── test_laudos_periciais.py
│   │   │   │   │       ├── test_mandados.py
│   │   │   │   │       ├── test_ocorrencias.py
│   │   │   │   │       ├── test_orm_integration_real.py
│   │   │   │   │       ├── test_policiais.py
│   │   │   │   │       ├── test_provas_periciais.py
│   │   │   │   │       ├── test_unidades_policiais.py
│   │   │   │   │       └── test_vestigios.py
│   │   │   │   ├── resources
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── agricultura
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_assistencia.py
│   │   │   │   │   │       ├── test_certificacoes.py
│   │   │   │   │   │       ├── test_colheitas.py
│   │   │   │   │   │       ├── test_comercializacao.py
│   │   │   │   │   │       ├── test_creditos.py
│   │   │   │   │   │       ├── test_culturas.py
│   │   │   │   │   │       ├── test_entidades_derivadas.py
│   │   │   │   │   │       ├── test_equipamentos.py
│   │   │   │   │   │       ├── test_estoques.py
│   │   │   │   │   │       ├── test_fitossanidade.py
│   │   │   │   │   │       ├── test_insumos.py
│   │   │   │   │   │       ├── test_operacoes.py
│   │   │   │   │   │       ├── test_plantios.py
│   │   │   │   │   │       ├── test_produtores.py
│   │   │   │   │   │       ├── test_propriedades.py
│   │   │   │   │   │       ├── test_safras.py
│   │   │   │   │   │       ├── test_talhoes.py
│   │   │   │   │   │       └── test_zoneamento.py
│   │   │   │   │   ├── aguas_saneamento
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── bus.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── handlers
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── repository.py
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── test_abastecimento.py
│   │   │   │   │   │   │   ├── test_consumo.py
│   │   │   │   │   │   │   ├── test_faturamento.py
│   │   │   │   │   │   │   ├── test_faturamento_eventos.py
│   │   │   │   │   │   │   ├── test_financas_gateway_publisher.py
│   │   │   │   │   │   │   ├── test_infraestrutura.py
│   │   │   │   │   │   │   ├── test_outbox_sqlalchemy_integration.py
│   │   │   │   │   │   │   └── test_outorgas.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       └── outbox_worker.py
│   │   │   │   │   ├── ambiente
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_car.py
│   │   │   │   │   │       ├── test_estudos.py
│   │   │   │   │   │       ├── test_fiscalizacao.py
│   │   │   │   │   │       ├── test_licenciamento.py
│   │   │   │   │   │       └── test_penalidades.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── florestas
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_alertas.py
│   │   │   │   │   │       ├── test_autorizacoes_supressao.py
│   │   │   │   │   │       ├── test_autos_infracao.py
│   │   │   │   │   │       ├── test_certificacoes.py
│   │   │   │   │   │       ├── test_concessoes.py
│   │   │   │   │   │       ├── test_cras.py
│   │   │   │   │   │       ├── test_creditos_carbono.py
│   │   │   │   │   │       ├── test_desmatamentos.py
│   │   │   │   │   │       ├── test_dofs.py
│   │   │   │   │   │       ├── test_exploracoes.py
│   │   │   │   │   │       ├── test_fiscalizacoes.py
│   │   │   │   │   │       ├── test_focos_calor.py
│   │   │   │   │   │       ├── test_incendios.py
│   │   │   │   │   │       ├── test_inventarios.py
│   │   │   │   │   │       ├── test_licencas_manejo.py
│   │   │   │   │   │       ├── test_monitoramento.py
│   │   │   │   │   │       ├── test_operadores_florestais.py
│   │   │   │   │   │       ├── test_planos_manejo.py
│   │   │   │   │   │       ├── test_produtos_florestais.py
│   │   │   │   │   │       └── test_unidades_manejo.py
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── pecuaria
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_animais.py
│   │   │   │   │   │       ├── test_pecuaristas.py
│   │   │   │   │   │       ├── test_propriedades.py
│   │   │   │   │   │       └── test_rebanhos.py
│   │   │   │   │   ├── pescas
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── industrial
│   │   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   │   └── tests
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_capturas.py
│   │   │   │   │   │       ├── test_embarcacoes.py
│   │   │   │   │   │       ├── test_licencas.py
│   │   │   │   │   │       └── test_pescadores.py
│   │   │   │   │   ├── petroleo_gas
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── recursos_minerais
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── seguranca_alimentar
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       ├── domain
│   │   │   │   │       └── infrastructure
│   │   │   │   ├── saude
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   └── vaccine_service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── clinical
│   │   │   │   │   │   │   └── epidemiology
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── module.yaml
│   │   │   │   │   └── module.yaml
│   │   │   │   ├── society
│   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   └── router.py
│   │   │   │   │   ├── application
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── assistencia_social
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── _fakes.py
│   │   │   │   │   │       ├── test_atendimento.py
│   │   │   │   │   │       ├── test_beneficiario.py
│   │   │   │   │   │       ├── test_beneficio_bpc_pcd.py
│   │   │   │   │   │       ├── test_cadastro_unico.py
│   │   │   │   │   │       ├── test_crianca_risco.py
│   │   │   │   │   │       ├── test_endpoints.py
│   │   │   │   │   │       ├── test_fluxo_completo_assistencia.py
│   │   │   │   │   │       ├── test_idoso_vulneravel.py
│   │   │   │   │   │       ├── test_orm_integration_real.py
│   │   │   │   │   │       ├── test_pcd.py
│   │   │   │   │   │       ├── test_programa_social.py
│   │   │   │   │   │       ├── test_situacao_rua.py
│   │   │   │   │   │       └── test_visita_domiciliar.py
│   │   │   │   │   ├── cultura
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── handlers
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _fakes.py
│   │   │   │   │   │   │   ├── test_artistas.py
│   │   │   │   │   │   │   ├── test_bens_culturais.py
│   │   │   │   │   │   │   ├── test_editais.py
│   │   │   │   │   │   │   ├── test_espacos_culturais.py
│   │   │   │   │   │   │   ├── test_eventos_culturais.py
│   │   │   │   │   │   │   ├── test_grupos_artisticos.py
│   │   │   │   │   │   │   ├── test_integracao_iphan.py
│   │   │   │   │   │   │   ├── test_orm_integration_real.py
│   │   │   │   │   │   │   ├── test_patrimonios_imateriais.py
│   │   │   │   │   │   │   └── test_projetos_culturais.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── edital_worker.py
│   │   │   │   │   │       ├── outbox_worker.py
│   │   │   │   │   │       └── patrimonio_worker.py
│   │   │   │   │   ├── desporto
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── config.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── bus.py
│   │   │   │   │   │   │   └── definitions.py
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── persistence
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   ├── resilience
│   │   │   │   │   │   │   └── __init__.py
│   │   │   │   │   │   ├── tests
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── _fakes.py
│   │   │   │   │   │   │   ├── test_atletas.py
│   │   │   │   │   │   │   ├── test_clubes.py
│   │   │   │   │   │   │   ├── test_competicoes.py
│   │   │   │   │   │   │   ├── test_estadios.py
│   │   │   │   │   │   │   ├── test_events.py
│   │   │   │   │   │   │   ├── test_jogos.py
│   │   │   │   │   │   │   ├── test_orm_integration_real.py
│   │   │   │   │   │   │   └── test_workers.py
│   │   │   │   │   │   └── workers
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── estatistica_worker.py
│   │   │   │   │   │       ├── notificacao_worker.py
│   │   │   │   │   │       ├── outbox_worker.py
│   │   │   │   │   │       └── ranking_worker.py
│   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── emprego
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_candidatos.py
│   │   │   │   │   │       ├── test_certificacoes.py
│   │   │   │   │   │       ├── test_concursos.py
│   │   │   │   │   │       ├── test_emprego_e2e.py
│   │   │   │   │   │       ├── test_formacoes.py
│   │   │   │   │   │       ├── test_mediacoes.py
│   │   │   │   │   │       ├── test_ofertas.py
│   │   │   │   │   │       └── test_trabalhistas.py
│   │   │   │   │   ├── familia
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── README.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── sagas
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── config.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── aggregates
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── events
│   │   │   │   │   │   │   ├── exceptions
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   ├── rules
│   │   │   │   │   │   │   └── value_objects
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── event_handlers
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── projections
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   ├── repository.py
│   │   │   │   │   │   │   └── resilience
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── _fakes.py
│   │   │   │   │   │       ├── e2e
│   │   │   │   │   │       ├── integration
│   │   │   │   │   │       └── unit
│   │   │   │   │   ├── igualdade
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── service.py
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   └── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   ├── juventude
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   └── repositories
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── _fakes.py
│   │   │   │   │   │       ├── test_auxilios.py
│   │   │   │   │   │       ├── test_formacoes.py
│   │   │   │   │   │       ├── test_jovens.py
│   │   │   │   │   │       ├── test_novos_slices_prioritarios.py
│   │   │   │   │   │       ├── test_orm_integration_real.py
│   │   │   │   │   │       ├── test_programas.py
│   │   │   │   │   │       ├── test_risco_evasao_com_educacao.py
│   │   │   │   │   │       └── test_workflow_service.py
│   │   │   │   │   ├── module.yaml
│   │   │   │   │   ├── patrimonio_cultural
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── _fakes.py
│   │   │   │   │   │       ├── test_patrimonio_cultural_endpoints.py
│   │   │   │   │   │       └── test_patrimonio_cultural_service.py
│   │   │   │   │   ├── seguranca_social
│   │   │   │   │   │   ├── ARCHITECTURE.md
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── deps.py
│   │   │   │   │   │   │   ├── endpoints
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   ├── router.py
│   │   │   │   │   │   │   └── schemas
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── ports
│   │   │   │   │   │   │   ├── service.py
│   │   │   │   │   │   │   └── services
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── entities.py
│   │   │   │   │   │   │   ├── enums.py
│   │   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   │   └── models
│   │   │   │   │   │   ├── exceptions.py
│   │   │   │   │   │   ├── infrastructure
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── adapters
│   │   │   │   │   │   │   ├── models
│   │   │   │   │   │   │   ├── repositories
│   │   │   │   │   │   │   └── repository.py
│   │   │   │   │   │   ├── module.yaml
│   │   │   │   │   │   └── tests
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── test_beneficiarios.py
│   │   │   │   │   │       └── test_pensoes.py
│   │   │   │   │   ├── tests
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── api
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── health.py
│   │   │   │   │   │   │   └── router.py
│   │   │   │   │   │   ├── application
│   │   │   │   │   │   ├── domain
│   │   │   │   │   │   └── infrastructure
│   │   │   │   │   └── trabalho_inspecao
│   │   │   │   │       ├── ARCHITECTURE.md
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   └── router.py
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── service.py
│   │   │   │   │       ├── domain
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── entities.py
│   │   │   │   │       │   └── exceptions.py
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   └── repository.py
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       └── tests
│   │   │   │   ├── tourism
│   │   │   │   │   └── core
│   │   │   │   │       ├── ARCHITECTURE.md
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── api
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── deps.py
│   │   │   │   │       │   ├── endpoints
│   │   │   │   │       │   ├── health.py
│   │   │   │   │       │   ├── router.py
│   │   │   │   │       │   └── schemas
│   │   │   │   │       ├── application
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── ports
│   │   │   │   │       │   └── services
│   │   │   │   │       ├── domain
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── enums.py
│   │   │   │   │       │   ├── exceptions.py
│   │   │   │   │       │   └── models
│   │   │   │   │       ├── infrastructure
│   │   │   │   │       │   ├── __init__.py
│   │   │   │   │       │   ├── adapters
│   │   │   │   │       │   ├── models
│   │   │   │   │       │   └── repositories
│   │   │   │   │       ├── module.yaml
│   │   │   │   │       └── tests
│   │   │   │   │           ├── __init__.py
│   │   │   │   │           ├── test_agencias_viagens.py
│   │   │   │   │           ├── test_atracoes.py
│   │   │   │   │           ├── test_autos_infracao.py
│   │   │   │   │           ├── test_avaliacoes.py
│   │   │   │   │           ├── test_cadastro_turistas.py
│   │   │   │   │           ├── test_cadastur.py
│   │   │   │   │           ├── test_certificacoes.py
│   │   │   │   │           ├── test_classificacoes.py
│   │   │   │   │           ├── test_estatisticas.py
│   │   │   │   │           ├── test_eventos.py
│   │   │   │   │           ├── test_fiscalizacoes.py
│   │   │   │   │           ├── test_fluxo_turistico.py
│   │   │   │   │           ├── test_guias_turismo.py
│   │   │   │   │           ├── test_hoteis.py
│   │   │   │   │           ├── test_licencas.py
│   │   │   │   │           ├── test_multas.py
│   │   │   │   │           ├── test_ocupacao_hoteleira.py
│   │   │   │   │           ├── test_operadores_turisticos.py
│   │   │   │   │           ├── test_pacotes.py
│   │   │   │   │           ├── test_pontos_turisticos.py
│   │   │   │   │           ├── test_pousadas.py
│   │   │   │   │           ├── test_promocoes.py
│   │   │   │   │           ├── test_receitas.py
│   │   │   │   │           ├── test_reclamacoes.py
│   │   │   │   │           ├── test_registro_guia.py
│   │   │   │   │           ├── test_reservas.py
│   │   │   │   │           ├── test_roteiros.py
│   │   │   │   │           ├── test_tarifas.py
│   │   │   │   │           └── test_temporadas.py
│   │   │   │   └── xroad
│   │   │   │       ├── api
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── api
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── health.py
│   │   │   │       │   │   └── router.py
│   │   │   │       │   ├── application
│   │   │   │       │   ├── domain
│   │   │   │       │   ├── infrastructure
│   │   │   │       │   └── router.py
│   │   │   │       ├── application
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── api
│   │   │   │       │   │   ├── __init__.py
│   │   │   │       │   │   ├── health.py
│   │   │   │       │   │   └── router.py
│   │   │   │       │   ├── application
│   │   │   │       │   ├── domain
│   │   │   │       │   ├── infrastructure
│   │   │   │       │   └── xroad_service.py
│   │   │   │       └── domain
│   │   │   │           ├── __init__.py
│   │   │   │           ├── api
│   │   │   │           │   ├── __init__.py
│   │   │   │           │   ├── health.py
│   │   │   │           │   └── router.py
│   │   │   │           ├── application
│   │   │   │           ├── domain
│   │   │   │           ├── envelope.py
│   │   │   │           └── infrastructure
│   │   │   ├── platform
│   │   │   │   ├── __init__.py
│   │   │   │   ├── integration
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── observability
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── logger.py
│   │   │   │   ├── persistence
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base_repository.py
│   │   │   │   │   └── unit_of_work.py
│   │   │   │   ├── runtime
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── compat_router.py
│   │   │   │   │   ├── health_router.py
│   │   │   │   │   └── loader.py
│   │   │   │   └── shared
│   │   │   │       ├── __init__.py
│   │   │   │       ├── bridges
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── citizen_repository_bridge.py
│   │   │   │       │   ├── citizen_repository_port_bridge.py
│   │   │   │       │   ├── civil_identity_bridge.py
│   │   │   │       │   ├── cross_domain_ports_bridge.py
│   │   │   │       │   ├── emprego_bridge.py
│   │   │   │       │   ├── finance_bridge.py
│   │   │   │       │   ├── governance_service_requests_bridge.py
│   │   │   │       │   ├── identity_bridge.py
│   │   │   │       │   ├── infrastructure_sector_bridge.py
│   │   │   │       │   ├── intelligence_bi_sources_bridge.py
│   │   │   │       │   ├── justice_public_safety_bridge.py
│   │   │   │       │   ├── resources_agricultura_bridge.py
│   │   │   │       │   ├── resources_external_services_bridge.py
│   │   │   │       │   ├── service_requests_bridge.py
│   │   │   │       │   ├── society_domain_enums_bridge.py
│   │   │   │       │   ├── society_repository_bridges.py
│   │   │   │       │   └── society_statistics_models_bridge.py
│   │   │   │       ├── db.py
│   │   │   │       └── enums.py
│   │   │   ├── presentation
│   │   │   │   ├── api
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── citizen_document_routes.py
│   │   │   │   │   └── citizen_routes.py
│   │   │   │   └── schemas
│   │   │   │       ├── __init__.py
│   │   │   │       ├── citizen_document_schema.py
│   │   │   │       └── citizen_schema.py
│   │   │   ├── schemas
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── login.py
│   │   │   │   ├── business.py
│   │   │   │   ├── citizen.py
│   │   │   │   └── user.py
│   │   │   ├── shared
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── current_user.py
│   │   │   │   │   └── permissions.py
│   │   │   │   ├── database
│   │   │   │   ├── db
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── mixins.py
│   │   │   │   │   └── session.py
│   │   │   │   ├── events
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── dispatcher.py
│   │   │   │   │   └── domain_event.py
│   │   │   │   ├── services
│   │   │   │   ├── utils
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── datetime.py
│   │   │   │   │   └── id_generator.py
│   │   │   │   └── value_objects
│   │   │   │       ├── __init__.py
│   │   │   │       ├── email.py
│   │   │   │       ├── money.py
│   │   │   │       └── pagination.py
│   │   │   ├── utils
│   │   │   │   ├── __init__.py
│   │   │   │   ├── security.py
│   │   │   │   └── territory_helpers.py
│   │   │   └── workers
│   │   │       ├── __init__.py
│   │   │       └── event_worker.py
│   │   ├── audit_triple_bootstrap_full.py
│   │   ├── check_docs.sh
│   │   ├── check_login.sh
│   │   ├── cleanup_duplicates.py
│   │   ├── cleanup_duplicates_auto.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── example_usage.py
│   │   │   ├── manager.py
│   │   │   ├── migrate_config.py
│   │   │   ├── settings.py
│   │   │   ├── test_config.py
│   │   │   └── validator.py
│   │   ├── conftest.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── cache
│   │   │   │   ├── __init__.py
│   │   │   │   └── redis.py
│   │   │   ├── celery
│   │   │   │   ├── __init__.py
│   │   │   │   └── app.py
│   │   │   ├── config.py
│   │   │   ├── db
│   │   │   │   ├── MIGRATION_EXAMPLE.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── session.py
│   │   │   ├── dependencies
│   │   │   │   └── __init__.py
│   │   │   ├── events
│   │   │   │   ├── __init__.py
│   │   │   │   └── event_bus.py
│   │   │   ├── exceptions.py
│   │   │   ├── health.py
│   │   │   ├── logger.py
│   │   │   ├── metrics.py
│   │   │   ├── repositories.py
│   │   │   ├── schemas.py
│   │   │   ├── scope.py
│   │   │   ├── security
│   │   │   │   ├── __init__.py
│   │   │   │   └── iam_client.py
│   │   │   ├── security.py
│   │   │   ├── sentry.py
│   │   │   └── services.py
│   │   ├── db
│   │   │   └── __init__.py
│   │   ├── demo_ultra_simple.sh
│   │   ├── docker-test.sh
│   │   ├── docs
│   │   │   ├── __init__.py
│   │   │   ├── architecture
│   │   │   ├── auth
│   │   │   │   └── __init__.py
│   │   │   ├── identity
│   │   │   │   └── __init__.py
│   │   │   └── user-guide
│   │   │       └── __init__.py
│   │   ├── entrypoint.sh
│   │   ├── env.example
│   │   ├── extract_error.py
│   │   ├── get-pip.py
│   │   ├── hydrate_vc_engine.sh
│   │   ├── interfaces
│   │   │   ├── grpc
│   │   │   └── http
│   │   ├── logs
│   │   │   └── test_db_connection.log
│   │   ├── main.py
│   │   ├── module_health_dashboard.html
│   │   ├── observability
│   │   │   ├── __init__.py
│   │   │   └── sentry_config.py
│   │   ├── platform
│   │   │   ├── config
│   │   │   ├── logging
│   │   │   └── middleware
│   │   ├── poetry.lock
│   │   ├── production_check.sh
│   │   ├── pyproject.toml
│   │   ├── pytest.ini
│   │   ├── refactor_locations.py
│   │   ├── requirements-dev.txt
│   │   ├── reset_local_db.py
│   │   ├── reset_password.py
│   │   ├── run_integration_tests_refactored.sh
│   │   ├── run_sila_dev.sh
│   │   ├── run_tests.py
│   │   ├── run_unit_tests.sh
│   │   ├── run_unit_tests_complete.sh
│   │   ├── scripts
│   │   │   ├── __init__.py
│   │   │   ├── apply_catalog_schema.py
│   │   │   ├── benchmark_operations_api_db.py
│   │   │   ├── bootstrap_institutional_modules.py
│   │   │   ├── check_catalog_metrics.py
│   │   │   ├── check_db_hierarchy.py
│   │   │   ├── check_users.py
│   │   │   ├── complete_migration.py
│   │   │   ├── create_module.py
│   │   │   ├── debug_mappers.py
│   │   │   ├── init-db.sql
│   │   │   ├── legacy
│   │   │   │   ├── check_login.py
│   │   │   │   ├── check_settings.py
│   │   │   │   ├── debug_login.py
│   │   │   │   ├── debug_mappers.py
│   │   │   │   ├── debug_tests.py
│   │   │   │   ├── fix_deps.py
│   │   │   │   ├── fix_password.py
│   │   │   │   ├── fix_tables.py
│   │   │   │   ├── fix_territory_model.py
│   │   │   │   └── inspect_routes.py
│   │   │   ├── list_provincial_users.py
│   │   │   ├── migrate_and_validate.py
│   │   │   ├── module_tools
│   │   │   │   ├── defesa_consumidor_generate_module.py
│   │   │   │   ├── estatistica_generate_module.py
│   │   │   │   ├── generate_module.py
│   │   │   │   └── setup_full_structure.py
│   │   │   ├── run_health_check.py
│   │   │   ├── run_health_check.sh
│   │   │   ├── run_migration.sh
│   │   │   ├── run_role_level_guard_tests.py
│   │   │   ├── run_statistics_block_tests.sh
│   │   │   ├── seed_admin_roles.py
│   │   │   ├── seed_all_users.py
│   │   │   ├── seed_angola_dpa_2024.py
│   │   │   ├── seed_citizen_roles.py
│   │   │   ├── seed_educacao_institucional.py
│   │   │   ├── seed_institutional_catalog.py
│   │   │   ├── seed_realistic_data.py
│   │   │   ├── setup_health_check.py
│   │   │   ├── test_central_auth.py
│   │   │   ├── test_persistence.py
│   │   │   └── validate_config.py
│   │   ├── seed_21_provinces_final.py
│   │   ├── seed_users.sql
│   │   ├── seed_users_v4.py
│   │   ├── seeds
│   │   │   ├── __init__.py
│   │   │   ├── catalog.py
│   │   │   ├── core
│   │   │   │   ├── __init__.py
│   │   │   │   ├── run_seed_angola.sh
│   │   │   │   ├── seed_and_token.py
│   │   │   │   ├── seed_angola_dpa_v3.py
│   │   │   │   ├── seed_angola_provinces.py
│   │   │   │   ├── seed_founding_users.py
│   │   │   │   ├── seed_founding_users_v2.py
│   │   │   │   ├── seed_founding_users_with_territories.py
│   │   │   │   ├── seed_fuc_citizen.py
│   │   │   │   └── seed_fuc_golden_citizen.py
│   │   │   ├── roles.py
│   │   │   ├── run.py
│   │   │   ├── run_all.py
│   │   │   ├── run_master_seed.py
│   │   │   ├── scripts
│   │   │   │   ├── __init__.py
│   │   │   │   ├── seed_base_users.py
│   │   │   │   └── seed_reference_data.py
│   │   │   ├── seed_admin_users.py
│   │   │   ├── seed_citizen_documents.py
│   │   │   ├── seed_integration_minimal.sql
│   │   │   └── seed_phase_20_2_events.sql
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── openai_client.py
│   │   ├── setup_env.sh
│   │   ├── simple_test.py
│   │   ├── static
│   │   │   ├── __init__.py
│   │   │   └── pdfs
│   │   │       ├── __init__.py
│   │   │       ├── certificado_judicial_19.pdf
│   │   │       └── certificado_judicial_20.pdf
│   │   ├── templates
│   │   │   ├── DDD_MODULE_ENTERPRISE
│   │   │   │   ├── application
│   │   │   │   │   ├── dto.py
│   │   │   │   │   └── service.py
│   │   │   │   ├── domain
│   │   │   │   │   ├── entities.py
│   │   │   │   │   ├── exceptions.py
│   │   │   │   │   └── value_objects.py
│   │   │   │   ├── infrastructure
│   │   │   │   │   └── repositories
│   │   │   │   │       └── sqlalchemy_repository.py
│   │   │   │   └── presentation
│   │   │   │       └── router.py
│   │   │   └── emails
│   │   │       ├── document_shared.html
│   │   │       ├── notification_base.html
│   │   │       └── payment_confirmed.html
│   │   ├── test_payment_endpoints_manual.py
│   │   ├── test_triple_bootstrap.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── ci_test_config.json
│   │   │   ├── citizen
│   │   │   │   └── unit
│   │   │   │       └── test_routing_engine.py
│   │   │   ├── conftest.py
│   │   │   ├── e2e
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── test_citizen_journey.py
│   │   │   │   ├── test_citizenship_flow.py
│   │   │   │   ├── test_integration_modules.py
│   │   │   │   ├── test_matricula_flow.py
│   │   │   │   └── test_payment_flow.py
│   │   │   ├── factories
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_factory.py
│   │   │   │   ├── license_factory.py
│   │   │   │   └── user_factory.py
│   │   │   ├── fixtures
│   │   │   │   ├── __init__.py
│   │   │   │   ├── check_citizen_cols.py
│   │   │   │   ├── check_db_fixture.py
│   │   │   │   ├── check_factory.py
│   │   │   │   └── check_setup.py
│   │   │   ├── integration
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cross_module
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── run_cross_module_tests.py
│   │   │   │   │   ├── test_citizenship_justice_payment.py
│   │   │   │   │   ├── test_education_justice_finance.py
│   │   │   │   │   ├── test_health_monitoring_notifications.py
│   │   │   │   │   ├── test_sanitation_monitoring_notifications.py
│   │   │   │   │   ├── validate_crud_implementation.py
│   │   │   │   │   ├── validate_integration_tests.py
│   │   │   │   │   └── validate_integration_tests_fixed.py
│   │   │   │   ├── db
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── logging_config.py
│   │   │   │   ├── modules
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── app
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── appointments
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── ci_integration.py
│   │   │   │   │   ├── commercial
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── common
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── education
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── health
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── internal
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── justice
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── reports
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── run_new_tests.py
│   │   │   │   │   ├── social
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── statistics
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   └── urbanism
│   │   │   │   │       └── __init__.py
│   │   │   │   ├── performance
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── run_tests.sh
│   │   │   │   ├── test_api_refactored.py
│   │   │   │   ├── test_app.py
│   │   │   │   ├── test_app_bootstrap.py
│   │   │   │   ├── test_appointments.py
│   │   │   │   ├── test_auth_flow.py
│   │   │   │   ├── test_auth_staging.py
│   │   │   │   ├── test_citizens.py
│   │   │   │   ├── test_commercial_schemas_fixed.py
│   │   │   │   ├── test_db_connection.py
│   │   │   │   ├── test_environment.py
│   │   │   │   ├── test_global_imports.py
│   │   │   │   ├── test_health_endpoints.py
│   │   │   │   ├── test_health_run.py
│   │   │   │   ├── test_integration.py
│   │   │   │   ├── test_minimal_notifications.py
│   │   │   │   ├── test_output.py
│   │   │   │   ├── test_services.py
│   │   │   │   ├── test_smoke.py
│   │   │   │   ├── test_users.py
│   │   │   │   └── utils
│   │   │   │       ├── __init__.py
│   │   │   │       ├── auth.py
│   │   │   │       └── utils.py
│   │   │   ├── load
│   │   │   │   └── test_operations_load.py
│   │   │   ├── module_health_check.py
│   │   │   ├── modules
│   │   │   │   ├── administracao_local
│   │   │   │   │   ├── conftest.py
│   │   │   │   │   ├── test_administracao_local_smoke.py
│   │   │   │   │   ├── test_router.py
│   │   │   │   │   └── test_service.py
│   │   │   │   ├── agricultura
│   │   │   │   │   └── test_agricultura_smoke.py
│   │   │   │   ├── aguas_saneamento
│   │   │   │   │   └── test_aguas_saneamento_smoke.py
│   │   │   │   ├── ambiente
│   │   │   │   │   └── test_ambiente_smoke.py
│   │   │   │   ├── apoio_empresarial
│   │   │   │   │   └── test_apoio_empresarial_smoke.py
│   │   │   │   ├── arquivo_nacional
│   │   │   │   │   └── test_arquivo_nacional_smoke.py
│   │   │   │   ├── assistencia_social
│   │   │   │   │   └── test_assistencia_social_smoke.py
│   │   │   │   ├── aviacao_civil
│   │   │   │   │   └── test_aviacao_civil_smoke.py
│   │   │   │   ├── ciencia_pesquisa
│   │   │   │   │   └── test_ciencia_pesquisa_smoke.py
│   │   │   │   ├── comercio
│   │   │   │   │   └── test_comercio_smoke.py
│   │   │   │   ├── comercio_externo
│   │   │   │   │   └── test_comercio_externo_smoke.py
│   │   │   │   ├── cooperacao_internacional
│   │   │   │   │   └── test_cooperacao_internacional_smoke.py
│   │   │   │   ├── cultura
│   │   │   │   │   └── test_cultura_smoke.py
│   │   │   │   ├── defesa_consumidor
│   │   │   │   │   └── test_defesa_consumidor_smoke.py
│   │   │   │   ├── desporto
│   │   │   │   │   └── test_desporto_smoke.py
│   │   │   │   ├── educacao
│   │   │   │   │   └── test_educacao_smoke.py
│   │   │   │   ├── emprego
│   │   │   │   │   └── test_emprego_smoke.py
│   │   │   │   ├── energia
│   │   │   │   │   └── test_energia_smoke.py
│   │   │   │   ├── estatistica
│   │   │   │   │   └── test_estatistica_smoke.py
│   │   │   │   ├── familia
│   │   │   │   │   └── test_familia_smoke.py
│   │   │   │   ├── financas_impostos
│   │   │   │   │   └── test_financas_impostos_smoke.py
│   │   │   │   ├── florestas
│   │   │   │   │   └── test_florestas_smoke.py
│   │   │   │   ├── gestao_fundiaria
│   │   │   │   │   └── test_gestao_fundiaria_smoke.py
│   │   │   │   ├── habitacao
│   │   │   │   │   └── test_habitacao_smoke.py
│   │   │   │   ├── igualdade
│   │   │   │   │   └── test_igualdade_smoke.py
│   │   │   │   ├── industria
│   │   │   │   │   └── test_industria_smoke.py
│   │   │   │   ├── justica
│   │   │   │   │   └── test_justica_smoke.py
│   │   │   │   ├── juventude
│   │   │   │   │   └── test_juventude_smoke.py
│   │   │   │   ├── meteorologia
│   │   │   │   │   └── test_meteorologia_smoke.py
│   │   │   │   ├── migracao
│   │   │   │   │   └── test_migracao_smoke.py
│   │   │   │   ├── obras_publicas
│   │   │   │   │   └── test_obras_publicas_smoke.py
│   │   │   │   ├── patrimonio_cultural
│   │   │   │   │   └── test_patrimonio_cultural_smoke.py
│   │   │   │   ├── pecuaria
│   │   │   │   │   └── test_pecuaria_smoke.py
│   │   │   │   ├── pescas
│   │   │   │   │   └── test_pescas_smoke.py
│   │   │   │   ├── pescas_industriais
│   │   │   │   │   └── test_pescas_industriais_smoke.py
│   │   │   │   ├── petroleo_gas
│   │   │   │   │   └── test_petroleo_gas_smoke.py
│   │   │   │   ├── planeamento
│   │   │   │   │   └── test_planeamento_smoke.py
│   │   │   │   ├── portos_logistica
│   │   │   │   │   └── test_portos_logistica_smoke.py
│   │   │   │   ├── protecao_civil
│   │   │   │   │   └── test_protecao_civil_smoke.py
│   │   │   │   ├── protecao_dados
│   │   │   │   │   └── test_protecao_dados_smoke.py
│   │   │   │   ├── recursos_minerais
│   │   │   │   │   └── test_recursos_minerais_smoke.py
│   │   │   │   ├── registo_civil
│   │   │   │   │   └── test_registo_civil_smoke.py
│   │   │   │   ├── saude
│   │   │   │   │   └── test_saude_smoke.py
│   │   │   │   ├── seguranca_alimentar
│   │   │   │   │   └── test_seguranca_alimentar_smoke.py
│   │   │   │   ├── seguranca_publica
│   │   │   │   │   └── test_seguranca_publica_smoke.py
│   │   │   │   ├── seguranca_social
│   │   │   │   │   └── test_seguranca_social_smoke.py
│   │   │   │   ├── tecnologia_inovacao
│   │   │   │   │   └── test_tecnologia_inovacao_smoke.py
│   │   │   │   ├── telecomunicacoes
│   │   │   │   │   └── test_telecomunicacoes_smoke.py
│   │   │   │   ├── trabalho_inspecao
│   │   │   │   │   └── test_trabalho_inspecao_smoke.py
│   │   │   │   ├── transportes
│   │   │   │   │   └── test_transportes_smoke.py
│   │   │   │   ├── turismo
│   │   │   │   │   └── test_turismo_smoke.py
│   │   │   │   └── urbanismo
│   │   │   │       └── test_urbanismo_smoke.py
│   │   │   ├── test_alembic_chain.py
│   │   │   ├── test_alembic_health.py
│   │   │   ├── test_audit_analytics.py
│   │   │   ├── test_auth_consolidated.py
│   │   │   ├── test_basic_endpoints.py
│   │   │   ├── test_catalog_governance.py
│   │   │   ├── test_citizen_documents.py
│   │   │   ├── test_import_check.py
│   │   │   ├── test_modules_ping.py
│   │   │   ├── test_profile_queries.py
│   │   │   ├── test_quality_report.json
│   │   │   ├── test_smoke_production.py
│   │   │   ├── test_territory_api.py
│   │   │   ├── unit
│   │   │   │   ├── __init__.py
│   │   │   │   ├── reports
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── unit_test_summary.json
│   │   │   │   ├── run_unit_tests.py
│   │   │   │   ├── test_dedup.py
│   │   │   │   ├── test_payment_models.py
│   │   │   │   ├── test_routing_engine.py
│   │   │   │   ├── test_sanity.py
│   │   │   │   └── test_service_hub_models.py
│   │   │   ├── utils
│   │   │   │   ├── __init__.py
│   │   │   │   ├── generate_tests.py
│   │   │   │   └── utils.py
│   │   │   └── wsl.localhost
│   │   │       └── Ubuntu
│   │   │           └── home
│   │   │               └── truman
│   │   │                   └── dev
│   │   ├── translations
│   │   │   ├── __init__.py
│   │   │   ├── en.json
│   │   │   └── pt.json
│   │   ├── update_schema.py
│   │   ├── update_schema_v2.py
│   │   ├── validate_identity_models.py
│   │   ├── validate_repository_decorators.py
│   │   ├── verify_etag.py
│   │   ├── verify_triple_bootstrap.py
│   │   └── verify_versioning.py
│   ├── frontend
│   │   ├── Dockerfile
│   │   ├── Dockerfile.prod
│   │   ├── README.md
│   │   ├── eslint.config.js
│   │   ├── index.html
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── postcss.config.js
│   │   ├── public
│   │   │   ├── test.txt
│   │   │   └── vite.svg
│   │   ├── src
│   │   │   ├── App.css
│   │   │   ├── App.tsx
│   │   │   ├── api
│   │   │   │   ├── adminHttp.ts
│   │   │   │   ├── axios.ts
│   │   │   │   ├── citizenHttp.ts
│   │   │   │   └── http.ts
│   │   │   ├── assets
│   │   │   │   ├── images
│   │   │   │   │   ├── Education-Dashboard-Admin-Template.jpg:Zone.Identifier
│   │   │   │   │   ├── bandeira-angola-ondulante.png
│   │   │   │   │   ├── bandeira-angola-ondulante.png.jpeg:Zone.Identifier
│   │   │   │   │   ├── brasao-angola.png
│   │   │   │   │   ├── brasao-angola.png.jpeg:Zone.Identifier
│   │   │   │   │   ├── level-central.webp
│   │   │   │   │   ├── level-municipal.png
│   │   │   │   │   ├── level-provincial.jpg
│   │   │   │   │   ├── login-hero.jpg
│   │   │   │   │   ├── mockup-dashboard-nacional.png.webp:Zone.Identifier
│   │   │   │   │   ├── mockup-portal-admin-provincial.png.jpeg:Zone.Identifier
│   │   │   │   │   ├── mockup-portal-cidadao.png.jpeg
│   │   │   │   │   ├── mockup-portal-cidadao.png.jpeg:Zone.Identifier
│   │   │   │   │   ├── mockup-portal-cidadao.png.png:Zone.Identifier
│   │   │   │   │   └── mockup-portal-estudante.png.jpg:Zone.Identifier
│   │   │   │   └── react.svg
│   │   │   ├── components
│   │   │   │   ├── Admin
│   │   │   │   │   └── AdminPanel.tsx
│   │   │   │   ├── Auth
│   │   │   │   │   ├── AdminRoute.tsx
│   │   │   │   │   └── ProtectedRoute.tsx
│   │   │   │   ├── Dashboard
│   │   │   │   │   ├── DocumentsTable.tsx
│   │   │   │   │   └── StatsCards.tsx
│   │   │   │   ├── Documents
│   │   │   │   │   └── DocumentCard.tsx
│   │   │   │   ├── Layout
│   │   │   │   │   └── Header.tsx
│   │   │   │   ├── Layout.tsx
│   │   │   │   ├── Payment
│   │   │   │   │   └── CheckoutCard.tsx
│   │   │   │   ├── ProtectedRoute.tsx
│   │   │   │   ├── Search
│   │   │   │   │   └── GlobalSearchBar.tsx
│   │   │   │   ├── Statistics
│   │   │   │   │   └── StatisticsSkeleton.tsx
│   │   │   │   └── Upload
│   │   │   │       └── UploadZone.tsx
│   │   │   ├── constants
│   │   │   │   └── images.ts
│   │   │   ├── constants.tsx
│   │   │   ├── hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useDocumentStatus.ts
│   │   │   │   ├── useDocumentUpload.ts
│   │   │   │   └── useMyDocuments.ts
│   │   │   ├── index.css
│   │   │   ├── index.tsx
│   │   │   ├── main.tsx
│   │   │   ├── modules
│   │   │   │   └── pagamentos
│   │   │   │       ├── FinancialDashboard.tsx
│   │   │   │       ├── PaymentsPage.tsx
│   │   │   │       ├── components
│   │   │   │       │   ├── Layout.tsx
│   │   │   │       │   └── PaymentModal.tsx
│   │   │   │       ├── index.tsx
│   │   │   │       ├── services
│   │   │   │       │   └── financeService.ts
│   │   │   │       └── types.ts
│   │   │   ├── pages
│   │   │   │   ├── AdminAuditViewer.tsx
│   │   │   │   ├── AdminStatistics.tsx
│   │   │   │   ├── CitizenDashboard.tsx
│   │   │   │   ├── CitizenLogin.tsx
│   │   │   │   ├── CitizenPortal.tsx
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── DocumentsView.tsx
│   │   │   │   ├── Login.tsx
│   │   │   │   ├── MyDocuments.tsx
│   │   │   │   ├── Notifications.tsx
│   │   │   │   ├── PortalSelection.tsx
│   │   │   │   ├── PublicLanding.tsx
│   │   │   │   ├── Register.tsx
│   │   │   │   ├── SearchDeepResults.tsx
│   │   │   │   ├── SearchDocuments.tsx
│   │   │   │   ├── Unauthorized.tsx
│   │   │   │   └── UploadDocuments.tsx
│   │   │   ├── router
│   │   │   │   └── routes.tsx
│   │   │   ├── services
│   │   │   │   ├── API_INTEGRATION_GUIDE.md
│   │   │   │   ├── api.ts
│   │   │   │   ├── apiService.ts
│   │   │   │   ├── auth.ts
│   │   │   │   ├── authGuard.ts
│   │   │   │   ├── authService.ts
│   │   │   │   ├── citizenAuthService.ts
│   │   │   │   ├── citizenService.ts
│   │   │   │   ├── dashboardService.ts
│   │   │   │   ├── documentService.ts
│   │   │   │   └── territoryService.ts
│   │   │   ├── store
│   │   │   │   └── authStore.ts
│   │   │   ├── types
│   │   │   │   └── auth.ts
│   │   │   ├── types.ts
│   │   │   └── utils
│   │   │       └── cn.ts
│   │   ├── tailwind.config.js
│   │   ├── tsconfig.app.json
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   └── vite.config.ts
│   └── worker
├── batch_extraction_identity.sh
├── batch_health_education_migrate.sh
├── batch_health_education_mkdir.sh
├── batch_purge_identity.sh
├── cleanup.sh
├── cleanup_saude_refs.py
├── cleanup_seeds.sh
├── code-quality.workflow
├── conftest.py
├── consolidate_and_purge.sh
├── consolidate_identity_core.log
├── consolidate_identity_core.sh
├── consolidate_justice_core.log
├── consolidate_justice_core.sh
├── deploy-wsl2.sh
├── docker-clean-and-up.sh
├── docker-compose.alerts.yml
├── docker-compose.elk.yml
├── docker-compose.events.yml
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── docker-compose.yml
├── docs
│   ├── AI_ARCHITECTURE_GRAPH.yaml
│   ├── AI_ARCHITECTURE_GUIDE.md
│   ├── AI_BOOTSTRAP_PROMPT.md
│   ├── AI_CONTEXT.md
│   ├── AI_DOMAIN_KERNEL.md
│   ├── AI_GUARDRAILS.md
│   ├── AI_WORKFLOW.md
│   ├── ANGOLA_SETUP.md
│   ├── ELK_OPERATIONS_GUIDE.md
│   ├── architecture
│   │   ├── REPOSITORY_MAP.yaml
│   │   ├── context_map.md
│   │   ├── domain_dependency_policy.yaml
│   │   ├── domains
│   │   │   ├── core_system
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── economy
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── educacao
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── environment
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── governance
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── identity
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── infrastructure
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── infrastructure_sector
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── intelligence
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── justice
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── resources
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── security
│   │   │   │   └── ARCHITECTURE.md
│   │   │   ├── social
│   │   │   │   └── ARCHITECTURE.md
│   │   │   └── society
│   │   │       └── ARCHITECTURE.md
│   │   ├── entrypoints
│   │   │   ├── API_ENTRYPOINTS.md
│   │   │   ├── BACKEND_ARCHITECTURE.md
│   │   │   ├── DATA_FLOW.md
│   │   │   ├── DOMAIN_MAP.md
│   │   │   └── SYSTEM_OVERVIEW.md
│   │   ├── migration_strategy.md
│   │   └── module_federation_plan.md
│   ├── modules
│   │   └── tree.txt
│   └── tree.md
├── execute_phase_20_2_schema.py
├── filebeat.yml
├── grafana-dashboards.yml
├── grafana-datasources.yml
├── heal_identity_bridge.py
├── identity_core.lock
├── inspect_db.sh
├── interfaces
│   ├── dashboard
│   │   └── institutional_dashboard.py
│   └── frontend
│       ├── Dockerfile
│       ├── Dockerfile.prod
│       ├── eslint.config.js
│       ├── index.html
│       ├── package-lock.json
│       ├── package.json
│       ├── postcss.config.js
│       ├── public
│       │   └── vite.svg
│       ├── src
│       │   ├── App.css
│       │   ├── App.tsx
│       │   ├── api
│       │   │   ├── adminHttp.ts
│       │   │   ├── axios.ts
│       │   │   ├── citizenHttp.ts
│       │   │   └── http.ts
│       │   ├── assets
│       │   │   ├── images
│       │   │   │   ├── auth-bg-admin.webp
│       │   │   │   ├── auth-bg-citizen.webp
│       │   │   │   ├── brand-logo-sila.webp
│       │   │   │   ├── dashboard-citizen-hero.webp
│       │   │   │   ├── feature-digital-wallet.webp
│       │   │   │   ├── geo-level-municipal.webp
│       │   │   │   ├── geo-level-national.webp
│       │   │   │   ├── geo-level-provincial.webp
│       │   │   │   ├── gov-insignia-color.webp
│       │   │   │   ├── gov-insignia-gold.webp
│       │   │   │   ├── seguranca_publica.png
│       │   │   │   └── seguranca_publica.png:Zone.Identifier
│       │   │   └── react.svg
│       │   ├── components
│       │   │   ├── Admin
│       │   │   │   └── AdminPanel.tsx
│       │   │   ├── Auth
│       │   │   │   ├── AdminRoute.tsx
│       │   │   │   └── ProtectedRoute.tsx
│       │   │   ├── Dashboard
│       │   │   │   ├── DocumentsTable.tsx
│       │   │   │   └── StatsCards.tsx
│       │   │   ├── Documents
│       │   │   │   └── DocumentCard.tsx
│       │   │   ├── Layout
│       │   │   │   └── Header.tsx
│       │   │   ├── Layout.tsx
│       │   │   ├── Payment
│       │   │   │   └── CheckoutCard.tsx
│       │   │   ├── ProtectedRoute.tsx
│       │   │   ├── Search
│       │   │   │   └── GlobalSearchBar.tsx
│       │   │   ├── Statistics
│       │   │   │   └── StatisticsSkeleton.tsx
│       │   │   └── Upload
│       │   │       └── UploadZone.tsx
│       │   ├── constants
│       │   │   └── images.ts
│       │   ├── constants.tsx
│       │   ├── hooks
│       │   │   ├── useAuth.ts
│       │   │   ├── useDocumentStatus.ts
│       │   │   ├── useDocumentUpload.ts
│       │   │   └── useMyDocuments.ts
│       │   ├── index.css
│       │   ├── main.tsx
│       │   ├── modules
│       │   │   └── pagamentos
│       │   │       ├── FinancialDashboard.tsx
│       │   │       ├── PaymentsPage.tsx
│       │   │       ├── components
│       │   │       │   ├── Layout.tsx
│       │   │       │   └── PaymentModal.tsx
│       │   │       ├── index.tsx
│       │   │       ├── services
│       │   │       │   └── financeService.ts
│       │   │       └── types.ts
│       │   ├── pages
│       │   │   ├── AdminAuditViewer.tsx
│       │   │   ├── AdminStatistics.tsx
│       │   │   ├── CitizenDashboard.tsx
│       │   │   ├── CitizenLogin.tsx
│       │   │   ├── CitizenPortal.tsx
│       │   │   ├── Dashboard.tsx
│       │   │   ├── DocumentsView.tsx
│       │   │   ├── Login.tsx
│       │   │   ├── MyDocuments.tsx
│       │   │   ├── Notifications.tsx
│       │   │   ├── PortalSelection.tsx
│       │   │   ├── PublicLanding.tsx
│       │   │   ├── Register.tsx
│       │   │   ├── SearchDeepResults.tsx
│       │   │   ├── SearchDocuments.tsx
│       │   │   ├── Unauthorized.tsx
│       │   │   ├── UploadDocuments.tsx
│       │   │   └── admin
│       │   │       ├── AdminCitizensPage.tsx
│       │   │       ├── AdminDocumentsPage.tsx
│       │   │       ├── AdminObservabilityPage.tsx
│       │   │       └── AdminTerritoryPage.tsx
│       │   ├── router
│       │   │   └── routes.tsx
│       │   ├── services
│       │   │   ├── api.ts
│       │   │   ├── apiService.ts
│       │   │   ├── auth.ts
│       │   │   ├── authGuard.ts
│       │   │   ├── authService.ts
│       │   │   ├── citizenAuthService.ts
│       │   │   ├── citizenService.ts
│       │   │   ├── dashboardService.ts
│       │   │   ├── documentService.ts
│       │   │   └── territoryService.ts
│       │   ├── store
│       │   │   └── authStore.ts
│       │   ├── types
│       │   │   └── auth.ts
│       │   ├── types.ts
│       │   └── utils
│       │       └── cn.ts
│       ├── tailwind.config.js
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       └── vite.config.ts
├── justice_core.lock
├── lint_architecture.sh
├── logs
│   ├── event_worker.log
│   ├── outbox_worker.log
│   └── test_db_connection.log
├── logstash.conf
├── migrate_justice_structure.sh
├── migrations
│   └── versions
│       ├── 001_create_health_tables.py
│       ├── 001_create_invoices_table.py
│       ├── 001_create_service_requests.py
│       ├── 002_add_health_indexes.py
│       ├── 002_create_attachments.py
│       ├── 002_create_payments_table.py
│       ├── 003_create_audit_logs_table.py
│       ├── 003_create_request_events.py
│       ├── 004_add_citizen_id_to_invoices.py
│       └── __init__.py
├── modules
│   ├── __init__.py
│   ├── documents
│   │   ├── __init__.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   └── documents.py
│   │   └── services
│   │       ├── __init__.py
│   │       └── document_service.py
│   ├── identity
│   │   ├── __init__.py
│   │   ├── domain
│   │   │   ├── __init__.py
│   │   │   └── trust_score.py
│   │   └── middleware
│   │       ├── __init__.py
│   │       └── trust_middleware.py
│   └── payment
│       ├── __init__.py
│       ├── models
│       │   ├── __init__.py
│       │   ├── enums.py
│       │   └── payment.py
│       ├── schemas
│       │   ├── __init__.py
│       │   └── payment.py
│       └── services
│           ├── __init__.py
│           ├── payment_service.py
│           └── webhook_service.py
├── modules_report.md
├── mypy.ini
├── orchestrator
│   └── infrastructure
│       └── factory
│           └── unified_ports_factory.py
├── platform
│   ├── ci
│   │   ├── backend_context.yaml
│   │   ├── endpoints.yaml
│   │   ├── run_tests.py
│   │   └── validate_py_syntax.py
│   ├── devops
│   │   ├── monitoring
│   │   │   ├── alertmanager
│   │   │   │   └── alerts_config.yaml
│   │   │   ├── grafana
│   │   │   │   ├── dashboards
│   │   │   │   │   ├── grafana_dashboard.json
│   │   │   │   │   ├── sila-business.json
│   │   │   │   │   ├── sila-metrics-dashboard.json
│   │   │   │   │   ├── sila-overview.json
│   │   │   │   │   └── sila-performance.json
│   │   │   │   └── provisioning
│   │   │   │       ├── alerting
│   │   │   │       │   ├── alerting.yml
│   │   │   │       │   ├── alertmanager.yml
│   │   │   │       │   └── templates
│   │   │   │       │       └── slack.tmpl
│   │   │   │       ├── dashboards
│   │   │   │       │   ├── cpf-validation-dashboard.json
│   │   │   │       │   ├── dashboard.yml
│   │   │   │       │   └── sila-metrics-dashboard.json
│   │   │   │       └── datasources
│   │   │   │           └── datasource.yml
│   │   │   ├── prometheus
│   │   │   │   ├── prometheus.yml
│   │   │   │   └── rules
│   │   │   │       └── sila-alerts.yml
│   │   │   └── validate_drift.sh
│   │   ├── scripts
│   │   │   └── deploy_producao.sh
│   │   ├── test_docker_setup.sh
│   │   ├── test_final.sh
│   │   ├── utils
│   │   │   ├── abrir-windsurf.sh
│   │   │   ├── complete_env.sh
│   │   │   ├── make_executable.sh
│   │   │   ├── prepare_environment.sh
│   │   │   ├── run_with_pythonpath.sh
│   │   │   ├── test_runner.sh
│   │   │   └── validar_dependencias_sila.sh
│   │   ├── validate.sh
│   │   ├── validate_compose_structure.sh
│   │   └── verify_backend.sh
│   ├── infrastructure
│   │   ├── config
│   │   │   ├── config_manager.py
│   │   │   ├── logrotate-sila.conf
│   │   │   └── test_config_system.sh
│   │   ├── db
│   │   ├── docker
│   │   │   ├── Dockerfile.frontend
│   │   │   ├── Dockerfile.test
│   │   │   ├── frontend.conf
│   │   │   └── nginx.conf
│   │   ├── dr
│   │   │   ├── patroni-config.yaml
│   │   │   ├── walg-backup-cronjob.yaml
│   │   │   └── walg-restore-job.yaml
│   │   ├── k8s
│   │   │   ├── obras-publicas-outbox-worker.yaml
│   │   │   ├── obras-publicas-worker-hpa.yaml
│   │   │   └── sila-deployment.yaml
│   │   └── multi-region
│   │       ├── geodns-routing.yaml
│   │       ├── kafka
│   │       │   └── mirrormaker2.yaml
│   │       └── postgres
│   │           ├── region-a-publication.sql
│   │           ├── region-a-subscription.sql
│   │           ├── region-b-publication.sql
│   │           └── region-b-subscription.sql
│   └── storage
│       ├── data
│       │   ├── clientes.csv
│       │   └── examples
│       │       ├── sila_150_services.csv
│       │       └── teste_servicos.csv
│       ├── media
│       └── reports
│           ├── ai_architecture_graph.json
│           ├── ai_architecture_graph_visual_report.md
│           ├── ai_bootstrap_integration_report.md
│           ├── ai_domain_kernel_visual_report.md
│           ├── architecture_audit_report.json
│           ├── architecture_index_visual_report.md
│           ├── architecture_map.md
│           ├── architecture_refactor_report.json
│           ├── architecture_scan_after.json
│           ├── architecture_scan_before.json
│           ├── architecture_scan_report.json
│           ├── dependency_graph.json
│           ├── domain_overlap_report.md
│           ├── migration_domain_inventory.md
│           ├── module_architecture_docs_visual_report.md
│           ├── module_dependencies.md
│           ├── module_dependency_graph.json
│           ├── module_health_report.md
│           ├── module_inventory.txt
│           └── module_map.json
├── prometheus.yml
├── pytest.ini
├── quickstart-event-bus.sh
├── repair_imports_ast.py
├── reports
│   ├── PHASE_18.3_AUDIT.json
│   ├── architecture_audit.json
│   ├── architecture_audit.md
│   ├── circular_dependency_scan.md
│   ├── daily_audit
│   │   ├── 01_arch_sync_2026-03-13_06-09-43.log
│   │   ├── 01_arch_sync_2026-03-13_06-16-40.log
│   │   ├── 01_arch_sync_2026-03-13_06-18-07.log
│   │   ├── 01_arch_sync_2026-03-13_06-19-47.log
│   │   ├── 01_arch_sync_2026-03-13_06-21-01.log
│   │   ├── 01_arch_sync_2026-03-13_06-22-02.log
│   │   ├── 01_arch_sync_2026-03-13_06-22-41.log
│   │   ├── 01_arch_sync_2026-03-13_06-23-18.log
│   │   ├── 01_arch_sync_2026-03-13_06-40-34.log
│   │   ├── 01_arch_sync_2026-03-13_06-41-22.log
│   │   ├── 01_arch_sync_2026-03-13_09-34-16.log
│   │   ├── 01_arch_sync_2026-03-13_09-35-30.log
│   │   ├── 01_arch_sync_2026-03-13_09-37-31.log
│   │   ├── 01_arch_sync_2026-03-13_09-38-14.log
│   │   ├── 01_arch_sync_2026-03-13_09-39-08.log
│   │   ├── 01_arch_sync_2026-03-13_09-39-12.log
│   │   ├── 01_arch_sync_2026-03-13_09-40-07.log
│   │   ├── 01_arch_sync_2026-03-13_09-40-37.log
│   │   ├── 01_arch_sync_2026-03-13_09-41-40.log
│   │   ├── 01_arch_sync_2026-03-13_09-42-58.log
│   │   ├── 02_domain_audit_2026-03-13_06-09-43.log
│   │   ├── 02_domain_audit_2026-03-13_06-16-40.log
│   │   ├── 02_domain_audit_2026-03-13_06-18-07.log
│   │   ├── 02_domain_audit_2026-03-13_06-19-47.log
│   │   ├── 02_domain_audit_2026-03-13_06-21-01.log
│   │   ├── 02_domain_audit_2026-03-13_06-22-02.log
│   │   ├── 02_domain_audit_2026-03-13_06-22-41.log
│   │   ├── 02_domain_audit_2026-03-13_06-23-18.log
│   │   ├── 02_domain_audit_2026-03-13_06-40-34.log
│   │   ├── 02_domain_audit_2026-03-13_06-41-22.log
│   │   ├── 02_domain_audit_2026-03-13_09-34-16.log
│   │   ├── 02_domain_audit_2026-03-13_09-35-30.log
│   │   ├── 02_domain_audit_2026-03-13_09-37-31.log
│   │   ├── 02_domain_audit_2026-03-13_09-38-14.log
│   │   ├── 02_domain_audit_2026-03-13_09-39-08.log
│   │   ├── 02_domain_audit_2026-03-13_09-39-12.log
│   │   ├── 02_domain_audit_2026-03-13_09-40-07.log
│   │   ├── 02_domain_audit_2026-03-13_09-40-37.log
│   │   ├── 02_domain_audit_2026-03-13_09-41-40.log
│   │   ├── 02_domain_audit_2026-03-13_09-42-58.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-09-43.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-16-40.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-18-07.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-19-47.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-21-01.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-22-02.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-22-41.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-23-18.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-40-34.log
│   │   ├── 03_module_diagnostics_2026-03-13_06-41-22.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-34-16.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-35-30.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-37-31.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-38-14.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-39-08.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-39-12.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-40-07.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-40-37.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-41-40.log
│   │   ├── 03_module_diagnostics_2026-03-13_09-42-58.log
│   │   ├── 04_import_scan_2026-03-13_06-09-43.log
│   │   ├── 04_import_scan_2026-03-13_06-16-40.log
│   │   ├── 04_import_scan_2026-03-13_06-18-07.log
│   │   ├── 04_import_scan_2026-03-13_06-19-47.log
│   │   ├── 04_import_scan_2026-03-13_06-21-01.log
│   │   ├── 04_import_scan_2026-03-13_06-22-02.log
│   │   ├── 04_import_scan_2026-03-13_06-22-41.log
│   │   ├── 04_import_scan_2026-03-13_06-23-18.log
│   │   ├── 04_import_scan_2026-03-13_06-40-34.log
│   │   ├── 04_import_scan_2026-03-13_06-41-22.log
│   │   ├── 04_import_scan_2026-03-13_09-34-16.log
│   │   ├── 04_import_scan_2026-03-13_09-35-30.log
│   │   ├── 04_import_scan_2026-03-13_09-37-31.log
│   │   ├── 04_import_scan_2026-03-13_09-38-14.log
│   │   ├── 04_import_scan_2026-03-13_09-39-08.log
│   │   ├── 04_import_scan_2026-03-13_09-39-12.log
│   │   ├── 04_import_scan_2026-03-13_09-40-07.log
│   │   ├── 04_import_scan_2026-03-13_09-40-37.log
│   │   ├── 04_import_scan_2026-03-13_09-41-40.log
│   │   ├── 04_import_scan_2026-03-13_09-42-58.log
│   │   ├── 05_router_scan_2026-03-13_06-09-43.log
│   │   ├── 05_router_scan_2026-03-13_06-16-40.log
│   │   ├── 05_router_scan_2026-03-13_06-18-07.log
│   │   ├── 05_router_scan_2026-03-13_06-19-47.log
│   │   ├── 05_router_scan_2026-03-13_06-21-01.log
│   │   ├── 05_router_scan_2026-03-13_06-22-02.log
│   │   ├── 05_router_scan_2026-03-13_06-22-41.log
│   │   ├── 05_router_scan_2026-03-13_06-23-18.log
│   │   ├── 05_router_scan_2026-03-13_06-40-34.log
│   │   ├── 05_router_scan_2026-03-13_06-41-22.log
│   │   ├── 05_router_scan_2026-03-13_09-34-16.log
│   │   ├── 05_router_scan_2026-03-13_09-35-30.log
│   │   ├── 05_router_scan_2026-03-13_09-37-31.log
│   │   ├── 05_router_scan_2026-03-13_09-38-14.log
│   │   ├── 05_router_scan_2026-03-13_09-39-08.log
│   │   ├── 05_router_scan_2026-03-13_09-39-12.log
│   │   ├── 05_router_scan_2026-03-13_09-40-07.log
│   │   ├── 05_router_scan_2026-03-13_09-40-37.log
│   │   ├── 05_router_scan_2026-03-13_09-41-40.log
│   │   └── 05_router_scan_2026-03-13_09-42-58.log
│   ├── daily_audit.json
│   ├── daily_audit.md
│   ├── domain_dependency_guardrail_report.md
│   ├── educacao_reconciliation.json
│   ├── educacao_reconciliation.md
│   ├── entity_collision_scan.md
│   ├── migration_domain_inventory.md
│   ├── module_dependencies.md
│   ├── module_dependency_graph.json
│   ├── module_manifest_graph.json
│   ├── replace_core_imports_targets.txt
│   ├── sql_bottleneck_report.json
│   ├── sql_bottleneck_report.md
│   └── stress_test_real.json
├── requirements
├── run_smoke_test.sh
├── schema_phase_20_2.sql
├── scripts
│   ├── 05_apply_observability_global.py
│   ├── 06_apply_resilience_global.py
│   ├── __init__.py
│   ├── ai
│   │   ├── ai_scope_filter.py
│   │   ├── bootstrap_context.sh
│   │   ├── generate_ai_domain_kernel.py
│   │   ├── generate_architecture_graph.py
│   │   └── generate_module_architecture_docs.py
│   ├── arch_compiler.py
│   ├── architecture
│   │   ├── __init__.py
│   │   ├── audit
│   │   │   ├── circular_dependency_scan.py
│   │   │   ├── entity_collision_scan.py
│   │   │   └── full_arch_audit.py
│   │   ├── consolidate_modules.sh
│   │   ├── fix
│   │   │   └── replace_core_imports.sh
│   │   ├── generate_architecture_index.py
│   │   ├── generate_context_map.py
│   │   ├── module_diagnostics.py
│   │   ├── module_graph.py
│   │   ├── normalize_modules_v2.sh
│   │   ├── refactor_import_paths.sh
│   │   ├── report_generator.py
│   │   ├── run_analysis.py
│   │   ├── scanner.py
│   │   ├── similarity.py
│   │   ├── test_coherence.sh
│   │   └── universalize_modules.sh
│   ├── architecture_map_report.py
│   ├── architecture_scan.py
│   ├── audit_dependencies.sh
│   ├── audit_duplicates.sh
│   ├── audit_imports.py
│   ├── audit_modules.sh
│   ├── audit_modules_detailed.sh
│   ├── auto_git_push.sh
│   ├── check_python_syntax.py
│   ├── check_yaml_syntax.py
│   ├── clean_cache_dirs.py
│   ├── cleanup
│   │   ├── consolidate.py
│   │   └── remove_structural_debt.py
│   ├── cleanup_ambiente.sh
│   ├── cleanup_infrastructure.sh
│   ├── cleanup_phase2_comprehensive.sh
│   ├── config.yml
│   ├── config_manager.py
│   ├── consolidate_audit.py
│   ├── core
│   │   ├── sila.sh
│   │   ├── sila_config.sh
│   │   ├── sila_start.sh
│   │   ├── sila_stop.sh
│   │   └── status_sila.sh
│   ├── correct_paths.py
│   ├── create_domain_module.py
│   ├── daily_audit.sh
│   ├── db_diagnostico.sql
│   ├── deploy
│   │   ├── START_NGINX.sh
│   │   ├── package.sh
│   │   └── quick_deploy.sh
│   ├── dev
│   │   ├── advanced_project_analyzer.sh
│   │   ├── master-index.sh
│   │   ├── orphan_cleaner.py
│   │   └── project_analyzer.sh
│   ├── diagnostico_sila.sh
│   ├── domain_overlap_analysis.py
│   ├── educacao_reconciliation.py
│   ├── essential
│   │   └── check_credentials.py
│   ├── fix_npm_workspaces.sh
│   ├── fix_router_imports.py
│   ├── get_dev_token.sh
│   ├── guardrails
│   │   ├── allowlists
│   │   │   ├── README.md
│   │   │   ├── module_boundaries.json
│   │   │   └── v1.sh
│   │   ├── architecture_audit.py
│   │   ├── architecture_guardrails.sh
│   │   ├── check_ai_bootstrap_stack.py
│   │   ├── check_architecture_guide_sync.py
│   │   ├── check_core_namespace.py
│   │   ├── check_cycles.py
│   │   ├── check_domain_dependencies.py
│   │   ├── check_macro_boundaries.py
│   │   ├── check_macro_boundaries_final.py
│   │   ├── check_module_boundaries.py
│   │   ├── check_module_registry_sync.py
│   │   ├── run_all_guardrails.sh
│   │   └── run_guardrails.sh
│   ├── hooks
│   │   ├── install_pre_commit_hook.sh
│   │   └── pre-commit-audit-full.sh
│   ├── infra
│   │   ├── get-docker.sh
│   │   ├── install_vsc_extensions.sh
│   │   ├── monitor_sila.sh
│   │   ├── nginx_automation.sh
│   │   ├── nginx_diagnostic.sh
│   │   └── nginx_monitor.sh
│   ├── lib
│   │   ├── __init__.py
│   │   ├── colors.sh
│   │   ├── db_connector.py
│   │   ├── logging.sh
│   │   ├── nginx_config.sh
│   │   ├── nginx_deploy.sh
│   │   ├── nginx_diagnostic.sh
│   │   └── seeders.py
│   ├── list_provincial_users.py
│   ├── main.py
│   ├── maintenance
│   │   ├── changelog_auto.sh
│   │   ├── clean_pendrive_safe.sh
│   │   ├── cleanup.sh
│   │   ├── cleanup_temp_files.sh
│   │   ├── consolidate_root_scripts.sh
│   │   ├── repair_all.sh
│   │   ├── restructure_project.sh
│   │   ├── run_mass_fix_dryrun.sh
│   │   ├── safe_root_reorganizer.sh
│   │   ├── structure-guard.sh
│   │   └── update_comandos.sh
│   ├── mfa_example_fastapi.py
│   ├── migrate_to_libs.sh
│   ├── migrate_users_to_iam.py
│   ├── migration
│   │   ├── auto_migrate_legacy.py
│   │   ├── execute_auth_migration.sh
│   │   ├── fix_imports.py
│   │   ├── monitor-migration.sh
│   │   ├── onboarding.sh
│   │   └── prepare_migration.sh
│   ├── migration_domain_inventory.py
│   ├── migrations
│   │   ├── fix_identity_imports.py
│   │   ├── fix_shim_docstrings.py
│   │   └── fix_shim_escapes.py
│   ├── module_dependency_analysis.py
│   ├── module_health_report.py
│   ├── monitoring
│   │   ├── monitor-migration.sh
│   │   └── nginx_monitor.sh
│   ├── normalize_endpoints.sh
│   ├── phase_20_2_workers.sh
│   ├── pytest_wrapper.sh
│   ├── refactor_justice_imports.py
│   ├── refactor_modules.py
│   ├── reorg_tables_apply.py
│   ├── reorg_tables_apply.sh
│   ├── replace_service_hub.py
│   ├── reset_iam_passwords.py
│   ├── routes_health_monitor.py
│   ├── run_backend_diagnosis.sh
│   ├── run_dev_env.sh
│   ├── run_guardrails.sh
│   ├── run_permission_tests.sh
│   ├── safe_fixers.sh
│   ├── scan_integrity.py
│   ├── seed_admin_user.py
│   ├── seed_test_db.sh
│   ├── setup
│   │   ├── init_database.sh
│   │   ├── init_live_session.sh
│   │   └── setup_admin.sql
│   ├── setup_precommit.sh
│   ├── sql_bottleneck_report.py
│   ├── start_backend.sh
│   ├── start_event_bus_workers.sh
│   ├── start_services_local.sh
│   ├── stress_test_real.py
│   ├── sync_and_check_db.py
│   ├── sync_iam_system.py
│   ├── test_permissions.py
│   ├── tests
│   │   ├── simple_test.sh
│   │   ├── smoke-test.sh
│   │   ├── test_example.py
│   │   ├── test_nginx_automation.sh
│   │   ├── test_start_backend.sh
│   │   └── test_utils.py
│   ├── utils
│   │   ├── abrir-windsurf.sh
│   │   ├── autofix.py
│   │   ├── complete_env.sh
│   │   ├── make_executable.sh
│   │   ├── prepare_environment.sh
│   │   ├── run_with_pythonpath.sh
│   │   ├── test_runner.sh
│   │   └── validar_dependencias_sila.sh
│   ├── utils_new
│   │   └── validate_auth.py
│   ├── validate_frontend_backend_integration.py
│   └── validate_migrations.py
├── setup_dev_env.sh
├── setup_local_dev.sh
├── sila-maint
├── smoke_test.py
├── start-dev.sh
├── storage
│   └── logs
│       └── xroad_audit.chain
├── tailwind.config.js
├── test-api-cors.sh
├── test_audit_chain.py
├── test_hierarchy_endpoints_runner.sh
├── tests
│   ├── conftest.py
│   ├── conftest_hierarchy.py
│   ├── conftest_shared.py
│   ├── modules
│   │   ├── documents
│   │   │   └── test_document_service.py
│   │   ├── location
│   │   └── payment
│   │       ├── test_payment_endpoints.py
│   │       ├── test_service.py
│   │       ├── test_webhook_engine.py
│   │       └── test_webhook_service.py
│   ├── test_architecture_guardrails.py
│   ├── test_database_integrity.py
│   ├── test_dedup.py
│   ├── test_hierarchy_service_endpoints.py
│   ├── test_institutional_catalog_blueprint.py
│   ├── test_openai_client.py
│   ├── test_operational_state_machine.py
│   ├── test_operations_service.py
│   ├── test_phase3_integration.py
│   ├── test_phase_18_2_alerts_anomaly.py
│   ├── test_phase_18_3_orchestration.py
│   ├── test_phase_19_event_bus.py
│   ├── test_phase_19_event_bus_simple.py
│   ├── test_phase_20_1_db_persistence.py
│   ├── test_phase_20_2_bridge.py
│   ├── test_phase_20_2_extension_bridge.py
│   └── test_phase_20_event_sourcing.py
├── tools
│   ├── apply_extend_existing.py
│   ├── autoheal_imports.py
│   ├── check_location_import.py
│   ├── ci_import_check.py
│   ├── codegen
│   │   ├── create_sample_csv.py
│   │   ├── generate_module.py
│   │   ├── generate_phase2_docs.py
│   │   ├── sample.csv
│   │   ├── templates.py
│   │   └── utils.py
│   ├── consistency
│   │   ├── check_env_files.py
│   │   ├── check_imports.py
│   │   └── check_paths.py
│   ├── migrate_all_modules.py
│   ├── migrate_module.py
│   ├── refactor
│   │   └── update_paths.py
│   ├── run_separation_demo.sh
│   ├── split_models_schemas.py
│   ├── sqlite_removal_automation.py
│   ├── test_separation_system.py
│   ├── validate_separation.py
│   └── validators
│       └── dependency_checker.py
├── validate_event_bus.py
├── validate_fixes.py
├── validate_phase18.1.sh
├── verify_audit_artifacts.sh
├── verify_endpoint.py
├── verify_service.py
└── xroad_smoke_test.py

2250 directories, 4087 files
(.venv) dev03wsl@Rochete-consultoria:~/sila-system$