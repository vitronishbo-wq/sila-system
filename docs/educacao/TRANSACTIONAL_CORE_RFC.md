RFC: Transactional Transfer & Enrollment Core
===========================================

Date: 2026-05-27

Context
-------

We audited the `apps/backend/app/modules/educacao` transactional code (transfer pipeline, enrollment, capacity repos). There is existing use of `AsyncSession` transaction boundaries and pessimistic locks (`FOR UPDATE`) across repositories. This RFC proposes an incremental consolidation into a reusable foundation core.

Goals
-----

- Consolidate transfer orchestration into a transactional core (`foundation.transactional.transfer`).
- Provide an `EnrollmentStateMachine` for canonical enrollment transitions.
- Provide a `CapacityReservationEngine` to centralize seat reservations, TTL/leases and `FOR UPDATE` semantics.
- Preserve outbox semantics and audit integration inside the same UoW.

Sequence (high-level)
---------------------

1. API receives transfer request and builds `payload` + `idempotency_key`.
2. Service opens `AsyncSession` and calls `TransferTransactionalPort.execute_transfer(session, payload, idempotency_key)`.
3. Core acquires pessimistic locks (via `CapacityReservationPort` / turma repository) and validates business invariants.
4. Core uses `EnrollmentStateMachinePort.transition(...)` to move origin enrollment to `TRANSFERRED` and create new `ACTIVE` enrollment atomically.
5. Core writes `TransferModel`/domain artifacts, persists outbox events and audit events, then commits UoW.
6. Core returns canonical receipt and transfer id.

Ports / Signatures (sketch)
---------------------------

```
class TransferTransactionalPort(Protocol):
    async def execute_transfer(self, session: AsyncSession, payload: dict, idempotency_key: str) -> dict: ...

class EnrollmentStateMachinePort(Protocol):
    async def transition(self, session: AsyncSession, enrollment_id: UUID, event: str, actor_id: UUID) -> dict: ...

class CapacityReservationPort(Protocol):
    async def reserve(self, session: AsyncSession, turma_id: UUID, qty:int=1, for_update:bool=True) -> dict: ...
    async def release(self, session: AsyncSession, reservation_id: UUID) -> None: ...
    async def get_available(self, session: AsyncSession, turma_id: UUID) -> int: ...
```

Milestones (incremental)
------------------------

1. RFC + ports (this doc). (done)
2. Implement ports stubs and core skeleton in `foundation.transactional`. (this PR)
3. Implement `CapacityReservationEngine` adapter reusing `sqlalchemy_capacity_repository` logic.
4. Extract `EnrollmentStateMachine` and refactor `matricula_service` and `transfer` services to use it.
5. Implement `TransferTransactionalEngine` and adapt `transfer_transaction_service` to delegate.
6. Run concurrency tests and daily-audit; tune locking/timeouts.

Testing strategy
----------------

- Unit tests for ports and state machine transitions.
- Integration tests that run the transfer flow end-to-end using test DB.
- Concurrency stress tests asserting no overbooking using multiple parallel tasks.

Migration notes
---------------

- Start by adding adapters that wrap current repositories (no behavior change). Then progressively change services to call the core.
- Avoid circular imports: foundation must depend on ports only; modules implement ports.

Risks
-----

- Accidentally changing commit/rollback patterns: ensure adapters do not call `session.commit()` directly.
- Deadlocks if locks order is inconsistent — define canonical lock order (e.g., turma then enrollment then capacity rows).

Estimated effort
----------------

- TASK-010: 13h
- TASK-011: 10h
- TASK-012: 10h

---

