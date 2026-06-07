dev03wsl@Rochete-consultoria:~/sila-system$ ls -f
.              reports                  tailwind.config.js  .env          sandbox       .gitlab-ci.architecture-audit.yml  .gitlab-ci.yml     templates                .env.devcontainer
..             .pre-commit-config.yaml  openapi.json        restart       scripts       Dockerfile.alerts                  .dockerignore      data                     .env.docker.example
.github        gmx                      sila-maint          .continue     .git          observability                      poetry.lock        .flake8                  pytest.ini
docs           .devcontainer            modules_report.md   .vscode       node_modules  foundation                         .env.host.example  sila_platform            Makefile.db
.agentignore   .ai                      .import-linter      .env.example  tools         docker-compose.minimal.yml         pyproject.toml     .secrets.baseline        .venv
.ruff_cache    tests                    .env.test.example   Makefile      .bandit       storage                            .cursorrules       .env.production.example  .coveragerc
.pytest_cache  conftest.py              .env.local          domain        infra         cleanup_continue.sh                requirements       interfaces               migrations
logs           .sixthrules              .gitignore          orchestrator  tmp           env                                .yamllint          apps
dev03wsl@Rochete-consultoria:~/sila-system$ tree -L 4 -I "venv|__pycache__|*.egg-info|node_modules|dist|build"
.
├── Dockerfile.alerts
├── Makefile
├── Makefile.db
├── apps
│   ├── __init__.py
│   ├── api_gateway
│   │   ├── eligibility.py
│   │   └── main.py
│   ├── backend
│   │   ├── 0.1.4
│   │   ├── 01_eliminate_db_duplication.sh
│   │   ├── 01_fix_imports_pragmatic.py
│   │   ├── 09_final_verification.sh
│   │   ├── Dockerfile
│   │   ├── Dockerfile.prod
│   │   ├── EXCEPTION_CONSOLIDATION_DISCOVERY.md
│   │   ├── EXCEPTION_CONSOLIDATION_EXECUTION.md
│   │   ├── FASE3_DEPLOYMENT_CHECK.sh
│   │   ├── Makefile
│   │   ├── REPOSITORY_CONSOLIDATION_DISCOVERY.md
│   │   ├── STRATEGIC_DECISION_POINT.py
│   │   ├── TEMPLATE_DDD_MODULE.py
│   │   ├── __init__.py
│   │   ├── _test_emis_final.py
│   │   ├── alembic
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   ├── alembic.ini
│   │   ├── analyze_duplicates.py
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   ├── api
│   │   │   ├── config.py
│   │   │   ├── conftest.py
│   │   │   ├── conftest_auth.py
│   │   │   ├── core
│   │   │   ├── db
│   │   │   ├── foundation
│   │   │   ├── infrastructure
│   │   │   ├── main.py
│   │   │   ├── main.py.bak
│   │   │   ├── models
│   │   │   ├── modules
│   │   │   ├── platform
│   │   │   ├── presentation
│   │   │   ├── schemas
│   │   │   ├── shared
│   │   │   ├── utils
│   │   │   └── workers
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
│   │   │   ├── audit
│   │   │   ├── auth
│   │   │   ├── cache
│   │   │   ├── celery
│   │   │   ├── config.py
│   │   │   ├── db
│   │   │   ├── dependencies
│   │   │   ├── events
│   │   │   ├── exceptions
│   │   │   ├── exceptions.py
│   │   │   ├── exports
│   │   │   ├── health.py
│   │   │   ├── logger.py
│   │   │   ├── metrics.py
│   │   │   ├── repositories
│   │   │   ├── repositories.py
│   │   │   ├── routers
│   │   │   ├── schemas.py
│   │   │   ├── scope.py
│   │   │   ├── security
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
│   │   │   ├── identity
│   │   │   └── user-guide
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
│   │   ├── module_health_dashboard.html
│   │   ├── observability
│   │   │   ├── __init__.py
│   │   │   └── sentry_config.py
│   │   ├── platform
│   │   │   ├── config
│   │   │   ├── logging
│   │   │   └── middleware
│   │   ├── poetry.lock
│   │   ├── post-mutation-pipeline.log
│   │   ├── production_check.sh
│   │   ├── pytest.ini
│   │   ├── refactor_locations.py
│   │   ├── reports
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
│   │   │   ├── generate_service_registry.py
│   │   │   ├── import_service_catalog.py
│   │   │   ├── init-db.sql
│   │   │   ├── legacy
│   │   │   ├── list_provincial_users.py
│   │   │   ├── locations_audit.py
│   │   │   ├── migrate_and_validate.py
│   │   │   ├── module_tools
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
│   │   │   ├── validate_config.py
│   │   │   └── validate_service_registry.py
│   │   ├── seed_21_provinces_final.py
│   │   ├── seed_users.sql
│   │   ├── seed_users_v4.py
│   │   ├── seeds
│   │   │   ├── __init__.py
│   │   │   ├── catalog.py
│   │   │   ├── core
│   │   │   ├── roles.py
│   │   │   ├── run.py
│   │   │   ├── run_all.py
│   │   │   ├── run_master_seed.py
│   │   │   ├── scripts
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
│   │   ├── start_automation_worker.py
│   │   ├── start_dlq_worker.py
│   │   ├── static
│   │   │   ├── __init__.py
│   │   │   └── pdfs
│   │   ├── templates
│   │   │   ├── DDD_MODULE_ENTERPRISE
│   │   │   └── emails
│   │   ├── test_app_integration.py
│   │   ├── test_payment_endpoints_manual.py
│   │   ├── test_registry_debug.py
│   │   ├── test_router_import.py
│   │   ├── test_triple_bootstrap.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── _check_leftovers.py
│   │   │   ├── _check_schema.py
│   │   │   ├── ci_test_config.json
│   │   │   ├── citizen
│   │   │   ├── conftest.py
│   │   │   ├── e2e
│   │   │   ├── factories
│   │   │   ├── fixtures
│   │   │   ├── integration
│   │   │   ├── load
│   │   │   ├── module_health_check.py
│   │   │   ├── modules
│   │   │   ├── test_alembic_chain.py
│   │   │   ├── test_alembic_health.py
│   │   │   ├── test_audit_analytics.py
│   │   │   ├── test_auth_consolidated.py
│   │   │   ├── test_basic_endpoints.py
│   │   │   ├── test_catalog_governance.py
│   │   │   ├── test_citizen_documents.py
│   │   │   ├── test_duplicate_detection.py
│   │   │   ├── test_e2e_flow.py
│   │   │   ├── test_ens_concurrency.py
│   │   │   ├── test_import_check.py
│   │   │   ├── test_modules_ping.py
│   │   │   ├── test_profile_queries.py
│   │   │   ├── test_quality_report.json
│   │   │   ├── test_sla_definitions.py
│   │   │   ├── test_smoke_production.py
│   │   │   ├── test_territory_api.py
│   │   │   ├── unit
│   │   │   ├── utils
│   │   │   ├── validation
│   │   │   └── wsl.localhost
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
│   │   ├── educacao
│   │   │   └── admin
│   │   ├── eslint.config.js
│   │   ├── index.html
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── package.json.tmp
│   │   ├── postcss.config.js
│   │   ├── public
│   │   │   └── vite.svg
│   │   ├── src
│   │   │   ├── App.css
│   │   │   ├── App.tsx
│   │   │   ├── api
│   │   │   ├── assets
│   │   │   ├── auth
│   │   │   ├── components
│   │   │   ├── constants
│   │   │   ├── constants.tsx
│   │   │   ├── hooks
│   │   │   ├── index.css
│   │   │   ├── index.tsx
│   │   │   ├── main.tsx
│   │   │   ├── modules
│   │   │   ├── pages
│   │   │   ├── router
│   │   │   ├── services
│   │   │   ├── store
│   │   │   ├── types
│   │   │   ├── types.ts
│   │   │   ├── utils
│   │   │   └── vite-env.d.ts
│   │   ├── tailwind.config.js
│   │   ├── tsconfig.app.json
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   ├── vacancy-marketplace-example.html
│   │   └── vite.config.ts
│   └── worker
├── cleanup_continue.sh
├── conftest.py
├── data
│   ├── foundation_outbox.db
│   ├── policies.json
│   ├── policies_audit.log
│   ├── policy_scan_report.json
│   ├── processed
│   │   └── catalogo.json
│   └── raw
│       └── catalogo_900.csv
├── docker-compose.minimal.yml
├── docs
│   ├── AI_ARCHITECTURE_GRAPH.yaml
│   ├── adr
│   ├── architecture
│   │   ├── API_MAP.yaml
│   │   ├── ARCHITECTURE_DEPENDENCIES.yaml
│   │   ├── ARCHITECTURE_INDEX.yaml
│   │   ├── REPOSITORY_MAP.yaml
│   │   ├── domain_dependency_policy.yaml
│   │   ├── domains
│   │   │   ├── economy
│   │   │   ├── educacao
│   │   │   ├── governance
│   │   │   ├── infrastructure_sector
│   │   │   ├── intelligence
│   │   │   ├── justice
│   │   │   ├── resources
│   │   │   └── society
│   │   └── entrypoints
│   │       ├── API_ENTRYPOINTS.md
│   │       ├── BACKEND_ARCHITECTURE.md
│   │       ├── DATA_FLOW.md
│   │       ├── DOMAIN_MAP.md
│   │       └── SYSTEM_OVERVIEW.md
│   ├── audit
│   │   └── registry_coverage_report.md
│   ├── educacao
│   │   ├── TRANSACTIONAL_CORE_PR_CHECKLIST.md
│   │   ├── TRANSACTIONAL_CORE_RFC.md
│   │   └── TRANSACTIONAL_CORE_SPEC.md
│   ├── implementation
│   │   ├── FASE_3_2_IMPLEMENTATION_SUMMARY.md
│   │   ├── PASSO_13_14_CHECKLIST.md
│   │   ├── PASSO_13_14_IMPLEMENTATION.md
│   │   ├── PASSO_13_14_IMPLEMENTATION_SUMMARY.md
│   │   ├── PASSO_6_IMPLEMENTATION.md
│   │   ├── PASSO_7_TRANSFER_TRANSACTION.md
│   │   ├── PLANO_PASSO_13_14_FINAL.md
│   │   └── code-quality.workflow
│   ├── modules
│   │   └── tree.modules.txt
│   ├── roadmaps
│   │   ├── FASE_3_2_CITIZEN_MARKETPLACE_PLAN.md
│   │   ├── ROADMAP_COMPLETO.md
│   │   └── TODO.md
│   └── tree.md
├── domain
│   ├── academic_identity.py
│   ├── academic_status.py
│   ├── eligibility_rule.py
│   ├── enrollment_automation.py
│   ├── institution_capacity.py
│   ├── transfer_automation.py
│   ├── transfer_policy.py
│   └── vacancy_marketplace.py
├── env
│   └── homologation
├── foundation
│   ├── __init__.py
│   ├── automation
│   │   ├── automator.py
│   │   └── message_bus.py
│   ├── eligibility
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── conditions.py
│   │   ├── engine.py
│   │   ├── evaluator.py
│   │   ├── exceptions.py
│   │   ├── policies.py
│   │   ├── rules.py
│   │   └── scoring.py
│   ├── matching
│   │   ├── __init__.py
│   │   ├── compatibility.py
│   │   ├── engine.py
│   │   ├── exceptions.py
│   │   ├── health.py
│   │   ├── ranking.py
│   │   ├── recommendation.py
│   │   └── scorer.py
│   ├── orchestration
│   │   ├── dlq.py
│   │   └── orchestrator.py
│   ├── persistence
│   │   ├── __init__.py
│   │   └── educacao_repository.py
│   ├── policies
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── defaults.py
│   │   └── engine.py
│   ├── resilience
│   │   ├── __init__.py
│   │   └── idempotency.py
│   └── search
│       ├── __init__.py
│       ├── engine.py
│       ├── filters.py
│       ├── indexer.py
│       ├── queries.py
│       └── ranking.py
├── gmx
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
│       └── prometheus.yml
├── interfaces
│   └── dashboard
│       └── institutional_dashboard.py
├── logs
│   ├── event_worker.log
│   ├── outbox_worker.log
│   └── test_db_connection.log
├── migrations
│   ├── README.md
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
│       ├── 20260524_create_foundation_outbox.py
│       └── __init__.py
├── modules_report.md
├── observability
│   ├── __init__.py
│   ├── grafana
│   │   ├── README.md
│   │   ├── dashboards
│   │   │   └── sila_backend_dashboard.json
│   │   ├── provisioning
│   │   │   ├── dashboards
│   │   │   └── datasources
│   │   └── sila_backend_dashboard.json
│   ├── logging
│   ├── metrics
│   ├── prometheus
│   │   └── alert_rules
│   │       ├── README.md
│   │       └── passo_10_sla_rules.yaml
│   ├── prometheus_job_example.yml
│   └── tracing
├── openapi.json
├── orchestrator
│   └── infrastructure
│       └── factory
│           └── unified_ports_factory.py
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── reports
│   ├── AUDIT_NOTES.md
│   ├── AUTONOMY_CHECKLIST.md
│   ├── CHANGELOG.md
│   ├── PASSO_6_VALIDATION_REPORT.sh
│   ├── PASSO_7_VALIDATION_REPORT.sh
│   ├── PR_DESCRIPTION.md
│   ├── ai_architecture_graph.json
│   ├── ai_architecture_graph_visual_report.md
│   ├── ai_domain_kernel_visual_report.md
│   ├── architecture
│   │   ├── AI_ARCHITECTURE_GRAPH.yaml
│   │   ├── REPOSITORY_MAP.yaml
│   │   └── domain_dependency_policy.yaml
│   ├── architecture_index_visual_report.md
│   ├── audits
│   │   ├── IAM_AUDIT_SUMMARY.csv
│   │   ├── cleanup_audit.jsonl
│   │   └── modules_report.md
│   ├── autonomy_100_percent.json
│   ├── consolidation
│   │   ├── consolidate_identity_core.log
│   │   └── consolidate_justice_core.log
│   ├── daily_audit
│   │   ├── 01_arch_sync_2026-06-07_08-18-19.log
│   │   ├── 02_domain_audit_2026-06-07_08-18-19.log
│   │   ├── 03_module_diagnostics_2026-06-07_08-18-19.log
│   │   ├── 04_import_scan_2026-06-07_08-18-19.log
│   │   └── 05_router_scan_2026-06-07_08-18-19.log
│   ├── daily_audit.json
│   ├── daily_audit.md
│   ├── domain_dependency_guardrail_report.md
│   ├── eligibility_audit.log
│   ├── government_dependency_graph.md
│   ├── legacy_analysis
│   │   ├── ANGOLA_CANDIDATES.txt
│   │   ├── ARCHIVE_DIFF_REPORT.md
│   │   ├── CONSOLIDATION_STATUS_REPORT.json
│   │   ├── DUPLICATION_ANALYSIS.csv
│   │   ├── DUPLICATION_ANALYSIS.json
│   │   ├── DUPLICATION_SUMMARY.csv
│   │   └── RESCUE_CANDIDATES.txt
│   ├── locations_corrections_full.csv
│   ├── locations_corrections_suggested.csv
│   ├── locations_name_audit.md
│   ├── locks
│   │   ├── identity_core.lock
│   │   └── justice_core.lock
│   ├── migration_domain_inventory.md
│   ├── ministerial_validation.md
│   ├── module_architecture_docs_visual_report.md
│   ├── module_dependencies.md
│   ├── module_dependency_graph.json
│   ├── module_manifest_graph.json
│   ├── mutation
│   │   └── post-mutation-pipeline.log
│   ├── orchestrator_dlq.log
│   ├── quality
│   │   ├── openapi_live.json
│   │   └── openapi_routes.csv
│   ├── runtime
│   └── sla_provinces_snapshot.md
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── restart
├── sandbox
│   ├── experiments
│   │   └── FASE_3_2_INTEGRATION_EXAMPLES.py
│   └── temporary
│       └── test_codex.txt
├── scripts
│   ├── 05_apply_observability_global.py
│   ├── 06_apply_resilience_global.py
│   ├── __init__.py
│   ├── acao_compliance_audit.py
│   ├── activate-autonomy.sh
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
│   ├── b904-batch-fixer.py
│   ├── catalog_mapper.py
│   ├── check_application_layer.py
│   ├── check_asyncsession_import.py
│   ├── check_python_syntax.py
│   ├── check_table.py
│   ├── check_yaml_syntax.py
│   ├── clean_cache_dirs.py
│   ├── cleanup
│   │   ├── consolidate.py
│   │   ├── remove_structural_debt.py
│   │   └── super_cleanup.py
│   ├── cleanup.sh
│   ├── cleanup_ambiente.sh
│   ├── cleanup_artifacts.py
│   ├── cleanup_infrastructure.sh
│   ├── cleanup_phase2_comprehensive.sh
│   ├── config.yml
│   ├── config_manager.py
│   ├── consolidate_audit.py
│   ├── consolidate_exceptions_execute.py
│   ├── consolidate_exceptions_sila.py
│   ├── consolidate_repositories_sila.py
│   ├── consolidation
│   │   ├── 01_frontend_merge.sh
│   │   ├── 02_alembic_cleanup.sh
│   │   └── 03_base_repository_scan.sh
│   ├── consolidation.sh
│   ├── core
│   │   ├── sila.sh
│   │   ├── sila_config.sh
│   │   ├── sila_start.sh
│   │   ├── sila_stop.sh
│   │   └── status_sila.sh
│   ├── correct_paths.py
│   ├── create_domain_module.py
│   ├── create_schema.py
│   ├── create_schema_targeted.py
│   ├── daily_audit.sh
│   ├── db_backup.sh
│   ├── db_compose_env.sh
│   ├── db_diagnostico.sql
│   ├── db_reset_full.sh
│   ├── db_restore.sh
│   ├── dependency_audit.py
│   ├── deploy
│   │   ├── START_NGINX.sh
│   │   ├── package.sh
│   │   └── quick_deploy.sh
│   ├── dev
│   │   ├── advanced_project_analyzer.sh
│   │   ├── load_runtime_env.sh
│   │   ├── master-index.sh
│   │   ├── orphan_cleaner.py
│   │   ├── print_runtime_status.sh
│   │   ├── print_runtime_urls.sh
│   │   ├── project_analyzer.sh
│   │   ├── run_local.sh
│   │   └── start_frontend_dev.sh
│   ├── diagnostico_sila.sh
│   ├── domain_overlap_analysis.py
│   ├── educacao_reconciliation.py
│   ├── essential
│   │   └── check_credentials.py
│   ├── fase5_assessment.py
│   ├── final_status_report.py
│   ├── fix_npm_workspaces.sh
│   ├── fix_router_imports.py
│   ├── generate-autonomy-report.py
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
│   ├── homologation_institucional.py
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
│   ├── migration-guardrail.sh
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
│   ├── normalize_base_imports.py
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
│   ├── post-mutation-pipeline.sh
│   ├── print_test_db_url.py
│   ├── provider_readiness_audit.sh
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
│   ├── run_idempotency_middleware_tests.py
│   ├── run_permission_tests.sh
│   ├── run_race_tests.py
│   ├── safe_fixers.sh
│   ├── scan_integrity.py
│   ├── seed_admin_user.py
│   ├── seed_provider_operations.py
│   ├── seed_test_db.sh
│   ├── setup
│   │   ├── FASE_3_2_QUICKSTART.sh
│   │   ├── init_database.sh
│   │   ├── init_live_session.sh
│   │   ├── quick-start.sh
│   │   ├── setup_admin.sql
│   │   └── validate-setup.sh
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
│   │   ├── test_passo_13_14.sh
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
├── sila_platform
│   ├── __init__.py
│   ├── ci
│   │   ├── backend_context.yaml
│   │   ├── endpoints.yaml
│   │   ├── run_tests.py
│   │   └── validate_py_syntax.py
│   ├── devops
│   │   ├── monitoring
│   │   │   ├── alertmanager
│   │   │   ├── grafana
│   │   │   ├── prometheus
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
│   ├── governance
│   │   ├── __init__.py
│   │   ├── approval_chain
│   │   │   ├── __init__.py
│   │   │   └── engine.py
│   │   ├── audit
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── bootstrap.py
│   │   ├── delegation
│   │   │   ├── __init__.py
│   │   │   └── engine.py
│   │   ├── digital_signature
│   │   │   ├── __init__.py
│   │   │   └── engine.py
│   │   ├── module.yaml
│   │   ├── organization
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── rbac
│   │   │   ├── __init__.py
│   │   │   ├── policies.py
│   │   │   └── roles.py
│   │   ├── registry
│   │   │   ├── __init__.py
│   │   │   └── catalog.py
│   │   ├── tenancy
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── territory
│   │   │   ├── __init__.py
│   │   │   ├── constants.py
│   │   │   ├── models.py
│   │   │   └── service.py
│   │   └── workflows
│   │       ├── __init__.py
│   │       └── engine.py
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
│   │       └── postgres
│   ├── interoperability
│   │   ├── __init__.py
│   │   ├── consent_management
│   │   │   ├── __init__.py
│   │   │   └── manager.py
│   │   ├── document_exchange
│   │   │   ├── __init__.py
│   │   │   └── manager.py
│   │   ├── event_bus
│   │   │   ├── __init__.py
│   │   │   └── bus.py
│   │   ├── process_catalog
│   │   │   ├── README.md
│   │   │   ├── __init__.py
│   │   │   └── catalog.py
│   │   ├── process_manager
│   │   │   ├── __init__.py
│   │   │   └── engine.py
│   │   ├── service_registry
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── workflow_orchestrator
│   │   │   ├── __init__.py
│   │   │   └── engine.py
│   │   └── workflows.py
│   └── storage
│       ├── data
│       │   ├── clientes.csv
│       │   └── examples
│       └── media
├── storage
│   └── logs
│       └── xroad_audit.chain
├── tailwind.config.js
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
│   ├── educacao
│   │   └── test_race_condition.py
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
│   ├── test_automation_e2e.py
│   ├── test_database_integrity.py
│   ├── test_dedup.py
│   ├── test_dlq_worker.py
│   ├── test_domain_transfer_automation.py
│   ├── test_educacao_marketplace_matching_endpoint.py
│   ├── test_educacao_marketplace_search_endpoint.py
│   ├── test_educacao_vacancies_endpoint.py
│   ├── test_eligibility_engine.py
│   ├── test_foundation_audit_events.py
│   ├── test_foundation_educacao_repository.py
│   ├── test_foundation_idempotency.py
│   ├── test_foundation_search.py
│   ├── test_hierarchy_service_endpoints.py
│   ├── test_instant_transfer_e2e.py
│   ├── test_instant_transfer_stub.py
│   ├── test_institutional_catalog_blueprint.py
│   ├── test_matching.py
│   ├── test_message_bus_dlq.py
│   ├── test_modules_real.py
│   ├── test_openai_client.py
│   ├── test_operational_state_machine.py
│   ├── test_operations_service.py
│   ├── test_orchestration.py
│   ├── test_orchestrator_retry_dlq.py
│   ├── test_passo_6_concurrent_locks.py
│   ├── test_passo_7_transfer_transaction.py
│   ├── test_phase3_integration.py
│   ├── test_phase_18_2_alerts_anomaly.py
│   ├── test_phase_18_3_orchestration.py
│   ├── test_phase_19_event_bus.py
│   ├── test_phase_19_event_bus_simple.py
│   ├── test_phase_20_1_db_persistence.py
│   ├── test_phase_20_2_bridge.py
│   ├── test_phase_20_2_extension_bridge.py
│   ├── test_phase_20_event_sourcing.py
│   ├── test_policy_and_dlq.py
│   ├── test_policy_engine.py
│   └── test_vacancy_marketplace.py
├── tmp
│   ├── scripts
│   └── tmp_audit.db
└── tools
    ├── apply_extend_existing.py
    ├── autoheal_imports.py
    ├── check_location_import.py
    ├── ci_import_check.py
    ├── cleanup_saude_refs.py
    ├── codegen
    │   ├── create_sample_csv.py
    │   ├── generate_module.py
    │   ├── generate_phase2_docs.py
    │   ├── sample.csv
    │   ├── templates.py
    │   └── utils.py
    ├── consistency
    │   ├── check_env_files.py
    │   ├── check_imports.py
    │   └── check_paths.py
    ├── discover_auth_imports.py
    ├── heal_identity_bridge.py
    ├── migrate_all_modules.py
    ├── migrate_module.py
    ├── policies
    │   └── scan_hardcoded.py
    ├── refactor
    │   └── update_paths.py
    ├── repair_imports_ast.py
    ├── run_separation_demo.sh
    ├── split_models_schemas.py
    ├── sqlite_removal_automation.py
    ├── test_separation_system.py
    ├── validate_separation.py
    └── validators
        └── dependency_checker.py

255 directories, 845 files
dev03wsl@Rochete-consultoria:~/sila-system$