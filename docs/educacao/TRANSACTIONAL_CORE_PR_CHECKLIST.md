# PR Checklist — Transactional Core Extraction

- [ ] RFC present and linked: `docs/educacao/TRANSACTIONAL_CORE_RFC.md` and `docs/educacao/TRANSACTIONAL_CORE_SPEC.md` (if provided)
- [ ] New files under `apps/backend/app/foundation/transactional` follow package conventions and import only ports
- [ ] No circular imports introduced between `foundation` and `modules` packages
- [ ] Adapters wrap existing repositories without changing behavior (no direct `session.commit()` in adapters)
- [ ] All existing tests in `apps/backend/app/modules/educacao/tests` pass locally
- [ ] New unit tests added for `EnrollmentStateMachine` and `CapacityReservationAdapter`
- [ ] Concurrency tests demonstrating no overbooking added (at least one high-contention test)
- [ ] Idempotency behavior documented and verified (idempotency_key handling)
- [ ] Outbox and audit continuations are preserved inside UoW
- [ ] Performance implications considered (lock order documented)
- [ ] Migration guide included in RFC for rolling update strategy
- [ ] PR description links to RFC and provides step-by-step migration plan
- [ ] Code formatted and linters pass (`ruff`, `black`) where applicable
- [ ] CHANGELOG entry drafted for the module refactor
