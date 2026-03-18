dev03wsl@Rochete-consultoria:~/sila-system$ tree -L 5 -I "venv|__pycache__|*.egg-info|node_modules|dist|build"
.
├── AI_ENTRYPOINTS.yaml
├── AI_FILE_SCOPE.yaml
├── API_MAP.yaml
├── ARCHITECTURE_DEPENDENCIES.yaml
├── ARCHITECTURE_INDEX.yaml
├── CONSOLIDATION_STATUS_REPORT.json
├── DUPLICATION_ANALYSIS.csv
├── DUPLICATION_ANALYSIS.json
├── DUPLICATION_SUMMARY.csv
├── Dockerfile.alerts
├── IAM_AUDIT_SUMMARY.csv
├── Makefile
├── Makefile.db
├── TODO.md
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
│       ├── 008_add_citizen_hierarchy_columns.py
│       └── 009_create_wallet_notifications_tables.py
├── app
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
│   │   │       ├── 20260314_052_transportes_logistica_audit_columns.py
│   │   │       ├── 20260314_053_wallet_notifications_tables.py
│   │   │       ├── 20260316_054_create_audit_logs.py
│   │   │       ├── 20260316_1100_export_jobs.py
│   │   │       ├── 20260316_1130_export_job_logs.py
│   │   │       ├── 20260318_1200_create_sla_engine_tables.py
│   │   │       ├── 20260318_1500_locations_parent_cascade.py
│   │   │       ├── 20260318_1510_merge_locations_cascade_head.py
│   │   │       ├── 20260318_1700_create_economy_financas_tables.py
│   │   │       ├── 20260318_1715_add_economy_audit_columns.py
│   │   │       ├── 2026_03_03_1304-3261f0e24605_modulo_juventude.py
│   │   │       ├── 2026_03_08_0847-47abb2f40d12_taxation_domain.py
│   │   │       ├── 2026_03_16_0639-6ce98d034292_iam_reconciliation.py
│   │   │       ├── 2026_03_16_0651-181c15049e80_citizenship_reconciliation.py
│   │   │       ├── 2026_03_16_0709-4b8e10487f5a_merge_heads.py
│   │   │       ├── 2026_03_16_0752-4fabf7e6d527_core_identity_reconciliation.py
│   │   │       ├── 2026_03_16_1618-22ab6d804070_merge_export_and_audit_heads.py
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
│   │   │   │   ├── router.py
│   │   │   │   ├── routers
│   │   │   │   └── schemas
│   │   │   ├── config.py
│   │   │   ├── conftest.py
│   │   │   ├── conftest_auth.py
│   │   │   ├── core
│   │   │   │   ├── AUDIT_REPORT.json
│   │   │   │   ├── __init__.py
│   │   │   │   ├── audit
│   │   │   │   ├── audit_compliance.py
│   │   │   │   ├── autonomous_economic_engine
│   │   │   │   ├── autonomous_government_agents
│   │   │   │   ├── autonomous_state
│   │   │   │   ├── bridges
│   │   │   │   ├── business
│   │   │   │   ├── cache
│   │   │   │   ├── catalog
│   │   │   │   ├── celery
│   │   │   │   ├── cloud_control
│   │   │   │   ├── communication
│   │   │   │   ├── config
│   │   │   │   ├── constants.py
│   │   │   │   ├── data_exchange
│   │   │   │   ├── data_platform
│   │   │   │   ├── database
│   │   │   │   ├── db
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── dev_platform
│   │   │   │   ├── document
│   │   │   │   ├── domain
│   │   │   │   ├── enums.py
│   │   │   │   ├── events
│   │   │   │   ├── exceptions
│   │   │   │   ├── feature_flags
│   │   │   │   ├── global_governance_protocol
│   │   │   │   ├── governance
│   │   │   │   ├── governance_ai
│   │   │   │   ├── identity
│   │   │   │   ├── integration
│   │   │   │   ├── integrations
│   │   │   │   ├── intelligence
│   │   │   │   ├── locks
│   │   │   │   ├── models
│   │   │   │   ├── models.py
│   │   │   │   ├── module_manifest.py
│   │   │   │   ├── module_registry.py
│   │   │   │   ├── monitoring
│   │   │   │   ├── national_ai_superintelligence
│   │   │   │   ├── notifications
│   │   │   │   ├── observability
│   │   │   │   ├── planetary_civilization_model
│   │   │   │   ├── platform
│   │   │   │   ├── quantum_internet_integration
│   │   │   │   ├── rate_limit
│   │   │   │   ├── rbac
│   │   │   │   ├── registry
│   │   │   │   ├── resilience
│   │   │   │   ├── schemas
│   │   │   │   ├── security
│   │   │   │   ├── sequencing.py
│   │   │   │   ├── services
│   │   │   │   ├── settings.py
│   │   │   │   ├── sila_os
│   │   │   │   ├── sla_engine
│   │   │   │   ├── sovereign_infrastructure
│   │   │   │   ├── sovereign_quantum_security
│   │   │   │   ├── tenants
│   │   │   │   ├── territory
│   │   │   │   ├── use-cases
│   │   │   │   ├── utils
│   │   │   │   ├── validate_refactor_simple.py
│   │   │   │   └── workflow
│   │   │   ├── db
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── migrations
│   │   │   │   └── seeds
│   │   │   ├── infrastructure
│   │   │   │   ├── event_sourcing
│   │   │   │   ├── message_broker
│   │   │   │   └── repositories
│   │   │   ├── main.py
│   │   │   ├── main.py.bak
│   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   └── iam_user.py
│   │   │   ├── modules
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api
│   │   │   │   ├── audit
│   │   │   │   ├── civil_protection
│   │   │   │   ├── compliance
│   │   │   │   ├── conftest.py
│   │   │   │   ├── documents
│   │   │   │   ├── economy
│   │   │   │   ├── educacao
│   │   │   │   ├── energy
│   │   │   │   ├── governance
│   │   │   │   ├── identity
│   │   │   │   ├── industry
│   │   │   │   ├── infrastructure
│   │   │   │   ├── infrastructure_sector
│   │   │   │   ├── intelligence
│   │   │   │   ├── justice
│   │   │   │   ├── logistics
│   │   │   │   ├── migration_service
│   │   │   │   ├── notifications
│   │   │   │   ├── operations
│   │   │   │   ├── payment
│   │   │   │   ├── procurement
│   │   │   │   ├── public_security
│   │   │   │   ├── resources
│   │   │   │   ├── saude
│   │   │   │   ├── society
│   │   │   │   ├── tests
│   │   │   │   ├── tourism
│   │   │   │   ├── wallet
│   │   │   │   └── xroad
│   │   │   ├── platform
│   │   │   │   ├── __init__.py
│   │   │   │   ├── integration
│   │   │   │   ├── observability
│   │   │   │   ├── persistence
│   │   │   │   ├── runtime
│   │   │   │   └── shared
│   │   │   ├── presentation
│   │   │   │   ├── api
│   │   │   │   └── schemas
│   │   │   ├── schemas
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth
│   │   │   │   ├── business.py
│   │   │   │   ├── citizen.py
│   │   │   │   └── user.py
│   │   │   ├── shared
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth
│   │   │   │   ├── database
│   │   │   │   ├── db
│   │   │   │   ├── events
│   │   │   │   ├── services
│   │   │   │   ├── utils
│   │   │   │   └── value_objects
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
│   │   │   ├── adapters
│   │   │   │   ├── __init__.py
│   │   │   │   └── adapter_factory.py
│   │   │   ├── audit
│   │   │   │   ├── __init__.py
│   │   │   │   ├── adapters
│   │   │   │   ├── audit_engine.py
│   │   │   │   └── middleware.py
│   │   │   ├── auth
│   │   │   │   ├── CONSOLIDATION_REPORT.json
│   │   │   │   ├── __init__.py
│   │   │   │   ├── guards
│   │   │   │   ├── jwt_handler.py
│   │   │   │   ├── keycloak_blueprint.md
│   │   │   │   ├── policies
│   │   │   │   ├── providers
│   │   │   │   └── roles
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
│   │   │   ├── exceptions
│   │   │   │   ├── __init__.py
│   │   │   │   ├── domain_exception.py
│   │   │   │   ├── domain_exception_factory.py
│   │   │   │   ├── factory.py
│   │   │   │   └── module_exception_factory.py
│   │   │   ├── exceptions.py
│   │   │   ├── exports
│   │   │   │   ├── __init__.py
│   │   │   │   └── tasks.py
│   │   │   ├── health.py
│   │   │   ├── logger.py
│   │   │   ├── metrics.py
│   │   │   ├── repositories
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_repository.py
│   │   │   │   └── repository_factory.py
│   │   │   ├── repositories.py
│   │   │   ├── routers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health_factory.py
│   │   │   │   └── router_factory.py
│   │   │   ├── schemas.py
│   │   │   ├── scope.py
│   │   │   ├── security
│   │   │   │   ├── __init__.py
│   │   │   │   └── iam_client.py
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
│   │   ├── fix_schema.py
│   │   ├── get-pip.py
│   │   ├── hydrate_vc_engine.sh
│   │   ├── interfaces
│   │   │   ├── grpc
│   │   │   └── http
│   │   ├── logs
│   │   │   └── test_db_connection.log
│   │   ├── main.py
│   │   ├── migrations
│   │   │   └── versions
│   │   │       └── 20260314_151759_merge_migrations_consolidation.py
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
│   │   ├── run_postgres_event_store_tests.sh
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
│   │   │   ├── fix_missing_imports.py
│   │   │   ├── generate_oidc_provider_keys.py
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
│   │   │   ├── locations_audit.py
│   │   │   ├── migrate_and_validate.py
│   │   │   ├── module_tools
│   │   │   │   ├── defesa_consumidor_generate_module.py
│   │   │   │   ├── estatistica_generate_module.py
│   │   │   │   ├── generate_module.py
│   │   │   │   └── setup_full_structure.py
│   │   │   ├── normalize_locations_title_case.sql
│   │   │   ├── run_health_check.py
│   │   │   ├── run_health_check.sh
│   │   │   ├── run_locations_maintenance.sh
│   │   │   ├── run_migration.sh
│   │   │   ├── run_role_level_guard_tests.py
│   │   │   ├── run_statistics_block_tests.sh
│   │   │   ├── seed_admin_roles.py
│   │   │   ├── seed_all_users.py
│   │   │   ├── seed_angola_dpa_2024.py
│   │   │   ├── seed_citizen_roles.py
│   │   │   ├── seed_educacao_institucional.py
│   │   │   ├── seed_financas_dashboard.py
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
│   │   │   │   ├── seed_fuc_golden_citizen.py
│   │   │   │   └── seed_locations_dpa_2024.py
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
│   │   │   ├── seed_phase_20_2_events.sql
│   │   │   └── seed_sla_completo.sql
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
│   │   │   │   ├── domain
│   │   │   │   ├── infrastructure
│   │   │   │   └── presentation
│   │   │   └── emails
│   │   │       ├── document_shared.html
│   │   │       ├── notification_base.html
│   │   │       └── payment_confirmed.html
│   │   ├── test_app_integration.py
│   │   ├── test_payment_endpoints_manual.py
│   │   ├── test_registry_debug.py
│   │   ├── test_router_import.py
│   │   ├── test_triple_bootstrap.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── ci_test_config.json
│   │   │   ├── citizen
│   │   │   │   └── unit
│   │   │   ├── conftest.py
│   │   │   ├── e2e
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── test_citizen_journey.py
│   │   │   │   ├── test_citizenship_flow.py
│   │   │   │   ├── test_integration_modules.py
│   │   │   │   ├── test_matricula_flow.py
│   │   │   │   ├── test_payment_flow.py
│   │   │   │   └── test_rabbitmq_integration.py
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
│   │   │   │   ├── db
│   │   │   │   ├── logging_config.py
│   │   │   │   ├── modules
│   │   │   │   ├── performance
│   │   │   │   ├── test_api_refactored.py
│   │   │   │   ├── test_app.py
│   │   │   │   ├── test_app_bootstrap.py
│   │   │   │   ├── test_appointments.py
│   │   │   │   ├── test_auth_flow.py
│   │   │   │   ├── test_auth_staging.py
│   │   │   │   ├── test_citizens.py
│   │   │   │   ├── test_commercial_schemas_fixed.py
│   │   │   │   ├── test_cqrs_flows.py
│   │   │   │   ├── test_db_connection.py
│   │   │   │   ├── test_environment.py
│   │   │   │   ├── test_global_imports.py
│   │   │   │   ├── test_health_endpoints.py
│   │   │   │   ├── test_health_run.py
│   │   │   │   ├── test_integration.py
│   │   │   │   ├── test_minimal_notifications.py
│   │   │   │   ├── test_output.py
│   │   │   │   ├── test_postgres_event_store.py
│   │   │   │   ├── test_services.py
│   │   │   │   ├── test_smoke.py
│   │   │   │   ├── test_users.py
│   │   │   │   └── utils
│   │   │   ├── load
│   │   │   │   └── test_operations_load.py
│   │   │   ├── module_health_check.py
│   │   │   ├── modules
│   │   │   │   ├── administracao_local
│   │   │   │   ├── agricultura
│   │   │   │   ├── aguas_saneamento
│   │   │   │   ├── ambiente
│   │   │   │   ├── apoio_empresarial
│   │   │   │   ├── arquivo_nacional
│   │   │   │   ├── assistencia_social
│   │   │   │   ├── aviacao_civil
│   │   │   │   ├── ciencia_pesquisa
│   │   │   │   ├── comercio
│   │   │   │   ├── comercio_externo
│   │   │   │   ├── cooperacao_internacional
│   │   │   │   ├── cultura
│   │   │   │   ├── defesa_consumidor
│   │   │   │   ├── desporto
│   │   │   │   ├── educacao
│   │   │   │   ├── emprego
│   │   │   │   ├── energia
│   │   │   │   ├── estatistica
│   │   │   │   ├── familia
│   │   │   │   ├── financas_impostos
│   │   │   │   ├── florestas
│   │   │   │   ├── gestao_fundiaria
│   │   │   │   ├── habitacao
│   │   │   │   ├── igualdade
│   │   │   │   ├── industria
│   │   │   │   ├── justica
│   │   │   │   ├── juventude
│   │   │   │   ├── meteorologia
│   │   │   │   ├── migracao
│   │   │   │   ├── obras_publicas
│   │   │   │   ├── patrimonio_cultural
│   │   │   │   ├── pecuaria
│   │   │   │   ├── pescas
│   │   │   │   ├── pescas_industriais
│   │   │   │   ├── petroleo_gas
│   │   │   │   ├── planeamento
│   │   │   │   ├── portos_logistica
│   │   │   │   ├── protecao_civil
│   │   │   │   ├── protecao_dados
│   │   │   │   ├── recursos_minerais
│   │   │   │   ├── registo_civil
│   │   │   │   ├── saude
│   │   │   │   ├── seguranca_alimentar
│   │   │   │   ├── seguranca_publica
│   │   │   │   ├── seguranca_social
│   │   │   │   ├── tecnologia_inovacao
│   │   │   │   ├── telecomunicacoes
│   │   │   │   ├── trabalho_inspecao
│   │   │   │   ├── transportes
│   │   │   │   ├── turismo
│   │   │   │   └── urbanismo
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
│   │   │   ├── validation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_domain_logic.py
│   │   │   │   ├── test_module_boundaries.py
│   │   │   │   └── test_router_validation.py
│   │   │   └── wsl.localhost
│   │   │       └── Ubuntu
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
│   │   │   └── vite.svg
│   │   ├── src
│   │   │   ├── App.css
│   │   │   ├── App.tsx
│   │   │   ├── api
│   │   │   │   ├── adminHttp.ts
│   │   │   │   ├── axios.ts
│   │   │   │   ├── citizenHttp.ts
│   │   │   │   ├── generated
│   │   │   │   └── http.ts
│   │   │   ├── assets
│   │   │   │   ├── images
│   │   │   │   └── react.svg
│   │   │   ├── auth
│   │   │   │   └── keycloak.ts
│   │   │   ├── components
│   │   │   │   ├── Admin
│   │   │   │   ├── AdminObservability.tsx
│   │   │   │   ├── Auth
│   │   │   │   ├── Dashboard
│   │   │   │   ├── Documents
│   │   │   │   ├── Layout
│   │   │   │   ├── Layout.tsx
│   │   │   │   ├── ObservabilityOverview.tsx
│   │   │   │   ├── Payment
│   │   │   │   ├── ProtectedRoute.tsx
│   │   │   │   ├── Search
│   │   │   │   ├── Statistics
│   │   │   │   ├── Toast.tsx
│   │   │   │   └── Upload
│   │   │   ├── constants
│   │   │   │   └── images.ts
│   │   │   ├── constants.tsx
│   │   │   ├── hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useDocumentStatus.ts
│   │   │   │   ├── useDocumentUpload.ts
│   │   │   │   ├── useMyDocuments.ts
│   │   │   │   └── useToast.tsx
│   │   │   ├── index.css
│   │   │   ├── index.tsx
│   │   │   ├── main.tsx
│   │   │   ├── modules
│   │   │   │   ├── admin
│   │   │   │   ├── citizen
│   │   │   │   ├── identity
│   │   │   │   ├── meteorologia
│   │   │   │   └── pagamentos
│   │   │   ├── pages
│   │   │   │   ├── AdminAuditViewer.tsx
│   │   │   │   ├── AdminCitizenFuc.tsx
│   │   │   │   ├── AdminCitizenProfile.tsx
│   │   │   │   ├── AdminCitizens.tsx
│   │   │   │   ├── AdminDocumentProfile.tsx
│   │   │   │   ├── AdminDocuments.tsx
│   │   │   │   ├── AdminExports.tsx
│   │   │   │   ├── AdminObservability.tsx
│   │   │   │   ├── AdminStatistics.tsx
│   │   │   │   ├── AdminTerritory.tsx
│   │   │   │   ├── BiometricEnrollmentPage.tsx
│   │   │   │   ├── CitizenDashboard.tsx
│   │   │   │   ├── CitizenLogin.tsx
│   │   │   │   ├── CitizenPortal.tsx
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── DocumentsView.tsx
│   │   │   │   ├── IdentityPage.tsx
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
│   │   │   │   ├── adminDocumentService.ts
│   │   │   │   ├── api.ts
│   │   │   │   ├── apiService.ts
│   │   │   │   ├── auth.ts
│   │   │   │   ├── authGuard.ts
│   │   │   │   ├── authService.ts
│   │   │   │   ├── citizenAuthService.ts
│   │   │   │   ├── citizenService.ts
│   │   │   │   ├── dashboardService.ts
│   │   │   │   ├── documentService.ts
│   │   │   │   ├── exportJobsService.ts
│   │   │   │   ├── operationsService.ts
│   │   │   │   ├── sla.ts
│   │   │   │   └── territoryService.ts
│   │   │   ├── store
│   │   │   │   └── authStore.ts
│   │   │   ├── types
│   │   │   │   ├── api.ts
│   │   │   │   └── auth.ts
│   │   │   ├── types.ts
│   │   │   └── utils
│   │   │       ├── cn.ts
│   │   │       └── globalToast.ts
│   │   ├── tailwind.config.js
│   │   ├── tsconfig.app.json
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   └── vite.config.ts
│   └── worker
├── code-quality.workflow
├── conftest.py
├── docs
│   ├── AI_ARCHITECTURE_GRAPH.yaml
│   ├── architecture
│   │   ├── REPOSITORY_MAP.yaml
│   │   ├── domain_dependency_policy.yaml
│   │   ├── domains
│   │   │   ├── core_system
│   │   │   ├── economy
│   │   │   ├── educacao
│   │   │   ├── environment
│   │   │   ├── governance
│   │   │   ├── identity
│   │   │   ├── infrastructure
│   │   │   ├── infrastructure_sector
│   │   │   ├── intelligence
│   │   │   ├── justice
│   │   │   ├── resources
│   │   │   ├── security
│   │   │   ├── social
│   │   │   └── society
│   │   └── entrypoints
│   ├── modules
│   │   └── tree.modules.txt
│   ├── seed_angola_dpa_2024.cpython-312.pyc
│   └── tree.md
├── er_id, status, severity, ts in result.fetchall():
├── find_broken_imports.py
├── hell -Command "q" 2>$null
├── infra
│   ├── alerts
│   │   ├── alert-rules.yml
│   │   └── alertmanager.yml
│   ├── docker-compose.alerts.yml
│   ├── docker-compose.elk.yml
│   ├── docker-compose.events.yml
│   ├── docker-compose.override.yml
│   ├── docker-compose.prod.yml
│   ├── docker-compose.yml
│   ├── identity
│   │   ├── docker-compose.yml
│   │   └── realm
│   │       └── sila-realm.json
│   ├── logging
│   │   ├── filebeat.yml
│   │   └── logstash.conf
│   └── observability
│       ├── grafana-dashboards.yml
│       ├── grafana-datasources.yml
│       └── prometheus.yml
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
│       │   │   └── react.svg
│       │   ├── components
│       │   │   ├── Admin
│       │   │   ├── Auth
│       │   │   ├── Dashboard
│       │   │   ├── Documents
│       │   │   ├── Layout
│       │   │   ├── Layout.tsx
│       │   │   ├── Payment
│       │   │   ├── ProtectedRoute.tsx
│       │   │   ├── Search
│       │   │   ├── Statistics
│       │   │   └── Upload
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
│       │   │   ├── identity
│       │   │   ├── meteorologia
│       │   │   └── pagamentos
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
│       │       ├── cn.ts
│       │       └── globalToast.ts
│       ├── tailwind.config.js
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       └── vite.config.ts
├── l bash -c PGPASSWORD=Trumanmarcelo_1983 psql -h localhost -U sila_user -d sila_db --pset=pager=off -c 'SELECT action, user_id, status, severity, timestamp FROM audit_logs ORDER BY timestamp DESC LIMIT 5' 2>&1 | grep -v '^$'
├── logs
│   ├── event_worker.log
│   ├── outbox_worker.log
│   └── test_db_connection.log
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
├── mypy.ini
├── observability
│   ├── __init__.py
│   ├── logging
│   ├── metrics
│   └── tracing
├── openapi.json
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
│   │   │   │   └── provisioning
│   │   │   ├── prometheus
│   │   │   │   ├── prometheus.yml
│   │   │   │   └── rules
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
│       └── media
├── pytest.ini
├── reports
│   ├── consolidation
│   │   ├── consolidate_identity_core.log
│   │   └── consolidate_justice_core.log
│   ├── locations_corrections_full.csv
│   ├── locations_corrections_suggested.csv
│   ├── locations_name_audit.md
│   ├── locks
│   │   ├── identity_core.lock
│   │   └── justice_core.lock
│   ├── module_dependencies.md
│   ├── module_dependency_graph.json
│   └── sla_provinces_snapshot.md
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── scripts
│   ├── 05_apply_observability_global.py
│   ├── 06_apply_resilience_global.py
│   ├── __init__.py
│   ├── acao_compliance_audit.py
│   ├── ai
│   │   ├── ai_scope_filter.py
│   │   ├── bootstrap_context.sh
│   │   ├── generate_ai_domain_kernel.py
│   │   ├── generate_architecture_graph.py
│   │   └── generate_module_architecture_docs.py
│   ├── alembic_health_check.py
│   ├── arch_compiler.py
│   ├── architecture
│   │   ├── __init__.py
│   │   ├── analyze_deficits_detailed.sh
│   │   ├── audit
│   │   │   ├── circular_dependency_scan.py
│   │   │   ├── entity_collision_scan.py
│   │   │   └── full_arch_audit.py
│   │   ├── consolidate_modules.sh
│   │   ├── evaluate_deficits_simple.sh
│   │   ├── evaluate_module_deficits.sh
│   │   ├── fix
│   │   │   └── replace_core_imports.sh
│   │   ├── generate_architecture_index.py
│   │   ├── generate_context_map.py
│   │   ├── generate_module_discovery.sh
│   │   ├── lint_architecture.sh
│   │   ├── module_diagnostics.py
│   │   ├── module_graph.py
│   │   ├── normalize_architecture.sh
│   │   ├── normalize_module.sh
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
│   ├── audit
│   │   ├── DIAGNOSTIC_REPORT.sh
│   │   ├── generate_compliance_report.sh
│   │   ├── inspect_db.sh
│   │   ├── run_smoke_test.sh
│   │   ├── smoke_test.py
│   │   ├── test-api-cors.sh
│   │   ├── test_audit_chain.py
│   │   ├── test_economy_transactions.py
│   │   ├── test_hierarchy_endpoints_runner.sh
│   │   ├── validate_event_bus.py
│   │   ├── validate_fixes.py
│   │   ├── validate_phase18.1.sh
│   │   ├── validate_routers.sh
│   │   ├── verify_audit_artifacts.sh
│   │   ├── verify_economy_endpoints.py
│   │   ├── verify_endpoint.py
│   │   ├── verify_service.py
│   │   └── xroad_smoke_test.py
│   ├── audit_dependencies.py
│   ├── audit_dependencies.sh
│   ├── audit_duplicates.sh
│   ├── audit_imports.py
│   ├── audit_modules.py
│   ├── audit_modules.sh
│   ├── audit_modules_detailed.sh
│   ├── auto_git_push.sh
│   ├── check_application_layer.py
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
│   ├── dependency_audit.py
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
│   ├── fase5_assessment.py
│   ├── final_status_report.py
│   ├── fix_npm_workspaces.sh
│   ├── fix_router_imports.py
│   ├── generate_modules.py
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
│   ├── lift_core_layers.py
│   ├── list_provincial_users.py
│   ├── main.py
│   ├── maintenance
│   │   ├── changelog_auto.sh
│   │   ├── clean_exceptions.py
│   │   ├── clean_pendrive_safe.sh
│   │   ├── cleanup.sh
│   │   ├── cleanup_temp_files.sh
│   │   ├── consolidate_and_purge.sh
│   │   ├── consolidate_identity_core.sh
│   │   ├── consolidate_justice_core.sh
│   │   ├── consolidate_root_scripts.sh
│   │   ├── fix_import_paths.sh
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
│   │   ├── P0A_DELETE_BASE_REPOSITORY.py
│   │   ├── P0A_DELETE_BASE_REPOSITORY.sh
│   │   ├── batch_extraction_identity.sh
│   │   ├── batch_health_education_migrate.sh
│   │   ├── batch_health_education_mkdir.sh
│   │   ├── batch_purge_identity.sh
│   │   ├── create_domain_enums.sh
│   │   ├── create_domain_exceptions.sh
│   │   ├── execute_phase_20_2_schema.py
│   │   ├── fix_identity_imports.py
│   │   ├── fix_shim_docstrings.py
│   │   ├── fix_shim_escapes.py
│   │   ├── migrate_justice_structure.sh
│   │   └── schema_phase_20_2.sql
│   ├── module_dependency_analysis.py
│   ├── module_health_report.py
│   ├── module_tools
│   │   └── enterprise_fix.py
│   ├── monitoring
│   │   ├── monitor-migration.sh
│   │   └── nginx_monitor.sh
│   ├── normalize_endpoints.sh
│   ├── operation_simetria.py
│   ├── ops
│   │   ├── access_db.sh
│   │   ├── cleanup.sh
│   │   ├── cleanup_seeds.sh
│   │   ├── deploy-wsl2.sh
│   │   ├── docker-clean-and-up.sh
│   │   ├── quickstart-event-bus.sh
│   │   ├── seed_citizen_events.sql
│   │   ├── setup_dev_env.sh
│   │   ├── setup_local_dev.sh
│   │   └── start-dev.sh
│   ├── performance_tests.py
│   ├── phase5_final_report.py
│   ├── phase_20_2_workers.sh
│   ├── pytest_wrapper.sh
│   ├── rabbitmq_broker_integration.py
│   ├── rabbitmq_integration_tests.py
│   ├── refactor_justice_imports.py
│   ├── refactor_modules.py
│   ├── reorg_tables_apply.py
│   ├── reorg_tables_apply.sh
│   ├── repair_acl_imports.py
│   ├── replace_service_hub.py
│   ├── reset_iam_passwords.py
│   ├── resolve_migration_heads.py
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
│   ├── test_report_visual.py
│   ├── tests
│   │   ├── create_test_structure.sh
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
│   ├── validate_migrations.py
│   ├── validate_modules.py
│   ├── validate_ports_adapters.py
│   └── validate_rabbitmq.py
├── sila-maint
├── src
│   ├── api
│   │   └── axios.ts
│   ├── modules
│   │   └── admin
│   │       ├── components
│   │       │   └── AdminDashboard.tsx
│   │       ├── hooks
│   │       │   └── useDashboard.ts
│   │       └── types
│   │           └── index.ts
│   ├── pages
│   │   └── ServicesPage.tsx
│   ├── services
│   │   ├── orderApi.ts
│   │   ├── paymentApi.ts
│   │   └── serviceApi.ts
│   └── types
│       └── api.ts
├── startup.log
├── storage
│   └── logs
│       └── xroad_audit.chain
├── tailwind.config.js
├── temp_seed.py
├── templates
│   ├── CORE_AUTH_INTEGRATION_TEMPLATE.py
│   ├── MODULE_DISCOVERY_TEMPLATE.yaml
│   ├── TEMPLATE_DOMAIN_EXCEPTION_PATTERN.py
│   ├── TEMPLATE_EXCEPTIONS_PATTERN.py
│   ├── TEMPLATE_REPOSITORY_PATTERN.py
│   └── sla
│       ├── dashboard.html
│       └── simulator.html
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
│   ├── test_modules_real.py
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
├── tmp
├── tools
│   ├── apply_extend_existing.py
│   ├── autoheal_imports.py
│   ├── check_location_import.py
│   ├── ci_import_check.py
│   ├── cleanup_saude_refs.py
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
│   ├── discover_auth_imports.py
│   ├── heal_identity_bridge.py
│   ├── migrate_all_modules.py
│   ├── migrate_module.py
│   ├── refactor
│   │   └── update_paths.py
│   ├── repair_imports_ast.py
│   ├── run_separation_demo.sh
│   ├── split_models_schemas.py
│   ├── sqlite_removal_automation.py
│   ├── test_separation_system.py
│   ├── validate_separation.py
│   └── validators
│       └── dependency_checker.py
└── ult = await db.execute(text(

433 directories, 1006 files
dev03wsl@Rochete-consultoria:~/sila-system$