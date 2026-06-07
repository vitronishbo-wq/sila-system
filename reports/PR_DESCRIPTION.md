Title: Feature/eligibility-engine + orchestration and audit

Summary:
- Implemented a Foundation Eligibility Engine with realistic rules (age, debt, vacancy).
- Exposed POST /educacao/eligibility/transfer in `apps/api_gateway/eligibility.py`.
- Integrated `VacancyMarketplace` capacity lookup when missing.
- Added an in-memory `Orchestrator` with retries and a simple DLQ.
- Added `AutomationEngine` to evaluate, audit and schedule transfers.
- Added audit logging for transfer requests and executions in the `audit_events` database table.
- Added tests covering eligibility rules, orchestration flow and DLQ behavior.

Files added/modified (key files):
- domain/academic_identity.py
- domain/eligibility_rule.py
- domain/transfer_policy.py
- domain/vacancy_marketplace.py
- domain/institution_capacity.py
- domain/academic_status.py
- domain/transfer_automation.py (audit integration)
- domain/enrollment_automation.py
- foundation/eligibility/engine.py
- foundation/eligibility/evaluator.py
- foundation/eligibility/rules.py
- foundation/eligibility/scoring.py
- foundation/eligibility/conditions.py
- foundation/eligibility/audit.py
- foundation/orchestration/orchestrator.py (retries + DLQ)
- foundation/automation/automator.py
- apps/api_gateway/eligibility.py
- apps/api_gateway/main.py
- tests/test_eligibility_engine.py
- tests/test_orchestration.py
- tests/test_orchestrator_retry_dlq.py

Testing notes:
- Unit tests added: run `pytest -q tests/test_eligibility_engine.py` (4 tests).
- Orchestration tests: `pytest -q tests/test_orchestration.py` and `pytest -q tests/test_orchestrator_retry_dlq.py`.
- Quick server smoke test:
  1. `pip install fastapi uvicorn` (project venv recommended)
  2. `python -m apps.api_gateway.main`
  3. POST JSON to `http://127.0.0.1:8000/educacao/eligibility/transfer` (example in PR body).

Audit & DLQ artifacts:
- Eligibility audit events: `audit_events` database table
- Orchestrator DLQ: `reports/orchestrator_dlq.log` (JSON lines)

Backward compatibility / Migration:
- This change introduces new foundation modules. They are additive and isolated under `foundation/` and `domain/`. No breaking changes expected.

Security / Compliance notes:
- Audit logs contain request/response payloads. Ensure `reports/` is protected and rotated according to retention policies.

Next steps (recommendations):
- Replace the in-memory `Orchestrator` with a durable worker (Celery/RQ/Kafka) for production.
- Implement fine-grained policy configurations (per-institution rules) and RBAC around automation triggers.
- Add end-to-end integration tests with mock services for capacity, identity and payment.
