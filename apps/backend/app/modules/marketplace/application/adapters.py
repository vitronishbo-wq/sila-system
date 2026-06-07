from __future__ import annotations

import os
import uuid
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
    InstitutionCapacityModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.institution_marketplace_projection_model import (
    InstitutionMarketplaceProjectionModel,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.sqlalchemy_capacity_repository import (
    SQLAlchemyCapacityRepository,
)
from apps.backend.app.modules.payment.domain.models.payment import Payment as ProviderPayment
from apps.backend.app.modules.payment.infrastructure.adapters.generic_payment_provider_adapter import (
    GenericPaymentProviderAdapter,
)
from apps.backend.app.foundation.transactional.core import TransferTransactionalEngine
from apps.backend.app.foundation.transactional.adapters.sqlalchemy_capacity_adapter import (
    SQLAlchemyCapacityReservationAdapter,
)
from apps.backend.app.foundation.transactional.adapters.sqlalchemy_enrollment_adapter import (
    SQLAlchemyEnrollmentStateMachineAdapter,
)
from foundation.matching.engine import InstitutionProfile, MatchingEngine, StudentProfile


class MatchingAdapter:
    def __init__(self, selected_institution: Optional[str] = None):
        self.selected_institution = selected_institution

    async def find_best_match(self, student_profile: dict) -> Optional[str]:
        return self.selected_institution


class ReservationAdapter:
    def __init__(self):
        self.reservations: Dict[str, Dict[str, Any]] = {}

    async def reserve(self, institution_id: str, student_id: str, ttl: int = 0) -> Dict[str, Any]:
        res_id = f"res_{institution_id}_{student_id}"
        self.reservations[res_id] = {"institution_id": institution_id, "student_id": student_id, "released": False}
        return {"reservation_id": res_id, "status": "reserved"}

    async def release(self, reservation_id: str) -> Dict[str, Any]:
        if reservation_id in self.reservations:
            self.reservations[reservation_id]["released"] = True
            return {"reservation_id": reservation_id, "status": "released"}
        return {"reservation_id": reservation_id, "status": "not_found"}


class RealMatchingAdapter(MatchingAdapter):
    def __init__(self, session: AsyncSession, max_results: int = 1):
        self.session = session
        self.engine = MatchingEngine()
        self.max_results = max_results

    async def find_best_match(self, student_profile: dict) -> Optional[str]:
        if not student_profile:
            return None

        profile = StudentProfile(
            student_id=student_profile.get("student_id", ""),
            age=int(student_profile.get("age", 18)),
            academic_performance=float(student_profile.get("academic_performance", 0.0)),
            special_needs=student_profile.get("special_needs", []) or [],
            location=student_profile.get(
                "location",
                {"province": "", "municipality": "", "district": ""},
            ),
            available_budget=float(student_profile.get("available_budget", 0.0)),
            preferred_modalities=student_profile.get("preferred_modalities", []) or [],
            educational_level=student_profile.get("educational_level"),
            previous_transfers=int(student_profile.get("previous_transfers", 0)),
        )

        stmt = select(InstitutionMarketplaceProjectionModel).where(
            InstitutionMarketplaceProjectionModel.is_active == True
        )
        result = await self.session.execute(stmt)
        institution_models = result.scalars().all()

        institution_profiles: list[InstitutionProfile] = []
        for model in institution_models:
            institution_profiles.append(
                InstitutionProfile(
                    institution_id=str(model.institution_id),
                    name=model.name,
                    type=model.type,
                    location={
                        "province": model.province,
                        "municipality": model.municipality,
                        "district": model.district,
                    },
                    available_slots=model.available_slots,
                    monthly_fee=model.monthly_fee_avg,
                    rating=model.rating,
                    approval_rate=model.approval_rate,
                    academic_performance=model.average_academic_performance,
                    specializations=model.specializations,
                    supports_special_needs=model.supports_special_needs,
                    special_needs_types=model.special_needs_types,
                    teaching_modalities=model.teaching_modalities,
                    transfer_acceptance_rate=model.transfer_acceptance_rate,
                )
            )

        matches = await self.engine.find_matches(
            session=self.session,
            student=profile,
            institutions=institution_profiles,
            max_results=self.max_results,
        )

        return matches[0].institution_id if matches else None


class RealReservationAdapter(ReservationAdapter):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.capacity_repo = SQLAlchemyCapacityRepository(session)

    async def reserve(self, institution_id: str, student_id: str, ttl: int = 0) -> Dict[str, Any]:
        if isinstance(institution_id, str):
            institution_id = UUID(institution_id)

        stmt = (
            select(InstitutionCapacityModel)
            .where(
                InstitutionCapacityModel.institution_id == institution_id,
                InstitutionCapacityModel.capacity_total
                - InstitutionCapacityModel.capacity_used
                - InstitutionCapacityModel.capacity_reserved
                >= 1,
            )
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        model = result.scalars().first()
        if not model:
            return {"reservation_id": None, "status": "no_availability"}

        reserved = await self.capacity_repo.reserve_capacity(
            institution_id=model.institution_id,
            grade=model.grade,
            shift=model.shift,
            quantity=1,
        )
        if not reserved:
            return {"reservation_id": None, "status": "no_availability"}

        return {
            "reservation_id": str(reserved["id"]),
            "status": "reserved",
            "institution_id": str(institution_id),
            "grade": reserved["grade"],
            "shift": reserved["shift"],
            "available": reserved["capacity_total"]
            - reserved["capacity_used"]
            - reserved["capacity_reserved"],
        }

    async def release(self, reservation_id: str) -> Dict[str, Any]:
        try:
            reservation_uuid = UUID(reservation_id)
        except ValueError:
            return {"reservation_id": reservation_id, "status": "invalid_id"}

        released = await self.capacity_repo.release_capacity(reservation_uuid, 1)
        if not released:
            return {"reservation_id": reservation_id, "status": "not_found"}

        return {
            "reservation_id": reservation_id,
            "status": "released",
            "capacity_reserved": released.get("capacity_reserved"),
        }


class PaymentAdapter:
    def __init__(self, fail_charge: bool = False, fail_refund: bool = False):
        self.fail_charge = fail_charge
        self.fail_refund = fail_refund
        self.charges: Dict[str, Dict[str, Any]] = {}

    async def charge(self, amount: float, method: Optional[str], txn_id: str) -> Dict[str, Any]:
        if self.fail_charge:
            raise Exception("payment_declined")
        pid = f"pay_{txn_id}"
        self.charges[pid] = {"amount": amount, "method": method}
        return {"payment_id": pid, "status": "paid"}

    async def refund(self, payment_id: str) -> Dict[str, Any]:
        if self.fail_refund:
            raise Exception("refund_failed")
        if payment_id in self.charges:
            return {"payment_id": payment_id, "status": "refunded"}
        return {"payment_id": payment_id, "status": "not_found"}


class TransferAdapter:
    def __init__(self, fail_execute: bool = False):
        self.fail_execute = fail_execute

    async def execute(
        self,
        student_id: str,
        institution_id: str,
        reservation_id: Optional[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self.fail_execute:
            raise Exception("transfer_failed")
        tid = f"tr_{student_id}_{institution_id}"
        return {"transfer_id": tid, "status": "enrolled"}


class RealPaymentAdapter(PaymentAdapter):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.provider = GenericPaymentProviderAdapter(
            api_key=os.getenv("PAYMENT_PROVIDER_API_KEY", ""),
            api_secret=os.getenv("PAYMENT_PROVIDER_API_SECRET", ""),
            endpoint=os.getenv("PAYMENT_PROVIDER_ENDPOINT", ""),
        )

    async def charge(self, amount: float, method: Optional[str], txn_id: str) -> Dict[str, Any]:
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        payment = ProviderPayment(id=txn_id, reference=f"PAY-{txn_id}")
        authorization = await self.provider.authorize(payment)
        capture = await self.provider.capture(authorization["provider_reference"])

        return {
            "payment_id": capture["provider_reference"],
            "status": capture["status"],
            "provider_reference": authorization["provider_reference"],
            "amount": amount,
            "method": method,
        }

    async def refund(self, payment_id: str) -> Dict[str, Any]:
        return await self.provider.refund(payment_id)


class RealTransferAdapter(TransferAdapter):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.engine = TransferTransactionalEngine(
            capacity=SQLAlchemyCapacityReservationAdapter(session),
            enrollment_sm=SQLAlchemyEnrollmentStateMachineAdapter(session),
        )

    async def execute(
        self,
        student_id: str,
        institution_id: str,
        reservation_id: Optional[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        metadata = metadata or {}
        grade = metadata.get("grade")
        shift = metadata.get("shift")
        current_enrollment_id = metadata.get("current_enrollment_id")
        actor_id = metadata.get("actor_id")

        if not all([grade, shift, current_enrollment_id, actor_id]):
            raise ValueError(
                "Transfer metadata must include current_enrollment_id, grade, shift, and actor_id"
            )

        if isinstance(institution_id, str):
            institution_id = UUID(institution_id)
        if isinstance(current_enrollment_id, str):
            current_enrollment_id = UUID(current_enrollment_id)
        if isinstance(actor_id, str):
            actor_id = UUID(actor_id)

        payload = {
            "institution_id": institution_id,
            "grade": grade,
            "shift": shift,
            "current_enrollment_id": current_enrollment_id,
            "actor_id": actor_id,
            "academic_year": metadata.get("academic_year"),
            "reason": metadata.get("reason"),
        }

        async with self.session.begin():
            return await self.engine.execute_transfer(
                self.session,
                payload,
                idempotency_key=reservation_id or str(uuid.uuid4()),
            )


class NotificationAdapter:
    async def send(self, student_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        nid = f"not_{student_id}"
        return {"notification_id": nid, "status": "sent"}
