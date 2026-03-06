PYTEST=python -m pytest

.PHONY: lint typecheck test-coverage validate-migrations test-statistics-block run-obras-worker k8s-obras-sovereign architecture-scan architecture-guardrails architecture-guardrails-core architecture-guardrails-integration architecture-guardrails-legacy architecture-guardrails-dry architecture-report migration-domain-report

lint:
	flake8

typecheck:
	mypy apps/backend/app || true

test-coverage:
	$(PYTEST) --cov=apps/backend/app --cov-report=term --cov-report=html:coverage_html_report --cov-fail-under=80

validate-migrations:
	python scripts/validate_migrations.py

test-statistics-block:
	bash apps/backend/scripts/run_statistics_block_tests.sh

run-obras-worker:
	cd apps/backend && python -m app.modules.obras_publicas.infrastructure.messaging.runner

k8s-obras-sovereign:
	kubectl apply -f infrastructure/k8s/obras-publicas-outbox-worker.yaml
	kubectl apply -f infrastructure/k8s/obras-publicas-worker-hpa.yaml
	kubectl apply -f infrastructure/multi-region/kafka/mirrormaker2.yaml
	kubectl apply -f infrastructure/dr/walg-backup-cronjob.yaml

architecture-scan:
	python apps/backend/tools/architecture/run_analysis.py

architecture-guardrails:
	bash scripts/run_guardrails.sh

architecture-guardrails-core:
	GUARDRAILS_PHASE=core bash scripts/run_guardrails.sh

architecture-guardrails-integration:
	GUARDRAILS_PHASE=integration bash scripts/run_guardrails.sh

architecture-guardrails-legacy:
	GUARDRAILS_PHASE=legacy bash scripts/run_guardrails.sh

architecture-guardrails-dry:
	REFACTOR_DRY_RUN=1 SKIP_TESTS=1 bash scripts/run_guardrails.sh

architecture-report:
	python3 scripts/guardrails/check_core_namespace.py --root apps/backend
	python3 scripts/guardrails/check_module_registry_sync.py --modules-root apps/backend/app/modules
	python3 scripts/guardrails/check_architecture_guide_sync.py
	python3 scripts/domain_overlap_analysis.py --modules-root apps/backend/app/modules --output reports/domain_overlap_report.md
	python3 scripts/module_dependency_analysis.py --modules-root apps/backend/app/modules --output-md reports/module_dependencies.md --output-json reports/module_dependency_graph.json
	python3 scripts/architecture_map_report.py --modules-root apps/backend/app/modules --dependency-json reports/module_dependency_graph.json --output reports/architecture_map.md
	python3 scripts/module_health_report.py --modules-root apps/backend/app/modules --tests-root apps/backend/tests/modules --dependency-json reports/module_dependency_graph.json --output reports/module_health_report.md
	python3 scripts/migration_domain_inventory.py --output reports/migration_domain_inventory.md

migration-domain-report:
	python3 scripts/migration_domain_inventory.py --output reports/migration_domain_inventory.md
