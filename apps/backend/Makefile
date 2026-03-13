SHELL := /usr/bin/env bash

.PHONY: seed-test-db audit-integration audit-integration-local

seed-test-db:
	@echo "[Seed] Preparando dataset minimo para testes de integracao..."
	@RUN_DB_INTEGRATION=1 bash ../../scripts/seed_test_db.sh

audit-integration: seed-test-db
	@echo "[Audit] Executando testes de integracao (DB/hierarchy)..."
	@RUN_DB_INTEGRATION=1 PYTHONPATH=apps/backend python -m pytest \
		tests/test_database_integrity.py \
		tests/test_hierarchy_service_endpoints.py -q

audit-integration-local:
	@echo "[Seed] Preparando dataset minimo para testes de integracao (local)..."
	@PGPASSWORD=postgres psql -h localhost -U postgres -d sila_db -f apps/backend/seeds/seed_integration_minimal.sql
	@echo "[Audit] Executando testes de integracao (DB/hierarchy)..."
	@RUN_DB_INTEGRATION=1 PYTHONPATH=apps/backend python -m pytest \
		tests/test_database_integrity.py \
		tests/test_hierarchy_service_endpoints.py -q
