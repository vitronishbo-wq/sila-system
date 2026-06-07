from __future__ import annotations

import uuid
import logging
from typing import Optional

from .dto import (
    InstantTransferRequestDTO,
    InstantTransferResponseDTO,
    StepResultDTO,
)
from .adapters import (
    MatchingAdapter,
    ReservationAdapter,
    PaymentAdapter,
    TransferAdapter,
    NotificationAdapter,
)
from ..infrastructure.redis_store import InMemoryOrchestrationStore

logger = logging.getLogger(__name__)


class InstantTransferOrchestrator:
    def __init__(
        self,
        matching: MatchingAdapter,
        reservation: ReservationAdapter,
        payment: PaymentAdapter,
        transfer: TransferAdapter,
        notification: NotificationAdapter,
        store: Optional[InMemoryOrchestrationStore] = None,
        ttl_seconds: int = 7 * 24 * 3600,
    ):
        self.matching = matching
        self.reservation = reservation
        self.payment = payment
        self.transfer = transfer
        self.notification = notification
        self.store = store or InMemoryOrchestrationStore(ttl_seconds)

    async def orchestrate(self, payload: InstantTransferRequestDTO, idempotency_key: Optional[str] = None) -> InstantTransferResponseDTO:
        txn_id = idempotency_key or str(uuid.uuid4())

        # Idempotency: return stored final response if available
        existing = await self.store.get(txn_id)
        if existing:
            return InstantTransferResponseDTO(**existing["response"])

        state: dict = {"txn_id": txn_id, "status": "IN_PROGRESS", "steps": {}}
        # Persist initial state
        await self.store.set(txn_id, {"response": {"status": "IN_PROGRESS", "transaction_id": txn_id, "steps": {}}}, ttl_seconds=0)

        selected_institution = None
        reservation_id = None
        payment_id = None

        try:
            # Matching
            if payload.preferred_institution_id:
                selected_institution = payload.preferred_institution_id
                state["steps"]["matching"] = {"status": "skipped", "detail": {"institution_id": selected_institution}}
            else:
                sp = payload.student_profile.dict() if payload.student_profile else {}
                selected_institution = await self.matching.find_best_match(sp)
                if not selected_institution:
                    raise Exception("no_match_found")
                state["steps"]["matching"] = {"status": "ok", "detail": {"institution_id": selected_institution}}

            # Eligibility (assume ok for scaffolding)
            state["steps"]["eligibility"] = {"status": "ok"}

            # Reservation
            res = await self.reservation.reserve(selected_institution, payload.student_id)
            reservation_id = res.get("reservation_id")
            state["steps"]["reservation"] = {"status": "ok", "detail": res}

            # Payment
            pay = await self.payment.charge(payload.amount or 0.0, payload.payment_method, txn_id)
            payment_id = pay.get("payment_id")
            state["steps"]["payment"] = {"status": "ok", "detail": pay}

            # Transfer / Enrollment
            tr = await self.transfer.execute(
                payload.student_id,
                selected_institution,
                reservation_id,
                payload.metadata,
            )
            state["steps"]["transfer"] = {"status": "ok", "detail": tr}

            # Notification
            note = await self.notification.send(payload.student_id, {"transfer": tr, "payment": pay})
            state["steps"]["notification"] = {"status": "ok", "detail": note}

            response = {
                "status": "success",
                "transfer_id": tr.get("transfer_id"),
                "transaction_id": txn_id,
                "steps": {k: v for k, v in state["steps"].items()},
            }

            # Persist final response
            await self.store.set(txn_id, {"response": response}, ttl_seconds=0)

            return InstantTransferResponseDTO(**response)

        except Exception as e:
            logger.exception("orchestration failed: %s", e)
            # Compensation logic
            try:
                if payment_id:
                    try:
                        await self.payment.refund(payment_id)
                        state["steps"]["payment"] = {"status": "refunded", "detail": {"payment_id": payment_id}}
                    except Exception as refund_err:
                        # Mark compensating state and record error
                        state["steps"]["payment"] = {"status": "refund_failed", "detail": {"error": str(refund_err)}}
                        await self.store.set(txn_id, {"response": {"status": "compensating", "transaction_id": txn_id, "steps": state["steps"]}}, ttl_seconds=0)
                        raise

                if reservation_id:
                    await self.reservation.release(reservation_id)
                    state["steps"]["reservation"] = {"status": "released", "detail": {"reservation_id": reservation_id}}

            except Exception as comp_exc:
                logger.exception("compensation failed: %s", comp_exc)
                # Persist state with explicit compensation error
                await self.store.set(txn_id, {"response": {"status": "compensation_failed", "transaction_id": txn_id, "steps": state["steps"]}}, ttl_seconds=0)
                raise

            # Persist failed response
            resp = {"status": "failed", "transfer_id": None, "transaction_id": txn_id, "steps": state["steps"]}
            await self.store.set(txn_id, {"response": resp}, ttl_seconds=0)
            raise
