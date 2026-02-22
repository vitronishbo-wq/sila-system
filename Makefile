PYTEST=python -m pytest

.PHONY: lint typecheck test-coverage validate-migrations

lint:
	flake8

typecheck:
	mypy apps/backend/app || true

test-coverage:
	$(PYTEST) --cov=apps/backend/app --cov-report=term --cov-report=html:coverage_html_report --cov-fail-under=80

validate-migrations:
	python scripts/validate_migrations.py
